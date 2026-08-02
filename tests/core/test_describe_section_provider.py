"""
Pruebas del Provider de DescribeSection.
"""

from heyti.capabilities.describe_section.models import (
    SectionDescription,
)
from heyti.capabilities.describe_section.provider import (
    DescribeSectionProvider,
)


def test_describe_section_provider_returns_section_description():
    provider = DescribeSectionProvider()

    description = provider.get_section(
        section_id="1524",
    )

    assert isinstance(
        description,
        SectionDescription,
    )

    assert description.section_id == "1524"