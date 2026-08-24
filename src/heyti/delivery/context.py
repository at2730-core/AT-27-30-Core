from dataclasses import dataclass


@dataclass(frozen=True)
class DeliveryContext:
    """
    Contexto mínimo requerido para una operación de Delivery.

    Transporta identidad y trazabilidad disponible.
    No contiene conocimiento cognitivo ni decisiones de presentación.
    """

    consumer_id: str
    adapter_id: str

    request_id: str | None = None
    session_id: str | None = None
    execution_id: str | None = None