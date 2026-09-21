from pathlib import Path

import pytest

from heyti.capabilities.describe_section.implementation import (
    DescribeSectionCapability,
)
from heyti.kernel.kernel import HeytiKernel
from heyti.runtime.guanajuato_2023_composition import (
    compose_guanajuato_2023_runtime,
)


def real_source_paths() -> tuple[Path, Path]:
    repository_root = Path(__file__).resolve().parents[2]

    master_path = (
        repository_root
        / "datasets"
        / "electoral"
        / "Datos_Electoral_con_2015.json"
    )
    geometry_path = (
        repository_root
        / "datasets"
        / "spatial"
        / "secciones.geojson"
    )

    return master_path, geometry_path


def get_block(response, role):
    return next(
        block
        for block in response.blocks
        if block.role == role
    )


def test_certified_composition_reaches_materialized_runtime():
    master_path, geometry_path = real_source_paths()

    composition = compose_guanajuato_2023_runtime(
        master_path=master_path,
        geometry_path=geometry_path,
    )

    assert composition.territorial_truth.profile.master_records == 3310
    assert composition.territorial_truth.profile.geometry_records == 3266
    assert (
        composition.territorial_truth.profile.comparable_sections
        == 3230
    )

    bootstrap = composition.bootstrap

    assert bootstrap.registry.count() == 0

    loaded_capabilities = bootstrap.initialize()

    assert len(loaded_capabilities) == 4
    assert bootstrap.registry.count() == 4

    capability = bootstrap.registry.get("describe_section")

    assert isinstance(
        capability,
        DescribeSectionCapability,
    )
    assert (
        capability.provider.truth_source
        is composition.territorial_truth.source
    )

    bootstrap.session_manager.create(
        "SESSION-GTO-2023",
        object(),
    )

    kernel = HeytiKernel(
        bootstrap=bootstrap,
    )

    current_response = kernel.execute_materialized(
        capability_name="describe_section",
        session_id="SESSION-GTO-2023",
        payload={
            "section_id": "1524",
        },
        request_id="REQ-CURRENT-1524",
        execution_id="EXE-CURRENT-1524",
        knowledge_version="GUANAJUATO_2023:1.0",
    )

    synthetic_response = kernel.execute_materialized(
        capability_name="describe_section",
        session_id="SESSION-GTO-2023",
        payload={
            "section_id": "9001",
        },
        request_id="REQ-SYNTHETIC-9001",
        execution_id="EXE-SYNTHETIC-9001",
        knowledge_version="GUANAJUATO_2023:1.0",
    )

    current_truth = get_block(
        current_response,
        "data_truth",
    )
    synthetic_truth = get_block(
        synthetic_response,
        "data_truth",
    )

    assert current_response.status == "success_with_warnings"
    assert len(current_response.warnings) == 1
    assert current_response.warnings[0].code == (
        "PARTIAL_ELECTORAL_COVERAGE"
    )
    assert current_truth.content["classification"] == (
        "CURRENT_TERRITORIAL_SECTION"
    )
    assert current_truth.content["publication_status"] == "ALLOWED"

    assert current_response.trace.request_id == "REQ-CURRENT-1524"
    assert current_response.trace.session_id == "SESSION-GTO-2023"
    assert current_response.trace.execution_id == "EXE-CURRENT-1524"
    assert current_response.trace.knowledge_version == (
        "GUANAJUATO_2023:1.0"
    )

    assert synthetic_response.status == "success_with_warnings"
    assert len(synthetic_response.warnings) == 1
    assert synthetic_response.warnings[0].code == (
        "SYNTHETIC_SECTION_CANDIDATE"
    )
    assert synthetic_truth.content["classification"] == (
        "SYNTHETIC_CANDIDATE"
    )
    assert synthetic_truth.content["publication_status"] == "BLOCKED"

    assert synthetic_response.trace.request_id == (
        "REQ-SYNTHETIC-9001"
    )
    assert synthetic_response.trace.session_id == "SESSION-GTO-2023"
    assert synthetic_response.trace.execution_id == (
        "EXE-SYNTHETIC-9001"
    )
    assert synthetic_response.trace.knowledge_version == (
        "GUANAJUATO_2023:1.0"
    )


def test_certified_composition_fails_closed_without_sources(
    tmp_path,
):
    with pytest.raises(FileNotFoundError):
        compose_guanajuato_2023_runtime(
            master_path=tmp_path / "missing-master.json",
            geometry_path=tmp_path / "missing-geometry.geojson",
        )
