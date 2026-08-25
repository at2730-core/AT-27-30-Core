import pytest

from heyti.capabilities.describe_section.implementation import (
    DescribeSectionCapability,
)
from heyti.delivery.adapters.in_memory import (
    InMemoryDeliveryAdapter,
)
from heyti.events.event_bus import EventBus
from heyti.materialization.describe_section.materializer import (
    DescribeSectionMaterializer,
)
from heyti.materialization.errors import MaterializationError
from heyti.registry.registry import CapabilityRegistry
from heyti.runtime.capability_runtime import CapabilityRuntime
from heyti.session.session_manager import SessionManager


class CountingDescribeSectionCapability(
    DescribeSectionCapability
):
    def __init__(self) -> None:
        super().__init__()
        self.execution_count = 0

    def execute(
        self,
        session=None,
        payload=None,
        section_id=None,
    ):
        self.execution_count += 1

        return super().execute(
            session=session,
            payload=payload,
            section_id=section_id,
        )


class FailingMaterializer:
    def materialize(
        self,
        cognitive_result,
        context,
    ):
        raise MaterializationError(
            "controlled materialization failure"
        )


def build_runtime(capability):
    registry = CapabilityRegistry()
    sessions = SessionManager()
    events = EventBus()

    sessions.create(
        "SESSION-001",
        object(),
    )

    registry.register(
        "describe_section",
        capability,
    )

    runtime = CapabilityRuntime(
        registry=registry,
        session_manager=sessions,
        event_bus=events,
    )

    return runtime, events


def test_runtime_delivers_materialized_response():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)
    adapter = InMemoryDeliveryAdapter()

    result = runtime.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="TEST_CONSUMER",
        adapter=adapter,
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
    )

    assert result.status == "DELIVERED"
    assert len(adapter.deliveries) == 1


def test_runtime_executes_capability_once_when_delivering():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    runtime.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="TEST_CONSUMER",
        adapter=InMemoryDeliveryAdapter(),
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
    )

    assert capability.execution_count == 1


def test_runtime_preserves_response_identity_into_delivery():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)
    adapter = InMemoryDeliveryAdapter()

    result = runtime.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="TEST_CONSUMER",
        adapter=adapter,
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
    )

    envelope = adapter.deliveries[0]

    assert result.response_id == envelope.response.response_id
    assert result.response_id == envelope.response_id


def test_runtime_creates_delivery_identity():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    result = runtime.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="TEST_CONSUMER",
        adapter=InMemoryDeliveryAdapter(),
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
    )

    assert result.delivery_id
    assert result.delivery_id != result.response_id


def test_runtime_preserves_trace_into_delivery():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    result = runtime.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="TEST_CONSUMER",
        adapter=InMemoryDeliveryAdapter(),
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
        request_id="REQ-001",
        execution_id="EXE-001",
        knowledge_version="K-001",
    )

    assert result.trace.request_id == "REQ-001"
    assert result.trace.session_id == "SESSION-001"
    assert result.trace.execution_id == "EXE-001"
    assert result.trace.response_id == result.response_id
    assert result.trace.delivery_id == result.delivery_id


def test_runtime_preserves_consumer_identity():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    result = runtime.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="PORTAL",
        adapter=InMemoryDeliveryAdapter(),
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
    )

    assert result.consumer_id == "PORTAL"


def test_materialization_failure_prevents_delivery():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)
    adapter = InMemoryDeliveryAdapter()

    with pytest.raises(MaterializationError):
        runtime.execute_delivered(
            capability_name="describe_section",
            session_id="SESSION-001",
            consumer_id="TEST_CONSUMER",
            adapter=adapter,
            payload={
                "section_id": "1234",
            },
            materializer=FailingMaterializer(),
        )

    assert capability.execution_count == 1
    assert len(adapter.deliveries) == 0


def test_runtime_keeps_single_capability_event_when_delivering():
    capability = CountingDescribeSectionCapability()
    runtime, events = build_runtime(capability)

    published_events = []

    events.subscribe(
        "capability_executed",
        published_events.append,
    )

    runtime.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="TEST_CONSUMER",
        adapter=InMemoryDeliveryAdapter(),
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
    )

    assert capability.execution_count == 1
    assert len(published_events) == 1

def test_runtime_delivery_resolves_materializer_from_registry():
    capability = CountingDescribeSectionCapability()

    registry = CapabilityRegistry()
    sessions = SessionManager()
    events = EventBus()

    from heyti.materialization.registry import (
        MaterializationRegistry,
    )

    materialization_registry = MaterializationRegistry()

    sessions.create(
        "SESSION-001",
        object(),
    )

    registry.register(
        "describe_section",
        capability,
    )

    materialization_registry.register(
        capability_id="describe_section",
        contract_version="1.0",
        materializer=DescribeSectionMaterializer(),
    )

    runtime = CapabilityRuntime(
        registry=registry,
        session_manager=sessions,
        event_bus=events,
        materialization_registry=materialization_registry,
    )

    adapter = InMemoryDeliveryAdapter()

    result = runtime.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="PORTAL",
        adapter=adapter,
        payload={
            "section_id": "1234",
        },
    )

    assert result.status == "DELIVERED"
    assert result.consumer_id == "PORTAL"
    assert result.response_id
    assert result.delivery_id
    assert capability.execution_count == 1
    assert len(adapter.deliveries) == 1

    envelope = adapter.deliveries[0]

    assert envelope.response.contract == "HEYTI_RESPONSE"
    assert envelope.response.version == "1.0"
    assert envelope.response.capability_id == "describe_section"

def test_runtime_publishes_delivery_completed_event():
    capability = CountingDescribeSectionCapability()
    runtime, events = build_runtime(capability)
    adapter = InMemoryDeliveryAdapter()

    published_events = []

    events.subscribe(
        "delivery_completed",
        published_events.append,
    )

    result = runtime.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="PORTAL",
        adapter=adapter,
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
    )

    assert published_events == [
        {
            "delivery_id": result.delivery_id,
            "response_id": result.response_id,
            "consumer_id": "PORTAL",
            "adapter_id": "IN_MEMORY",
            "status": "DELIVERED",
        }
    ]


def test_runtime_publishes_delivery_event_after_capability_event():
    capability = CountingDescribeSectionCapability()
    runtime, events = build_runtime(capability)

    event_order = []

    events.subscribe(
        "capability_executed",
        lambda payload: event_order.append(
            "capability_executed"
        ),
    )

    events.subscribe(
        "delivery_completed",
        lambda payload: event_order.append(
            "delivery_completed"
        ),
    )

    runtime.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="PORTAL",
        adapter=InMemoryDeliveryAdapter(),
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
    )

    assert event_order == [
        "capability_executed",
        "delivery_completed",
    ]


def test_materialization_failure_does_not_publish_delivery_event():
    capability = CountingDescribeSectionCapability()
    runtime, events = build_runtime(capability)
    adapter = InMemoryDeliveryAdapter()

    published_events = []

    events.subscribe(
        "delivery_completed",
        published_events.append,
    )

    with pytest.raises(MaterializationError):
        runtime.execute_delivered(
            capability_name="describe_section",
            session_id="SESSION-001",
            consumer_id="PORTAL",
            adapter=adapter,
            payload={
                "section_id": "1234",
            },
            materializer=FailingMaterializer(),
        )

    assert published_events == []
    assert len(adapter.deliveries) == 0