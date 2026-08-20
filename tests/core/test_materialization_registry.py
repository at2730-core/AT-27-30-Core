import pytest

from heyti.materialization.describe_section.materializer import (
    DescribeSectionMaterializer,
)
from heyti.materialization.errors import (
    UnsupportedContractVersionError,
    UnsupportedMaterializationError,
)
from heyti.materialization.registry import (
    MaterializationRegistry,
)


def test_registry_registers_materializer():
    registry = MaterializationRegistry()
    materializer = DescribeSectionMaterializer()

    registry.register(
        capability_id="describe_section",
        contract_version="1.0",
        materializer=materializer,
    )

    assert registry.count() == 1


def test_registry_resolves_materializer():
    registry = MaterializationRegistry()
    materializer = DescribeSectionMaterializer()

    registry.register(
        capability_id="describe_section",
        contract_version="1.0",
        materializer=materializer,
    )

    resolved = registry.resolve(
        capability_id="describe_section",
        contract_version="1.0",
    )

    assert resolved is materializer


def test_registry_reports_existing_registration():
    registry = MaterializationRegistry()

    registry.register(
        capability_id="describe_section",
        contract_version="1.0",
        materializer=DescribeSectionMaterializer(),
    )

    assert registry.exists(
        "describe_section",
        "1.0",
    )


def test_registry_rejects_unknown_capability():
    registry = MaterializationRegistry()

    with pytest.raises(
        UnsupportedMaterializationError
    ):
        registry.resolve(
            capability_id="unknown",
            contract_version="1.0",
        )


def test_registry_rejects_unknown_version():
    registry = MaterializationRegistry()

    registry.register(
        capability_id="describe_section",
        contract_version="1.0",
        materializer=DescribeSectionMaterializer(),
    )

    with pytest.raises(
        UnsupportedContractVersionError
    ):
        registry.resolve(
            capability_id="describe_section",
            contract_version="2.0",
        )


def test_registry_lists_registrations_deterministically():
    registry = MaterializationRegistry()

    registry.register(
        capability_id="describe_section",
        contract_version="1.0",
        materializer=DescribeSectionMaterializer(),
    )

    registrations = registry.list_registrations()

    assert len(registrations) == 1
    assert (
        registrations[0].capability_id
        == "describe_section"
    )
    assert registrations[0].contract_version == "1.0"