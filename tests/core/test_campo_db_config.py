import importlib.util
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
CONFIG_PATH = (
    REPOSITORY_ROOT
    / "database"
    / "etl"
    / "campo_db_config.py"
)

SPEC = importlib.util.spec_from_file_location(
    "campo_db_config_under_test",
    CONFIG_PATH,
)
campo_db_config = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(campo_db_config)


def test_campo_db_config_reads_environment(monkeypatch):
    monkeypatch.setenv("HEYTI_DB_HOST", "db.example")
    monkeypatch.setenv("HEYTI_DB_PORT", "5544")
    monkeypatch.setenv("HEYTI_DB_NAME", "heyti_test")
    monkeypatch.setenv("HEYTI_DB_USER", "heyti_user")
    monkeypatch.setenv("HEYTI_DB_PASSWORD", "secret-from-env")

    config = campo_db_config.get_campo_db_config()

    assert config == {
        "host": "db.example",
        "port": 5544,
        "dbname": "heyti_test",
        "user": "heyti_user",
        "password": "secret-from-env",
    }


def test_campo_db_config_prompts_without_password(monkeypatch):
    for variable in [
        "HEYTI_DB_HOST",
        "HEYTI_DB_PORT",
        "HEYTI_DB_NAME",
        "HEYTI_DB_USER",
        "HEYTI_DB_PASSWORD",
    ]:
        monkeypatch.delenv(variable, raising=False)

    monkeypatch.setattr(
        campo_db_config.getpass,
        "getpass",
        lambda prompt: "secret-from-prompt",
    )

    config = campo_db_config.get_campo_db_config()

    assert config == {
        "host": "localhost",
        "port": 5432,
        "dbname": "at2730_core",
        "user": "postgres",
        "password": "secret-from-prompt",
    }
