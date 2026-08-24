from heyti.delivery.base import DeliveryAdapter
from heyti.delivery.contracts import (
    AdapterResult,
    DeliveryEnvelope,
)


class InMemoryDeliveryAdapter(DeliveryAdapter):
    """
    Adapter determinista para pruebas y verificación de HRRD.

    Captura DeliveryEnvelope en memoria.
    No utiliza red ni infraestructura externa.
    """

    ADAPTER_ID = "IN_MEMORY"

    def __init__(self) -> None:
        self._deliveries: list[DeliveryEnvelope] = []

    @property
    def adapter_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def deliveries(self) -> tuple[DeliveryEnvelope, ...]:
        return tuple(self._deliveries)

    def deliver(
        self,
        envelope: DeliveryEnvelope,
    ) -> AdapterResult:
        self._deliveries.append(envelope)

        return AdapterResult(
            success=True,
            metadata={
                "adapter_id": self.adapter_id,
            },
        )