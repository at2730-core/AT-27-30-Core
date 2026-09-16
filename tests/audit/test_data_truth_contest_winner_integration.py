from pathlib import Path

from heyti.audit.data_truth.electoral_master import (
    CONTEST_WINNERS_NOT_DERIVABLE,
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


def test_audit_emits_one_aggregate_contest_finding(tmp_path):
    source = write_source(
        tmp_path / "master.json",
        (
            '[{"SECCION": 1,'
            ' "24A_PAN": 0,'
            ' "24A_PRI": 0,'
            ' "24A_PVEM": 0,'
            ' "24A_MORENA": 0,'
            ' "24A_TOTAL": 10,'
            ' "24A_LN": 20,'
            ' "GANADOR_24A": "PAN"},'
            ' {"SECCION": 2,'
            ' "24A_PAN": 0,'
            ' "24A_PRI": 0,'
            ' "24A_PVEM": 0,'
            ' "24A_MORENA": 0,'
            ' "24A_TOTAL": 0,'
            ' "24A_LN": 30,'
            ' "GANADOR_24A": "PAN"}]'
        ),
    )

    result = audit_electoral_master(
        path=source,
        audit_id="AUDIT-CONTEST-001",
        source_id="contest-master",
    )

    aggregate = tuple(
        finding
        for finding in result.findings
        if finding.code
        == CONTEST_WINNERS_NOT_DERIVABLE
    )

    assert len(aggregate) == 1

    metadata = aggregate[0].metadata

    assert metadata["total_findings"] == 2
    assert metadata["affected_sections"] == (
        "1",
        "2",
    )
    assert metadata["total_positive"] == 1
    assert metadata["total_zero"] == 1
    assert (
        metadata["possible_origin_status"]
        == "UNVERIFIED_HYPOTHESIS"
    )


def test_clean_source_does_not_emit_aggregate_finding(
    tmp_path,
):
    source = write_source(
        tmp_path / "clean.json",
        (
            '[{"SECCION": 1,'
            ' "24A_PAN": 10,'
            ' "GANADOR_24A": "PAN"}]'
        ),
    )

    result = audit_electoral_master(
        path=source,
        audit_id="AUDIT-CONTEST-002",
        source_id="clean-master",
    )

    assert all(
        finding.code
        != CONTEST_WINNERS_NOT_DERIVABLE
        for finding in result.findings
    )

    assert (
        result.metadata["non_derivable_contest_winners"]
        == 0
    )
