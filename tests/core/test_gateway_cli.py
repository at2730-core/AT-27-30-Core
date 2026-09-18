from pathlib import Path

import pytest

from heyti.gateway.cli import (
    default_geometry_path,
    default_master_path,
    main,
    repository_root,
)


def test_cli_resolves_official_repository_sources():
    root = repository_root()

    assert root == Path(__file__).resolve().parents[2]
    assert default_master_path() == (
        root
        / "datasets"
        / "electoral"
        / "Datos_Electoral_con_2015.json"
    )
    assert default_geometry_path() == (
        root
        / "datasets"
        / "spatial"
        / "secciones.geojson"
    )
    assert default_master_path().is_file()
    assert default_geometry_path().is_file()


def test_cli_check_validates_certified_runtime(
    capsys,
):
    result = main(
        [
            "--check",
        ]
    )

    captured = capsys.readouterr()

    assert result == 0
    assert "HEYTI-CORE VALIDATION OK" in captured.out


def test_cli_fails_closed_for_missing_sources(
    tmp_path,
    capsys,
):
    with pytest.raises(SystemExit) as error:
        main(
            [
                "--check",
                "--master",
                str(tmp_path / "missing-master.json"),
                "--geometry",
                str(tmp_path / "missing-geometry.geojson"),
            ]
        )

    captured = capsys.readouterr()

    assert error.value.code == 1
    assert "HEYTI-CORE no pudo iniciar" in captured.err


@pytest.mark.parametrize(
    "port",
    [
        "-1",
        "65536",
    ],
)
def test_cli_rejects_invalid_port(
    port,
):
    with pytest.raises(SystemExit) as error:
        main(
            [
                "--check",
                "--port",
                port,
            ]
        )

    assert error.value.code == 2
