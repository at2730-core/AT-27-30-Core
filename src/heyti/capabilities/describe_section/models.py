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

        self.recommendations = []