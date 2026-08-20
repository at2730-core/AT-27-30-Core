from dataclasses import dataclass

from heyti.materialization.base import Materializer
from heyti.materialization.errors import (
    UnsupportedContractVersionError,
    UnsupportedMaterializationError,
)


@dataclass(frozen=True)
class MaterializationRegistration:
    capability_id: str
    contract_version: str
    materializer: Materializer


class MaterializationRegistry:
    """
    Registry de materializadores disponibles en HEYTI.

    Es independiente del CapabilityRegistry.

    Resuelve qué Materializer corresponde a una capability
    y versión contractual determinadas.
    """

    def __init__(self) -> None:
        self._registrations: dict[
            tuple[str, str],
            MaterializationRegistration,
        ] = {}

    def register(
        self,
        capability_id: str,
        contract_version: str,
        materializer: Materializer,
    ) -> None:
        key = (
            capability_id,
            contract_version,
        )

        self._registrations[key] = MaterializationRegistration(
            capability_id=capability_id,
            contract_version=contract_version,
            materializer=materializer,
        )

    def exists(
        self,
        capability_id: str,
        contract_version: str,
    ) -> bool:
        return (
            capability_id,
            contract_version,
        ) in self._registrations

    def resolve(
        self,
        capability_id: str,
        contract_version: str,
    ) -> Materializer:
        key = (
            capability_id,
            contract_version,
        )

        registration = self._registrations.get(key)

        if registration is not None:
            return registration.materializer

        known_versions = {
            version
            for capability, version in self._registrations
            if capability == capability_id
        }

        if known_versions:
            raise UnsupportedContractVersionError(
                f"Versión contractual no registrada para "
                f"{capability_id}: {contract_version}"
            )

        raise UnsupportedMaterializationError(
            f"No existe materialización registrada para "
            f"{capability_id}"
        )

    def count(self) -> int:
        return len(self._registrations)

    def list_registrations(
        self,
    ) -> list[MaterializationRegistration]:
        return sorted(
            self._registrations.values(),
            key=lambda item: (
                item.capability_id,
                item.contract_version,
            ),
        )