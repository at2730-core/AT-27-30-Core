from unittest.mock import MagicMock

import pytest

from heyti.security.authentication import (
    AuthenticationResult,
    AuthenticationStatus,
)
from heyti.security.contracts import AccessRole
from heyti.security.password_change import (
    InvalidPasswordChangeCredentialsError,
    PasswordChangeLockedError,
    PasswordChangeResult,
    PasswordChangeService,
)
from heyti.security.postgres_credentials import (
    PASSWORD_CHANGE_SQL,
    PostgresCredentialRepository,
)


def authenticated_result(
    status=(
        AuthenticationStatus
        .PASSWORD_CHANGE_REQUIRED
    ),
):
    return AuthenticationResult(
        status=status,
        user_id=7,
        username="jose.de.jesus",
        display_name="Jose de Jesus",
        role=AccessRole.COORDINATOR,
    )


def make_service(result=None):
    authentication_service = MagicMock()
    authentication_service.authenticate.return_value = (
        authenticated_result()
        if result is None
        else result
    )

    repository = MagicMock()
    hasher = MagicMock()
    hasher.hash_password.return_value = (
        "$argon2id$new-hash"
    )

    service = PasswordChangeService(
        authentication_service,
        repository,
        hasher,
    )

    return (
        service,
        authentication_service,
        repository,
        hasher,
    )


def test_changes_required_password():
    (
        service,
        authentication_service,
        repository,
        hasher,
    ) = make_service()

    result = service.change_password(
        username="  jose.de.jesus  ",
        current_password="temporary-password",
        new_password="new-secure-password",
        confirmation="new-secure-password",
    )

    assert result == PasswordChangeResult(
        user_id=7,
        username="jose.de.jesus",
        display_name="Jose de Jesus",
    )

    authentication_service.authenticate        .assert_called_once_with(
            "jose.de.jesus",
            "temporary-password",
        )
    hasher.hash_password.assert_called_once_with(
        "new-secure-password"
    )
    repository.complete_password_change        .assert_called_once_with(
            7,
            "$argon2id$new-hash",
        )


def test_allows_voluntary_password_change():
    result = authenticated_result(
        AuthenticationStatus.AUTHENTICATED
    )
    service, _, repository, _ = make_service(
        result
    )

    service.change_password(
        username="jose.de.jesus",
        current_password="current-password",
        new_password="replacement-password",
        confirmation="replacement-password",
    )

    repository.complete_password_change        .assert_called_once()


def test_rejects_invalid_current_password():
    service, _, repository, hasher = make_service(
        AuthenticationResult(
            status=(
                AuthenticationStatus
                .INVALID_CREDENTIALS
            )
        )
    )

    with pytest.raises(
        InvalidPasswordChangeCredentialsError
    ):
        service.change_password(
            username="jose.de.jesus",
            current_password="wrong-password",
            new_password="replacement-password",
            confirmation="replacement-password",
        )

    repository.complete_password_change        .assert_not_called()
    hasher.hash_password.assert_not_called()


def test_rejects_locked_credential():
    service, _, repository, hasher = make_service(
        AuthenticationResult(
            status=AuthenticationStatus.LOCKED
        )
    )

    with pytest.raises(
        PasswordChangeLockedError
    ):
        service.change_password(
            username="jose.de.jesus",
            current_password="current-password",
            new_password="replacement-password",
            confirmation="replacement-password",
        )

    repository.complete_password_change        .assert_not_called()
    hasher.hash_password.assert_not_called()


def test_rejects_mismatched_confirmation():
    service, authentication, repository, _ = (
        make_service()
    )

    with pytest.raises(
        ValueError,
        match="confirmacion",
    ):
        service.change_password(
            username="jose.de.jesus",
            current_password="current-password",
            new_password="replacement-password",
            confirmation="different-password",
        )

    authentication.authenticate.assert_not_called()
    repository.complete_password_change        .assert_not_called()


def test_rejects_reused_password():
    service, authentication, repository, _ = (
        make_service()
    )

    with pytest.raises(
        ValueError,
        match="debe ser diferente",
    ):
        service.change_password(
            username="jose.de.jesus",
            current_password="same-password",
            new_password="same-password",
            confirmation="same-password",
        )

    authentication.authenticate.assert_not_called()
    repository.complete_password_change        .assert_not_called()


@pytest.mark.parametrize(
    "field_name, value",
    [
        ("username", ""),
        ("current_password", ""),
        ("new_password", ""),
        ("confirmation", ""),
    ],
)
def test_rejects_empty_fields(
    field_name,
    value,
):
    service, _, repository, _ = make_service()

    payload = {
        "username": "jose.de.jesus",
        "current_password": "current-password",
        "new_password": "new-password",
        "confirmation": "new-password",
    }
    payload[field_name] = value

    with pytest.raises(ValueError):
        service.change_password(**payload)

    repository.complete_password_change        .assert_not_called()


def test_repository_completes_password_change():
    connection = MagicMock()
    cursor = connection.cursor.return_value
    cursor.fetchone.return_value = (7,)

    repository = PostgresCredentialRepository(
        lambda: connection
    )

    repository.complete_password_change(
        7,
        "$argon2id$new-hash",
    )

    cursor.execute.assert_called_once_with(
        PASSWORD_CHANGE_SQL,
        (
            "$argon2id$new-hash",
            7,
        ),
    )
    connection.commit.assert_called_once()
    connection.rollback.assert_not_called()
    connection.close.assert_called_once()


def test_repository_rejects_missing_credential():
    connection = MagicMock()
    cursor = connection.cursor.return_value
    cursor.fetchone.return_value = None

    repository = PostgresCredentialRepository(
        lambda: connection
    )

    with pytest.raises(
        ValueError,
        match="no existe",
    ):
        repository.complete_password_change(
            999,
            "$argon2id$new-hash",
        )

    connection.rollback.assert_called_once()
    connection.commit.assert_not_called()


def test_rejects_incompatible_dependencies():
    authentication = MagicMock()
    authentication.authenticate = MagicMock()

    repository = MagicMock()
    repository.complete_password_change = (
        MagicMock()
    )

    hasher = MagicMock()
    hasher.hash_password = MagicMock()

    with pytest.raises(TypeError):
        PasswordChangeService(
            object(),
            repository,
            hasher,
        )

    with pytest.raises(TypeError):
        PasswordChangeService(
            authentication,
            object(),
            hasher,
        )

    with pytest.raises(TypeError):
        PasswordChangeService(
            authentication,
            repository,
            object(),
        )
