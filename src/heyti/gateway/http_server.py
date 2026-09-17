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

    normalized_origins = frozenset(
        origin.rstrip("/")
        for origin in allowed_origins
        if isinstance(origin, str) and origin.strip()
    )

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

            if self._request_path() not in {
                "/health",
                "/v1/sections/describe",
            }:
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
                "Content-Type, X-Request-ID",
            )
            self.send_header(
                "Access-Control-Max-Age",
                "600",
            )
            self.end_headers()

        def do_GET(self) -> None:
            if self._reject_disallowed_origin():
                return

            if self._request_path() != "/health":
                self._send_error_contract(
                    HTTPStatus.NOT_FOUND,
                    "NOT_FOUND",
                    "Ruta no encontrada.",
                )
                return

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

        def do_POST(self) -> None:
            if self._reject_disallowed_origin():
                return

            if (
                self._request_path()
                != "/v1/sections/describe"
            ):
                self._send_error_contract(
                    HTTPStatus.NOT_FOUND,
                    "NOT_FOUND",
                    "Ruta no encontrada.",
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

            request_id = (
                self.headers.get("X-Request-ID", "").strip()
                or f"REQ-{uuid4()}"
            )
            execution_id = f"EXE-{uuid4()}"

            try:
                response = application.describe_section(
                    section_id=payload.get("section_id"),
                    request_id=request_id,
                    execution_id=execution_id,
                    knowledge_version=knowledge_version,
                )
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

    return ThreadingHTTPServer(
        (host, port),
        HeytiRequestHandler,
    )
