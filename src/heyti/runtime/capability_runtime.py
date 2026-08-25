"""
Capability Runtime de HEYTI.

Responsabilidad:
Orquestar la ejecución de capacidades registradas
dentro de una sesión válida.
"""

from typing import Any

from heyti.delivery.base import DeliveryAdapter
from heyti.delivery.context import DeliveryContext
from heyti.delivery.contracts import DeliveryResult
from heyti.delivery.service import DeliveryService

from heyti.events.event_bus import EventBus
from heyti.materialization.base import Materializer
from heyti.materialization.context import MaterializationContext
from heyti.materialization.contracts import HeytiResponseContract
from heyti.materialization.validator import ResponseContractValidator
from heyti.registry.registry import CapabilityRegistry
from heyti.session.session_manager import SessionManager

from heyti.materialization.errors import (
    UnsupportedMaterializationError,
)
from heyti.materialization.registry import (
    MaterializationRegistry,
)


class SessionNotFoundError(Exception):
    """
    Se produce cuando la sesión solicitada no existe.
    """


class CapabilityNotFoundError(Exception):
    """
    Se produce cuando la capacidad solicitada no está registrada.
    """


class CapabilityRuntime:
    """
    Coordina la ejecución de capacidades dentro del Runtime.
    """

    def __init__(
        self,
        registry: CapabilityRegistry,
        session_manager: SessionManager,
        event_bus: EventBus,
        materialization_registry: MaterializationRegistry | None = None,
    ) -> None:
        self._registry = registry
        self._session_manager = session_manager
        self._event_bus = event_bus
        self._materialization_registry = materialization_registry

    def _execute_capability(
        self,
        capability_name: str,
        session_id: str,
        payload: Any = None,
    ) -> Any:
        """
        Ejecuta una capability exactamente una vez y publica
        el evento interno correspondiente.
        """

        if not self._session_manager.exists(session_id):
            raise SessionNotFoundError(
                f"Session not found: {session_id}"
            )

        session = self._session_manager.get(session_id)

        if not self._registry.exists(capability_name):
            raise CapabilityNotFoundError(
                f"Capability not found: {capability_name}"
            )

        capability = self._registry.get(capability_name)

        result = capability.execute(
            session,
            payload,
        )

        self._event_bus.publish(
            "capability_executed",
            {
                "capability_name": capability_name,
                "session_id": session_id,
                "result": result,
            },
        )

        return result

    def execute(
        self,
        capability_name: str,
        session_id: str,
        payload: Any = None,
    ) -> Any:
        """
        Ejecuta una capability y devuelve su Cognitive Result.

        Mantiene el comportamiento heredado del Runtime.
        """

        return self._execute_capability(
            capability_name=capability_name,
            session_id=session_id,
            payload=payload,
        )

    def execute_materialized(
        self,
        capability_name: str,
        session_id: str,
        materializer: Materializer | None = None,
        payload: Any = None,
        contract_version: str = "1.0",
        request_id: str | None = None,
        execution_id: str | None = None,
        knowledge_version: str | None = None,
        validator: ResponseContractValidator | None = None,
    ) -> HeytiResponseContract:
        """
        Ejecuta una capability exactamente una vez, materializa
        su Cognitive Result y valida el Response Contract.

        No existe fallback hacia el Cognitive Result si
        Materialization o Validation fallan.
        """

        resolved_materializer = materializer

        if resolved_materializer is None:
            if self._materialization_registry is None:
                raise UnsupportedMaterializationError(
                    "No se proporcionó un Materializer y "
                    "el Runtime no posee MaterializationRegistry"
                )

            resolved_materializer = (
                self._materialization_registry.resolve(
                    capability_id=capability_name,
                    contract_version=contract_version,
                )
            )

        cognitive_result = self._execute_capability(
            capability_name=capability_name,
            session_id=session_id,
            payload=payload,
        )

        context = MaterializationContext(
            capability_id=capability_name,
            contract_version=contract_version,
            request_id=request_id,
            session_id=session_id,
            execution_id=execution_id,
            knowledge_version=knowledge_version,
        )

        response = resolved_materializer.materialize(
            cognitive_result,
            context,
        )

        response_validator = (
            validator or ResponseContractValidator()
        )
        return response_validator.validate(response)

    def execute_delivered(
        self,
        capability_name: str,
        session_id: str,
        consumer_id: str,
        adapter: DeliveryAdapter,
        materializer: Materializer | None = None,
        payload: Any = None,
        contract_version: str = "1.0",
        request_id: str | None = None,
        execution_id: str | None = None,
        knowledge_version: str | None = None,
        validator: ResponseContractValidator | None = None,
        delivery_service: DeliveryService | None = None,
    ) -> DeliveryResult:
        """
        Ejecuta la capability, materializa la respuesta,
        y la entrega a un consumidor a través de un adapter.

        La entrega se realiza únicamente sobre la respuesta
        contractual ya validada; la ejecución cognitiva ocurre
        exactamente una vez.
        """

        response = self.execute_materialized(
            capability_name=capability_name,
            session_id=session_id,
            materializer=materializer,
            payload=payload,
            contract_version=contract_version,
            request_id=request_id,
            execution_id=execution_id,
            knowledge_version=knowledge_version,
            validator=validator,
        )

        delivery_context = DeliveryContext(
            consumer_id=consumer_id,
            adapter_id=adapter.adapter_id,
            request_id=response.trace.request_id,
            session_id=response.trace.session_id,
            execution_id=response.trace.execution_id,
        )

        resolved_delivery_service = (
            delivery_service or DeliveryService()
        )

        delivery_result = resolved_delivery_service.deliver(
            response=response,
            context=delivery_context,
            adapter=adapter,
        )

        self._event_bus.publish(
            "delivery_completed",
            {
                "delivery_id": delivery_result.delivery_id,
                "response_id": delivery_result.response_id,
                "consumer_id": delivery_result.consumer_id,
                "adapter_id": delivery_result.adapter_id,
                "status": delivery_result.status,
            },
        )

        return delivery_result