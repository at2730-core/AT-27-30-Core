from pathlib import Path

from heyti.audit.data_truth.profiles import (
    profile_json_non_finite,
)


def write_source(
    path: Path,
    content: str,
) -> Path:
    path.write_text(
        content,
        encoding="utf-8",
    )
    return path


def test_profile_reports_clean_json(tmp_path):
    source = write_source(
        tmp_path / "clean.json",
        '[{"SECCION": 1, "VOTOS": null}]',
    )

    profile = profile_json_non_finite(source)

    assert profile.total_values == 0
    assert profile.affected_records == 0
    assert profile.affected_fields == 0
    assert profile.field_counts == {}


def test_profile_counts_nan_values_by_field(tmp_path):
    source = write_source(
        tmp_path / "nan.json",
        (
            '[{"SECCION": 1, "VOTOS": NaN},'
            ' {"SECCION": 2, "VOTOS": NaN, "LN": NaN},'
            ' {"SECCION": 3, "VOTOS": 10}]'
        ),
    )

    profile = profile_json_non_finite(source)

    assert profile.total_values == 3
    assert profile.affected_records == 2
    assert profile.affected_fields == 2
    assert profile.field_counts == {
        "LN": 1,
        "VOTOS": 2,
    }


def test_profile_counts_positive_and_negative_infinity(tmp_path):
    source = write_source(
        tmp_path / "infinity.json",
        '[{"MAX": Infinity, "MIN": -Infinity}]',
    )

    profile = profile_json_non_finite(source)

    assert profile.total_values == 2
    assert profile.affected_records == 1
    assert profile.field_counts == {
        "MAX": 1,
        "MIN": 1,
    }


def test_profile_preserves_nested_field_paths(tmp_path):
    source = write_source(
        tmp_path / "nested.json",
        (
            '[{"SECCION": 1,'
            ' "resultados": {"2024": {"PAN": NaN}}}]'
        ),
    )

    profile = profile_json_non_finite(source)

    assert profile.field_counts == {
        "resultados.2024.PAN": 1,
    }


def test_profile_serializes_complete_result(tmp_path):
    source = write_source(
        tmp_path / "serialized.json",
        '[{"SECCION": 1, "VOTOS": NaN}]',
    )

    data = profile_json_non_finite(
        source
    ).to_dict()

    assert data == {
        "total_values": 1,
        "affected_records": 1,
        "affected_fields": 1,
        "field_counts": {
            "VOTOS": 1,
        },
    }


def test_profile_does_not_modify_source(tmp_path):
    original = '[{"SECCION": 1, "VOTOS": NaN}]'

    source = write_source(
        tmp_path / "preserved.json",
        original,
    )

    before = source.read_bytes()

    profile_json_non_finite(source)

    after = source.read_bytes()

    assert before == after
