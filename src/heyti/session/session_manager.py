"""
Session Manager de HEYTI.

Responsabilidad:
Administrar las sesiones activas del Runtime.
"""

from typing import Any


class SessionManager:
    """
    Administra las sesiones activas del Runtime.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, Any] = {}

    def create(self, session_id: str, session: Any) -> None:
        """
        Registra una nueva sesión.
        """
        self._sessions[session_id] = session

    def exists(self, session_id: str) -> bool:
        """
        Indica si una sesión existe.
        """
        return session_id in self._sessions

    def get(self, session_id: str) -> Any | None:
        """
        Recupera una sesión registrada.
        """
        return self._sessions.get(session_id)

    def remove(self, session_id: str) -> None:
        """
        Elimina una sesión.
        """
        self._sessions.pop(session_id, None)

    def count(self) -> int:
        """
        Devuelve el número de sesiones activas.
        """
        return len(self._sessions)