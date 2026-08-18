from abc import ABC, abstractmethod
from typing import Any

from heyti.materialization.context import MaterializationContext


class Materializer(ABC):
    """
    Contrato base para materializadores HEYTI.

    Un Materializer transforma un resultado cognitivo ya construido
    en una representación contractual.

    No ejecuta capabilities ni produce nuevo significado cognitivo.
    """

    @abstractmethod
    def materialize(
        self,
        cognitive_result: Any,
        context: MaterializationContext,
    ) -> Any:
        raise NotImplementedError