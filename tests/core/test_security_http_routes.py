import json

import pytest
from contextlib import contextmanager
from datetime import datetime, timezone
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from heyti.gateway.gateway import HeytiGateway
from heyti.gateway.http_application import (
    HeytiHttpApplication,
)
from heyti.gateway.http_server import (
    create_http_server,
)
from heyti.security.authentication import (
    AuthenticationResult,
    AuthenticationStatus,
)
from heyti.security.contracts import (
    AccessRole,
    AuthorizationDecision,
    DecisionReason,
    PermissionScope,
    PrivacyProjection,
)
from heyti.security.http_application import (
    SecurityHttpApplication,
)
from heyti.security.sessions import (
    AuthenticatedSession,
)


SESSION_TOKEN = "A" * 43

SESSION = AuthenticatedSession(
    session_id=SESSION_TOKEN,
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


class HealthKernel:
    def execute(
        self,
        capability_name,
        session_id,
        payload=None,
    ):
        if capability_name == "describe_universe":
            response = {
                "contract": "HEYTI_UNIVERSE_RESPONSE",
                "version": "1.0",
                "capability_id": "describe_universe",
            }

            if payload.get("operation") == "catalog":
                return {
                    **response,
                    "catalog": [
                        {
                            "level": "state",
                            "id": "11",
                            "label": "Guanajuato",
                            "sections": 3266,
                        },
                        {
                            "level": "municipality",
                            "id": "20",
                            "label": "Leon",
                            "sections": 787,
                        },
                        {
                            "level": "municipality",
                            "id": "1",
                            "label": "Abasolo",
                            "sections": 50,
                        },
                    ],
                }

            return {
                **response,
                "operation": payload.get("operation"),
                "level": payload.get("level"),
                "id": payload.get("id"),
            }

        return {
            "status": "OK",
            "runtime": "HEYTI CORE",
            "version": "0.1.0",
        }


class AuthenticationStub:
    def __init__(self, status):
        self.status = status

    def authenticate(
        self,
        username,
        password,
    ):
        if self.status is (
            AuthenticationStatus.AUTHENTICATED
        ):
            return AuthenticationResult(
                status=self.status,
                user_id=7,
                username=username,
                display_name="Alex",
                role=AccessRole.COORDINATOR,
            )

        return AuthenticationResult(
            status=self.status,
        )


class SessionMemory:
    def __init__(self):
        self.active = True

    def create_session(self, result):
        self.active = True
        return SESSION

    def resolve(self, session_id):
        if (
            self.active
            and session_id == SESSION_TOKEN
        ):
            return SESSION

        return None

    def revoke(self, session_id):
        if session_id == SESSION_TOKEN:
            self.active = False
            return True

        return False


class PasswordChangeStub:
    def __init__(self, mode="success"):
        self.mode = mode

    def change_password(
        self,
        *,
        username,
        current_password,
        new_password,
        confirmation,
    ):
        from heyti.security.password_change import (
            InvalidPasswordChangeCredentialsError,
            PasswordChangeLockedError,
            PasswordChangeResult,
        )

        if self.mode == "invalid":
            raise (
                InvalidPasswordChangeCredentialsError()
            )

        if self.mode == "locked":
            raise PasswordChangeLockedError()

        if self.mode == "validation":
            raise ValueError(
                "La confirmacion no coincide"
            )

        return PasswordChangeResult(
            user_id=8,
            username=username,
            display_name="Jose de Jesus",
        )


class OperationalAuthorizationStub:
    def authorize(
        self,
        *,
        user_id,
        session_id,
        permission_code,
        resource,
    ):
        allowed = True

        if permission_code == "SECTION_READ":
            allowed = resource.section_code == "1261"

        if permission_code == "UNIVERSE_MAP_READ":
            allowed = (
                resource.municipality_code in (
                    None,
                    "20",
                )
            )

        return AuthorizationDecision(
            allowed=allowed,
            permission_code=permission_code,
            reason=(
                DecisionReason.AUTHORIZED
                if allowed
                else (
                    DecisionReason
                    .RESOURCE_OUTSIDE_SCOPE
                )
            ),
            scope=PermissionScope.ASSIGNED_TERRITORY,
            audit_required=not allowed,
            privacy_projection=(
                PrivacyProjection.PUBLIC_OPERATIONAL
                if allowed
                else PrivacyProjection.REDACTED
            ),
        )


class ScopeItemStub:
    municipality_code = "20"


class ScopeProfileStub:
    global_access = False
    scopes = (ScopeItemStub(),)

    def to_dict(self):
        return {
            "global_access": False,
            "scopes": [
                {
                    "scope_id": 2,
                    "name": "Municipio 20 - Leon",
                    "type": "MUNICIPALITY",
                    "municipality": {
                        "municipality_id": 20,
                        "code": "20",
                        "name": "Leon de los Aldama",
                    },
                    "section_count": 787,
                }
            ],
        }


class ScopeProfileServiceStub:
    def profile(self, user_id):
        return ScopeProfileStub()


@contextmanager
def running_server(
    status=AuthenticationStatus.AUTHENTICATED,
    include_security=True,
    password_change_mode="success",
):
    application = HeytiHttpApplication(
        gateway=HeytiGateway(HealthKernel()),
        session_id="HTTP-SESSION",
    )

    security_application = None

    if include_security:
        security_application = (
            SecurityHttpApplication(
                AuthenticationStub(status),
                SessionMemory(),
                password_change_service=(
                    PasswordChangeStub(
                        password_change_mode
                    )
                ),
                authorization_service=(
                    OperationalAuthorizationStub()
                ),
                scope_profile_service=(
                    ScopeProfileServiceStub()
                ),
            )
        )

    server = create_http_server(
        application=application,
        host="127.0.0.1",
        port=0,
        security_application=security_application,
        require_authenticated_operations=(
            security_application is not None
        ),
    )

    thread = Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    host, port = server.server_address

    try:
        yield f"http://{host}:{port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def request_json(
    url,
    method="GET",
    payload=None,
    headers=None,
):
    body = None

    if payload is not None:
        body = json.dumps(
            payload
        ).encode("utf-8")

    request = Request(
        url,
        data=body,
        method=method,
        headers=headers or {},
    )

    try:
        response = urlopen(
            request,
            timeout=5,
        )
    except HTTPError as exc:
        response = exc

    raw_body = response.read()

    decoded = (
        json.loads(
            raw_body.decode("utf-8")
        )
        if raw_body
        else None
    )

    return (
        response.status,
        response.headers,
        decoded,
    )


