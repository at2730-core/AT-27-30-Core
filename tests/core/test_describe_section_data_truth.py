import pytest

from heyti.capabilities.describe_section.models import (
    SectionDescription,
    SectionWarning,
)
from heyti.materialization.context import MaterializationContext
from heyti.materialization.describe_section.materializer import (
    DescribeSectionMaterializer,
)
from heyti.materialization.errors import MaterializationError
from heyti.materialization.validator import (
    ResponseContractValidator,
)


def build_context() -> MaterializationContext:
    return MaterializationContext(
        capability_id="describe_section",
    )


def test_section_description_starts_without_truth_findings():
    result = SectionDescription()

    assert result.data_truth is None
    assert result.warnings == []


def test_materializer_preserves_data_truth_block():
    result = SectionDescription()
    result.section_id = "1524"
    result.data_truth = {
        "status": "CERTIFIED",
        "policy_id": "GUANAJUATO_2023",
    }

    response = DescribeSectionMaterializer().materialize(
        result,
        build_context(),
    )

    truth_block = next(
        block
        for block in response.blocks
        if block.role == "data_truth"
    )

    assert truth_block.type == "metadata"
    assert truth_block.content == {
        "status": "CERTIFIED",
        "policy_id": "GUANAJUATO_2023",
    }


def test_materializer_preserves_typed_warning():
    result = SectionDescription()
    result.section_id = "3486"
    result.warnings = [
        SectionWarning(
            code="UNRESOLVED_TERRITORIAL_IDENTITY",
            message=(
                "La identidad territorial de la sección "
                "no está certificada."
            ),
        )
    ]

    response = DescribeSectionMaterializer().materialize(
        result,
        build_context(),
    )

    assert response.status == "success_with_warnings"
    assert len(response.warnings) == 1
    assert (
        response.warnings[0].code
        == "UNRESOLVED_TERRITORIAL_IDENTITY"
    )

    validated = ResponseContractValidator().validate(response)

    assert validated is response


def test_materializer_rejects_untyped_warning():
    result = SectionDescription()
    result.section_id = "3486"
    result.warnings = [
        {
            "code": "INVALID_WARNING",
            "message": "Advertencia sin contrato.",
        }
    ]

    with pytest.raises(MaterializationError):
        DescribeSectionMaterializer().materialize(
            result,
            build_context(),
        )


def test_materialized_data_truth_isolated_from_source_mutation():
    result = SectionDescription()
    result.section_id = "1524"
    result.data_truth = {
        "status": "CERTIFIED",
        "evidence": {
            "source": "territorial-baseline",
        },
    }

    response = DescribeSectionMaterializer().materialize(
        result,
        build_context(),
    )

    truth_block = next(
        block
        for block in response.blocks
        if block.role == "data_truth"
    )

    result.data_truth["status"] = "MODIFIED"
    result.data_truth["evidence"]["source"] = "modified-source"

    assert truth_block.content == {
        "status": "CERTIFIED",
        "evidence": {
            "source": "territorial-baseline",
        },
    }
