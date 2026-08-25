"""
HEYTI Kernel.

Componente central responsable de coordinar el ciclo de vida
de los servicios internos de HEYTI-CORE.

PCA-001 — Kernel HEYTI
"""

from typing import Any

from heyti.runtime.runtime_bootstrap import RuntimeBootstrap


class HeytiKernel:
    """
    Representa el núcleo coordinador de HEYTI.

    El Kernel no implementa lógica de negocio directamente.
    Su responsabilidad es coordinar los componentes internos
    del Runtime y mantener el estado operativo del sistema.
    """

    def __init__(
        self,
        bootstrap: Any | None = None,
    ) -> None:
        """Inicializa el Kernel en estado detenido."""
        self._is_running = False
        self._bootstrap = bootstrap or RuntimeBootstrap()

    @property
    def is_running(self) -> bool:
        """Indica si el Kernel se encuentra en ejecución."""
        return self._is_running

    def execute(
        self,
        capability_name: str,
        session_id: str,
        payload: Any = None,
    ) -> Any:
        """
        Delega la ejecución de una capability al Runtime operativo.

        El Kernel conserva la frontera pública del Core y no
        implementa lógica cognitiva directamente.
        """

        return self._bootstrap.runtime.execute(
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
        Delega al Runtime la ejecución materializada de una capability.

        El Kernel conserva la frontera pública del Core sin
        implementar Materialization directamente.
        """

        return self._bootstrap.runtime.execute_materialized(
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
        Delega al Runtime la ejecución, materialización y entrega
        de una respuesta HEYTI.

        El Kernel conserva la frontera pública del Core y no
        implementa lógica de Delivery directamente.
        """

        return self._bootstrap.runtime.execute_delivered(
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

    def start(self) -> None:
        """Inicia la operación del Kernel."""
        if self._is_running:
            return

        self._bootstrap.initialize()

        self._is_running = True

    def stop(self) -> None:
        """Detiene la operación del Kernel."""
        if not self._is_running:
            return

        self._is_running = False