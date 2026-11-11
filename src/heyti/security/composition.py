from dataclasses import dataclass

from heyti.security.authentication import (
    AuthenticationService,
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


@dataclass(frozen=True)
class SecurityComposition:
    credential_repository: (
        PostgresCredentialRepository
    )
    credential_hasher: Argon2CredentialHasher
    authentication_service: AuthenticationService
    authorization_source: (
        PostgresAuthorizationSource
    )
    authorization_service: AuthorizationService
    session_service: AuthenticatedSessionService


def compose_security(
    *,
    connection_factory,
    session_manager: SessionManager,
) -> SecurityComposition:
    if not callable(connection_factory):
        raise TypeError(
            "connection_factory debe ser invocable"
        )

    if not isinstance(
        session_manager,
        SessionManager,
    ):
        raise TypeError(
            "session_manager debe ser SessionManager"
        )

    credential_repository = (
        PostgresCredentialRepository(
            connection_factory
        )
    )
    credential_hasher = Argon2CredentialHasher()

    authentication_service = (
        AuthenticationService(
            credential_repository,
            credential_hasher,
        )
    )

    authorization_source = (
        PostgresAuthorizationSource(
            connection_factory
        )
    )
    authorization_service = AuthorizationService(
        authorization_source
    )

    session_service = (
        AuthenticatedSessionService(
            session_manager
        )
    )

    return SecurityComposition(
        credential_repository=(
            credential_repository
        ),
        credential_hasher=credential_hasher,
        authentication_service=(
            authentication_service
        ),
        authorization_source=(
            authorization_source
        ),
        authorization_service=(
            authorization_service
        ),
        session_service=session_service,
    )
