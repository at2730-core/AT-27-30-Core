"""
Capability Runtime de HEYTI.

Responsabilidad:
Orquestar la ejecución de capacidades registradas
dentro de una sesión válida.
"""

from typing import Any

from heyti.events.event_bus import EventBus
from heyti.registry.registry import CapabilityRegistry
from heyti.session.session_manager import SessionManager


class SessionNotFoundError(Exception):
    """
    Se produce cuando la sesión solicitada no existe.
    """


class CapabilityNotFoundError(Exception):
    """
    Se produce cuando la capacidad solicitada no está registrada.
    """


class CapabilityRuntime:
    """
    Coordina la ejecución de capacidades dentro del Runtime.
    """

    def __init__(
        self,
        registry: CapabilityRegistry,
        session_manager: SessionManager,
        event_bus: EventBus,
    ) -> None:
        self._registry = registry
        self._session_manager = session_manager
        self._event_bus = event_bus

    def execute(
        self,
        capability_name: str,
        session_id: str,
        payload: Any = None,
    ) -> Any:
        """
        Ejecuta una capacidad registrada dentro de una sesión válida.
        """

        if not self._session_manager.exists(session_id):
            raise SessionNotFoundError(
                f"Session not found: {session_id}"
            )

        session = self._session_manager.get(session_id)

        if not self._registry.exists(capability_name):
            raise CapabilityNotFoundError(
                f"Capability not found: {capability_name}"
            )

        capability = self._registry.get(capability_name)

        result = capability.execute(
            session,
            payload,
        )

        self._event_bus.publish(
            "capability_executed",
            {
                "capability_name": capability_name,
                "session_id": session_id,
                "result": result,
            },
        )

        return result