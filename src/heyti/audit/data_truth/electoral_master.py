import json
from pathlib import Path

from heyti.audit.data_truth.contracts import (
    AUDIT_STATUS_BLOCKED,
    AUDIT_STATUS_PASSED,
    PUBLICATION_BLOCKED,
    SEVERITY_CRITICAL,
    TRUTH_UNRESOLVED,
    DataTruthAuditResult,
    DataTruthEvidence,
    DataTruthFinding,
)
from heyti.audit.data_truth.json_source import (
    audit_json_source,
)
from heyti.audit.data_truth.profiles import (
    profile_json_non_finite,
)
from heyti.audit.data_truth.contest_winner_summary import (
    summarize_contest_winners_without_party_votes,
)
from heyti.audit.data_truth.winner_evidence import (
    profile_winners_without_numeric_evidence,
)


NON_FINITE_NUMERIC_VALUES = "NON_FINITE_NUMERIC_VALUES"
CONTEST_WINNERS_NOT_DERIVABLE = (
    "CONTEST_WINNERS_NOT_DERIVABLE"
)
WINNER_WITHOUT_NUMERIC_EVIDENCE = (
    "WINNER_WITHOUT_NUMERIC_EVIDENCE"
)


def _build_source_evidence(
    path: Path,
    source_id: str,
    source_sha256: str,
) -> DataTruthEvidence:
    """Construye evidencia común para hallazgos semánticos."""

    return DataTruthEvidence(
        source_id=source_id,
        description="Fuente electoral auditada sin modificación",
        sha256=source_sha256,
        metadata={
            "path": str(path),
            "bytes": path.stat().st_size,
        },
    )


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

    source_evidence = _build_source_evidence(
        path=source_path,
        source_id=source_id,
        source_sha256=metadata["source_sha256"],
    )

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
                    evidence=(source_evidence,),
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

    try:
        winner_profile = (
            profile_winners_without_numeric_evidence(
                source_path
            )
        )
    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
        ValueError,
    ) as error:
        metadata["winner_evidence_profile_available"] = False
        metadata["winner_evidence_profile_error"] = str(error)
    else:
        metadata.update(
            {
                "winner_evidence_profile_available": True,
                "winner_without_numeric_evidence": len(
                    winner_profile
                ),
                "winner_without_numeric_sections": tuple(
                    item.section_code
                    for item in winner_profile
                ),
            }
        )

        for item in winner_profile:
            findings.append(
                DataTruthFinding(
                    code=WINNER_WITHOUT_NUMERIC_EVIDENCE,
                    message=(
                        "La sección contiene etiquetas de ganador "
                        "sin evidencia numérica finita distinta de cero"
                    ),
                    severity=SEVERITY_CRITICAL,
                    entity_type="SECTION",
                    entity_id=item.section_code,
                    truth_status=TRUTH_UNRESOLVED,
                    publication_status=PUBLICATION_BLOCKED,
                    evidence=(source_evidence,),
                    metadata={
                        "winner_fields": item.winner_fields,
                    },
                )
            )

    try:
        contest_summary = (
            summarize_contest_winners_without_party_votes(
                source_path
            )
        )
    except (
        UnicodeDecodeError,
        json.JSONDecodeError,
        ValueError,
    ) as error:
        metadata["contest_winner_summary_available"] = False
        metadata["contest_winner_summary_error"] = str(error)
    else:
        metadata.update(
            {
                "contest_winner_summary_available": True,
                "non_derivable_contest_winners": (
                    contest_summary.total_findings
                ),
                "contest_winner_affected_sections": len(
                    contest_summary.affected_sections
                ),
            }
        )

        if contest_summary.total_findings:
            findings.append(
                DataTruthFinding(
                    code=CONTEST_WINNERS_NOT_DERIVABLE,
                    message=(
                        "Existen ganadores almacenados que no "
                        "pueden derivarse de los votos partidistas "
                        "representados"
                    ),
                    severity=SEVERITY_CRITICAL,
                    entity_type="DATASET",
                    entity_id=source_id,
                    truth_status=TRUTH_UNRESOLVED,
                    publication_status=PUBLICATION_BLOCKED,
                    evidence=(source_evidence,),
                    metadata={
                        "total_findings": (
                            contest_summary.total_findings
                        ),
                        "affected_sections": (
                            contest_summary.affected_sections
                        ),
                        "winner_field_counts": (
                            contest_summary.winner_field_counts
                        ),
                        "total_positive": (
                            contest_summary.total_positive
                        ),
                        "total_zero": (
                            contest_summary.total_zero
                        ),
                        "total_unavailable": (
                            contest_summary.total_unavailable
                        ),
                        "ln_positive": (
                            contest_summary.ln_positive
                        ),
                        "ln_zero": (
                            contest_summary.ln_zero
                        ),
                        "ln_unavailable": (
                            contest_summary.ln_unavailable
                        ),
                        "possible_origin": (
                            "ARGMAX_ZERO_TIE_BREAK"
                        ),
                        "possible_origin_status": (
                            "UNVERIFIED_HYPOTHESIS"
                        ),
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
