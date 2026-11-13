from dataclasses import dataclass

from heyti.security.authentication import (
    AuthenticationStatus,
)


class InvalidPasswordChangeCredentialsError(
    Exception
):
    pass


class PasswordChangeLockedError(Exception):
    pass


@dataclass(frozen=True)
class PasswordChangeResult:
    user_id: int
    username: str
    display_name: str


class PasswordChangeService:
    def __init__(
        self,
        authentication_service,
        credential_repository,
        credential_hasher,
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

        if not callable(
            getattr(
                credential_repository,
                "complete_password_change",
                None,
            )
        ):
            raise TypeError(
                "credential_repository debe proporcionar "
                "complete_password_change"
            )

        if not callable(
            getattr(
                credential_hasher,
                "hash_password",
                None,
            )
        ):
            raise TypeError(
                "credential_hasher incompatible"
            )

        self._authentication_service = (
            authentication_service
        )
        self._credential_repository = (
            credential_repository
        )
        self._credential_hasher = (
            credential_hasher
        )

    def change_password(
        self,
        *,
        username: str,
        current_password: str,
        new_password: str,
        confirmation: str,
    ) -> PasswordChangeResult:
        normalized_username = self._text(
            username,
            "username",
            strip=True,
        )
        current_password = self._text(
            current_password,
            "current_password",
        )
        new_password = self._text(
            new_password,
            "new_password",
        )
        confirmation = self._text(
            confirmation,
            "confirmation",
        )

        if new_password != confirmation:
            raise ValueError(
                "La confirmacion no coincide"
            )

        if new_password == current_password:
            raise ValueError(
                "La nueva contrasena debe ser diferente"
            )

        result = (
            self._authentication_service.authenticate(
                normalized_username,
                current_password,
            )
        )

        if result.status is AuthenticationStatus.LOCKED:
            raise PasswordChangeLockedError(
                "La credencial esta bloqueada"
            )

        if not result.credentials_valid:
            raise (
                InvalidPasswordChangeCredentialsError(
                    "Credenciales invalidas"
                )
            )

        if (
            result.user_id is None
            or result.username is None
            or result.display_name is None
        ):
            raise RuntimeError(
                "La autenticacion no devolvio "
                "una identidad completa"
            )

        replacement_hash = (
            self._credential_hasher.hash_password(
                new_password
            )
        )

        self._credential_repository.complete_password_change(
            result.user_id,
            replacement_hash,
        )

        return PasswordChangeResult(
            user_id=result.user_id,
            username=result.username,
            display_name=result.display_name,
        )

    @staticmethod
    def _text(
        value,
        field_name,
        *,
        strip=False,
    ) -> str:
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} debe ser una cadena"
            )

        normalized = (
            value.strip()
            if strip
            else value
        )

        if not normalized:
            raise ValueError(
                f"{field_name} no puede estar vacio"
            )

        return normalized
