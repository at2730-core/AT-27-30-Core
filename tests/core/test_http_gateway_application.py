import pytest

from heyti.gateway.gateway import HeytiGateway
from heyti.gateway.http_application import (
    HeytiHttpApplication,
)
from heyti.materialization.contracts import (
    HeytiResponseContract,
)


class RecordingKernel:
    def __init__(self):
        self.execute_calls = []
        self.materialized_calls = []
        self.health_result = {
            "status": "OK",
            "runtime": "HEYTI CORE",
            "version": "0.1.0",
        }
        self.materialized_result = HeytiResponseContract(
            response_id="RESP-1",
            contract="HEYTI_RESPONSE",
            version="1.0",
            capability_id="describe_section",
            status="success",
        )

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
        return self.health_result

    def execute_materialized(self, **kwargs):
        self.materialized_calls.append(kwargs)
        return self.materialized_result


def build_application():
    kernel = RecordingKernel()
    gateway = HeytiGateway(kernel)
    application = HeytiHttpApplication(
        gateway=gateway,
        session_id="HTTP-SESSION",
    )

    return application, kernel


def test_http_application_requires_gateway():
    with pytest.raises(TypeError):
        HeytiHttpApplication(
            gateway=object(),
            session_id="HTTP-SESSION",
        )


@pytest.mark.parametrize(
    "session_id",
    [
        "",
        "   ",
        None,
    ],
)
def test_http_application_requires_session_id(
    session_id,
):
    gateway = HeytiGateway(
        RecordingKernel()
    )

    with pytest.raises(ValueError):
        HeytiHttpApplication(
            gateway=gateway,
            session_id=session_id,
        )


def test_health_delegates_to_official_gateway():
    application, kernel = build_application()

    result = application.health()

    assert result == {
        "status": "OK",
        "runtime": "HEYTI CORE",
        "version": "0.1.0",
    }
    assert kernel.execute_calls == [
        {
            "capability_name": "health",
            "session_id": "HTTP-SESSION",
            "payload": None,
        }
    ]


def test_health_rejects_invalid_cognitive_result():
    application, kernel = build_application()
    kernel.health_result = "INVALID"

    with pytest.raises(TypeError):
        application.health()


def test_describe_section_materializes_through_gateway():
    application, kernel = build_application()

    result = application.describe_section(
        section_id=" 1524 ",
        request_id="REQ-1",
        execution_id="EXE-1",
        knowledge_version="K-1",
    )

    assert result["response_id"] == "RESP-1"
    assert result["contract"] == "HEYTI_RESPONSE"
    assert result["capability_id"] == "describe_section"

    assert kernel.materialized_calls == [
        {
            "capability_name": "describe_section",
            "session_id": "HTTP-SESSION",
            "payload": {
                "section_id": "1524",
            },
            "request_id": "REQ-1",
            "execution_id": "EXE-1",
            "knowledge_version": "K-1",
            "materializer": None,
            "contract_version": "1.0",
            "validator": None,
        }
    ]


@pytest.mark.parametrize(
    "section_id",
    [
        "",
        "   ",
        None,
    ],
)
def test_describe_section_requires_section_id(
    section_id,
):
    application, _ = build_application()

    with pytest.raises(ValueError):
        application.describe_section(
            section_id=section_id,
        )


def test_describe_section_rejects_invalid_response():
    application, kernel = build_application()
    kernel.materialized_result = {
        "status": "success",
    }

    with pytest.raises(TypeError):
        application.describe_section(
            section_id="1524",
        )
