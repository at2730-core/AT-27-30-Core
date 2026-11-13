from datetime import datetime, timezone
from types import SimpleNamespace

import pytest

from heyti.security.http_application import (
    SecurityHttpApplication,
)
from heyti.security.scope_assignment import (
    TerritorialScopeType,
)
from heyti.security.scope_profile import (
    TerritorialAccessProfile,
    TerritorialScopeProfile,
)


class AuthenticationService:
    def authenticate(self, username, password):
        raise AssertionError(
            "authenticate no debe ejecutarse"
        )


class SessionService:
    def __init__(self):
        self.session = SimpleNamespace(
            session_id="session-4",
            user_id=4,
            username="jose.de.jesus",
            display_name="Jose de Jesus",
            role=SimpleNamespace(
                value="COORDINATOR"
            ),
            expires_at=datetime(
                2026,
                11,
                14,
                12,
                0,
                tzinfo=timezone.utc,
            ),
        )

    def create_session(self, result):
        raise AssertionError(
            "create_session no debe ejecutarse"
        )

    def resolve(self, session_id):
        assert session_id == "session-4"
        return self.session

    def revoke(self, session_id):
        raise AssertionError(
            "revoke no debe ejecutarse"
        )


class ScopeProfileService:
    def __init__(self):
        self.user_ids = []

    def profile(self, user_id):
        self.user_ids.append(user_id)

        return TerritorialAccessProfile(
            scopes=(
                TerritorialScopeProfile(
                    scope_id=2,
                    scope_name=(
                        "Municipio 20 - Leon"
                    ),
                    scope_type=(
                        TerritorialScopeType
                        .MUNICIPALITY
                    ),
                    municipality_id=20,
                    municipality_code="20",
                    municipality_name=(
                        "Leon de los Aldama"
                    ),
                    section_count=787,
                ),
            )
        )


def build_application(
    scope_profile_service=None,
):
    return SecurityHttpApplication(
        authentication_service=(
            AuthenticationService()
        ),
        session_service=SessionService(),
        scope_profile_service=(
            scope_profile_service
        ),
    )


def test_session_includes_territorial_profile():
    profile_service = ScopeProfileService()

    payload = build_application(
        profile_service
    ).current_session("session-4")

    assert profile_service.user_ids == [4]
    assert payload["territorial_access"] == {
        "global_access": False,
        "scopes": [
            {
                "scope_id": 2,
                "name": "Municipio 20 - Leon",
                "type": "MUNICIPALITY",
                "municipality": {
                    "municipality_id": 20,
                    "code": "20",
                    "name": (
                        "Leon de los Aldama"
                    ),
                },
                "section_count": 787,
            }
        ],
    }


def test_session_identity_is_preserved():
    payload = build_application(
        ScopeProfileService()
    ).current_session("session-4")

    assert payload["user"] == {
        "user_id": 4,
        "username": "jose.de.jesus",
        "display_name": "Jose de Jesus",
        "role": "COORDINATOR",
    }


def test_profile_service_remains_optional():
    payload = build_application().current_session(
        "session-4"
    )

    assert "territorial_access" not in payload


def test_rejects_incompatible_profile_service():
    with pytest.raises(
        TypeError,
        match="scope_profile_service incompatible",
    ):
        build_application(object())
