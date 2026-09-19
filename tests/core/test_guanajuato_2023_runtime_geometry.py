from pathlib import Path

from heyti.capabilities.describe_section.territorial_geometry_source import (
    CertifiedGeoJsonSectionSource,
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


def materialized_response(
    section_id: str,
):
    master_path, geometry_path = real_source_paths()

    composition = compose_guanajuato_2023_runtime(
        master_path=master_path,
        geometry_path=geometry_path,
    )
    composition.bootstrap.initialize()
    composition.bootstrap.session_manager.create(
        "GEOMETRY-TEST",
        object(),
    )

    response = (
        composition.bootstrap.runtime.execute_materialized(
            capability_name="describe_section",
            session_id="GEOMETRY-TEST",
            payload={
                "section_id": section_id,
            },
            knowledge_version="GUANAJUATO_2023:1.0",
        )
    )

    return composition, response


def block_by_role(response, role: str):
    return next(
        (
            block
            for block in response.blocks
            if block.role == role
        ),
        None,
    )


def test_composition_exposes_certified_current_geometry():
    composition, response = materialized_response(
        "1524"
    )

    assert isinstance(
        composition.territorial_geometry,
        CertifiedGeoJsonSectionSource,
    )
    assert len(
        composition.territorial_geometry
        .authorized_section_ids
    ) == 3230

    truth_block = block_by_role(
        response,
        "data_truth",
    )
    territorial_block = block_by_role(
        response,
        "territorial",
    )

    assert truth_block is not None
    assert truth_block.content[
        "publication_status"
    ] == "ALLOWED"

    assert territorial_block is not None
    assert territorial_block.type == "domain"
    assert set(territorial_block.content) == {
        "section_id",
        "crs",
        "geometry",
    }
    assert territorial_block.content[
        "section_id"
    ] == "1524"
    assert territorial_block.content[
        "crs"
    ] == "OGC:CRS84"
    assert territorial_block.content[
        "geometry"
    ]["type"] == "MultiPolygon"
    assert territorial_block.content[
        "geometry"
    ]["coordinates"]


def test_composition_withholds_blocked_geometry():
    _, response = materialized_response(
        "9001"
    )

    truth_block = block_by_role(
        response,
        "data_truth",
    )
    territorial_block = block_by_role(
        response,
        "territorial",
    )

    assert truth_block is not None
    assert truth_block.content[
        "publication_status"
    ] == "BLOCKED"
    assert territorial_block is None
    assert response.status == "success_with_warnings"
    assert response.warnings[0].code == (
        "SYNTHETIC_SECTION_CANDIDATE"
    )
