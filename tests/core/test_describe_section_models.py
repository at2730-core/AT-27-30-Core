"""
Modelos cognitivos de DescribeSection.
"""

from heyti.capabilities.describe_section.models import (
    SectionDescription,
)


def test_section_description_starts_empty():

    description = SectionDescription()

    assert description.section_id is None

    assert description.territorial is None
    assert description.electoral is None
    assert description.socioeconomic is None
    assert description.field is None
    assert description.security is None
    assert description.risk is None

    assert description.recommendations == []