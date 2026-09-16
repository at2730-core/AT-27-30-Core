import pytest

from heyti.capabilities.describe_section.models import (
    SectionTruthSnapshot,
    SectionWarning,
)
from heyti.capabilities.describe_section.provider import (
    DescribeSectionProvider,
)


class FakeTruthSource:
    def __init__(self, snapshot):
        self.snapshot = snapshot
        self.requested_section_ids = []

    def get_section_truth(self, section_id):
        self.requested_section_ids.append(section_id)
        return self.snapshot


def test_provider_preserves_behavior_without_truth_source():
    description = DescribeSectionProvider().get_section(
        section_id="1524",
    )

    assert description.section_id == "1524"
    assert description.data_truth is None
    assert description.warnings == []


def test_provider_injects_truth_content_and_warning():
    warning = SectionWarning(
        code="SYNTHETIC_SECTION_CANDIDATE",
        message="La sección no está certificada.",
    )
    snapshot = SectionTruthSnapshot(
        content={
            "classification": "SYNTHETIC_CANDIDATE",
            "publication_status": "BLOCKED",
        },
        warnings=(warning,),
    )
    source = FakeTruthSource(snapshot)

    description = DescribeSectionProvider(
        truth_source=source,
    ).get_section(
        section_id="9001",
    )

    assert source.requested_section_ids == ["9001"]
    assert description.data_truth == {
        "classification": "SYNTHETIC_CANDIDATE",
        "publication_status": "BLOCKED",
    }
    assert description.warnings == [warning]


def test_provider_copies_truth_content_defensively():
    snapshot = SectionTruthSnapshot(
        content={
            "classification": "CERTIFIED_SUCCESSOR",
            "evidence": {
                "policy_id": "GUANAJUATO_2023",
            },
        },
    )
    source = FakeTruthSource(snapshot)

    description = DescribeSectionProvider(
        truth_source=source,
    ).get_section(
        section_id="3290",
    )

    snapshot.content["classification"] = "MODIFIED"
    snapshot.content["evidence"]["policy_id"] = "MODIFIED"

    assert description.data_truth == {
        "classification": "CERTIFIED_SUCCESSOR",
        "evidence": {
            "policy_id": "GUANAJUATO_2023",
        },
    }


def test_provider_copies_warning_collection():
    warning = SectionWarning(
        code="TEST_WARNING",
        message="Advertencia controlada.",
    )
    snapshot = SectionTruthSnapshot(
        content={
            "status": "UNVERIFIED",
        },
        warnings=(warning,),
    )

    description = DescribeSectionProvider(
        truth_source=FakeTruthSource(snapshot),
    ).get_section(
        section_id="1524",
    )

    description.warnings.clear()

    assert snapshot.warnings == (warning,)


def test_provider_rejects_invalid_source_result():
    source = FakeTruthSource(
        {
            "classification": "INVALID",
        }
    )

    with pytest.raises(TypeError):
        DescribeSectionProvider(
            truth_source=source,
        ).get_section(
            section_id="1524",
        )


def test_snapshot_rejects_non_dictionary_content():
    with pytest.raises(TypeError):
        SectionTruthSnapshot(
            content=[],
        )


def test_snapshot_rejects_non_tuple_warnings():
    with pytest.raises(TypeError):
        SectionTruthSnapshot(
            content={},
            warnings=[],
        )


def test_snapshot_rejects_untyped_warning():
    with pytest.raises(TypeError):
        SectionTruthSnapshot(
            content={},
            warnings=(
                {
                    "code": "INVALID",
                    "message": "Sin contrato.",
                },
            ),
        )