def test_login_returns_authenticated_session():
    with running_server() as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/auth/login",
            method="POST",
            payload={
                "username": "alex",
                "password": "secret-password",
            },
            headers={
                "Content-Type": "application/json",
            },
        )

    assert status == 200
    assert payload["status"] == "AUTHENTICATED"
    assert payload["session_token"] == SESSION_TOKEN
    assert payload["user"]["role"] == "COORDINATOR"


def test_login_rejects_invalid_credentials_uniformly():
    with running_server(
        AuthenticationStatus.INVALID_CREDENTIALS
    ) as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/auth/login",
            method="POST",
            payload={
                "username": "alex",
                "password": "wrong-password",
            },
            headers={
                "Content-Type": "application/json",
            },
        )

    assert status == 401
    assert payload == {
        "error": {
            "code": "INVALID_CREDENTIALS",
            "message": "Credenciales invalidas.",
        }
    }


def test_login_reports_required_password_change():
    with running_server(
        AuthenticationStatus
        .PASSWORD_CHANGE_REQUIRED
    ) as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/auth/login",
            method="POST",
            payload={
                "username": "alex",
                "password": "temporary-password",
            },
            headers={
                "Content-Type": "application/json",
            },
        )

    assert status == 403
    assert payload["error"]["code"] == (
        "PASSWORD_CHANGE_REQUIRED"
    )


