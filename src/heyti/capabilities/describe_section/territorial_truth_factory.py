from dataclasses import dataclass
from pathlib import Path

from heyti.audit.data_truth.baselines.guanajuato_2023 import (
    GUANAJUATO_2023_V1,
)
from heyti.audit.data_truth.section_universe import (
    SectionUniverseProfile,
    profile_section_universes,
)
from heyti.audit.data_truth.territorial_policy import (
    TerritorialClassification,
    classify_section_universes,
)
from heyti.capabilities.describe_section.territorial_truth_source import (
    TerritorialSectionTruthSource,
)


EXPECTED_MASTER_RECORDS = 3310
EXPECTED_GEOMETRY_RECORDS = 3266
EXPECTED_COMPARABLE_SECTIONS = 3230
EXPECTED_MASTER_ONLY = 80
EXPECTED_GEOMETRY_ONLY = 36
EXPECTED_UNCLASSIFIED_MASTER_ONLY = 4


@dataclass(frozen=True)
class GuanajuatoTerritorialTruthAssembly:
    """
    Ensamblaje territorial certificado para Guanajuato 2023.

    Conserva el perfil y la clasificación que originaron
    la fuente utilizada por DescribeSection.
    """

    profile: SectionUniverseProfile
    classification: TerritorialClassification
    source: TerritorialSectionTruthSource


def _validate_profile(
    profile: SectionUniverseProfile,
) -> None:
    observed = {
        "master_records": profile.master_records,
        "geometry_records": profile.geometry_records,
        "comparable_sections": profile.comparable_sections,
        "master_only": len(profile.master_only),
        "geometry_only": len(profile.geometry_only),
    }
    expected = {
        "master_records": EXPECTED_MASTER_RECORDS,
        "geometry_records": EXPECTED_GEOMETRY_RECORDS,
        "comparable_sections": EXPECTED_COMPARABLE_SECTIONS,
        "master_only": EXPECTED_MASTER_ONLY,
        "geometry_only": EXPECTED_GEOMETRY_ONLY,
    }

    mismatches = {
        key: {
            "expected": expected[key],
            "observed": observed[key],
        }
        for key in expected
        if observed[key] != expected[key]
    }

    if profile.master_duplicates:
        mismatches["master_duplicates"] = {
            "expected": (),
            "observed": profile.master_duplicates,
        }

    if profile.geometry_duplicates:
        mismatches["geometry_duplicates"] = {
            "expected": (),
            "observed": profile.geometry_duplicates,
        }

    if profile.master_invalid_values:
        mismatches["master_invalid_values"] = {
            "expected": (),
            "observed": profile.master_invalid_values,
        }

    if profile.geometry_invalid_values:
        mismatches["geometry_invalid_values"] = {
            "expected": (),
            "observed": profile.geometry_invalid_values,
        }

    if len(profile.comparable_section_ids) != (
        profile.comparable_sections
    ):
        mismatches["comparable_section_ids"] = {
            "expected": profile.comparable_sections,
            "observed": len(
                profile.comparable_section_ids
            ),
        }

    if mismatches:
        raise ValueError(
            "El perfil territorial no coincide con "
            f"GUANAJUATO_2023: {mismatches}"
        )


def _validate_classification(
    classification: TerritorialClassification,
) -> None:
    expected = {
        "certified_predecessors": len(
            GUANAJUATO_2023_V1.certified_lineage
        ),
        "certified_successors": sum(
            len(successors)
            for successors
            in GUANAJUATO_2023_V1.certified_lineage.values()
        ),
        "unresolved_historical": len(
            GUANAJUATO_2023_V1.unresolved_historical
        ),
        "synthetic_candidates": len(
            GUANAJUATO_2023_V1.synthetic_candidates
        ),
        "unclassified_master_only": (
            EXPECTED_UNCLASSIFIED_MASTER_ONLY
        ),
        "unexpected_geometry_only": 0,
    }

    observed = {
        key: len(getattr(classification, key))
        for key in expected
    }

    mismatches = {
        key: {
            "expected": expected[key],
            "observed": observed[key],
        }
        for key in expected
        if observed[key] != expected[key]
    }

    if mismatches:
        raise ValueError(
            "La clasificación territorial no coincide con "
            f"GUANAJUATO_2023: {mismatches}"
        )


def build_guanajuato_2023_territorial_truth(
    master_path: str | Path,
    geometry_path: str | Path,
) -> GuanajuatoTerritorialTruthAssembly:
    """
    Construye la fuente territorial de DescribeSection.

    Falla de forma explícita si las fuentes se apartan
    del baseline certificado.
    """

    profile = profile_section_universes(
        master_path=master_path,
        geometry_path=geometry_path,
    )
    _validate_profile(profile)

    classification = classify_section_universes(
        profile=profile,
        policy=GUANAJUATO_2023_V1,
    )
    _validate_classification(classification)

    source = TerritorialSectionTruthSource(
        classification=classification,
        policy=GUANAJUATO_2023_V1,
        current_section_ids=(
            profile.comparable_section_ids
        ),
    )

    return GuanajuatoTerritorialTruthAssembly(
        profile=profile,
        classification=classification,
        source=source,
    )
