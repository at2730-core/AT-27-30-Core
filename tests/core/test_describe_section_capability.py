"""
Pruebas de la capability DescribeSection.
"""

from heyti.capabilities.describe_section.implementation import (
    DescribeSectionCapability,
)


def test_describe_section_capability_returns_section_description():

    capability = DescribeSectionCapability()

    result = capability.execute(
        section_id="1524",
    )

    assert result.section_id == "1524"