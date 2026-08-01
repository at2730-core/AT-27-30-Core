class RuntimeStartupSequence:
    """
    Registra ordenadamente las etapas del arranque
    del Runtime de HEYTI.
    """

    def __init__(self) -> None:
        self.steps: list[tuple[str, str]] = []

    def add_step(
        self,
        name: str,
        status: str,
    ) -> None:
        self.steps.append(
            (name, status)
        )