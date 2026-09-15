import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


DEFAULT_PARTIES = (
    "PAN",
    "PRI",
    "PVEM",
    "MORENA",
)


@dataclass(frozen=True)
class ContestWinnerWithoutPartyVotes:
    """Ganador almacenado sin votos partidistas positivos en su elección."""

    section_code: str
    winner_field: str
    stored_winner: str
    party_fields: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Devuelve una representación estructurada del hallazgo."""

        return asdict(self)


def _is_positive_finite_number(
    value: Any,
) -> bool:
    """Reconoce votos partidistas positivos y finitos."""

    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
        and value > 0
    )


def _contest_prefix(
    winner_field: str,
    winner_prefix: str,
) -> str:
    """Obtiene el prefijo numérico correspondiente al campo ganador."""

    return winner_field.removeprefix(
        winner_prefix
    ) + "_"


def profile_contest_winners_without_party_votes(
    path: str | Path,
    section_field: str = "SECCION",
    winner_prefix: str = "GANADOR_",
    parties: tuple[str, ...] = DEFAULT_PARTIES,
) -> tuple[ContestWinnerWithoutPartyVotes, ...]:
    """
    Localiza ganadores sin votos partidistas positivos en su elección.

    Totales, lista nominal, participación y valores de otras elecciones
    no se consideran evidencia del ganador evaluado.
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

    findings: list[ContestWinnerWithoutPartyVotes] = []

    for record in records:
        if not isinstance(record, dict):
            continue

        section_code = str(
            record.get(section_field, "")
        ).strip()

        winner_fields = sorted(
            key
            for key, value in record.items()
            if key.startswith(winner_prefix)
            and isinstance(value, str)
            and value.strip()
        )

        for winner_field in winner_fields:
            contest_prefix = _contest_prefix(
                winner_field,
                winner_prefix,
            )

            party_fields = tuple(
                contest_prefix + party
                for party in parties
            )

            has_party_votes = any(
                _is_positive_finite_number(
                    record.get(field)
                )
                for field in party_fields
            )

            if not has_party_votes:
                findings.append(
                    ContestWinnerWithoutPartyVotes(
                        section_code=section_code,
                        winner_field=winner_field,
                        stored_winner=str(
                            record[winner_field]
                        ).strip(),
                        party_fields=party_fields,
                    )
                )

    return tuple(findings)
