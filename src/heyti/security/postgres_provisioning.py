from heyti.security.contracts import AccessRole
from heyti.security.provisioning import (
    ProvisionedUser,
)


ROLE_SQL = """
SELECT role_id
FROM security.access_role
WHERE role_code = %s
  AND active = TRUE;
"""

USER_SQL = """
INSERT INTO security.app_user (
    username,
    display_name
)
VALUES (%s, %s)
RETURNING
    user_id,
    user_uuid::text;
"""

CREDENTIAL_SQL = """
INSERT INTO security.user_credential (
    user_id,
    credential_hash,
    must_change
)
VALUES (%s, %s, %s);
"""

ROLE_ASSIGNMENT_SQL = """
INSERT INTO security.user_role_assignment (
    user_id,
    role_id,
    assigned_by_user_id
)
VALUES (%s, %s, %s);
"""


class PostgresUserProvisioningRepository:
    def __init__(self, connection_factory):
        if not callable(connection_factory):
            raise TypeError(
                "connection_factory debe ser invocable"
            )

        self._connection_factory = (
            connection_factory
        )

    def create_user(
        self,
        *,
        username: str,
        display_name: str,
        credential_hash: str,
        role: AccessRole,
        must_change: bool,
        assigned_by_user_id: int | None,
    ) -> ProvisionedUser:
        username = self._normalize_text(
            username,
            "username",
        ).lower()
        display_name = self._normalize_text(
            display_name,
            "display_name",
        )

        if not isinstance(credential_hash, str):
            raise TypeError(
                "credential_hash debe ser una cadena"
            )

        credential_hash = credential_hash.strip()

        if not credential_hash.startswith(
            "$argon2id$"
        ):
            raise ValueError(
                "credential_hash debe ser Argon2id"
            )

        if not isinstance(role, AccessRole):
            raise TypeError(
                "role debe ser AccessRole"
            )

        if not isinstance(must_change, bool):
            raise TypeError(
                "must_change debe ser booleano"
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

        connection = self._connection_factory()

        try:
            connection.set_session(
                readonly=False,
                autocommit=False,
            )
            cursor = connection.cursor()

            try:
                cursor.execute(
                    ROLE_SQL,
                    (role.value,),
                )
                role_row = cursor.fetchone()

                if role_row is None:
                    raise ValueError(
                        "El rol solicitado no esta activo"
                    )

                role_id = int(role_row[0])

                cursor.execute(
                    USER_SQL,
                    (
                        username,
                        display_name,
                    ),
                )
                user_row = cursor.fetchone()

                if user_row is None:
                    raise RuntimeError(
                        "PostgreSQL no devolvio el usuario"
                    )

                user_id = int(user_row[0])
                user_uuid = str(user_row[1])

                cursor.execute(
                    CREDENTIAL_SQL,
                    (
                        user_id,
                        credential_hash,
                        must_change,
                    ),
                )
                cursor.execute(
                    ROLE_ASSIGNMENT_SQL,
                    (
                        user_id,
                        role_id,
                        assigned_by_user_id,
                    ),
                )

                connection.commit()
            except Exception:
                connection.rollback()
                raise
            finally:
                cursor.close()
        finally:
            connection.close()

        return ProvisionedUser(
            user_id=user_id,
            user_uuid=user_uuid,
            username=username,
            display_name=display_name,
            role=role,
            must_change=must_change,
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
