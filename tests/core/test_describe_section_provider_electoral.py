from heyti.capabilities.describe_section.models import (
    SectionTruthSnapshot,
)
from heyti.capabilities.describe_section.provider import (
    DescribeSectionProvider,
)


class TruthSource:
    def __init__(
        self,
        publication_status="ALLOWED",
    ):
        self.publication_status = publication_status

    def get_section_truth(
        self,
        section_id,
    ):
        return SectionTruthSnapshot(
            content={
                "section_id": section_id,
                "publication_status": (
                    self.publication_status
                ),
            }
        )


class ElectoralSource:
    def __init__(
        self,
        result,
    ):
        self.result = result
        self.requests = []

    def get_section_electoral(
        self,
        section_id,
    ):
        self.requests.append(section_id)
        return self.result


def electoral_content():
    return {
        "section_id": "1",
        "election_year": 2024,
        "coverage_scope": "TRACKED_PARTIES_ONLY",
        "quality_status": "COMPLETE",
        "contests": {
            "A": {
                "data_status": "AVAILABLE",
                "leading_tracked_party": "PRI",
            }
        },
    }


def test_provider_injects_authorized_electoral_content():
    electoral_source = ElectoralSource(
        electoral_content()
    )
    provider = DescribeSectionProvider(
        truth_source=TruthSource(),
        electoral_source=electoral_source,
    )

    description = provider.get_section("1")

    assert electoral_source.requests == ["1"]
    assert description.electoral == (
        electoral_content()
    )


def test_provider_copies_electoral_content():
    source_content = electoral_content()
    electoral_source = ElectoralSource(
        source_content
    )
    provider = DescribeSectionProvider(
        truth_source=TruthSource(),
        electoral_source=electoral_source,
    )

    description = provider.get_section("1")
    description.electoral["contests"]["A"][
        "leading_tracked_party"
    ] = "ALTERED"

    assert source_content["contests"]["A"][
        "leading_tracked_party"
    ] == "PRI"


def test_provider_does_not_request_blocked_electoral():
    electoral_source = ElectoralSource(
        electoral_content()
    )
    provider = DescribeSectionProvider(
        truth_source=TruthSource(
            publication_status="BLOCKED"
        ),
        electoral_source=electoral_source,
    )

    description = provider.get_section("9001")

    assert electoral_source.requests == []
    assert description.electoral is None


def test_provider_does_not_publish_without_truth_source():
    electoral_source = ElectoralSource(
        electoral_content()
    )
    provider = DescribeSectionProvider(
        electoral_source=electoral_source,
    )

    description = provider.get_section("1")

    assert electoral_source.requests == []
    assert description.electoral is None


def test_provider_allows_authorized_missing_electoral():
    electoral_source = ElectoralSource(None)
    provider = DescribeSectionProvider(
        truth_source=TruthSource(),
        electoral_source=electoral_source,
    )

    description = provider.get_section("1")

    assert electoral_source.requests == ["1"]
    assert description.electoral is None


def test_provider_rejects_invalid_electoral_result():
    electoral_source = ElectoralSource(
        ["invalid"]
    )
    provider = DescribeSectionProvider(
        truth_source=TruthSource(),
        electoral_source=electoral_source,
    )

    try:
        provider.get_section("1")
    except TypeError as error:
        assert str(error) == (
            "SectionElectoralSource debe devolver "
            "dict o None"
        )
    else:
        raise AssertionError(
            "Se esperaba TypeError"
        )

def test_provider_warns_about_partial_electoral_content():
    partial_content = electoral_content()
    partial_content["quality_status"] = "PARTIAL"

    electoral_source = ElectoralSource(
        partial_content
    )
    provider = DescribeSectionProvider(
        truth_source=TruthSource(),
        electoral_source=electoral_source,
    )

    description = provider.get_section("1524")

    assert description.electoral is not None
    assert len(description.warnings) == 1
    assert description.warnings[0].code == (
        "PARTIAL_ELECTORAL_COVERAGE"
    )
    assert description.warnings[0].message == (
        "La sección contiene uno o más concursos "
        "electorales sin cobertura completa y positiva."
    )
