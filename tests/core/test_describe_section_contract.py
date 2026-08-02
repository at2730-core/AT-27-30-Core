"""
Contrato Cognitivo de DescribeSectionCapability.
"""


from heyti.capabilities.describe_section.contract import (
    DescribeSectionContract,
)


def test_describe_section_contract_contains_all_domains():

    contract = DescribeSectionContract()

    assert contract.domains == [
        "territorial",
        "electoral",
        "socioeconomic",
        "field",
        "security",
        "risk",
        "recommendations",
    ]