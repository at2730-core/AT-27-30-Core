from heyti.delivery.base import DeliveryAdapter
from heyti.delivery.context import DeliveryContext
from heyti.delivery.contracts import (
    DELIVERY_STATUS_DELIVERED,
    DELIVERY_STATUS_FAILED,
    DELIVERY_STATUS_REJECTED,
    DeliveryError,
    DeliveryResult,
)
from heyti.delivery.factory import DeliveryEnvelopeFactory
from heyti.delivery.validator import DeliveryContractValidator
from heyti.materialization.contracts import HeytiResponseContract


class DeliveryService:
    """
    Orquesta una operación de Runtime Response Delivery.

    No ejecuta capabilities.
    No materializa respuestas.
    No modifica significado cognitivo.
    """

    def __init__(self) -> None:
        self._factory = DeliveryEnvelopeFactory()
        self._validator = DeliveryContractValidator()

    def deliver(
        self,
        response: HeytiResponseContract,
        context: DeliveryContext,
        adapter: DeliveryAdapter,
    ) -> DeliveryResult:
        envelope = self._factory.create(
            response,
            context,
        )

        self._validator.validate_envelope(envelope)

        if adapter.adapter_id != context.adapter_id:
            result = DeliveryResult(
                delivery_id=envelope.delivery_id,
                response_id=envelope.response_id,
                consumer_id=envelope.consumer_id,
                adapter_id=context.adapter_id,
                status=DELIVERY_STATUS_REJECTED,
                error=DeliveryError(
                    code="DELIVERY_ADAPTER_MISMATCH",
                    message=(
                        "El adapter suministrado no coincide "
                        "con el adapter solicitado"
                    ),
                    stage="ADAPTER_RESOLUTION",
                ),
                trace=envelope.trace,
            )

            return self._validator.validate_result(result)

        adapter_result = adapter.deliver(envelope)

        if adapter_result.success:
            result = DeliveryResult(
                delivery_id=envelope.delivery_id,
                response_id=envelope.response_id,
                consumer_id=envelope.consumer_id,
                adapter_id=envelope.adapter_id,
                status=DELIVERY_STATUS_DELIVERED,
                trace=envelope.trace,
            )

            return self._validator.validate_result(result)

        error = adapter_result.error

        if error is None:
            error = DeliveryError(
                code="DELIVERY_ADAPTER_ERROR",
                message="El adapter no completó la entrega",
                stage="DELIVERY_EXECUTION",
            )

        result = DeliveryResult(
            delivery_id=envelope.delivery_id,
            response_id=envelope.response_id,
            consumer_id=envelope.consumer_id,
            adapter_id=envelope.adapter_id,
            status=DELIVERY_STATUS_FAILED,
            error=error,
            trace=envelope.trace,
        )

        return self._validator.validate_result(result)