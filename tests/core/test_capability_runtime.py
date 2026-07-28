"""
Pruebas unitarias del Capability Runtime de HEYTI.
"""

import pytest

from heyti.events.event_bus import EventBus
from heyti.registry.registry import CapabilityRegistry
from heyti.runtime.capability_runtime import (
    CapabilityNotFoundError,
    CapabilityRuntime,
    SessionNotFoundError,
)
from heyti.session.session_manager import SessionManager


class FakeCapability:
    """
    Capacidad de prueba utilizada para verificar
    la coordinación realizada por el Runtime.
    """

    def __init__(self) -> None:
        self.received_session = None
        self.received_payload = None

    def execute(self, session, payload):
        self.received_session = session
        self.received_payload = payload

        return "execution_result"


def test_runtime_executes_registered_capability() -> None:
    """Debe ejecutar una capacidad registrada."""

    registry = CapabilityRegistry()
    sessions = SessionManager()
    events = EventBus()

    session = object()
    capability = FakeCapability()

    sessions.create("SESSION-001", session)
    registry.register("test_capability", capability)

    runtime = CapabilityRuntime(
        registry=registry,
        session_manager=sessions,
        event_bus=events,
    )

    result = runtime.execute(
        capability_name="test_capability",
        session_id="SESSION-001",
        payload={"section": 1523},
    )

    assert result == "execution_result"
    assert capability.received_session is session
    assert capability.received_payload == {"section": 1523}


def test_runtime_rejects_unknown_session() -> None:
    """Debe rechazar una sesión inexistente."""

    registry = CapabilityRegistry()
    sessions = SessionManager()
    events = EventBus()

    registry.register("test_capability", FakeCapability())

    runtime = CapabilityRuntime(
        registry=registry,
        session_manager=sessions,
        event_bus=events,
    )

    with pytest.raises(SessionNotFoundError):
        runtime.execute(
            capability_name="test_capability",
            session_id="UNKNOWN-SESSION",
        )


def test_runtime_rejects_unknown_capability() -> None:
    """Debe rechazar una capacidad inexistente."""

    registry = CapabilityRegistry()
    sessions = SessionManager()
    events = EventBus()

    sessions.create("SESSION-001", object())

    runtime = CapabilityRuntime(
        registry=registry,
        session_manager=sessions,
        event_bus=events,
    )

    with pytest.raises(CapabilityNotFoundError):
        runtime.execute(
            capability_name="unknown_capability",
            session_id="SESSION-001",
        )


def test_runtime_publishes_execution_event() -> None:
    """Debe publicar un evento después de una ejecución exitosa."""

    registry = CapabilityRegistry()
    sessions = SessionManager()
    events = EventBus()

    session = object()
    capability = FakeCapability()
    published_events = []

    sessions.create("SESSION-001", session)
    registry.register("test_capability", capability)

    events.subscribe(
        "capability_executed",
        published_events.append,
    )

    runtime = CapabilityRuntime(
        registry=registry,
        session_manager=sessions,
        event_bus=events,
    )

    runtime.execute(
        capability_name="test_capability",
        session_id="SESSION-001",
        payload="payload",
    )

    assert published_events == [
        {
            "capability_name": "test_capability",
            "session_id": "SESSION-001",
            "result": "execution_result",
        }
    ]