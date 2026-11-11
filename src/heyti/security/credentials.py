from dataclasses import dataclass

from argon2 import PasswordHasher
from argon2.exceptions import (
    InvalidHashError,
    VerificationError,
    VerifyMismatchError,
)


@dataclass(frozen=True)
class PasswordVerification:
    valid: bool
    needs_rehash: bool = False


class Argon2CredentialHasher:
    def __init__(self, password_hasher=None):
        if password_hasher is None:
            password_hasher = PasswordHasher()

        if not callable(
            getattr(password_hasher, "hash", None)
        ):
            raise TypeError(
                "password_hasher debe proporcionar hash"
            )

        if not callable(
            getattr(password_hasher, "verify", None)
        ):
            raise TypeError(
                "password_hasher debe proporcionar verify"
            )

        if not callable(
            getattr(
                password_hasher,
                "check_needs_rehash",
                None,
            )
        ):
            raise TypeError(
                "password_hasher debe proporcionar "
                "check_needs_rehash"
            )

        self._password_hasher = password_hasher

    def hash_password(self, password: str) -> str:
        normalized = self._validate_password(password)

        credential_hash = self._password_hasher.hash(
            normalized
        )

        if not credential_hash.startswith(
            "$argon2id$"
        ):
            raise ValueError(
                "El proveedor no gener? un hash Argon2id"
            )

        return credential_hash

    def verify_password(
        self,
        credential_hash: str,
        password: str,
    ) -> PasswordVerification:
        if not isinstance(credential_hash, str):
            raise TypeError(
                "credential_hash debe ser una cadena"
            )

        normalized_hash = credential_hash.strip()

        if not normalized_hash:
            raise ValueError(
                "credential_hash no puede estar vacio"
            )

        normalized_password = (
            self._validate_password(password)
        )

        try:
            valid = bool(
                self._password_hasher.verify(
                    normalized_hash,
                    normalized_password,
                )
            )
        except (
            InvalidHashError,
            VerificationError,
            VerifyMismatchError,
        ):
            return PasswordVerification(
                valid=False,
                needs_rehash=False,
            )

        if not valid:
            return PasswordVerification(
                valid=False,
                needs_rehash=False,
            )

        return PasswordVerification(
            valid=True,
            needs_rehash=bool(
                self._password_hasher
                .check_needs_rehash(
                    normalized_hash
                )
            ),
        )

    @staticmethod
    def _validate_password(password: str) -> str:
        if not isinstance(password, str):
            raise TypeError(
                "password debe ser una cadena"
            )

        if not password:
            raise ValueError(
                "password no puede estar vacio"
            )

        return password
