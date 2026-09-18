import argparse
from pathlib import Path
from typing import Sequence

from heyti.gateway.guanajuato_2023_http_host import (
    build_guanajuato_2023_http_host,
)


DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765


def repository_root() -> Path:
    """Obtiene la raíz del repositorio desde este módulo."""

    return Path(__file__).resolve().parents[3]


def default_master_path() -> Path:
    """Devuelve la ruta oficial del maestro electoral."""

    return (
        repository_root()
        / "datasets"
        / "electoral"
        / "Datos_Electoral_con_2015.json"
    )


def default_geometry_path() -> Path:
    """Devuelve la ruta oficial de la geometría seccional."""

    return (
        repository_root()
        / "datasets"
        / "spatial"
        / "secciones.geojson"
    )


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser del comando local."""

    parser = argparse.ArgumentParser(
        prog="heyti-gateway",
        description=(
            "Inicia el Gateway HTTP local certificado "
            "de HEYTI-CORE."
        ),
    )
    parser.add_argument(
        "--master",
        type=Path,
        default=default_master_path(),
        help="Ruta al maestro electoral JSON.",
    )
    parser.add_argument(
        "--geometry",
        type=Path,
        default=default_geometry_path(),
        help="Ruta al GeoJSON de secciones.",
    )
    parser.add_argument(
        "--host",
        default=DEFAULT_HOST,
        help="Interfaz local de escucha.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help="Puerto HTTP local.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help=(
            "Valida fuentes y composición sin dejar "
            "el servidor ejecutándose."
        ),
    )

    return parser


def main(
    argv: Sequence[str] | None = None,
) -> int:
    """Ejecuta el host HTTP local de HEYTI."""

    parser = build_parser()
    arguments = parser.parse_args(argv)

    if not 0 <= arguments.port <= 65535:
        parser.error(
            "--port debe estar entre 0 y 65535"
        )

    effective_port = (
        0
        if arguments.check
        else arguments.port
    )

    try:
        runtime_host = build_guanajuato_2023_http_host(
            master_path=arguments.master,
            geometry_path=arguments.geometry,
            host=arguments.host,
            port=effective_port,
        )
    except (
        FileNotFoundError,
        OSError,
        TypeError,
        ValueError,
    ) as exc:
        parser.exit(
            status=1,
            message=f"HEYTI-CORE no pudo iniciar: {exc}\n",
        )

    address, port = runtime_host.address

    if arguments.check:
        runtime_host.server.server_close()
        runtime_host.gateway.stop()

        print(
            "HEYTI-CORE VALIDATION OK "
            f"{address}:{port}"
        )
        return 0

    print(
        "HEYTI-CORE READY "
        f"http://{address}:{port}"
    )
    print(
        "Presiona Ctrl+C para detener el servidor."
    )

    try:
        runtime_host.serve_forever()
    except KeyboardInterrupt:
        print("\nHEYTI-CORE STOPPED")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
