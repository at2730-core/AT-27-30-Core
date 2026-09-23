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

def test_source_sanitizes_non_finite_values_for_json(
    tmp_path,
):
    record = build_record()
    record["24DL_LN"] = float("nan")

    source = CertifiedElectoralSectionSource(
        master_path=write_master(
            tmp_path,
            [record],
        ),
        authorized_section_ids=[1],
    )

    content = source.get_section_electoral("1")
    contest = content["contests"]["DL"]

    assert contest["data_status"] == "INCOMPLETE"
    assert contest["nominal_list"] is None

    serialized = json.dumps(
        content,
        allow_nan=False,
    )

    assert '"nominal_list": null' in serialized

def test_source_quarantines_configured_contest():
    source = CertifiedElectoralSectionSource(
        master_path=real_master_path(),
        authorized_section_ids=[1],
        quarantined_contests=["G"],
    )

    content = source.get_section_electoral("1")

    assert content is not None
    assert content["quality_status"] == "PARTIAL"
    assert source.quarantined_contests == frozenset({"G"})

    ayuntamiento = content["contests"]["A"]
    gubernatura = content["contests"]["G"]

    assert ayuntamiento["data_status"] == "AVAILABLE"

    assert gubernatura["data_status"] == "INCONSISTENT"
    assert all(
        value is None
        for value in gubernatura[
            "votes_by_tracked_party"
        ].values()
    )
    assert gubernatura["total_votes"] is None
    assert gubernatura["nominal_list"] is None
    assert gubernatura["tracked_votes"] is None
    assert gubernatura["residual_votes"] is None
    assert gubernatura["participation_rate"] is None
    assert gubernatura["leading_tracked_party"] is None
    assert gubernatura["tracked_lead_margin"] is None

@pytest.mark.parametrize(
    "quarantined_contests",
    [
        "G",
        [1],
    ],
)
def test_source_rejects_invalid_quarantine_container(
    quarantined_contests,
):
    with pytest.raises(TypeError):
        CertifiedElectoralSectionSource(
            master_path=real_master_path(),
            authorized_section_ids=[1],
            quarantined_contests=quarantined_contests,
        )


def test_source_rejects_unknown_quarantined_contest():
    with pytest.raises(
        ValueError,
        match="contiendas no soportadas",
    ):
        CertifiedElectoralSectionSource(
            master_path=real_master_path(),
            authorized_section_ids=[1],
            quarantined_contests=["UNKNOWN"],
        )

def test_real_golden_section_one_exposes_historical_elections():
    source = CertifiedElectoralSectionSource(
        master_path=real_master_path(),
        authorized_section_ids=[1],
    )

    content = source.get_section_electoral("1")
    history = content["historical_elections"]

    assert [
        election["election_year"]
        for election in history
    ] == [2018, 2021]

    election_2018 = history[0]

    assert election_2018["quality_status"] == "PARTIAL"

    ayuntamiento_2018 = election_2018[
        "contests"
    ]["A"]

    assert ayuntamiento_2018["data_status"] == "AVAILABLE"
    assert ayuntamiento_2018[
        "votes_by_tracked_party"
    ] == {
        "PAN": 250.0,
        "PRI": 441.0,
        "PVEM": 40.0,
        "MORENA": 131.0,
    }
    assert ayuntamiento_2018["total_votes"] == 932.0
    assert ayuntamiento_2018["nominal_list"] == 1535.0
    assert ayuntamiento_2018["tracked_votes"] == 862.0
    assert ayuntamiento_2018["residual_votes"] == 70.0
    assert ayuntamiento_2018[
        "participation_rate"
    ] == pytest.approx(932 / 1535)
    assert ayuntamiento_2018[
        "leading_tracked_party"
    ] == "PRI"
    assert ayuntamiento_2018[
        "tracked_lead_margin"
    ] == 191.0

    diputacion_federal_2018 = election_2018[
        "contests"
    ]["DF"]

    assert diputacion_federal_2018[
        "data_status"
    ] == "AVAILABLE_WITHOUT_NOMINAL_LIST"
    assert diputacion_federal_2018[
        "total_votes"
    ] == 931.0
    assert diputacion_federal_2018[
        "nominal_list"
    ] is None
    assert diputacion_federal_2018[
        "tracked_votes"
    ] == 797.0
    assert diputacion_federal_2018[
        "residual_votes"
    ] == 134.0
    assert diputacion_federal_2018[
        "participation_rate"
    ] is None
    assert diputacion_federal_2018[
        "leading_tracked_party"
    ] == "PAN"
    assert diputacion_federal_2018[
        "tracked_lead_margin"
    ] == 25.0

    election_2021 = history[1]

    assert election_2021["quality_status"] == "PARTIAL"

    diputacion_federal_2021 = election_2021[
        "contests"
    ]["DF"]

    assert diputacion_federal_2021[
        "data_status"
    ] == "SUMMARY_ONLY"
    assert all(
        value is None
        for value in diputacion_federal_2021[
            "votes_by_tracked_party"
        ].values()
    )
    assert diputacion_federal_2021[
        "total_votes"
    ] == 877.0
    assert diputacion_federal_2021[
        "nominal_list"
    ] == 1580.0
    assert diputacion_federal_2021[
        "tracked_votes"
    ] is None
    assert diputacion_federal_2021[
        "residual_votes"
    ] is None
    assert diputacion_federal_2021[
        "participation_rate"
    ] == pytest.approx(877 / 1580)
    assert diputacion_federal_2021[
        "leading_tracked_party"
    ] is None
    assert diputacion_federal_2021[
        "tracked_lead_margin"
    ] is None

    for contest in ("G", "S", "P"):
        unavailable = election_2021[
            "contests"
        ][contest]

        assert unavailable[
            "data_status"
        ] == "NOT_CONTESTED"
        assert all(
            value is None
            for value in unavailable[
                "votes_by_tracked_party"
            ].values()
        )
        assert unavailable["total_votes"] is None
        assert unavailable["nominal_list"] is None
        assert unavailable["tracked_votes"] is None
        assert unavailable["residual_votes"] is None
        assert unavailable["participation_rate"] is None
        assert unavailable[
            "leading_tracked_party"
        ] is None
        assert unavailable[
            "tracked_lead_margin"
        ] is None

