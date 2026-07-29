from abc import ABC, abstractmethod
from typing import Any


class Capability(ABC):
    """
    Contrato base para todas las capacidades ejecutables de HEYTI.
    """

    @abstractmethod
    def execute(
        self,
        session: Any,
        payload: Any = None,
    ) -> Any:
        """
        Ejecuta la capacidad utilizando una sesión válida y un payload opcional.
        """
        raise NotImplementedError