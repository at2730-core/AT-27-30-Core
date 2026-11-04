"""Cotejo exploratorio de votos IEEG 2024 frente a SEC SICEE, sin DB."""
from collections import Counter, defaultdict
import csv
import io
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent
FIELDS = ("PAN", "PRI", "PVEM", "MORENA", "TOTAL_VOTOS")
SERIES = (
    ("A", "AYUN_GTO.zip", "2024_SEE_AYUN_GTO_SEC.csv"),
    ("DL_MR", "DIP_LOC_GTO.zip", "2024_SEE_DIP_LOC_MR_GTO_SEC.csv"),
    ("G", "GUB_GTO.zip", "2024_SEE_GOB_GTO_SEC.csv"),
)


def read_ieeg(outer, suffix):
    member = next(n for n in outer.namelist() if n.endswith(suffix))
    with zipfile.ZipFile(io.BytesIO(outer.read(member))) as inner:
        csv_member = next(n for n in inner.namelist() if "CANDIDATURAS" not in n)
        lines = inner.read(csv_member).decode("utf-8-sig").splitlines()
    assert "SECCION" in lines[8] and "CONTABILIZADA" in lines[8]
    return member, csv_member, list(csv.DictReader(lines[8:]))


def main():
    output = ROOT / "HEYTI_Diferencias_IEEG_SICEE_2024_v0_1.csv"
    with zipfile.ZipFile(ROOT / "IEEG_Computos_2024_original.zip") as ieeg, zipfile.ZipFile(
        ROOT / "INE_SICEE_GTO_PEL_2024_original.zip"
    ) as sicee, output.open("w", newline="", encoding="utf-8-sig") as dest:
        columns = ["serie", "seccion", "campo", "ieeg_suma_contabilizada", "sicee_sec", "diferencia_ieeg_menos_sicee", "ieeg_filas", "ieeg_filas_contabilizadas", "ieeg_filas_no_contabilizadas", "ieeg_miembro", "sicee_miembro"]
        writer = csv.DictWriter(dest, fieldnames=columns)
        writer.writeheader()
        for series, suffix, sec_suffix in SERIES:
            ieeg_zip_member, ieeg_member, rows = read_ieeg(ieeg, suffix)
            sec_member = next(n for n in sicee.namelist() if n.endswith(sec_suffix))
            sec_rows = {
                int(r["SECCION"]): r
                for r in csv.DictReader(io.StringIO(sicee.read(sec_member).decode("utf-8-sig")))
                if 0 < int(r["SECCION"]) < 9000
            }
            groups = defaultdict(list)
            for r in rows:
                key = int(r["SECCION"])
                if 0 < key < 9000:
                    # IEEG DL mezcla casillas especiales MR y RP en el CSV.
                    if series == "DL_MR" and r["ACTA_CASILLA-MEC"].strip().upper().startswith("SRP"):
                        continue
                    groups[key].append(r)
            field_counts = Counter()
            affected = set()
            compared = 0
            for key in sorted(groups.keys() & sec_rows.keys()):
                counted = [r for r in groups[key] if r["CONTABILIZADA"] == "1"]
                if not counted:
                    continue
                compared += 1
                for field in FIELDS:
                    values = [r[field].strip() for r in counted]
                    source = sec_rows[key][field].strip()
                    if not source or any(not v for v in values):
                        raise ValueError(f"Dato vacío: {series} {key} {field}")
                    left, right = sum(map(int, values)), int(source)
                    if left != right:
                        field_counts[field] += 1
                        affected.add(key)
                        writer.writerow({"serie": series, "seccion": key, "campo": field, "ieeg_suma_contabilizada": left, "sicee_sec": right, "diferencia_ieeg_menos_sicee": left - right, "ieeg_filas": len(groups[key]), "ieeg_filas_contabilizadas": len(counted), "ieeg_filas_no_contabilizadas": len(groups[key]) - len(counted), "ieeg_miembro": f"{ieeg_zip_member}/{ieeg_member}", "sicee_miembro": sec_member})
            print(series, "pares", compared, "secciones_diferentes", len(affected), "celdas", dict(field_counts), "ejemplos", sorted(affected)[:10])
    print(output)


if __name__ == "__main__":
    main()
