import json
from http import HTTPStatus
from http.server import (
    BaseHTTPRequestHandler,
    ThreadingHTTPServer,
)
from typing import Any
from urllib.parse import urlsplit
from uuid import uuid4

from heyti.gateway.http_application import (
    HeytiHttpApplication,
)
from heyti.security.http_application import (
    AuthenticatedSessionRequiredError,
    InvalidCredentialsError,
    PasswordChangeRequiredError,
    SecurityHttpApplication,
)


DEFAULT_ALLOWED_ORIGINS = (
    "http://127.0.0.1:5173",
    "http://localhost:5173",
)
MAX_REQUEST_BODY_BYTES = 64 * 1024


def create_http_server(
    application: HeytiHttpApplication,
    host: str = "127.0.0.1",
    port: int = 8765,
    allowed_origins: tuple[str, ...] = DEFAULT_ALLOWED_ORIGINS,
    knowledge_version: str | None = None,
    security_application: SecurityHttpApplication | None = None,
    require_authenticated_operations: bool = False,
) -> ThreadingHTTPServer:
    """
    Construye el servidor HTTP local de HEYTI.

    No inicia el ciclo serve_forever. El llamador conserva
    el control explícito sobre inicio, apagado y ciclo de vida.
    """

    if not isinstance(application, HeytiHttpApplication):
        raise TypeError(
            "application debe ser HeytiHttpApplication"
        )

    if (
        security_application is not None
        and not isinstance(
            security_application,
            SecurityHttpApplication,
        )
    ):
        raise TypeError(
            "security_application debe ser "
            "SecurityHttpApplication"
        )

    if not isinstance(
        require_authenticated_operations,
        bool,
    ):
        raise TypeError(
            "require_authenticated_operations debe ser bool"
        )

    if (
        require_authenticated_operations
        and security_application is None
    ):
        raise ValueError(
            "La proteccion operativa requiere "
            "security_application"
        )

    normalized_origins = frozenset(
        origin.rstrip("/")
        for origin in allowed_origins
        if isinstance(origin, str) and origin.strip()
    )

    operational_paths = frozenset({
        "/v1/sections/describe",
        "/v1/universes/describe",
        "/v1/field/describe",
    })

    class HeytiRequestHandler(BaseHTTPRequestHandler):
        server_version = "HEYTI-HTTP/0.1"

        def log_message(
            self,
            format: str,
            *args: Any,
        ) -> None:
            """Evita escribir solicitudes en stderr por defecto."""

        def _request_path(self) -> str:
            return urlsplit(self.path).path

        def _origin(self) -> str | None:
            origin = self.headers.get("Origin")

            if origin is None:
                return None

            return origin.rstrip("/")

        def _origin_is_allowed(self) -> bool:
            origin = self._origin()

            return (
                origin is None
                or origin in normalized_origins
            )

        def _bearer_token(self) -> str:
            authorization = self.headers.get(
                "Authorization",
                "",
            ).strip()

            scheme, separator, token = (
                authorization.partition(" ")
            )
            token = token.strip()

            if (
                scheme.lower() != "bearer"
                or not separator
                or not token
                or " " in token
            ):
                raise AuthenticatedSessionRequiredError(
                    "Se requiere una sesion autenticada"
                )

            return token

        def _send_json(
            self,
            status: HTTPStatus,
            payload: dict[str, Any],
        ) -> None:
            body = json.dumps(
                payload,
                ensure_ascii=False,
                allow_nan=False,
            ).encode("utf-8")

            self.send_response(status.value)
            self.send_header(
                "Content-Type",
                "application/json; charset=utf-8",
            )
            self.send_header(
                "Content-Length",
                str(len(body)),
            )
            self.send_header(
                "Cache-Control",
                "no-store",
            )

            origin = self._origin()

            if (
                origin is not None
                and origin in normalized_origins
            ):
                self.send_header(
                    "Access-Control-Allow-Origin",
                    origin,
                )
                self.send_header(
                    "Vary",
                    "Origin",
                )

            self.end_headers()

            if self.command != "HEAD":
                self.wfile.write(body)

        def _send_error_contract(
            self,
            status: HTTPStatus,
            code: str,
            message: str,
        ) -> None:
            self._send_json(
                status,
                {
                    "error": {
                        "code": code,
                        "message": message,
                    }
                },
            )

        def _reject_disallowed_origin(self) -> bool:
            if self._origin_is_allowed():
                return False

            self._send_error_contract(
                HTTPStatus.FORBIDDEN,
                "ORIGIN_NOT_ALLOWED",
                "El origen de la solicitud no está permitido.",
            )
            return True

        def _read_json_body(self) -> dict[str, Any]:
            content_type = self.headers.get(
                "Content-Type",
                "",
            ).split(";", 1)[0].strip().lower()

            if content_type != "application/json":
                raise TypeError(
                    "Content-Type debe ser application/json"
                )

            raw_length = self.headers.get(
                "Content-Length",
                "",
            )

            try:
                content_length = int(raw_length)
            except ValueError as exc:
                raise ValueError(
                    "Content-Length inválido"
                ) from exc

            if content_length <= 0:
                raise ValueError(
                    "El cuerpo JSON es obligatorio"
                )

            if content_length > MAX_REQUEST_BODY_BYTES:
                raise OverflowError(
                    "El cuerpo excede el límite permitido"
                )

            raw_body = self.rfile.read(content_length)

            try:
                payload = json.loads(
                    raw_body.decode("utf-8")
                )
            except (
                UnicodeDecodeError,
                json.JSONDecodeError,
            ) as exc:
                raise ValueError(
                    "El cuerpo no contiene JSON válido"
                ) from exc

            if not isinstance(payload, dict):
                raise ValueError(
                    "El cuerpo JSON debe ser un objeto"
                )

            return payload

        def do_OPTIONS(self) -> None:
            if self._reject_disallowed_origin():
                return

            allowed_paths = {
                "/health",
                "/v1/sections/describe",
                "/v1/universes/describe",
                "/v1/field/describe",
            }

            if security_application is not None:
                allowed_paths.update({
                    "/v1/auth/login",
                    "/v1/auth/session",
                    "/v1/auth/logout",
                })

            if self._request_path() not in allowed_paths:
                self._send_error_contract(
                    HTTPStatus.NOT_FOUND,
                    "NOT_FOUND",
                    "Ruta no encontrada.",
                )
                return

            self.send_response(HTTPStatus.NO_CONTENT.value)

            origin = self._origin()

            if origin is not None:
                self.send_header(
                    "Access-Control-Allow-Origin",
                    origin,
                )
                self.send_header(
                    "Vary",
                    "Origin",
                )

            self.send_header(
                "Access-Control-Allow-Methods",
                "GET, POST, OPTIONS",
            )
            self.send_header(
                "Access-Control-Allow-Headers",
                "Content-Type, X-Request-ID, Authorization",
            )
            self.send_header(
                "Access-Control-Max-Age",
                "600",
            )
            self.end_headers()

        def do_GET(self) -> None:
            if self._reject_disallowed_origin():
                return

            path = self._request_path()

            if path == "/health":
                try:
                    payload = application.health()
                except Exception:
                    self._send_error_contract(
                        HTTPStatus.INTERNAL_SERVER_ERROR,
                        "INTERNAL_ERROR",
                        "HEYTI-CORE no pudo completar la solicitud.",
                    )
                    return

                self._send_json(
                    HTTPStatus.OK,
                    payload,
                )
                return

            if (
                path == "/v1/auth/session"
                and security_application is not None
            ):
                try:
                    token = self._bearer_token()
                    payload = (
                        security_application
                        .current_session(token)
                    )
                except AuthenticatedSessionRequiredError:
                    self._send_error_contract(
                        HTTPStatus.UNAUTHORIZED,
                        "AUTHENTICATION_REQUIRED",
                        "Se requiere una sesion autenticada.",
                    )
                    return
                except Exception:
                    self._send_error_contract(
                        HTTPStatus.INTERNAL_SERVER_ERROR,
                        "INTERNAL_ERROR",
                        "HEYTI-CORE no pudo completar la solicitud.",
                    )
                    return

                self._send_json(
                    HTTPStatus.OK,
                    payload,
                )
                return

            self._send_error_contract(
                HTTPStatus.NOT_FOUND,
                "NOT_FOUND",
                "Ruta no encontrada.",
            )

        def do_POST(self) -> None:
            if self._reject_disallowed_origin():
                return

            path = self._request_path()

            allowed_paths = set(
                operational_paths
            )

            if security_application is not None:
                allowed_paths.update({
                    "/v1/auth/login",
                    "/v1/auth/logout",
                })

            if path not in allowed_paths:
                self._send_error_contract(
                    HTTPStatus.NOT_FOUND,
                    "NOT_FOUND",
                    "Ruta no encontrada.",
                )
                return

            if path == "/v1/auth/logout":
                try:
                    token = self._bearer_token()
                    response = (
                        security_application.logout(token)
                    )
                except AuthenticatedSessionRequiredError:
                    self._send_error_contract(
                        HTTPStatus.UNAUTHORIZED,
                        "AUTHENTICATION_REQUIRED",
                        "Se requiere una sesion autenticada.",
                    )
                    return
                except Exception:
                    self._send_error_contract(
                        HTTPStatus.INTERNAL_SERVER_ERROR,
                        "INTERNAL_ERROR",
                        "HEYTI-CORE no pudo completar la solicitud.",
                    )
                    return

                self._send_json(
                    HTTPStatus.OK,
                    response,
                )
                return

            try:
                payload = self._read_json_body()
            except TypeError as exc:
                self._send_error_contract(
                    HTTPStatus.UNSUPPORTED_MEDIA_TYPE,
                    "UNSUPPORTED_MEDIA_TYPE",
                    str(exc),
                )
                return
            except OverflowError as exc:
                self._send_error_contract(
                    HTTPStatus.REQUEST_ENTITY_TOO_LARGE,
                    "REQUEST_TOO_LARGE",
                    str(exc),
                )
                return
            except ValueError as exc:
                self._send_error_contract(
                    HTTPStatus.BAD_REQUEST,
                    "INVALID_JSON",
                    str(exc),
                )
                return

            if path == "/v1/auth/login":
                try:
                    response = (
                        security_application.login(payload)
                    )
                except InvalidCredentialsError:
                    self._send_error_contract(
                        HTTPStatus.UNAUTHORIZED,
                        "INVALID_CREDENTIALS",
                        "Credenciales invalidas.",
                    )
                    return
                except PasswordChangeRequiredError:
                    self._send_error_contract(
                        HTTPStatus.FORBIDDEN,
                        "PASSWORD_CHANGE_REQUIRED",
                        "Debe cambiarse la contrasena.",
                    )
                    return
                except ValueError as exc:
                    self._send_error_contract(
                        HTTPStatus.BAD_REQUEST,
                        "INVALID_REQUEST",
                        str(exc),
                    )
                    return
                except Exception:
                    self._send_error_contract(
                        HTTPStatus.INTERNAL_SERVER_ERROR,
                        "INTERNAL_ERROR",
                        "HEYTI-CORE no pudo completar la solicitud.",
                    )
                    return

                self._send_json(
                    HTTPStatus.OK,
                    response,
                )
                return

            if (
                require_authenticated_operations
                and path in operational_paths
            ):
                try:
                    token = self._bearer_token()
                    security_application.current_session(
                        token
                    )
                except AuthenticatedSessionRequiredError:
                    self._send_error_contract(
                        HTTPStatus.UNAUTHORIZED,
                        "AUTHENTICATION_REQUIRED",
                        (
                            "Se requiere una sesion "
                            "autenticada."
                        ),
                    )
                    return
                except Exception:
                    self._send_error_contract(
                        HTTPStatus.INTERNAL_SERVER_ERROR,
                        "INTERNAL_ERROR",
                        (
                            "HEYTI-CORE no pudo completar "
                            "la solicitud."
                        ),
                    )
                    return

            request_id = (
                self.headers.get(
                    "X-Request-ID",
                    "",
                ).strip()
                or f"REQ-{uuid4()}"
            )
            execution_id = f"EXE-{uuid4()}"

            try:
                if path == "/v1/universes/describe":
                    response = (
                        application
                        .describe_universe(payload)
                    )
                elif path == "/v1/field/describe":
                    response = (
                        application.describe_field(payload)
                    )
                else:
                    if (
                        "electoral_query" in payload
                        and not isinstance(
                            payload["electoral_query"],
                            dict,
                        )
                    ):
                        raise ValueError(
                            "electoral_query debe ser un objeto"
                        )

                    response = application.describe_section(
                        section_id=payload.get(
                            "section_id"
                        ),
                        request_id=request_id,
                        execution_id=execution_id,
                        knowledge_version=knowledge_version,
                        electoral_query=payload.get(
                            "electoral_query"
                        ),
                    )
            except (TypeError, ValueError) as exc:
                self._send_error_contract(
                    HTTPStatus.BAD_REQUEST,
                    "INVALID_REQUEST",
                    str(exc),
                )
                return
            except Exception:
                self._send_error_contract(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    "INTERNAL_ERROR",
                    "HEYTI-CORE no pudo completar la solicitud.",
                )
                return

            self._send_json(
                HTTPStatus.OK,
                response,
            )

    return ThreadingHTTPServer(
        (host, port),
        HeytiRequestHandler,
    )
