from dataclasses import dataclass
from pathlib import Path

from heyti.capabilities.describe_section.implementation import (
    DescribeSectionCapability,
)
from heyti.capabilities.describe_section.provider import (
    DescribeSectionProvider,
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

    Conserva tanto el bootstrap configurado como el ensamblaje
    territorial certificado utilizado para construirlo.
    """

    bootstrap: RuntimeBootstrap
    territorial_truth: GuanajuatoTerritorialTruthAssembly


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

    def build_describe_section() -> DescribeSectionCapability:
        provider = DescribeSectionProvider(
            truth_source=territorial_truth.source,
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
    )
