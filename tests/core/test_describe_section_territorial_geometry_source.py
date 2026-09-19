import hashlib
import json
from pathlib import Path

import pytest

from heyti.capabilities.describe_section.territorial_geometry_source import (
    CertifiedGeoJsonSectionSource,
)


EXPECTED_CRS = {
    "type": "name",
    "properties": {
        "name": "urn:ogc:def:crs:OGC:1.3:CRS84",
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def real_geometry_path() -> Path:
    repository_root = Path(__file__).resolve().parents[2]

    return (
        repository_root
        / "datasets"
        / "spatial"
        / "secciones.geojson"
    )


def feature(
    section_id: int,
    *,
    geometry_type: str = "MultiPolygon",
    coordinates=None,
) -> dict:
    resolved_coordinates = (
        coordinates
        if coordinates is not None
        else [
            [
                [
                    [-101.7, 21.1],
                    [-101.6, 21.1],
                    [-101.6, 21.2],
                    [-101.7, 21.1],
                ]
            ]
        ]
    )

    return {
        "type": "Feature",
        "properties": {
            "SECCION": section_id,
            "CONTROL": "NO_PUBLICAR",
        },
        "geometry": {
            "type": geometry_type,
            "coordinates": resolved_coordinates,
        },
    }


def write_geojson(
    path: Path,
    features: list[dict],
    *,
    crs: dict = EXPECTED_CRS,
) -> None:
    path.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "name": "test-sections",
                "crs": crs,
                "features": features,
            }
        ),
        encoding="utf-8",
    )


def test_real_source_returns_only_authorized_minimal_geometry():
    geometry_path = real_geometry_path()
    source_before = sha256(geometry_path)

    source = CertifiedGeoJsonSectionSource(
        geometry_path=geometry_path,
        authorized_section_ids={
            "1524",
        },
    )

    territorial = source.get_section_territorial(
        "1524"
    )

    assert territorial is not None
    assert set(territorial) == {
        "section_id",
        "crs",
        "geometry",
    }
    assert territorial["section_id"] == "1524"
    assert territorial["crs"] == "OGC:CRS84"
    assert territorial["geometry"]["type"] == (
        "MultiPolygon"
    )
    assert territorial["geometry"]["coordinates"]
    assert "properties" not in territorial
    assert source.get_section_territorial("9001") is None
    assert sha256(geometry_path) == source_before


def test_source_returns_defensive_geometry_copy():
    source = CertifiedGeoJsonSectionSource(
        geometry_path=real_geometry_path(),
        authorized_section_ids={
            "1524",
        },
    )

    first = source.get_section_territorial("1524")
    second = source.get_section_territorial("1524")

    assert first is not None
    assert second is not None
    assert first == second
    assert first is not second
    assert first["geometry"] is not second["geometry"]

    first["geometry"]["coordinates"].clear()

    preserved = source.get_section_territorial("1524")

    assert preserved is not None
    assert preserved["geometry"]["coordinates"]


def test_source_rejects_invalid_authorized_section_id(
    tmp_path,
):
    geometry_path = tmp_path / "sections.geojson"
    write_geojson(
        geometry_path,
        [
            feature(1524),
        ],
    )

    with pytest.raises(
        TypeError,
        match="identificadores enteros positivos",
    ):
        CertifiedGeoJsonSectionSource(
            geometry_path=geometry_path,
            authorized_section_ids={
                "invalid",
            },
        )


def test_source_rejects_empty_authorization(
    tmp_path,
):
    geometry_path = tmp_path / "sections.geojson"
    write_geojson(
        geometry_path,
        [
            feature(1524),
        ],
    )

    with pytest.raises(
        ValueError,
        match="no puede estar vacío",
    ):
        CertifiedGeoJsonSectionSource(
            geometry_path=geometry_path,
            authorized_section_ids=set(),
        )


def test_source_rejects_unexpected_crs(
    tmp_path,
):
    geometry_path = tmp_path / "sections.geojson"
    write_geojson(
        geometry_path,
        [
            feature(1524),
        ],
        crs={
            "type": "name",
            "properties": {
                "name": "EPSG:3857",
            },
        },
    )

    with pytest.raises(
        ValueError,
        match="no utiliza CRS84",
    ):
        CertifiedGeoJsonSectionSource(
            geometry_path=geometry_path,
            authorized_section_ids={
                "1524",
            },
        )


def test_source_rejects_missing_authorized_section(
    tmp_path,
):
    geometry_path = tmp_path / "sections.geojson"
    write_geojson(
        geometry_path,
        [
            feature(1524),
        ],
    )

    with pytest.raises(
        ValueError,
        match="no contiene todas las secciones autorizadas",
    ):
        CertifiedGeoJsonSectionSource(
            geometry_path=geometry_path,
            authorized_section_ids={
                "1524",
                "2000",
            },
        )


def test_source_rejects_duplicate_section_geometry(
    tmp_path,
):
    geometry_path = tmp_path / "sections.geojson"
    write_geojson(
        geometry_path,
        [
            feature(1524),
            feature(1524),
        ],
    )

    with pytest.raises(
        ValueError,
        match="sección duplicada: 1524",
    ):
        CertifiedGeoJsonSectionSource(
            geometry_path=geometry_path,
            authorized_section_ids={
                "1524",
            },
        )


def test_source_rejects_unsupported_geometry(
    tmp_path,
):
    geometry_path = tmp_path / "sections.geojson"
    write_geojson(
        geometry_path,
        [
            feature(
                1524,
                geometry_type="Point",
                coordinates=[
                    -101.7,
                    21.1,
                ],
            ),
        ],
    )

    with pytest.raises(
        ValueError,
        match="Geometría no soportada para 1524",
    ):
        CertifiedGeoJsonSectionSource(
            geometry_path=geometry_path,
            authorized_section_ids={
                "1524",
            },
        )
