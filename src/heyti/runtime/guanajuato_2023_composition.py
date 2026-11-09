from heyti.capabilities.describe_field.implementation import DescribeFieldCapability
from heyti.capabilities.describe_field.postgres_source import (
    PostgresFieldSource,
    build_environment_connection_factory,
)
from heyti.capabilities.describe_universe.implementation import DescribeUniverseCapability, UniverseSource
from heyti.capabilities.describe_section.presentation_electoral_source import build_unselected_electoral_source
from dataclasses import dataclass
from pathlib import Path

from heyti.capabilities.describe_section.electoral_result_source import (
    CertifiedElectoralSectionSource,
)
from heyti.capabilities.describe_section.implementation import (
    DescribeSectionCapability,
)
from heyti.capabilities.describe_section.provider import (
    DescribeSectionProvider,
)
from heyti.capabilities.describe_section.territorial_geometry_source import (
    CertifiedGeoJsonSectionSource,
)
from heyti.capabilities.describe_section.territorial_truth_factory import (
    GuanajuatoTerritorialTruthAssembly,
    build_guanajuato_2023_territorial_truth,
)
from heyti.runtime.runtime_bootstrap import RuntimeBootstrap


@dataclass(frozen=True)
class Guanajuato2023RuntimeComposition:
    """
    Composición trazable del Runtime para Guanajuato 2023.

    Conserva el bootstrap y las fuentes certificadas utilizadas
    para construir la capability DescribeSection.
    """

    bootstrap: RuntimeBootstrap
    territorial_truth: GuanajuatoTerritorialTruthAssembly
    territorial_geometry: CertifiedGeoJsonSectionSource
    electoral_results: CertifiedElectoralSectionSource
    field_results: PostgresFieldSource


def compose_guanajuato_2023_runtime(
    master_path: str | Path,
    geometry_path: str | Path,
    *,
    versioned_electoral_source=None,
    field_connection_factory=None,
) -> Guanajuato2023RuntimeComposition:
    """
    Compone un RuntimeBootstrap con DescribeSection certificado.

    Las fuentes se validan al construir la composición. El Runtime
    no se inicializa automáticamente y las rutas no se fabrican.
    """

    territorial_truth = (
        build_guanajuato_2023_territorial_truth(
            master_path=master_path,
            geometry_path=geometry_path,
        )
    )

    authorized_section_ids = (
        territorial_truth.profile.comparable_section_ids
    )

    territorial_geometry = CertifiedGeoJsonSectionSource(
        geometry_path=geometry_path,
        authorized_section_ids=authorized_section_ids,
    )

    electoral_results = CertifiedElectoralSectionSource(
        master_path=master_path,
        authorized_section_ids=authorized_section_ids,
        election_year=2024,

    )

    if versioned_electoral_source is None:
        versioned_electoral_source = build_unselected_electoral_source(
            Path(__file__).resolve().parents[3] / "docs/auditoria/HEYTI_Matriz_Seleccion_Cortes_23_Series_v0_1.csv"
        )

    def build_describe_section() -> DescribeSectionCapability:
        provider = DescribeSectionProvider(
            truth_source=territorial_truth.source,
            territorial_source=territorial_geometry,
            electoral_source=electoral_results,
            versioned_electoral_source=versioned_electoral_source,
        )

        return DescribeSectionCapability(
            provider=provider,
        )

    universe_source = UniverseSource(geometry_path, master_path, territorial_truth.source, territorial_geometry, electoral_results, len(territorial_truth.profile.master_only))
    if field_connection_factory is None:
        field_connection_factory = (
            build_environment_connection_factory()
        )
    field_results = PostgresFieldSource(
        field_connection_factory
    )
    bootstrap = RuntimeBootstrap(
        capability_factories={
            "describe_section": build_describe_section,
            "describe_universe": lambda: DescribeUniverseCapability(universe_source),
            "describe_field": lambda: DescribeFieldCapability(field_results),
        },
    )

    return Guanajuato2023RuntimeComposition(
        bootstrap=bootstrap,
        territorial_truth=territorial_truth,
        territorial_geometry=territorial_geometry,
        electoral_results=electoral_results,
        field_results=field_results,
    )
