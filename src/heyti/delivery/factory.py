from uuid import uuid4

from heyti.delivery.context import DeliveryContext
from heyti.delivery.contracts import (
    DeliveryEnvelope,
    DeliveryTrace,
)
from heyti.materialization.contracts import HeytiResponseContract


class DeliveryEnvelopeFactory:
    """
    Construye DeliveryEnvelope a partir de una respuesta materializada.

    Genera una identidad nueva para cada operación de Delivery.
    No modifica la respuesta cognitiva ni su response_id.
    """

    def create(
        self,
        response: HeytiResponseContract,
        context: DeliveryContext,
    ) -> DeliveryEnvelope:
        delivery_id = str(uuid4())

        return DeliveryEnvelope(
            delivery_id=delivery_id,
            response_id=response.response_id,
            consumer_id=context.consumer_id,
            adapter_id=context.adapter_id,
            response=response,
            trace=DeliveryTrace(
                request_id=context.request_id,
                session_id=context.session_id,
                execution_id=context.execution_id,
                response_id=response.response_id,
                delivery_id=delivery_id,
            ),
        )