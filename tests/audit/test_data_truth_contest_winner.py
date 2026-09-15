import json
from pathlib import Path

import pytest

from heyti.audit.data_truth.contest_winner import (
    profile_contest_winners_without_party_votes,
)


def write_json(
    path: Path,
    value,
) -> Path:
    path.write_text(
        json.dumps(
            value,
            allow_nan=True,
        ),
        encoding="utf-8",
    )
    return path


def test_reports_winner_without_party_votes(tmp_path):
    source = write_json(
        tmp_path / "master.json",
        [
            {
                "SECCION": 9012,
                "24DL_TOTAL": 1,
                "24DL_LN": 3,
                "GANADOR_24DL": "PAN",
            },
        ],
    )

    findings = (
        profile_contest_winners_without_party_votes(
            source
        )
    )

    assert len(findings) == 1
    assert findings[0].section_code == "9012"
    assert findings[0].winner_field == "GANADOR_24DL"
    assert findings[0].stored_winner == "PAN"
    assert findings[0].party_fields == (
        "24DL_PAN",
        "24DL_PRI",
        "24DL_PVEM",
        "24DL_MORENA",
    )


def test_projection_uses_its_own_party_fields(tmp_path):
    source = write_json(
        tmp_path / "master.json",
        [
            {
                "SECCION": 9013,
                "24DL_PAN": 10,
                "GANADOR_24DL": "PAN",
                "GANADOR_PROY_2027_DL": "MORENA",
            },
        ],
    )

    findings = (
        profile_contest_winners_without_party_votes(
            source
        )
    )

    assert len(findings) == 1
    assert (
        findings[0].winner_field
        == "GANADOR_PROY_2027_DL"
    )


def test_supported_winner_is_not_reported(tmp_path):
    source = write_json(
        tmp_path / "master.json",
        [
            {
                "SECCION": 1,
                "24A_MORENA": 20,
                "GANADOR_24A": "MORENA",
            },
        ],
    )

    findings = (
        profile_contest_winners_without_party_votes(
            source
        )
    )

    assert findings == ()


def test_zero_nan_and_null_are_not_party_votes(tmp_path):
    source = write_json(
        tmp_path / "master.json",
        [
            {
                "SECCION": 2,
                "24A_PAN": 0,
                "24A_PRI": None,
                "24A_PVEM": float("nan"),
                "24A_MORENA": 0,
                "GANADOR_24A": "PAN",
            },
        ],
    )

    findings = (
        profile_contest_winners_without_party_votes(
            source
        )
    )

    assert len(findings) == 1


def test_total_and_ln_do_not_support_winner(tmp_path):
    source = write_json(
        tmp_path / "master.json",
        [
            {
                "SECCION": 3,
                "24A_TOTAL": 50,
                "24A_LN": 100,
                "GANADOR_24A": "PAN",
            },
        ],
    )

    findings = (
        profile_contest_winners_without_party_votes(
            source
        )
    )

    assert len(findings) == 1


def test_emits_one_result_per_unsupported_contest(tmp_path):
    source = write_json(
        tmp_path / "master.json",
        [
            {
                "SECCION": 4,
                "GANADOR_24A": "PAN",
                "GANADOR_PROY_2027_A": "MORENA",
            },
        ],
    )

    findings = (
        profile_contest_winners_without_party_votes(
            source
        )
    )

    assert tuple(
        finding.winner_field
        for finding in findings
    ) == (
        "GANADOR_24A",
        "GANADOR_PROY_2027_A",
    )


def test_rejects_non_list_master(tmp_path):
    source = write_json(
        tmp_path / "master.json",
        {
            "SECCION": 1,
        },
    )

    with pytest.raises(
        ValueError,
        match="lista de registros",
    ):
        profile_contest_winners_without_party_votes(
            source
        )


def test_profile_does_not_modify_source(tmp_path):
    source = write_json(
        tmp_path / "master.json",
        [
            {
                "SECCION": 5,
                "GANADOR_24A": "PAN",
            },
        ],
    )

    before = source.read_bytes()

    profile_contest_winners_without_party_votes(
        source
    )

    assert source.read_bytes() == before
