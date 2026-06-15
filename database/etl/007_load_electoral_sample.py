import json
import re
import psycopg2
from pathlib import Path

DB_NAME = "at2730_core"
DB_USER = "postgres"
DB_PASSWORD = "at2730core"
DB_HOST = "localhost"
DB_PORT = "5432"

ELECTORAL_JSON_PATH = Path("datasets/electoral/Datos_Electoral_con_2015.json")
LIMIT = 10

PARTIES = {"PAN", "PRI", "PVEM", "MORENA", "PRD", "PT", "MC", "NA"}

FIELD_PATTERN = re.compile(r"^(15|18|21|24)(A|DF|DL|G|P|S)_([A-Z]+)$")


def get_id(cur, sql, params):
    cur.execute(sql, params)
    row = cur.fetchone()
    return row[0] if row else None


def main():
    if not ELECTORAL_JSON_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ELECTORAL_JSON_PATH}")

    with ELECTORAL_JSON_PATH.open("r", encoding="utf-8") as f:
        records = json.load(f)

    records = records[:LIMIT]
    print(f"Registros electorales a procesar: {len(records)}")

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )

    inserted = 0
    skipped = 0

    try:
        with conn:
            with conn.cursor() as cur:
                for record in records:
                    section_code = str(int(record["SECCION"]))

                    section_id = get_id(
                        cur,
                        """
                        SELECT section_id
                        FROM territorial.section
                        WHERE section_code = %s
                        """,
                        (section_code,),
                    )

                    if not section_id:
                        print(f"Saltando sección {section_code}: no existe en territorial.section")
                        skipped += 1
                        continue

                    for field_name, votes in record.items():
                        match = FIELD_PATTERN.match(field_name)

                        if not match:
                            continue

                        year_suffix, election_type, party_code = match.groups()

                        if party_code not in PARTIES:
                            continue

                        election_year = 2000 + int(year_suffix)

                        election_id = get_id(
                            cur,
                            """
                            SELECT election_id
                            FROM electoral.election
                            WHERE election_year = %s
                              AND election_type = %s
                            """,
                            (election_year, election_type),
                        )

                        party_id = get_id(
                            cur,
                            """
                            SELECT party_id
                            FROM electoral.party
                            WHERE party_code = %s
                            """,
                            (party_code,),
                        )

                        if not election_id or not party_id:
                            print(
                                f"Saltando {field_name} en sección {section_code}: "
                                f"election_id={election_id}, party_id={party_id}"
                            )
                            skipped += 1
                            continue

                        total_votes = record.get(f"{year_suffix}{election_type}_TOTAL")
                        nominal_list = record.get(f"{year_suffix}{election_type}_LN")

                        participation_pct = None
                        if total_votes is not None and nominal_list:
                            participation_pct = round((float(total_votes) / float(nominal_list)) * 100, 2)

                        cur.execute(
                            """
                            INSERT INTO electoral.section_result (
                                section_id,
                                election_id,
                                party_id,
                                votes,
                                total_votes,
                                nominal_list,
                                participation_pct
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s)
                            ON CONFLICT (section_id, election_id, party_id)
                            DO UPDATE SET
                                votes = EXCLUDED.votes,
                                total_votes = EXCLUDED.total_votes,
                                nominal_list = EXCLUDED.nominal_list,
                                participation_pct = EXCLUDED.participation_pct
                            """,
                            (
                                section_id,
                                election_id,
                                party_id,
                                int(votes),
                                int(total_votes) if total_votes is not None else None,
                                int(nominal_list) if nominal_list is not None else None,
                                participation_pct,
                            ),
                        )

                        inserted += 1

                    print(f"Sección electoral procesada: {section_code}")

        print("ETL 007 completado correctamente.")
        print(f"Resultados insertados/actualizados: {inserted}")
        print(f"Registros saltados: {skipped}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()