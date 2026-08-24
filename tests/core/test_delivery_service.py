from heyti.delivery.adapters.in_memory import (
    InMemoryDeliveryAdapter,
)
from heyti.delivery.base import DeliveryAdapter
from heyti.delivery.context import DeliveryContext
from heyti.delivery.contracts import (
    AdapterResult,
    DeliveryEnvelope,
    DeliveryError,
)
from heyti.delivery.service import DeliveryService
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


def build_context(
    adapter_id: str = "IN_MEMORY",
) -> DeliveryContext:
    return DeliveryContext(
        consumer_id="TEST_CONSUMER",
        adapter_id=adapter_id,
        request_id="REQ-001",
        session_id="SES-001",
        execution_id="EXE-001",
    )


class FailingDeliveryAdapter(DeliveryAdapter):
    @property
    def adapter_id(self) -> str:
        return "FAILING"

    def deliver(
        self,
        envelope: DeliveryEnvelope,
    ) -> AdapterResult:
        return AdapterResult(
            success=False,
            error=DeliveryError(
                code="TEST_ADAPTER_FAILURE",
                message="Fallo controlado de prueba",
                stage="DELIVERY_EXECUTION",
            ),
        )


class SilentFailingDeliveryAdapter(DeliveryAdapter):
    @property
    def adapter_id(self) -> str:
        return "SILENT_FAILING"

    def deliver(
        self,
        envelope: DeliveryEnvelope,
    ) -> AdapterResult:
        return AdapterResult(
            success=False,
        )


def test_delivery_service_delivers_valid_response():
    adapter = InMemoryDeliveryAdapter()

    result = DeliveryService().deliver(
        build_response(),
        build_context(),
        adapter,
    )

    assert result.status == "DELIVERED"
    assert result.error is None


def test_delivery_service_preserves_response_id():
    adapter = InMemoryDeliveryAdapter()

    result = DeliveryService().deliver(
        build_response("RESP-123"),
        build_context(),
        adapter,
    )

    assert result.response_id == "RESP-123"


def test_delivery_service_creates_delivery_id():
    adapter = InMemoryDeliveryAdapter()

    result = DeliveryService().deliver(
        build_response(),
        build_context(),
        adapter,
    )

    assert isinstance(result.delivery_id, str)
    assert result.delivery_id


def test_delivery_service_preserves_trace():
    adapter = InMemoryDeliveryAdapter()

    result = DeliveryService().deliver(
        build_response(),
        build_context(),
        adapter,
    )

    assert result.trace.request_id == "REQ-001"
    assert result.trace.session_id == "SES-001"
    assert result.trace.execution_id == "EXE-001"
    assert result.trace.response_id == "RESP-001"
    assert result.trace.delivery_id == result.delivery_id


def test_delivery_service_executes_adapter_once():
    adapter = InMemoryDeliveryAdapter()

    DeliveryService().deliver(
        build_response(),
        build_context(),
        adapter,
    )

    assert len(adapter.deliveries) == 1


def test_adapter_mismatch_is_rejected_without_execution():
    adapter = InMemoryDeliveryAdapter()

    result = DeliveryService().deliver(
        build_response(),
        build_context(adapter_id="OTHER_ADAPTER"),
        adapter,
    )

    assert result.status == "REJECTED"
    assert result.error is not None
    assert result.error.code == "DELIVERY_ADAPTER_MISMATCH"
    assert len(adapter.deliveries) == 0


def test_adapter_failure_produces_failed_result():
    adapter = FailingDeliveryAdapter()

    result = DeliveryService().deliver(
        build_response(),
        build_context(adapter_id="FAILING"),
        adapter,
    )

    assert result.status == "FAILED"
    assert result.error is not None
    assert result.error.code == "TEST_ADAPTER_FAILURE"


def test_adapter_failure_without_error_is_normalized():
    adapter = SilentFailingDeliveryAdapter()

    result = DeliveryService().deliver(
        build_response(),
        build_context(adapter_id="SILENT_FAILING"),
        adapter,
    )

    assert result.status == "FAILED"
    assert result.error is not None
    assert result.error.code == "DELIVERY_ADAPTER_ERROR"


def test_same_response_can_be_delivered_multiple_times():
    response = build_response("RESP-001")

    first = DeliveryService().deliver(
        response,
        build_context(),
        InMemoryDeliveryAdapter(),
    )

    second = DeliveryService().deliver(
        response,
        build_context(),
        InMemoryDeliveryAdapter(),
    )

    assert first.response_id == second.response_id
    assert first.delivery_id != second.delivery_id