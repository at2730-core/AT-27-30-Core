import math
from copy import deepcopy

import pytest

from heyti.audit.data_truth.gubernatura_2024 import (
    GubernaturaSectionResult,
    GubernaturaSourceMismatch,
    rebuild_gubernatura_records,
)


def result(
    section_id: str,
    *,
    pan: int,
    pri: int,
    pvem: int,
    morena: int,
    total: int,
    nominal_list: int,
) -> GubernaturaSectionResult:
    return GubernaturaSectionResult(
        section_id=section_id,
        pan=pan,
        pri=pri,
        pvem=pvem,
        morena=morena,
        total=total,
        nominal_list=nominal_list,
    )


def test_rebuild_updates_only_certified_gubernatura_fields():
    master = [
        {
            "SECCION": 1,
            "MUNICIPIO": "ACAMBARO",
            "24A_PAN": 351.0,
            "24G_PAN": 380.0,
            "24G_PRI": 235.0,
            "24G_PVEM": 42.0,
            "24G_MORENA": 168.0,
            "24G_TOTAL": 925.0,
            "24G_LN": 1535.0,
        },
        {
            "SECCION": 1524,
            "MUNICIPIO": "LEON",
            "24A_PAN": 0.0,
            "24G_PAN": 275.0,
            "24G_PRI": 34.0,
            "24G_PVEM": 33.0,
            "24G_MORENA": 61.0,
            "24G_TOTAL": 444.0,
            "24G_LN": 668.0,
        },
    ]

    ine = {
        "1": result(
            "1",
            pan=492,
            pri=160,
            pvem=41,
            morena=266,
            total=1037,
            nominal_list=1570,
        ),
        "1524": result(
            "1524",
            pan=248,
            pri=9,
            pvem=8,
            morena=126,
            total=443,
            nominal_list=621,
        ),
    }

    ieeg = {
        "1": result(
            "1",
            pan=492,
            pri=160,
            pvem=41,
            morena=266,
            total=1037,
            nominal_list=1573,
        ),
        "1524": result(
            "1524",
            pan=248,
            pri=9,
            pvem=8,
            morena=126,
            total=443,
            nominal_list=620,
        ),
    }

    rebuilt, report = rebuild_gubernatura_records(
        master_records=master,
        ine_results=ine,
        ieeg_results=ieeg,
    )

    assert rebuilt[0] == {
        "SECCION": 1,
        "MUNICIPIO": "ACAMBARO",
        "24A_PAN": 351.0,
        "24G_PAN": 492,
        "24G_PRI": 160,
        "24G_PVEM": 41,
        "24G_MORENA": 266,
        "24G_TOTAL": 1037,
        "24G_LN": 1570,
    }
    assert rebuilt[1]["24G_PAN"] == 248
    assert rebuilt[1]["24G_PRI"] == 9
    assert rebuilt[1]["24G_PVEM"] == 8
    assert rebuilt[1]["24G_MORENA"] == 126
    assert rebuilt[1]["24G_TOTAL"] == 443
    assert rebuilt[1]["24G_LN"] == 621
    assert rebuilt[1]["24A_PAN"] == 0.0

    assert report.updated_sections == 2
    assert report.preserved_sections == 0
    assert report.verified_sections == 2


def test_rebuild_preserves_sections_without_ine_evidence():
    unavailable = float("nan")

    master = [
        {
            "SECCION": 9001,
            "24G_PAN": unavailable,
            "24G_PRI": unavailable,
            "24G_PVEM": unavailable,
            "24G_MORENA": unavailable,
            "24G_TOTAL": unavailable,
            "24G_LN": unavailable,
            "UNRELATED": "preserved",
        }
    ]

    rebuilt, report = rebuild_gubernatura_records(
        master_records=master,
        ine_results={},
        ieeg_results={
            "9001": result(
                "9001",
                pan=1,
                pri=2,
                pvem=3,
                morena=4,
                total=15,
                nominal_list=20,
            )
        },
    )

    assert rebuilt[0]["UNRELATED"] == "preserved"

    for field in (
        "24G_PAN",
        "24G_PRI",
        "24G_PVEM",
        "24G_MORENA",
        "24G_TOTAL",
        "24G_LN",
    ):
        assert math.isnan(rebuilt[0][field])

    assert report.updated_sections == 0
    assert report.preserved_sections == 1
    assert report.verified_sections == 0


