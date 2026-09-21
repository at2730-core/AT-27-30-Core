import json
from pathlib import Path
from threading import Thread
from urllib.request import Request, urlopen

import pytest

from heyti.gateway.guanajuato_2023_http_host import (
    build_guanajuato_2023_http_host,
)


def real_source_paths() -> tuple[Path, Path]:
    repository_root = Path(__file__).resolve().parents[2]

    master_path = (
        repository_root
        / "datasets"
        / "electoral"
        / "Datos_Electoral_con_2015.json"
    )
    geometry_path = (
        repository_root
        / "datasets"
        / "spatial"
        / "secciones.geojson"
    )

    return master_path, geometry_path


def request_json(
    url,
    method="GET",
    payload=None,
    headers=None,
):
    body = (
        json.dumps(payload).encode("utf-8")
        if payload is not None
        else None
    )

    request = Request(
        url,
        data=body,
        method=method,
        headers=headers or {},
    )

    with urlopen(
        request,
        timeout=10,
    ) as response:
        return (
            response.status,
            response.headers,
            json.loads(
                response.read().decode("utf-8")
            ),
        )


def get_block(response, role):
    return next(
        block
        for block in response["blocks"]
        if block["role"] == role
    )


def test_certified_http_host_serves_real_section_truth():
    master_path, geometry_path = real_source_paths()

    host = build_guanajuato_2023_http_host(
        master_path=master_path,
        geometry_path=geometry_path,
        host="127.0.0.1",
        port=0,
    )

    assert host.gateway.is_running() is True
    assert (
        host.composition.bootstrap.session_manager.exists(
            "HEYTI-HTTP-LOCAL"
        )
        is True
    )

    thread = Thread(
        target=host.serve_forever,
        daemon=True,
    )
    thread.start()

    server_host, server_port = host.address
    base_url = f"http://{server_host}:{server_port}"

    try:
        health_status, health_headers, health = request_json(
            f"{base_url}/health",
            headers={
                "Origin": "http://localhost:5173",
                "Accept": "application/json",
            },
        )

        current_status, _, current = request_json(
            f"{base_url}/v1/sections/describe",
            method="POST",
            payload={
                "section_id": "1524",
            },
            headers={
                "Origin": "http://localhost:5173",
                "Content-Type": "application/json",
                "X-Request-ID": "REQ-HTTP-CURRENT-1524",
            },
        )

        synthetic_status, _, synthetic = request_json(
            f"{base_url}/v1/sections/describe",
            method="POST",
            payload={
                "section_id": "9001",
            },
            headers={
                "Origin": "http://localhost:5173",
                "Content-Type": "application/json",
                "X-Request-ID": "REQ-HTTP-SYNTHETIC-9001",
            },
        )
    finally:
        host.shutdown()
        thread.join(timeout=10)

    assert thread.is_alive() is False
    assert host.gateway.is_running() is False

    assert health_status == 200
    assert health["status"] == "OK"
    assert health["runtime"] == "HEYTI CORE"
    assert health_headers["Access-Control-Allow-Origin"] == (
        "http://localhost:5173"
    )

    assert current_status == 200
    assert current["contract"] == "HEYTI_RESPONSE"
    assert current["capability_id"] == "describe_section"
    assert current["status"] == "success_with_warnings"
    assert len(current["warnings"]) == 1
    assert current["warnings"][0]["code"] == (
        "PARTIAL_ELECTORAL_COVERAGE"
    )

    current_truth = get_block(
        current,
        "data_truth",
    )
    current_electoral = get_block(
        current,
        "electoral",
    )

    assert current_truth["content"]["classification"] == (
        "CURRENT_TERRITORIAL_SECTION"
    )
    assert current_truth["content"]["publication_status"] == (
        "ALLOWED"
    )

    assert current_electoral is not None
    assert current_electoral["type"] == "domain"
    assert current_electoral["content"]["section_id"] == (
        "1524"
    )
    assert current_electoral["content"][
        "coverage_scope"
    ] == "TRACKED_PARTIES_ONLY"
    assert current_electoral["content"][
        "quality_status"
    ] == "PARTIAL"

    ayuntamiento = current_electoral["content"][
        "contests"
    ]["A"]

    assert ayuntamiento["data_status"] == "ZERO_TOTAL"
    assert ayuntamiento["total_votes"] == 0.0
    assert ayuntamiento["nominal_list"] == 620.0
    assert ayuntamiento[
        "leading_tracked_party"
    ] is None
    assert "winner" not in ayuntamiento

    assert current["trace"]["request_id"] == (
        "REQ-HTTP-CURRENT-1524"
    )
    assert current["trace"]["session_id"] == (
        "HEYTI-HTTP-LOCAL"
    )
    assert current["trace"]["execution_id"].startswith("EXE-")
    assert current["trace"]["knowledge_version"] == (
        "GUANAJUATO_2023:1.0"
    )

    assert synthetic_status == 200
    assert synthetic["status"] == "success_with_warnings"
    assert len(synthetic["warnings"]) == 1
    assert synthetic["warnings"][0]["code"] == (
        "SYNTHETIC_SECTION_CANDIDATE"
    )

    synthetic_truth = get_block(
        synthetic,
        "data_truth",
    )

    assert synthetic_truth["content"]["classification"] == (
        "SYNTHETIC_CANDIDATE"
    )
    assert synthetic_truth["content"]["publication_status"] == (
        "BLOCKED"
    )
    assert synthetic["trace"]["request_id"] == (
        "REQ-HTTP-SYNTHETIC-9001"
    )
    assert synthetic["trace"]["knowledge_version"] == (
        "GUANAJUATO_2023:1.0"
    )


def test_certified_http_host_fails_closed_without_sources(
    tmp_path,
):
    with pytest.raises(FileNotFoundError):
        build_guanajuato_2023_http_host(
            master_path=tmp_path / "missing-master.json",
            geometry_path=tmp_path / "missing-geometry.geojson",
            host="127.0.0.1",
            port=0,
        )
