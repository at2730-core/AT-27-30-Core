from heyti.delivery.context import DeliveryContext
from heyti.delivery.contracts import (
    DELIVERY_CONTRACT,
    DELIVERY_CONTRACT_VERSION,
    DELIVERY_STATUS_DELIVERED,
    DeliveryEnvelope,
    DeliveryError,
    DeliveryResult,
    DeliveryTrace,
)
from heyti.materialization.contracts import HeytiResponseContract


def build_response() -> HeytiResponseContract:
    return HeytiResponseContract(
        response_id="RESP-001",
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success",
    )


def test_delivery_context_preserves_consumer_and_adapter():
    context = DeliveryContext(
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
        request_id="REQ-001",
        session_id="SES-001",
        execution_id="EXE-001",
    )

    assert context.consumer_id == "TEST_CONSUMER"
    assert context.adapter_id == "IN_MEMORY"
    assert context.request_id == "REQ-001"
    assert context.session_id == "SES-001"
    assert context.execution_id == "EXE-001"


def test_delivery_envelope_preserves_response_identity():
    response = build_response()

    envelope = DeliveryEnvelope(
        delivery_id="DEL-001",
        response_id=response.response_id,
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
        response=response,
    )

    assert envelope.delivery_id == "DEL-001"
    assert envelope.response_id == "RESP-001"
    assert envelope.response is response


def test_delivery_and_response_ids_are_independent():
    response = build_response()

    envelope = DeliveryEnvelope(
        delivery_id="DEL-001",
        response_id=response.response_id,
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
        response=response,
    )

    assert envelope.delivery_id != envelope.response_id


def test_delivery_envelope_uses_contract_v1():
    envelope = DeliveryEnvelope(
        delivery_id="DEL-001",
        response_id="RESP-001",
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
    )

    assert envelope.contract == DELIVERY_CONTRACT
    assert envelope.version == DELIVERY_CONTRACT_VERSION


def test_delivery_trace_preserves_response_and_delivery_ids():
    trace = DeliveryTrace(
        request_id="REQ-001",
        session_id="SES-001",
        execution_id="EXE-001",
        response_id="RESP-001",
        delivery_id="DEL-001",
    )

    assert trace.response_id == "RESP-001"
    assert trace.delivery_id == "DEL-001"


def test_delivered_result_preserves_identity():
    result = DeliveryResult(
        delivery_id="DEL-001",
        response_id="RESP-001",
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
        status=DELIVERY_STATUS_DELIVERED,
    )

    assert result.delivery_id == "DEL-001"
    assert result.response_id == "RESP-001"
    assert result.status == "DELIVERED"


def test_delivery_result_can_carry_structured_error():
    error = DeliveryError(
        code="DELIVERY_TEST_ERROR",
        message="Error controlado de prueba",
        stage="TEST",
    )

    result = DeliveryResult(
        delivery_id="DEL-001",
        response_id="RESP-001",
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
        status="FAILED",
        error=error,
    )

    assert result.error is error
    assert result.error.code == "DELIVERY_TEST_ERROR"


def test_delivery_envelope_to_dict_preserves_response_id():
    response = build_response()

    envelope = DeliveryEnvelope(
        delivery_id="DEL-001",
        response_id=response.response_id,
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
        response=response,
    )

    data = envelope.to_dict()

    assert data["delivery_id"] == "DEL-001"
    assert data["response_id"] == "RESP-001"
    assert data["response"]["response_id"] == "RESP-001"