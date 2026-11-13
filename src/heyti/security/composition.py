from dataclasses import dataclass

from heyti.security.authentication import (
    AuthenticationService,
)
from heyti.security.credentials import (
    Argon2CredentialHasher,
)
from heyti.security.password_change import (
    PasswordChangeService,
)
from heyti.security.postgres_authorization import (
    PostgresAuthorizationSource,
)
from heyti.security.postgres_credentials import (
    PostgresCredentialRepository,
)
from heyti.security.postgres_scope_profile import (
    PostgresTerritorialScopeProfileSource,
)
from heyti.security.scope_profile import (
    TerritorialScopeProfileService,
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
    password_change_service: PasswordChangeService
    authorization_source: (
        PostgresAuthorizationSource
    )
    authorization_service: AuthorizationService
    scope_profile_source: (
        PostgresTerritorialScopeProfileSource
    )
    scope_profile_service: (
        TerritorialScopeProfileService
    )
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

    password_change_service = (
        PasswordChangeService(
            authentication_service,
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

    scope_profile_source = (
        PostgresTerritorialScopeProfileSource(
            connection_factory
        )
    )
    scope_profile_service = (
        TerritorialScopeProfileService(
            scope_profile_source
        )
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
        password_change_service=(
            password_change_service
        ),
        authorization_source=(
            authorization_source
        ),
        authorization_service=(
            authorization_service
        ),
        scope_profile_source=(
            scope_profile_source
        ),
        scope_profile_service=(
            scope_profile_service
        ),
        session_service=session_service,
    )
