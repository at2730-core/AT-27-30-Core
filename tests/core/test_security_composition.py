import pytest

from heyti.security.authentication import (
    AuthenticationService,
)
from heyti.security.composition import (
    SecurityComposition,
    compose_security,
)
from heyti.security.credentials import (
    Argon2CredentialHasher,
)
from heyti.security.postgres_authorization import (
    PostgresAuthorizationSource,
)
from heyti.security.postgres_credentials import (
    PostgresCredentialRepository,
)
from heyti.security.service import (
    AuthorizationService,
)
from heyti.security.sessions import (
    AuthenticatedSessionService,
)
from heyti.session.session_manager import (
    SessionManager,
)


def test_composes_all_security_components():
    marker = object()

    def connect():
        return marker

    manager = SessionManager()

    composition = compose_security(
        connection_factory=connect,
        session_manager=manager,
    )

    assert isinstance(
        composition,
        SecurityComposition,
    )
    assert isinstance(
        composition.credential_repository,
        PostgresCredentialRepository,
    )
    assert isinstance(
        composition.credential_hasher,
        Argon2CredentialHasher,
    )
    assert isinstance(
        composition.authentication_service,
        AuthenticationService,
    )
    assert isinstance(
        composition.authorization_source,
        PostgresAuthorizationSource,
    )
    assert isinstance(
        composition.authorization_service,
        AuthorizationService,
    )
    assert isinstance(
        composition.session_service,
        AuthenticatedSessionService,
    )


def test_composition_uses_shared_connection_factory():
    calls = []

    def connect():
        calls.append("called")
        raise RuntimeError("probe")

    composition = compose_security(
        connection_factory=connect,
        session_manager=SessionManager(),
    )

    with pytest.raises(
        RuntimeError,
        match="probe",
    ):
        (
            composition.credential_repository
            .find_by_username("alex")
        )

    with pytest.raises(
        RuntimeError,
        match="probe",
    ):
        (
            composition.authorization_source
            .grants(
                __import__(
                    "heyti.security.contracts",
                    fromlist=["AccessRole"],
                ).AccessRole.ADMINISTRATOR
            )
        )

    assert calls == ["called", "called"]


def test_composition_uses_runtime_session_manager():
    manager = SessionManager()

    composition = compose_security(
        connection_factory=lambda: object(),
        session_manager=manager,
    )

    authentication = __import__(
        "heyti.security.authentication",
        fromlist=[
            "AuthenticationResult",
            "AuthenticationStatus",
        ],
    )

    contracts = __import__(
        "heyti.security.contracts",
        fromlist=["AccessRole"],
    )

    session = (
        composition.session_service
        .create_session(
            authentication.AuthenticationResult(
                status=(
                    authentication
                    .AuthenticationStatus
                    .AUTHENTICATED
                ),
                user_id=7,
                username="alex",
                display_name="Alex",
                role=(
                    contracts
                    .AccessRole
                    .COORDINATOR
                ),
            )
        )
    )

    assert manager.get(
        session.session_id
    ) is session


@pytest.mark.parametrize(
    ("connection_factory", "session_manager"),
    [
        (None, SessionManager()),
        (lambda: object(), None),
    ],
)
def test_rejects_invalid_dependencies(
    connection_factory,
    session_manager,
):
    with pytest.raises(TypeError):
        compose_security(
            connection_factory=connection_factory,
            session_manager=session_manager,
        )
