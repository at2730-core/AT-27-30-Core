"""Coteja filas SEC=0 de Guanajuato contra CAS=0 por identidad y columna literal.
No modifica fuentes ni PostgreSQL. Verifica hashes del manifiesto antes de leer.
"""
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv)>1 else Path.cwd()
MANIFEST = ROOT / 'HEYTI_Manifiesto_23_Series_2018_2024_v0_1.json'
OUT = ROOT / 'HEYTI_Cotejo_Seccion_Cero_Casillas_v0_1.json'
IDENTITY = ('ID_ESTADO','ID_DISTRITO_FEDERAL','ID_DISTRITO_LOCAL','ID_MUNICIPIO','MUNICIPIO')
NON_VOTE = set(IDENTITY)|{'CIRCUNSCRIPCION','NOMBRE_ESTADO','CABECERA_DISTRITAL_FEDERAL',
    'CABECERA_DISTRITAL_LOCAL','CABECERA_DISTRITAL','SECCION','CASILLAS','ACTAS_CASILLA-MEC'}

def read(z, name):
    data=z.read(name)
    try: text=data.decode('utf-8-sig')
    except UnicodeDecodeError: text=data.removeprefix(b'\xef\xbb\xbf').decode('cp1252')
    return data, csv.DictReader(io.StringIO(text,newline=''))

def identity(row): return tuple(row.get(k,'').strip() for k in IDENTITY)
def gto_zero(row): return row.get('ID_ESTADO','').strip() in ('11','011') and row.get('SECCION','').strip()=='0'
def number(raw):
    raw=raw.strip()
    return int(raw) if raw.isdecimal() else None

def main():
    m=json.loads(MANIFEST.read_text(encoding='utf-8'))
    report=[]
    for release in m['releases']:
        p=ROOT/release['zip_name']
        if hashlib.sha256(p.read_bytes()).hexdigest()!=release['outer_zip_sha256']:
            raise ValueError('ZIP cambió: '+str(p))
        with zipfile.ZipFile(p) as z:
            for s in release['series']:
                if not s['zero_section_rows']:continue
                b, sec=read(z,s['member_path'])
                if hashlib.sha256(b).hexdigest()!=s['member_sha256']:
                    raise ValueError('CSV cambió: '+s['member_path'])
                cas_basename=s['member_path'].rsplit('/',1)[-1].replace('_SEC.csv','_CAS.csv')
                matches=[n for n in z.namelist() if n.endswith('/'+cas_basename)]
                if len(matches)!=1: raise ValueError('CAS ambiguo/ausente: '+cas_basename)
                _, cas=read(z,matches[0])
                sec_rows=[x for x in sec if gto_zero(x)]
                cas_rows=collections.defaultdict(list)
                for x in cas:
                    if gto_zero(x):cas_rows[identity(x)].append(x)
                cols=[k for k in sec.fieldnames if k in cas.fieldnames and k not in NON_VOTE]
                for ordinal, row in enumerate(sec_rows,1):
                    key=identity(row)
                    associated=cas_rows.get(key,[])
                    differences=[];indeterminate=[];blank_both=[]; compared=0
                    for col in cols:
                        published=number(row[col])
                        values=[number(x[col]) for x in associated]
                        if associated and not row[col].strip() and all(not x[col].strip() for x in associated):
                            blank_both.append(col)
                            continue
                        if published is None or not associated or any(v is None for v in values):
                            indeterminate.append({'column':col,'published':row[col],
                                'cas_values':[x[col] for x in associated]})
                            continue
                        computed=sum(values);compared+=1
                        if computed!=published:
                            differences.append({'column':col,'section':published,'sum_casilla':computed,
                                'delta':published-computed})
                    report.append({'year':s['election_year'],'type':s['election_type'],
                        'modality':s['modality'],'section_member':s['member_path'],
                        'casilla_member':matches[0],'ordinal_within_section_zero':ordinal,
                        'identity':dict(zip(IDENTITY,key)), 'casilla_count':len(associated),
                        'compared_fields':compared,'differences':differences,
                        'indeterminate_fields':indeterminate,'blank_both_fields':blank_both})
    if len(report)!=137: raise ValueError('Conteo de filas SEC=0 distinto de 137')
    OUT.write_text(json.dumps({'schema_version':'0.1','rows':len(report),'results':report},
        indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    print('filas',len(report),'sin casilla',sum(not r['casilla_count'] for r in report),
          'diferencias',sum(len(r['differences']) for r in report),
          'indeterminados',sum(len(r['indeterminate_fields']) for r in report),
          'vacíos_literales_coincidentes',sum(len(r['blank_both_fields']) for r in report))
    for r in report:
        if r['differences'] or r['indeterminate_fields']:
            print(r['year'],r['type'],r['modality'],r['identity'],
                  'cas',r['casilla_count'],'diff',len(r['differences']),
                  'unknown',len(r['indeterminate_fields']),
                  'fields',[x['column'] for x in r['differences'][:5]])

if __name__=='__main__':main()
