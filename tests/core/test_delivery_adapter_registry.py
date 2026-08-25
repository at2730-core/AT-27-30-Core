from heyti.delivery.adapters.in_memory import (
    InMemoryDeliveryAdapter,
)
from heyti.delivery.registry import DeliveryAdapterRegistry


def test_delivery_adapter_registry_starts_empty():
    registry = DeliveryAdapterRegistry()

    assert registry.count() == 0
    assert registry.list_adapters() == []


def test_delivery_adapter_registry_registers_adapter():
    registry = DeliveryAdapterRegistry()
    adapter = InMemoryDeliveryAdapter()

    registry.register(adapter)

    assert registry.count() == 1
    assert registry.exists("IN_MEMORY") is True


def test_delivery_adapter_registry_returns_registered_adapter():
    registry = DeliveryAdapterRegistry()
    adapter = InMemoryDeliveryAdapter()

    registry.register(adapter)

    assert registry.get("IN_MEMORY") is adapter


def test_delivery_adapter_registry_returns_none_for_unknown_adapter():
    registry = DeliveryAdapterRegistry()

    assert registry.get("UNKNOWN") is None


def test_delivery_adapter_registry_lists_adapters_sorted():
    registry = DeliveryAdapterRegistry()

    class ZAdapter(InMemoryDeliveryAdapter):
        ADAPTER_ID = "Z_ADAPTER"

    class AAdapter(InMemoryDeliveryAdapter):
        ADAPTER_ID = "A_ADAPTER"

    registry.register(ZAdapter())
    registry.register(AAdapter())

    assert registry.list_adapters() == [
        "A_ADAPTER",
        "Z_ADAPTER",
    ]


def test_delivery_adapter_registry_replaces_same_identity():
    registry = DeliveryAdapterRegistry()

    first = InMemoryDeliveryAdapter()
    second = InMemoryDeliveryAdapter()

    registry.register(first)
    registry.register(second)

    assert registry.count() == 1
    assert registry.get("IN_MEMORY") is second