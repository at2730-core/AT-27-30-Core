from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Iterable, Mapping


GUBERNATURA_FIELDS = (
    "24G_PAN",
    "24G_PRI",
    "24G_PVEM",
    "24G_MORENA",
    "24G_TOTAL",
    "24G_LN",
)


class GubernaturaSourceMismatch(ValueError):
    """Indica una divergencia entre resultados oficiales."""


def _normalize_section_id(
    value: Any,
) -> str:
    if isinstance(value, bool):
        raise TypeError(
            "La sección debe ser un entero positivo"
        )

    try:
        number = int(value)
    except (TypeError, ValueError) as error:
        raise TypeError(
            "La sección debe ser un entero positivo"
        ) from error

    if number <= 0:
        raise ValueError(
            "La sección debe ser un entero positivo"
        )

    if isinstance(value, float) and not value.is_integer():
        raise ValueError(
            "La sección debe ser un entero positivo"
        )

    if isinstance(value, str):
        stripped = value.strip()

        if not stripped.isdigit():
            raise ValueError(
                "La sección debe ser un entero positivo"
            )

    return str(number)


def _validate_count(
    value: Any,
    field_name: str,
) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(
            f"{field_name} debe ser un entero"
        )

    if value < 0:
        raise ValueError(
            f"{field_name} no puede ser negativo"
        )

    return value


@dataclass(frozen=True)
class GubernaturaSectionResult:
    """Resultado certificado de Gubernatura por sección."""

    section_id: str
    pan: int
    pri: int
    pvem: int
    morena: int
    total: int
    nominal_list: int

    def __post_init__(self) -> None:
        normalized_section_id = _normalize_section_id(
            self.section_id
        )

        object.__setattr__(
            self,
            "section_id",
            normalized_section_id,
        )

        for field_name in (
            "pan",
            "pri",
            "pvem",
            "morena",
            "total",
            "nominal_list",
        ):
            object.__setattr__(
                self,
                field_name,
                _validate_count(
                    getattr(self, field_name),
                    field_name,
                ),
            )

    @property
    def comparable_votes(
        self,
    ) -> tuple[int, int, int, int, int]:
        """
        Valores comparables entre INE e IEEG.

        La lista nominal queda fuera porque las fuentes oficiales
        presentan diferencias documentadas en ese campo.
        """

        return (
            self.pan,
            self.pri,
            self.pvem,
            self.morena,
            self.total,
        )

    def as_master_fields(
        self,
    ) -> dict[str, int]:
        return {
            "24G_PAN": self.pan,
            "24G_PRI": self.pri,
            "24G_PVEM": self.pvem,
            "24G_MORENA": self.morena,
            "24G_TOTAL": self.total,
            "24G_LN": self.nominal_list,
        }


@dataclass(frozen=True)
class GubernaturaRebuildReport:
    """Resumen inmutable de una reconstrucción controlada."""

    total_master_sections: int
    updated_sections: int
    preserved_sections: int
    verified_sections: int


def _index_master_records(
    master_records: Iterable[dict[str, Any]],
) -> dict[str, int]:
    indexed: dict[str, int] = {}

    for position, record in enumerate(master_records):
        if not isinstance(record, dict):
            raise TypeError(
                "El maestro contiene un registro no válido"
            )

        if "SECCION" not in record:
            raise ValueError(
                "El maestro contiene un registro sin SECCION"
            )

        section_id = _normalize_section_id(
            record["SECCION"]
        )

        if section_id in indexed:
            raise ValueError(
                "El maestro contiene una sección duplicada: "
                f"{section_id}"
            )

        indexed[section_id] = position

    return indexed


def _validate_result_mapping(
    results: Mapping[str, GubernaturaSectionResult],
    source_name: str,
) -> dict[str, GubernaturaSectionResult]:
    validated: dict[str, GubernaturaSectionResult] = {}

    for raw_section_id, result in results.items():
        section_id = _normalize_section_id(
            raw_section_id
        )

        if not isinstance(
            result,
            GubernaturaSectionResult,
        ):
            raise TypeError(
                f"{source_name} contiene un resultado no válido"
            )

        if result.section_id != section_id:
            raise ValueError(
                f"{source_name} contiene una identidad "
                f"inconsistente para la sección {section_id}"
            )

        if section_id in validated:
            raise ValueError(
                f"{source_name} contiene una sección duplicada: "
                f"{section_id}"
            )

        validated[section_id] = result

    return validated


