from heyti.runtime.runtime_bootstrap import RuntimeBootstrap
from heyti.runtime.runtime_startup_sequence import RuntimeStartupSequence
from heyti.materialization.describe_section.materializer import (
        DescribeSectionMaterializer,
    )

def test_runtime_bootstrap_loads_official_capabilities():
    bootstrap = RuntimeBootstrap()

    loaded_capabilities = bootstrap.initialize()

    assert len(loaded_capabilities) == 4
    assert bootstrap.registry.count() == 4

    assert bootstrap.registry.exists("describe_section") is True
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