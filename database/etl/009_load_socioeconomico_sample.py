import json
import psycopg2
from pathlib import Path

DB_NAME = "at2730_core"
DB_USER = "postgres"
DB_PASSWORD = "at2730core"
DB_HOST = "localhost"
DB_PORT = "5432"

SOCIO_JSON_PATH = Path("datasets/socioeconomico/Datos_Socioeconomicos.json")
LIMIT = 10


INDICATOR_NAMES = {
    "POB_TOTAL": "Población total",
    "POB_15_17": "Población de 15 a 17 años",
    "POB_18MAS": "Población de 18 años y más",
    "ESCOLARIDAD_PROM": "Escolaridad promedio",
    "ANALFABETAS_15MAS": "Analfabetas de 15 años y más",
    "PEA_12MAS": "Población económicamente activa de 12 años y más",
    "OCUPADOS_12MAS": "Ocupados de 12 años y más",
    "DESOCUPADOS_12MAS": "Desocupados de 12 años y más",
    "VIV_CON_ELECTRICIDAD": "Viviendas con electricidad",
    "VIV_CON_AGUA": "Viviendas con agua",
    "VIV_CON_DRENAJE": "Viviendas con drenaje",
    "VIV_CON_INTERNET": "Viviendas con internet",
    "VIV_CON_CEL": "Viviendas con celular",
    "VIV_CON_PC": "Viviendas con computadora",
}

INDICATOR_CATEGORIES = {
    "POB_TOTAL": "poblacion",
    "POB_15_17": "poblacion",
    "POB_18MAS": "poblacion",
    "ESCOLARIDAD_PROM": "educacion",
    "ANALFABETAS_15MAS": "educacion",
    "PEA_12MAS": "economia",
    "OCUPADOS_12MAS": "economia",
    "DESOCUPADOS_12MAS": "economia",
    "VIV_CON_ELECTRICIDAD": "vivienda_servicios",
    "VIV_CON_AGUA": "vivienda_servicios",
    "VIV_CON_DRENAJE": "vivienda_servicios",
    "VIV_CON_INTERNET": "vivienda_conectividad",
    "VIV_CON_CEL": "vivienda_conectividad",
    "VIV_CON_PC": "vivienda_conectividad",
}


def get_section_id(cur, section_code):
    cur.execute(
        """
        SELECT section_id
        FROM territorial.section
        WHERE section_code = %s
        """,
        (section_code,),
    )
    row = cur.fetchone()
    return row[0] if row else None


def to_numeric(value):
    if value is None or value == "":
        return None
    return float(value)


def main():
    if not SOCIO_JSON_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {SOCIO_JSON_PATH}")

    with SOCIO_JSON_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    items = list(data.items())[:LIMIT]

    print(f"Secciones socioeconómicas a procesar: {len(items)}")

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )

    inserted = 0
    skipped_sections = 0

    try:
        with conn:
            with conn.cursor() as cur:
                for section_code, indicators in items:
                    section_code = str(int(section_code))

                    section_id = get_section_id(cur, section_code)

                    if not section_id:
                        print(f"Saltando sección {section_code}: no existe en territorial.section")
                        skipped_sections += 1
                        continue

                    for indicator_code, raw_value in indicators.items():
                        value = to_numeric(raw_value)

                        indicator_name = INDICATOR_NAMES.get(indicator_code, indicator_code)
                        indicator_category = INDICATOR_CATEGORIES.get(indicator_code, "sin_categoria")

                        cur.execute(
                            """
                            INSERT INTO socioeconomico.section_indicator (
                                section_id,
                                indicator_code,
                                indicator_name,
                                indicator_value,
                                indicator_category,
                                source_dataset
                            )
                            VALUES (%s, %s, %s, %s, %s, 'Datos_Socioeconomicos.json')
                            ON CONFLICT (section_id, indicator_code)
                            DO UPDATE SET
                                indicator_name = EXCLUDED.indicator_name,
                                indicator_value = EXCLUDED.indicator_value,
                                indicator_category = EXCLUDED.indicator_category
                            """,
                            (
                                section_id,
                                indicator_code,
                                indicator_name,
                                value,
                                indicator_category,
                            ),
                        )

                        inserted += 1

                    print(f"Sección socioeconómica procesada: {section_code}")

        print("ETL 009 completado correctamente.")
        print(f"Indicadores insertados/actualizados: {inserted}")
        print(f"Secciones saltadas: {skipped_sections}")

    finally:
        conn.close()


if __name__ == "__main__":
    main()