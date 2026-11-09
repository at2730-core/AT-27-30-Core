from heyti.runtime.runtime_bootstrap import RuntimeBootstrap
from heyti.runtime.runtime_startup_sequence import RuntimeStartupSequence
from heyti.materialization.describe_section.materializer import (
        DescribeSectionMaterializer,
    )
from heyti.delivery.registry import DeliveryAdapterRegistry
from heyti.events.event_bus import EventBus
from heyti.runtime.capability_runtime import CapabilityRuntime
from heyti.session.session_manager import SessionManager

def test_runtime_bootstrap_loads_official_capabilities():
    bootstrap = RuntimeBootstrap()

    loaded_capabilities = bootstrap.initialize()

    assert len(loaded_capabilities) == 6
    assert bootstrap.registry.count() == 6

    assert bootstrap.registry.exists("describe_section") is True
    assert bootstrap.registry.exists("describe_universe") is True
    assert bootstrap.registry.exists("health") is True
    assert bootstrap.registry.exists("system_info") is True
    assert bootstrap.registry.exists("version") is True

def test_runtime_bootstrap_records_startup_sequence():
    sequence = RuntimeStartupSequence()

    bootstrap = RuntimeBootstrap(
        sequence=sequence,
    )

    bootstrap.initialize()

    assert sequence.steps == [
        ("Bootstrap", "STARTED"),
        ("Capabilities", "OK"),
        ("Runtime", "READY"),
    ]

def test_runtime_bootstrap_registers_materialization():
    bootstrap = RuntimeBootstrap()

    bootstrap.initialize()

    assert bootstrap.materialization_registry.count() == 1
    assert bootstrap.materialization_registry.exists(
        "describe_section",
        "1.0",
    ) is True


def test_runtime_bootstrap_resolves_describe_section_materializer():
    bootstrap = RuntimeBootstrap()

    bootstrap.initialize()

    materializer = bootstrap.materialization_registry.resolve(
        capability_id="describe_section",
        contract_version="1.0",
    )

    assert isinstance(
        materializer,
        DescribeSectionMaterializer,
    )

def test_runtime_bootstrap_materialization_registration_is_idempotent():
    bootstrap = RuntimeBootstrap()

    bootstrap.initialize()
    bootstrap.initialize()

    assert bootstrap.materialization_registry.count() == 1
    assert bootstrap.materialization_registry.exists(
        "describe_section",
        "1.0",
    ) is True

def test_runtime_bootstrap_composes_runtime_dependencies():
    bootstrap = RuntimeBootstrap()

    assert isinstance(
        bootstrap.session_manager,
        SessionManager,
    )
    assert isinstance(
        bootstrap.event_bus,
        EventBus,
    )
    assert isinstance(
        bootstrap.delivery_adapter_registry,
        DeliveryAdapterRegistry,
    )
    assert isinstance(
        bootstrap.runtime,
        CapabilityRuntime,
    )


def test_runtime_bootstrap_runtime_uses_shared_dependencies():
    bootstrap = RuntimeBootstrap()

    assert bootstrap.runtime._registry is bootstrap.registry
    assert (
        bootstrap.runtime._session_manager
        is bootstrap.session_manager
    )
    assert (
        bootstrap.runtime._event_bus
        is bootstrap.event_bus
    )
    assert (
        bootstrap.runtime._materialization_registry
        is bootstrap.materialization_registry
    )
    assert (
        bootstrap.runtime._delivery_adapter_registry
        is bootstrap.delivery_adapter_registry
    )


def test_runtime_bootstrap_delivery_registry_starts_empty():
    bootstrap = RuntimeBootstrap()

    assert bootstrap.delivery_adapter_registry.count() == 0