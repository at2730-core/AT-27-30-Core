"""
Pruebas unitarias del Kernel de HEYTI.

Verifica el ciclo básico de inicio y detención
del componente central del Runtime.
"""
from unittest.mock import Mock
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

def test_kernel_initializes_runtime_before_starting() -> None:
    """El Kernel debe preparar el Runtime antes de declararse activo."""
    bootstrap = Mock()
    kernel = HeytiKernel(
        bootstrap=bootstrap,
    )

    kernel.start()

    bootstrap.initialize.assert_called_once_with()
    assert kernel.is_running is True

def test_kernel_delegates_execution_to_runtime() -> None:
    """El Kernel debe delegar la ejecución al Runtime compuesto."""
    bootstrap = Mock()
    bootstrap.runtime.execute.return_value = "runtime-result"

    kernel = HeytiKernel(
        bootstrap=bootstrap,
    )

    result = kernel.execute(
        capability_name="describe_section",
        session_id="SESSION-001",
        payload={"section_id": "1234"},
    )

    bootstrap.runtime.execute.assert_called_once_with(
        capability_name="describe_section",
        session_id="SESSION-001",
        payload={"section_id": "1234"},
    )
    assert result == "runtime-result"


def test_kernel_does_not_initialize_runtime_during_execute() -> None:
    """
    Execute no debe alterar implícitamente el ciclo de vida.
    """
    bootstrap = Mock()

    kernel = HeytiKernel(
        bootstrap=bootstrap,
    )

    kernel.execute(
        capability_name="describe_section",
        session_id="SESSION-001",
    )

    bootstrap.initialize.assert_not_called()

def test_kernel_delegates_materialized_execution_to_runtime() -> None:
    """El Kernel debe delegar Materialization al Runtime."""
    bootstrap = Mock()
    bootstrap.runtime.execute_materialized.return_value = (
        "materialized-result"
    )

    kernel = HeytiKernel(
        bootstrap=bootstrap,
    )

    result = kernel.execute_materialized(
        capability_name="describe_section",
        session_id="SESSION-001",
        payload={"section_id": "1234"},
        contract_version="1.0",
        request_id="REQ-001",
        execution_id="EXE-001",
        knowledge_version="K-001",
    )

    bootstrap.runtime.execute_materialized.assert_called_once_with(
        capability_name="describe_section",
        session_id="SESSION-001",
        materializer=None,
        payload={"section_id": "1234"},
        contract_version="1.0",
        request_id="REQ-001",
        execution_id="EXE-001",
        knowledge_version="K-001",
        validator=None,
    )

    assert result == "materialized-result"


def test_kernel_materialized_execution_does_not_initialize_runtime() -> None:
    """Materialization tampoco debe provocar auto-start."""
    bootstrap = Mock()

    kernel = HeytiKernel(
        bootstrap=bootstrap,
    )

    kernel.execute_materialized(
        capability_name="describe_section",
        session_id="SESSION-001",
    )

    bootstrap.initialize.assert_not_called()

def test_kernel_delegates_delivered_execution_to_runtime() -> None:
    """El Kernel debe delegar Delivery al Runtime."""
    bootstrap = Mock()
    bootstrap.runtime.execute_delivered.return_value = (
        "delivery-result"
    )

    kernel = HeytiKernel(
        bootstrap=bootstrap,
    )

    result = kernel.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="PORTAL",
        adapter_id="IN_MEMORY",
        payload={"section_id": "1234"},
        contract_version="1.0",
        request_id="REQ-001",
        execution_id="EXE-001",
        knowledge_version="K-001",
    )

    bootstrap.runtime.execute_delivered.assert_called_once_with(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="PORTAL",
        adapter=None,
        adapter_id="IN_MEMORY",
        materializer=None,
        payload={"section_id": "1234"},
        contract_version="1.0",
        request_id="REQ-001",
        execution_id="EXE-001",
        knowledge_version="K-001",
        validator=None,
        delivery_service=None,
    )

    assert result == "delivery-result"


def test_kernel_delivered_execution_does_not_initialize_runtime() -> None:
    """Delivery tampoco debe provocar auto-start."""
    bootstrap = Mock()

    kernel = HeytiKernel(
        bootstrap=bootstrap,
    )

    kernel.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="PORTAL",
        adapter_id="IN_MEMORY",
    )

    bootstrap.initialize.assert_not_called()