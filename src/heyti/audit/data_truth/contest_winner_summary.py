import json
import math
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

from heyti.audit.data_truth.contest_winner import (
    profile_contest_winners_without_party_votes,
)


@dataclass(frozen=True)
class ContestWinnerSummary:
    """Resumen agregado de ganadores sin respaldo partidista."""

    total_findings: int
    affected_sections: tuple[str, ...]
    winner_field_counts: dict[str, int] = field(
        default_factory=dict,
    )
    total_positive: int = 0
    total_zero: int = 0
    total_unavailable: int = 0
    ln_positive: int = 0
    ln_zero: int = 0
    ln_unavailable: int = 0

    def to_dict(self) -> dict[str, Any]:
        """Devuelve una representación estructurada del resumen."""

        return asdict(self)


def _numeric_state(
    value: Any,
) -> str:
    """Clasifica un valor para fines diagnósticos."""

    if (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    ):
        if value > 0:
            return "POSITIVE"

        if value == 0:
            return "ZERO"

    return "UNAVAILABLE"


def summarize_contest_winners_without_party_votes(
    path: str | Path,
) -> ContestWinnerSummary:
    """Resume los casos detectados sin alterar la fuente."""

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

    records_by_section = {
        str(record["SECCION"]).strip(): record
        for record in records
        if isinstance(record, dict)
        and "SECCION" in record
    }

    findings = (
        profile_contest_winners_without_party_votes(
            source_path
        )
    )

    winner_field_counts = Counter()
    total_states = Counter()
    ln_states = Counter()

    for finding in findings:
        record = records_by_section[
            finding.section_code
        ]

        contest_prefix = (
            finding.winner_field
            .removeprefix("GANADOR_")
            + "_"
        )

        winner_field_counts[
            finding.winner_field
        ] += 1

        total_states[
            _numeric_state(
                record.get(
                    contest_prefix + "TOTAL"
                )
            )
        ] += 1

        ln_states[
            _numeric_state(
                record.get(
                    contest_prefix + "LN"
                )
            )
        ] += 1

    affected_sections = tuple(
        sorted(
            {
                finding.section_code
                for finding in findings
            },
            key=lambda value: int(value),
        )
    )

    return ContestWinnerSummary(
        total_findings=len(findings),
        affected_sections=affected_sections,
        winner_field_counts=dict(
            sorted(winner_field_counts.items())
        ),
        total_positive=total_states["POSITIVE"],
        total_zero=total_states["ZERO"],
        total_unavailable=total_states["UNAVAILABLE"],
        ln_positive=ln_states["POSITIVE"],
        ln_zero=ln_states["ZERO"],
        ln_unavailable=ln_states["UNAVAILABLE"],
    )