def rebuild_gubernatura_records(
    *,
    master_records: Iterable[dict[str, Any]],
    ine_results: Mapping[
        str,
        GubernaturaSectionResult,
    ],
    ieeg_results: Mapping[
        str,
        GubernaturaSectionResult,
    ],
) -> tuple[
    list[dict[str, Any]],
    GubernaturaRebuildReport,
]:
    """
    Reconstruye exclusivamente los campos 24G certificados.

    INE define los valores publicados, incluida la lista nominal.
    IEEG verifica los votos y el total. Las secciones sin evidencia
    INE se preservan sin modificación.
    """

    master_copy = deepcopy(list(master_records))
    master_index = _index_master_records(
        master_copy
    )
    validated_ine = _validate_result_mapping(
        ine_results,
        "INE",
    )
    validated_ieeg = _validate_result_mapping(
        ieeg_results,
        "IEEG",
    )

    unknown_ine_sections = (
        set(validated_ine)
        - set(master_index)
    )

    if unknown_ine_sections:
        ordered = sorted(
            unknown_ine_sections,
            key=int,
        )
        raise ValueError(
            "INE contiene secciones ausentes del maestro: "
            f"{ordered}"
        )

    verified_sections = 0

    for section_id, ine_result in validated_ine.items():
        ieeg_result = validated_ieeg.get(
            section_id
        )

        if ieeg_result is None:
            raise GubernaturaSourceMismatch(
                "IEEG no contiene evidencia para la "
                f"sección {section_id}"
            )

        if (
            ine_result.comparable_votes
            != ieeg_result.comparable_votes
        ):
            raise GubernaturaSourceMismatch(
                "INE e IEEG difieren en la "
                f"sección {section_id}"
            )

        verified_sections += 1

    for section_id, ine_result in validated_ine.items():
        record_position = master_index[section_id]
        master_copy[record_position].update(
            ine_result.as_master_fields()
        )

    updated_sections = len(validated_ine)
    total_master_sections = len(master_copy)

    return (
        master_copy,
        GubernaturaRebuildReport(
            total_master_sections=total_master_sections,
            updated_sections=updated_sections,
            preserved_sections=(
                total_master_sections
                - updated_sections
            ),
            verified_sections=verified_sections,
        ),
    )

import csv
import json
import math
import os
from pathlib import Path

from openpyxl import load_workbook


INE_REQUIRED_COLUMNS = frozenset(
    {
        "SECCION",
        "PAN",
        "PRI",
        "PVEM",
        "MORENA",
        "TOTAL_VOTOS",
        "LISTA_NOMINAL",
    }
)

IEEG_REQUIRED_COLUMNS = INE_REQUIRED_COLUMNS


def _source_count(
    value: Any,
    field_name: str,
    source_name: str,
) -> int:
    if isinstance(value, bool):
        raise TypeError(
            f"{source_name}: {field_name} no es numérico"
        )

    try:
        number = float(value)
    except (TypeError, ValueError) as error:
        raise TypeError(
            f"{source_name}: {field_name} no es numérico"
        ) from error

    if not math.isfinite(number):
        raise ValueError(
            f"{source_name}: {field_name} no es finito"
        )

    if not number.is_integer():
        raise ValueError(
            f"{source_name}: {field_name} no es entero"
        )

    integer = int(number)

    if integer < 0:
        raise ValueError(
            f"{source_name}: {field_name} es negativo"
        )

    return integer


def _source_section_id(
    value: Any,
    source_name: str,
) -> str | None:
    if isinstance(value, bool):
        raise TypeError(
            f"{source_name}: SECCION no es válida"
        )

    try:
        number = int(value)
    except (TypeError, ValueError) as error:
        raise TypeError(
            f"{source_name}: SECCION no es válida"
        ) from error

    if number == 0:
        return None

    try:
        return _normalize_section_id(value)
    except (TypeError, ValueError) as error:
        raise ValueError(
            f"{source_name}: SECCION no es válida"
        ) from error


def _result_from_source_record(
    *,
    section_id: str,
    record: Mapping[str, Any],
    source_name: str,
) -> GubernaturaSectionResult:
    return GubernaturaSectionResult(
        section_id=section_id,
        pan=_source_count(
            record["PAN"],
            "PAN",
            source_name,
        ),
        pri=_source_count(
            record["PRI"],
            "PRI",
            source_name,
        ),
        pvem=_source_count(
            record["PVEM"],
            "PVEM",
            source_name,
        ),
        morena=_source_count(
            record["MORENA"],
            "MORENA",
            source_name,
        ),
        total=_source_count(
            record["TOTAL_VOTOS"],
            "TOTAL_VOTOS",
            source_name,
        ),
        nominal_list=_source_count(
            record["LISTA_NOMINAL"],
            "LISTA_NOMINAL",
            source_name,
        ),
    )


def load_ine_section_results(
    path: str | Path,
) -> dict[str, GubernaturaSectionResult]:
    """Lee resultados oficiales INE agregados por sección."""

    source_path = Path(path)

    if not source_path.is_file():
        raise FileNotFoundError(
            f"No se encontró la fuente INE: {source_path}"
        )

    workbook = load_workbook(
        source_path,
        read_only=True,
        data_only=True,
    )

    try:
        if len(workbook.sheetnames) != 1:
            raise ValueError(
                "La fuente INE debe contener una sola hoja"
            )

        worksheet = workbook[workbook.sheetnames[0]]
        rows = worksheet.iter_rows(values_only=True)
        headers = next(rows, None)

        if headers is None:
            raise ValueError(
                "La fuente INE está vacía"
            )

        header_set = frozenset(headers)

        if not INE_REQUIRED_COLUMNS <= header_set:
            missing = sorted(
                INE_REQUIRED_COLUMNS - header_set
            )
            raise ValueError(
                "La fuente INE no contiene las columnas "
                f"requeridas: {missing}"
            )

        results: dict[
            str,
            GubernaturaSectionResult,
        ] = {}

        for values in rows:
            record = dict(zip(headers, values))
            section_id = _source_section_id(
                record["SECCION"],
                "INE",
            )

            if section_id is None:
                continue

            if section_id in results:
                raise ValueError(
                    "La fuente INE contiene una sección "
                    f"duplicada: {section_id}"
                )

            results[section_id] = (
                _result_from_source_record(
                    section_id=section_id,
                    record=record,
                    source_name="INE",
                )
            )

        return results
    finally:
        workbook.close()


