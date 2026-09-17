import json
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import pytest

from heyti.gateway.gateway import HeytiGateway
from heyti.gateway.http_application import (
    HeytiHttpApplication,
)
from heyti.gateway.http_server import create_http_server
from heyti.materialization.contracts import (
    HeytiResponseContract,
)


class RecordingKernel:
    def __init__(self):
        self.execute_calls = []
        self.materialized_calls = []

    def execute(
        self,
        capability_name,
        session_id,
        payload=None,
    ):
        self.execute_calls.append(
            {
                "capability_name": capability_name,
                "session_id": session_id,
                "payload": payload,
            }
        )

        return {
            "status": "OK",
            "runtime": "HEYTI CORE",
            "version": "0.1.0",
        }

    def execute_materialized(self, **kwargs):
        self.materialized_calls.append(kwargs)

        return HeytiResponseContract(
            response_id="RESP-HTTP-1",
            contract="HEYTI_RESPONSE",
            version="1.0",
            capability_id="describe_section",
            status="success",
        )


@pytest.fixture
def running_server():
    kernel = RecordingKernel()
    application = HeytiHttpApplication(
        gateway=HeytiGateway(kernel),
        session_id="HTTP-SESSION",
    )
    server = create_http_server(
        application=application,
        host="127.0.0.1",
        port=0,
        knowledge_version="GUANAJUATO_2023:1.0",
    )

    thread = Thread(
        target=server.serve_forever,
        daemon=True,
    )
    thread.start()

    host, port = server.server_address

    try:
        yield f"http://{host}:{port}", kernel
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
        body = (
            payload
            if isinstance(payload, bytes)
            else json.dumps(payload).encode("utf-8")
        )

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
        json.loads(raw_body.decode("utf-8"))
        if raw_body
        else None
    )

    return response.status, response.headers, decoded


def test_health_route_uses_gateway_and_allows_vite_origin(
    running_server,
):
    base_url, kernel = running_server

    status, headers, payload = request_json(
        f"{base_url}/health",
        headers={
            "Origin": "http://localhost:5173",
            "Accept": "application/json",
        },
    )

    assert status == 200
    assert payload["status"] == "OK"
    assert headers["Access-Control-Allow-Origin"] == (
        "http://localhost:5173"
    )
    assert kernel.execute_calls == [
        {
            "capability_name": "health",
            "session_id": "HTTP-SESSION",
            "payload": None,
        }
    ]


def test_server_rejects_disallowed_origin(
    running_server,
):
    base_url, _ = running_server

    status, _, payload = request_json(
        f"{base_url}/health",
        headers={
            "Origin": "https://example.invalid",
        },
    )

    assert status == 403
    assert payload["error"]["code"] == (
        "ORIGIN_NOT_ALLOWED"
    )


def test_server_returns_safe_not_found_contract(
    running_server,
):
    base_url, _ = running_server

    status, _, payload = request_json(
        f"{base_url}/missing",
    )

    assert status == 404
    assert payload == {
        "error": {
            "code": "NOT_FOUND",
            "message": "Ruta no encontrada.",
        }
    }


def test_options_supports_local_vite_preflight(
    running_server,
):
    base_url, _ = running_server

    status, headers, payload = request_json(
        f"{base_url}/v1/sections/describe",
        method="OPTIONS",
        headers={
            "Origin": "http://127.0.0.1:5173",
        },
    )

    assert status == 204
    assert payload is None
    assert headers["Access-Control-Allow-Origin"] == (
        "http://127.0.0.1:5173"
    )
    assert "POST" in headers["Access-Control-Allow-Methods"]


def test_describe_section_route_delegates_materialization(
    running_server,
):
    base_url, kernel = running_server

    status, _, payload = request_json(
        f"{base_url}/v1/sections/describe",
        method="POST",
        payload={
            "section_id": "1524",
            "knowledge_version": "CLIENT_VALUE_IGNORED",
        },
        headers={
            "Content-Type": "application/json",
            "X-Request-ID": "REQ-HTTP-1",
        },
    )

    assert status == 200
    assert payload["response_id"] == "RESP-HTTP-1"
    assert payload["contract"] == "HEYTI_RESPONSE"

    assert len(kernel.materialized_calls) == 1

    call = kernel.materialized_calls[0]

    assert call["capability_name"] == "describe_section"
    assert call["session_id"] == "HTTP-SESSION"
    assert call["payload"] == {
        "section_id": "1524",
    }
    assert call["request_id"] == "REQ-HTTP-1"
    assert call["execution_id"].startswith("EXE-")
    assert call["knowledge_version"] == (
        "GUANAJUATO_2023:1.0"
    )


def test_describe_section_requires_json_content_type(
    running_server,
):
    base_url, _ = running_server

    status, _, payload = request_json(
        f"{base_url}/v1/sections/describe",
        method="POST",
        payload=b'{"section_id": "1524"}',
        headers={
            "Content-Type": "text/plain",
        },
    )

    assert status == 415
    assert payload["error"]["code"] == (
        "UNSUPPORTED_MEDIA_TYPE"
    )


def test_describe_section_rejects_invalid_json(
    running_server,
):
    base_url, _ = running_server

    status, _, payload = request_json(
        f"{base_url}/v1/sections/describe",
        method="POST",
        payload=b"{invalid",
        headers={
            "Content-Type": "application/json",
        },
    )

    assert status == 400
    assert payload["error"]["code"] == "INVALID_JSON"


@pytest.mark.parametrize(
    "section_id",
    [
        "",
        "   ",
        None,
    ],
)
def test_describe_section_rejects_missing_section_id(
    running_server,
    section_id,
):
    base_url, _ = running_server

    status, _, payload = request_json(
        f"{base_url}/v1/sections/describe",
        method="POST",
        payload={
            "section_id": section_id,
        },
        headers={
            "Content-Type": "application/json",
        },
    )

    assert status == 400
    assert payload["error"]["code"] == "INVALID_REQUEST"
