from copy import deepcopy
from typing import Any, Protocol

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


class SectionTerritorialSource(Protocol):
    """Fuente contractual de contenido territorial."""

    def get_section_territorial(
        self,
        section_id: str,
    ) -> dict[str, Any] | None:
        """
        Devuelve contenido territorial autorizado o None.
        """
        ...


class DescribeSectionProvider:
    """
    Proveedor inicial de información para DescribeSection.

    Construye el modelo raíz, incorpora el estado de verdad
    y sólo publica contenido territorial cuando Data Truth
    lo autoriza explícitamente.
    """

    def __init__(
        self,
        truth_source: SectionTruthSource | None = None,
        territorial_source: (
            SectionTerritorialSource | None
        ) = None,
    ) -> None:
        self.truth_source = truth_source
        self.territorial_source = territorial_source

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

        if self.territorial_source is None:
            return description

        publication_status = (
            description.data_truth.get(
                "publication_status"
            )
        )

        if publication_status != "ALLOWED":
            return description

        territorial = (
            self.territorial_source
            .get_section_territorial(
                section_id=section_id,
            )
        )

        if territorial is None:
            return description

        if not isinstance(territorial, dict):
            raise TypeError(
                "SectionTerritorialSource debe devolver "
                "dict o None"
            )

        description.territorial = deepcopy(
            territorial
        )

        return description
