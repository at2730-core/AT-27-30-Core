"""Explicit release inspection and selection boundary; no DB or UI wiring.

Release identifiers below are deterministic audit keys, not PostgreSQL IDs.
Repository implementations must return the literal SEC/CAS contract snapshot.
This component preserves values; it never calculates winners or certifies data.
"""

from copy import deepcopy
import csv
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Any, Iterable, Protocol


@dataclass(frozen=True)
class SeriesKey:
    year: int
    election_type: str
    modality: str

    def __post_init__(self) -> None:
        if type(self.year) is not int or self.year not in (2018, 2021, 2024):
            raise ValueError("Only 2018, 2021 and 2024 are admitted")
        modalities = {
            "A": ("UNICA",), "G": ("UNICA",), "P": ("UNICA",),
            "DF": ("MR", "RP"), "DL": ("MR", "RP"), "S": ("MR", "RP"),
        }
        if self.modality not in modalities.get(self.election_type, ()):
            raise ValueError("Explicit election type and modality required")


@dataclass(frozen=True)
class Release:
    release_id: str
    series: SeriesKey
    authority: str
    source_zip: str
    zip_sha256: str
    section_member: str
    section_sha256: str
    casilla_member: str
    casilla_sha256: str
    cut_label: str
    cut_date_status: str
    technical_status: str
    selection_status: str
    certification_status: str
    known_issues: str
    cut_date: str | None = None

    def __post_init__(self) -> None:
        if self.cut_date_status == "VERIFIED":
            if self.cut_date is None:
                raise ValueError("Verified cut requires a documented date")
            date.fromisoformat(self.cut_date)

    def provenance(self) -> dict[str, Any]:
        return {
            "release_id": self.release_id, "authority": self.authority,
            "source_zip": self.source_zip, "zip_sha256": self.zip_sha256,
            "section_member": self.section_member,
            "section_sha256": self.section_sha256,
            "casilla_member": self.casilla_member,
            "casilla_sha256": self.casilla_sha256,
            "cut_label": self.cut_label, "cut_date": self.cut_date,
            "cut_date_status": self.cut_date_status,
        }


class ReleaseRegistry:
    """Immutable-by-interface catalog; refuses duplicate audit release keys."""

    def __init__(self, releases: Iterable[Release]) -> None:
        self._releases: dict[str, Release] = {}
        for release in releases:
            if release.release_id in self._releases:
                raise ValueError("Duplicate release identity")
            self._releases[release.release_id] = release

    @classmethod
    def from_matrix(cls, path: Path) -> "ReleaseRegistry":
        releases = []
        with path.open(encoding="utf-8-sig", newline="") as stream:
            for row in csv.DictReader(stream):
                series = SeriesKey(int(row["year"]), row["type"], row["modality"])
                for column in ("zip_sha256", "section_sha256", "casilla_sha256"):
                    value = row[column]
                    if len(value) != 64 or any(c not in "0123456789abcdef" for c in value):
                        raise ValueError("Invalid source hash")
                # Same ZIP can contain several series; SEC hash disambiguates members.
                key = (f"{series.year}:{series.election_type}:{series.modality}:"
                       f"{row['zip_sha256']}:{row['section_sha256']}")
                releases.append(Release(
                    key, series, row["authority"], row["source_zip"],
                    row["zip_sha256"], row["section_csv"], row["section_sha256"],
                    row["casilla_csv"], row["casilla_sha256"], row["cut_label"],
                    row["cut_date_status"], row["technical_staging_status"],
                    row["presentation_selection"], row["certification_status"],
                    row["known_issues"],
                ))
        return cls(releases)

    @property
    def releases(self) -> tuple[Release, ...]:
        return tuple(self._releases.values())

    def get(self, release_id: str) -> Release | None:
        return self._releases.get(release_id)


@dataclass(frozen=True)
class ReadRequest:
    series: SeriesKey
    unit_kind: str
    unit_key: str
    purpose: str = "PRESENTATION"
    release_id: str | None = None
    policy_id: str | None = None
    metric_scope: str = "RESULT"

    def __post_init__(self) -> None:
        if self.purpose not in ("AUDIT", "PRESENTATION"):
            raise ValueError("Unknown read purpose")
        if not self.unit_kind.strip() or not self.unit_key.strip():
            raise ValueError("Historical unit identity required")
        if self.metric_scope not in ("RESULT", "NOMINAL_LIST"):
            raise ValueError("Unsupported metric scope")


@dataclass(frozen=True)
class SelectionDecision:
    policy_id: str
    series: SeriesKey
    unit_kind: str
    unit_key: str
    metric_scope: str
    release_id: str
    status: str
    certification_status: str
    evidence_refs: tuple[str, ...]


class ElectoralSnapshotRepository(Protocol):
    def get_snapshot(self, release_id: str, request: ReadRequest) -> dict[str, Any] | None:
        """Read literal identity, provenance, result, cas_evidence, issues, coverage."""
        ...


