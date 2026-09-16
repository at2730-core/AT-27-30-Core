import pytest

from heyti.audit.data_truth.baselines.guanajuato_2023 import (
    GUANAJUATO_2023_V1,
)
from heyti.audit.data_truth.contracts import (
    PUBLICATION_ALLOWED,
    PUBLICATION_BLOCKED,
    PUBLICATION_HISTORICAL_ONLY,
    TRUTH_OBSERVED,
    TRUTH_UNRESOLVED,
    TRUTH_UNVERIFIED,
)
from heyti.audit.data_truth.section_truth import (
    CLASSIFICATION_CERTIFIED_PREDECESSOR,
    CLASSIFICATION_CERTIFIED_SUCCESSOR,
    CLASSIFICATION_REQUIRES_REPOSITORY_CONFIRMATION,
    CLASSIFICATION_SYNTHETIC_CANDIDATE,
    CLASSIFICATION_UNCLASSIFIED_MASTER_ONLY,
    CLASSIFICATION_UNEXPECTED_GEOMETRY_ONLY,
    CLASSIFICATION_UNRESOLVED_HISTORICAL,
    resolve_section_truth,
)
from heyti.audit.data_truth.territorial_policy import (
    TerritorialClassification,
)


def build_classification() -> TerritorialClassification:
    return TerritorialClassification(
        certified_predecessors=(
            343,
            1059,
            1110,
            1634,
            1647,
        ),
        certified_successors=tuple(
            range(3278, 3314)
        ),
        unresolved_historical=(
            145,
            315,
        ),
        synthetic_candidates=(
            9001,
            9002,
        ),
        unclassified_master_only=(
            3486,
            4986,
        ),
        unexpected_geometry_only=(
            7777,
        ),
    )


def resolve(section_id):
    return resolve_section_truth(
        section_id=section_id,
        classification=build_classification(),
        policy=GUANAJUATO_2023_V1,
    )


def test_certified_predecessor_is_historical_only():
    resolution = resolve(343)

    assert (
        resolution.classification
        == CLASSIFICATION_CERTIFIED_PREDECESSOR
    )
    assert resolution.truth_status == TRUTH_OBSERVED
    assert (
        resolution.publication_status
        == PUBLICATION_HISTORICAL_ONLY
    )
    assert resolution.related_sections == tuple(
        range(3290, 3300)
    )
    assert resolution.warning_code == (
        "HISTORICAL_PREDECESSOR_SECTION"
    )


def test_certified_successor_is_allowed():
    resolution = resolve("3290")

    assert (
        resolution.classification
        == CLASSIFICATION_CERTIFIED_SUCCESSOR
    )
    assert resolution.truth_status == TRUTH_OBSERVED
    assert (
        resolution.publication_status
        == PUBLICATION_ALLOWED
    )
    assert resolution.related_sections == (343,)
    assert resolution.warning_code is None


def test_unresolved_historical_section_is_blocked():
    resolution = resolve(145)

    assert (
        resolution.classification
        == CLASSIFICATION_UNRESOLVED_HISTORICAL
    )
    assert resolution.truth_status == TRUTH_UNRESOLVED
    assert (
        resolution.publication_status
        == PUBLICATION_BLOCKED
    )
    assert (
        resolution.warning_code
        == "UNRESOLVED_HISTORICAL_SECTION"
    )


def test_synthetic_candidate_is_unverified_and_blocked():
    resolution = resolve(9001)

    assert (
        resolution.classification
        == CLASSIFICATION_SYNTHETIC_CANDIDATE
    )
    assert resolution.truth_status == TRUTH_UNVERIFIED
    assert (
        resolution.publication_status
        == PUBLICATION_BLOCKED
    )
    assert (
        resolution.warning_code
        == "SYNTHETIC_SECTION_CANDIDATE"
    )


def test_unclassified_master_section_is_blocked():
    resolution = resolve(3486)

    assert (
        resolution.classification
        == CLASSIFICATION_UNCLASSIFIED_MASTER_ONLY
    )
    assert resolution.truth_status == TRUTH_UNRESOLVED
    assert (
        resolution.publication_status
        == PUBLICATION_BLOCKED
    )
    assert (
        resolution.warning_code
        == "UNCLASSIFIED_MASTER_SECTION"
    )


def test_unexpected_geometry_section_is_blocked():
    resolution = resolve(7777)

    assert (
        resolution.classification
        == CLASSIFICATION_UNEXPECTED_GEOMETRY_ONLY
    )
    assert resolution.truth_status == TRUTH_UNRESOLVED
    assert (
        resolution.publication_status
        == PUBLICATION_BLOCKED
    )
    assert (
        resolution.warning_code
        == "UNEXPECTED_GEOMETRY_SECTION"
    )


def test_normal_section_requires_repository_confirmation():
    resolution = resolve(1524)

    assert resolution.classification == (
        CLASSIFICATION_REQUIRES_REPOSITORY_CONFIRMATION
    )
    assert resolution.truth_status == TRUTH_UNVERIFIED
    assert (
        resolution.publication_status
        == PUBLICATION_BLOCKED
    )
    assert resolution.warning_code == (
        "SECTION_REQUIRES_REPOSITORY_CONFIRMATION"
    )


def test_resolution_serializes_policy_identity():
    data = resolve(3290).to_dict()

    assert data["section_id"] == 3290
    assert data["policy_id"] == "GUANAJUATO_2023"
    assert data["policy_version"] == "1.0"
    assert data["evidence_reference"].endswith(
        "HEYTI_Data_Truth_Governance_v1.0.md"
    )


@pytest.mark.parametrize(
    "invalid_section_id",
    [
        None,
        "",
        "ABC",
        0,
        -1,
        1.5,
        True,
    ],
)
def test_invalid_section_id_is_rejected(
    invalid_section_id,
):
    with pytest.raises(ValueError):
        resolve(invalid_section_id)
