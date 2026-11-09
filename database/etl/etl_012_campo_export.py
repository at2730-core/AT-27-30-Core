import json
from pathlib import Path

import psycopg2
from campo_db_config import get_campo_db_config

OUTPUT_GEOJSON = Path("data/puntos_campo_export.geojson")

SQL = """
SELECT
    a.actor_uuid,
    a.full_name,
    a.phone,
    a.address,
    a.observations,
    a.capture_source,
    a.capture_timestamp,

    s.section_code,

    a.district_local,
    a.district_federal,

    a.municipality_code,
    a.municipality_name,

    r.role_code,

    ST_X(a.geom) AS longitude,
    ST_Y(a.geom) AS latitude

FROM field.actor a

JOIN territorial.section s
    ON a.section_id = s.section_id

JOIN field.actor_assignment aa
    ON a.actor_id = aa.actor_id

JOIN field.role r
    ON aa.role_id = r.role_id

WHERE aa.active = TRUE

ORDER BY a.actor_id;
"""


def main():

    conn = psycopg2.connect(**get_campo_db_config())
    cur = conn.cursor()

    cur.execute(SQL)

    rows = cur.fetchall()

    features = []

    for row in rows:

        (
            actor_uuid,
            full_name,
            phone,
            address,
            observations,
            capture_source,
            capture_timestamp,
            section_code,
            district_local,
            district_federal,
            municipality_code,
            municipality_name,
            role_code,
            longitude,
            latitude
        ) = row

        feature = {
            "type": "Feature",
            "properties": {
                "ID": str(actor_uuid),
                "TS": capture_timestamp.isoformat() if capture_timestamp else None,
                "ORIGEN": capture_source,
                "ESTATUS": "ACTIVO",
                "TIPO": role_code,
                "NOMBRE": full_name,
                "TELEFONO": phone,
                "DOMICILIO": address,
                "SECCION": str(section_code),
                "DISTRITO_L": district_local,
                "DISTRITO_F": district_federal,
                "MUNICIPIO": municipality_code,
                "MUNICIPIO_NOMBRE": municipality_name,
                "OBS": observations
            },
            "geometry": {
                "type": "Point",
                "coordinates": [
                    float(longitude),
                    float(latitude)
                ]
            }
        }

        features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "name": "puntos_campo_export",
        "features": features
    }

    with open(
        OUTPUT_GEOJSON,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            geojson,
            f,
            ensure_ascii=False,
            indent=2
        )

    cur.close()
    conn.close()

    print("\n=== ETL_012_CAMPO_EXPORT ===")
    print(f"Registros exportados: {len(features)}")
    print(f"Archivo generado: {OUTPUT_GEOJSON}")


if __name__ == "__main__":
    main()