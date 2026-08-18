from dataclasses import dataclass


@dataclass(frozen=True)
class MaterializationContext:
    """
    Contexto mínimo requerido para materializar un resultado cognitivo.

    Transporta identidad contractual y trazabilidad disponible.
    No contiene conocimiento de dominio ni decisiones de presentación.
    """

    capability_id: str
    contract_version: str = "1.0"

    request_id: str | None = None
    session_id: str | None = None
    execution_id: str | None = None
    knowledge_version: str | None = None