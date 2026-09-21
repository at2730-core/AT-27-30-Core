import json
import math
from copy import deepcopy
from pathlib import Path
from typing import Any, Iterable


TRACKED_PARTIES = (
    "PAN",
    "PRI",
    "PVEM",
    "MORENA",
)

ELECTORAL_CONTESTS = (
    "A",
    "DL",
    "DF",
    "G",
    "S",
    "P",
)


def _normalize_section_id(
    value: Any,
) -> str | None:
    if isinstance(value, bool):
        return None

    if isinstance(value, int):
        return str(value) if value > 0 else None

    if isinstance(value, float):
        if (
            not math.isfinite(value)
            or not value.is_integer()
            or value <= 0
        ):
            return None

        return str(int(value))

    if isinstance(value, str):
        normalized = value.strip()

        if not normalized.isdigit():
            return None

        number = int(normalized)

        return str(number) if number > 0 else None

    return None


def _finite_number(
    value: Any,
) -> bool:
    return (
        isinstance(value, (int, float))
        and not isinstance(value, bool)
        and math.isfinite(value)
    )


class CertifiedElectoralSectionSource:
    """
    Fuente electoral certificada para DescribeSection.

    Lee exclusivamente el maestro autorizado y publica valores
    explícitos de los partidos rastreados, total de votos y lista
    nominal. No infiere ganadores absolutos y no completa datos
    faltantes.
    """

    def __init__(
        self,
        master_path: str | Path,
        authorized_section_ids: Iterable[str | int],
        election_year: int = 2024,
        section_field: str = "SECCION",
    ) -> None:
        self.master_path = Path(master_path)
        self.section_field = section_field

        if (
            isinstance(election_year, bool)
            or not isinstance(election_year, int)
            or election_year < 2000
            or election_year > 9999
        ):
            raise ValueError(
                "election_year debe ser un año de cuatro dígitos"
            )

        self.election_year = election_year
        self.year_prefix = str(election_year)[-2:]

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
        try:
            with self.master_path.open(
                "r",
                encoding="utf-8-sig",
            ) as source:
                payload = json.load(source)
        except (OSError, UnicodeError, json.JSONDecodeError) as error:
            raise ValueError(
                "No fue posible leer el maestro electoral"
            ) from error

        if not isinstance(payload, list):
            raise ValueError(
                "El maestro electoral debe ser una lista"
            )

        indexed_records: dict[str, dict[str, Any]] = {}

        for record in payload:
            if not isinstance(record, dict):
                raise ValueError(
                    "El maestro electoral contiene "
                    "un registro no válido"
                )

            section_id = _normalize_section_id(
                record.get(self.section_field)
            )

            if section_id is None:
                continue

            if section_id in indexed_records:
                raise ValueError(
                    "El maestro electoral contiene una "
                    f"sección duplicada: {section_id}"
                )

            indexed_records[section_id] = record

        missing_section_ids = (
            self.authorized_section_ids
            - indexed_records.keys()
        )

        if missing_section_ids:
            raise ValueError(
                "El maestro electoral no contiene todas las "
                "secciones autorizadas: "
                f"{sorted(missing_section_ids, key=int)}"
            )

        return {
            section_id: self._build_section_content(
                section_id=section_id,
                record=indexed_records[section_id],
            )
            for section_id in self.authorized_section_ids
        }

    def _field_name(
        self,
        contest: str,
        suffix: str,
    ) -> str:
        return (
            f"{self.year_prefix}"
            f"{contest}_{suffix}"
        )

    def _build_contest_content(
        self,
        record: dict[str, Any],
        contest: str,
    ) -> dict[str, Any]:
        votes = {
            party: record.get(
                self._field_name(contest, party)
            )
            for party in TRACKED_PARTIES
        }
        total_votes = record.get(
            self._field_name(contest, "TOTAL")
        )
        nominal_list = record.get(
            self._field_name(contest, "LN")
        )

        required_values = [
            *votes.values(),
            total_votes,
            nominal_list,
        ]

        base_content: dict[str, Any] = {
            "contest_id": contest,
            "votes_by_tracked_party": votes,
            "total_votes": total_votes,
            "nominal_list": nominal_list,
            "tracked_votes": None,
            "residual_votes": None,
            "participation_rate": None,
            "leading_tracked_party": None,
            "tracked_lead_margin": None,
        }

        if not all(
            _finite_number(value)
            for value in required_values
        ):
            return {
                **base_content,
                "data_status": "INCOMPLETE",
            }

        if any(
            value < 0
            for value in required_values
        ):
            return {
                **base_content,
                "data_status": "INCONSISTENT",
            }

        tracked_votes = sum(votes.values())
        residual_votes = total_votes - tracked_votes

        derived_content = {
            **base_content,
            "tracked_votes": tracked_votes,
            "residual_votes": residual_votes,
            "participation_rate": (
                total_votes / nominal_list
                if nominal_list > 0
                else None
            ),
        }

        if (
            tracked_votes > total_votes
            or total_votes > nominal_list
            or nominal_list <= 0
        ):
            return {
                **derived_content,
                "data_status": "INCONSISTENT",
            }

        if total_votes == 0:
            return {
                **derived_content,
                "data_status": "ZERO_TOTAL",
            }

        ordered_votes = sorted(
            votes.items(),
            key=lambda item: (
                -item[1],
                item[0],
            ),
        )

        first_party, first_votes = ordered_votes[0]
        _, second_votes = ordered_votes[1]

        if first_votes == second_votes:
            return {
                **derived_content,
                "data_status": "TIED_TRACKED_LEAD",
            }

        return {
            **derived_content,
            "data_status": "AVAILABLE",
            "leading_tracked_party": first_party,
            "tracked_lead_margin": (
                first_votes - second_votes
            ),
        }

    def _build_section_content(
        self,
        section_id: str,
        record: dict[str, Any],
    ) -> dict[str, Any]:
        contests = {
            contest: self._build_contest_content(
                record=record,
                contest=contest,
            )
            for contest in ELECTORAL_CONTESTS
        }

        quality_status = (
            "COMPLETE"
            if all(
                content["data_status"] == "AVAILABLE"
                for content in contests.values()
            )
            else "PARTIAL"
        )

        return {
            "section_id": section_id,
            "election_year": self.election_year,
            "coverage_scope": "TRACKED_PARTIES_ONLY",
            "tracked_parties": list(TRACKED_PARTIES),
            "quality_status": quality_status,
            "contests": contests,
        }

    def get_section_electoral(
        self,
        section_id: str,
    ) -> dict[str, Any] | None:
        """
        Devuelve una copia del contenido electoral autorizado.
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