def test_login_rejects_invalid_payload():
    with running_server() as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/auth/login",
            method="POST",
            payload={
                "username": "",
                "password": "secret-password",
            },
            headers={
                "Content-Type": "application/json",
            },
        )

    assert status == 400
    assert payload["error"]["code"] == (
        "INVALID_REQUEST"
    )


def test_current_session_accepts_bearer_token():
    with running_server() as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/auth/session",
            headers={
                "Authorization": (
                    f"Bearer {SESSION_TOKEN}"
                ),
            },
        )

    assert status == 200
    assert payload["user"]["user_id"] == 7
    assert payload["user"]["username"] == "alex"


def test_current_session_requires_bearer_token():
    with running_server() as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/auth/session",
        )

    assert status == 401
    assert payload["error"]["code"] == (
        "AUTHENTICATION_REQUIRED"
    )


def test_logout_revokes_authenticated_session():
    with running_server() as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/auth/logout",
            method="POST",
            headers={
                "Authorization": (
                    f"Bearer {SESSION_TOKEN}"
                ),
            },
        )

        after_status, _, after_payload = (
            request_json(
                f"{base_url}/v1/auth/session",
                headers={
                    "Authorization": (
                        f"Bearer {SESSION_TOKEN}"
                    ),
                },
            )
        )

    assert status == 200
    assert payload == {
        "status": "SIGNED_OUT",
    }
    assert after_status == 401
    assert after_payload["error"]["code"] == (
        "AUTHENTICATION_REQUIRED"
    )


def test_auth_preflight_allows_authorization_header():
    with running_server() as base_url:
        status, headers, payload = request_json(
            f"{base_url}/v1/auth/session",
            method="OPTIONS",
            headers={
                "Origin": (
                    "http://127.0.0.1:5173"
                ),
            },
        )

    assert status == 204
    assert payload is None
    assert "Authorization" in (
        headers["Access-Control-Allow-Headers"]
    )


def test_auth_routes_are_not_exposed_without_security():
    with running_server(
        include_security=False
    ) as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/auth/session",
            headers={
                "Authorization": (
                    f"Bearer {SESSION_TOKEN}"
                ),
            },
        )

    assert status == 404
    assert payload["error"]["code"] == "NOT_FOUND"


def test_operational_route_requires_bearer_token():
    with running_server() as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/sections/describe",
            method="POST",
            payload={
                "section_id": "1",
            },
            headers={
                "Content-Type": "application/json",
            },
        )

    assert status == 401
    assert payload == {
        "error": {
            "code": "AUTHENTICATION_REQUIRED",
            "message": (
                "Se requiere una sesion autenticada."
            ),
        }
    }


def test_operational_route_rejects_invalid_token():
    with running_server() as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/universes/describe",
            method="POST",
            payload={
                "operation": "catalog",
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": (
                    "Bearer INVALID-SESSION"
                ),
            },
        )

    assert status == 401
    assert payload["error"]["code"] == (
        "AUTHENTICATION_REQUIRED"
    )


def test_protection_requires_security_application():
    from heyti.gateway.http_application import (
        HeytiHttpApplication,
    )

    application = HeytiHttpApplication.__new__(
        HeytiHttpApplication
    )

    with pytest.raises(
        ValueError,
        match=(
            "proteccion operativa requiere "
            "security_application"
        ),
    ):
        create_http_server(
            application=application,
            host="127.0.0.1",
            port=0,
            require_authenticated_operations=True,
        )

def test_password_route_changes_required_password():
    with running_server() as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/auth/password",
            method="POST",
            payload={
                "username": "jose.de.jesus",
                "current_password": "Temporal-2026",
                "new_password": "Definitiva-2026",
                "confirmation": "Definitiva-2026",
            },
            headers={
                "Content-Type": "application/json",
            },
        )

    assert status == 200
    assert payload == {
        "status": "PASSWORD_CHANGED",
        "user": {
            "user_id": 8,
            "username": "jose.de.jesus",
            "display_name": "Jose de Jesus",
        },
    }
    assert "Temporal-2026" not in str(payload)
    assert "Definitiva-2026" not in str(payload)


