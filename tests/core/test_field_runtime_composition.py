from pathlib import Path

from heyti.capabilities.describe_field.implementation import (
    DescribeFieldCapability,
)
from heyti.runtime.guanajuato_2023_composition import (
    compose_guanajuato_2023_runtime,
)


ROOT = Path(__file__).resolve().parents[2]


def test_field_capability_is_composed_without_connecting():
    invocations = []

    def forbidden_connection():
        invocations.append("connected")
        raise AssertionError(
            "La composici?n no debe abrir PostgreSQL"
        )

    composition = compose_guanajuato_2023_runtime(
        master_path=(
            ROOT
            / "datasets"
            / "electoral"
            / "Datos_Electoral_con_2015.json"
        ),
        geometry_path=(
            ROOT
            / "datasets"
            / "spatial"
            / "secciones.geojson"
        ),
        field_connection_factory=forbidden_connection,
    )

    composition.bootstrap.initialize()

    capability = composition.bootstrap.registry.get(
        "describe_field"
    )

    assert isinstance(
        capability,
        DescribeFieldCapability,
    )
    assert capability.source is composition.field_results
    assert invocations == []
