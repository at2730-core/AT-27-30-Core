from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from heyti.security.contracts import AccessRole
from heyti.security.postgres_credentials import (
    CREDENTIAL_SQL,
    FAILURE_SQL,
    REHASH_SQL,
    SUCCESS_SQL,
    CredentialRecord,
    PostgresCredentialRepository,
)


def make_repository():
    connection = MagicMock()
    cursor = connection.cursor.return_value

    repository = PostgresCredentialRepository(
        lambda: connection
    )

    return repository, connection, cursor


def test_find_by_username_maps_record():
    repository, connection, cursor = (
        make_repository()
    )
    locked_until = datetime(
        2026,
        11,
        11,
        18,
        0,
        tzinfo=timezone.utc,
    )

    cursor.fetchone.return_value = (
        7,
        "alex",
        "Alex",
        True,
        "$argon2id$example",
        2,
        locked_until,
        False,
        "COORDINATOR",
    )

    record = repository.find_by_username(
        "  Alex  "
    )

    assert record == CredentialRecord(
        user_id=7,
        username="alex",
        display_name="Alex",
        active=True,
        credential_hash="$argon2id$example",
        failed_attempts=2,
        locked_until=locked_until,
        must_change=False,
        role=AccessRole.COORDINATOR,
    )

    query_call = cursor.execute.call_args_list[-1]
    assert query_call.args == (
        CREDENTIAL_SQL,
        ("Alex",),
    )
    connection.set_session.assert_called_once_with(
        readonly=True,
        autocommit=False,
    )
    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()


def test_find_by_username_returns_none():
    repository, connection, cursor = (
        make_repository()
    )
    cursor.fetchone.return_value = None

    assert repository.find_by_username(
        "unknown"
    ) is None

    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()


def test_record_failure_is_transactional():
    repository, connection, cursor = (
        make_repository()
    )

    repository.record_failure(
        7,
        max_attempts=5,
        lock_seconds=900,
    )

    cursor.execute.assert_called_once_with(
        FAILURE_SQL,
        (5, 900, 7),
    )
    connection.set_session.assert_called_once_with(
        readonly=False,
        autocommit=False,
    )
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    connection.close.assert_called_once()


def test_record_success_resets_credential_state():
    repository, connection, cursor = (
        make_repository()
    )

    repository.record_success(7)

    cursor.execute.assert_called_once_with(
        SUCCESS_SQL,
        (7,),
    )
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    connection.close.assert_called_once()


def test_replace_hash_is_parameterized():
    repository, connection, cursor = (
        make_repository()
    )
    credential_hash = "$argon2id$updated"

    repository.replace_hash(
        7,
        credential_hash,
    )

    cursor.execute.assert_called_once_with(
        REHASH_SQL,
        (credential_hash, 7),
    )
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    connection.close.assert_called_once()


def test_write_rolls_back_after_error():
    repository, connection, cursor = (
        make_repository()
    )
    cursor.execute.side_effect = RuntimeError(
        "database failure"
    )

    with pytest.raises(
        RuntimeError,
        match="database failure",
    ):
        repository.record_success(7)

    connection.commit.assert_not_called()
    connection.rollback.assert_called_once()
    connection.close.assert_called_once()


@pytest.mark.parametrize(
    ("user_id", "error"),
    [
        (True, TypeError),
        ("7", TypeError),
        (0, ValueError),
    ],
)
def test_write_rejects_invalid_user_id(
    user_id,
    error,
):
    repository, connection, _ = (
        make_repository()
    )

    with pytest.raises(error):
        repository.record_success(user_id)

    connection.assert_not_called()


def test_rejects_non_argon2_hash():
    repository, connection, _ = (
        make_repository()
    )

    with pytest.raises(
        ValueError,
        match="debe ser Argon2id",
    ):
        repository.replace_hash(
            7,
            "plaintext-password",
        )

    connection.assert_not_called()


def test_rejects_invalid_factory():
    with pytest.raises(TypeError):
        PostgresCredentialRepository(
            connection_factory=None
        )
