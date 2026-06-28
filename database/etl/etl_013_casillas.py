import json
from pathlib import Path

import psycopg2

INPUT_JSON = Path("data/casillas_min_rows.json")

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "at2730_core",
    "user": "postgres",
    "password": "at2730core"
}


def main():
    if not INPUT_JSON.exists():
        raise FileNotFoundError(f"No existe el archivo: {INPUT_JSON}")

    with open(INPUT_JSON, "r", encoding="utf-8") as f:
        rows = json.load(f)

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()

    inserted = 0
    skipped = 0
    missing_sections = []
    errors = []

    try:
        for i, row in enumerate(rows, start=1):
            section_code = str(row.get("SECCION", "")).strip()
            casilla_code = str(row.get("CASILLA", "")).strip()

            locality = row.get("LOCALIDAD")
            address = row.get("DOMICILIO")

            if not section_code or not casilla_code:
                errors.append((i, "SECCION_O_CASILLA_VACIA", row))
                continue

            cur.execute("""
                SELECT section_id
                FROM territorial.section
                WHERE section_code = %s
            """, (section_code,))
            sec = cur.fetchone()

            if not sec:
                missing_sections.append(section_code)
                errors.append((i, "SECCION_NO_ENCONTRADA", section_code, casilla_code))
                continue

            section_id = sec[0]

            cur.execute("""
                INSERT INTO structure.casilla (
                    section_id,
                    section_code,
                    casilla_code,
                    locality,
                    address,
                    required_reps,
                    source_dataset,
                    created_at,
                    updated_at
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    1,
                    'casillas_min_rows.json',
                    NOW(),
                    NOW()
                )
                ON CONFLICT (section_code, casilla_code)
                DO NOTHING
            """, (
                section_id,
                section_code,
                casilla_code,
                locality,
                address
            ))

            if cur.rowcount == 1:
                inserted += 1
            else:
                skipped += 1

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()
        conn.close()

    print("\n=== ETL_013_CASILLAS ===")
    print(f"Archivo: {INPUT_JSON}")
    print(f"Registros leídos: {len(rows)}")
    print(f"Casillas insertadas: {inserted}")
    print(f"Casillas omitidas por duplicado: {skipped}")
    print(f"Secciones no encontradas: {len(set(missing_sections))}")
    print(f"Errores: {len(errors)}")

    if errors:
        print("\n--- ERRORES / ALERTAS ---")
        for err in errors[:50]:
            print(err)

        if len(errors) > 50:
            print(f"... y {len(errors) - 50} errores más.")
    else:
        print("\nCarga completada sin errores.")


if __name__ == "__main__":
    main()