from heyti.delivery.context import DeliveryContext
from heyti.delivery.factory import DeliveryEnvelopeFactory
from heyti.materialization.contracts import HeytiResponseContract


def build_response(
    response_id: str = "RESP-001",
) -> HeytiResponseContract:
    return HeytiResponseContract(
        response_id=response_id,
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success",
    )


def build_context() -> DeliveryContext:
    return DeliveryContext(
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
        request_id="REQ-001",
        session_id="SES-001",
        execution_id="EXE-001",
    )


def test_factory_creates_delivery_id():
    envelope = DeliveryEnvelopeFactory().create(
        build_response(),
        build_context(),
    )

    assert isinstance(envelope.delivery_id, str)
    assert envelope.delivery_id


def test_factory_preserves_response_id():
    response = build_response("RESP-123")

    envelope = DeliveryEnvelopeFactory().create(
        response,
        build_context(),
    )

    assert envelope.response_id == "RESP-123"
    assert envelope.response.response_id == "RESP-123"


def test_factory_creates_distinct_delivery_ids():
    response = build_response()

    first = DeliveryEnvelopeFactory().create(
        response,
        build_context(),
    )

    second = DeliveryEnvelopeFactory().create(
        response,
        build_context(),
    )

    assert first.delivery_id != second.delivery_id


def test_same_response_can_have_multiple_deliveries():
    response = build_response("RESP-001")

    first = DeliveryEnvelopeFactory().create(
        response,
        build_context(),
    )

    second = DeliveryEnvelopeFactory().create(
        response,
        build_context(),
    )

    assert first.response_id == second.response_id
    assert first.delivery_id != second.delivery_id


def test_factory_preserves_delivery_context_trace():
    envelope = DeliveryEnvelopeFactory().create(
        build_response(),
        build_context(),
    )

    assert envelope.trace.request_id == "REQ-001"
    assert envelope.trace.session_id == "SES-001"
    assert envelope.trace.execution_id == "EXE-001"
    assert envelope.trace.response_id == "RESP-001"
    assert envelope.trace.delivery_id == envelope.delivery_id