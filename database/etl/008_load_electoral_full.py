import json
import math
import re
import psycopg2
from pathlib import Path

DB_NAME = "at2730_core"
DB_USER = "postgres"
DB_PASSWORD = "at2730core"
DB_HOST = "localhost"
DB_PORT = "5432"

ELECTORAL_JSON_PATH = Path("datasets/electoral/Datos_Electoral_con_2015.json")
LIMIT = None
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

    if LIMIT:
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
                counter = 0

                for record in records:
                    counter += 1

                    if counter % 100 == 0:
                        print(f"Secciones procesadas: {counter}")

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

                        # Validar valores numéricos antes de convertirlos a int.
                        try:
                            votes_value = float(votes)
                        except (TypeError, ValueError):
                            print(
                                f"Saltando {field_name} en sección {section_code}: "
                                f"valor de votos no numérico: {votes!r}"
                            )
                            skipped += 1
                            continue

                        if math.isnan(votes_value):
                            print(
                                f"Saltando {field_name} en sección {section_code}: votos NaN"
                            )
                            skipped += 1
                            continue

                        votes_int = int(votes_value)

                        total_votes_raw = record.get(f"{year_suffix}{election_type}_TOTAL")
                        nominal_list_raw = record.get(f"{year_suffix}{election_type}_LN")

                        total_votes_int = None
                        nominal_list_int = None

                        if total_votes_raw is not None:
                            try:
                                tv = float(total_votes_raw)
                                if not math.isnan(tv):
                                    total_votes_int = int(tv)
                                else:
                                    print(f"Sección {section_code}: total_votes NaN, se deja NULL")
                            except (TypeError, ValueError):
                                print(f"Sección {section_code}: total_votes no numérico {total_votes_raw!r}, se deja NULL")

                        if nominal_list_raw is not None:
                            try:
                                nl = float(nominal_list_raw)
                                if not math.isnan(nl):
                                    nominal_list_int = int(nl)
                                else:
                                    print(f"Sección {section_code}: nominal_list NaN, se deja NULL")
                            except (TypeError, ValueError):
                                print(f"Sección {section_code}: nominal_list no numérico {nominal_list_raw!r}, se deja NULL")

                        participation_pct = None
                        if (
                            total_votes_int is not None
                            and nominal_list_int is not None
                            and nominal_list_int != 0
                        ):
                            participation_pct = round((float(total_votes_int) / float(nominal_list_int)) * 100, 2)
                        elif nominal_list_int == 0:
                            print(f"Sección {section_code}: nominal_list es 0, participation_pct no calculado")

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
                                votes_int,
                                total_votes_int,
                                nominal_list_int,
                                participation_pct,
                            ),
                        )

                        inserted += 1

                    print(f"Sección electoral procesada: {section_code}")

        print("ETL 008 completado correctamente.")
        print(f"Resultados insertados/actualizados: {inserted}")
        print(f"Registros saltados: {skipped}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()