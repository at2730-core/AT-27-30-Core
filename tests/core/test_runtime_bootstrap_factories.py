import pytest

from heyti.capabilities.describe_section.implementation import (
    DescribeSectionCapability,
)
from heyti.runtime.runtime_bootstrap import RuntimeBootstrap


def test_runtime_bootstrap_registers_injected_capability():
    configured_capability = DescribeSectionCapability()

    bootstrap = RuntimeBootstrap(
        capability_factories={
            "describe_section": lambda: configured_capability,
        },
    )

    loaded_capabilities = bootstrap.initialize()

    assert (
        bootstrap.registry.get("describe_section")
        is configured_capability
    )
    assert configured_capability in loaded_capabilities


def test_runtime_bootstrap_invokes_factory_once():
    configured_capability = DescribeSectionCapability()
    invocations = []

    def build_describe_section():
        invocations.append("describe_section")
        return configured_capability

    bootstrap = RuntimeBootstrap(
        capability_factories={
            "describe_section": build_describe_section,
        },
    )

    bootstrap.initialize()

    assert invocations == ["describe_section"]


def test_runtime_bootstrap_preserves_other_capabilities():
    configured_capability = DescribeSectionCapability()

    bootstrap = RuntimeBootstrap(
        capability_factories={
            "describe_section": lambda: configured_capability,
        },
    )

    loaded_capabilities = bootstrap.initialize()

    assert len(loaded_capabilities) == 5
    assert bootstrap.registry.count() == 5

    assert bootstrap.registry.exists("describe_section") is True
    assert bootstrap.registry.exists("describe_universe") is True
    assert bootstrap.registry.exists("health") is True
    assert bootstrap.registry.exists("system_info") is True
    assert bootstrap.registry.exists("version") is True


def test_runtime_bootstrap_rejects_invalid_factory_result():
    bootstrap = RuntimeBootstrap(
        capability_factories={
            "describe_section": lambda: object(),
        },
    )

    with pytest.raises(TypeError):
        bootstrap.initialize()
