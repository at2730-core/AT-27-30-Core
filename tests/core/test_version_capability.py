from types import SimpleNamespace

from heyti.capabilities.version.version import VersionCapability
from heyti.events.event_bus import EventBus
from heyti.registry.registry import CapabilityRegistry
from heyti.runtime.capability_runtime import CapabilityRuntime
from heyti.session.session_manager import SessionManager


def test_version_capability_executes_through_runtime():
    registry = CapabilityRegistry()
    session_manager = SessionManager()
    event_bus = EventBus()

    capability = VersionCapability()

    registry.register(
        "version",
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
        capability_name="version",
        session_id=session_id,
    )

    assert result == {
        "name": "HEYTI CORE",
        "version": "0.1.0",
        "api": "v1",
    }