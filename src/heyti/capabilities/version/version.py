from heyti.capabilities.base import Capability


class VersionCapability(Capability):
    """
    Capability que informa la identidad y versión de HEYTI Core.
    """

    NAME = "HEYTI CORE"
    VERSION = "0.1.0"
    API_VERSION = "v1"

    def execute(
        self,
        session,
        payload=None,
    ):
        return {
            "name": self.NAME,
            "version": self.VERSION,
            "api": self.API_VERSION,
        }