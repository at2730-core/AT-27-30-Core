import json
from pathlib import Path

import pytest

from heyti.audit.data_truth.winner_evidence import (
    profile_winners_without_numeric_evidence,
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


def test_reports_winner_without_numeric_evidence(tmp_path):
    source = write_json(
        tmp_path / "master.json",
        [
            {
                "SECCION": 3486,
                "24A_PAN": None,
                "24A_MORENA": float("nan"),
                "GANADOR_24A": "PAN",
            },
        ],
    )

    findings = (
        profile_winners_without_numeric_evidence(
            source
        )
    )

    assert len(findings) == 1
    assert findings[0].section_code == "3486"
    assert findings[0].winner_fields == (
        "GANADOR_24A",
    )


def test_does_not_report_supported_winner(tmp_path):
    source = write_json(
        tmp_path / "master.json",
        [
            {
                "SECCION": 1,
                "24A_PAN": 10,
                "24A_MORENA": 20,
                "GANADOR_24A": "MORENA",
            },
        ],
    )

    findings = (
        profile_winners_without_numeric_evidence(
            source
        )
    )

    assert findings == ()


def test_zero_is_not_numeric_winner_evidence(tmp_path):
    source = write_json(
        tmp_path / "master.json",
        [
            {
                "SECCION": 2,
                "24A_PAN": 0,
                "24A_MORENA": 0,
                "GANADOR_24A": "PAN",
            },
        ],
    )

    findings = (
        profile_winners_without_numeric_evidence(
            source
        )
    )

    assert len(findings) == 1


def test_ignores_records_without_winner(tmp_path):
    source = write_json(
        tmp_path / "master.json",
        [
            {
                "SECCION": 3,
                "24A_PAN": None,
                "24A_MORENA": None,
            },
        ],
    )

    findings = (
        profile_winners_without_numeric_evidence(
            source
        )
    )

    assert findings == ()


def test_orders_winner_fields_deterministically(tmp_path):
    source = write_json(
        tmp_path / "master.json",
        [
            {
                "SECCION": 4,
                "GANADOR_PROY_2027_A": "MORENA",
                "GANADOR_24A": "PAN",
            },
        ],
    )

    findings = (
        profile_winners_without_numeric_evidence(
            source
        )
    )

    assert findings[0].winner_fields == (
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
        profile_winners_without_numeric_evidence(
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

    profile_winners_without_numeric_evidence(
        source
    )

    assert source.read_bytes() == before
