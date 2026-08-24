from abc import ABC, abstractmethod

from heyti.delivery.contracts import (
    AdapterResult,
    DeliveryEnvelope,
)


class DeliveryAdapter(ABC):
    """
    Contrato base para mecanismos de entrega HRRD.

    Un DeliveryAdapter recibe un DeliveryEnvelope ya construido
    y ejecuta un mecanismo técnico de entrega.

    No modifica cognición.
    No materializa respuestas.
    No ejecuta capabilities.
    """

    @property
    @abstractmethod
    def adapter_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def deliver(
        self,
        envelope: DeliveryEnvelope,
    ) -> AdapterResult:
        raise NotImplementedError