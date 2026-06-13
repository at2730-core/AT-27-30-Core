import json
import psycopg2
from pathlib import Path

# =====================================================
# AT-27-30 Core
# ETL 002 - Load first 10 sections from secciones.geojson
# =====================================================

DB_NAME = "at2730_core"
DB_USER = "postgres"
DB_PASSWORD = "at2730core"
DB_HOST = "localhost"
DB_PORT = "5432"

GEOJSON_PATH = Path("datasets/spatial/secciones.geojson")



def main():
    if not GEOJSON_PATH.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {GEOJSON_PATH}")

    with GEOJSON_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    features = data.get("features", [])

    print(f"Features a cargar: {len(features)}")

    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )

    try:
        with conn:
            with conn.cursor() as cur:

                counter =  0

                for feature in features:

                    counter += 1

                    if counter % 100 == 0:
                        print(f"Cargadas{counter} secciones...")

                    props = feature["properties"]
                    geometry = feature["geometry"]

                    section_code = str(int(props["SECCION"]))
                    municipio_code = str(int(props["MUNICIPIO"]))
                    dl_code = str(int(props["DISTRITO_L"]))
                    df_code = str(int(props["DISTRITO_F"]))
                    section_type = str(props.get("TIPO")) if props.get("TIPO") is not None else None

                    geom_json = json.dumps(geometry)

                    # Buscar IDs de catálogos
                    cur.execute(
                        """
                        SELECT municipio_id
                        FROM territorial.municipio
                        WHERE municipio_code = %s
                        """,
                        (municipio_code,),
                    )
                    municipio = cur.fetchone()

                    cur.execute(
                        """
                        SELECT distrito_local_id
                        FROM territorial.distrito_local
                        WHERE dl_code = %s
                        """,
                        (dl_code,),
                    )
                    distrito_local = cur.fetchone()

                    cur.execute(
                        """
                        SELECT distrito_federal_id
                        FROM territorial.distrito_federal
                        WHERE df_code = %s
                        """,
                        (df_code,),
                    )
                    distrito_federal = cur.fetchone()

                    if not municipio or not distrito_local or not distrito_federal:
                        print(
                            f"Saltando sección {section_code}: "
                            f"municipio={municipio_code}, dl={dl_code}, df={df_code}"
                        )
                        continue

                    municipio_id = municipio[0]
                    distrito_local_id = distrito_local[0]
                    distrito_federal_id = distrito_federal[0]

                    # Insertar sección
                    cur.execute(
                        """
                        INSERT INTO territorial.section (
                            section_code,
                            municipio_id,
                            distrito_local_id,
                            distrito_federal_id,
                            section_type,
                            current_status,
                            source_dataset
                        )
                        VALUES (%s, %s, %s, %s, %s, 'active', 'secciones.geojson')
                        ON CONFLICT (section_code)
                        DO UPDATE SET
                            municipio_id = EXCLUDED.municipio_id,
                            distrito_local_id = EXCLUDED.distrito_local_id,
                            distrito_federal_id = EXCLUDED.distrito_federal_id,
                            section_type = EXCLUDED.section_type,
                            updated_at = CURRENT_TIMESTAMP
                        RETURNING section_id
                        """,
                        (
                            section_code,
                            municipio_id,
                            distrito_local_id,
                            distrito_federal_id,
                            section_type,
                        ),
                    )

                    section_id = cur.fetchone()[0]

                    # Insertar geometría
                    cur.execute(
                        """
                        INSERT INTO spatial.section_geometry (
                            section_id,
                            geom,
                            area_m2,
                            centroid,
                            geometry_source,
                            geometry_status
                        )
                        VALUES (
                            %s,
                            ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326),
                            ST_Area(ST_Transform(ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326), 6372)),
                            ST_Centroid(ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326)),
                            'secciones.geojson',
                            'loaded'
                        )
                        ON CONFLICT (section_id)
                        DO UPDATE SET
                            geom = EXCLUDED.geom,
                            area_m2 = EXCLUDED.area_m2,
                            centroid = EXCLUDED.centroid,
                            geometry_source = EXCLUDED.geometry_source,
                            geometry_status = EXCLUDED.geometry_status
                        """,
                        (section_id, geom_json, geom_json, geom_json),
                    )

                    print(f"Total cargadas: {counter}")

        print("ETL 003 completado correctamente.")

    finally:
        conn.close()


if __name__ == "__main__":
    main()