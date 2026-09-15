from dataclasses import asdict, dataclass, field
from typing import Any

from heyti.audit.data_truth.section_universe import (
    SectionUniverseProfile,
)


@dataclass(frozen=True)
class TerritorialSectionPolicy:
    """
    Política versionada para interpretar diferencias territoriales.

    Los códigos provienen de evidencia externa al motor y no se infieren
    automáticamente por rango o apariencia.
    """

    policy_id: str
    version: str
    certified_lineage: dict[int, tuple[int, ...]] = field(
        default_factory=dict,
    )
    unresolved_historical: tuple[int, ...] = field(
        default_factory=tuple,
    )
    synthetic_candidates: tuple[int, ...] = field(
        default_factory=tuple,
    )
    evidence_reference: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Devuelve una representación estructurada de la política."""

        return asdict(self)


@dataclass(frozen=True)
class TerritorialClassification:
    """Resultado de aplicar una política a universos reconciliados."""

    certified_predecessors: tuple[int, ...]
    certified_successors: tuple[int, ...]
    unresolved_historical: tuple[int, ...]
    synthetic_candidates: tuple[int, ...]
    unclassified_master_only: tuple[int, ...]
    unexpected_geometry_only: tuple[int, ...]

    def to_dict(self) -> dict[str, Any]:
        """Devuelve una representación estructurada del resultado."""

        return asdict(self)


def _validate_policy(
    policy: TerritorialSectionPolicy,
) -> None:
    """Impide categorías superpuestas o genealogías vacías."""

    predecessors = set(policy.certified_lineage)
    historical = set(policy.unresolved_historical)
    synthetic = set(policy.synthetic_candidates)

    overlaps = (
        (predecessors & historical)
        | (predecessors & synthetic)
        | (historical & synthetic)
    )

    if overlaps:
        raise ValueError(
            "La política contiene categorías superpuestas: "
            + ", ".join(map(str, sorted(overlaps)))
        )

    empty_lineages = sorted(
        predecessor
        for predecessor, successors
        in policy.certified_lineage.items()
        if not successors
    )

    if empty_lineages:
        raise ValueError(
            "La política contiene genealogías sin sucesores: "
            + ", ".join(map(str, empty_lineages))
        )


def classify_section_universes(
    profile: SectionUniverseProfile,
    policy: TerritorialSectionPolicy,
) -> TerritorialClassification:
    """
    Clasifica diferencias ya observadas mediante una política explícita.

    No altera el perfil, las fuentes ni la base de datos.
    """

    _validate_policy(policy)

    master_only = set(profile.master_only)
    geometry_only = set(profile.geometry_only)

    predecessors = set(policy.certified_lineage)
    successors = {
        successor
        for values in policy.certified_lineage.values()
        for successor in values
    }
    historical = set(policy.unresolved_historical)
    synthetic = set(policy.synthetic_candidates)

    classified_master = (
        predecessors
        | historical
        | synthetic
    )

    return TerritorialClassification(
        certified_predecessors=tuple(
            sorted(predecessors & master_only)
        ),
        certified_successors=tuple(
            sorted(successors & geometry_only)
        ),
        unresolved_historical=tuple(
            sorted(historical & master_only)
        ),
        synthetic_candidates=tuple(
            sorted(synthetic & master_only)
        ),
        unclassified_master_only=tuple(
            sorted(master_only - classified_master)
        ),
        unexpected_geometry_only=tuple(
            sorted(geometry_only - successors)
        ),
    )
