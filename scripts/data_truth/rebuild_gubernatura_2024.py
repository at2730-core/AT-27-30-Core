import argparse
import hashlib
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = REPOSITORY_ROOT / "src"

if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(SOURCE_ROOT),
    )

from heyti.audit.data_truth.gubernatura_2024 import (
    rebuild_gubernatura_file,
)


MASTER_SHA256 = (
    "7c0bcbfd5bdb00ac9bfafe6110cf2a916e60d68f"
    "f909773d58348e0655e945b8"
)
INE_SECTION_SHA256 = (
    "10d2b3b9201215a530ba37c1f000acceb4a25f16"
    "b40a19d18a31fe94f3294363"
)
IEEG_SHA256 = (
    "49c8a87708ef236c9782085caa189d7df4a652316"
    "ecc1c9a1400cf69e1bf7ac5"
)

INE_SOURCE_URL = "https://sicee.ine.mx/downloadzip"
IEEG_SOURCE_URL = (
    "https://computosgto2024.ieeg.mx/"
    "#/gubernatura/entidad/votos-entidad/mapa"
)

DEFAULT_MASTER_PATH = (
    REPOSITORY_ROOT
    / "datasets"
    / "electoral"
    / "Datos_Electoral_con_2015.json"
)
DEFAULT_INE_SECTION_PATH = (
    REPOSITORY_ROOT
    / "datasets"
    / "electoral"
    / "sources"
    / "official"
    / "2024"
    / "gubernatura"
    / "ine"
    / "2024_SEE_GOB_GTO_SEC.xlsx"
)
DEFAULT_IEEG_PATH = (
    REPOSITORY_ROOT
    / "datasets"
    / "electoral"
    / "sources"
    / "official"
    / "2024"
    / "gubernatura"
    / "ieeg"
    / "GTO_GUB_2024_IEEG.csv"
)
DEFAULT_OUTPUT_PATH = (
    REPOSITORY_ROOT
    / "datasets"
    / "electoral"
    / "candidates"
    / (
        "Datos_Electoral_con_2015."
        "gubernatura_2024_candidate.json"
    )
)


def sha256_file(
    path: Path,
) -> str:
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for chunk in iter(
            lambda: stream.read(1024 * 1024),
            b"",
        ):
            digest.update(chunk)

    return digest.hexdigest()


def require_sha256(
    *,
    path: Path,
    expected: str,
    source_name: str,
) -> str:
    if not path.is_file():
        raise FileNotFoundError(
            f"No se encontro {source_name}: {path}"
        )

    actual = sha256_file(path)

    if actual != expected:
        raise ValueError(
            f"SHA-256 inesperado para {source_name}: "
            f"esperado={expected}, actual={actual}"
        )

    return actual


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Genera un maestro electoral candidato con "
            "Gubernatura 2024 conciliada entre INE e IEEG. "
            "Nunca sobrescribe el maestro original."
        ),
    )
    parser.add_argument(
        "--master",
        type=Path,
        default=DEFAULT_MASTER_PATH,
        help="Ruta al maestro electoral original.",
    )
    parser.add_argument(
        "--ine-section",
        type=Path,
        default=DEFAULT_INE_SECTION_PATH,
        help="Ruta al XLSX del INE agregado por seccion.",
    )
    parser.add_argument(
        "--ieeg",
        type=Path,
        default=DEFAULT_IEEG_PATH,
        help="Ruta al CSV por casilla del IEEG.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_PATH,
        help="Ruta nueva para el maestro candidato.",
    )

    return parser


def main() -> int:
    parser = build_parser()
    arguments = parser.parse_args()

    master_path = arguments.master.resolve()
    ine_section_path = arguments.ine_section.resolve()
    ieeg_path = arguments.ieeg.resolve()
    output_path = arguments.output.resolve()

    master_hash = require_sha256(
        path=master_path,
        expected=MASTER_SHA256,
        source_name="maestro electoral",
    )
    ine_hash = require_sha256(
        path=ine_section_path,
        expected=INE_SECTION_SHA256,
        source_name="fuente INE por seccion",
    )
    ieeg_hash = require_sha256(
        path=ieeg_path,
        expected=IEEG_SHA256,
        source_name="fuente IEEG por casilla",
    )

    report = rebuild_gubernatura_file(
        master_path=master_path,
        ine_section_path=ine_section_path,
        ieeg_path=ieeg_path,
        output_path=output_path,
    )

    output_hash = sha256_file(output_path)

    print("status=SUCCESS")
    print(
        "total_master_sections="
        f"{report.total_master_sections}"
    )
    print(
        "updated_sections="
        f"{report.updated_sections}"
    )
    print(
        "preserved_sections="
        f"{report.preserved_sections}"
    )
    print(
        "verified_sections="
        f"{report.verified_sections}"
    )
    print(f"master_sha256={master_hash}")
    print(f"ine_section_sha256={ine_hash}")
    print(f"ieeg_sha256={ieeg_hash}")
    print(f"output_sha256={output_hash}")
    print(f"output_path={output_path}")
    print(f"ine_source_url={INE_SOURCE_URL}")
    print(f"ieeg_source_url={IEEG_SOURCE_URL}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())