import json
import uuid
from pathlib import Path
import psycopg2
from psycopg2.extras import execute_values

INPUT_GEOJSON = Path("data/puntos_campo.geojson")

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "at2730_core",
    "user": "postgres",
    "password": "at2730core"
}


def main():
    with open(INPUT_GEOJSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    features = data.get("features", [])

    conn = psycopg2.connect(**DB_CONFIG)
    conn.autocommit = False
    cur = conn.cursor()

    inserted = 0
    skipped = 0
    errors = []

    try:
        for i, feature in enumerate(features, start=1):
            props = feature.get("properties", {})
            geom = feature.get("geometry", {})
            coords = geom.get("coordinates", [None, None])

            actor_uuid = props.get("ID")
            if not actor_uuid:
                errors.append((i, "SIN_ID"))
                continue

            actor_uuid = str(uuid.UUID(actor_uuid))
            source_id = actor_uuid

            seccion = str(props.get("SECCION", "")).strip()
            tipo = str(props.get("TIPO", "")).strip().upper()

            cur.execute("""
                SELECT section_id
                FROM territorial.section
                WHERE section_code = %s
            """, (seccion,))
            sec_row = cur.fetchone()

            if not sec_row:
                errors.append((i, "SECCION_NO_ENCONTRADA", seccion))
                continue

            section_id = sec_row[0]

            cur.execute("""
                SELECT role_id
                FROM field.role
                WHERE role_code = %s
                  AND active = TRUE
            """, (tipo,))
            role_row = cur.fetchone()

            if not role_row:
                errors.append((i, "ROL_NO_ENCONTRADO", tipo))
                continue

            role_id = role_row[0]

            cur.execute("""
                SELECT actor_id
                FROM field.actor
                WHERE actor_uuid = %s
            """, (actor_uuid,))
            existing = cur.fetchone()

            if existing:
                skipped += 1
                continue

            lon = coords[0]
            lat = coords[1]

            cur.execute("""
                INSERT INTO field.actor (
                    actor_uuid,
                    source_id,
                    full_name,
                    phone,
                    address,
                    observations,
                    section_id,
                    district_local,
                    district_federal,
                    municipality_code,
                    municipality_name,
                    capture_source,
                    capture_timestamp,
                    geom,
                    created_at,
                    updated_at
                )
                VALUES (
                    %s, %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                    NOW(), NOW()
                )
                RETURNING actor_id
            """, (
                actor_uuid,
                source_id,
                props.get("NOMBRE"),
                props.get("TELEFONO"),
                props.get("DOMICILIO"),
                props.get("OBS"),
                section_id,
                props.get("DISTRITO_L"),
                props.get("DISTRITO_F"),
                props.get("MUNICIPIO"),
                props.get("MUNICIPIO_NOMBRE"),
                props.get("ORIGEN"),
                props.get("TS"),
                lon,
                lat
            ))

            actor_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO field.actor_location (
                    actor_id,
                    section_id,
                    latitude,
                    longitude,
                    address,
                    created_at
                )
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (
                actor_id,
                section_id,
                lat,
                lon,
                props.get("DOMICILIO")
            ))

            cur.execute("""
                INSERT INTO field.actor_assignment (
                    actor_id,
                    role_id,
                    section_id,
                    scope_type,
                    scope_code,
                    active,
                    created_at,
                    updated_at
                )
                VALUES (%s, %s, %s, %s, %s, TRUE, NOW(), NOW())
            """, (
                actor_id,
                role_id,
                section_id,
                "SECTION",
                seccion
            ))

            inserted += 1

        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        cur.close()
        conn.close()

    print("\n=== ETL_011_CAMPO ===")
    print(f"Archivo: {INPUT_GEOJSON}")
    print(f"Registros leídos: {len(features)}")
    print(f"Actores insertados: {inserted}")
    print(f"Registros omitidos por duplicado: {skipped}")
    print(f"Errores: {len(errors)}")

    if errors:
        print("\n--- ERRORES ---")
        for err in errors:
            print(err)
    else:
        print("\nCarga completada sin errores.")


if __name__ == "__main__":
    main()