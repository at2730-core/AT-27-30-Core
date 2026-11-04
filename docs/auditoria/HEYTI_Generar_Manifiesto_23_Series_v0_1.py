"""Genera un manifiesto verificable de CSV seccionales desde 15 ZIP ya auditados.
No conecta a PostgreSQL ni escribe dentro de los ZIP. Ejecutar en una copia aislada.
"""
import csv
import hashlib
import io
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
OUT = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else ROOT / 'HEYTI_Manifiesto_23_Series_2018_2024_v0_1.json'
NAMES = {
 'INE_SICEE_DF_MR_2018_original.zip': ('DF', 2018, 'MR'),
 'INE_SICEE_DF_MR_2021_original.zip': ('DF', 2021, 'MR'),
 'INE_SICEE_DF_MR_2024_original.zip': ('DF', 2024, 'MR'),
 'INE_SICEE_DF_RP_2018_original.zip': ('DF', 2018, 'RP'),
 'INE_SICEE_DF_RP_2021_original.zip': ('DF', 2021, 'RP'),
 'INE_SICEE_DF_RP_2024_original.zip': ('DF', 2024, 'RP'),
 'INE_SICEE_GTO_PEL_2018_original.zip': ('LOCAL', 2018, None),
 'INE_SICEE_GTO_PEL_2021_original.zip': ('LOCAL', 2021, None),
 'INE_SICEE_GTO_PEL_2024_original.zip': ('LOCAL', 2024, None),
 'INE_SICEE_P_2018_original.zip': ('P', 2018, 'UNICA'),
 'INE_SICEE_P_2024_original.zip': ('P', 2024, 'UNICA'),
 'INE_SICEE_S_2018_original.zip': ('S', 2018, 'MR'),
 'INE_SICEE_S_2024_original.zip': ('S', 2024, 'MR'),
 'INE_SICEE_S_RP_2018_original.zip': ('S', 2018, 'RP'),
 'INE_SICEE_S_RP_2024_original.zip': ('S', 2024, 'RP'),
}

def local_type(member):
    name = member.rsplit('/', 1)[-1]
    if '_AYUN_' in name: return 'A', 'UNICA'
    if '_GOB_' in name: return 'G', 'UNICA'
    if '_DIP_LOC_MR_' in name: return 'DL', 'MR'
    if '_DIP_LOC_RP_' in name: return 'DL', 'RP'
    raise ValueError('Serie local no identificada: ' + member)

def digest(b): return hashlib.sha256(b).hexdigest()

def main():
    releases = []
    for name, (typ, year, modality) in NAMES.items():
        path = ROOT / name
        outer = path.read_bytes()
        with zipfile.ZipFile(io.BytesIO(outer)) as z:
            if z.testzip() is not None: raise ValueError('ZIP CRC fallido: ' + name)
            members = [n for n in z.namelist() if re.search(r'_SEC\.csv$', n, re.I)]
            if not members: raise ValueError('Sin CSV seccional: ' + name)
            series = []
            for member in members:
                data = z.read(member)
                try:
                    content = data.decode('utf-8-sig')
                    encoding = 'utf-8-sig'
                except UnicodeDecodeError:
                    content = data.decode('cp1252')
                    encoding = 'cp1252'
                reader = csv.reader(io.StringIO(content, newline=''))
                header = next(reader)
                if len(header) != len(set(header)) or 'SECCION' not in header:
                    raise ValueError('Cabecera no única o sin SECCION: ' + member)
                count = 0
                gto_rows = 0
                ordinary_rows = zero_section_rows = special_section_rows = other_section_rows = 0
                section_idx = header.index('SECCION')
                state_idx = header.index('ID_ESTADO')
                for line in reader:
                    if len(line) != len(header):
                        raise ValueError(f'Ancho inválido {member}, registro {count+2}')
                    count += 1
                    if line[state_idx].strip() in ('11', '011'):
                        gto_rows += 1
                        section = line[section_idx].strip()
                        if section.isdecimal():
                            section_number = int(section)
                            if section_number == 0: zero_section_rows += 1
                            elif section_number >= 9000: special_section_rows += 1
                            else: ordinary_rows += 1
                        else: other_section_rows += 1
                t, m = local_type(member) if typ == 'LOCAL' else (typ, modality)
                series.append({'election_year': year, 'election_type': t, 'modality': m,
                    'aggregation_level': 'SECTION', 'member_path': member,
                    'member_sha256': digest(data), 'encoding': encoding, 'delimiter': ',',
                    'rows': count, 'gto_rows': gto_rows, 'ordinary_section_rows': ordinary_rows, 'zero_section_rows': zero_section_rows, 'special_section_rows': special_section_rows, 'other_section_rows': other_section_rows, 'state_filter': {'column': 'ID_ESTADO', 'accepted_numeric_value': 11}, 'header_columns': header,
                    'cut_label': 'SOURCE_AS_PUBLISHED_UNVERIFIED_DATE', 'selection_status': 'UNREVIEWED'})
            releases.append({'zip_name': name, 'outer_zip_sha256': digest(outer),
                'authority': 'INE/SICEE', 'source_uri': None, 'published_at': None,
                'series': series})
    if len(releases) != 15 or sum(len(x['series']) for x in releases) != 23:
        raise ValueError('Inventario incompleto: se esperaban 15 ZIP y 23 series')
    OUT.write_text(json.dumps({'schema_version': '0.1', 'scope': 'Guanajuato',
        'release_count': 15, 'series_count': 23, 'releases': releases}, ensure_ascii=False,
        indent=2) + '\n', encoding='utf-8')
    print(f'{OUT}: 15 ZIP, 23 series, {sum(s["rows"] for r in releases for s in r["series"])} filas fuente, {sum(s["gto_rows"] for r in releases for s in r["series"])} filas GTO')

if __name__ == '__main__': main()
