from unittest.mock import MagicMock

import pytest

from heyti.security.postgres_scope_assignment import (
    PostgresTerritorialScopeRepository,
)
from heyti.security.scope_assignment import (
    TerritorialScopeType,
)


def make_repository():
    connection = MagicMock()
    cursor = MagicMock()
    connection.cursor.return_value = cursor

    repository = (
        PostgresTerritorialScopeRepository(
            lambda: connection
        )
    )

    return repository, connection, cursor


def test_assigns_municipality_atomically():
    repository, connection, cursor = (
        make_repository()
    )

    cursor.fetchall.side_effect = [
        [(7, "COORDINATOR")],
        [
            (1001, "1"),
            (1002, "2"),
        ],
    ]
    cursor.fetchone.side_effect = [
        (3,),
        (1, "Abasolo"),
        (20,),
        (30,),
    ]

    result = repository.assign_scope(
        user_id=7,
        scope_name="Abasolo",
        scope_type=(
            TerritorialScopeType.MUNICIPALITY
        ),
        municipality_id=1,
        section_codes=(),
        assigned_by_user_id=3,
    )

    assert result.assignment_id == 30
    assert result.scope_id == 20
    assert result.user_id == 7
    assert result.section_count == 2

    connection.set_session.assert_called_once_with(
        readonly=False,
        autocommit=False,
    )
    cursor.executemany.assert_called_once()
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_assigns_section_set_atomically():
    repository, connection, cursor = (
        make_repository()
    )

    cursor.fetchall.side_effect = [
        [(8, "PROMOTER")],
        [
            (1481, "1481"),
            (1482, "1482"),
        ],
    ]
    cursor.fetchone.side_effect = [
        (40,),
        (50,),
    ]

    result = repository.assign_scope(
        user_id=8,
        scope_name="Secciones prioritarias",
        scope_type=(
            TerritorialScopeType.SECTION_SET
        ),
        municipality_id=None,
        section_codes=("1481", "1482"),
        assigned_by_user_id=None,
    )

    assert result.scope_id == 40
    assert result.assignment_id == 50
    assert result.section_count == 2
    connection.commit.assert_called_once()


def test_assigns_global_to_administrator():
    repository, connection, cursor = (
        make_repository()
    )

    cursor.fetchall.side_effect = [
        [(3, "ADMINISTRATOR")],
    ]
    cursor.fetchone.side_effect = [
        (60,),
        (70,),
    ]

    result = repository.assign_scope(
        user_id=3,
        scope_name="Acceso estatal",
        scope_type=TerritorialScopeType.GLOBAL,
        municipality_id=None,
        section_codes=(),
        assigned_by_user_id=None,
    )

    assert result.section_count == 0
    cursor.executemany.assert_not_called()
    connection.commit.assert_called_once()


@pytest.mark.parametrize(
    "role_code, scope_type",
    [
        (
            "COORDINATOR",
            TerritorialScopeType.GLOBAL,
        ),
        (
            "PROMOTER",
            TerritorialScopeType.GLOBAL,
        ),
        (
            "ADMINISTRATOR",
            TerritorialScopeType.MUNICIPALITY,
        ),
        (
            "ADMINISTRATOR",
            TerritorialScopeType.SECTION_SET,
        ),
    ],
)
def test_rejects_incompatible_role_scope(
    role_code,
    scope_type,
):
    repository, connection, cursor = (
        make_repository()
    )

    cursor.fetchall.return_value = [
        (7, role_code),
    ]

    with pytest.raises(ValueError):
        repository.assign_scope(
            user_id=7,
            scope_name="Alcance invalido",
            scope_type=scope_type,
            municipality_id=(
                1
                if scope_type
                is TerritorialScopeType.MUNICIPALITY
                else None
            ),
            section_codes=(
                ("1481",)
                if scope_type
                is TerritorialScopeType.SECTION_SET
                else ()
            ),
            assigned_by_user_id=None,
        )

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    connection.close.assert_called_once()


def test_rejects_non_administrator_assigner():
    repository, connection, cursor = (
        make_repository()
    )

    cursor.fetchall.return_value = [
        (7, "COORDINATOR"),
    ]
    cursor.fetchone.return_value = None

    with pytest.raises(
        ValueError,
        match="administrador activo",
    ):
        repository.assign_scope(
            user_id=7,
            scope_name="Abasolo",
            scope_type=(
                TerritorialScopeType.MUNICIPALITY
            ),
            municipality_id=1,
            section_codes=(),
            assigned_by_user_id=9,
        )

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()


def test_rejects_missing_sections():
    repository, connection, cursor = (
        make_repository()
    )

    cursor.fetchall.side_effect = [
        [(8, "PROMOTER")],
        [(1481, "1481")],
    ]

    with pytest.raises(
        ValueError,
        match="9999",
    ):
        repository.assign_scope(
            user_id=8,
            scope_name="Secciones",
            scope_type=(
                TerritorialScopeType.SECTION_SET
            ),
            municipality_id=None,
            section_codes=("1481", "9999"),
            assigned_by_user_id=None,
        )

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()


def test_rejects_user_without_unique_active_role():
    repository, connection, cursor = (
        make_repository()
    )

    cursor.fetchall.return_value = []

    with pytest.raises(
        ValueError,
        match="unico",
    ):
        repository.assign_scope(
            user_id=999,
            scope_name="Abasolo",
            scope_type=(
                TerritorialScopeType.MUNICIPALITY
            ),
            municipality_id=1,
            section_codes=(),
            assigned_by_user_id=None,
        )

    connection.rollback.assert_called_once()


def test_rolls_back_database_error():
    repository, connection, cursor = (
        make_repository()
    )

    cursor.execute.side_effect = RuntimeError(
        "database error"
    )

    with pytest.raises(RuntimeError):
        repository.assign_scope(
            user_id=7,
            scope_name="Abasolo",
            scope_type=(
                TerritorialScopeType.MUNICIPALITY
            ),
            municipality_id=1,
            section_codes=(),
            assigned_by_user_id=None,
        )

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()
    cursor.close.assert_called_once()
    connection.close.assert_called_once()


def test_rejects_incompatible_factory():
    with pytest.raises(TypeError):
        PostgresTerritorialScopeRepository(
            object()
        )
