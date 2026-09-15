import json
from pathlib import Path

from heyti.audit.data_truth.contracts import (
    AUDIT_STATUS_BLOCKED,
    AUDIT_STATUS_PASSED,
    PUBLICATION_BLOCKED,
    SEVERITY_CRITICAL,
    TRUTH_UNRESOLVED,
    DataTruthAuditResult,
    DataTruthFinding,
)
from heyti.audit.data_truth.json_source import (
    audit_json_source,
)
from heyti.audit.data_truth.profiles import (
    profile_json_non_finite,
)


NON_FINITE_NUMERIC_VALUES = "NON_FINITE_NUMERIC_VALUES"


def audit_electoral_master(
    path: str | Path,
    audit_id: str,
    source_id: str,
) -> DataTruthAuditResult:
    """
    Ejecuta la auditoría técnica y semántica de un maestro electoral.

    La fuente se lee exclusivamente para diagnóstico. No se corrige,
    completa ni reescribe.
    """

    source_path = Path(path)

    strict_result = audit_json_source(
        path=source_path,
        audit_id=audit_id,
        source_id=source_id,
    )

    findings = list(strict_result.findings)
    metadata = dict(strict_result.metadata)

    try:
        profile = profile_json_non_finite(
            source_path
        )
    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
        ValueError,
    ) as error:
        metadata["non_finite_profile_available"] = False
        metadata["non_finite_profile_error"] = str(error)
    else:
        metadata.update(
            {
                "non_finite_profile_available": True,
                "non_finite_values": profile.total_values,
                "non_finite_records": profile.affected_records,
                "non_finite_fields": profile.affected_fields,
                "non_finite_field_counts": profile.field_counts,
            }
        )

        if profile.total_values:
            findings.append(
                DataTruthFinding(
                    code=NON_FINITE_NUMERIC_VALUES,
                    message=(
                        "La fuente contiene valores numéricos "
                        "no finitos"
                    ),
                    severity=SEVERITY_CRITICAL,
                    entity_type="DATASET",
                    entity_id=source_id,
                    truth_status=TRUTH_UNRESOLVED,
                    publication_status=PUBLICATION_BLOCKED,
                    evidence=(
                        strict_result.findings[0].evidence
                        if strict_result.findings
                        else ()
                    ),
                    metadata={
                        "total_values": profile.total_values,
                        "affected_records": (
                            profile.affected_records
                        ),
                        "affected_fields": (
                            profile.affected_fields
                        ),
                        "field_counts": profile.field_counts,
                    },
                )
            )

    status = (
        AUDIT_STATUS_BLOCKED
        if any(
            finding.publication_status
            == PUBLICATION_BLOCKED
            for finding in findings
        )
        else AUDIT_STATUS_PASSED
    )

    return DataTruthAuditResult(
        audit_id=audit_id,
        status=status,
        findings=tuple(findings),
        metadata=metadata,
    )
