import json
from pathlib import Path

import pytest

from heyti.capabilities.describe_section.electoral_result_source import (
    ELECTORAL_CONTESTS,
    CertifiedElectoralSectionSource,
)


def build_record(
    section_id=1,
):
    record = {
        "SECCION": section_id,
    }

    for contest in ELECTORAL_CONTESTS:
        record.update(
            {
                f"24{contest}_PAN": 40,
                f"24{contest}_PRI": 20,
                f"24{contest}_PVEM": 10,
                f"24{contest}_MORENA": 30,
                f"24{contest}_TOTAL": 120,
                f"24{contest}_LN": 200,
            }
        )

    return record


def write_master(
    tmp_path: Path,
    records,
) -> Path:
    master_path = tmp_path / "master.json"
    master_path.write_text(
        json.dumps(records),
        encoding="utf-8",
    )
    return master_path


def real_master_path() -> Path:
    return (
        Path(__file__).resolve().parents[2]
        / "datasets"
        / "electoral"
        / "Datos_Electoral_con_2015.json"
    )


def test_source_returns_certified_electoral_content(
    tmp_path,
):
    master_path = write_master(
        tmp_path,
        [build_record()],
    )

    source = CertifiedElectoralSectionSource(
        master_path=master_path,
        authorized_section_ids=[1],
    )

    content = source.get_section_electoral("1")

    assert content is not None
    assert content["section_id"] == "1"
    assert content["election_year"] == 2024
    assert content["coverage_scope"] == (
        "TRACKED_PARTIES_ONLY"
    )
    assert content["tracked_parties"] == [
        "PAN",
        "PRI",
        "PVEM",
        "MORENA",
    ]
    assert content["quality_status"] == "COMPLETE"

    contest = content["contests"]["A"]

    assert contest["data_status"] == "AVAILABLE"
    assert contest["votes_by_tracked_party"] == {
        "PAN": 40,
        "PRI": 20,
        "PVEM": 10,
        "MORENA": 30,
    }
    assert contest["total_votes"] == 120
    assert contest["nominal_list"] == 200
    assert contest["tracked_votes"] == 100
    assert contest["residual_votes"] == 20
    assert contest["participation_rate"] == 0.6
    assert contest["leading_tracked_party"] == "PAN"
    assert contest["tracked_lead_margin"] == 10
    assert "winner" not in contest


def test_source_marks_zero_total_without_fabricating_leader(
    tmp_path,
):
    record = build_record()

    for party in ("PAN", "PRI", "PVEM", "MORENA"):
        record[f"24A_{party}"] = 0

    record["24A_TOTAL"] = 0

    source = CertifiedElectoralSectionSource(
        master_path=write_master(
            tmp_path,
            [record],
        ),
        authorized_section_ids=[1],
    )

    content = source.get_section_electoral("1")
    contest = content["contests"]["A"]

    assert content["quality_status"] == "PARTIAL"
    assert contest["data_status"] == "ZERO_TOTAL"
    assert contest["tracked_votes"] == 0
    assert contest["residual_votes"] == 0
    assert contest["participation_rate"] == 0
    assert contest["leading_tracked_party"] is None
    assert contest["tracked_lead_margin"] is None


def test_source_marks_incomplete_contest(
    tmp_path,
):
    record = build_record()
    del record["24DL_MORENA"]

    source = CertifiedElectoralSectionSource(
        master_path=write_master(
            tmp_path,
            [record],
        ),
        authorized_section_ids=[1],
    )

    content = source.get_section_electoral("1")
    contest = content["contests"]["DL"]

    assert content["quality_status"] == "PARTIAL"
    assert contest["data_status"] == "INCOMPLETE"
    assert contest["leading_tracked_party"] is None


def test_source_marks_inconsistent_values(
    tmp_path,
):
    record = build_record()
    record["24DF_TOTAL"] = 50

    source = CertifiedElectoralSectionSource(
        master_path=write_master(
            tmp_path,
            [record],
        ),
        authorized_section_ids=[1],
    )

    content = source.get_section_electoral("1")
    contest = content["contests"]["DF"]

    assert content["quality_status"] == "PARTIAL"
    assert contest["data_status"] == "INCONSISTENT"
    assert contest["tracked_votes"] == 100
    assert contest["residual_votes"] == -50
    assert contest["leading_tracked_party"] is None


