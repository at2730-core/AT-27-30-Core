import pytest

from heyti.capabilities.base import Capability
from heyti.registry.registry import CapabilityRegistry
from heyti.runtime.capability_loader import CapabilityLoader


class FactoryCapability(Capability):
    def __init__(self, marker="factory"):
        self.marker = marker

    def execute(self, session=None, payload=None):
        return {
            "marker": self.marker,
        }


class DefaultCapability(Capability):
    def execute(self, session=None, payload=None):
        return {
            "marker": "default",
        }


def test_loader_uses_named_factory():
    expected = FactoryCapability(
        marker="injected",
    )
    loader = CapabilityLoader(
        registry=CapabilityRegistry(),
        capability_factories={
            "sample_capability": lambda: expected,
        },
    )

    capability = loader._instantiate_capability(
        DefaultCapability,
        capability_name="sample_capability",
    )

    assert capability is expected
    assert capability.execute()["marker"] == "injected"


def test_loader_preserves_default_instantiation():
    loader = CapabilityLoader(
        registry=CapabilityRegistry(),
        capability_factories={
            "another_capability": FactoryCapability,
        },
    )

    capability = loader._instantiate_capability(
        DefaultCapability,
        capability_name="sample_capability",
    )

    assert isinstance(capability, DefaultCapability)
    assert capability.execute()["marker"] == "default"


def test_direct_legacy_instantiation_remains_supported():
    loader = CapabilityLoader(
        registry=CapabilityRegistry(),
    )

    capability = loader._instantiate_capability(
        DefaultCapability,
    )

    assert isinstance(capability, DefaultCapability)


def test_load_all_uses_directory_named_factory(
    tmp_path,
):
    capability_directory = (
        tmp_path / "sample_capability"
    )
    capability_directory.mkdir()

    (
        capability_directory / "__init__.py"
    ).write_text(
        "",
        encoding="utf-8",
    )
    (
        capability_directory / "implementation.py"
    ).write_text(
        "\n".join(
            [
                "from heyti.capabilities.base import Capability",
                "",
                "class DiscoveredCapability(Capability):",
                "    def execute(self, session=None, payload=None):",
                "        return {'marker': 'discovered'}",
                "",
            ]
        ),
        encoding="utf-8",
    )

    expected = FactoryCapability(
        marker="injected",
    )
    registry = CapabilityRegistry()
    loader = CapabilityLoader(
        registry=registry,
        capability_factories={
            "sample_capability": lambda: expected,
        },
    )

    loaded = loader.load_all(tmp_path)

    assert loaded == [expected]
    assert registry.count() == 1


@pytest.mark.parametrize(
    "factories",
    [
        {
            "": FactoryCapability,
        },
        {
            "sample_capability": None,
        },
    ],
)
def test_loader_rejects_invalid_factory_mapping(
    factories,
):
    with pytest.raises(TypeError):
        CapabilityLoader(
            registry=CapabilityRegistry(),
            capability_factories=factories,
        )


def test_loader_rejects_invalid_factory_result():
    loader = CapabilityLoader(
        registry=CapabilityRegistry(),
        capability_factories={
            "sample_capability": lambda: object(),
        },
    )

    with pytest.raises(TypeError):
        loader._instantiate_capability(
            DefaultCapability,
            capability_name="sample_capability",
        )