def test_real_golden_section_1524_exposes_historical_elections():
    source = CertifiedElectoralSectionSource(
        master_path=real_master_path(),
        authorized_section_ids=[1524],
    )

    content = source.get_section_electoral("1524")
    history = content["historical_elections"]

    assert [
        election["election_year"]
        for election in history
    ] == [2018, 2021]

    election_2018 = history[0]

    assert election_2018["quality_status"] == "PARTIAL"

    gubernatura_2018 = election_2018[
        "contests"
    ]["G"]

    assert gubernatura_2018["data_status"] == "AVAILABLE"
    assert gubernatura_2018[
        "votes_by_tracked_party"
    ] == {
        "PAN": 275.0,
        "PRI": 34.0,
        "PVEM": 33.0,
        "MORENA": 61.0,
    }
    assert gubernatura_2018["total_votes"] == 444.0
    assert gubernatura_2018["nominal_list"] == 668.0
    assert gubernatura_2018["tracked_votes"] == 403.0
    assert gubernatura_2018["residual_votes"] == 41.0
    assert gubernatura_2018[
        "participation_rate"
    ] == pytest.approx(444 / 668)
    assert gubernatura_2018[
        "leading_tracked_party"
    ] == "PAN"
    assert gubernatura_2018[
        "tracked_lead_margin"
    ] == 214.0

    diputacion_federal_2018 = election_2018[
        "contests"
    ]["DF"]

    assert diputacion_federal_2018[
        "data_status"
    ] == "AVAILABLE_WITHOUT_NOMINAL_LIST"
    assert diputacion_federal_2018[
        "total_votes"
    ] == 444.0
    assert diputacion_federal_2018[
        "nominal_list"
    ] is None
    assert diputacion_federal_2018[
        "tracked_votes"
    ] == 394.0
    assert diputacion_federal_2018[
        "residual_votes"
    ] == 50.0
    assert diputacion_federal_2018[
        "participation_rate"
    ] is None
    assert diputacion_federal_2018[
        "leading_tracked_party"
    ] == "PAN"
    assert diputacion_federal_2018[
        "tracked_lead_margin"
    ] == 188.0

    election_2021 = history[1]

    assert election_2021["quality_status"] == "PARTIAL"

    ayuntamiento_2021 = election_2021[
        "contests"
    ]["A"]

    assert ayuntamiento_2021["data_status"] == "AVAILABLE"
    assert ayuntamiento_2021[
        "votes_by_tracked_party"
    ] == {
        "PAN": 231.0,
        "PRI": 12.0,
        "PVEM": 6.0,
        "MORENA": 75.0,
    }
    assert ayuntamiento_2021["total_votes"] == 355.0
    assert ayuntamiento_2021["nominal_list"] == 647.0
    assert ayuntamiento_2021["tracked_votes"] == 324.0
    assert ayuntamiento_2021["residual_votes"] == 31.0
    assert ayuntamiento_2021[
        "participation_rate"
    ] == pytest.approx(355 / 647)
    assert ayuntamiento_2021[
        "leading_tracked_party"
    ] == "PAN"
    assert ayuntamiento_2021[
        "tracked_lead_margin"
    ] == 156.0

    diputacion_local_2021 = election_2021[
        "contests"
    ]["DL"]

    assert diputacion_local_2021[
        "data_status"
    ] == "INCOMPLETE"
    assert all(
        value is None
        for value in diputacion_local_2021[
            "votes_by_tracked_party"
        ].values()
    )
    assert diputacion_local_2021["total_votes"] is None
    assert diputacion_local_2021["nominal_list"] is None
    assert diputacion_local_2021["tracked_votes"] is None
    assert diputacion_local_2021["residual_votes"] is None
    assert diputacion_local_2021[
        "participation_rate"
    ] is None

    diputacion_federal_2021 = election_2021[
        "contests"
    ]["DF"]

    assert diputacion_federal_2021[
        "data_status"
    ] == "SUMMARY_ONLY"
    assert diputacion_federal_2021[
        "total_votes"
    ] == 353.0
    assert diputacion_federal_2021[
        "nominal_list"
    ] == 647.0
    assert diputacion_federal_2021[
        "participation_rate"
    ] == pytest.approx(353 / 647)

    for contest in ("G", "S", "P"):
        assert election_2021[
            "contests"
        ][contest]["data_status"] == "NOT_CONTESTED"
