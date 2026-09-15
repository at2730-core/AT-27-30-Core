import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class WinnerWithoutNumericEvidence:
    """
    Registro que contiene ganadores pero carece de evidencia numérica
    finita distinta de cero.
    """

    section_code: str
    winner_fields: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Devuelve una representación estructurada del hallazgo."""

        return asdict(self)


def _is_finite_nonzero_number(
    value: Any,
) -> bool:
    """Reconoce evidencia numérica finita distinta de cero."""

    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and value != 0
    )


def profile_winners_without_numeric_evidence(
    path: str | Path,
    section_field: str = "SECCION",
    winner_prefix: str = "GANADOR_",
) -> tuple[WinnerWithoutNumericEvidence, ...]:
    """
    Localiza ganadores almacenados sin evidencia numérica finita.

    La revisión es diagnóstica: no recalcula, elimina ni sustituye
    ganadores.
    """

    source_path = Path(path)

    with source_path.open(
        "r",
        encoding="utf-8-sig",
    ) as source:
        records = json.load(source)

    if not isinstance(records, list):
        raise ValueError(
            "El maestro electoral debe contener una lista de registros"
        )

    findings: list[WinnerWithoutNumericEvidence] = []

    for record in records:
        if not isinstance(record, dict):
            continue

        winner_fields = tuple(
            sorted(
                key
                for key, value in record.items()
                if key.startswith(winner_prefix)
                and isinstance(value, str)
                and value.strip()
            )
        )

        if not winner_fields:
            continue

        has_numeric_evidence = any(
            _is_finite_nonzero_number(value)
            for key, value in record.items()
            if key != section_field
        )

        if not has_numeric_evidence:
            findings.append(
                WinnerWithoutNumericEvidence(
                    section_code=str(
                        record.get(section_field, "")
                    ).strip(),
                    winner_fields=winner_fields,
                )
            )

    return tuple(findings)
