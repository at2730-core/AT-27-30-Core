from heyti.security.scope_assignment import (
    AssignedTerritorialScope,
    TerritorialScopeType,
)


ACTIVE_USER_SQL = """
SELECT
    u.user_id,
    r.role_code
FROM security.app_user u
JOIN security.user_role_assignment ura
  ON ura.user_id = u.user_id
 AND ura.active
 AND (
     ura.valid_until IS NULL
     OR ura.valid_until > CURRENT_TIMESTAMP
 )
JOIN security.access_role r
  ON r.role_id = ura.role_id
 AND r.active
WHERE u.user_id = %s
  AND u.active;
"""

ACTIVE_ADMIN_SQL = """
SELECT u.user_id
FROM security.app_user u
JOIN security.user_role_assignment ura
  ON ura.user_id = u.user_id
 AND ura.active
 AND (
     ura.valid_until IS NULL
     OR ura.valid_until > CURRENT_TIMESTAMP
 )
JOIN security.access_role r
  ON r.role_id = ura.role_id
 AND r.active
WHERE u.user_id = %s
  AND u.active
  AND r.role_code = 'ADMINISTRATOR';
"""

MUNICIPALITY_SQL = """
SELECT
    municipio_id,
    municipio_name
FROM territorial.municipio
WHERE municipio_id = %s;
"""

MUNICIPALITY_SECTIONS_SQL = """
SELECT
    section_id,
    section_code
FROM territorial.section
WHERE municipio_id = %s
ORDER BY section_code;
"""

SECTION_SET_SQL = """
SELECT
    section_id,
    section_code
FROM territorial.section
WHERE section_code = ANY(%s)
ORDER BY section_code;
"""

INSERT_SCOPE_SQL = """
INSERT INTO security.territorial_scope (
    scope_name,
    scope_type,
    created_by_user_id
)
VALUES (%s, %s, %s)
RETURNING scope_id;
"""

INSERT_SCOPE_SECTION_SQL = """
INSERT INTO security.territorial_scope_section (
    scope_id,
    section_id
)
VALUES (%s, %s);
"""

INSERT_ASSIGNMENT_SQL = """
INSERT INTO security.user_scope_assignment (
    user_id,
    scope_id,
    assigned_by_user_id
)
VALUES (%s, %s, %s)
RETURNING assignment_id;
"""


