from typing import Any

from heyti.security.authentication import (
    AuthenticationStatus,
)
from heyti.security.sessions import (
    AuthenticatedSession,
)


class InvalidCredentialsError(Exception):
    pass


class PasswordChangeRequiredError(Exception):
    pass


class AuthenticatedSessionRequiredError(Exception):
    pass


from dataclasses import replace

from heyti.security.contracts import (
    AuthorizationResource,
    DecisionReason,
    PermissionScope,
    PrivacyProjection,
)


class SecurityHttpApplication:
    def __init__(
        self,
        authentication_service,
        session_service,
        authorization_service=None,
        password_change_service=None,
    ):
        if not callable(
            getattr(
                authentication_service,
                "authenticate",
                None,
            )
        ):
            raise TypeError(
                "authentication_service incompatible"
            )

        for method in (
            "create_session",
            "resolve",
            "revoke",
        ):
            if not callable(
                getattr(
                    session_service,
                    method,
                    None,
                )
            ):
                raise TypeError(
                    "session_service incompatible"
                )

        self._authentication_service = (
            authentication_service
        )
        self._session_service = session_service

        if (
            authorization_service is not None
            and not callable(
                getattr(
                    authorization_service,
                    "authorize",
                    None,
                )
            )
        ):
            raise TypeError(
                "authorization_service incompatible"
            )

        self._authorization_service = (
            authorization_service
        )

        if (
            password_change_service is not None
            and not callable(
                getattr(
                    password_change_service,
                    "change_password",
                    None,
                )
            )
        ):
            raise TypeError(
                "password_change_service incompatible"
            )

        self._password_change_service = (
            password_change_service
        )

    def login(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError(
                "La solicitud de acceso debe ser un objeto"
            )

        username = payload.get("username")
        password = payload.get("password")

        if not isinstance(username, str):
            raise ValueError(
                "username debe ser una cadena"
            )

        if not username.strip():
            raise ValueError(
                "username no puede estar vacio"
            )

        if not isinstance(password, str):
            raise ValueError(
                "password debe ser una cadena"
            )

        if not password:
            raise ValueError(
                "password no puede estar vacio"
            )

        result = (
            self._authentication_service
            .authenticate(
                username.strip(),
                password,
            )
        )

        if result.status is (
            AuthenticationStatus
            .PASSWORD_CHANGE_REQUIRED
        ):
            raise PasswordChangeRequiredError(
                "Debe cambiarse la contrase?a"
            )

        if result.status is not (
            AuthenticationStatus.AUTHENTICATED
        ):
            raise InvalidCredentialsError(
                "Credenciales inv?lidas"
            )

        session = (
            self._session_service
            .create_session(result)
        )

        return self._session_payload(session)

    def change_password(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if self._password_change_service is None:
            raise RuntimeError(
                "El cambio de contrasena no esta configurado"
            )

        if not isinstance(payload, dict):
            raise ValueError(
                "La solicitud debe ser un objeto"
            )

        result = (
            self._password_change_service
            .change_password(
                username=payload.get("username"),
                current_password=payload.get(
                    "current_password"
                ),
                new_password=payload.get(
                    "new_password"
                ),
                confirmation=payload.get(
                    "confirmation"
                ),
            )
        )

        return {
            "status": "PASSWORD_CHANGED",
            "user": {
                "user_id": result.user_id,
                "username": result.username,
                "display_name": result.display_name,
            },
        }

    def current_session(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        session = self._session_service.resolve(
            session_id
        )

        if session is None:
            raise AuthenticatedSessionRequiredError(
                "Se requiere una sesi?n autenticada"
            )

        return self._session_payload(session)

    def authorize_field_operation(
        self,
        *,
        user_id: int,
        session_id: str,
        payload: dict[str, Any],
    ):
        if self._authorization_service is None:
            raise RuntimeError(
                "La autorizacion no esta configurada"
            )

        if not isinstance(payload, dict):
            raise ValueError(
                "La consulta de Campo debe ser un objeto"
            )

        operation = payload.get("operation")

        permission_by_operation = {
            "summary": "FIELD_SUMMARY_READ",
            "map": "FIELD_MAP_READ",
        }

        permission_code = (
            permission_by_operation.get(operation)
        )

        if permission_code is None:
            raise ValueError(
                "Operacion de Campo no soportada"
            )

        section_code = None

        if operation == "map":
            raw_section_code = payload.get(
                "section_code"
            )

            if raw_section_code is not None:
                section_code = str(
                    raw_section_code
                ).strip()

                if not section_code:
                    raise ValueError(
                        "section_code no puede estar vacio"
                    )

        decision = (
            self._authorization_service.authorize(
                user_id=user_id,
                session_id=session_id,
                permission_code=permission_code,
                resource=AuthorizationResource(
                    resource_type=(
                        f"FIELD_{operation.upper()}"
                    ),
                    resource_ref=operation,
                    section_code=section_code,
                ),
            )
        )

        if (
            operation == "map"
            and section_code is None
            and decision.allowed
            and decision.scope
            is not PermissionScope.GLOBAL
        ):
            return replace(
                decision,
                allowed=False,
                reason=(
                    DecisionReason
                    .RESOURCE_OUTSIDE_SCOPE
                ),
                audit_required=True,
                privacy_projection=(
                    PrivacyProjection.REDACTED
                ),
            )

        return decision

    def logout(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        session = self._session_service.resolve(
            session_id
        )

        if session is None:
            raise AuthenticatedSessionRequiredError(
                "Se requiere una sesi?n autenticada"
            )

        self._session_service.revoke(
            session.session_id
        )

        return {
            "status": "SIGNED_OUT",
        }

    @staticmethod
    def _session_payload(
        session: AuthenticatedSession,
    ) -> dict[str, Any]:
        return {
            "status": "AUTHENTICATED",
            "session_token": session.session_id,
            "expires_at": (
                session.expires_at.isoformat()
            ),
            "user": {
                "user_id": session.user_id,
                "username": session.username,
                "display_name": (
                    session.display_name
                ),
                "role": session.role.value,
            },
        }
