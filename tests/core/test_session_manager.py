"""
Pruebas unitarias del Session Manager de HEYTI.

Verifica la creación, consulta, eliminación
y conteo de sesiones activas.
"""

from heyti.session.session_manager import SessionManager


def test_session_manager_starts_empty() -> None:
    """Debe iniciar sin sesiones."""
    manager = SessionManager()

    assert manager.count() == 0


def test_session_manager_can_create_session() -> None:
    """Debe permitir registrar una sesión."""
    manager = SessionManager()
    session = object()

    manager.create("session_001", session)

    assert manager.exists("session_001") is True
    assert manager.count() == 1


def test_session_manager_can_get_session() -> None:
    """Debe recuperar una sesión registrada."""
    manager = SessionManager()
    session = object()

    manager.create("session_001", session)

    assert manager.get("session_001") is session


def test_session_manager_can_remove_session() -> None:
    """Debe eliminar una sesión existente."""
    manager = SessionManager()
    session = object()

    manager.create("session_001", session)
    manager.remove("session_001")

    assert manager.exists("session_001") is False
    assert manager.count() == 0


def test_session_manager_returns_none_for_unknown_session() -> None:
    """Debe devolver None cuando la sesión no existe."""
    manager = SessionManager()

    assert manager.get("unknown_session") is None