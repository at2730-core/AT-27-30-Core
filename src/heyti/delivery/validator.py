from heyti.delivery.contracts import (
    DELIVERY_STATUS_DELIVERED,
    DELIVERY_STATUS_FAILED,
    DELIVERY_STATUS_REJECTED,
    SUPPORTED_DELIVERY_STATUSES,
    DeliveryEnvelope,
    DeliveryResult,
)
from heyti.delivery.errors import DeliveryValidationError


class DeliveryContractValidator:
    """
    Valida las invariantes contractuales base de HRRD.

    No crea, corrige ni completa información.
    """

    def validate_envelope(
        self,
        envelope: DeliveryEnvelope,
    ) -> DeliveryEnvelope:
        if not isinstance(envelope, DeliveryEnvelope):
            raise DeliveryValidationError(
                "El candidato no es un DeliveryEnvelope"
            )

        if not envelope.delivery_id:
            raise DeliveryValidationError(
                "delivery_id es obligatorio"
            )

        if not envelope.response_id:
            raise DeliveryValidationError(
                "response_id es obligatorio"
            )

        if not envelope.consumer_id:
            raise DeliveryValidationError(
                "consumer_id es obligatorio"
            )

        if not envelope.adapter_id:
            raise DeliveryValidationError(
                "adapter_id es obligatorio"
            )

        if envelope.response is not None:
            if envelope.response.response_id != envelope.response_id:
                raise DeliveryValidationError(
                    "response_id del envelope no coincide "
                    "con la respuesta materializada"
                )

        return envelope

    def validate_result(
        self,
        result: DeliveryResult,
    ) -> DeliveryResult:
        if not isinstance(result, DeliveryResult):
            raise DeliveryValidationError(
                "El candidato no es un DeliveryResult"
            )

        if not result.delivery_id:
            raise DeliveryValidationError(
                "delivery_id es obligatorio"
            )

        if not result.response_id:
            raise DeliveryValidationError(
                "response_id es obligatorio"
            )

        if not result.consumer_id:
            raise DeliveryValidationError(
                "consumer_id es obligatorio"
            )

        if not result.adapter_id:
            raise DeliveryValidationError(
                "adapter_id es obligatorio"
            )

        if result.status not in SUPPORTED_DELIVERY_STATUSES:
            raise DeliveryValidationError(
                f"Status de Delivery no soportado: {result.status}"
            )

        if (
            result.status == DELIVERY_STATUS_DELIVERED
            and result.error is not None
        ):
            raise DeliveryValidationError(
                "DELIVERED no puede contener error fatal"
            )

        if (
            result.status in {
                DELIVERY_STATUS_FAILED,
                DELIVERY_STATUS_REJECTED,
            }
            and result.error is None
        ):
            raise DeliveryValidationError(
                f"{result.status} requiere error"
            )

        return result