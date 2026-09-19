import json
from collections.abc import Iterable
from copy import deepcopy
from pathlib import Path
from typing import Any


EXPECTED_CRS_NAME = "urn:ogc:def:crs:OGC:1.3:CRS84"
PUBLIC_CRS_NAME = "OGC:CRS84"
SUPPORTED_GEOMETRY_TYPES = frozenset(
    {
        "Polygon",
        "MultiPolygon",
    }
)


def _normalize_section_id(
    value: Any,
) -> str | None:
    """
    Normaliza identificadores enteros positivos sin inventarlos.
    """

    if isinstance(value, bool):
        return None

    if isinstance(value, int):
        return str(value) if value > 0 else None

    if isinstance(value, float):
        if value.is_integer() and value > 0:
            return str(int(value))

        return None

    if isinstance(value, str):
        normalized = value.strip()

        if normalized.isdigit() and int(normalized) > 0:
            return str(int(normalized))

    return None


class CertifiedGeoJsonSectionSource:
    """
    Fuente de geometría territorial autorizada para DescribeSection.

    Carga un FeatureCollection certificado, valida su estructura
    y conserva únicamente las secciones cuya publicación fue
    autorizada por el ensamblaje territorial.

    No modifica la fuente y no expone propiedades crudas.
    """

    def __init__(
        self,
        geometry_path: str | Path,
        authorized_section_ids: Iterable[str | int],
        section_field: str = "SECCION",
    ) -> None:
        self.geometry_path = Path(geometry_path)
        self.section_field = section_field

        normalized_authorized_ids = {
            _normalize_section_id(section_id)
            for section_id in authorized_section_ids
        }

        if None in normalized_authorized_ids:
            raise TypeError(
                "authorized_section_ids debe contener "
                "identificadores enteros positivos"
            )

        self.authorized_section_ids = frozenset(
            section_id
            for section_id in normalized_authorized_ids
            if section_id is not None
        )

        if not self.authorized_section_ids:
            raise ValueError(
                "authorized_section_ids no puede estar vacío"
            )

        self._sections = self._load_sections()

    def _load_sections(
        self,
    ) -> dict[str, dict[str, Any]]:
        with self.geometry_path.open(
            "r",
            encoding="utf-8-sig",
        ) as source:
            payload = json.load(source)

        if not isinstance(payload, dict):
            raise TypeError(
                "La fuente geométrica debe contener un objeto JSON"
            )

        if payload.get("type") != "FeatureCollection":
            raise ValueError(
                "La fuente geométrica debe ser FeatureCollection"
            )

        features = payload.get("features")

        if not isinstance(features, list):
            raise TypeError(
                "FeatureCollection.features debe ser list"
            )

        crs = payload.get("crs")

        if not isinstance(crs, dict):
            raise ValueError(
                "La fuente geométrica no declara CRS"
            )

        crs_properties = crs.get("properties")

        if not isinstance(crs_properties, dict):
            raise ValueError(
                "La declaración CRS no contiene properties"
            )

        if crs_properties.get("name") != EXPECTED_CRS_NAME:
            raise ValueError(
                "La fuente geométrica no utiliza CRS84"
            )

        observed_section_ids: set[str] = set()
        authorized_sections: dict[
            str,
            dict[str, Any],
        ] = {}

        for index, feature in enumerate(features):
            if not isinstance(feature, dict):
                raise TypeError(
                    f"Feature {index} debe ser un objeto"
                )

            if feature.get("type") != "Feature":
                raise ValueError(
                    f"Feature {index} no declara type=Feature"
                )

            properties = feature.get("properties")

            if not isinstance(properties, dict):
                raise TypeError(
                    f"Feature {index} no contiene properties"
                )

            section_id = _normalize_section_id(
                properties.get(self.section_field)
            )

            if section_id is None:
                raise ValueError(
                    f"Feature {index} contiene una sección inválida"
                )

            if section_id in observed_section_ids:
                raise ValueError(
                    "La fuente geométrica contiene una sección "
                    f"duplicada: {section_id}"
                )

            observed_section_ids.add(section_id)

            geometry = feature.get("geometry")

            if not isinstance(geometry, dict):
                raise TypeError(
                    f"La sección {section_id} no contiene geometría"
                )

            geometry_type = geometry.get("type")

            if geometry_type not in SUPPORTED_GEOMETRY_TYPES:
                raise ValueError(
                    f"Geometría no soportada para {section_id}: "
                    f"{geometry_type}"
                )

            coordinates = geometry.get("coordinates")

            if not isinstance(coordinates, list) or not coordinates:
                raise ValueError(
                    f"La sección {section_id} no contiene coordenadas"
                )

            if section_id not in self.authorized_section_ids:
                continue

            authorized_sections[section_id] = {
                "section_id": section_id,
                "crs": PUBLIC_CRS_NAME,
                "geometry": deepcopy(geometry),
            }

        missing_section_ids = (
            self.authorized_section_ids
            - authorized_sections.keys()
        )

        if missing_section_ids:
            raise ValueError(
                "La fuente geométrica no contiene todas las "
                "secciones autorizadas: "
                f"{sorted(missing_section_ids, key=int)}"
            )

        return authorized_sections

    def get_section_territorial(
        self,
        section_id: str,
    ) -> dict[str, Any] | None:
        """
        Devuelve una copia de la geometría autorizada.

        Las identidades no autorizadas no producen contenido
        territorial.
        """

        normalized_section_id = _normalize_section_id(
            section_id
        )

        if normalized_section_id is None:
            return None

        content = self._sections.get(
            normalized_section_id
        )

        return (
            deepcopy(content)
            if content is not None
            else None
        )
