import getpass
import os


def get_campo_db_config():
    password = os.environ.get("HEYTI_DB_PASSWORD")

    if password is None:
        password = getpass.getpass(
            "Contrasena PostgreSQL para HEYTI: "
        )

    return {
        "host": os.environ.get("HEYTI_DB_HOST", "localhost"),
        "port": int(os.environ.get("HEYTI_DB_PORT", "5432")),
        "dbname": os.environ.get(
            "HEYTI_DB_NAME",
            "at2730_core",
        ),
        "user": os.environ.get("HEYTI_DB_USER", "postgres"),
        "password": password,
    }
