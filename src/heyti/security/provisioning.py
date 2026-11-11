from dataclasses import dataclass

from heyti.security.contracts import AccessRole


@dataclass(frozen=True)
class UserProvisioningRequest:
    username: str
    display_name: str
    password: str
    role: AccessRole
    must_change: bool = True
    assigned_by_user_id: int | None = None


@dataclass(frozen=True)
class ProvisionedUser:
    user_id: int
    user_uuid: str
    username: str
    display_name: str
    role: AccessRole
    must_change: bool


class UserProvisioningService:
    def __init__(
        self,
        repository,
        credential_hasher,
    ):
        if not callable(
            getattr(
                repository,
                "create_user",
                None,
            )
        ):
            raise TypeError(
                "repository debe proporcionar create_user"
            )

        if not callable(
            getattr(
                credential_hasher,
                "hash_password",
                None,
            )
        ):
            raise TypeError(
                "credential_hasher debe proporcionar "
                "hash_password"
            )

        self._repository = repository
        self._credential_hasher = credential_hasher

    def provision(
        self,
        request: UserProvisioningRequest,
    ) -> ProvisionedUser:
        if not isinstance(
            request,
            UserProvisioningRequest,
        ):
            raise TypeError(
                "request debe ser UserProvisioningRequest"
            )

        username = self._normalize_text(
            request.username,
            "username",
        ).lower()
        display_name = self._normalize_text(
            request.display_name,
            "display_name",
        )

        if not isinstance(request.password, str):
            raise TypeError(
                "password debe ser una cadena"
            )

        if not request.password:
            raise ValueError(
                "password no puede estar vacio"
            )

        if not isinstance(request.role, AccessRole):
            raise TypeError(
                "role debe ser AccessRole"
            )

        if not isinstance(request.must_change, bool):
            raise TypeError(
                "must_change debe ser booleano"
            )

        assigned_by_user_id = (
            request.assigned_by_user_id
        )

        if assigned_by_user_id is not None:
            if (
                isinstance(
                    assigned_by_user_id,
                    bool,
                )
                or not isinstance(
                    assigned_by_user_id,
                    int,
                )
            ):
                raise TypeError(
                    "assigned_by_user_id debe ser entero"
                )

            if assigned_by_user_id <= 0:
                raise ValueError(
                    "assigned_by_user_id debe ser positivo"
                )

        credential_hash = (
            self._credential_hasher
            .hash_password(request.password)
        )

        return self._repository.create_user(
            username=username,
            display_name=display_name,
            credential_hash=credential_hash,
            role=request.role,
            must_change=request.must_change,
            assigned_by_user_id=(
                assigned_by_user_id
            ),
        )

    @staticmethod
    def _normalize_text(
        value,
        field_name,
    ) -> str:
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} debe ser una cadena"
            )

        normalized = value.strip()

        if not normalized:
            raise ValueError(
                f"{field_name} no puede estar vacio"
            )

        return normalized
