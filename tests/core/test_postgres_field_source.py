from unittest.mock import MagicMock, patch

import pytest

from heyti.capabilities.describe_field.postgres_source import (
    PostgresFieldSource,
    build_environment_connection_factory,
)


def make_source():
    connection = MagicMock()
    cursor = connection.cursor.return_value

    source = PostgresFieldSource(
        lambda: connection
    )

    return source, connection, cursor


def test_postgres_field_summary_is_read_only():
    source, connection, cursor = make_source()

    cursor.fetchone.return_value = (45, 45, 0, 0)
    cursor.fetchall.return_value = [
        ("LIDER", 4),
        ("SIMPATIZANTE", 41),
    ]

    summary = source.summary()

    assert summary == {
        "total_records": 45,
        "geolocated_records": 45,
        "records_without_geometry": 0,
        "unassigned_records": 0,
        "by_role": {
            "LIDER": 4,
            "SIMPATIZANTE": 41,
        },
    }
    connection.set_session.assert_called_once_with(
        readonly=True,
        autocommit=False,
    )
    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()


def test_postgres_field_map_uses_parameterized_filter():
    source, connection, cursor = make_source()

    cursor.fetchall.return_value = [
        (
            "uuid-example",
            "1001",
            "LIDER",
            -101.68,
            21.12,
        )
    ]

    records = source.map_points(
        section_code="1001"
    )

    assert records == [
        {
            "actor_uuid": "uuid-example",
            "section_code": "1001",
            "role_code": "LIDER",
            "longitude": -101.68,
            "latitude": 21.12,
        }
    ]

    map_call = cursor.execute.call_args_list[-1]

    assert "%s" in map_call.args[0]
    assert map_call.args[1] == ("1001",)
    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()


def test_postgres_field_source_closes_after_error():
    source, connection, cursor = make_source()

    cursor.execute.side_effect = RuntimeError(
        "database failure"
    )

    with pytest.raises(
        RuntimeError,
        match="database failure",
    ):
        source.summary()

    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()



def test_environment_factory_uses_explicit_configuration():
    environment = {
        "HEYTI_DB_HOST": "db.example",
        "HEYTI_DB_PORT": "5544",
        "HEYTI_DB_NAME": "heyti_test",
        "HEYTI_DB_USER": "heyti_user",
        "HEYTI_DB_PASSWORD": "secret",
    }

    factory = build_environment_connection_factory(
        environment
    )

    marker = object()

    with patch(
        "heyti.capabilities.describe_field."
        "postgres_source.psycopg2.connect",
        return_value=marker,
    ) as connect:
        assert factory() is marker

    connect.assert_called_once_with(
        host="db.example",
        port=5544,
        dbname="heyti_test",
        user="heyti_user",
        password="secret",
        connect_timeout=5,
        application_name="HEYTI_FIELD_RUNTIME",
    )
