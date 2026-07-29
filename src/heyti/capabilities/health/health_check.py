from heyti.capabilities.base import Capability


class HealthCheckCapability(Capability):
    """
    Capability de diagnóstico del estado del Core.
    """

    VERSION = "0.1.0"

    def execute(
        self,
        session,
        payload=None,
    ):
        return {
            "status": "OK",
            "runtime": "HEYTI CORE",
            "version": self.VERSION,
        }