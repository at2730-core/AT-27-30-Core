import json
from pathlib import Path

import pytest

from heyti.audit.data_truth.section_universe import (
    profile_section_universes,
)


def write_json(
    path: Path,
    value,
) -> Path:
    path.write_text(
        json.dumps(value),
        encoding="utf-8",
    )
    return path


def build_geojson(section_codes):
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "SECCION": code,
                },
                "geometry": None,
            }
            for code in section_codes
        ],
    }


def test_profiles_matching_universes(tmp_path):
    master = write_json(
        tmp_path / "master.json",
        [
            {"SECCION": 1},
            {"SECCION": 2},
        ],
    )

    geometry = write_json(
        tmp_path / "sections.geojson",
        build_geojson([1, 2]),
    )

    profile = profile_section_universes(
        master,
        geometry,
    )

    assert profile.master_unique == 2
    assert profile.geometry_unique == 2
    assert profile.comparable_sections == 2
    assert profile.master_only == ()
    assert profile.geometry_only == ()


def test_profiles_both_directions_of_difference(tmp_path):
    master = write_json(
        tmp_path / "master.json",
        [
            {"SECCION": 1},
            {"SECCION": 2},
            {"SECCION": 9001},
        ],
    )

    geometry = write_json(
        tmp_path / "sections.geojson",
        build_geojson([1, 2, 3]),
    )

    profile = profile_section_universes(
        master,
        geometry,
    )

    assert profile.comparable_sections == 2
    assert profile.master_only == (9001,)
    assert profile.geometry_only == (3,)


def test_profiles_duplicates_and_invalid_values(tmp_path):
    master = write_json(
        tmp_path / "master.json",
        [
            {"SECCION": 1},
            {"SECCION": "1"},
            {"SECCION": 0},
            {"SECCION": "ABC"},
        ],
    )

    geometry = write_json(
        tmp_path / "sections.geojson",
        build_geojson([1, 1, None]),
    )

    profile = profile_section_universes(
        master,
        geometry,
    )

    assert profile.master_duplicates == (1,)
    assert profile.geometry_duplicates == (1,)
    assert profile.master_invalid_values == (
        "0",
        "'ABC'",
    )
    assert profile.geometry_invalid_values == (
        "None",
    )


def test_rejects_non_list_master(tmp_path):
    master = write_json(
        tmp_path / "master.json",
        {"SECCION": 1},
    )

    geometry = write_json(
        tmp_path / "sections.geojson",
        build_geojson([1]),
    )

    with pytest.raises(
        ValueError,
        match="lista de registros",
    ):
        profile_section_universes(
            master,
            geometry,
        )


def test_rejects_geojson_without_features(tmp_path):
    master = write_json(
        tmp_path / "master.json",
        [{"SECCION": 1}],
    )

    geometry = write_json(
        tmp_path / "sections.geojson",
        {
            "type": "FeatureCollection",
        },
    )

    with pytest.raises(
        ValueError,
        match="lista features",
    ):
        profile_section_universes(
            master,
            geometry,
        )


def test_profile_does_not_modify_sources(tmp_path):
    master = write_json(
        tmp_path / "master.json",
        [{"SECCION": 1}],
    )

    geometry = write_json(
        tmp_path / "sections.geojson",
        build_geojson([1]),
    )

    master_before = master.read_bytes()
    geometry_before = geometry.read_bytes()

    profile_section_universes(
        master,
        geometry,
    )

    assert master.read_bytes() == master_before
    assert geometry.read_bytes() == geometry_before