def test_password_route_rejects_invalid_credentials():
    with running_server(
        password_change_mode="invalid"
    ) as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/auth/password",
            method="POST",
            payload={
                "username": "jose.de.jesus",
                "current_password": "incorrecta",
                "new_password": "Definitiva-2026",
                "confirmation": "Definitiva-2026",
            },
            headers={
                "Content-Type": "application/json",
            },
        )

    assert status == 401
    assert payload["error"]["code"] == (
        "INVALID_CREDENTIALS"
    )


def test_password_route_reports_locked_account():
    with running_server(
        password_change_mode="locked"
    ) as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/auth/password",
            method="POST",
            payload={
                "username": "jose.de.jesus",
                "current_password": "Temporal-2026",
                "new_password": "Definitiva-2026",
                "confirmation": "Definitiva-2026",
            },
            headers={
                "Content-Type": "application/json",
            },
        )

    assert status == 423
    assert payload["error"]["code"] == (
        "ACCOUNT_LOCKED"
    )


def test_password_route_rejects_invalid_request():
    with running_server(
        password_change_mode="validation"
    ) as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/auth/password",
            method="POST",
            payload={
                "username": "jose.de.jesus",
                "current_password": "Temporal-2026",
                "new_password": "Definitiva-2026",
                "confirmation": "Otra-2026",
            },
            headers={
                "Content-Type": "application/json",
            },
        )

    assert status == 400
    assert payload["error"]["code"] == (
        "INVALID_REQUEST"
    )


def test_password_route_supports_preflight():
    with running_server() as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/auth/password",
            method="OPTIONS",
            headers={
                "Origin": (
                    "http://127.0.0.1:5173"
                ),
            },
        )

    assert status == 204
    assert payload is None

def test_authenticated_catalog_is_filtered_to_municipality():
    with running_server() as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/universes/describe",
            method="POST",
            payload={
                "operation": "catalog",
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": (
                    f"Bearer {SESSION_TOKEN}"
                ),
            },
        )

    assert status == 200
    assert payload["catalog"] == [
        {
            "level": "municipality",
            "id": "20",
            "label": "Leon",
            "sections": 787,
        }
    ]


def test_assigned_municipality_map_is_authorized():
    with running_server() as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/universes/describe",
            method="POST",
            payload={
                "operation": "map",
                "level": "municipality",
                "id": "20",
                "year": 2024,
                "contest": "A",
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": (
                    f"Bearer {SESSION_TOKEN}"
                ),
            },
        )

    assert status == 200
    assert payload["level"] == "municipality"
    assert payload["id"] == "20"


def test_external_municipality_map_is_rejected():
    with running_server() as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/universes/describe",
            method="POST",
            payload={
                "operation": "map",
                "level": "municipality",
                "id": "1",
                "year": 2024,
                "contest": "A",
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": (
                    f"Bearer {SESSION_TOKEN}"
                ),
            },
        )

    assert status == 403
    assert payload["error"]["code"] == (
        "AUTHORIZATION_DENIED"
    )


def test_state_map_is_rejected_for_scoped_user():
    with running_server() as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/universes/describe",
            method="POST",
            payload={
                "operation": "map",
                "level": "state",
                "id": "11",
                "year": 2024,
                "contest": "A",
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": (
                    f"Bearer {SESSION_TOKEN}"
                ),
            },
        )

    assert status == 403
    assert payload["error"]["code"] == (
        "AUTHORIZATION_DENIED"
    )


def test_external_section_is_rejected():
    with running_server() as base_url:
        status, _, payload = request_json(
            f"{base_url}/v1/sections/describe",
            method="POST",
            payload={
                "section_id": "1",
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": (
                    f"Bearer {SESSION_TOKEN}"
                ),
            },
        )

    assert status == 403
    assert payload["error"]["code"] == (
        "AUTHORIZATION_DENIED"
    )
