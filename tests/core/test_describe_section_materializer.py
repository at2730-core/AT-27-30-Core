import pytest

from heyti.capabilities.describe_section.models import (
    SectionDescription,
)
from heyti.materialization.context import MaterializationContext
from heyti.materialization.describe_section.materializer import (
    DescribeSectionMaterializer,
)
from heyti.materialization.errors import (
    MaterializationError,
    UnsupportedContractVersionError,
)
from heyti.materialization.validator import (
    ResponseContractValidator,
)


def test_describe_section_materializes_minimal_result():
    result = SectionDescription()
    result.section_id = "1234"

    context = MaterializationContext(
        capability_id="describe_section"
    )

    response = DescribeSectionMaterializer().materialize(
        result,
        context,
    )

    assert response.contract == "HEYTI_RESPONSE"
    assert response.version == "1.0"
    assert response.capability_id == "describe_section"
    assert response.status == "success"

    assert len(response.blocks) == 1
    assert response.blocks[0].type == "text"
    assert response.blocks[0].role == "section_identity"
    assert response.blocks[0].content == {
        "section_id": "1234"
    }


def test_describe_section_preserves_domain_values():
    result = SectionDescription()
    result.section_id = "1234"
    result.electoral = {
        "votes": 0,
        "competitive": False,
    }

    context = MaterializationContext(
        capability_id="describe_section"
    )

    response = DescribeSectionMaterializer().materialize(
        result,
        context,
    )

    electoral_block = next(
        block
        for block in response.blocks
        if block.role == "electoral"
    )

    assert electoral_block.content["votes"] == 0
    assert electoral_block.content["competitive"] is False


def test_describe_section_preserves_recommendations():
    result = SectionDescription()
    result.section_id = "1234"
    result.recommendations = [
        "Recomendación A",
        "Recomendación B",
    ]

    context = MaterializationContext(
        capability_id="describe_section"
    )

    response = DescribeSectionMaterializer().materialize(
        result,
        context,
    )

    recommendations_block = next(
        block
        for block in response.blocks
        if block.role == "recommendations"
    )

    assert recommendations_block.content == [
        "Recomendación A",
        "Recomendación B",
    ]


def test_describe_section_preserves_traceability():
    result = SectionDescription()
    result.section_id = "1234"

    context = MaterializationContext(
        capability_id="describe_section",
        request_id="REQ-1",
        session_id="SES-1",
        execution_id="EXE-1",
        knowledge_version="K-1",
    )

    response = DescribeSectionMaterializer().materialize(
        result,
        context,
    )

    assert response.trace.request_id == "REQ-1"
    assert response.trace.session_id == "SES-1"
    assert response.trace.execution_id == "EXE-1"
    assert response.trace.knowledge_version == "K-1"


def test_describe_section_does_not_fabricate_traceability():
    result = SectionDescription()
    result.section_id = "1234"

    context = MaterializationContext(
        capability_id="describe_section"
    )

    response = DescribeSectionMaterializer().materialize(
        result,
        context,
    )

    assert response.trace.request_id is None
    assert response.trace.session_id is None
    assert response.trace.execution_id is None
    assert response.trace.knowledge_version is None


def test_describe_section_rejects_invalid_result_type():
    context = MaterializationContext(
        capability_id="describe_section"
    )

    with pytest.raises(MaterializationError):
        DescribeSectionMaterializer().materialize(
            {"section_id": "1234"},
            context,
        )


def test_describe_section_rejects_unsupported_contract_version():
    result = SectionDescription()
    result.section_id = "1234"

    context = MaterializationContext(
        capability_id="describe_section",
        contract_version="2.0",
    )

    with pytest.raises(UnsupportedContractVersionError):
        DescribeSectionMaterializer().materialize(
            result,
            context,
        )


def test_describe_section_materialized_response_passes_validator():
    result = SectionDescription()
    result.section_id = "1234"

    context = MaterializationContext(
        capability_id="describe_section"
    )

    response = DescribeSectionMaterializer().materialize(
        result,
        context,
    )

    validated = ResponseContractValidator().validate(response)

    assert validated is response

def test_internal_fields_are_not_materialized():
    result = SectionDescription()
    result.section_id = "1234"

    result.internal_secret = "DO_NOT_EXPOSE"
    result.debug_state = {
        "raw_query": "internal",
    }

    context = MaterializationContext(
        capability_id="describe_section"
    )

    response = DescribeSectionMaterializer().materialize(
        result,
        context,
    )

    serialized = response.to_dict()

    assert "internal_secret" not in str(serialized)
    assert "debug_state" not in str(serialized)
    assert "DO_NOT_EXPOSE" not in str(serialized)


def test_materializer_uses_explicit_known_fields_only():
    result = SectionDescription()
    result.section_id = "1234"
    result.territorial = {
        "municipality": "León",
    }

    result.unexpected_domain = {
        "value": 999,
    }

    context = MaterializationContext(
        capability_id="describe_section"
    )

    response = DescribeSectionMaterializer().materialize(
        result,
        context,
    )

    roles = {
        block.role
        for block in response.blocks
    }

    assert "section_identity" in roles
    assert "territorial" in roles
    assert "unexpected_domain" not in roles

def test_materialized_domain_isolated_from_source_mutation():
    result = SectionDescription()
    result.section_id = "1234"
    result.electoral = {
        "votes": 100,
        "details": {
            "competitive": True,
        },
    }

    context = MaterializationContext(
        capability_id="describe_section"
    )

    response = DescribeSectionMaterializer().materialize(
        result,
        context,
    )

    electoral_block = next(
        block
        for block in response.blocks
        if block.role == "electoral"
    )

    result.electoral["votes"] = 999
    result.electoral["details"]["competitive"] = False

    assert electoral_block.content == {
        "votes": 100,
        "details": {
            "competitive": True,
        },
    }


def test_materialized_recommendations_isolated_from_source_mutation():
    result = SectionDescription()
    result.section_id = "1234"
    result.recommendations = [
        {
            "text": "Recomendación original",
            "metadata": {
                "priority": 1,
            },
        }
    ]

    context = MaterializationContext(
        capability_id="describe_section"
    )

    response = DescribeSectionMaterializer().materialize(
        result,
        context,
    )

    recommendations_block = next(
        block
        for block in response.blocks
        if block.role == "recommendations"
    )

    result.recommendations[0]["text"] = "MODIFICADA"
    result.recommendations[0]["metadata"]["priority"] = 999
    result.recommendations.append(
        {
            "text": "Nueva",
        }
    )

    assert recommendations_block.content == [
        {
            "text": "Recomendación original",
            "metadata": {
                "priority": 1,
            },
        }
    ]
