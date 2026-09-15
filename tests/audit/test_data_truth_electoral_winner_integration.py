from pathlib import Path

from heyti.audit.data_truth.contracts import (
    AUDIT_STATUS_BLOCKED,
)
from heyti.audit.data_truth.electoral_master import (
    WINNER_WITHOUT_NUMERIC_EVIDENCE,
    audit_electoral_master,
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


def test_integrated_audit_blocks_unsupported_winner(tmp_path):
    source = write_source(
        tmp_path / "winner.json",
        (
            '[{"SECCION": 3486,'
            ' "24A_PAN": null,'
            ' "GANADOR_24A": "PAN"}]'
        ),
    )

    result = audit_electoral_master(
        path=source,
        audit_id="AUDIT-WINNER-001",
        source_id="winner-master",
    )

    assert result.status == AUDIT_STATUS_BLOCKED
    assert len(result.findings) == 1

    finding = result.findings[0]

    assert (
        finding.code
        == WINNER_WITHOUT_NUMERIC_EVIDENCE
    )
    assert finding.entity_type == "SECTION"
    assert finding.entity_id == "3486"
    assert finding.metadata["winner_fields"] == (
        "GANADOR_24A",
    )
    assert len(finding.evidence) == 1
    assert len(finding.evidence[0].sha256) == 64


def test_integrated_audit_emits_one_finding_per_section(
    tmp_path,
):
    source = write_source(
        tmp_path / "winners.json",
        (
            '[{"SECCION": 3486, "GANADOR_24A": "PAN"},'
            ' {"SECCION": 4986, "GANADOR_24A": "PAN"}]'
        ),
    )

    result = audit_electoral_master(
        path=source,
        audit_id="AUDIT-WINNER-002",
        source_id="winner-master",
    )

    winner_findings = tuple(
        finding
        for finding in result.findings
        if finding.code
        == WINNER_WITHOUT_NUMERIC_EVIDENCE
    )

    assert tuple(
        finding.entity_id
        for finding in winner_findings
    ) == (
        "3486",
        "4986",
    )

    assert len(result.blocking_findings) == 2


def test_integrated_audit_exposes_winner_profile_metadata(
    tmp_path,
):
    source = write_source(
        tmp_path / "metadata.json",
        (
            '[{"SECCION": 5885,'
            ' "GANADOR_24DF": "PAN",'
            ' "GANADOR_PROY_2027_DF": "MORENA"}]'
        ),
    )

    result = audit_electoral_master(
        path=source,
        audit_id="AUDIT-WINNER-003",
        source_id="winner-master",
    )

    assert (
        result.metadata["winner_evidence_profile_available"]
        is True
    )
    assert (
        result.metadata["winner_without_numeric_evidence"]
        == 1
    )
    assert (
        result.metadata["winner_without_numeric_sections"]
        == ("5885",)
    )


def test_supported_winner_does_not_create_finding(tmp_path):
    source = write_source(
        tmp_path / "supported.json",
        (
            '[{"SECCION": 1,'
            ' "24A_PAN": 10,'
            ' "GANADOR_24A": "PAN"}]'
        ),
    )

    result = audit_electoral_master(
        path=source,
        audit_id="AUDIT-WINNER-004",
        source_id="winner-master",
    )

    assert result.findings == ()
    assert (
        result.metadata["winner_without_numeric_evidence"]
        == 0
    )