class VersionedElectoralSource:
    def __init__(self, registry: ReleaseRegistry,
                 repository: ElectoralSnapshotRepository,
                 decisions: Iterable[SelectionDecision] = ()) -> None:
        self.registry = registry
        self.repository = repository
        self._decisions = tuple(decisions)

    def read(self, request: ReadRequest) -> dict[str, Any]:
        response: dict[str, Any] = {
            "status": "NO_RELEASE_SELECTED", "purpose": request.purpose,
            "metric_scope": request.metric_scope, "data": None,
            "provenance": None, "policy_id": request.policy_id,
            "selection_status": "UNDECIDED",
            "certification_status": "PENDING_SOURCE_ADJUDICATION",
            "issues": [], "winner": None, "margin": None,
            "winner_reason": "CANDIDACY_MAPPING_NOT_IMPLEMENTED",
        }
        decision = None
        release_id = request.release_id
        if request.purpose == "PRESENTATION":
            if not request.policy_id:
                return response
            matches = [d for d in self._decisions if (
                d.policy_id == request.policy_id and d.series == request.series
                and d.unit_kind == request.unit_kind and d.unit_key == request.unit_key
                and d.metric_scope == request.metric_scope
            )]
            if len(matches) != 1:
                return response
            decision = matches[0]
            if (decision.status != "SELECTED" or not decision.evidence_refs
                    or not all(isinstance(ref, str) and ref.strip()
                               for ref in decision.evidence_refs)
                    or decision.certification_status != "CERTIFIED"):
                return response
            if release_id is not None and release_id != decision.release_id:
                response["status"] = "SELECTION_RELEASE_MISMATCH"
                return response
            release_id = decision.release_id
        if not release_id:
            return response
        release = self.registry.get(release_id)
        if release is None or release.series != request.series:
            response["status"] = "RELEASE_IDENTITY_MISMATCH"
            return response
        response.update(
            provenance=release.provenance(),
            certification_status=release.certification_status,
            selection_status=release.selection_status,
            issues=[release.known_issues] if release.known_issues else [],
        )
        if request.purpose == "PRESENTATION":
            # Current matrix is unresolved. No technical-success bypass or local
            # override of a series-wide conflict is implemented in this block.
            if release.certification_status.startswith("BLOCKED"):
                response["status"] = release.certification_status
                return response
            if release.cut_date_status != "VERIFIED":
                response["status"] = "UNVERIFIED_CUT"
                return response
        snapshot = self.repository.get_snapshot(release_id, request)
        if snapshot is None:
            response["status"] = "UNIT_NOT_AVAILABLE"
            return response
        if not isinstance(snapshot, dict):
            response["status"] = "INCOMPLETE_SNAPSHOT_CONTRACT"
            return response
        identity = snapshot.get("identity", {})
        required_identity = {
            "year": request.series.year, "type": request.series.election_type,
            "modality": request.series.modality, "unit_kind": request.unit_kind,
            "unit_key": request.unit_key,
        }
        provenance = snapshot.get("provenance", {})
        if not isinstance(identity, dict) or not isinstance(provenance, dict):
            response["status"] = "INCOMPLETE_SNAPSHOT_CONTRACT"
            return response
        if (any(identity.get(k) != v for k, v in required_identity.items())
                or any(provenance.get(k) != v for k, v in release.provenance().items())):
            response["status"] = "SNAPSHOT_IDENTITY_MISMATCH"
            return response
        if not all(k in snapshot for k in ("result", "cas_evidence", "issues", "coverage")):
            response["status"] = "INCOMPLETE_SNAPSHOT_CONTRACT"
            return response
        if (not isinstance(snapshot["cas_evidence"], list)
                or not isinstance(snapshot["issues"], list)
                or not isinstance(snapshot["coverage"], dict)):
            response["status"] = "INCOMPLETE_SNAPSHOT_CONTRACT"
            return response
        result = snapshot["result"]
        if not isinstance(result, dict) or not all(k in result for k in (
            "total_votes", "total_raw", "total_status", "total_missing_cause",
            "nominal_list", "nominal_raw", "nominal_status", "nominal_missing_cause",
            "options",
        )):
            response["status"] = "INCOMPLETE_SNAPSHOT_CONTRACT"
            return response
        if not self._valid_result(result):
            response["status"] = "INVALID_LITERAL_RESULT"
            return response
        if request.purpose == "PRESENTATION":
            if snapshot["issues"]:
                response.update(status="OPEN_UNIT_ISSUES", issues=deepcopy(snapshot["issues"]))
                return response
            # Partial-metric authorization must never reveal uncertified votes.
            if request.metric_scope == "NOMINAL_LIST":
                response["data"] = {
                    "identity": deepcopy(identity),
                    "result": {k: deepcopy(result[k]) for k in (
                        "nominal_list", "nominal_raw", "nominal_status", "nominal_missing_cause",
                    )},
                    "coverage": deepcopy(snapshot["coverage"]),
                }
            else:
                response["data"] = deepcopy(snapshot)
            response.update(status="SELECTED_RESULT", selection_status=decision.status,
                            certification_status=decision.certification_status,
                            selection_evidence=list(decision.evidence_refs))
        else:
            response.update(status="AUDIT_SOURCE_AS_PUBLISHED", data=deepcopy(snapshot))
        return response

    @staticmethod
    def _valid_result(result: dict[str, Any]) -> bool:
        def valid_cell(value: Any, raw: Any, cause: Any) -> bool:
            return (isinstance(raw, str) and (
                (value is None and isinstance(cause, str) and bool(cause.strip()))
                or (type(value) is int and value >= 0)
            ))

        for value, raw, cause in (
            ("total_votes", "total_raw", "total_missing_cause"),
            ("nominal_list", "nominal_raw", "nominal_missing_cause"),
        ):
            if not valid_cell(result[value], result[raw], result[cause]):
                return False
        options = result["options"]
        if not isinstance(options, list):
            return False
        columns, ordinals = set(), set()
        for option in options:
            if not isinstance(option, dict) or not all(k in option for k in (
                "raw_column", "ordinal", "option_kind", "votes", "raw_value", "missing_cause",
            )):
                return False
            column, ordinal = option["raw_column"], option["ordinal"]
            if (not isinstance(column, str) or not column
                    or type(ordinal) is not int or ordinal < 0
                    or column in columns or ordinal in ordinals
                    or not valid_cell(option["votes"], option["raw_value"], option["missing_cause"])):
                return False
            columns.add(column)
            ordinals.add(ordinal)
        return True
