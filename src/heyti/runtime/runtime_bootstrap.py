from pathlib import Path

from heyti.registry.registry import CapabilityRegistry
from heyti.runtime.capability_loader import CapabilityLoader


class RuntimeBootstrap:
    """
    Responsable del arranque inicial del Runtime de HEYTI.
    """

    def __init__(self) -> None:
        self.registry = CapabilityRegistry()
        self.loader = CapabilityLoader(
            registry=self.registry,
        )

    def initialize(self):
        """
        Descubre, carga y registra las capabilities oficiales.
        """
        capabilities_root = Path(
            "src/heyti/capabilities"
        )

        return self.loader.load_all(
            capabilities_root
        )