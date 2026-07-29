from types import SimpleNamespace

from heyti.capabilities.system_info.system_info import SystemInfoCapability
from heyti.events.event_bus import EventBus
from heyti.registry.registry import CapabilityRegistry
from heyti.runtime.capability_runtime import CapabilityRuntime
from heyti.session.session_manager import SessionManager


def test_system_info_capability_executes_through_runtime():
    registry = CapabilityRegistry()
    session_manager = SessionManager()
    event_bus = EventBus()

    capability = SystemInfoCapability()

    registry.register(
        "system_info",
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
        capability_name="system_info",
        session_id=session_id,
    )

    assert result["core"] == "HEYTI CORE"
    assert isinstance(result["python"], str)
    assert isinstance(result["platform"], str)
    assert isinstance(result["system"], str)
    assert isinstance(result["machine"], str)