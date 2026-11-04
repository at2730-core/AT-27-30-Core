"""Ensayo del adaptador en clon temporal; no habilita presentación."""
import getpass
import hashlib
from pathlib import Path
import uuid
import psycopg2
from psycopg2 import sql
from heyti.capabilities.describe_section.versioned_electoral_source import (
    ReleaseRegistry, SeriesKey, ReadRequest, VersionedElectoralSource,
)
from heyti.capabilities.describe_section.staging_electoral_repository import (
    StagingCutBinding, StagingElectoralRepository,
)

ROOT = Path(__file__).resolve().parents[3]
SOURCE = "heyti_cas_full_probe_d12d6718adb8"
CLONE = "heyti_a2024_reader_probe_" + uuid.uuid4().hex[:12]
QUERY = Path(__file__).with_name("HEYTI_Ensayo_Incidencia_A2024_ROLLBACK_v0_1.sql")
EXPECTED_cf5948579740b676f069fe22e0727d1dc028a69b300129677f2c905193720395 = "cf5948579740b676f069fe22e0727d1dc028a69b300129677f2c905193720395"
assert hashlib.sha256(QUERY.read_bytes()).hexdigest() == EXPECTED_cf5948579740b676f069fe22e0727d1dc028a69b300129677f2c905193720395, "SQL distinto del ensayo validado"
password = getpass.getpass("Contraseña PostgreSQL: ")

def connect(database):
    c = psycopg2.connect(host="localhost", port=5432, user="postgres", dbname=database, password=password)
    c.autocommit = True
    return c

def source_counts():
    c = connect(SOURCE)
    try:
        with c.cursor() as cur:
            cur.execute("BEGIN TRANSACTION READ ONLY")
            cur.execute("SELECT (SELECT count(*) FROM electoral_stage.audit_run), (SELECT count(*) FROM electoral_stage.reconciliation_issue)")
            return cur.fetchone()
    finally:
        c.rollback()
        c.close()

baseline = source_counts()
registry = ReleaseRegistry.from_matrix(ROOT / "docs/auditoria/HEYTI_Matriz_Seleccion_Cortes_23_Series_v0_1.csv")
admin = connect("postgres")
created = False
try:
    with admin.cursor() as cur:
        cur.execute(sql.SQL("CREATE DATABASE {} TEMPLATE {}").format(sql.Identifier(CLONE), sql.Identifier(SOURCE)))
    created = True
    print("Copia temporal:", CLONE)
    trial = QUERY.read_text(encoding="utf-8")
    guard = "current_database() <> '" + SOURCE + "'"
    assert trial.count(guard) == 1
    assert trial.count("ROLLBACK;") == 1
    trial = trial.split("ROLLBACK;", 1)[0].replace(guard, "current_database() <> '" + CLONE + "'")
    c = connect(CLONE)
    try:
        with c.cursor() as cur:
            cur.execute(trial)
            cur.execute("COMMIT")
    finally:
        c.rollback()
        c.close()

    cases = [("A", "UNICA"), ("DL", "MR"), ("DL", "RP"), ("G", "UNICA")]
    for typ, modality in cases:
        series = SeriesKey(2024, typ, modality)
        releases = [r for r in registry.releases if r.series == series]
        assert len(releases) == 1
        release = releases[0]
        assert release.zip_sha256 == "13fe6a2ddb432922bddc9090f08eb0e558aeb3094ef1ba763b78d789b3d55e69"
        repository = StagingElectoralRepository(registry, lambda: connect(CLONE), [StagingCutBinding(
            release.release_id, "SOURCE_AS_PUBLISHED_UNVERIFIED_DATE", "Temporary clone probe; not cut certification",
        )])
        request = ReadRequest(series, "ORDINARY_SECTION", "SEC:156", purpose="AUDIT", release_id=release.release_id)
        snapshot = repository.get_snapshot(release.release_id, request)
        assert snapshot is not None
        conflicts = [i for i in snapshot["issues"] if i.get("code") == "JUDICIAL_CUT_CONFLICT"]
        assert len(conflicts) == (1 if typ == "A" else 0), conflicts
        reader = VersionedElectoralSource(registry, repository)
        response = reader.read(request)
        assert response["status"] == "AUDIT_SOURCE_AS_PUBLISHED", response["status"]
        assert response["data"] is not None
        if typ == "A":
            assert any(i.get("code") == "JUDICIAL_CUT_CONFLICT" for i in response["data"]["issues"])
        for metric in ("RESULT", "NOMINAL_LIST"):
            blocked = reader.read(ReadRequest(series, "ORDINARY_SECTION", "SEC:156", metric_scope=metric))
            assert blocked["status"] == "NO_RELEASE_SELECTED" and blocked["data"] is None
        print(typ, modality, "| conflictos DB:", len(conflicts), "| auditoría: OK | presentación: NO_RELEASE_SELECTED")
    print("ADAPTADOR A2024: incidencia visible, auditoría preservada, DL/G sin esta incidencia: OK")
    print("Alcance: no se ensayó presentación con corte certificado ni política aprobada.")
finally:
    try:
        if created:
            with admin.cursor() as cur:
                cur.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(CLONE)))
            print("Copia temporal eliminada:", CLONE)
    finally:
        admin.close()
    assert source_counts() == baseline, "Cambió el conteo de auditorías/incidencias de la base original"
    print("Base original: conteos de auditorías e incidencias conservados.")
