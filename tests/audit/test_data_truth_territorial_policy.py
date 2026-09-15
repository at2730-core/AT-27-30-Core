import pytest

from heyti.audit.data_truth.section_universe import (
    SectionUniverseProfile,
)
from heyti.audit.data_truth.territorial_policy import (
    TerritorialSectionPolicy,
    classify_section_universes,
)


def build_profile():
    return SectionUniverseProfile(
        master_records=7,
        geometry_records=4,
        master_unique=7,
        geometry_unique=4,
        comparable_sections=2,
        master_only=(
            10,
            20,
            30,
            40,
            9001,
        ),
        geometry_only=(
            101,
            102,
        ),
        master_duplicates=(),
        geometry_duplicates=(),
        master_invalid_values=(),
        geometry_invalid_values=(),
    )


def test_classifies_sections_from_explicit_policy():
    policy = TerritorialSectionPolicy(
        policy_id="TEST-POLICY",
        version="1.0",
        certified_lineage={
            10: (101, 102),
        },
        unresolved_historical=(20,),
        synthetic_candidates=(9001,),
    )

    result = classify_section_universes(
        build_profile(),
        policy,
    )

    assert result.certified_predecessors == (10,)
    assert result.certified_successors == (101, 102)
    assert result.unresolved_historical == (20,)
    assert result.synthetic_candidates == (9001,)
    assert result.unclassified_master_only == (30, 40)
    assert result.unexpected_geometry_only == ()


def test_does_not_infer_synthetic_status_from_number():
    policy = TerritorialSectionPolicy(
        policy_id="TEST-POLICY",
        version="1.0",
    )

    result = classify_section_universes(
        build_profile(),
        policy,
    )

    assert result.synthetic_candidates == ()
    assert 9001 in result.unclassified_master_only


def test_reports_unexpected_geometry_only_sections():
    policy = TerritorialSectionPolicy(
        policy_id="TEST-POLICY",
        version="1.0",
        certified_lineage={
            10: (101,),
        },
    )

    result = classify_section_universes(
        build_profile(),
        policy,
    )

    assert result.certified_successors == (101,)
    assert result.unexpected_geometry_only == (102,)


def test_rejects_overlapping_policy_categories():
    policy = TerritorialSectionPolicy(
        policy_id="INVALID-POLICY",
        version="1.0",
        certified_lineage={
            10: (101,),
        },
        unresolved_historical=(10,),
    )

    with pytest.raises(
        ValueError,
        match="categorías superpuestas",
    ):
        classify_section_universes(
            build_profile(),
            policy,
        )


def test_rejects_lineage_without_successors():
    policy = TerritorialSectionPolicy(
        policy_id="INVALID-POLICY",
        version="1.0",
        certified_lineage={
            10: (),
        },
    )

    with pytest.raises(
        ValueError,
        match="genealogías sin sucesores",
    ):
        classify_section_universes(
            build_profile(),
            policy,
        )


def test_policy_and_result_are_serializable():
    policy = TerritorialSectionPolicy(
        policy_id="TEST-POLICY",
        version="1.0",
        certified_lineage={
            10: (101, 102),
        },
        evidence_reference="GOVERNANCE-TEST",
    )

    result = classify_section_universes(
        build_profile(),
        policy,
    )

    assert policy.to_dict()["policy_id"] == "TEST-POLICY"
    assert result.to_dict()["certified_successors"] == (
        101,
        102,
    )