def test_rebuild_rejects_disagreement_between_sources():
    master = [
        {
            "SECCION": 1,
            "24G_PAN": 380.0,
        }
    ]

    ine = {
        "1": result(
            "1",
            pan=492,
            pri=160,
            pvem=41,
            morena=266,
            total=1037,
            nominal_list=1570,
        )
    }

    ieeg = {
        "1": result(
            "1",
            pan=491,
            pri=160,
            pvem=41,
            morena=266,
            total=1037,
            nominal_list=1573,
        )
    }

    with pytest.raises(
        GubernaturaSourceMismatch,
        match="sección 1",
    ):
        rebuild_gubernatura_records(
            master_records=master,
            ine_results=ine,
            ieeg_results=ieeg,
        )


def test_rebuild_does_not_mutate_master_input():
    master = [
        {
            "SECCION": 1,
            "24G_PAN": 380.0,
            "NESTED": {
                "value": 1,
            },
        }
    ]
    original = deepcopy(master)

    certified = result(
        "1",
        pan=492,
        pri=160,
        pvem=41,
        morena=266,
        total=1037,
        nominal_list=1570,
    )

    rebuild_gubernatura_records(
        master_records=master,
        ine_results={
            "1": certified,
        },
        ieeg_results={
            "1": certified,
        },
    )

    assert master == original

import csv
import json

from openpyxl import Workbook

from heyti.audit.data_truth.gubernatura_2024 import (
    load_ieeg_casilla_results,
    load_ine_section_results,
    rebuild_gubernatura_file,
)


def write_ine_source(
    path,
    rows,
):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "2024_SEE_GOB_GTO_SEC"

    worksheet.append(
        [
            "SECCION",
            "PAN",
            "PRI",
            "PVEM",
            "MORENA",
            "TOTAL_VOTOS",
            "LISTA_NOMINAL",
        ]
    )

    for row in rows:
        worksheet.append(row)

    workbook.save(path)
    workbook.close()

    return path


