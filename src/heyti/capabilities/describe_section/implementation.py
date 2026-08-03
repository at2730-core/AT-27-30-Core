from heyti.capabilities.base import Capability
from heyti.capabilities.describe_section.provider import (
    DescribeSectionProvider,
)


class DescribeSectionCapability(Capability):
    """
    Capability ejecutable para construir la descripción
    integrada de una sección electoral.
    """

    def __init__(
        self,
        provider: DescribeSectionProvider | None = None,
    ) -> None:
        self.provider = provider or DescribeSectionProvider()

    def execute(
        self,
        session=None,
        payload=None,
        section_id: str | None = None,
    ):
        resolved_section_id = section_id

        if resolved_section_id is None and payload is not None:
            resolved_section_id = payload.get(
                "section_id"
            )

        if resolved_section_id is None:
            raise ValueError(
                "section_id es obligatorio"
            )

        return self.provider.get_section(
            section_id=resolved_section_id,
        )