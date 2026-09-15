import json
from collections import Counter
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SectionUniverseProfile:
    """
    Reconciliación entre un maestro y una geografía de secciones.

    Describe coincidencias y diferencias sin asignarles todavía una
    interpretación histórica, sintética o administrativa.
    """

    master_records: int
    geometry_records: int
    master_unique: int
    geometry_unique: int
    comparable_sections: int
    master_only: tuple[int, ...]
    geometry_only: tuple[int, ...]
    master_duplicates: tuple[int, ...]
    geometry_duplicates: tuple[int, ...]
    master_invalid_values: tuple[str, ...]
    geometry_invalid_values: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Devuelve una representación estructurada del perfil."""

        return asdict(self)


def _normalize_section_code(
    value: Any,
) -> int | None:
    """Normaliza códigos enteros positivos sin inventar identidades."""

    if isinstance(value, bool):
        return None

    if isinstance(value, int):
        return value if value > 0 else None

    if isinstance(value, float):
        if value.is_integer() and value > 0:
            return int(value)

        return None

    if isinstance(value, str):
        normalized = value.strip()

        if normalized.isdigit():
            code = int(normalized)
            return code if code > 0 else None

    return None


def _profile_codes(
    values: list[Any],
) -> tuple[
    set[int],
    tuple[int, ...],
    tuple[str, ...],
]:
    """Obtiene códigos únicos, duplicados y valores inválidos."""

    valid_codes: list[int] = []
    invalid_values: list[str] = []

    for value in values:
        code = _normalize_section_code(value)

        if code is None:
            invalid_values.append(repr(value))
        else:
            valid_codes.append(code)

    counts = Counter(valid_codes)

    duplicates = tuple(
        sorted(
            code
            for code, count in counts.items()
            if count > 1
        )
    )

    return (
        set(valid_codes),
        duplicates,
        tuple(invalid_values),
    )


def profile_section_universes(
    master_path: str | Path,
    geometry_path: str | Path,
    master_section_field: str = "SECCION",
    geometry_section_field: str = "SECCION",
) -> SectionUniverseProfile:
    """
    Compara las secciones de un maestro JSON con un GeoJSON.

    Ninguno de los dos archivos se modifica.
    """

    master_source = Path(master_path)
    geometry_source = Path(geometry_path)

    with master_source.open(
        "r",
        encoding="utf-8-sig",
    ) as source:
        master = json.load(source)

    with geometry_source.open(
        "r",
        encoding="utf-8-sig",
    ) as source:
        geometry = json.load(source)

    if not isinstance(master, list):
        raise ValueError(
            "El maestro debe contener una lista de registros"
        )

    if not isinstance(geometry, dict):
        raise ValueError(
            "El GeoJSON debe contener un objeto"
        )

    features = geometry.get("features")

    if not isinstance(features, list):
        raise ValueError(
            "El GeoJSON debe contener una lista features"
        )

    master_values = [
        record.get(master_section_field)
        if isinstance(record, dict)
        else None
        for record in master
    ]

    geometry_values = [
        feature.get("properties", {}).get(
            geometry_section_field
        )
        if isinstance(feature, dict)
        and isinstance(
            feature.get("properties"),
            dict,
        )
        else None
        for feature in features
    ]

    (
        master_codes,
        master_duplicates,
        master_invalid,
    ) = _profile_codes(master_values)

    (
        geometry_codes,
        geometry_duplicates,
        geometry_invalid,
    ) = _profile_codes(geometry_values)

    return SectionUniverseProfile(
        master_records=len(master),
        geometry_records=len(features),
        master_unique=len(master_codes),
        geometry_unique=len(geometry_codes),
        comparable_sections=len(
            master_codes & geometry_codes
        ),
        master_only=tuple(
            sorted(master_codes - geometry_codes)
        ),
        geometry_only=tuple(
            sorted(geometry_codes - master_codes)
        ),
        master_duplicates=master_duplicates,
        geometry_duplicates=geometry_duplicates,
        master_invalid_values=master_invalid,
        geometry_invalid_values=geometry_invalid,
    )
