from heyti.delivery.base import DeliveryAdapter


class DeliveryAdapterRegistry:
    """
    Registro de DeliveryAdapters disponibles para HRRD.

    Mantiene la resolución de adapters separada del Runtime
    y del DeliveryService.
    """

    def __init__(self) -> None:
        self._adapters: dict[str, DeliveryAdapter] = {}

    def register(
        self,
        adapter: DeliveryAdapter,
    ) -> None:
        """
        Registra un adapter utilizando su identidad contractual.
        """

        self._adapters[adapter.adapter_id] = adapter

    def exists(
        self,
        adapter_id: str,
    ) -> bool:
        """
        Indica si existe un adapter registrado.
        """

        return adapter_id in self._adapters

    def get(
        self,
        adapter_id: str,
    ) -> DeliveryAdapter | None:
        """
        Recupera un adapter registrado.
        """

        return self._adapters.get(adapter_id)

    def count(self) -> int:
        """
        Devuelve el número de adapters registrados.
        """

        return len(self._adapters)

    def list_adapters(self) -> list[str]:
        """
        Devuelve las identidades registradas en orden alfabético.
        """

        return sorted(self._adapters.keys())