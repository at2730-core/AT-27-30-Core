"""
Pruebas unitarias del Event Bus de HEYTI.
"""

from heyti.events.event_bus import EventBus


def test_event_bus_starts_empty() -> None:
    """Debe iniciar sin suscriptores."""
    bus = EventBus()

    assert bus.count("session_created") == 0


def test_event_bus_can_subscribe_handler() -> None:
    """Debe permitir registrar un manejador."""
    bus = EventBus()

    def handler(payload):
        pass

    bus.subscribe("session_created", handler)

    assert bus.count("session_created") == 1


def test_event_bus_calls_subscribed_handler() -> None:
    """Debe invocar el manejador registrado."""

    bus = EventBus()

    received = []

    def handler(payload):
        received.append(payload)

    bus.subscribe("session_created", handler)

    bus.publish("session_created", "SESSION-001")

    assert received == ["SESSION-001"]


def test_event_bus_calls_multiple_handlers() -> None:
    """Debe invocar todos los manejadores registrados."""

    bus = EventBus()

    first = []
    second = []

    def handler_one(payload):
        first.append(payload)

    def handler_two(payload):
        second.append(payload)

    bus.subscribe("session_created", handler_one)
    bus.subscribe("session_created", handler_two)

    bus.publish("session_created", 123)

    assert first == [123]
    assert second == [123]


def test_event_bus_publish_unknown_event_does_not_fail() -> None:
    """Publicar un evento sin suscriptores no debe producir error."""

    bus = EventBus()

    bus.publish("unknown_event")

    assert bus.count("unknown_event") == 0