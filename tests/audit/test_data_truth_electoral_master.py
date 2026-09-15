from pathlib import Path

from heyti.audit.data_truth.contracts import (
    AUDIT_STATUS_BLOCKED,
    AUDIT_STATUS_PASSED,
)
from heyti.audit.data_truth.electoral_master import (
    NON_FINITE_NUMERIC_VALUES,
    audit_electoral_master,
)
from heyti.audit.data_truth.json_source import (
    STRICT_JSON_FAILURE,
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


def test_clean_electoral_master_passes(tmp_path):
    source = write_source(
        tmp_path / "clean.json",
        (
            '[{"SECCION": 1,'
            ' "24A_PAN": 10,'
            ' "24A_MORENA": 20}]'
        ),
    )

    result = audit_electoral_master(
        path=source,
        audit_id="AUDIT-MASTER-001",
        source_id="clean-master",
    )

    assert result.status == AUDIT_STATUS_PASSED
    assert result.findings == ()
    assert result.metadata["strict_json"] is True
    assert result.metadata["non_finite_values"] == 0


def test_non_finite_master_produces_two_findings(tmp_path):
    source = write_source(
        tmp_path / "nan.json",
        (
            '[{"SECCION": 1, "VOTOS": NaN},'
            ' {"SECCION": 2, "VOTOS": NaN, "LN": NaN}]'
        ),
    )

    result = audit_electoral_master(
        path=source,
        audit_id="AUDIT-MASTER-002",
        source_id="nan-master",
    )

    codes = tuple(
        finding.code
        for finding in result.findings
    )

    assert result.status == AUDIT_STATUS_BLOCKED
    assert codes == (
        STRICT_JSON_FAILURE,
        NON_FINITE_NUMERIC_VALUES,
    )
    assert len(result.blocking_findings) == 2


def test_non_finite_finding_contains_computed_profile(tmp_path):
    source = write_source(
        tmp_path / "profile.json",
        (
            '[{"SECCION": 1, "VOTOS": NaN},'
            ' {"SECCION": 2, "VOTOS": NaN, "LN": NaN}]'
        ),
    )

    result = audit_electoral_master(
        path=source,
        audit_id="AUDIT-MASTER-003",
        source_id="profile-master",
    )

    finding = result.findings[1]

    assert finding.code == NON_FINITE_NUMERIC_VALUES
    assert finding.metadata["total_values"] == 3
    assert finding.metadata["affected_records"] == 2
    assert finding.metadata["affected_fields"] == 2
    assert finding.metadata["field_counts"] == {
        "LN": 1,
        "VOTOS": 2,
    }


def test_malformed_json_reports_unavailable_profile(tmp_path):
    source = write_source(
        tmp_path / "malformed.json",
        '{"SECCION": 1',
    )

    result = audit_electoral_master(
        path=source,
        audit_id="AUDIT-MASTER-004",
        source_id="malformed-master",
    )

    assert result.status == AUDIT_STATUS_BLOCKED
    assert len(result.findings) == 1
    assert result.findings[0].code == STRICT_JSON_FAILURE
    assert (
        result.metadata["non_finite_profile_available"]
        is False
    )


def test_integrated_audit_preserves_source(tmp_path):
    original = '[{"SECCION": 1, "VOTOS": NaN}]'

    source = write_source(
        tmp_path / "preserved.json",
        original,
    )

    before = source.read_bytes()

    audit_electoral_master(
        path=source,
        audit_id="AUDIT-MASTER-005",
        source_id="preserved-master",
    )

    after = source.read_bytes()

    assert before == after
