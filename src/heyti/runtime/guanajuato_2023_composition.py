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


def compose_guanajuato_2023_runtime(
    master_path: str | Path,
    geometry_path: str | Path,
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

    def build_describe_section() -> DescribeSectionCapability:
        provider = DescribeSectionProvider(
            truth_source=territorial_truth.source,
            territorial_source=territorial_geometry,
            electoral_source=electoral_results,
        )

        return DescribeSectionCapability(
            provider=provider,
        )

    bootstrap = RuntimeBootstrap(
        capability_factories={
            "describe_section": build_describe_section,
        },
    )

    return Guanajuato2023RuntimeComposition(
        bootstrap=bootstrap,
        territorial_truth=territorial_truth,
        territorial_geometry=territorial_geometry,
        electoral_results=electoral_results,
    )
