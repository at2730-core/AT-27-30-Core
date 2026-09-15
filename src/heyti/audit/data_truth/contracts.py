from dataclasses import asdict, dataclass, field
from typing import Any


DATA_TRUTH_CONTRACT = "HEYTI_DATA_TRUTH_AUDIT"
DATA_TRUTH_CONTRACT_VERSION = "1.0"

AUDIT_STATUS_PASSED = "PASSED"
AUDIT_STATUS_PASSED_WITH_FINDINGS = "PASSED_WITH_FINDINGS"
AUDIT_STATUS_BLOCKED = "BLOCKED"

SEVERITY_INFO = "INFO"
SEVERITY_WARNING = "WARNING"
SEVERITY_ERROR = "ERROR"
SEVERITY_CRITICAL = "CRITICAL"

PUBLICATION_ALLOWED = "ALLOWED"
PUBLICATION_HISTORICAL_ONLY = "HISTORICAL_ONLY"
PUBLICATION_BLOCKED = "BLOCKED"

TRUTH_OBSERVED = "OBSERVED_DATA"
TRUTH_DERIVED = "DERIVED_DATA"
TRUTH_UNVERIFIED = "UNVERIFIED"
TRUTH_UNRESOLVED = "UNRESOLVED"

SUPPORTED_AUDIT_STATUSES = {
    AUDIT_STATUS_PASSED,
    AUDIT_STATUS_PASSED_WITH_FINDINGS,
    AUDIT_STATUS_BLOCKED,
}

SUPPORTED_SEVERITIES = {
    SEVERITY_INFO,
    SEVERITY_WARNING,
    SEVERITY_ERROR,
    SEVERITY_CRITICAL,
}

SUPPORTED_PUBLICATION_STATUSES = {
    PUBLICATION_ALLOWED,
    PUBLICATION_HISTORICAL_ONLY,
    PUBLICATION_BLOCKED,
}

SUPPORTED_TRUTH_STATUSES = {
    TRUTH_OBSERVED,
    TRUTH_DERIVED,
    TRUTH_UNVERIFIED,
    TRUTH_UNRESOLVED,
}


@dataclass(frozen=True)
class DataTruthEvidence:
    """
    Evidencia verificable asociada a un hallazgo de Data Truth.

    Conserva identidad, descripción y huella sin modificar la fuente.
    """

    source_id: str
    description: str
    sha256: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Devuelve una representación estructurada de la evidencia."""

        return asdict(self)


@dataclass(frozen=True)
class DataTruthFinding:
    """
    Hallazgo producido por una auditoría de veracidad.

    Un hallazgo informa; no corrige ni fabrica datos.
    """

    code: str
    message: str
    severity: str
    entity_type: str
    entity_id: str | None = None
    truth_status: str = TRUTH_UNRESOLVED
    publication_status: str = PUBLICATION_BLOCKED
    evidence: tuple[DataTruthEvidence, ...] = field(
        default_factory=tuple,
    )
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Devuelve una representación estructurada del hallazgo."""

        return asdict(self)


@dataclass(frozen=True)
class DataTruthAuditResult:
    """
    Resultado inmutable de una ejecución de auditoría.

    Separa el diagnóstico de cualquier proceso de remediación.
    """

    audit_id: str
    status: str
    findings: tuple[DataTruthFinding, ...] = field(
        default_factory=tuple,
    )
    contract: str = DATA_TRUTH_CONTRACT
    version: str = DATA_TRUTH_CONTRACT_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def blocking_findings(self) -> tuple[DataTruthFinding, ...]:
        """Devuelve exclusivamente hallazgos que bloquean publicación."""

        return tuple(
            finding
            for finding in self.findings
            if finding.publication_status == PUBLICATION_BLOCKED
        )

    def to_dict(self) -> dict[str, Any]:
        """Devuelve una representación estructurada del resultado."""

        return asdict(self)
