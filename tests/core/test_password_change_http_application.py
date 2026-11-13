from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from heyti.security.http_application import (
    SecurityHttpApplication,
)


def make_application(password_change_service=None):
    authentication_service = Mock()
    authentication_service.authenticate = Mock()

    session_service = Mock()
    session_service.create_session = Mock()
    session_service.resolve = Mock()
    session_service.revoke = Mock()

    return SecurityHttpApplication(
        authentication_service=(
            authentication_service
        ),
        session_service=session_service,
        password_change_service=(
            password_change_service
        ),
    )


def test_changes_password_without_creating_session():
    password_change_service = Mock()
    password_change_service.change_password = Mock(
        return_value=SimpleNamespace(
            user_id=8,
            username="jose.de.jesus",
            display_name="Jose de Jesus",
            role=SimpleNamespace(
                value="COORDINATOR"
            ),
        )
    )

    application = make_application(
        password_change_service
    )

    response = application.change_password(
        {
            "username": "jose.de.jesus",
            "current_password": "Temporal-2026",
            "new_password": "Definitiva-2026",
            "confirmation": "Definitiva-2026",
        }
    )

    assert response == {
        "status": "PASSWORD_CHANGED",
        "user": {
            "user_id": 8,
            "username": "jose.de.jesus",
            "display_name": "Jose de Jesus",
        },
    }

    password_change_service.change_password        .assert_called_once_with(
            username="jose.de.jesus",
            current_password="Temporal-2026",
            new_password="Definitiva-2026",
            confirmation="Definitiva-2026",
        )

    assert "current_password" not in response
    assert "new_password" not in response
    assert "confirmation" not in response


def test_rejects_non_object_password_change():
    password_change_service = Mock()
    password_change_service.change_password = Mock()

    application = make_application(
        password_change_service
    )

    with pytest.raises(
        ValueError,
        match="debe ser un objeto",
    ):
        application.change_password(None)

    password_change_service.change_password        .assert_not_called()


def test_requires_configured_password_change():
    application = make_application()

    with pytest.raises(
        RuntimeError,
        match="no esta configurado",
    ):
        application.change_password({})


def test_rejects_incompatible_password_change_service():
    with pytest.raises(
        TypeError,
        match="password_change_service incompatible",
    ):
        make_application(
            password_change_service=object()
        )
