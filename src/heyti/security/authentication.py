from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Callable

from heyti.security.contracts import AccessRole


class AuthenticationStatus(str, Enum):
    AUTHENTICATED = "AUTHENTICATED"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    LOCKED = "LOCKED"
    PASSWORD_CHANGE_REQUIRED = (
        "PASSWORD_CHANGE_REQUIRED"
    )


@dataclass(frozen=True)
class AuthenticationResult:
    status: AuthenticationStatus
    user_id: int | None = None
    username: str | None = None
    display_name: str | None = None
    role: AccessRole | None = None

    @property
    def credentials_valid(self) -> bool:
        return self.status in {
            AuthenticationStatus.AUTHENTICATED,
            AuthenticationStatus.PASSWORD_CHANGE_REQUIRED,
        }

    @property
    def session_allowed(self) -> bool:
        return (
            self.status
            is AuthenticationStatus.AUTHENTICATED
        )


class AuthenticationService:
    def __init__(
        self,
        repository,
        credential_hasher,
        *,
        max_attempts: int = 5,
        lock_seconds: int = 900,
        clock: Callable[[], datetime] | None = None,
    ):
        if repository is None:
            raise TypeError(
                "repository es obligatorio"
            )

        for method in (
            "find_by_username",
            "record_failure",
            "record_success",
            "replace_hash",
        ):
            if not callable(
                getattr(repository, method, None)
            ):
                raise TypeError(
                    f"repository debe proporcionar {method}"
                )

        for method in (
            "hash_password",
            "verify_password",
        ):
            if not callable(
                getattr(
                    credential_hasher,
                    method,
                    None,
                )
            ):
                raise TypeError(
                    "credential_hasher incompatible"
                )

        if isinstance(max_attempts, bool) or not isinstance(
            max_attempts,
            int,
        ):
            raise TypeError(
                "max_attempts debe ser un entero"
            )

        if max_attempts <= 0:
            raise ValueError(
                "max_attempts debe ser positivo"
            )

        if isinstance(lock_seconds, bool) or not isinstance(
            lock_seconds,
            int,
        ):
            raise TypeError(
                "lock_seconds debe ser un entero"
            )

        if lock_seconds <= 0:
            raise ValueError(
                "lock_seconds debe ser positivo"
            )

        if clock is None:
            clock = lambda: datetime.now(
                timezone.utc
            )

        if not callable(clock):
            raise TypeError(
                "clock debe ser invocable"
            )

        self._repository = repository
        self._credential_hasher = credential_hasher
        self._max_attempts = max_attempts
        self._lock_seconds = lock_seconds
        self._clock = clock
        self._dummy_hash = (
            credential_hasher.hash_password(
                "HEYTI-DUMMY-CREDENTIAL"
            )
        )

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> AuthenticationResult:
        record = self._repository.find_by_username(
            username
        )

        if record is None:
            self._credential_hasher.verify_password(
                self._dummy_hash,
                password,
            )
            return self._invalid()

        verification = (
            self._credential_hasher.verify_password(
                record.credential_hash,
                password,
            )
        )

        now = self._clock()

        if (
            record.locked_until is not None
            and record.locked_until > now
        ):
            return AuthenticationResult(
                status=AuthenticationStatus.LOCKED
            )

        if (
            not record.active
            or record.role is None
        ):
            return self._invalid()

        if not verification.valid:
            self._repository.record_failure(
                record.user_id,
                max_attempts=self._max_attempts,
                lock_seconds=self._lock_seconds,
            )
            return self._invalid()

        self._repository.record_success(
            record.user_id
        )

        if verification.needs_rehash:
            replacement_hash = (
                self._credential_hasher.hash_password(
                    password
                )
            )
            self._repository.replace_hash(
                record.user_id,
                replacement_hash,
            )

        status = (
            AuthenticationStatus.PASSWORD_CHANGE_REQUIRED
            if record.must_change
            else AuthenticationStatus.AUTHENTICATED
        )

        return AuthenticationResult(
            status=status,
            user_id=record.user_id,
            username=record.username,
            display_name=record.display_name,
            role=record.role,
        )

    @staticmethod
    def _invalid() -> AuthenticationResult:
        return AuthenticationResult(
            status=(
                AuthenticationStatus.INVALID_CREDENTIALS
            )
        )
