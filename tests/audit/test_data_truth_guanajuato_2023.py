from heyti.audit.data_truth.baselines.guanajuato_2023 import (
    GUANAJUATO_2023_CERTIFIED_LINEAGE,
    GUANAJUATO_2023_EVIDENCE,
    GUANAJUATO_2023_SYNTHETIC_CANDIDATES,
    GUANAJUATO_2023_UNRESOLVED_HISTORICAL,
    GUANAJUATO_2023_V1,
)


def test_baseline_identity_is_versioned():
    assert GUANAJUATO_2023_V1.policy_id == "GUANAJUATO_2023"
    assert GUANAJUATO_2023_V1.version == "1.0"


def test_baseline_contains_five_certified_predecessors():
    assert tuple(
        sorted(GUANAJUATO_2023_CERTIFIED_LINEAGE)
    ) == (
        343,
        1059,
        1110,
        1634,
        1647,
    )


def test_baseline_contains_36_unique_successors():
    successors = {
        successor
        for values in GUANAJUATO_2023_CERTIFIED_LINEAGE.values()
        for successor in values
    }

    assert len(successors) == 36
    assert successors == set(range(3278, 3314))


def test_baseline_preserves_exact_certified_lineage():
    assert GUANAJUATO_2023_CERTIFIED_LINEAGE == {
        343: tuple(range(3290, 3300)),
        1059: tuple(range(3300, 3308)),
        1110: tuple(range(3308, 3314)),
        1634: tuple(range(3278, 3284)),
        1647: tuple(range(3284, 3290)),
    }


def test_baseline_contains_26_unresolved_historical_sections():
    assert len(
        GUANAJUATO_2023_UNRESOLVED_HISTORICAL
    ) == 26

    assert set(
        GUANAJUATO_2023_UNRESOLVED_HISTORICAL
    ) == {
        145,
        315,
        336,
        878,
        892,
        899,
        966,
        1078,
        1099,
        1268,
        1285,
        1477,
        1490,
        1494,
        1495,
        1509,
        1614,
        1642,
        1681,
        1687,
        2190,
        2193,
        2477,
        2514,
        2860,
        2907,
    }


def test_baseline_contains_45_synthetic_candidates():
    assert len(
        GUANAJUATO_2023_SYNTHETIC_CANDIDATES
    ) == 45

    assert 9042 not in (
        GUANAJUATO_2023_SYNTHETIC_CANDIDATES
    )


def test_baseline_categories_do_not_overlap():
    predecessors = set(
        GUANAJUATO_2023_CERTIFIED_LINEAGE
    )
    historical = set(
        GUANAJUATO_2023_UNRESOLVED_HISTORICAL
    )
    synthetic = set(
        GUANAJUATO_2023_SYNTHETIC_CANDIDATES
    )

    assert predecessors.isdisjoint(historical)
    assert predecessors.isdisjoint(synthetic)
    assert historical.isdisjoint(synthetic)


def test_baseline_references_governance_evidence():
    assert (
        GUANAJUATO_2023_V1.evidence_reference
        == GUANAJUATO_2023_EVIDENCE
    )
    assert GUANAJUATO_2023_EVIDENCE.endswith(
        "HEYTI_Data_Truth_Governance_v1.0.md"
    )
