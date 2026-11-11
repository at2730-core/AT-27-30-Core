from datetime import datetime, timezone
from unittest.mock import MagicMock

import pytest

from heyti.security.authentication import (
    AuthenticationResult,
    AuthenticationStatus,
)
from heyti.security.contracts import AccessRole
from heyti.security.http_application import (
    AuthenticatedSessionRequiredError,
    InvalidCredentialsError,
    PasswordChangeRequiredError,
    SecurityHttpApplication,
)
from heyti.security.sessions import (
    AuthenticatedSession,
)


SESSION = AuthenticatedSession(
    session_id="A" * 43,
    user_id=7,
    username="alex",
    display_name="Alex",
    role=AccessRole.COORDINATOR,
    created_at=datetime(
        2026,
        11,
        11,
        18,
        0,
        tzinfo=timezone.utc,
    ),
    expires_at=datetime(
        2026,
        11,
        12,
        2,
        0,
        tzinfo=timezone.utc,
    ),
)


def make_application(status):
    authentication = MagicMock()
    authentication.authenticate.return_value = (
        AuthenticationResult(
            status=status,
            user_id=7,
            username="alex",
            display_name="Alex",
            role=AccessRole.COORDINATOR,
        )
    )

    sessions = MagicMock()
    sessions.create_session.return_value = (
        SESSION
    )
    sessions.resolve.return_value = SESSION

    application = SecurityHttpApplication(
        authentication,
        sessions,
    )

    return application, authentication, sessions


def test_login_creates_session():
    application, authentication, sessions = (
        make_application(
            AuthenticationStatus.AUTHENTICATED
        )
    )

    response = application.login({
        "username": "  alex  ",
        "password": "secret-password",
    })

    assert response == {
        "status": "AUTHENTICATED",
        "session_token": "A" * 43,
        "expires_at": (
            "2026-11-12T02:00:00+00:00"
        ),
        "user": {
            "user_id": 7,
            "username": "alex",
            "display_name": "Alex",
            "role": "COORDINATOR",
        },
    }
    authentication.authenticate.assert_called_once_with(
        "alex",
        "secret-password",
    )
    sessions.create_session.assert_called_once()


@pytest.mark.parametrize(
    "status",
    [
        AuthenticationStatus.INVALID_CREDENTIALS,
        AuthenticationStatus.LOCKED,
    ],
)
def test_login_returns_uniform_rejection(status):
    application, _, sessions = (
        make_application(status)
    )

    with pytest.raises(
        InvalidCredentialsError
    ):
        application.login({
            "username": "alex",
            "password": "wrong-password",
        })

    sessions.create_session.assert_not_called()


def test_login_requires_password_change():
    application, _, sessions = (
        make_application(
            AuthenticationStatus
            .PASSWORD_CHANGE_REQUIRED
        )
    )

    with pytest.raises(
        PasswordChangeRequiredError
    ):
        application.login({
            "username": "alex",
            "password": "temporary-password",
        })

    sessions.create_session.assert_not_called()


@pytest.mark.parametrize(
    "payload",
    [
        None,
        {},
        {"username": "", "password": "secret"},
        {"username": "alex"},
        {"username": "alex", "password": ""},
    ],
)
def test_login_rejects_invalid_payload(payload):
    application, authentication, _ = (
        make_application(
            AuthenticationStatus.AUTHENTICATED
        )
    )

    with pytest.raises(ValueError):
        application.login(payload)

    authentication.authenticate.assert_not_called()


def test_current_session_returns_identity():
    application, _, sessions = (
        make_application(
            AuthenticationStatus.AUTHENTICATED
        )
    )

    response = application.current_session(
        SESSION.session_id
    )

    assert response["user"]["user_id"] == 7
    assert response["user"]["role"] == (
        "COORDINATOR"
    )
    sessions.resolve.assert_called_once_with(
        SESSION.session_id
    )


def test_current_session_rejects_unknown_token():
    application, _, sessions = (
        make_application(
            AuthenticationStatus.AUTHENTICATED
        )
    )
    sessions.resolve.return_value = None

    with pytest.raises(
        AuthenticatedSessionRequiredError
    ):
        application.current_session(
            "B" * 43
        )


def test_logout_revokes_session():
    application, _, sessions = (
        make_application(
            AuthenticationStatus.AUTHENTICATED
        )
    )

    response = application.logout(
        SESSION.session_id
    )

    assert response == {
        "status": "SIGNED_OUT"
    }
    sessions.revoke.assert_called_once_with(
        SESSION.session_id
    )


def test_logout_rejects_unknown_token():
    application, _, sessions = (
        make_application(
            AuthenticationStatus.AUTHENTICATED
        )
    )
    sessions.resolve.return_value = None

    with pytest.raises(
        AuthenticatedSessionRequiredError
    ):
        application.logout("B" * 43)

    sessions.revoke.assert_not_called()


@pytest.mark.parametrize(
    ("authentication", "sessions"),
    [
        (object(), MagicMock()),
        (MagicMock(), object()),
    ],
)
def test_rejects_invalid_services(
    authentication,
    sessions,
):
    with pytest.raises(TypeError):
        SecurityHttpApplication(
            authentication,
            sessions,
        )
