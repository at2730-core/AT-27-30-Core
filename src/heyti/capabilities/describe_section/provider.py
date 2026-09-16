from copy import deepcopy
from typing import Protocol

from heyti.capabilities.describe_section.models import (
    SectionDescription,
    SectionTruthSnapshot,
)


class SectionTruthSource(Protocol):
    """Fuente contractual de verdad para una sección."""

    def get_section_truth(
        self,
        section_id: str,
    ) -> SectionTruthSnapshot:
        """Devuelve el estado de verdad disponible."""
        ...


class DescribeSectionProvider:
    """
    Proveedor inicial de información para DescribeSection.

    Construye el modelo raíz y puede incorporar un estado de verdad
    mediante una fuente contractual inyectada.
    """

    def __init__(
        self,
        truth_source: SectionTruthSource | None = None,
    ) -> None:
        self.truth_source = truth_source

    def get_section(
        self,
        section_id: str,
    ) -> SectionDescription:
        description = SectionDescription()
        description.section_id = section_id

        if self.truth_source is None:
            return description

        snapshot = self.truth_source.get_section_truth(
            section_id=section_id,
        )

        if not isinstance(snapshot, SectionTruthSnapshot):
            raise TypeError(
                "SectionTruthSource debe devolver "
                "SectionTruthSnapshot"
            )

        description.data_truth = deepcopy(snapshot.content)
        description.warnings = list(snapshot.warnings)

        return description
