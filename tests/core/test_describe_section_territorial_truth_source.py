import pytest

from heyti.audit.data_truth.baselines.guanajuato_2023 import (
    GUANAJUATO_2023_V1,
)
from heyti.audit.data_truth.contracts import (
    PUBLICATION_ALLOWED,
    PUBLICATION_BLOCKED,
)
from heyti.audit.data_truth.territorial_policy import (
    TerritorialClassification,
)
from heyti.capabilities.describe_section.provider import (
    DescribeSectionProvider,
)
from heyti.capabilities.describe_section.territorial_truth_source import (
    TerritorialSectionTruthSource,
)
from heyti.materialization.context import MaterializationContext
from heyti.materialization.describe_section.materializer import (
    DescribeSectionMaterializer,
)
from heyti.materialization.validator import (
    ResponseContractValidator,
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


def build_source() -> TerritorialSectionTruthSource:
    return TerritorialSectionTruthSource(
        classification=build_classification(),
        policy=GUANAJUATO_2023_V1,
    )


def test_source_rejects_invalid_classification():
    with pytest.raises(TypeError):
        TerritorialSectionTruthSource(
            classification={},
            policy=GUANAJUATO_2023_V1,
        )


def test_source_rejects_invalid_policy():
    with pytest.raises(TypeError):
        TerritorialSectionTruthSource(
            classification=build_classification(),
            policy={},
        )


def test_certified_successor_snapshot_is_allowed():
    snapshot = build_source().get_section_truth(
        section_id="3290",
    )

    assert snapshot.content["section_id"] == 3290
    assert (
        snapshot.content["classification"]
        == "CERTIFIED_SUCCESSOR"
    )
    assert (
        snapshot.content["publication_status"]
        == PUBLICATION_ALLOWED
    )
    assert snapshot.content["related_sections"] == (343,)
    assert snapshot.warnings == ()


def test_synthetic_snapshot_is_blocked_with_warning():
    snapshot = build_source().get_section_truth(
        section_id="9001",
    )

    assert (
        snapshot.content["classification"]
        == "SYNTHETIC_CANDIDATE"
    )
    assert (
        snapshot.content["publication_status"]
        == PUBLICATION_BLOCKED
    )
    assert len(snapshot.warnings) == 1
    assert snapshot.warnings[0].code == (
        "SYNTHETIC_SECTION_CANDIDATE"
    )


def test_historical_predecessor_exposes_certified_lineage():
    snapshot = build_source().get_section_truth(
        section_id="343",
    )

    assert (
        snapshot.content["classification"]
        == "CERTIFIED_PREDECESSOR"
    )
    assert snapshot.content["related_sections"] == tuple(
        range(3290, 3300)
    )
    assert snapshot.warnings[0].code == (
        "HISTORICAL_PREDECESSOR_SECTION"
    )


def test_unclassified_master_section_is_blocked():
    snapshot = build_source().get_section_truth(
        section_id="3486",
    )

    assert (
        snapshot.content["classification"]
        == "UNCLASSIFIED_MASTER_ONLY"
    )
    assert (
        snapshot.content["publication_status"]
        == PUBLICATION_BLOCKED
    )
    assert snapshot.warnings[0].code == (
        "UNCLASSIFIED_MASTER_SECTION"
    )


def test_invalid_section_id_is_propagated():
    with pytest.raises(ValueError):
        build_source().get_section_truth(
            section_id="ABC",
        )


def test_synthetic_section_reaches_materialized_warning():
    provider = DescribeSectionProvider(
        truth_source=build_source(),
    )
    description = provider.get_section(
        section_id="9001",
    )

    response = DescribeSectionMaterializer().materialize(
        description,
        MaterializationContext(
            capability_id="describe_section",
        ),
    )

    validated = ResponseContractValidator().validate(
        response
    )

    truth_block = next(
        block
        for block in response.blocks
        if block.role == "data_truth"
    )

    assert validated is response
    assert response.status == "success_with_warnings"
    assert response.warnings[0].code == (
        "SYNTHETIC_SECTION_CANDIDATE"
    )
    assert truth_block.content["section_id"] == 9001
    assert (
        truth_block.content["publication_status"]
        == PUBLICATION_BLOCKED
    )


def test_certified_successor_reaches_clean_materialization():
    provider = DescribeSectionProvider(
        truth_source=build_source(),
    )
    description = provider.get_section(
        section_id="3290",
    )

    response = DescribeSectionMaterializer().materialize(
        description,
        MaterializationContext(
            capability_id="describe_section",
        ),
    )

    validated = ResponseContractValidator().validate(
        response
    )

    assert validated is response
    assert response.status == "success"
    assert response.warnings == []
