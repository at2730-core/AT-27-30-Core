"""
Pruebas unitarias del Kernel de HEYTI.

Verifica el ciclo básico de inicio y detención
del componente central del Runtime.
"""

from heyti.kernel.kernel import HeytiKernel


def test_kernel_starts_stopped() -> None:
    """El Kernel debe iniciar en estado detenido."""
    kernel = HeytiKernel()

    assert kernel.is_running is False


def test_kernel_can_start() -> None:
    """El Kernel debe cambiar a estado activo al iniciarse."""
    kernel = HeytiKernel()

    kernel.start()

    assert kernel.is_running is True


def test_kernel_can_stop() -> None:
    """El Kernel debe regresar a estado detenido."""
    kernel = HeytiKernel()
    kernel.start()

    kernel.stop()

    assert kernel.is_running is False