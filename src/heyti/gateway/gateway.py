"""
HEYTI Gateway.

Punto único de entrada al Runtime de HEYTI.

Toda solicitud proveniente de módulos, APIs o interfaces externas
deberá ingresar al sistema a través de este componente.

PCA-002 — Gateway HEYTI
"""

from heyti.kernel.kernel import HeytiKernel
from typing import Any


class HeytiGateway:
    """
    Gateway oficial del Runtime HEYTI.

    Su única responsabilidad consiste en recibir solicitudes
    externas y delegarlas al Kernel correspondiente.
    """

    def __init__(self, kernel: HeytiKernel) -> None:
        """
        Inicializa el Gateway.

        Parameters
        ----------
        kernel:
            Instancia del Kernel que será utilizada para
            coordinar la ejecución del Runtime.
        """
        self._kernel = kernel

    @property
    def kernel(self) -> HeytiKernel:
        """Devuelve la instancia del Kernel asociada."""
        return self._kernel

    def start(self) -> None:
        """
        Solicita el inicio del Runtime.
        """
        self._kernel.start()

    def stop(self) -> None:
        """
        Solicita la detención del Runtime.
        """
        self._kernel.stop()

    def is_running(self) -> bool:
        """
        Indica si el Runtime se encuentra activo.
        """
        return self._kernel.is_running

    def execute(
        self,
        capability_name: str,
        session_id: str,
        payload: Any = None,
    ) -> Any:
        """
        Recibe una solicitud externa de ejecución cognitiva
        y la delega al Kernel.
        """

        return self._kernel.execute(
            capability_name=capability_name,
            session_id=session_id,
            payload=payload,
        )

    def execute_materialized(
        self,
        capability_name: str,
        session_id: str,
        materializer: Any = None,
        payload: Any = None,
        contract_version: str = "1.0",
        request_id: str | None = None,
        execution_id: str | None = None,
        knowledge_version: str | None = None,
        validator: Any = None,
    ) -> Any:
        """
        Recibe una solicitud externa de ejecución materializada
        y la delega al Kernel.
        """

        return self._kernel.execute_materialized(
            capability_name=capability_name,
            session_id=session_id,
            materializer=materializer,
            payload=payload,
            contract_version=contract_version,
            request_id=request_id,
            execution_id=execution_id,
            knowledge_version=knowledge_version,
            validator=validator,
        )

    def execute_delivered(
        self,
        capability_name: str,
        session_id: str,
        consumer_id: str,
        adapter: Any = None,
        adapter_id: str | None = None,
        materializer: Any = None,
        payload: Any = None,
        contract_version: str = "1.0",
        request_id: str | None = None,
        execution_id: str | None = None,
        knowledge_version: str | None = None,
        validator: Any = None,
        delivery_service: Any = None,
    ) -> Any:
        """
        Recibe una solicitud externa de ejecución entregable
        y la delega al Kernel.
        """

        return self._kernel.execute_delivered(
            capability_name=capability_name,
            session_id=session_id,
            consumer_id=consumer_id,
            adapter=adapter,
            adapter_id=adapter_id,
            materializer=materializer,
            payload=payload,
            contract_version=contract_version,
            request_id=request_id,
            execution_id=execution_id,
            knowledge_version=knowledge_version,
            validator=validator,
            delivery_service=delivery_service,
        )