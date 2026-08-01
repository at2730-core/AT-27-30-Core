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