import pytest

from heyti.security.postgres_scope_profile import (
    ACTIVE_SCOPES_SQL,
    PostgresTerritorialScopeProfileSource,
)
from heyti.security.scope_assignment import (
    TerritorialScopeType,
)


class RecordingCursor:
    def __init__(self, rows):
        self.rows = rows
        self.executions = []
        self.closed = False

    def execute(self, sql, parameters=None):
        self.executions.append(
            (sql, parameters)
        )

    def fetchall(self):
        return list(self.rows)

    def close(self):
        self.closed = True


class RecordingConnection:
    def __init__(self, rows):
        self.cursor_instance = RecordingCursor(
            rows
        )
        self.session_calls = []
        self.rollback_count = 0
        self.closed = False

    def set_session(self, **options):
        self.session_calls.append(options)

    def cursor(self):
        return self.cursor_instance

    def rollback(self):
        self.rollback_count += 1

    def close(self):
        self.closed = True


def source_for(rows):
    connection = RecordingConnection(rows)

    return (
        PostgresTerritorialScopeProfileSource(
            lambda: connection
        ),
        connection,
    )


def test_reads_municipality_scope():
    source, connection = source_for(
        [
            (
                2,
                "Municipio 20 - Leon",
                "MUNICIPALITY",
                20,
                "20",
                "Leon de los Aldama",
                787,
            )
        ]
    )

    scopes = source.active_scopes(user_id=4)

    assert len(scopes) == 1

    scope = scopes[0]

    assert scope.scope_id == 2
    assert scope.scope_name == (
        "Municipio 20 - Leon"
    )
    assert (
        scope.scope_type
        is TerritorialScopeType.MUNICIPALITY
    )
    assert scope.municipality_id == 20
    assert scope.municipality_code == "20"
    assert (
        scope.municipality_name
        == "Leon de los Aldama"
    )
    assert scope.section_count == 787

    assert connection.session_calls == [
        {
            "readonly": True,
            "autocommit": False,
        }
    ]
    assert connection.rollback_count == 1
    assert connection.closed is True
    assert (
        connection.cursor_instance.closed
        is True
    )


def test_reads_global_scope():
    source, _ = source_for(
        [
            (
                1,
                "Acceso global",
                "GLOBAL",
                None,
                None,
                None,
                0,
            )
        ]
    )

    scopes = source.active_scopes(user_id=3)

    assert scopes[0].scope_type is (
        TerritorialScopeType.GLOBAL
    )
    assert scopes[0].municipality_id is None
    assert scopes[0].section_count == 0


def test_reads_section_set_without_single_municipality():
    source, _ = source_for(
        [
            (
                3,
                "Secciones regionales",
                "SECTION_SET",
                None,
                None,
                None,
                12,
            )
        ]
    )

    scopes = source.active_scopes(user_id=5)

    assert scopes[0].scope_type is (
        TerritorialScopeType.SECTION_SET
    )
    assert scopes[0].municipality_name is None
    assert scopes[0].section_count == 12


def test_returns_all_active_scopes():
    source, _ = source_for(
        [
            (
                2,
                "Leon",
                "MUNICIPALITY",
                20,
                "20",
                "Leon de los Aldama",
                787,
            ),
            (
                3,
                "Secciones adicionales",
                "SECTION_SET",
                None,
                None,
                None,
                2,
            ),
        ]
    )

    scopes = source.active_scopes(user_id=4)

    assert tuple(
        scope.scope_id
        for scope in scopes
    ) == (2, 3)


def test_uses_parameterized_query():
    source, connection = source_for([])

    source.active_scopes(user_id=4)

    executions = (
        connection.cursor_instance.executions
    )

    assert executions[0] == (
        "SET TRANSACTION ISOLATION LEVEL "
        "REPEATABLE READ READ ONLY",
        None,
    )
    assert executions[1] == (
        ACTIVE_SCOPES_SQL,
        (4,),
    )


@pytest.mark.parametrize(
    "user_id",
    [
        None,
        True,
        "4",
    ],
)
def test_rejects_invalid_user_id_type(user_id):
    source, connection = source_for([])

    with pytest.raises(TypeError):
        source.active_scopes(
            user_id=user_id
        )

    assert connection.session_calls == []


def test_rejects_non_positive_user_id():
    source, connection = source_for([])

    with pytest.raises(ValueError):
        source.active_scopes(user_id=0)

    assert connection.session_calls == []


def test_rejects_incompatible_factory():
    with pytest.raises(TypeError):
        PostgresTerritorialScopeProfileSource(
            object()
        )


def test_closes_transaction_when_query_fails():
    class FailingCursor(RecordingCursor):
        def execute(
            self,
            sql,
            parameters=None,
        ):
            super().execute(sql, parameters)

            if parameters is not None:
                raise RuntimeError(
                    "query failure"
                )

    connection = RecordingConnection([])
    connection.cursor_instance = (
        FailingCursor([])
    )

    source = (
        PostgresTerritorialScopeProfileSource(
            lambda: connection
        )
    )

    with pytest.raises(
        RuntimeError,
        match="query failure",
    ):
        source.active_scopes(user_id=4)

    assert connection.rollback_count == 1
    assert connection.closed is True
    assert (
        connection.cursor_instance.closed
        is True
    )
