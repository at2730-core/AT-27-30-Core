from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SectionWarning:
    """
    Advertencia cognitiva asociada a la descripción de una sección.

    Informa una limitación verificable sin modificar,
    completar ni fabricar datos.
    """

    code: str
    message: str


@dataclass(frozen=True)
class SectionTruthSnapshot:
    """
    Estado de verdad preparado para DescribeSection.

    Mantiene separados el contenido verificable y sus advertencias.
    """

    content: dict[str, Any]
    warnings: tuple[SectionWarning, ...] = ()

    def __post_init__(self) -> None:
        if not isinstance(self.content, dict):
            raise TypeError(
                "SectionTruthSnapshot.content debe ser dict"
            )

        if not isinstance(self.warnings, tuple):
            raise TypeError(
                "SectionTruthSnapshot.warnings debe ser tuple"
            )

        if not all(
            isinstance(warning, SectionWarning)
            for warning in self.warnings
        ):
            raise TypeError(
                "SectionTruthSnapshot.warnings debe contener "
                "exclusivamente SectionWarning"
            )


class SectionDescription:
    """
    Modelo raíz de conocimiento para la descripción
    integrada de una sección electoral.
    """

    def __init__(self) -> None:
        self.section_id = None

        self.territorial = None
        self.electoral = None
        self.electoral_versioned = None
        self.socioeconomic = None
        self.field = None
        self.security = None
        self.risk = None

        self.data_truth = None
        self.warnings: list[SectionWarning] = []

        self.recommendations = []
