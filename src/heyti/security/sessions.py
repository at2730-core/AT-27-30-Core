from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe
from typing import Callable

from heyti.security.authentication import (
    AuthenticationResult,
)
from heyti.security.contracts import AccessRole
from heyti.session.session_manager import (
    SessionManager,
)


@dataclass(frozen=True)
class AuthenticatedSession:
    session_id: str
    user_id: int
    username: str
    display_name: str
    role: AccessRole
    created_at: datetime
    expires_at: datetime


class AuthenticatedSessionService:
    def __init__(
        self,
        session_manager: SessionManager,
        *,
        ttl_seconds: int = 8 * 60 * 60,
        clock: Callable[[], datetime] | None = None,
        token_factory: Callable[[], str] | None = None,
    ):
        if not isinstance(
            session_manager,
            SessionManager,
        ):
            raise TypeError(
                "session_manager debe ser SessionManager"
            )

        if isinstance(ttl_seconds, bool) or not isinstance(
            ttl_seconds,
            int,
        ):
            raise TypeError(
                "ttl_seconds debe ser un entero"
            )

        if ttl_seconds <= 0:
            raise ValueError(
                "ttl_seconds debe ser positivo"
            )

        if clock is None:
            clock = lambda: datetime.now(
                timezone.utc
            )

        if token_factory is None:
            token_factory = (
                lambda: token_urlsafe(32)
            )

        if not callable(clock):
            raise TypeError(
                "clock debe ser invocable"
            )

        if not callable(token_factory):
            raise TypeError(
                "token_factory debe ser invocable"
            )

        self._session_manager = session_manager
        self._ttl_seconds = ttl_seconds
        self._clock = clock
        self._token_factory = token_factory

    def create_session(
        self,
        authentication: AuthenticationResult,
    ) -> AuthenticatedSession:
        if not isinstance(
            authentication,
            AuthenticationResult,
        ):
            raise TypeError(
                "authentication debe ser "
                "AuthenticationResult"
            )

        if not authentication.session_allowed:
            raise ValueError(
                "La autenticacion no permite crear sesion"
            )

        if (
            authentication.user_id is None
            or authentication.username is None
            or authentication.display_name is None
            or authentication.role is None
        ):
            raise ValueError(
                "La autenticacion esta incompleta"
            )

        session_id = self._new_session_id()
        created_at = self._clock()

        session = AuthenticatedSession(
            session_id=session_id,
            user_id=authentication.user_id,
            username=authentication.username,
            display_name=(
                authentication.display_name
            ),
            role=authentication.role,
            created_at=created_at,
            expires_at=created_at + timedelta(
                seconds=self._ttl_seconds
            ),
        )

        self._session_manager.create(
            session_id,
            session,
        )

        return session

    def resolve(
        self,
        session_id: str,
    ) -> AuthenticatedSession | None:
        normalized = self._normalize_session_id(
            session_id
        )

        session = self._session_manager.get(
            normalized
        )

        if not isinstance(
            session,
            AuthenticatedSession,
        ):
            return None

        if session.expires_at <= self._clock():
            self._session_manager.remove(
                normalized
            )
            return None

        return session

    def revoke(self, session_id: str) -> None:
        normalized = self._normalize_session_id(
            session_id
        )
        self._session_manager.remove(normalized)

    def _new_session_id(self) -> str:
        for _ in range(5):
            candidate = self._token_factory()

            if not isinstance(candidate, str):
                raise TypeError(
                    "token_factory debe devolver cadena"
                )

            normalized = candidate.strip()

            if len(normalized) < 32:
                raise ValueError(
                    "El identificador de sesi?n "
                    "es demasiado corto"
                )

            if not self._session_manager.exists(
                normalized
            ):
                return normalized

        raise RuntimeError(
            "No pudo generarse una sesion unica"
        )

    @staticmethod
    def _normalize_session_id(
        session_id: str,
    ) -> str:
        if not isinstance(session_id, str):
            raise TypeError(
                "session_id debe ser una cadena"
            )

        normalized = session_id.strip()

        if not normalized:
            raise ValueError(
                "session_id no puede estar vacio"
            )

        return normalized
