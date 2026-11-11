from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime

from heyti.security.contracts import AccessRole


CREDENTIAL_SQL = """
SELECT
    u.user_id,
    u.username,
    u.display_name,
    u.active,
    c.credential_hash,
    c.failed_attempts,
    c.locked_until,
    c.must_change,
    r.role_code
FROM security.app_user u
JOIN security.user_credential c
  ON c.user_id = u.user_id
LEFT JOIN security.user_role_assignment ura
  ON ura.user_id = u.user_id
 AND ura.active = TRUE
 AND ura.valid_from <= CURRENT_TIMESTAMP
 AND (
        ura.valid_until IS NULL
        OR ura.valid_until > CURRENT_TIMESTAMP
 )
LEFT JOIN security.access_role r
  ON r.role_id = ura.role_id
 AND r.active = TRUE
WHERE lower(u.username) = lower(%s);
"""

FAILURE_SQL = """
UPDATE security.user_credential
SET
    failed_attempts = failed_attempts + 1,
    locked_until = CASE
        WHEN failed_attempts + 1 >= %s
        THEN CURRENT_TIMESTAMP
             + make_interval(secs => %s)
        ELSE locked_until
    END,
    updated_at = CURRENT_TIMESTAMP
WHERE user_id = %s;
"""

SUCCESS_SQL = """
UPDATE security.user_credential
SET
    failed_attempts = 0,
    locked_until = NULL,
    updated_at = CURRENT_TIMESTAMP
WHERE user_id = %s;
"""

REHASH_SQL = """
UPDATE security.user_credential
SET
    credential_hash = %s,
    password_changed_at = CURRENT_TIMESTAMP,
    updated_at = CURRENT_TIMESTAMP
WHERE user_id = %s;
"""


@dataclass(frozen=True)
class CredentialRecord:
    user_id: int
    username: str
    display_name: str
    active: bool
    credential_hash: str
    failed_attempts: int
    locked_until: datetime | None
    must_change: bool
    role: AccessRole | None


class PostgresCredentialRepository:
    def __init__(self, connection_factory):
        if not callable(connection_factory):
            raise TypeError(
                "connection_factory debe ser invocable"
            )

        self._connection_factory = connection_factory

    @contextmanager
    def _read_cursor(self):
        connection = self._connection_factory()

        try:
            connection.set_session(
                readonly=True,
                autocommit=False,
            )
            cursor = connection.cursor()

            try:
                cursor.execute(
                    "SET TRANSACTION ISOLATION LEVEL "
                    "REPEATABLE READ READ ONLY"
                )
                yield cursor
            finally:
                cursor.close()
                connection.rollback()
        finally:
            connection.close()

    @contextmanager
    def _write_cursor(self):
        connection = self._connection_factory()

        try:
            connection.set_session(
                readonly=False,
                autocommit=False,
            )
            cursor = connection.cursor()

            try:
                yield cursor
                connection.commit()
            except Exception:
                connection.rollback()
                raise
            finally:
                cursor.close()
        finally:
            connection.close()

    def find_by_username(
        self,
        username: str,
    ) -> CredentialRecord | None:
        if not isinstance(username, str):
            raise TypeError(
                "username debe ser una cadena"
            )

        normalized_username = username.strip()

        if not normalized_username:
            raise ValueError(
                "username no puede estar vacio"
            )

        with self._read_cursor() as cursor:
            cursor.execute(
                CREDENTIAL_SQL,
                (normalized_username,),
            )
            row = cursor.fetchone()

        if row is None:
            return None

        role = (
            AccessRole(str(row[8]))
            if row[8] is not None
            else None
        )

        return CredentialRecord(
            user_id=int(row[0]),
            username=str(row[1]),
            display_name=str(row[2]),
            active=bool(row[3]),
            credential_hash=str(row[4]),
            failed_attempts=int(row[5]),
            locked_until=row[6],
            must_change=bool(row[7]),
            role=role,
        )

    def record_failure(
        self,
        user_id: int,
        *,
        max_attempts: int,
        lock_seconds: int,
    ) -> None:
        self._validate_user_id(user_id)

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

        with self._write_cursor() as cursor:
            cursor.execute(
                FAILURE_SQL,
                (
                    max_attempts,
                    lock_seconds,
                    user_id,
                ),
            )

    def record_success(self, user_id: int) -> None:
        self._validate_user_id(user_id)

        with self._write_cursor() as cursor:
            cursor.execute(
                SUCCESS_SQL,
                (user_id,),
            )

    def replace_hash(
        self,
        user_id: int,
        credential_hash: str,
    ) -> None:
        self._validate_user_id(user_id)

        if not isinstance(credential_hash, str):
            raise TypeError(
                "credential_hash debe ser una cadena"
            )

        normalized_hash = credential_hash.strip()

        if not normalized_hash.startswith(
            "$argon2id$"
        ):
            raise ValueError(
                "credential_hash debe ser Argon2id"
            )

        with self._write_cursor() as cursor:
            cursor.execute(
                REHASH_SQL,
                (
                    normalized_hash,
                    user_id,
                ),
            )

    @staticmethod
    def _validate_user_id(user_id: int) -> None:
        if isinstance(user_id, bool) or not isinstance(
            user_id,
            int,
        ):
            raise TypeError(
                "user_id debe ser un entero"
            )

        if user_id <= 0:
            raise ValueError(
                "user_id debe ser positivo"
            )
