import hashlib
import json
from pathlib import Path

import pytest

from heyti.capabilities.describe_section.provider import (
    DescribeSectionProvider,
)
from heyti.capabilities.describe_section.territorial_truth_factory import (
    build_guanajuato_2023_territorial_truth,
)
from heyti.materialization.context import MaterializationContext
from heyti.materialization.describe_section.materializer import (
    DescribeSectionMaterializer,
)
from heyti.materialization.validator import (
    ResponseContractValidator,
)


def sha256(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


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


def materialize(source, section_id):
    description = DescribeSectionProvider(
        truth_source=source,
    ).get_section(
        section_id=section_id,
    )

    response = DescribeSectionMaterializer().materialize(
        description,
        MaterializationContext(
            capability_id="describe_section",
        ),
    )

    return ResponseContractValidator().validate(
        response
    )


def test_real_factory_builds_certified_read_only_assembly():
    master_path, geometry_path = real_source_paths()

    master_before = sha256(master_path)
    geometry_before = sha256(geometry_path)

    assembly = build_guanajuato_2023_territorial_truth(
        master_path=master_path,
        geometry_path=geometry_path,
    )

    assert assembly.profile.master_records == 3310
    assert assembly.profile.geometry_records == 3266
    assert assembly.profile.comparable_sections == 3230
    assert len(
        assembly.profile.comparable_section_ids
    ) == 3230

    current_response = materialize(
        assembly.source,
        "1524",
    )
    synthetic_response = materialize(
        assembly.source,
        "9001",
    )

    current_truth = next(
        block
        for block in current_response.blocks
        if block.role == "data_truth"
    )
    synthetic_truth = next(
        block
        for block in synthetic_response.blocks
        if block.role == "data_truth"
    )

    assert current_response.status == "success"
    assert current_response.warnings == []
    assert current_truth.content["classification"] == (
        "CURRENT_TERRITORIAL_SECTION"
    )
    assert (
        current_truth.content["publication_status"]
        == "ALLOWED"
    )

    assert (
        synthetic_response.status
        == "success_with_warnings"
    )
    assert synthetic_response.warnings[0].code == (
        "SYNTHETIC_SECTION_CANDIDATE"
    )
    assert synthetic_truth.content["publication_status"] == (
        "BLOCKED"
    )

    assert sha256(master_path) == master_before
    assert sha256(geometry_path) == geometry_before


def test_factory_fails_closed_for_incomplete_sources(
    tmp_path,
):
    master_path = tmp_path / "master.json"
    geometry_path = tmp_path / "sections.geojson"

    master_path.write_text(
        json.dumps(
            [
                {
                    "SECCION": 1524,
                }
            ]
        ),
        encoding="utf-8",
    )
    geometry_path.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {
                        "type": "Feature",
                        "properties": {
                            "SECCION": 1524,
                        },
                        "geometry": None,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="no coincide con GUANAJUATO_2023",
    ):
        build_guanajuato_2023_territorial_truth(
            master_path=master_path,
            geometry_path=geometry_path,
        )


def test_factory_propagates_missing_source_failure(
    tmp_path,
):
    with pytest.raises(FileNotFoundError):
        build_guanajuato_2023_territorial_truth(
            master_path=tmp_path / "missing-master.json",
            geometry_path=tmp_path / "missing-geometry.geojson",
        )
