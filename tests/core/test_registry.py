"""
Pruebas unitarias del Capability Registry de HEYTI.

Verifica el registro, consulta y conteo
de capacidades disponibles en el Runtime.
"""

from heyti.registry.registry import CapabilityRegistry


def test_registry_starts_empty() -> None:
    """El Registry debe iniciar sin capacidades registradas."""
    registry = CapabilityRegistry()

    assert registry.count() == 0


def test_registry_can_register_capability() -> None:
    """El Registry debe permitir registrar una capacidad."""
    registry = CapabilityRegistry()
    capability = object()

    registry.register("territorial_analysis", capability)

    assert registry.exists("territorial_analysis") is True
    assert registry.count() == 1


def test_registry_can_get_registered_capability() -> None:
    """El Registry debe devolver la capacidad registrada."""
    registry = CapabilityRegistry()
    capability = object()

    registry.register("territorial_analysis", capability)

    assert registry.get("territorial_analysis") is capability


def test_registry_returns_none_for_unknown_capability() -> None:
    """El Registry debe devolver None cuando la capacidad no existe."""
    registry = CapabilityRegistry()

    assert registry.get("unknown_capability") is None


def test_registry_replaces_capability_with_same_name() -> None:
    """Registrar el mismo nombre debe sustituir la referencia anterior."""
    registry = CapabilityRegistry()
    first_capability = object()
    second_capability = object()

    registry.register("territorial_analysis", first_capability)
    registry.register("territorial_analysis", second_capability)

    assert registry.get("territorial_analysis") is second_capability
    assert registry.count() == 1