from dataclasses import dataclass
from http.server import ThreadingHTTPServer
from pathlib import Path

from heyti.audit.data_truth.baselines.guanajuato_2023 import (
    GUANAJUATO_2023_POLICY_ID,
    GUANAJUATO_2023_POLICY_VERSION,
)
from heyti.capabilities.describe_field.postgres_source import (
    build_environment_connection_factory,
)
from heyti.gateway.gateway import HeytiGateway
from heyti.gateway.http_application import (
    HeytiHttpApplication,
)
from heyti.gateway.http_server import (
    DEFAULT_ALLOWED_ORIGINS,
    create_http_server,
)
from heyti.kernel.kernel import HeytiKernel
from heyti.runtime.guanajuato_2023_composition import (
    Guanajuato2023RuntimeComposition,
    compose_guanajuato_2023_runtime,
)
from heyti.security.composition import (
    SecurityComposition,
    compose_security,
)
from heyti.security.http_application import (
    SecurityHttpApplication,
)


DEFAULT_HTTP_SESSION_ID = "HEYTI-HTTP-LOCAL"


@dataclass
class Guanajuato2023HttpHost:
    """
    Host local compuesto para HEYTI Guanajuato 2023.

    Conserva referencias explícitas a cada frontera del ciclo
    de ejecución y controla el apagado ordenado del servidor.
    """

    composition: Guanajuato2023RuntimeComposition
    security_composition: SecurityComposition
    kernel: HeytiKernel
    gateway: HeytiGateway
    application: HeytiHttpApplication
    security_application: SecurityHttpApplication
    server: ThreadingHTTPServer

    @property
    def address(self) -> tuple[str, int]:
        """Devuelve la dirección efectiva del servidor."""

        host, port = self.server.server_address
        return str(host), int(port)

    def serve_forever(self) -> None:
        """
        Atiende solicitudes hasta recibir una orden de apagado.

        El socket y el Gateway se cierran aun cuando la ejecución
        termina por una excepción o interrupción.
        """

        try:
            self.server.serve_forever()
        finally:
            self.server.server_close()
            self.gateway.stop()

    def shutdown(self) -> None:
        """Solicita el apagado de un servidor en ejecución."""

        self.server.shutdown()


def build_guanajuato_2023_http_host(
    master_path: str | Path,
    geometry_path: str | Path,
    host: str = "127.0.0.1",
    port: int = 8765,
    session_id: str = DEFAULT_HTTP_SESSION_ID,
    allowed_origins: (
        tuple[str, ...]
    ) = DEFAULT_ALLOWED_ORIGINS,
    field_connection_factory=None,
) -> Guanajuato2023HttpHost:
    """
    Construye y arranca internamente el Runtime certificado.

    El servidor queda enlazado al host y puerto indicados, pero
    no comienza serve_forever hasta que el llamador lo solicite.
    """

    if not isinstance(session_id, str) or not session_id.strip():
        raise ValueError(
            "session_id debe ser una cadena no vacía"
        )

    effective_connection_factory = (
        field_connection_factory
    )

    if effective_connection_factory is None:
        effective_connection_factory = (
            build_environment_connection_factory()
        )

    composition = compose_guanajuato_2023_runtime(
        master_path=master_path,
        geometry_path=geometry_path,
        field_connection_factory=(
            effective_connection_factory
        ),
    )

    security_composition = compose_security(
        connection_factory=(
            effective_connection_factory
        ),
        session_manager=(
            composition.bootstrap.session_manager
        ),
    )

    kernel = HeytiKernel(
        bootstrap=composition.bootstrap,
    )
    gateway = HeytiGateway(kernel)
    gateway.start()

    normalized_session_id = session_id.strip()

    composition.bootstrap.session_manager.create(
        normalized_session_id,
        {
            "transport": "HTTP",
            "scope": "LOCAL",
        },
    )

    application = HeytiHttpApplication(
        gateway=gateway,
        session_id=normalized_session_id,
    )

    security_application = SecurityHttpApplication(
        authentication_service=(
            security_composition
            .authentication_service
        ),
        session_service=(
            security_composition.session_service
        ),
    )

    knowledge_version = (
        f"{GUANAJUATO_2023_POLICY_ID}:"
        f"{GUANAJUATO_2023_POLICY_VERSION}"
    )

    try:
        server = create_http_server(
            application=application,
            host=host,
            port=port,
            allowed_origins=allowed_origins,
            knowledge_version=knowledge_version,
            security_application=(
                security_application
            ),
        )
    except Exception:
        gateway.stop()
        raise

    return Guanajuato2023HttpHost(
        composition=composition,
        security_composition=(
            security_composition
        ),
        kernel=kernel,
        gateway=gateway,
        application=application,
        security_application=(
            security_application
        ),
        server=server,
    )
