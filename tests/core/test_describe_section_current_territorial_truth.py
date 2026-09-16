import pytest

from heyti.audit.data_truth.baselines.guanajuato_2023 import (
    GUANAJUATO_2023_V1,
)
from heyti.audit.data_truth.contracts import (
    PUBLICATION_ALLOWED,
    PUBLICATION_BLOCKED,
    PUBLICATION_HISTORICAL_ONLY,
    TRUTH_OBSERVED,
)
from heyti.audit.data_truth.territorial_policy import (
    TerritorialClassification,
)
from heyti.capabilities.describe_section.provider import (
    DescribeSectionProvider,
)
from heyti.capabilities.describe_section.territorial_truth_source import (
    CLASSIFICATION_CURRENT_TERRITORIAL_SECTION,
    CONFIRMATION_MASTER_AND_GEOMETRY,
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
        certified_predecessors=(343,),
        certified_successors=tuple(
            range(3290, 3300)
        ),
        unresolved_historical=(145,),
        synthetic_candidates=(9001,),
        unclassified_master_only=(3486,),
        unexpected_geometry_only=(),
    )


def build_source(
    current_section_ids=(1524, 2788),
) -> TerritorialSectionTruthSource:
    return TerritorialSectionTruthSource(
        classification=build_classification(),
        policy=GUANAJUATO_2023_V1,
        current_section_ids=current_section_ids,
    )


def test_confirmed_current_section_is_allowed():
    snapshot = build_source().get_section_truth(
        section_id="1524",
    )

    assert snapshot.content["classification"] == (
        CLASSIFICATION_CURRENT_TERRITORIAL_SECTION
    )
    assert snapshot.content["truth_status"] == TRUTH_OBSERVED
    assert (
        snapshot.content["publication_status"]
        == PUBLICATION_ALLOWED
    )
    assert snapshot.content["confirmation_basis"] == (
        CONFIRMATION_MASTER_AND_GEOMETRY
    )
    assert snapshot.content["warning_code"] is None
    assert snapshot.content["warning_message"] is None
    assert snapshot.warnings == ()


def test_current_section_reaches_clean_materialization():
    description = DescribeSectionProvider(
        truth_source=build_source(),
    ).get_section(
        section_id="1524",
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
    assert response.status == "success"
    assert response.warnings == []
    assert truth_block.content["classification"] == (
        CLASSIFICATION_CURRENT_TERRITORIAL_SECTION
    )


def test_synthetic_exception_cannot_be_unblocked():
    source = build_source(
        current_section_ids=(1524, 9001),
    )

    snapshot = source.get_section_truth(
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


def test_historical_predecessor_remains_historical_only():
    source = build_source(
        current_section_ids=(343, 1524),
    )

    snapshot = source.get_section_truth(
        section_id="343",
    )

    assert (
        snapshot.content["classification"]
        == "CERTIFIED_PREDECESSOR"
    )
    assert snapshot.content["publication_status"] == (
        PUBLICATION_HISTORICAL_ONLY
    )
    assert len(snapshot.warnings) == 1


def test_source_rejects_non_tuple_current_sections():
    with pytest.raises(TypeError):
        TerritorialSectionTruthSource(
            classification=build_classification(),
            policy=GUANAJUATO_2023_V1,
            current_section_ids=[1524],
        )


@pytest.mark.parametrize(
    "invalid_section_id",
    [
        True,
        0,
        -1,
        "1524",
    ],
)
def test_source_rejects_invalid_current_section_members(
    invalid_section_id,
):
    with pytest.raises(ValueError):
        build_source(
            current_section_ids=(invalid_section_id,),
        )
