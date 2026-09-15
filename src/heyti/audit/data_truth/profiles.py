import json
import math
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class NonFiniteJsonProfile:
    """
    Perfil de valores numéricos no finitos presentes en una fuente JSON.

    El perfil describe la fuente sin corregirla ni reinterpretarla.
    """

    total_values: int
    affected_records: int
    affected_fields: int
    field_counts: dict[str, int] = field(
        default_factory=dict,
    )

    def to_dict(self) -> dict[str, Any]:
        """Devuelve una representación estructurada del perfil."""

        return asdict(self)


def _is_non_finite(value: Any) -> bool:
    """Indica si el valor es NaN o infinito."""

    return (
        isinstance(value, float)
        and not math.isfinite(value)
    )


def _collect_non_finite_paths(
    value: Any,
    prefix: str = "",
) -> list[str]:
    """Recorre una estructura y devuelve rutas con valores no finitos."""

    if _is_non_finite(value):
        return [prefix or "$"]

    if isinstance(value, dict):
        paths: list[str] = []

        for key, child in value.items():
            child_prefix = (
                f"{prefix}.{key}"
                if prefix
                else str(key)
            )

            paths.extend(
                _collect_non_finite_paths(
                    child,
                    child_prefix,
                )
            )

        return paths

    if isinstance(value, list):
        paths = []

        for index, child in enumerate(value):
            child_prefix = (
                f"{prefix}[{index}]"
                if prefix
                else f"[{index}]"
            )

            paths.extend(
                _collect_non_finite_paths(
                    child,
                    child_prefix,
                )
            )

        return paths

    return []


def profile_json_non_finite(
    path: str | Path,
) -> NonFiniteJsonProfile:
    """
    Cuenta NaN e infinitos mediante la lectura permisiva de Python.

    Esta lectura se utiliza exclusivamente para diagnóstico. No convierte
    valores ni produce una nueva fuente.
    """

    source_path = Path(path)

    with source_path.open(
        "r",
        encoding="utf-8-sig",
    ) as source:
        parsed = json.load(source)

    records = (
        parsed
        if isinstance(parsed, list)
        else [parsed]
    )

    field_counts: Counter[str] = Counter()
    affected_records = 0

    for record in records:
        paths = _collect_non_finite_paths(record)

        if paths:
            affected_records += 1
            field_counts.update(paths)

    return NonFiniteJsonProfile(
        total_values=sum(field_counts.values()),
        affected_records=affected_records,
        affected_fields=len(field_counts),
        field_counts=dict(
            sorted(field_counts.items())
        ),
    )
