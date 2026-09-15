import hashlib
import json
from pathlib import Path
from typing import Any

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


STRICT_JSON_FAILURE = "STRICT_JSON_FAILURE"


def _reject_non_standard_constant(value: str) -> None:
    """
    Rechaza constantes no permitidas por JSON estricto.

    Python acepta NaN e Infinity por compatibilidad, aunque no pertenecen
    al estándar JSON.
    """

    raise ValueError(
        f"Constante JSON no válida: {value}"
    )


def _sha256(content: bytes) -> str:
    """Calcula la huella SHA-256 del contenido original."""

    return hashlib.sha256(content).hexdigest().upper()


def audit_json_source(
    path: str | Path,
    audit_id: str,
    source_id: str,
) -> DataTruthAuditResult:
    """
    Audita una fuente JSON sin modificarla.

    Conserva la huella del archivo y bloquea la publicación cuando el
    documento no puede interpretarse como JSON estricto.
    """

    source_path = Path(path)
    content = source_path.read_bytes()
    source_hash = _sha256(content)

    evidence = DataTruthEvidence(
        source_id=source_id,
        description="Fuente JSON auditada sin modificación",
        sha256=source_hash,
        metadata={
            "path": str(source_path),
            "bytes": len(content),
        },
    )

    try:
        text = content.decode("utf-8-sig")

        parsed: Any = json.loads(
            text,
            parse_constant=_reject_non_standard_constant,
        )
    except (UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
        finding = DataTruthFinding(
            code=STRICT_JSON_FAILURE,
            message="La fuente no cumple el formato JSON estricto",
            severity=SEVERITY_CRITICAL,
            entity_type="DATASET",
            entity_id=source_id,
            truth_status=TRUTH_UNRESOLVED,
            publication_status=PUBLICATION_BLOCKED,
            evidence=(evidence,),
            metadata={
                "error_type": type(error).__name__,
                "error": str(error),
            },
        )

        return DataTruthAuditResult(
            audit_id=audit_id,
            status=AUDIT_STATUS_BLOCKED,
            findings=(finding,),
            metadata={
                "source_id": source_id,
                "source_sha256": source_hash,
                "strict_json": False,
            },
        )

    record_count = (
        len(parsed)
        if isinstance(parsed, (list, dict))
        else None
    )

    return DataTruthAuditResult(
        audit_id=audit_id,
        status=AUDIT_STATUS_PASSED,
        metadata={
            "source_id": source_id,
            "source_sha256": source_hash,
            "strict_json": True,
            "record_count": record_count,
        },
    )
