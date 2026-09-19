import pytest

from heyti.capabilities.describe_section.models import (
    SectionTruthSnapshot,
)
from heyti.capabilities.describe_section.provider import (
    DescribeSectionProvider,
)


class StaticTruthSource:
    def __init__(
        self,
        publication_status: str,
    ) -> None:
        self.publication_status = publication_status

    def get_section_truth(
        self,
        section_id: str,
    ) -> SectionTruthSnapshot:
        return SectionTruthSnapshot(
            content={
                "section_id": section_id,
                "classification": "TEST",
                "publication_status": (
                    self.publication_status
                ),
            }
        )


class TrackingTerritorialSource:
    def __init__(self, content) -> None:
        self.content = content
        self.requested_section_ids: list[str] = []

    def get_section_territorial(
        self,
        section_id: str,
    ):
        self.requested_section_ids.append(section_id)
        return self.content


def allowed_truth_source() -> StaticTruthSource:
    return StaticTruthSource(
        publication_status="ALLOWED",
    )


def test_provider_injects_authorized_territorial_content():
    territorial_content = {
        "section_id": "1524",
        "crs": "OGC:CRS84",
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [
                [],
            ],
        },
    }
    territorial_source = TrackingTerritorialSource(
        territorial_content
    )
    provider = DescribeSectionProvider(
        truth_source=allowed_truth_source(),
        territorial_source=territorial_source,
    )

    description = provider.get_section("1524")

    assert description.territorial == (
        territorial_content
    )
    assert territorial_source.requested_section_ids == [
        "1524",
    ]


def test_provider_copies_territorial_content():
    territorial_content = {
        "section_id": "1524",
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [
                [
                    "original",
                ],
            ],
        },
    }
    provider = DescribeSectionProvider(
        truth_source=allowed_truth_source(),
        territorial_source=TrackingTerritorialSource(
            territorial_content
        ),
    )

    description = provider.get_section("1524")

    assert description.territorial is not None

    description.territorial[
        "geometry"
    ]["coordinates"].clear()

    assert territorial_content["geometry"][
        "coordinates"
    ] == [
        [
            "original",
        ],
    ]


def test_provider_does_not_request_blocked_geometry():
    territorial_source = TrackingTerritorialSource(
        {
            "forbidden": True,
        }
    )
    provider = DescribeSectionProvider(
        truth_source=StaticTruthSource(
            publication_status="BLOCKED",
        ),
        territorial_source=territorial_source,
    )

    description = provider.get_section("9001")

    assert description.territorial is None
    assert territorial_source.requested_section_ids == []


def test_provider_does_not_publish_without_truth_source():
    territorial_source = TrackingTerritorialSource(
        {
            "forbidden": True,
        }
    )
    provider = DescribeSectionProvider(
        territorial_source=territorial_source,
    )

    description = provider.get_section("1524")

    assert description.territorial is None
    assert description.data_truth is None
    assert territorial_source.requested_section_ids == []


def test_provider_allows_authorized_missing_geometry():
    territorial_source = TrackingTerritorialSource(
        None
    )
    provider = DescribeSectionProvider(
        truth_source=allowed_truth_source(),
        territorial_source=territorial_source,
    )

    description = provider.get_section("1524")

    assert description.territorial is None
    assert territorial_source.requested_section_ids == [
        "1524",
    ]


def test_provider_rejects_invalid_territorial_result():
    provider = DescribeSectionProvider(
        truth_source=allowed_truth_source(),
        territorial_source=TrackingTerritorialSource(
            [
                "invalid",
            ]
        ),
    )

    with pytest.raises(
        TypeError,
        match="debe devolver dict o None",
    ):
        provider.get_section("1524")
