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


class SecurityHttpApplication:
    def __init__(
        self,
        authentication_service,
        session_service,
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
