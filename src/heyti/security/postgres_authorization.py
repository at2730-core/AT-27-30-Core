from contextlib import contextmanager

from heyti.security.contracts import (
    AccessRole,
    PermissionGrant,
    PermissionScope,
    SecurityIdentity,
    TerritorialAccess,
)


IDENTITY_SQL = """
SELECT
    u.user_id,
    u.active,
    r.role_code,
    tm.team_id,
    ts.scope_type,
    s.section_code::text,
    m.municipio_code::text
FROM security.app_user u
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
LEFT JOIN security.team_membership tm
  ON tm.user_id = u.user_id
 AND tm.active = TRUE
 AND tm.valid_from <= CURRENT_TIMESTAMP
 AND (
        tm.valid_until IS NULL
        OR tm.valid_until > CURRENT_TIMESTAMP
 )
LEFT JOIN security.team t
  ON t.team_id = tm.team_id
 AND t.active = TRUE
LEFT JOIN security.user_scope_assignment usa
  ON usa.user_id = u.user_id
 AND usa.active = TRUE
 AND usa.valid_from <= CURRENT_TIMESTAMP
 AND (
        usa.valid_until IS NULL
        OR usa.valid_until > CURRENT_TIMESTAMP
 )
LEFT JOIN security.territorial_scope ts
  ON ts.scope_id = usa.scope_id
 AND ts.active = TRUE
LEFT JOIN security.territorial_scope_section tss
  ON tss.scope_id = ts.scope_id
LEFT JOIN territorial.section s
  ON s.section_id = tss.section_id
LEFT JOIN territorial.municipio m
  ON m.municipio_id = s.municipio_id
 AND ts.scope_type = 'MUNICIPALITY'
WHERE u.user_id = %s
ORDER BY
    tm.team_id,
    ts.scope_id,
    s.section_code;
"""

GRANTS_SQL = """
SELECT
    p.permission_code,
    rp.permission_scope,
    p.audit_required
FROM security.role_permission rp
JOIN security.access_role r
  ON r.role_id = rp.role_id
JOIN security.access_permission p
  ON p.permission_id = rp.permission_id
WHERE r.role_code = %s
  AND r.active = TRUE
  AND p.active = TRUE
ORDER BY p.permission_code;
"""


class PostgresAuthorizationSource:
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

    def identity(
        self,
        user_id: int,
        session_id: str,
    ) -> SecurityIdentity | None:
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

        if not isinstance(session_id, str):
            raise TypeError(
                "session_id debe ser una cadena"
            )

        normalized_session_id = session_id.strip()

        if not normalized_session_id:
            raise ValueError(
                "session_id no puede estar vac?o"
            )

        with self._read_cursor() as cursor:
            cursor.execute(
                IDENTITY_SQL,
                (user_id,),
            )
            rows = cursor.fetchall()

        if not rows:
            return None

        role_codes = {
            str(row[2])
            for row in rows
            if row[2] is not None
        }

        if len(role_codes) != 1:
            return None

        team_ids = frozenset(
            int(row[3])
            for row in rows
            if row[3] is not None
        )

        global_access = any(
            row[4] == "GLOBAL"
            for row in rows
        )

        section_codes = frozenset(
            str(row[5])
            for row in rows
            if row[5] is not None
        )

        municipality_codes = frozenset(
            str(row[6])
            for row in rows
            if row[6] is not None
        )

        return SecurityIdentity(
            user_id=int(rows[0][0]),
            session_id=normalized_session_id,
            role=AccessRole(role_codes.pop()),
            active=bool(rows[0][1]),
            team_ids=team_ids,
            territorial_access=TerritorialAccess(
                global_access=global_access,
                municipality_codes=(
                    municipality_codes
                ),
                section_codes=section_codes,
            ),
        )

    def grants(
        self,
        role: AccessRole,
    ) -> tuple[PermissionGrant, ...]:
        if not isinstance(role, AccessRole):
            raise TypeError(
                "role debe ser AccessRole"
            )

        with self._read_cursor() as cursor:
            cursor.execute(
                GRANTS_SQL,
                (role.value,),
            )
            rows = cursor.fetchall()

        return tuple(
            PermissionGrant(
                permission_code=str(row[0]),
                scope=PermissionScope(str(row[1])),
                audit_required=bool(row[2]),
            )
            for row in rows
        )
