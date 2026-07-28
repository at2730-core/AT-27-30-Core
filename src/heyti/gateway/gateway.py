"""
HEYTI Gateway.

Punto único de entrada al Runtime de HEYTI.

Toda solicitud proveniente de módulos, APIs o interfaces externas
deberá ingresar al sistema a través de este componente.

PCA-002 — Gateway HEYTI
"""

from heyti.kernel.kernel import HeytiKernel


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