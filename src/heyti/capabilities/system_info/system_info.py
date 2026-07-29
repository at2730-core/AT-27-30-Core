import platform
import sys

from heyti.capabilities.base import Capability


class SystemInfoCapability(Capability):
    """
    Capability que informa datos básicos del entorno
    donde se ejecuta HEYTI Core.
    """

    def execute(
        self,
        session,
        payload=None,
    ):
        return {
            "core": "HEYTI CORE",
            "python": platform.python_version(),
            "platform": sys.platform,
            "system": platform.system(),
            "machine": platform.machine(),
        }