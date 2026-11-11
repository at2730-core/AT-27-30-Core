from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock

import pytest

from heyti.security.authentication import (
    AuthenticationResult,
    AuthenticationService,
    AuthenticationStatus,
)
from heyti.security.contracts import AccessRole
from heyti.security.credentials import (
    PasswordVerification,
)
from heyti.security.postgres_credentials import (
    CredentialRecord,
)


NOW = datetime(
    2026,
    11,
    11,
    18,
    0,
    tzinfo=timezone.utc,
)


def make_record(
    *,
    active=True,
    role=AccessRole.COORDINATOR,
    locked_until=None,
    must_change=False,
):
    return CredentialRecord(
        user_id=7,
        username="alex",
        display_name="Alex",
        active=active,
        credential_hash="$argon2id$stored",
        failed_attempts=0,
        locked_until=locked_until,
        must_change=must_change,
        role=role,
    )


def make_service(
    record,
    verification,
):
    repository = MagicMock()
    repository.find_by_username.return_value = (
        record
    )

    hasher = MagicMock()
    hasher.hash_password.return_value = (
        "$argon2id$dummy-or-replacement"
    )
    hasher.verify_password.return_value = (
        verification
    )

    service = AuthenticationService(
        repository,
        hasher,
        clock=lambda: NOW,
    )

    return service, repository, hasher


def test_authenticates_valid_credentials():
    service, repository, _ = make_service(
        make_record(),
        PasswordVerification(
            valid=True,
            needs_rehash=False,
        ),
    )

    result = service.authenticate(
        "alex",
        "correct-password",
    )

    assert result == AuthenticationResult(
        status=AuthenticationStatus.AUTHENTICATED,
        user_id=7,
        username="alex",
        display_name="Alex",
        role=AccessRole.COORDINATOR,
    )
    assert result.credentials_valid is True
    assert result.session_allowed is True
    repository.record_success.assert_called_once_with(
        7
    )
    repository.record_failure.assert_not_called()
    repository.replace_hash.assert_not_called()


def test_rejects_wrong_password_and_records_failure():
    service, repository, _ = make_service(
        make_record(),
        PasswordVerification(valid=False),
    )

    result = service.authenticate(
        "alex",
        "wrong-password",
    )

    assert result.status is (
        AuthenticationStatus.INVALID_CREDENTIALS
    )
    assert result.credentials_valid is False
    assert result.session_allowed is False

    repository.record_failure.assert_called_once_with(
        7,
        max_attempts=5,
        lock_seconds=900,
    )
    repository.record_success.assert_not_called()


def test_unknown_user_uses_dummy_verification():
    service, repository, hasher = make_service(
        None,
        PasswordVerification(valid=False),
    )

    result = service.authenticate(
        "unknown",
        "some-password",
    )

    assert result.status is (
        AuthenticationStatus.INVALID_CREDENTIALS
    )

    hasher.verify_password.assert_called_once_with(
        "$argon2id$dummy-or-replacement",
        "some-password",
    )
    repository.record_failure.assert_not_called()
    repository.record_success.assert_not_called()


def test_locked_user_is_not_authenticated():
    service, repository, hasher = make_service(
        make_record(
            locked_until=NOW + timedelta(
                minutes=10
            )
        ),
        PasswordVerification(valid=True),
    )

    result = service.authenticate(
        "alex",
        "correct-password",
    )

    assert result.status is (
        AuthenticationStatus.LOCKED
    )
    hasher.verify_password.assert_called_once()
    repository.record_failure.assert_not_called()
    repository.record_success.assert_not_called()


@pytest.mark.parametrize(
    "record",
    [
        make_record(active=False),
        make_record(role=None),
    ],
)
def test_ineligible_user_returns_uniform_failure(
    record,
):
    service, repository, hasher = make_service(
        record,
        PasswordVerification(valid=True),
    )

    result = service.authenticate(
        "alex",
        "correct-password",
    )

    assert result == AuthenticationResult(
        status=(
            AuthenticationStatus.INVALID_CREDENTIALS
        )
    )
    hasher.verify_password.assert_called_once()
    repository.record_failure.assert_not_called()
    repository.record_success.assert_not_called()


def test_requires_password_change_without_session():
    service, repository, _ = make_service(
        make_record(must_change=True),
        PasswordVerification(valid=True),
    )

    result = service.authenticate(
        "alex",
        "correct-password",
    )

    assert result.status is (
        AuthenticationStatus.PASSWORD_CHANGE_REQUIRED
    )
    assert result.credentials_valid is True
    assert result.session_allowed is False
    repository.record_success.assert_called_once_with(
        7
    )


def test_rehashes_after_success():
    service, repository, hasher = make_service(
        make_record(),
        PasswordVerification(
            valid=True,
            needs_rehash=True,
        ),
    )

    result = service.authenticate(
        "alex",
        "correct-password",
    )

    assert result.session_allowed is True
    hasher.hash_password.assert_any_call(
        "correct-password"
    )
    repository.replace_hash.assert_called_once_with(
        7,
        "$argon2id$dummy-or-replacement",
    )


def test_expired_lock_allows_authentication():
    service, repository, _ = make_service(
        make_record(
            locked_until=NOW - timedelta(
                seconds=1
            )
        ),
        PasswordVerification(valid=True),
    )

    result = service.authenticate(
        "alex",
        "correct-password",
    )

    assert result.status is (
        AuthenticationStatus.AUTHENTICATED
    )
    repository.record_success.assert_called_once()


@pytest.mark.parametrize(
    ("max_attempts", "lock_seconds", "error"),
    [
        (0, 900, ValueError),
        (5, 0, ValueError),
        (True, 900, TypeError),
        (5, True, TypeError),
    ],
)
def test_rejects_invalid_policy(
    max_attempts,
    lock_seconds,
    error,
):
    repository = MagicMock()
    hasher = MagicMock()

    with pytest.raises(error):
        AuthenticationService(
            repository,
            hasher,
            max_attempts=max_attempts,
            lock_seconds=lock_seconds,
        )
