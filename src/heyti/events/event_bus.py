"""
Event Bus de HEYTI.

Responsabilidad:
Administrar suscripciones y distribuir eventos
a los manejadores registrados.
"""

from collections.abc import Callable
from typing import Any


EventHandler = Callable[[Any], None]


class EventBus:
    """
    Publica eventos y los distribuye entre sus suscriptores.
    """

    def __init__(self) -> None:
        self._subscribers: dict[str, list[EventHandler]] = {}

    def subscribe(
        self,
        event_name: str,
        handler: EventHandler,
    ) -> None:
        """
        Suscribe un manejador a un evento.
        """
        if event_name not in self._subscribers:
            self._subscribers[event_name] = []

        self._subscribers[event_name].append(handler)

    def publish(
        self,
        event_name: str,
        payload: Any = None,
    ) -> None:
        """
        Publica un evento y notifica a sus manejadores.
        """
        handlers = self._subscribers.get(event_name, [])

        for handler in handlers:
            handler(payload)

    def count(self, event_name: str) -> int:
        """
        Devuelve el número de manejadores suscritos
        a un evento.
        """
        return len(self._subscribers.get(event_name, []))