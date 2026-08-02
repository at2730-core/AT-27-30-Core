class DescribeSectionContract:
    """
    Define los dominios mínimos que debe integrar
    una descripción de sección producida por HEYTI.
    """

    def __init__(self) -> None:
        self.domains = [
            "territorial",
            "electoral",
            "socioeconomic",
            "field",
            "security",
            "risk",
            "recommendations",
        ]