from unittest.mock import MagicMock

import pytest

from heyti.security.contracts import AccessRole
from heyti.security.postgres_provisioning import (
    PostgresUserProvisioningRepository,
)
from heyti.security.provisioning import (
    ProvisionedUser,
    UserProvisioningRequest,
    UserProvisioningService,
)


HASH = "$argon2id$test-hash"


def make_service():
    repository = MagicMock()
    repository.create_user.return_value = (
        ProvisionedUser(
            user_id=7,
            user_uuid="user-uuid",
            username="alex",
            display_name="Alex",
            role=AccessRole.ADMINISTRATOR,
            must_change=True,
        )
    )

    hasher = MagicMock()
    hasher.hash_password.return_value = HASH

    return (
        UserProvisioningService(
            repository,
            hasher,
        ),
        repository,
        hasher,
    )


def test_service_hashes_and_normalizes_user():
    service, repository, hasher = (
        make_service()
    )

    result = service.provision(
        UserProvisioningRequest(
            username="  ALEX  ",
            display_name="  Alex  ",
            password="temporary-password",
            role=AccessRole.ADMINISTRATOR,
        )
    )

    assert result.user_id == 7
    hasher.hash_password.assert_called_once_with(
        "temporary-password"
    )
    repository.create_user.assert_called_once_with(
        username="alex",
        display_name="Alex",
        credential_hash=HASH,
        role=AccessRole.ADMINISTRATOR,
        must_change=True,
        assigned_by_user_id=None,
    )


def test_service_never_sends_plain_password_to_repository():
    service, repository, _ = make_service()

    service.provision(
        UserProvisioningRequest(
            username="alex",
            display_name="Alex",
            password="plain-secret",
            role=AccessRole.ADMINISTRATOR,
        )
    )

    call_values = str(
        repository.create_user.call_args
    )

    assert "plain-secret" not in call_values
    assert HASH in call_values


@pytest.mark.parametrize(
    "candidate",
    [
        None,
        object(),
    ],
)
def test_service_requires_request_contract(candidate):
    service, repository, hasher = make_service()

    with pytest.raises(TypeError):
        service.provision(candidate)

    repository.create_user.assert_not_called()
    hasher.hash_password.assert_not_called()


@pytest.mark.parametrize(
    "candidate",
    [
        UserProvisioningRequest(
            username="",
            display_name="Alex",
            password="password",
            role=AccessRole.ADMINISTRATOR,
        ),
        UserProvisioningRequest(
            username="alex",
            display_name="",
            password="password",
            role=AccessRole.ADMINISTRATOR,
        ),
        UserProvisioningRequest(
            username="alex",
            display_name="Alex",
            password="",
            role=AccessRole.ADMINISTRATOR,
        ),
    ],
)
def test_service_rejects_empty_fields(candidate):
    service, repository, _ = make_service()

    with pytest.raises(ValueError):
        service.provision(candidate)

    repository.create_user.assert_not_called()


class CursorStub:
    def __init__(self, rows):
        self.rows = list(rows)
        self.calls = []
        self.closed = False

    def execute(self, statement, parameters):
        self.calls.append(
            (statement, parameters)
        )

    def fetchone(self):
        if not self.rows:
            return None

        return self.rows.pop(0)

    def close(self):
        self.closed = True


class ConnectionStub:
    def __init__(self, rows):
        self.cursor_instance = CursorStub(rows)
        self.session_arguments = None
        self.commits = 0
        self.rollbacks = 0
        self.closed = False

    def set_session(self, **kwargs):
        self.session_arguments = kwargs

    def cursor(self):
        return self.cursor_instance

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1

    def close(self):
        self.closed = True


def test_repository_creates_user_atomically():
    connection = ConnectionStub([
        (1,),
        (7, "user-uuid"),
    ])
    repository = (
        PostgresUserProvisioningRepository(
            lambda: connection
        )
    )

    result = repository.create_user(
        username="Alex",
        display_name="Alex",
        credential_hash=HASH,
        role=AccessRole.ADMINISTRATOR,
        must_change=True,
        assigned_by_user_id=None,
    )

    assert result == ProvisionedUser(
        user_id=7,
        user_uuid="user-uuid",
        username="alex",
        display_name="Alex",
        role=AccessRole.ADMINISTRATOR,
        must_change=True,
    )
    assert connection.session_arguments == {
        "readonly": False,
        "autocommit": False,
    }
    assert connection.commits == 1
    assert connection.rollbacks == 0
    assert connection.closed is True
    assert connection.cursor_instance.closed is True
    assert len(
        connection.cursor_instance.calls
    ) == 4


def test_repository_rolls_back_when_role_is_missing():
    connection = ConnectionStub([None])
    repository = (
        PostgresUserProvisioningRepository(
            lambda: connection
        )
    )

    with pytest.raises(
        ValueError,
        match="rol solicitado",
    ):
        repository.create_user(
            username="alex",
            display_name="Alex",
            credential_hash=HASH,
            role=AccessRole.ADMINISTRATOR,
            must_change=True,
            assigned_by_user_id=None,
        )

    assert connection.commits == 0
    assert connection.rollbacks == 1
    assert connection.closed is True
    assert connection.cursor_instance.closed is True


def test_repository_rejects_plaintext_credential():
    connection_factory = MagicMock()
    repository = (
        PostgresUserProvisioningRepository(
            connection_factory
        )
    )

    with pytest.raises(
        ValueError,
        match="Argon2id",
    ):
        repository.create_user(
            username="alex",
            display_name="Alex",
            credential_hash="plain-password",
            role=AccessRole.ADMINISTRATOR,
            must_change=True,
            assigned_by_user_id=None,
        )

    connection_factory.assert_not_called()


def test_rejects_incompatible_dependencies():
    with pytest.raises(TypeError):
        UserProvisioningService(
            object(),
            MagicMock(),
        )

    with pytest.raises(TypeError):
        PostgresUserProvisioningRepository(
            object()
        )
