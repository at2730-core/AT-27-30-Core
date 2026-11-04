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
cases = [
    ("DL", "MR", "1080", 0),
    ("DL", "RP", "1080", None),
    ("A", "UNICA", "163", None),
    ("A", "UNICA", "2541", None),
    ("DF", "MR", "218", 614),
    ("DF", "RP", "218", "INSPECT"),
]

for election_type, modality, section, expected in cases:
    series = SeriesKey(2021, election_type, modality)
    releases = [r for r in registry.releases if r.series == series]
    assert len(releases) == 1, "Serie ausente o ambigua"
    release = releases[0]

    connection = connect()
    try:
        with connection.cursor() as cursor:
            cursor.execute("BEGIN TRANSACTION READ ONLY")
            cursor.execute("""
                SELECT DISTINCT sr.cut_label
                FROM electoral_stage.source_release sr
                JOIN electoral_stage.source_member sm
                  ON sm.release_id = sr.release_id
                JOIN electoral_stage.election_series es
                  ON es.member_id = sm.member_id
                WHERE sr.outer_zip_sha256 = %s
                  AND sm.member_path = %s AND sm.member_sha256 = %s
                  AND es.election_year = %s
                  AND es.election_type = %s AND es.modality = %s
                  AND es.geography = 'GTO'
                  AND es.aggregation_level = 'SECTION'
                  AND es.judicial_cut = 'SOURCE_AS_PUBLISHED'
            """, (
                release.zip_sha256, release.section_member,
                release.section_sha256, 2021, election_type, modality,
            ))
            cuts = cursor.fetchall()
            assert len(cuts) == 1, "Corte staging ausente o ambiguo"
    finally:
        try:
            connection.rollback()
        finally:
            connection.close()

    binding = StagingCutBinding(
        release.release_id, cuts[0][0],
        "Ensayo local por hashes y serie; no certifica fecha ni corte judicial",
    )
    repository = StagingElectoralRepository(registry, connect, [binding])
    reader = VersionedElectoralSource(registry, repository)
    unit_key = "SEC:" + section

    response = reader.read(ReadRequest(
        series, "ORDINARY_SECTION", unit_key,
        purpose="AUDIT", release_id=release.release_id,
    ))
    assert response["status"] == "AUDIT_SOURCE_AS_PUBLISHED", response["status"]
    data = response["data"]
    result = data["result"]

    if expected != "INSPECT":
        assert result["total_votes"] == expected, (
            election_type, modality, section, result["total_votes"], expected
        )

    # Comprueba preservación frente a la fila SEC cruda.
    raw_total = data["sec_source"]["raw_cells"]["TOTAL_VOTOS"]
    assert result["total_raw"] == raw_total
    if raw_total == "":
        assert result["total_votes"] is None
        assert result["total_missing_cause"]
    else:
        assert result["total_votes"] == int(raw_total)

    assert data["identity"]["modality"] == modality
    assert response["provenance"]["release_id"] == release.release_id
    assert reader.read(ReadRequest(
        series, "ORDINARY_SECTION", unit_key,
    ))["status"] == "NO_RELEASE_SELECTED"

    print(
        election_type, modality, unit_key,
        "| total:", result["total_votes"],
        "| literal:", repr(result["total_raw"]),
        "| causa:", result["total_missing_cause"],
        "| opciones:", len(result["options"]),
        "| CAS:", len(data["cas_evidence"]),
        "| presentación: NO_RELEASE_SELECTED",
    )

print("LECTURA POSTGRESQL: 6 CASOS 2021 OK")
print("DF RP 218: cifra inspeccionada y cotejada con fila cruda; sin adjudicación externa.")
