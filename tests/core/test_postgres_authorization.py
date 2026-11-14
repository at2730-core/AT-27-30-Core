from unittest.mock import MagicMock

import pytest

from heyti.security.contracts import (
    AccessRole,
    PermissionGrant,
    PermissionScope,
)
from heyti.security.postgres_authorization import (
    GRANTS_SQL,
    IDENTITY_SQL,
    PostgresAuthorizationSource,
)


def make_source():
    connection = MagicMock()
    cursor = connection.cursor.return_value

    source = PostgresAuthorizationSource(
        lambda: connection
    )

    return source, connection, cursor


def test_identity_loads_role_teams_and_sections():
    source, connection, cursor = make_source()

    cursor.fetchall.return_value = [
        (
            7,
            True,
            "COORDINATOR",
            41,
            "SECTION_SET",
            "1481",
            None,
        ),
        (
            7,
            True,
            "COORDINATOR",
            42,
            "SECTION_SET",
            "1482",
            None,
        ),
    ]

    identity = source.identity(
        user_id=7,
        session_id="  SESSION-7  ",
    )

    assert identity is not None
    assert identity.user_id == 7
    assert identity.session_id == "SESSION-7"
    assert identity.role is AccessRole.COORDINATOR
    assert identity.active is True
    assert identity.team_ids == frozenset({41, 42})
    assert identity.territorial_access.global_access is False
    assert identity.territorial_access.municipality_codes == (
        frozenset()
    )
    assert identity.territorial_access.section_codes == (
        frozenset({"1481", "1482"})
    )

    query_call = cursor.execute.call_args_list[-1]

    assert query_call.args[0] == IDENTITY_SQL
    assert query_call.args[1] == (7,)
    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()


def test_identity_loads_municipality_and_sections():
    source, _, cursor = make_source()

    cursor.fetchall.return_value = [
        (
            4,
            True,
            "COORDINATOR",
            None,
            "MUNICIPALITY",
            "1261",
            "20",
        ),
        (
            4,
            True,
            "COORDINATOR",
            None,
            "MUNICIPALITY",
            "1262",
            "20",
        ),
    ]

    identity = source.identity(
        user_id=4,
        session_id="COORDINATOR-SESSION",
    )

    assert identity is not None
    assert identity.role is AccessRole.COORDINATOR
    assert identity.territorial_access.global_access is False
    assert identity.territorial_access.municipality_codes == (
        frozenset({"20"})
    )
    assert identity.territorial_access.section_codes == (
        frozenset({"1261", "1262"})
    )


def test_identity_loads_global_access():
    source, _, cursor = make_source()

    cursor.fetchall.return_value = [
        (
            1,
            True,
            "ADMINISTRATOR",
            None,
            "GLOBAL",
            None,
            None,
        )
    ]

    identity = source.identity(
        user_id=1,
        session_id="ADMIN-SESSION",
    )

    assert identity is not None
    assert identity.role is AccessRole.ADMINISTRATOR
    assert identity.territorial_access.global_access is True
    assert identity.territorial_access.municipality_codes == (
        frozenset()
    )
    assert identity.territorial_access.section_codes == (
        frozenset()
    )


def test_identity_returns_none_for_unknown_user():
    source, connection, cursor = make_source()

    cursor.fetchall.return_value = []

    assert source.identity(
        user_id=99,
        session_id="SESSION-99",
    ) is None

    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()


def test_identity_returns_none_without_single_role():
    source, _, cursor = make_source()

    cursor.fetchall.return_value = [
        (
            7,
            True,
            None,
            None,
            None,
            None,
            None,
        )
    ]

    assert source.identity(
        user_id=7,
        session_id="SESSION-7",
    ) is None


def test_grants_map_scope_and_audit_requirement():
    source, connection, cursor = make_source()

    cursor.fetchall.return_value = [
        (
            "FIELD_MAP_READ",
            "ASSIGNED_TERRITORY",
            False,
        ),
        (
            "FIELD_PERSONAL_DATA_READ",
            "ASSIGNED_TEAM",
            True,
        ),
    ]

    grants = source.grants(
        AccessRole.COORDINATOR
    )

    assert grants == (
        PermissionGrant(
            permission_code="FIELD_MAP_READ",
            scope=PermissionScope.ASSIGNED_TERRITORY,
            audit_required=False,
        ),
        PermissionGrant(
            permission_code="FIELD_PERSONAL_DATA_READ",
            scope=PermissionScope.ASSIGNED_TEAM,
            audit_required=True,
        ),
    )

    query_call = cursor.execute.call_args_list[-1]

    assert query_call.args[0] == GRANTS_SQL
    assert query_call.args[1] == ("COORDINATOR",)
    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()


def test_source_closes_connection_after_error():
    source, connection, cursor = make_source()

    cursor.execute.side_effect = RuntimeError(
        "database failure"
    )

    with pytest.raises(
        RuntimeError,
        match="database failure",
    ):
        source.identity(
            user_id=7,
            session_id="SESSION-7",
        )

    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()


@pytest.mark.parametrize(
    ("user_id", "session_id", "error"),
    [
        (True, "SESSION", TypeError),
        ("7", "SESSION", TypeError),
        (0, "SESSION", ValueError),
        (7, 123, TypeError),
        (7, "   ", ValueError),
    ],
)
def test_identity_rejects_invalid_inputs(
    user_id,
    session_id,
    error,
):
    source, connection, _ = make_source()

    with pytest.raises(error):
        source.identity(
            user_id=user_id,
            session_id=session_id,
        )

    connection.assert_not_called()


def test_grants_requires_access_role():
    source, connection, _ = make_source()

    with pytest.raises(
        TypeError,
        match="role debe ser AccessRole",
    ):
        source.grants("COORDINATOR")

    connection.assert_not_called()
