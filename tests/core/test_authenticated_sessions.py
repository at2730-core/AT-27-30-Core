from datetime import datetime, timedelta, timezone

import pytest

from heyti.security.authentication import (
    AuthenticationResult,
    AuthenticationStatus,
)
from heyti.security.contracts import AccessRole
from heyti.security.sessions import (
    AuthenticatedSession,
    AuthenticatedSessionService,
)
from heyti.session.session_manager import (
    SessionManager,
)


NOW = datetime(
    2026,
    11,
    11,
    18,
    0,
    tzinfo=timezone.utc,
)
TOKEN = "A" * 43


def authenticated_result():
    return AuthenticationResult(
        status=AuthenticationStatus.AUTHENTICATED,
        user_id=7,
        username="alex",
        display_name="Alex",
        role=AccessRole.COORDINATOR,
    )


def make_service(
    manager=None,
    clock=None,
    token_factory=None,
):
    manager = manager or SessionManager()

    service = AuthenticatedSessionService(
        manager,
        ttl_seconds=3600,
        clock=clock or (lambda: NOW),
        token_factory=(
            token_factory or (lambda: TOKEN)
        ),
    )

    return service, manager


def test_creates_authenticated_session():
    service, manager = make_service()

    session = service.create_session(
        authenticated_result()
    )

    assert session == AuthenticatedSession(
        session_id=TOKEN,
        user_id=7,
        username="alex",
        display_name="Alex",
        role=AccessRole.COORDINATOR,
        created_at=NOW,
        expires_at=NOW + timedelta(hours=1),
    )
    assert manager.get(TOKEN) is session
    assert manager.count() == 1


def test_resolves_active_session():
    service, _ = make_service()

    created = service.create_session(
        authenticated_result()
    )

    assert service.resolve(TOKEN) is created


def test_expired_session_is_removed():
    current = [NOW]
    service, manager = make_service(
        clock=lambda: current[0]
    )

    service.create_session(
        authenticated_result()
    )

    current[0] = NOW + timedelta(
        hours=1,
        seconds=1,
    )

    assert service.resolve(TOKEN) is None
    assert manager.exists(TOKEN) is False


def test_revoke_removes_session():
    service, manager = make_service()

    service.create_session(
        authenticated_result()
    )
    service.revoke(TOKEN)

    assert manager.exists(TOKEN) is False


@pytest.mark.parametrize(
    "status",
    [
        AuthenticationStatus.INVALID_CREDENTIALS,
        AuthenticationStatus.LOCKED,
        (
            AuthenticationStatus
            .PASSWORD_CHANGE_REQUIRED
        ),
    ],
)
def test_rejects_non_session_authentication(
    status,
):
    service, manager = make_service()

    result = AuthenticationResult(
        status=status
    )

    with pytest.raises(
        ValueError,
        match="no permite crear",
    ):
        service.create_session(result)

    assert manager.count() == 0


def test_rejects_incomplete_authentication():
    service, manager = make_service()

    result = AuthenticationResult(
        status=AuthenticationStatus.AUTHENTICATED,
        user_id=7,
    )

    with pytest.raises(
        ValueError,
        match="incompleta",
    ):
        service.create_session(result)

    assert manager.count() == 0


def test_retries_token_collision():
    manager = SessionManager()
    manager.create(
        TOKEN,
        {"existing": True},
    )

    candidates = iter([
        TOKEN,
        "B" * 43,
    ])

    service, _ = make_service(
        manager=manager,
        token_factory=lambda: next(candidates),
    )

    session = service.create_session(
        authenticated_result()
    )

    assert session.session_id == "B" * 43
    assert manager.count() == 2


def test_rejects_short_token():
    service, manager = make_service(
        token_factory=lambda: "short"
    )

    with pytest.raises(
        ValueError,
        match="demasiado corto",
    ):
        service.create_session(
            authenticated_result()
        )

    assert manager.count() == 0


def test_resolve_ignores_legacy_session():
    manager = SessionManager()
    manager.create(
        TOKEN,
        {
            "transport": "HTTP",
            "scope": "LOCAL",
        },
    )

    service, _ = make_service(
        manager=manager
    )

    assert service.resolve(TOKEN) is None
    assert manager.exists(TOKEN) is True


@pytest.mark.parametrize(
    ("ttl_seconds", "error"),
    [
        (0, ValueError),
        (True, TypeError),
    ],
)
def test_rejects_invalid_ttl(
    ttl_seconds,
    error,
):
    with pytest.raises(error):
        AuthenticatedSessionService(
            SessionManager(),
            ttl_seconds=ttl_seconds,
        )
