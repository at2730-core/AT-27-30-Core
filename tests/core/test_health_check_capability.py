from types import SimpleNamespace

from heyti.capabilities.health.health_check import HealthCheckCapability
from heyti.events.event_bus import EventBus
from heyti.registry.registry import CapabilityRegistry
from heyti.runtime.capability_runtime import CapabilityRuntime
from heyti.session.session_manager import SessionManager


def test_health_check_capability_executes_through_runtime():
    registry = CapabilityRegistry()
    session_manager = SessionManager()
    event_bus = EventBus()

    capability = HealthCheckCapability()

    registry.register(
        "health_check",
        capability,
    )

    session_id = "session-001"
    session = SimpleNamespace(id=session_id)

    session_manager.create(
        session_id,
        session,
    )

    runtime = CapabilityRuntime(
        registry=registry,
        session_manager=session_manager,
        event_bus=event_bus,
    )

    result = runtime.execute(
        capability_name="health_check",
        session_id=session_id,
    )

    assert result == {
        "status": "OK",
        "runtime": "HEYTI CORE",
        "version": "0.1.0",
    }