def _find_ieeg_header_index(
    lines: list[str],
) -> int:
    for index, line in enumerate(lines):
        try:
            columns = next(
                csv.reader([line])
            )
        except csv.Error:
            continue

        if IEEG_REQUIRED_COLUMNS <= frozenset(columns):
            return index

    raise ValueError(
        "La fuente IEEG no contiene el encabezado esperado"
    )


def load_ieeg_casilla_results(
    path: str | Path,
) -> dict[str, GubernaturaSectionResult]:
    """Agrega por sección los cómputos de casilla del IEEG."""

    source_path = Path(path)

    if not source_path.is_file():
        raise FileNotFoundError(
            f"No se encontró la fuente IEEG: {source_path}"
        )

    lines = source_path.read_text(
        encoding="utf-8-sig",
    ).splitlines()

    header_index = _find_ieeg_header_index(lines)
    reader = csv.DictReader(
        lines[header_index:]
    )

    if reader.fieldnames is None:
        raise ValueError(
            "La fuente IEEG no contiene columnas"
        )

    fieldnames = frozenset(reader.fieldnames)

    if not IEEG_REQUIRED_COLUMNS <= fieldnames:
        missing = sorted(
            IEEG_REQUIRED_COLUMNS - fieldnames
        )
        raise ValueError(
            "La fuente IEEG no contiene las columnas "
            f"requeridas: {missing}"
        )

    aggregated: dict[str, dict[str, int]] = {}

    for record in reader:
        section_id = _source_section_id(
            record["SECCION"],
            "IEEG",
        )

        if section_id is None:
            continue

        section_values = aggregated.setdefault(
            section_id,
            {
                "PAN": 0,
                "PRI": 0,
                "PVEM": 0,
                "MORENA": 0,
                "TOTAL_VOTOS": 0,
                "LISTA_NOMINAL": 0,
            },
        )

        for field_name in (
            "PAN",
            "PRI",
            "PVEM",
            "MORENA",
            "TOTAL_VOTOS",
            "LISTA_NOMINAL",
        ):
            section_values[field_name] += _source_count(
                record[field_name],
                field_name,
                "IEEG",
            )

    return {
        section_id: _result_from_source_record(
            section_id=section_id,
            record=values,
            source_name="IEEG",
        )
        for section_id, values in aggregated.items()
    }


def rebuild_gubernatura_file(
    *,
    master_path: str | Path,
    ine_section_path: str | Path,
    ieeg_path: str | Path,
    output_path: str | Path,
) -> GubernaturaRebuildReport:
    """
    Genera un maestro candidato sin modificar la fuente original.

    La salida debe ser nueva. Nunca se sobrescribe el maestro ni un
    candidato previamente generado.
    """

    source_path = Path(master_path)
    candidate_path = Path(output_path)

    if not source_path.is_file():
        raise FileNotFoundError(
            f"No se encontró el maestro: {source_path}"
        )

    if (
        source_path.resolve()
        == candidate_path.resolve()
    ):
        raise ValueError(
            "La salida debe ser distinta del maestro original"
        )

    if candidate_path.exists():
        raise FileExistsError(
            f"La salida ya existe: {candidate_path}"
        )

    with source_path.open(
        "r",
        encoding="utf-8-sig",
    ) as stream:
        master_records = json.load(stream)

    if not isinstance(master_records, list):
        raise TypeError(
            "El maestro electoral debe tener raíz list"
        )

    ine_results = load_ine_section_results(
        ine_section_path
    )
    ieeg_results = load_ieeg_casilla_results(
        ieeg_path
    )

    rebuilt_records, report = (
        rebuild_gubernatura_records(
            master_records=master_records,
            ine_results=ine_results,
            ieeg_results=ieeg_results,
        )
    )

    candidate_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path = candidate_path.with_name(
        f".{candidate_path.name}.tmp"
    )

    if temporary_path.exists():
        raise FileExistsError(
            f"La salida temporal ya existe: {temporary_path}"
        )

    try:
        with temporary_path.open(
            "x",
            encoding="utf-8",
            newline="\n",
        ) as stream:
            json.dump(
                rebuilt_records,
                stream,
                ensure_ascii=False,
                indent=2,
            )
            stream.write("\n")

        os.replace(
            temporary_path,
            candidate_path,
        )
    except BaseException:
        if temporary_path.exists():
            temporary_path.unlink()

        raise

    return report
