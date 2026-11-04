"""Cotejo de columnas literales SEC/CAS de GTO; sólo lee ZIP oficiales."""
import collections
import csv
import hashlib
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path(__file__).resolve().parent
MANIFEST = ROOT / 'HEYTI_Manifiesto_23_Series_2018_2024_v0_1.json'
OUT = ROOT / 'HEYTI_Cotejo_Secciones_Casillas_23_Series_v0_1.json'
EXCLUDE = {'CASILLAS', 'ACTAS_CASILLA-MEC', 'NUM_VOTOS_VALIDOS'}


def reader(data):
    try:
        decoded = data.decode('utf-8-sig')
    except UnicodeDecodeError:
        decoded = data.removeprefix(b'\xef\xbb\xbf').decode('cp1252')
    return csv.DictReader(io.StringIO(decoded, newline=''))


def parse(value):
    value = value.strip()
    return int(value) if value.isdecimal() else None


def main():
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    results = []
    for release in manifest['releases']:
        path = ROOT / release['zip_name']
        if hashlib.sha256(path.read_bytes()).hexdigest() != release['outer_zip_sha256']:
            raise ValueError(f'Hash ZIP no coincide: {path}')
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            for series in release['series']:
                sec_name = series['member_path']
                sec_bytes = z.read(sec_name)
                if hashlib.sha256(sec_bytes).hexdigest() != series['member_sha256']:
                    raise ValueError(f'Hash SEC no coincide: {sec_name}')
                suffix = sec_name.rsplit('/', 1)[-1].replace('_SEC.csv', '_CAS.csv')
                candidates = [n for n in names if n.endswith('/' + suffix)]
                if len(candidates) != 1:
                    raise ValueError(f'CAS ausente o ambiguo: {suffix}')
                cas_name = candidates[0]
                sec, cas = reader(sec_bytes), reader(z.read(cas_name))
                key_cols = [c for c in sec.fieldnames if c in cas.fieldnames
                            and (c.startswith('ID_') or c == 'SECCION')]
                if 'SECCION' not in key_cols or 'ID_ESTADO' not in key_cols:
                    raise ValueError(f'Identidad incompleta: {sec_name}')
                vote_cols = [c for c in sec.fieldnames if c in cas.fieldnames
                             and c not in EXCLUDE and c not in key_cols
                             and c not in {'CIRCUNSCRIPCION', 'NOMBRE_ESTADO', 'MUNICIPIO'}
                             and not c.startswith('CABECERA_')]
                if 'TOTAL_VOTOS' not in vote_cols:
                    raise ValueError(f'Falta TOTAL_VOTOS común: {sec_name}')
                # Una sección ordinaria es única por entidad; SEC=0 requiere todos
                # los identificadores, pues hay varias unidades especiales.
                def key(row):
                    basic = (row['ID_ESTADO'].strip(), row['SECCION'].strip())
                    return basic if basic[1] != '0' else basic + tuple(
                        row[c].strip() for c in key_cols if c not in ('ID_ESTADO', 'SECCION'))
                cas_groups = collections.defaultdict(list)
                cas_rows = 0
                for row in cas:
                    if row['ID_ESTADO'].strip() in ('11', '011'):
                        cas_groups[key(row)].append(row)
                        cas_rows += 1
                seen = set()
                counts = collections.Counter()
                examples = []
                discrepancies = []
                for row in sec:
                    if row['ID_ESTADO'].strip() not in ('11', '011'):
                        continue
                    identity = key(row)
                    counts['sections'] += 1
                    if identity in seen:
                        counts['duplicate_sections'] += 1
                    seen.add(identity)
                    group = cas_groups.get(identity, [])
                    if not group:
                        counts['sections_without_casilla'] += 1
                        if len(examples) < 30:
                            examples.append({'kind': 'no_casilla', 'identity': identity})
                    if row['SECCION'].strip() == '0':
                        counts['section_zero'] += 1
                    for col in vote_cols:
                        section_value = parse(row[col])
                        raw_cas = [r[col].strip() for r in group]
                        numeric_cas = [parse(v) for v in raw_cas]
                        if group and not row[col].strip() and all(not v for v in raw_cas):
                            counts['both_literal_blank'] += 1
                        elif section_value is None or not group or any(v is None for v in numeric_cas):
                            counts['indeterminate_cells'] += 1
                            if len(examples) < 30:
                                examples.append({'kind': 'indeterminate', 'identity': identity,
                                                 'column': col, 'section': row[col],
                                                 'casilla_values': raw_cas[:8]})
                        else:
                            counts['numeric_cells'] += 1
                            total = sum(numeric_cas)
                            if total != section_value:
                                counts['differences'] += 1
                                if col == 'TOTAL_VOTOS':
                                    counts['total_differences'] += 1
                                discrepancies.append({'identity': identity, 'column': col,
                                                      'section': section_value, 'casilla_sum': total,
                                                      'delta': section_value-total,
                                                      'casillas': [
                                                          {'tipo': r.get('TIPO_CASILLA', ''),
                                                           'id': r.get('ID_CASILLA', ''),
                                                           'estatus': r.get('ESTATUS_ACTA', ''),
                                                           'tribunal': r.get('TRIBUNAL', ''),
                                                           'juicio': r.get('JUICIO', ''),
                                                           'observaciones': r.get('OBSERVACIONES', ''),
                                                           'valor': r[col]}
                                                          for r in group]})
                                if len(examples) < 30:
                                    examples.append({'kind': 'difference', 'identity': identity,
                                                     'column': col, 'section': section_value,
                                                     'casilla_sum': total, 'delta': section_value-total})
                unmatched = set(cas_groups) - seen
                counts['unmatched_casilla_groups'] = len(unmatched)
                counts['unmatched_casilla_rows'] = sum(len(cas_groups[k]) for k in unmatched)
                counts['casilla_rows'] = cas_rows
                counts['distinct_sections'] = len(seen)
                results.append({'year': series['election_year'], 'type': series['election_type'],
                                'modality': series['modality'], 'zip_name': release['zip_name'],
                                'sec_member': sec_name, 'cas_member': cas_name,
                                'key_columns': key_cols, 'compared_columns': vote_cols,
                                'counts': dict(counts), 'examples': examples,
                                'discrepancies': discrepancies})
                print(series['election_year'], series['election_type'], series['modality'], dict(counts), flush=True)
    OUT.write_text(json.dumps({'schema_version': '0.1', 'results': results},
                              ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__':
    main()
