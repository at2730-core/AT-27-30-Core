import json
from pathlib import Path

from heyti.audit.data_truth.section_universe import (
    SectionUniverseProfile,
    profile_section_universes,
)


def test_profile_preserves_exact_comparable_section_ids(
    tmp_path,
):
    master_path = tmp_path / "master.json"
    geometry_path = tmp_path / "sections.geojson"

    master_path.write_text(
        json.dumps(
            [
                {"SECCION": 10},
                {"SECCION": 20},
                {"SECCION": 30},
                {"SECCION": 40},
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
                            "SECCION": 30,
                        },
                        "geometry": None,
                    },
                    {
                        "type": "Feature",
                        "properties": {
                            "SECCION": 10,
                        },
                        "geometry": None,
                    },
                    {
                        "type": "Feature",
                        "properties": {
                            "SECCION": 50,
                        },
                        "geometry": None,
                    },
                ],
            }
        ),
        encoding="utf-8",
    )

    profile = profile_section_universes(
        master_path=master_path,
        geometry_path=geometry_path,
    )

    assert profile.comparable_sections == 2
    assert profile.comparable_section_ids == (
        10,
        30,
    )


def test_profile_default_preserves_backward_compatibility():
    profile = SectionUniverseProfile(
        master_records=0,
        geometry_records=0,
        master_unique=0,
        geometry_unique=0,
        comparable_sections=0,
        master_only=(),
        geometry_only=(),
        master_duplicates=(),
        geometry_duplicates=(),
        master_invalid_values=(),
        geometry_invalid_values=(),
    )

    assert profile.comparable_section_ids == ()


def test_real_sources_preserve_guanajuato_comparable_ids():
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

    profile = profile_section_universes(
        master_path=master_path,
        geometry_path=geometry_path,
    )

    assert profile.comparable_sections == 3230
    assert len(profile.comparable_section_ids) == 3230
    assert 1524 in profile.comparable_section_ids
    assert 9001 not in profile.comparable_section_ids
    assert 3290 not in profile.comparable_section_ids