class PostgresTerritorialScopeRepository:
    def __init__(self, connection_factory):
        if not callable(connection_factory):
            raise TypeError(
                "connection_factory debe ser invocable"
            )

        self._connection_factory = (
            connection_factory
        )

    def assign_scope(
        self,
        *,
        user_id: int,
        scope_name: str,
        scope_type: TerritorialScopeType,
        municipality_id: int | None,
        section_codes: tuple[str, ...],
        assigned_by_user_id: int | None,
    ) -> AssignedTerritorialScope:
        user_id = self._positive_id(
            user_id,
            "user_id",
        )
        scope_name = self._normalize_text(
            scope_name,
            "scope_name",
        )

        if not isinstance(
            scope_type,
            TerritorialScopeType,
        ):
            raise TypeError(
                "scope_type debe ser TerritorialScopeType"
            )

        if assigned_by_user_id is not None:
            assigned_by_user_id = self._positive_id(
                assigned_by_user_id,
                "assigned_by_user_id",
            )

        if not isinstance(section_codes, tuple):
            raise TypeError(
                "section_codes debe ser una tupla"
            )

        normalized_codes = tuple(
            self._normalize_text(
                code,
                "section_code",
            )
            for code in section_codes
        )

        if len(set(normalized_codes)) != len(
            normalized_codes
        ):
            raise ValueError(
                "section_codes contiene duplicados"
            )

        if municipality_id is not None:
            municipality_id = self._positive_id(
                municipality_id,
                "municipality_id",
            )

        connection = self._connection_factory()

        try:
            connection.set_session(
                readonly=False,
                autocommit=False,
            )
            cursor = connection.cursor()

            try:
                role_code = self._active_role(
                    cursor,
                    user_id,
                )

                self._validate_role_scope(
                    role_code,
                    scope_type,
                )

                if assigned_by_user_id is not None:
                    cursor.execute(
                        ACTIVE_ADMIN_SQL,
                        (assigned_by_user_id,),
                    )

                    if cursor.fetchone() is None:
                        raise ValueError(
                            "El asignador no es un "
                            "administrador activo"
                        )

                section_rows = self._sections(
                    cursor=cursor,
                    scope_type=scope_type,
                    municipality_id=municipality_id,
                    section_codes=normalized_codes,
                )

                cursor.execute(
                    INSERT_SCOPE_SQL,
                    (
                        scope_name,
                        scope_type.value,
                        assigned_by_user_id,
                    ),
                )
                scope_row = cursor.fetchone()

                if scope_row is None:
                    raise RuntimeError(
                        "PostgreSQL no devolvio el alcance"
                    )

                scope_id = int(scope_row[0])

                if section_rows:
                    cursor.executemany(
                        INSERT_SCOPE_SECTION_SQL,
                        [
                            (
                                scope_id,
                                int(section_id),
                            )
                            for section_id, _
                            in section_rows
                        ],
                    )

                cursor.execute(
                    INSERT_ASSIGNMENT_SQL,
                    (
                        user_id,
                        scope_id,
                        assigned_by_user_id,
                    ),
                )
                assignment_row = cursor.fetchone()

                if assignment_row is None:
                    raise RuntimeError(
                        "PostgreSQL no devolvio "
                        "la asignacion"
                    )

                assignment_id = int(
                    assignment_row[0]
                )

                connection.commit()
            except Exception:
                connection.rollback()
                raise
            finally:
                cursor.close()
        finally:
            connection.close()

        return AssignedTerritorialScope(
            assignment_id=assignment_id,
            scope_id=scope_id,
            user_id=user_id,
            scope_name=scope_name,
            scope_type=scope_type,
            section_count=len(section_rows),
        )

    @staticmethod
    def _active_role(cursor, user_id) -> str:
        cursor.execute(
            ACTIVE_USER_SQL,
            (user_id,),
        )
        rows = cursor.fetchall()

        role_codes = {
            str(row[1])
            for row in rows
        }

        if len(role_codes) != 1:
            raise ValueError(
                "El usuario no tiene un unico "
                "rol activo"
            )

        return role_codes.pop()

    @staticmethod
    def _validate_role_scope(
        role_code: str,
        scope_type: TerritorialScopeType,
    ) -> None:
        if scope_type is TerritorialScopeType.GLOBAL:
            if role_code != "ADMINISTRATOR":
                raise ValueError(
                    "GLOBAL requiere rol "
                    "ADMINISTRATOR"
                )

            return

        if role_code not in (
            "COORDINATOR",
            "PROMOTER",
        ):
            raise ValueError(
                "El alcance territorial requiere "
                "rol COORDINATOR o PROMOTER"
            )

    @staticmethod
    def _sections(
        *,
        cursor,
        scope_type,
        municipality_id,
        section_codes,
    ):
        if scope_type is TerritorialScopeType.GLOBAL:
            if (
                municipality_id is not None
                or section_codes
            ):
                raise ValueError(
                    "GLOBAL no admite recursos"
                )

            return ()

        if (
            scope_type
            is TerritorialScopeType.MUNICIPALITY
        ):
            if municipality_id is None:
                raise ValueError(
                    "MUNICIPALITY requiere "
                    "municipality_id"
                )

            if section_codes:
                raise ValueError(
                    "MUNICIPALITY no admite secciones"
                )

            cursor.execute(
                MUNICIPALITY_SQL,
                (municipality_id,),
            )

            if cursor.fetchone() is None:
                raise ValueError(
                    "El municipio solicitado no existe"
                )

            cursor.execute(
                MUNICIPALITY_SECTIONS_SQL,
                (municipality_id,),
            )
            rows = tuple(cursor.fetchall())

            if not rows:
                raise ValueError(
                    "El municipio no contiene secciones"
                )

            return rows

        if municipality_id is not None:
            raise ValueError(
                "SECTION_SET no admite municipality_id"
            )

        if not section_codes:
            raise ValueError(
                "SECTION_SET requiere secciones"
            )

        cursor.execute(
            SECTION_SET_SQL,
            (list(section_codes),),
        )
        rows = tuple(cursor.fetchall())

        located_codes = {
            str(row[1])
            for row in rows
        }
        requested_codes = set(section_codes)

        missing_codes = sorted(
            requested_codes - located_codes
        )

        if missing_codes:
            raise ValueError(
                "Secciones inexistentes: "
                + ", ".join(missing_codes)
            )

        return rows

    @staticmethod
    def _positive_id(value, field_name) -> int:
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
        ):
            raise TypeError(
                f"{field_name} debe ser entero"
            )

        if value <= 0:
            raise ValueError(
                f"{field_name} debe ser positivo"
            )

        return value

    @staticmethod
    def _normalize_text(value, field_name) -> str:
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
