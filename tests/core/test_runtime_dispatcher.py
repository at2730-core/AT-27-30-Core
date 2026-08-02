"""
Pruebas del Runtime Dispatcher.
"""

from heyti.capabilities.base import Capability
from heyti.registry.registry import CapabilityRegistry
from heyti.runtime.runtime_dispatcher import RuntimeDispatcher


class DummyCapability(Capability):

    def execute(
        self,
        session,
        payload=None,
    ):
        return {
            "status": "OK",
        }


def test_runtime_dispatcher_executes_registered_capability():

    registry = CapabilityRegistry()

    registry.register(
        "dummy",
        DummyCapability(),
    )

    dispatcher = RuntimeDispatcher(
        registry=registry,
    )

    result = dispatcher.execute(
        "dummy",
        session=None,
    )

    assert result == {
        "status": "OK",
    }