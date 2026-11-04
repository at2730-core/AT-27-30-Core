"""Read-only PostgreSQL probe: all 106 units share one exported snapshot."""
from pathlib import Path
import getpass
import json
import psycopg2
from psycopg2 import sql
from heyti.capabilities.describe_section.judicial_derived_audit_source import JudicialDerivedAuditSource, digest
from heyti.capabilities.describe_section.versioned_electoral_source import ReleaseRegistry, SeriesKey, ReadRequest, VersionedElectoralSource
from heyti.capabilities.describe_section.staging_electoral_repository import StagingElectoralRepository, StagingCutBinding

ROOT=Path(__file__).resolve().parents[3]
DATABASE='heyti_cas_full_probe_d12d6718adb8'
MANIFEST_HASH='60664fdf7a5c30ba7cd90ccb0ce7eb41b6b8b0630877e46394bb0e2c5db82712'
manifest=json.loads((ROOT/'docs/auditoria/HEYTI_Manifiesto_Candidato_SanMiguel_A2024_v0_1.json').read_text(encoding='utf-8-sig'))
assert digest(manifest)==MANIFEST_HASH, 'Manifiesto distinto del validado'
password=getpass.getpass('Contraseña PostgreSQL: ')
def connect():
    c=psycopg2.connect(host='localhost',port=5432,user='postgres',dbname=DATABASE,password=password)
    c.autocommit=True
    return c

class SnapshotCursor:
    def __init__(self,cursor,snapshot): self.cursor,self.snapshot=cursor,snapshot
    def execute(self,query,params=None):
        self.cursor.execute(query,params)
        if query=='BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY':
            self.cursor.execute(sql.SQL('SET TRANSACTION SNAPSHOT {}').format(sql.Literal(self.snapshot)))
    def fetchall(self): return self.cursor.fetchall()
    def close(self): self.cursor.close()
class SnapshotConnection:
    def __init__(self,connection,snapshot):self.connection,self.snapshot=connection,snapshot
    def cursor(self):return SnapshotCursor(self.connection.cursor(),self.snapshot)
    def rollback(self):self.connection.rollback()
    def close(self):self.connection.close()

series=SeriesKey(2024,'A','UNICA')
registry=ReleaseRegistry.from_matrix(ROOT/'docs/auditoria/HEYTI_Matriz_Seleccion_Cortes_23_Series_v0_1.csv')
releases=[r for r in registry.releases if r.series==series]
assert len(releases)==1
release=releases[0]
assert all(release.provenance()[k]==v for k,v in manifest['source'].items())
exporter=connect()
try:
    with exporter.cursor() as cur:
        cur.execute('BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY')
        cur.execute('SELECT pg_export_snapshot()')
        snapshot_id=cur.fetchone()[0]
        cur.execute("""SELECT es.series_id,sr.cut_label
          FROM electoral_stage.source_release sr
          JOIN electoral_stage.source_member sm ON sm.release_id=sr.release_id
          JOIN electoral_stage.election_series es ON es.member_id=sm.member_id
          WHERE sr.outer_zip_sha256=%s AND sm.member_path=%s AND sm.member_sha256=%s
          AND es.election_year=2024 AND es.election_type='A' AND es.modality='UNICA'
          AND es.geography='GTO' AND es.aggregation_level='SECTION'
          AND es.judicial_cut='SOURCE_AS_PUBLISHED'""",
          (release.zip_sha256,release.section_member,release.section_sha256))
        matches=cur.fetchall();assert len(matches)==1,'Serie ausente o ambigua'
        series_id,cut=matches[0]
        cur.execute("SELECT unit_kind,unit_key FROM electoral_stage.computation_unit WHERE series_id=%s AND municipality_code='3' ORDER BY unit_key",(series_id,))
        units=cur.fetchall();assert len(units)==106
    repository=StagingElectoralRepository(registry,lambda:SnapshotConnection(connect(),snapshot_id),[StagingCutBinding(release.release_id,cut,'Read-only consistent snapshot; not certification')])
    reader=VersionedElectoralSource(registry,repository)
    responses=[]
    for kind,key in units:
        response=reader.read(ReadRequest(series,kind,key,purpose='AUDIT',release_id=release.release_id))
        assert response['status']=='AUDIT_SOURCE_AS_PUBLISHED',(key,response['status'])
        responses.append(response)
    candidate=JudicialDerivedAuditSource(manifest,MANIFEST_HASH,responses)
    print('Base:',DATABASE)
    print('Candidato:',candidate.candidate_id)
    totals=[];deltas=[]
    for kind,key in units:
        response=candidate.read(ReadRequest(series,kind,key,purpose='AUDIT',release_id=release.release_id),candidate_id=candidate.candidate_id)
        assert response['status']=='AUDIT_JUDICIAL_DERIVED_CANDIDATE'
        data=response['data'];totals.append(data['derived_result']['total_votes'])
        if data['delta_total']:
            print(key,'| base:',data['base_snapshot']['result']['total_votes'],'| delta:',data['delta_total'],'| derivado:',data['derived_result']['total_votes'])
            deltas.append(key)
        else:
            assert data['base_vector']==[o['votes'] for o in data['derived_result']['options']]
    assert sum(totals)==76757 and len(deltas)==4
    for metric in ['RESULT','NOMINAL_LIST']:
        out=candidate.read(ReadRequest(series,'ORDINARY_SECTION','SEC:156',metric_scope=metric),candidate_id=candidate.candidate_id)
        assert out['status']=='NO_RELEASE_SELECTED' and out['data'] is None
        print('Presentación',metric+':',out['status'])
    for req,cid,status in [
        (ReadRequest(series,'ORDINARY_SECTION','SEC:156',purpose='AUDIT'),'wrong','DERIVED_IDENTITY_MISMATCH'),
        (ReadRequest(SeriesKey(2024,'DL','MR'),'ORDINARY_SECTION','SEC:156',purpose='AUDIT'),candidate.candidate_id,'DERIVED_IDENTITY_MISMATCH'),
        (ReadRequest(series,'ORDINARY_SECTION','SEC:99999',purpose='AUDIT'),candidate.candidate_id,'UNIT_OUTSIDE_DERIVED_SCOPE')]:
        assert candidate.read(req,candidate_id=cid)['status']==status
    print('CANDIDATO JUDICIAL: 106 unidades, 1802 celdas, 76757 votos; 102 unidades sin delta: OK')
    print('Originales, marcas ANULADA, LN e identidad especial preservados en base_snapshot.')
    print('Sin escritura DB ni selección/certificación ni conexión del candidato al runtime.')
finally:
    exporter.rollback();exporter.close()
    print('Snapshot de lectura cerrado.')
