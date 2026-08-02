from typing import Any

from heyti.registry.registry import CapabilityRegistry


class RuntimeDispatcher:
    """
    Localiza y ejecuta una capability registrada.

    No administra sesiones, eventos ni decisiones cognitivas.
    Es únicamente el mecanismo básico de despacho.
    """

    def __init__(
        self,
        registry: CapabilityRegistry,
    ) -> None:
        self.registry = registry

    def execute(
        self,
        capability_name: str,
        session: Any,
        payload: Any = None,
    ) -> Any:
        capability = self.registry.get(
            capability_name
        )

        if capability is None:
            raise LookupError(
                f"Capability no registrada: "
                f"{capability_name}"
            )

        return capability.execute(
            session=session,
            payload=payload,
        )