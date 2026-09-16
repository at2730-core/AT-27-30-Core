from dataclasses import dataclass


@dataclass(frozen=True)
class SectionWarning:
    """
    Advertencia cognitiva asociada a la descripción de una sección.

    Informa una limitación verificable sin modificar,
    completar ni fabricar datos.
    """

    code: str
    message: str


class SectionDescription:
    """
    Modelo raíz de conocimiento para la descripción
    integrada de una sección electoral.
    """

    def __init__(self) -> None:
        self.section_id = None

        self.territorial = None
        self.electoral = None
        self.socioeconomic = None
        self.field = None
        self.security = None
        self.risk = None

        self.data_truth = None
        self.warnings: list[SectionWarning] = []

        self.recommendations = []
