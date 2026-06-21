import json
import uuid
from pathlib import Path
import psycopg2

INPUT_GEOJSON = Path("data/puntos_campo.geojson")

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "at2730_core",
    "user": "postgres",
    "password": "at2730core"
}


def is_valid_uuid(value):
    try:
        uuid.UUID(str(value))
        return True
    except Exception:
        return False


def main():
    if not INPUT_GEOJSON.exists():
        raise FileNotFoundError(f"No existe el archivo: {INPUT_GEOJSON}")

    with open(INPUT_GEOJSON, "r", encoding="utf-8") as f:
        data = json.load(f)

    features = data.get("features", [])

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("SELECT section_code FROM territorial.section;")
    valid_sections = {str(r[0]) for r in cur.fetchall()}

    cur.execute("SELECT role_code FROM field.role WHERE active = TRUE;")
    valid_roles = {str(r[0]).upper() for r in cur.fetchall()}

    total = len(features)
    uuid_validos = 0
    uuid_invalidos = 0
    uuid_duplicados = 0
    secciones_ok = 0
    secciones_error = 0
    roles_ok = 0
    roles_error = 0
    geom_ok = 0
    geom_error = 0

    seen_ids = set()
    errores = []

    for i, feature in enumerate(features, start=1):
        props = feature.get("properties", {})
        geom = feature.get("geometry", {})

        record_id = props.get("ID")
        seccion = str(props.get("SECCION", "")).strip()
        tipo = str(props.get("TIPO", "")).strip().upper()

        if is_valid_uuid(record_id):
            uuid_validos += 1
            if record_id in seen_ids:
                uuid_duplicados += 1
                errores.append((i, "UUID_DUPLICADO", record_id))
            seen_ids.add(record_id)
        else:
            uuid_invalidos += 1
            errores.append((i, "UUID_INVALIDO", record_id))

        if seccion in valid_sections:
            secciones_ok += 1
        else:
            secciones_error += 1
            errores.append((i, "SECCION_NO_ENCONTRADA", seccion))

        if tipo in valid_roles:
            roles_ok += 1
        else:
            roles_error += 1
            errores.append((i, "ROL_NO_ENCONTRADO", tipo))

        coords = geom.get("coordinates")
        if (
            geom.get("type") == "Point"
            and isinstance(coords, list)
            and len(coords) == 2
            and coords[0] is not None
            and coords[1] is not None
        ):
            geom_ok += 1
        else:
            geom_error += 1
            errores.append((i, "GEOMETRIA_INVALIDA", geom))

    print("\n=== ETL_011_CAMPO_VALIDADOR ===")
    print(f"Archivo: {INPUT_GEOJSON}")
    print(f"Registros leídos: {total}")
    print(f"UUID válidos: {uuid_validos}")
    print(f"UUID inválidos: {uuid_invalidos}")
    print(f"UUID duplicados: {uuid_duplicados}")
    print(f"Secciones encontradas: {secciones_ok}")
    print(f"Secciones no encontradas: {secciones_error}")
    print(f"Roles encontrados: {roles_ok}")
    print(f"Roles no encontrados: {roles_error}")
    print(f"Geometrías válidas: {geom_ok}")
    print(f"Geometrías inválidas: {geom_error}")

    if errores:
        print("\n--- ERRORES / ALERTAS ---")
        for err in errores:
            print(err)
    else:
        print("\nValidación completada sin errores.")

    cur.close()
    conn.close()


if __name__ == "__main__":
    main()