from pathlib import Path

from heyti.audit.data_truth.contest_winner_summary import (
    summarize_contest_winners_without_party_votes,
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


def test_summary_aggregates_findings(tmp_path):
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

    summary = (
        summarize_contest_winners_without_party_votes(
            source
        )
    )

    assert summary.total_findings == 2
    assert summary.affected_sections == (
        "1",
        "2",
    )
    assert summary.winner_field_counts == {
        "GANADOR_24A": 2,
    }
    assert summary.total_positive == 1
    assert summary.total_zero == 1
    assert summary.total_unavailable == 0
    assert summary.ln_positive == 2


def test_summary_distinguishes_unavailable_values(tmp_path):
    source = write_source(
        tmp_path / "master.json",
        (
            '[{"SECCION": 3,'
            ' "24A_PAN": 0,'
            ' "24A_PRI": 0,'
            ' "24A_PVEM": 0,'
            ' "24A_MORENA": 0,'
            ' "24A_TOTAL": null,'
            ' "24A_LN": null,'
            ' "GANADOR_24A": "PAN"}]'
        ),
    )

    summary = (
        summarize_contest_winners_without_party_votes(
            source
        )
    )

    assert summary.total_unavailable == 1
    assert summary.ln_unavailable == 1


def test_clean_source_produces_empty_summary(tmp_path):
    source = write_source(
        tmp_path / "master.json",
        (
            '[{"SECCION": 4,'
            ' "24A_PAN": 10,'
            ' "GANADOR_24A": "PAN"}]'
        ),
    )

    summary = (
        summarize_contest_winners_without_party_votes(
            source
        )
    )

    assert summary.total_findings == 0
    assert summary.affected_sections == ()
    assert summary.winner_field_counts == {}


def test_summary_is_serializable(tmp_path):
    source = write_source(
        tmp_path / "master.json",
        (
            '[{"SECCION": 5,'
            ' "24A_PAN": 0,'
            ' "GANADOR_24A": "PAN"}]'
        ),
    )

    data = (
        summarize_contest_winners_without_party_votes(
            source
        ).to_dict()
    )

    assert data["total_findings"] == 1
    assert data["affected_sections"] == ("5",)


def test_summary_does_not_modify_source(tmp_path):
    original = (
        '[{"SECCION": 6,'
        ' "24A_PAN": 0,'
        ' "GANADOR_24A": "PAN"}]'
    )

    source = write_source(
        tmp_path / "master.json",
        original,
    )

    before = source.read_bytes()

    summarize_contest_winners_without_party_votes(
        source
    )

    assert source.read_bytes() == before
