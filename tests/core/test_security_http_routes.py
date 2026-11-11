import json
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
from heyti.security.contracts import AccessRole
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


@contextmanager
def running_server(
    status=AuthenticationStatus.AUTHENTICATED,
    include_security=True,
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
            )
        )

    server = create_http_server(
        application=application,
        host="127.0.0.1",
        port=0,
        security_application=security_application,
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
