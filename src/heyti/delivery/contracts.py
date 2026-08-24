from dataclasses import asdict, dataclass, field
from typing import Any

from heyti.materialization.contracts import HeytiResponseContract


DELIVERY_CONTRACT = "HEYTI_DELIVERY"
DELIVERY_CONTRACT_VERSION = "1.0"

DELIVERY_STATUS_DELIVERED = "DELIVERED"
DELIVERY_STATUS_REJECTED = "REJECTED"
DELIVERY_STATUS_FAILED = "FAILED"

SUPPORTED_DELIVERY_STATUSES = {
    DELIVERY_STATUS_DELIVERED,
    DELIVERY_STATUS_REJECTED,
    DELIVERY_STATUS_FAILED,
}


@dataclass(frozen=True)
class DeliveryTrace:
    """
    Trazabilidad asociada a una operación de Delivery.

    Conserva las identidades disponibles sin fabricarlas.
    """

    request_id: str | None = None
    session_id: str | None = None
    execution_id: str | None = None
    response_id: str | None = None
    delivery_id: str | None = None


@dataclass(frozen=True)
class DeliveryError:
    """
    Error contractual seguro asociado a Runtime Response Delivery.
    """

    code: str
    message: str
    stage: str | None = None


@dataclass(frozen=True)
class AdapterResult:
    """
    Resultado técnico normalizado producido por un DeliveryAdapter.
    """

    success: bool
    error: DeliveryError | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """
        Devuelve una representación estructurada del resultado técnico.
        """

        return asdict(self)


@dataclass(frozen=True)
class DeliveryEnvelope:
    """
    Contrato interno de una operación de Runtime Response Delivery.

    Encapsula una respuesta ya materializada.
    No altera su significado cognitivo.
    """

    delivery_id: str
    response_id: str
    consumer_id: str
    adapter_id: str

    contract: str = DELIVERY_CONTRACT
    version: str = DELIVERY_CONTRACT_VERSION

    response: HeytiResponseContract | None = None
    trace: DeliveryTrace = field(default_factory=DeliveryTrace)

    def to_dict(self) -> dict[str, Any]:
        """
        Devuelve una representación estructurada del envelope.
        """

        return asdict(self)


@dataclass(frozen=True)
class DeliveryResult:
    """
    Resultado terminal de una operación de Delivery.
    """

    delivery_id: str
    response_id: str
    consumer_id: str
    adapter_id: str
    status: str

    error: DeliveryError | None = None
    trace: DeliveryTrace = field(default_factory=DeliveryTrace)

    def to_dict(self) -> dict[str, Any]:
        """
        Devuelve una representación estructurada del resultado.
        """

        return asdict(self)