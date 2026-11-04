import getpass
from pathlib import Path
import psycopg2

from heyti.capabilities.describe_section.versioned_electoral_source import (
    ReleaseRegistry, SeriesKey, ReadRequest, VersionedElectoralSource,
)
from heyti.capabilities.describe_section.staging_electoral_repository import (
    StagingCutBinding, StagingElectoralRepository,
)

database = "heyti_cas_full_probe_d12d6718adb8"
password = getpass.getpass("Contraseña PostgreSQL: ")

def connect():
    connection = psycopg2.connect(
        host="localhost", port=5432, user="postgres",
        dbname=database, password=password,
    )
    connection.autocommit = True
    return connection

registry = ReleaseRegistry.from_matrix(
    Path("docs/auditoria/HEYTI_Matriz_Seleccion_Cortes_23_Series_v0_1.csv")
)
series = SeriesKey(2024, "P", "UNICA")
releases = [r for r in registry.releases if r.series == series]
assert len(releases) == 1, "Serie ausente o ambigua"
release = releases[0]

connection = connect()
try:
    with connection.cursor() as cursor:
        cursor.execute("BEGIN TRANSACTION READ ONLY")
        cursor.execute("""
            SELECT DISTINCT sr.cut_label, es.series_id
            FROM electoral_stage.source_release sr
            JOIN electoral_stage.source_member sm ON sm.release_id=sr.release_id
            JOIN electoral_stage.election_series es ON es.member_id=sm.member_id
            WHERE sr.outer_zip_sha256=%s
              AND sm.member_path=%s AND sm.member_sha256=%s
              AND es.election_year=2024 AND es.election_type='P'
              AND es.modality='UNICA' AND es.geography='GTO'
              AND es.aggregation_level='SECTION'
              AND es.judicial_cut='SOURCE_AS_PUBLISHED'
        """, (release.zip_sha256, release.section_member, release.section_sha256))
        matches = cursor.fetchall()
        assert len(matches) == 1, "Corte o serie staging ausente/ambiguo"
        cut, series_id = matches[0]

        cursor.execute("""
            SELECT unit_kind, unit_key
            FROM electoral_stage.computation_unit
            WHERE series_id=%s AND section_code='0'
            ORDER BY unit_key
        """, (series_id,))
        specials = cursor.fetchall()
        assert len(specials) == 1, "Se esperaba una unidad SEC0 en P2024"
finally:
    try:
        connection.rollback()
    finally:
        connection.close()

binding = StagingCutBinding(
    release.release_id, cut,
    "Ensayo local por hashes y serie; no certifica fecha ni corte judicial",
)
reader = VersionedElectoralSource(
    registry, StagingElectoralRepository(registry, connect, [binding]),
)

cases = [
    ("ORDINARY_SECTION", "SEC:1150"),
    ("ORDINARY_SECTION", "SEC:343"),
    specials[0],
]

for kind, key in cases:
    response = reader.read(ReadRequest(
        series, kind, key, purpose="AUDIT", release_id=release.release_id,
    ))
    assert response["status"] == "AUDIT_SOURCE_AS_PUBLISHED", response["status"]
    data = response["data"]
    identity = data["identity"]
    result = data["result"]

    assert identity["unit_kind"] == kind
    assert identity["unit_key"] == key
    raw_total = data["sec_source"]["raw_cells"]["TOTAL_VOTOS"]
    assert result["total_raw"] == raw_total
    assert result["total_votes"] == (None if raw_total == "" else int(raw_total))

    if key == "SEC:1150":
        assert result["total_votes"] == 1596
        assert result["nominal_list"] == 2448
        options = {o["raw_column"]: o["votes"] for o in result["options"]}
        for party, expected in {"PAN": 1246, "PRI": 51, "PVEM": 7, "MORENA": 152}.items():
            assert options.get(party) == expected, (party, options.get(party), expected)
        print("P2024 1150: total 1596, LN 2448 y cuatro columnas cotejadas: OK")

    if key == "SEC:343":
        assert identity["section_literal"] == "343"
        print("Sección 343: identidad original conservada; genealogía no certificada.")

    if key == specials[0][1]:
        assert identity["section_literal"] == "0"
        assert kind != "ORDINARY_SECTION"
        assert identity["current_section_fk"] is None
        print("SEC0: identidad especial conservada, sin FK ordinaria: OK")

    assert reader.read(ReadRequest(
        series, kind, key,
    ))["status"] == "NO_RELEASE_SELECTED"

    print(
        "Identidad:", kind, key,
        "| total:", result["total_votes"],
        "| LN:", result["nominal_list"],
        "| opciones:", len(result["options"]),
        "| CAS:", len(data["cas_evidence"]),
        "| presentación: NO_RELEASE_SELECTED",
    )

print("LECTURA POSTGRESQL P2024 E IDENTIDADES: 3 CASOS OK")