def write_ieeg_source(
    path,
    rows,
):
    with path.open(
        "w",
        encoding="utf-8",
        newline="",
    ) as stream:
        stream.write("GUBERNATURA\n")
        stream.write("09/06/2024 12:00 (UTC-6)\n")
        stream.write('"\n')
        stream.write('"\n')
        stream.write(
            "ACTAS_ESPERADAS,ACTAS_COMPUTADAS,"
            "PORCENTAJE_ACTAS_COMPUTADAS,"
            "LN_COMPUTADA,TOTAL_VOTOS,"
            "PARTICIPACION_CONTABILIZADA\n"
        )
        stream.write("2,2,100.0000,100,60,60.0000\n")
        stream.write('"\n')
        stream.write('"\n')

        writer = csv.DictWriter(
            stream,
            fieldnames=[
                "SECCION",
                "PAN",
                "PRI",
                "PVEM",
                "MORENA",
                "TOTAL_VOTOS",
                "LISTA_NOMINAL",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    return path


def test_official_loaders_reconcile_votes_and_allow_ln_difference(
    tmp_path,
):
    ine_path = write_ine_source(
        tmp_path / "ine.xlsx",
        [
            [1, 30, 10, 5, 15, 70, 100],
            [0, 1, 1, 1, 1, 5, 10],
        ],
    )
    ieeg_path = write_ieeg_source(
        tmp_path / "ieeg.csv",
        [
            {
                "SECCION": 1,
                "PAN": 20,
                "PRI": 4,
                "PVEM": 2,
                "MORENA": 8,
                "TOTAL_VOTOS": 40,
                "LISTA_NOMINAL": 51,
            },
            {
                "SECCION": 1,
                "PAN": 10,
                "PRI": 6,
                "PVEM": 3,
                "MORENA": 7,
                "TOTAL_VOTOS": 30,
                "LISTA_NOMINAL": 50,
            },
        ],
    )

    ine = load_ine_section_results(ine_path)
    ieeg = load_ieeg_casilla_results(ieeg_path)

    assert set(ine) == {"1"}
    assert set(ieeg) == {"1"}

    assert ine["1"].comparable_votes == (
        30,
        10,
        5,
        15,
        70,
    )
    assert ieeg["1"].comparable_votes == (
        30,
        10,
        5,
        15,
        70,
    )

    assert ine["1"].nominal_list == 100
    assert ieeg["1"].nominal_list == 101


def test_file_rebuild_writes_candidate_and_preserves_source(
    tmp_path,
):
    master_path = tmp_path / "master.json"
    output_path = tmp_path / "candidate.json"
    ine_path = write_ine_source(
        tmp_path / "ine.xlsx",
        [
            [1, 30, 10, 5, 15, 70, 100],
        ],
    )
    ieeg_path = write_ieeg_source(
        tmp_path / "ieeg.csv",
        [
            {
                "SECCION": 1,
                "PAN": 30,
                "PRI": 10,
                "PVEM": 5,
                "MORENA": 15,
                "TOTAL_VOTOS": 70,
                "LISTA_NOMINAL": 101,
            },
        ],
    )

    original_records = [
        {
            "SECCION": 1,
            "24G_PAN": 99,
            "24G_PRI": 99,
            "24G_PVEM": 99,
            "24G_MORENA": 99,
            "24G_TOTAL": 999,
            "24G_LN": 999,
            "UNCHANGED": "yes",
        },
        {
            "SECCION": 9001,
            "24G_PAN": None,
            "UNCHANGED": "blocked",
        },
    ]

    master_path.write_text(
        json.dumps(original_records),
        encoding="utf-8",
    )
    source_before = master_path.read_bytes()

    report = rebuild_gubernatura_file(
        master_path=master_path,
        ine_section_path=ine_path,
        ieeg_path=ieeg_path,
        output_path=output_path,
    )

    assert master_path.read_bytes() == source_before
    assert output_path.is_file()

    candidate = json.loads(
        output_path.read_text(
            encoding="utf-8",
        )
    )

    assert candidate[0]["24G_PAN"] == 30
    assert candidate[0]["24G_PRI"] == 10
    assert candidate[0]["24G_PVEM"] == 5
    assert candidate[0]["24G_MORENA"] == 15
    assert candidate[0]["24G_TOTAL"] == 70
    assert candidate[0]["24G_LN"] == 100
    assert candidate[0]["UNCHANGED"] == "yes"
    assert candidate[1] == original_records[1]

    assert report.total_master_sections == 2
    assert report.updated_sections == 1
    assert report.preserved_sections == 1
    assert report.verified_sections == 1


def test_file_rebuild_refuses_existing_output(
    tmp_path,
):
    master_path = tmp_path / "master.json"
    output_path = tmp_path / "candidate.json"
    ine_path = write_ine_source(
        tmp_path / "ine.xlsx",
        [],
    )
    ieeg_path = write_ieeg_source(
        tmp_path / "ieeg.csv",
        [],
    )

    master_path.write_text(
        '[{"SECCION": 1}]',
        encoding="utf-8",
    )
    output_path.write_text(
        "protected",
        encoding="utf-8",
    )

    with pytest.raises(
        FileExistsError,
        match="ya existe",
    ):
        rebuild_gubernatura_file(
            master_path=master_path,
            ine_section_path=ine_path,
            ieeg_path=ieeg_path,
            output_path=output_path,
        )

    assert output_path.read_text(
        encoding="utf-8",
    ) == "protected"


def test_file_rebuild_refuses_source_as_output(
    tmp_path,
):
    master_path = tmp_path / "master.json"
    ine_path = write_ine_source(
        tmp_path / "ine.xlsx",
        [],
    )
    ieeg_path = write_ieeg_source(
        tmp_path / "ieeg.csv",
        [],
    )

    master_path.write_text(
        '[{"SECCION": 1}]',
        encoding="utf-8",
    )

    with pytest.raises(
        ValueError,
        match="distinta",
    ):
        rebuild_gubernatura_file(
            master_path=master_path,
            ine_section_path=ine_path,
            ieeg_path=ieeg_path,
            output_path=master_path,
        )