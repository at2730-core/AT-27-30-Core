from pathlib import Path

from heyti.audit.data_truth.contracts import (
    AUDIT_STATUS_BLOCKED,
    AUDIT_STATUS_PASSED,
    PUBLICATION_BLOCKED,
)
from heyti.audit.data_truth.json_source import (
    STRICT_JSON_FAILURE,
    audit_json_source,
)


def write_source(
    path: Path,
    content: str,
) -> Path:
    path.write_text(
        content,
        encoding="utf-8",
    )
    return path


def test_valid_json_passes_without_findings(tmp_path):
    source = write_source(
        tmp_path / "valid.json",
        '[{"SECCION": 1, "VOTOS": null}]',
    )

    result = audit_json_source(
        path=source,
        audit_id="AUDIT-JSON-001",
        source_id="valid-source",
    )

    assert result.status == AUDIT_STATUS_PASSED
    assert result.findings == ()
    assert result.metadata["strict_json"] is True
    assert result.metadata["record_count"] == 1


def test_nan_blocks_strict_json_source(tmp_path):
    source = write_source(
        tmp_path / "nan.json",
        '[{"SECCION": 1, "VOTOS": NaN}]',
    )

    result = audit_json_source(
        path=source,
        audit_id="AUDIT-JSON-002",
        source_id="nan-source",
    )

    assert result.status == AUDIT_STATUS_BLOCKED
    assert len(result.findings) == 1

    finding = result.findings[0]

    assert finding.code == STRICT_JSON_FAILURE
    assert finding.publication_status == PUBLICATION_BLOCKED
    assert "NaN" in finding.metadata["error"]


def test_infinity_blocks_strict_json_source(tmp_path):
    source = write_source(
        tmp_path / "infinity.json",
        '{"value": Infinity}',
    )

    result = audit_json_source(
        path=source,
        audit_id="AUDIT-JSON-003",
        source_id="infinity-source",
    )

    assert result.status == AUDIT_STATUS_BLOCKED
    assert result.findings[0].code == STRICT_JSON_FAILURE


def test_malformed_json_is_blocked(tmp_path):
    source = write_source(
        tmp_path / "malformed.json",
        '{"SECCION": 1',
    )

    result = audit_json_source(
        path=source,
        audit_id="AUDIT-JSON-004",
        source_id="malformed-source",
    )

    assert result.status == AUDIT_STATUS_BLOCKED
    assert (
        result.findings[0].metadata["error_type"]
        == "JSONDecodeError"
    )


def test_audit_preserves_source_content(tmp_path):
    original = '[{"SECCION": 1, "VOTOS": NaN}]'

    source = write_source(
        tmp_path / "preserved.json",
        original,
    )

    audit_json_source(
        path=source,
        audit_id="AUDIT-JSON-005",
        source_id="preserved-source",
    )

    assert source.read_text(
        encoding="utf-8"
    ) == original


def test_audit_records_sha256_evidence(tmp_path):
    source = write_source(
        tmp_path / "evidence.json",
        '{"SECCION": 2788}',
    )

    result = audit_json_source(
        path=source,
        audit_id="AUDIT-JSON-006",
        source_id="evidence-source",
    )

    source_hash = result.metadata["source_sha256"]

    assert len(source_hash) == 64
    assert source_hash.isupper() is True
