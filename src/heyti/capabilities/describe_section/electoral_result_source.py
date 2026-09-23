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


HISTORICAL_ELECTION_YEARS = (
    2018,
    2021,
)

CONTESTED_CONTESTS_BY_YEAR = {
    2018: frozenset(ELECTORAL_CONTESTS),
    2021: frozenset(("A", "DL", "DF")),
}

HISTORICAL_CONTEST_PROFILES = {
    (2018, "DF"): "WITHOUT_NOMINAL_LIST",
    (2021, "DF"): "SUMMARY_ONLY",
}


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
        quarantined_contests: Iterable[str] = (),
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

        if isinstance(
            quarantined_contests,
            (str, bytes),
        ):
            raise TypeError(
                "quarantined_contests debe ser un iterable "
                "de identificadores de contienda"
            )

        try:
            normalized_quarantined_contests = frozenset(
                quarantined_contests
            )
        except TypeError as error:
            raise TypeError(
                "quarantined_contests debe ser un iterable "
                "de identificadores de contienda"
            ) from error

        if any(
            not isinstance(contest, str)
            for contest in normalized_quarantined_contests
        ):
            raise TypeError(
                "quarantined_contests debe contener "
                "identificadores de texto"
            )

        unknown_quarantined_contests = (
            normalized_quarantined_contests
            - set(ELECTORAL_CONTESTS)
        )

        if unknown_quarantined_contests:
            raise ValueError(
                "quarantined_contests contiene contiendas "
                "no soportadas: "
                f"{sorted(unknown_quarantined_contests)}"
            )

        self.quarantined_contests = (
            normalized_quarantined_contests
        )

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
        election_year: int | None = None,
    ) -> str:
        selected_year = (
            self.election_year
            if election_year is None
            else election_year
        )

        return (
            f"{str(selected_year)[-2:]}"
            f"{contest}_{suffix}"
        )

    @staticmethod
    def _empty_contest_content(
        contest: str,
        data_status: str,
    ) -> dict[str, Any]:
        return {
            "contest_id": contest,
            "votes_by_tracked_party": {
                party: None
                for party in TRACKED_PARTIES
            },
            "total_votes": None,
            "nominal_list": None,
            "tracked_votes": None,
            "residual_votes": None,
            "participation_rate": None,
            "leading_tracked_party": None,
            "tracked_lead_margin": None,
            "data_status": data_status,
        }

    def _contest_is_applicable(
        self,
        election_year: int,
        contest: str,
    ) -> bool:
        contested = CONTESTED_CONTESTS_BY_YEAR.get(
            election_year
        )

        return (
            contest in contested
            if contested is not None
            else True
        )

    def _build_contest_content(
        self,
        record: dict[str, Any],
        contest: str,
        election_year: int | None = None,
    ) -> dict[str, Any]:
        selected_year = (
            self.election_year
            if election_year is None
            else election_year
        )
        data_profile = HISTORICAL_CONTEST_PROFILES.get(
            (
                selected_year,
                contest,
            )
        )

        if not self._contest_is_applicable(
            selected_year,
            contest,
        ):
            return self._empty_contest_content(
                contest=contest,
                data_status="NOT_CONTESTED",
            )

        if contest in self.quarantined_contests:
            return self._empty_contest_content(
                contest=contest,
                data_status="INCONSISTENT",
            )

        raw_votes = {
            party: record.get(
                self._field_name(
                    contest,
                    party,
                    selected_year,
                )
            )
            for party in TRACKED_PARTIES
        }
        raw_total_votes = record.get(
            self._field_name(
                contest,
                "TOTAL",
                selected_year,
            )
        )
        raw_nominal_list = record.get(
            self._field_name(
                contest,
                "LN",
                selected_year,
            )
        )

        votes = {
            party: (
                value
                if _finite_number(value)
                else None
            )
            for party, value in raw_votes.items()
        }
        total_votes = (
            raw_total_votes
            if _finite_number(raw_total_votes)
            else None
        )
        nominal_list = (
            raw_nominal_list
            if _finite_number(raw_nominal_list)
            else None
        )

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

        finite_votes = [
            value
            for value in votes.values()
            if value is not None
        ]
        has_all_votes = (
            len(finite_votes) == len(TRACKED_PARTIES)
        )
        has_no_votes = not finite_votes

        if (
            data_profile == "SUMMARY_ONLY"
            and has_no_votes
            and total_votes is not None
            and nominal_list is not None
        ):
            summary_content = {
                **base_content,
                "participation_rate": (
                    total_votes / nominal_list
                    if nominal_list > 0
                    else None
                ),
            }

            if (
                total_votes < 0
                or nominal_list <= 0
                or total_votes > nominal_list
            ):
                return {
                    **summary_content,
                    "data_status": "INCONSISTENT",
                }

            return {
                **summary_content,
                "data_status": "SUMMARY_ONLY",
            }

        if (
            not has_all_votes
            or total_votes is None
            or (
                nominal_list is None
                and data_profile != "WITHOUT_NOMINAL_LIST"
            )
        ):
            return {
                **base_content,
                "data_status": "INCOMPLETE",
            }

        tracked_votes = sum(finite_votes)
        residual_votes = total_votes - tracked_votes

        derived_content = {
            **base_content,
            "tracked_votes": tracked_votes,
            "residual_votes": residual_votes,
            "participation_rate": (
                total_votes / nominal_list
                if (
                    nominal_list is not None
                    and nominal_list > 0
                )
                else None
            ),
        }

        if (
            any(value < 0 for value in finite_votes)
            or total_votes < 0
            or tracked_votes > total_votes
            or (
                nominal_list is not None
                and (
                    nominal_list <= 0
                    or total_votes > nominal_list
                )
            )
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
            "data_status": (
                "AVAILABLE_WITHOUT_NOMINAL_LIST"
                if data_profile == "WITHOUT_NOMINAL_LIST"
                else "AVAILABLE"
            ),
            "leading_tracked_party": first_party,
            "tracked_lead_margin": (
                first_votes - second_votes
            ),
        }
    def _build_election_content(
        self,
        record: dict[str, Any],
        election_year: int,
    ) -> dict[str, Any]:
        contests = {
            contest: self._build_contest_content(
                record=record,
                contest=contest,
                election_year=election_year,
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
            "election_year": election_year,
            "quality_status": quality_status,
            "contests": contests,
        }

    def _build_section_content(
        self,
        section_id: str,
        record: dict[str, Any],
    ) -> dict[str, Any]:
        current_election = self._build_election_content(
            record=record,
            election_year=self.election_year,
        )
        historical_elections = [
            self._build_election_content(
                record=record,
                election_year=historical_year,
            )
            for historical_year
            in HISTORICAL_ELECTION_YEARS
            if historical_year != self.election_year
        ]

        return {
            "section_id": section_id,
            "election_year": self.election_year,
            "coverage_scope": "TRACKED_PARTIES_ONLY",
            "tracked_parties": list(TRACKED_PARTIES),
            "quality_status": current_election[
                "quality_status"
            ],
            "contests": current_election["contests"],
            "historical_elections": historical_elections,
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
