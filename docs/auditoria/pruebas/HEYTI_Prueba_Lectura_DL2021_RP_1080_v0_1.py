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
series = SeriesKey(2021, "DL", "RP")
releases = [r for r in registry.releases if r.series == series]
assert len(releases) == 1, "Serie ausente o ambigua en la matriz"
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
            release.section_sha256, 2021, "DL", "RP",
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
    "Ensayo local: correspondencia por hashes SEC/ZIP y serie; no certifica fecha",
)
repository = StagingElectoralRepository(registry, connect, [binding])
reader = VersionedElectoralSource(registry, repository)

request = ReadRequest(
    series, "ORDINARY_SECTION", "SEC:1080",
    purpose="AUDIT", release_id=release.release_id,
)
response = reader.read(request)
assert response["status"] == "AUDIT_SOURCE_AS_PUBLISHED", response["status"]
data = response["data"]
assert data["result"]["total_votes"] is None, "El total perdió su NULL"

print("Base:", database)
print("Identidad:", data["identity"]["unit_key"], data["identity"]["modality"])
print("Total:", data["result"]["total_votes"])
print("Literal del total:", repr(data["result"]["total_raw"]))
print("Causa:", data["result"]["total_missing_cause"])
print("Opciones:", len(data["result"]["options"]))
print("Casillas vinculadas:", len(data["cas_evidence"]))
print("Fecha de corte:", response["provenance"]["cut_date_status"])

blocked = reader.read(ReadRequest(series, "ORDINARY_SECTION", "SEC:1080"))
assert blocked["status"] == "NO_RELEASE_SELECTED"
print("Presentación sin selección:", blocked["status"])
print("LECTURA POSTGRESQL DL2021 RP 1080: OK")
