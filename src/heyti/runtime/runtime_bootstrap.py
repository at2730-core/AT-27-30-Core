from collections.abc import Mapping
from pathlib import Path

from heyti.delivery.registry import DeliveryAdapterRegistry
from heyti.events.event_bus import EventBus
from heyti.materialization.describe_section.materializer import (
    DescribeSectionMaterializer,
)
from heyti.materialization.registry import (
    MaterializationRegistry,
)
from heyti.registry.registry import CapabilityRegistry
from heyti.runtime.capability_loader import (
    CapabilityFactory,
    CapabilityLoader,
)
from heyti.runtime.capability_runtime import CapabilityRuntime
from heyti.runtime.runtime_startup_sequence import RuntimeStartupSequence
from heyti.session.session_manager import SessionManager


class RuntimeBootstrap:
    """
    Responsable del arranque inicial del Runtime de HEYTI.

    Puede recibir fábricas explícitas para componer dependencias
    de capabilities concretas sin acoplar esa composición al loader.
    """

    def __init__(
        self,
        sequence: RuntimeStartupSequence | None = None,
        capability_factories: (
            Mapping[str, CapabilityFactory] | None
        ) = None,
    ) -> None:
        self.registry = CapabilityRegistry()
        self.loader = CapabilityLoader(
            registry=self.registry,
            capability_factories=capability_factories,
        )
        self.sequence = sequence or RuntimeStartupSequence()
        self.materialization_registry = MaterializationRegistry()
        self.session_manager = SessionManager()
        self.event_bus = EventBus()
        self.delivery_adapter_registry = DeliveryAdapterRegistry()

        self.runtime = CapabilityRuntime(
            registry=self.registry,
            session_manager=self.session_manager,
            event_bus=self.event_bus,
            materialization_registry=self.materialization_registry,
            delivery_adapter_registry=self.delivery_adapter_registry,
        )

    def initialize(self):
        """
        Descubre, carga y registra las capabilities oficiales,
        conservando la secuencia de arranque del Runtime.
        """
        self.sequence.add_step(
            "Bootstrap",
            "STARTED",
        )

        capabilities_root = Path(
            "src/heyti/capabilities"
        )

        loaded_capabilities = self.loader.load_all(
            capabilities_root
        )

        self.materialization_registry.register(
            capability_id="describe_section",
            contract_version="1.0",
            materializer=DescribeSectionMaterializer(),
        )

        self.sequence.add_step(
            "Capabilities",
            "OK",
        )

        self.sequence.add_step(
            "Runtime",
            "READY",
        )

        return loaded_capabilities
