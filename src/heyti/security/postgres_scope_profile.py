from contextlib import contextmanager

from heyti.security.scope_assignment import (
    TerritorialScopeType,
)
from heyti.security.scope_profile import (
    TerritorialScopeProfile,
)


ACTIVE_SCOPES_SQL = """
SELECT
    ts.scope_id,
    ts.scope_name,
    ts.scope_type,
    CASE
        WHEN COUNT(DISTINCT s.municipio_id) = 1
        THEN MIN(m.municipio_id)
        ELSE NULL
    END AS municipality_id,
    CASE
        WHEN COUNT(DISTINCT s.municipio_id) = 1
        THEN MIN(m.municipio_code)
        ELSE NULL
    END AS municipality_code,
    CASE
        WHEN COUNT(DISTINCT s.municipio_id) = 1
        THEN MIN(m.municipio_name)
        ELSE NULL
    END AS municipality_name,
    COUNT(DISTINCT s.section_id) AS section_count
FROM security.user_scope_assignment usa
JOIN security.territorial_scope ts
  ON ts.scope_id = usa.scope_id
 AND ts.active = TRUE
LEFT JOIN security.territorial_scope_section tss
  ON tss.scope_id = ts.scope_id
LEFT JOIN territorial.section s
  ON s.section_id = tss.section_id
LEFT JOIN territorial.municipio m
  ON m.municipio_id = s.municipio_id
WHERE usa.user_id = %s
  AND usa.active = TRUE
  AND usa.valid_from <= CURRENT_TIMESTAMP
  AND (
      usa.valid_until IS NULL
      OR usa.valid_until > CURRENT_TIMESTAMP
  )
GROUP BY
    ts.scope_id,
    ts.scope_name,
    ts.scope_type
ORDER BY ts.scope_id;
"""


class PostgresTerritorialScopeProfileSource:
    def __init__(self, connection_factory):
        if not callable(connection_factory):
            raise TypeError(
                "connection_factory debe ser invocable"
            )

        self._connection_factory = (
            connection_factory
        )

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

    def active_scopes(
        self,
        *,
        user_id: int,
    ) -> tuple[TerritorialScopeProfile, ...]:
        if (
            isinstance(user_id, bool)
            or not isinstance(user_id, int)
        ):
            raise TypeError(
                "user_id debe ser entero"
            )

        if user_id <= 0:
            raise ValueError(
                "user_id debe ser positivo"
            )

        with self._read_cursor() as cursor:
            cursor.execute(
                ACTIVE_SCOPES_SQL,
                (user_id,),
            )
            rows = tuple(cursor.fetchall())

        return tuple(
            TerritorialScopeProfile(
                scope_id=int(row[0]),
                scope_name=str(row[1]),
                scope_type=TerritorialScopeType(
                    str(row[2])
                ),
                municipality_id=(
                    None
                    if row[3] is None
                    else int(row[3])
                ),
                municipality_code=(
                    None
                    if row[4] is None
                    else str(row[4])
                ),
                municipality_name=(
                    None
                    if row[5] is None
                    else str(row[5])
                ),
                section_count=int(row[6]),
            )
            for row in rows
        )
