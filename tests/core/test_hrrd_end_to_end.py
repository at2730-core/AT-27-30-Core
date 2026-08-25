from heyti.delivery.adapters.in_memory import (
    InMemoryDeliveryAdapter,
)
from heyti.gateway.gateway import HeytiGateway
from heyti.kernel.kernel import HeytiKernel
from heyti.runtime.runtime_bootstrap import RuntimeBootstrap


def test_hrrd_end_to_end_preserves_contract_and_trace() -> None:
    """
    Verifica la vertical completa de HRRD:

    Gateway
        -> Kernel
        -> CapabilityRuntime
        -> Materialization
        -> Delivery

    La respuesta debe conservar identidades contractuales
    y trazabilidad sin fabricar ni perder información.
    """

    bootstrap = RuntimeBootstrap()
    bootstrap.initialize()

    bootstrap.session_manager.create(
        "SESSION-001",
        object(),
    )

    adapter = InMemoryDeliveryAdapter()
    bootstrap.delivery_adapter_registry.register(adapter)

    kernel = HeytiKernel(
        bootstrap=bootstrap,
    )
    gateway = HeytiGateway(kernel)

    result = gateway.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="PORTAL",
        adapter_id="IN_MEMORY",
        payload={
            "section_id": "1234",
        },
        request_id="REQ-001",
        execution_id="EXE-001",
        knowledge_version="K-001",
    )

    assert result.status == "DELIVERED"
    assert result.consumer_id == "PORTAL"
    assert result.adapter_id == "IN_MEMORY"

    assert result.delivery_id
    assert result.response_id
    assert result.delivery_id != result.response_id

    assert result.trace.request_id == "REQ-001"
    assert result.trace.session_id == "SESSION-001"
    assert result.trace.execution_id == "EXE-001"
    assert result.trace.response_id == result.response_id
    assert result.trace.delivery_id == result.delivery_id

    assert len(adapter.deliveries) == 1

    envelope = adapter.deliveries[0]
    response = envelope.response

    assert envelope.delivery_id == result.delivery_id
    assert envelope.response_id == result.response_id
    assert envelope.consumer_id == "PORTAL"
    assert envelope.adapter_id == "IN_MEMORY"

    assert envelope.contract == "HEYTI_DELIVERY"
    assert envelope.version == "1.0"

    assert response.response_id == result.response_id
    assert response.contract == "HEYTI_RESPONSE"
    assert response.version == "1.0"
    assert response.capability_id == "describe_section"

    assert response.trace.request_id == "REQ-001"
    assert response.trace.session_id == "SESSION-001"
    assert response.trace.execution_id == "EXE-001"
    assert response.trace.knowledge_version == "K-001"