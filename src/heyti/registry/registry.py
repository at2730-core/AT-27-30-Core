"""
Capability Registry de HEYTI.

Responsabilidad:
Administrar el catálogo de capacidades disponibles
dentro del Runtime de HEYTI.
"""

from typing import Any


class CapabilityRegistry:
    """
    Registro central de capacidades del Runtime.

    Esta primera versión únicamente administra el
    catálogo de capacidades registradas.
    """

    def __init__(self) -> None:
        self._capabilities: dict[str, Any] = {}

    def register(self, name: str, capability: Any) -> None:
        """
        Registra una capacidad.
        """
        self._capabilities[name] = capability

    def exists(self, name: str) -> bool:
        """
        Indica si una capacidad existe.
        """
        return name in self._capabilities

    def get(self, name: str) -> Any | None:
        """
        Recupera una capacidad registrada.
        """
        return self._capabilities.get(name)

    def count(self) -> int:
        """
        Devuelve el número de capacidades registradas.
        """
        return len(self._capabilities)