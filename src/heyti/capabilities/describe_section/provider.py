from copy import deepcopy
from typing import Any, Protocol
from heyti.capabilities.describe_section.electoral_query import validate_section_request
from heyti.capabilities.describe_section.versioned_electoral_source import ReadRequest

from heyti.capabilities.describe_section.models import (
    SectionDescription,
    SectionTruthSnapshot,
    SectionWarning,
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


class SectionElectoralSource(Protocol):
    """Fuente contractual de contenido electoral."""

    def get_section_electoral(
        self,
        section_id: str,
    ) -> dict[str, Any] | None:
        """
        Devuelve contenido electoral autorizado o None.
        """
        ...


class SectionVersionedElectoralSource(Protocol):
    def read(self, request: ReadRequest) -> dict[str, Any]:
        ...


class DescribeSectionProvider:
    """
    Proveedor inicial de información para DescribeSection.

    Construye el modelo raíz, incorpora el estado de verdad
    y sólo publica dominios cuando Data Truth los autoriza
    explícitamente.
    """

    def __init__(
        self,
        truth_source: SectionTruthSource | None = None,
        territorial_source: (
            SectionTerritorialSource | None
        ) = None,
        electoral_source: (
            SectionElectoralSource | None
        ) = None,
        versioned_electoral_source: SectionVersionedElectoralSource | None = None,
    ) -> None:
        self.truth_source = truth_source
        self.territorial_source = territorial_source
        self.electoral_source = electoral_source
        self.versioned_electoral_source = versioned_electoral_source

    def get_section(
        self,
        section_id: str,
        electoral_request: ReadRequest | None = None,
    ) -> SectionDescription:
        description = SectionDescription()
        description.section_id = section_id
        if electoral_request is not None:
            validate_section_request(section_id, electoral_request)
            description.electoral_versioned = {
                "status": "DATA_TRUTH_NOT_ALLOWED", "data": None,
                "purpose": "PRESENTATION", "metric_scope": electoral_request.metric_scope,
            }

        if self.truth_source is None:
            if electoral_request is not None:
                description.warnings.append(SectionWarning(
                    code="VERSIONED_ELECTORAL_UNAVAILABLE",
                    message="Resultado electoral versionado bloqueado por Data Truth.",
                ))
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

        publication_status = (
            description.data_truth.get(
                "publication_status"
            )
        )

        if publication_status != "ALLOWED":
            if electoral_request is not None:
                description.warnings.append(SectionWarning(
                    code="VERSIONED_ELECTORAL_UNAVAILABLE",
                    message="Resultado electoral versionado bloqueado por Data Truth.",
                ))
            return description

        if self.territorial_source is not None:
            territorial = (
                self.territorial_source
                .get_section_territorial(
                    section_id=section_id,
                )
            )

            if territorial is not None:
                if not isinstance(territorial, dict):
                    raise TypeError(
                        "SectionTerritorialSource debe "
                        "devolver dict o None"
                    )

                description.territorial = deepcopy(
                    territorial
                )

        if electoral_request is not None:
            if self.versioned_electoral_source is None:
                response = {
                    "status": "VERSIONED_SOURCE_NOT_CONFIGURED", "data": None,
                    "purpose": "PRESENTATION", "metric_scope": electoral_request.metric_scope,
                }
            else:
                response = self.versioned_electoral_source.read(electoral_request)
                if (not isinstance(response, dict)
                        or response.get("purpose") != "PRESENTATION"
                        or response.get("metric_scope") != electoral_request.metric_scope
                        or "data" not in response or not isinstance(response.get("status"), str)):
                    raise TypeError("Invalid versioned presentation response")
                if response["data"] is not None and (
                    response["status"] != "SELECTED_RESULT"
                    or response.get("selection_status") != "SELECTED"
                    or response.get("certification_status") != "CERTIFIED"
                ):
                    raise ValueError("Unselected electoral data cannot enter DescribeSection")
            description.electoral_versioned = deepcopy(response)
            if response["data"] is None:
                description.warnings.append(SectionWarning(
                    code="VERSIONED_ELECTORAL_UNAVAILABLE",
                    message="Resultado electoral versionado no disponible: " + response["status"],
                ))
        elif self.electoral_source is not None:
            electoral = (
                self.electoral_source
                .get_section_electoral(
                    section_id=section_id,
                )
            )

            if electoral is not None:
                if not isinstance(electoral, dict):
                    raise TypeError(
                        "SectionElectoralSource debe "
                        "devolver dict o None"
                    )

                description.electoral = deepcopy(
                    electoral
                )

                if (
                    electoral.get("quality_status")
                    == "PARTIAL"
                ):
                    description.warnings.append(
                        SectionWarning(
                            code=(
                                "PARTIAL_ELECTORAL_COVERAGE"
                            ),
                            message=(
                                "La sección contiene uno o más "
                                "concursos electorales sin "
                                "cobertura completa y positiva."
                            ),
                        )
                    )

        return description