def test_source_marks_tied_tracked_lead(
    tmp_path,
):
    record = build_record()
    record["24G_PAN"] = 40
    record["24G_MORENA"] = 40

    source = CertifiedElectoralSectionSource(
        master_path=write_master(
            tmp_path,
            [record],
        ),
        authorized_section_ids=[1],
    )

    content = source.get_section_electoral("1")
    contest = content["contests"]["G"]

    assert content["quality_status"] == "PARTIAL"
    assert contest["data_status"] == (
        "TIED_TRACKED_LEAD"
    )
    assert contest["leading_tracked_party"] is None
    assert contest["tracked_lead_margin"] is None


def test_source_does_not_publish_unauthorized_section(
    tmp_path,
):
    source = CertifiedElectoralSectionSource(
        master_path=write_master(
            tmp_path,
            [build_record()],
        ),
        authorized_section_ids=[1],
    )

    assert source.get_section_electoral("2") is None
    assert source.get_section_electoral("invalid") is None


def test_source_returns_isolated_copies(
    tmp_path,
):
    source = CertifiedElectoralSectionSource(
        master_path=write_master(
            tmp_path,
            [build_record()],
        ),
        authorized_section_ids=[1],
    )

    first = source.get_section_electoral("1")
    first["contests"]["A"][
        "votes_by_tracked_party"
    ]["PAN"] = 999

    second = source.get_section_electoral("1")

    assert second["contests"]["A"][
        "votes_by_tracked_party"
    ]["PAN"] == 40


def test_source_rejects_invalid_authorized_ids(
    tmp_path,
):
    master_path = write_master(
        tmp_path,
        [build_record()],
    )

    with pytest.raises(
        TypeError,
        match="identificadores enteros positivos",
    ):
        CertifiedElectoralSectionSource(
            master_path=master_path,
            authorized_section_ids=[1, "invalid"],
        )


def test_source_rejects_empty_authorized_ids(
    tmp_path,
):
    master_path = write_master(
        tmp_path,
        [build_record()],
    )

    with pytest.raises(
        ValueError,
        match="no puede estar vacío",
    ):
        CertifiedElectoralSectionSource(
            master_path=master_path,
            authorized_section_ids=[],
        )


def test_source_rejects_non_list_master(
    tmp_path,
):
    master_path = write_master(
        tmp_path,
        {"SECCION": 1},
    )

    with pytest.raises(
        ValueError,
        match="debe ser una lista",
    ):
        CertifiedElectoralSectionSource(
            master_path=master_path,
            authorized_section_ids=[1],
        )


def test_source_rejects_duplicate_sections(
    tmp_path,
):
    master_path = write_master(
        tmp_path,
        [
            build_record(1),
            build_record("1"),
        ],
    )

    with pytest.raises(
        ValueError,
        match="sección duplicada: 1",
    ):
        CertifiedElectoralSectionSource(
            master_path=master_path,
            authorized_section_ids=[1],
        )


def test_source_rejects_missing_authorized_section(
    tmp_path,
):
    master_path = write_master(
        tmp_path,
        [build_record(1)],
    )

    with pytest.raises(
        ValueError,
        match="no contiene todas las secciones",
    ):
        CertifiedElectoralSectionSource(
            master_path=master_path,
            authorized_section_ids=[1, 2],
        )


def test_real_golden_section_one_is_complete():
    source = CertifiedElectoralSectionSource(
        master_path=real_master_path(),
        authorized_section_ids=[1, 1524],
    )

    content = source.get_section_electoral("1")

    assert content["quality_status"] == "COMPLETE"

    assert content["contests"]["A"][
        "leading_tracked_party"
    ] == "PRI"
    assert content["contests"]["A"][
        "tracked_lead_margin"
    ] == 5.0

    assert content["contests"]["P"][
        "leading_tracked_party"
    ] == "MORENA"
    assert content["contests"]["P"][
        "residual_votes"
    ] == 214.0

    for contest in ELECTORAL_CONTESTS:
        assert content["contests"][contest][
            "data_status"
        ] == "AVAILABLE"


def test_real_section_1524_preserves_partial_truth():
    source = CertifiedElectoralSectionSource(
        master_path=real_master_path(),
        authorized_section_ids=[1, 1524],
    )

    content = source.get_section_electoral("1524")

    assert content["quality_status"] == "PARTIAL"

    ayuntamiento = content["contests"]["A"]

    assert ayuntamiento["data_status"] == "ZERO_TOTAL"
    assert ayuntamiento["total_votes"] == 0.0
    assert ayuntamiento["nominal_list"] == 620.0
    assert ayuntamiento["leading_tracked_party"] is None

    assert content["contests"]["DL"][
        "data_status"
    ] == "AVAILABLE"
