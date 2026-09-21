from pathlib import Path

import pytest

from heyti.capabilities.describe_section.electoral_result_source import (
    CertifiedElectoralSectionSource,
)
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


@pytest.fixture(scope="module")
def runtime_context():
    master_path, geometry_path = real_source_paths()

    composition = compose_guanajuato_2023_runtime(
        master_path=master_path,
        geometry_path=geometry_path,
    )
    composition.bootstrap.initialize()
    composition.bootstrap.session_manager.create(
        "ELECTORAL-TEST",
        object(),
    )

    return composition


def execute_section(
    composition,
    section_id: str,
):
    return (
        composition.bootstrap.runtime.execute_materialized(
            capability_name="describe_section",
            session_id="ELECTORAL-TEST",
            payload={
                "section_id": section_id,
            },
            knowledge_version="GUANAJUATO_2023:1.0",
        )
    )


def block_by_role(
    response,
    role: str,
):
    return next(
        (
            block
            for block in response.blocks
            if block.role == role
        ),
        None,
    )


def test_runtime_exposes_complete_golden_electoral_case(
    runtime_context,
):
    composition = runtime_context
    response = execute_section(
        composition,
        "1",
    )

    assert isinstance(
        composition.electoral_results,
        CertifiedElectoralSectionSource,
    )
    assert len(
        composition.electoral_results
        .authorized_section_ids
    ) == 3230

    electoral_block = block_by_role(
        response,
        "electoral",
    )

    assert response.status == "success"
    assert response.warnings == []
    assert electoral_block is not None
    assert electoral_block.type == "domain"

    content = electoral_block.content

    assert content["section_id"] == "1"
    assert content["election_year"] == 2024
    assert content["coverage_scope"] == (
        "TRACKED_PARTIES_ONLY"
    )
    assert content["quality_status"] == "COMPLETE"

    ayuntamiento = content["contests"]["A"]

    assert ayuntamiento["data_status"] == "AVAILABLE"
    assert ayuntamiento[
        "leading_tracked_party"
    ] == "PRI"
    assert ayuntamiento[
        "tracked_lead_margin"
    ] == 5.0
    assert ayuntamiento["total_votes"] == 1037.0
    assert ayuntamiento["nominal_list"] == 1573.0
    assert ayuntamiento["residual_votes"] == 51.0
    assert "winner" not in ayuntamiento


def test_runtime_preserves_partial_section_1524(
    runtime_context,
):
    response = execute_section(
        runtime_context,
        "1524",
    )

    electoral_block = block_by_role(
        response,
        "electoral",
    )

    assert response.status == "success_with_warnings"
    assert electoral_block is not None
    assert electoral_block.content[
        "quality_status"
    ] == "PARTIAL"

    ayuntamiento = electoral_block.content[
        "contests"
    ]["A"]

    assert ayuntamiento["data_status"] == "ZERO_TOTAL"
    assert ayuntamiento["total_votes"] == 0.0
    assert ayuntamiento["nominal_list"] == 620.0
    assert ayuntamiento[
        "leading_tracked_party"
    ] is None

    assert any(
        warning.code
        == "PARTIAL_ELECTORAL_COVERAGE"
        for warning in response.warnings
    )


def test_runtime_withholds_blocked_electoral_content(
    runtime_context,
):
    response = execute_section(
        runtime_context,
        "9001",
    )

    assert block_by_role(
        response,
        "territorial",
    ) is None
    assert block_by_role(
        response,
        "electoral",
    ) is None

    assert response.status == "success_with_warnings"
    assert any(
        warning.code
        == "SYNTHETIC_SECTION_CANDIDATE"
        for warning in response.warnings
    )
    assert not any(
        warning.code
        == "PARTIAL_ELECTORAL_COVERAGE"
        for warning in response.warnings
    )
