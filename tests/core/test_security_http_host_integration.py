import json
from pathlib import Path
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from heyti.gateway.guanajuato_2023_http_host import (
    build_guanajuato_2023_http_host,
)
from heyti.security.composition import (
    SecurityComposition,
)
from heyti.security.http_application import (
    SecurityHttpApplication,
)


def real_source_paths():
    repository_root = (
        Path(__file__).resolve().parents[2]
    )

    return (
        repository_root
        / "datasets"
        / "electoral"
        / "Datos_Electoral_con_2015.json",
        repository_root
        / "datasets"
        / "spatial"
        / "secciones.geojson",
    )


def forbidden_connection():
    raise AssertionError(
        "La ruta de sesion no debe consultar PostgreSQL"
    )


def request_json(url, headers=None):
    request = Request(
        url,
        method="GET",
        headers=headers or {},
    )

    try:
        response = urlopen(
            request,
            timeout=10,
        )
    except HTTPError as exc:
        response = exc

    return (
        response.status,
        response.headers,
        json.loads(
            response.read().decode("utf-8")
        ),
    )


def test_real_host_exposes_security_composition():
    master_path, geometry_path = (
        real_source_paths()
    )

    host = build_guanajuato_2023_http_host(
        master_path=master_path,
        geometry_path=geometry_path,
        host="127.0.0.1",
        port=0,
        field_connection_factory=(
            forbidden_connection
        ),
    )

    assert isinstance(
        host.security_composition,
        SecurityComposition,
    )
    assert isinstance(
        host.security_application,
        SecurityHttpApplication,
    )
    assert (
        host.security_composition
        .session_service
        ._session_manager
        is host.composition
        .bootstrap
        .session_manager
    )

    thread = Thread(
        target=host.serve_forever,
        daemon=True,
    )
    thread.start()

    server_host, server_port = host.address
    base_url = (
        f"http://{server_host}:{server_port}"
    )

    try:
        status, headers, payload = request_json(
            f"{base_url}/v1/auth/session",
            headers={
                "Origin": "http://localhost:5173",
            },
        )
    finally:
        host.shutdown()
        thread.join(timeout=10)

    assert thread.is_alive() is False
    assert host.gateway.is_running() is False
    assert status == 401
    assert payload == {
        "error": {
            "code": "AUTHENTICATION_REQUIRED",
            "message": (
                "Se requiere una sesion autenticada."
            ),
        }
    }
    assert headers[
        "Access-Control-Allow-Origin"
    ] == "http://localhost:5173"
