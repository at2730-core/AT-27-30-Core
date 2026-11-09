import os
from contextlib import contextmanager

import psycopg2


SUMMARY_SQL = """
SELECT
    COUNT(*) AS total_records,
    COUNT(*) FILTER (
        WHERE geom IS NOT NULL
    ) AS geolocated_records,
    COUNT(*) FILTER (
        WHERE geom IS NULL
    ) AS records_without_geometry,
    COUNT(*) FILTER (
        WHERE NOT EXISTS (
            SELECT 1
            FROM field.actor_assignment aa
            WHERE aa.actor_id = a.actor_id
              AND aa.active = TRUE
        )
    ) AS unassigned_records
FROM field.actor a;
"""

ROLES_SQL = """
SELECT
    r.role_code,
    COUNT(DISTINCT aa.actor_id) AS records
FROM field.actor_assignment aa
JOIN field.role r
  ON r.role_id = aa.role_id
WHERE aa.active = TRUE
GROUP BY r.role_code
ORDER BY r.role_code;
"""

MAP_SQL = """
SELECT
    a.actor_uuid::text,
    s.section_code::text,
    r.role_code,
    CASE
        WHEN a.geom IS NULL THEN NULL
        ELSE ST_X(a.geom)
    END AS longitude,
    CASE
        WHEN a.geom IS NULL THEN NULL
        ELSE ST_Y(a.geom)
    END AS latitude
FROM field.actor a
JOIN territorial.section s
  ON s.section_id = a.section_id
LEFT JOIN field.actor_assignment aa
  ON aa.actor_id = a.actor_id
 AND aa.active = TRUE
LEFT JOIN field.role r
  ON r.role_id = aa.role_id
"""


def build_environment_connection_factory(environ=None):
    environment = os.environ if environ is None else environ

    def connect():
        parameters = {
            "host": environment.get(
                "HEYTI_DB_HOST",
                "localhost",
            ),
            "port": int(
                environment.get(
                    "HEYTI_DB_PORT",
                    "5432",
                )
            ),
            "dbname": environment.get(
                "HEYTI_DB_NAME",
                "at2730_core",
            ),
            "user": environment.get(
                "HEYTI_DB_USER",
                "postgres",
            ),
            "connect_timeout": 5,
            "application_name": "HEYTI_FIELD_RUNTIME",
        }

        password = environment.get(
            "HEYTI_DB_PASSWORD"
        )

        if password:
            parameters["password"] = password

        return psycopg2.connect(**parameters)

    return connect


class PostgresFieldSource:
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

    def summary(self):
        with self._read_cursor() as cursor:
            cursor.execute(SUMMARY_SQL)
            row = cursor.fetchone()

            if row is None:
                raise ValueError(
                    "PostgreSQL no devolvi? resumen de Campo"
                )

            cursor.execute(ROLES_SQL)
            role_rows = cursor.fetchall()

        return {
            "total_records": int(row[0]),
            "geolocated_records": int(row[1]),
            "records_without_geometry": int(row[2]),
            "unassigned_records": int(row[3]),
            "by_role": {
                str(role_code): int(records)
                for role_code, records in role_rows
            },
        }

    def map_points(self, section_code=None):
        sql = MAP_SQL
        parameters = ()

        if section_code is not None:
            sql += " WHERE s.section_code = %s"
            parameters = (str(section_code),)

        sql += " ORDER BY a.actor_id"

        with self._read_cursor() as cursor:
            cursor.execute(sql, parameters)
            rows = cursor.fetchall()

        return [
            {
                "actor_uuid": row[0],
                "section_code": row[1],
                "role_code": row[2],
                "longitude": row[3],
                "latitude": row[4],
            }
            for row in rows
        ]
