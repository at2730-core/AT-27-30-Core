from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class ResponseBlock:
    """
    Unidad mínima de contenido materializado.

    type:
        Tipo estructural del bloque.

    role:
        Significado semántico del bloque dentro de la respuesta.

    content:
        Contenido materializado.
    """

    type: str
    role: str
    content: Any


@dataclass(frozen=True)
class ResponseWarning:
    """
    Advertencia no fatal asociada a una respuesta materializada.
    """

    code: str
    message: str


@dataclass(frozen=True)
class ResponseError:
    """
    Error contractual seguro para exposición externa.
    """

    code: str
    message: str


@dataclass(frozen=True)
class ResponseTrace:
    """
    Trazabilidad disponible para una respuesta HEYTI.

    Los identificadores ausentes permanecen como None.
    Nunca deberán fabricarse para completar el contrato.
    """

    request_id: str | None = None
    session_id: str | None = None
    execution_id: str | None = None
    knowledge_version: str | None = None


@dataclass(frozen=True)
class HeytiResponseContract:
    """
    Contrato externo base de respuestas materializadas HEYTI.
    """

    contract: str
    version: str
    capability_id: str
    status: str

    blocks: list[ResponseBlock] = field(default_factory=list)
    warnings: list[ResponseWarning] = field(default_factory=list)
    errors: list[ResponseError] = field(default_factory=list)

    trace: ResponseTrace = field(default_factory=ResponseTrace)

    def to_dict(self) -> dict[str, Any]:
        """
        Devuelve una representación compatible con serialización JSON.
        """

        return asdict(self)