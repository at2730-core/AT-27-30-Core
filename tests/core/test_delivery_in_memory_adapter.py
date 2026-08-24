from heyti.delivery.adapters.in_memory import (
    InMemoryDeliveryAdapter,
)
from heyti.delivery.contracts import DeliveryEnvelope
from heyti.materialization.contracts import HeytiResponseContract


def build_envelope(
    delivery_id: str = "DEL-001",
) -> DeliveryEnvelope:
    response = HeytiResponseContract(
        response_id="RESP-001",
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success",
    )

    return DeliveryEnvelope(
        delivery_id=delivery_id,
        response_id=response.response_id,
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
        response=response,
    )


def test_in_memory_adapter_has_stable_identity():
    adapter = InMemoryDeliveryAdapter()

    assert adapter.adapter_id == "IN_MEMORY"


def test_in_memory_adapter_delivers_envelope():
    adapter = InMemoryDeliveryAdapter()
    envelope = build_envelope()

    result = adapter.deliver(envelope)

    assert result.success is True
    assert result.error is None


def test_in_memory_adapter_captures_delivery():
    adapter = InMemoryDeliveryAdapter()
    envelope = build_envelope()

    adapter.deliver(envelope)

    assert len(adapter.deliveries) == 1
    assert adapter.deliveries[0] is envelope


def test_in_memory_adapter_preserves_response():
    adapter = InMemoryDeliveryAdapter()
    envelope = build_envelope()

    adapter.deliver(envelope)

    captured = adapter.deliveries[0]

    assert captured.response_id == "RESP-001"
    assert captured.response is envelope.response


def test_in_memory_adapter_preserves_delivery_id():
    adapter = InMemoryDeliveryAdapter()
    envelope = build_envelope("DEL-123")

    adapter.deliver(envelope)

    assert adapter.deliveries[0].delivery_id == "DEL-123"


def test_in_memory_adapter_supports_multiple_deliveries():
    adapter = InMemoryDeliveryAdapter()

    first = build_envelope("DEL-001")
    second = build_envelope("DEL-002")

    adapter.deliver(first)
    adapter.deliver(second)

    assert len(adapter.deliveries) == 2
    assert adapter.deliveries[0].delivery_id == "DEL-001"
    assert adapter.deliveries[1].delivery_id == "DEL-002"


def test_in_memory_adapter_metadata_identifies_adapter():
    adapter = InMemoryDeliveryAdapter()

    result = adapter.deliver(build_envelope())

    assert result.metadata["adapter_id"] == "IN_MEMORY"