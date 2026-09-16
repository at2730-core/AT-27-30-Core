from dataclasses import asdict, dataclass
from typing import Any

from heyti.audit.data_truth.contracts import (
    PUBLICATION_ALLOWED,
    PUBLICATION_BLOCKED,
    PUBLICATION_HISTORICAL_ONLY,
    TRUTH_OBSERVED,
    TRUTH_UNRESOLVED,
    TRUTH_UNVERIFIED,
)
from heyti.audit.data_truth.territorial_policy import (
    TerritorialClassification,
    TerritorialSectionPolicy,
)


CLASSIFICATION_CERTIFIED_PREDECESSOR = (
    "CERTIFIED_PREDECESSOR"
)
CLASSIFICATION_CERTIFIED_SUCCESSOR = (
    "CERTIFIED_SUCCESSOR"
)
CLASSIFICATION_UNRESOLVED_HISTORICAL = (
    "UNRESOLVED_HISTORICAL"
)
CLASSIFICATION_SYNTHETIC_CANDIDATE = (
    "SYNTHETIC_CANDIDATE"
)
CLASSIFICATION_UNCLASSIFIED_MASTER_ONLY = (
    "UNCLASSIFIED_MASTER_ONLY"
)
CLASSIFICATION_UNEXPECTED_GEOMETRY_ONLY = (
    "UNEXPECTED_GEOMETRY_ONLY"
)
CLASSIFICATION_REQUIRES_REPOSITORY_CONFIRMATION = (
    "REQUIRES_REPOSITORY_CONFIRMATION"
)


@dataclass(frozen=True)
class SectionTruthResolution:
    """
    Resolución contractual de verdad para una sección individual.

    No certifica información que la política o el repositorio
    territorial no hayan confirmado expresamente.
    """

    section_id: int
    classification: str
    truth_status: str
    publication_status: str
    policy_id: str
    policy_version: str
    evidence_reference: str | None = None
    related_sections: tuple[int, ...] = ()
    warning_code: str | None = None
    warning_message: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Devuelve una representación estructurada de la resolución."""

        return asdict(self)


def _normalize_section_id(
    section_id: int | str,
) -> int:
    if isinstance(section_id, bool):
        raise ValueError(
            "section_id debe ser un entero positivo"
        )

    if isinstance(section_id, int):
        normalized = section_id
    elif isinstance(section_id, str):
        candidate = section_id.strip()

        if not candidate.isdecimal():
            raise ValueError(
                "section_id debe ser un entero positivo"
            )

        normalized = int(candidate)
    else:
        raise ValueError(
            "section_id debe ser un entero positivo"
        )

    if normalized <= 0:
        raise ValueError(
            "section_id debe ser un entero positivo"
        )

    return normalized


def _build_resolution(
    section_id: int,
    classification: str,
    truth_status: str,
    publication_status: str,
    policy: TerritorialSectionPolicy,
    related_sections: tuple[int, ...] = (),
    warning_code: str | None = None,
    warning_message: str | None = None,
) -> SectionTruthResolution:
    return SectionTruthResolution(
        section_id=section_id,
        classification=classification,
        truth_status=truth_status,
        publication_status=publication_status,
        policy_id=policy.policy_id,
        policy_version=policy.version,
        evidence_reference=policy.evidence_reference,
        related_sections=related_sections,
        warning_code=warning_code,
        warning_message=warning_message,
    )


def resolve_section_truth(
    section_id: int | str,
    classification: TerritorialClassification,
    policy: TerritorialSectionPolicy,
) -> SectionTruthResolution:
    """
    Resuelve una sección contra una clasificación ya auditada.

    Una sección fuera de las excepciones no se certifica aquí:
    requiere confirmación posterior del repositorio territorial.
    """

    normalized = _normalize_section_id(section_id)

    if normalized in classification.certified_predecessors:
        return _build_resolution(
            section_id=normalized,
            classification=(
                CLASSIFICATION_CERTIFIED_PREDECESSOR
            ),
            truth_status=TRUTH_OBSERVED,
            publication_status=PUBLICATION_HISTORICAL_ONLY,
            policy=policy,
            related_sections=tuple(
                policy.certified_lineage[normalized]
            ),
            warning_code="HISTORICAL_PREDECESSOR_SECTION",
            warning_message=(
                "La sección es una predecesora histórica "
                "con linaje territorial certificado."
            ),
        )

    successor_to_predecessor = {
        successor: predecessor
        for predecessor, successors
        in policy.certified_lineage.items()
        for successor in successors
    }

    if normalized in classification.certified_successors:
        predecessor = successor_to_predecessor[normalized]

        return _build_resolution(
            section_id=normalized,
            classification=(
                CLASSIFICATION_CERTIFIED_SUCCESSOR
            ),
            truth_status=TRUTH_OBSERVED,
            publication_status=PUBLICATION_ALLOWED,
            policy=policy,
            related_sections=(predecessor,),
        )

    if normalized in classification.unresolved_historical:
        return _build_resolution(
            section_id=normalized,
            classification=(
                CLASSIFICATION_UNRESOLVED_HISTORICAL
            ),
            truth_status=TRUTH_UNRESOLVED,
            publication_status=PUBLICATION_BLOCKED,
            policy=policy,
            warning_code="UNRESOLVED_HISTORICAL_SECTION",
            warning_message=(
                "La identidad territorial histórica "
                "no está resuelta."
            ),
        )

    if normalized in classification.synthetic_candidates:
        return _build_resolution(
            section_id=normalized,
            classification=(
                CLASSIFICATION_SYNTHETIC_CANDIDATE
            ),
            truth_status=TRUTH_UNVERIFIED,
            publication_status=PUBLICATION_BLOCKED,
            policy=policy,
            warning_code="SYNTHETIC_SECTION_CANDIDATE",
            warning_message=(
                "La sección es una candidata sintética "
                "sin identidad territorial certificada."
            ),
        )

    if normalized in classification.unclassified_master_only:
        return _build_resolution(
            section_id=normalized,
            classification=(
                CLASSIFICATION_UNCLASSIFIED_MASTER_ONLY
            ),
            truth_status=TRUTH_UNRESOLVED,
            publication_status=PUBLICATION_BLOCKED,
            policy=policy,
            warning_code="UNCLASSIFIED_MASTER_SECTION",
            warning_message=(
                "La sección existe únicamente en el maestro "
                "y permanece sin clasificación territorial."
            ),
        )

    if normalized in classification.unexpected_geometry_only:
        return _build_resolution(
            section_id=normalized,
            classification=(
                CLASSIFICATION_UNEXPECTED_GEOMETRY_ONLY
            ),
            truth_status=TRUTH_UNRESOLVED,
            publication_status=PUBLICATION_BLOCKED,
            policy=policy,
            warning_code="UNEXPECTED_GEOMETRY_SECTION",
            warning_message=(
                "La sección existe únicamente en geometría "
                "y no está cubierta por la política."
            ),
        )

    return _build_resolution(
        section_id=normalized,
        classification=(
            CLASSIFICATION_REQUIRES_REPOSITORY_CONFIRMATION
        ),
        truth_status=TRUTH_UNVERIFIED,
        publication_status=PUBLICATION_BLOCKED,
        policy=policy,
        warning_code="SECTION_REQUIRES_REPOSITORY_CONFIRMATION",
        warning_message=(
            "La sección no pertenece a una excepción auditada; "
            "su vigencia debe confirmarse en el repositorio "
            "territorial."
        ),
    )
