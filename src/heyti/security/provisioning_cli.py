import argparse
import os
from getpass import getpass
from typing import Sequence

from heyti.capabilities.describe_field.postgres_source import (
    build_environment_connection_factory,
)
from heyti.security.contracts import AccessRole
from heyti.security.credentials import (
    Argon2CredentialHasher,
)
from heyti.security.postgres_provisioning import (
    PostgresUserProvisioningRepository,
)
from heyti.security.provisioning import (
    UserProvisioningRequest,
    UserProvisioningService,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="heyti-provision-user",
        description=(
            "Crea usuarios de HEYTI con credenciales "
            "Argon2id y asignacion atomica de rol."
        ),
    )
    parser.add_argument(
        "--username",
        required=True,
        help="Nombre unico de acceso.",
    )
    parser.add_argument(
        "--display-name",
        required=True,
        help="Nombre visible del usuario.",
    )
    parser.add_argument(
        "--role",
        required=True,
        choices=[
            role.value
            for role in AccessRole
        ],
        help="Rol inicial del usuario.",
    )
    parser.add_argument(
        "--assigned-by-user-id",
        type=int,
        default=None,
        help=(
            "Identificador del administrador que "
            "realiza la asignacion."
        ),
    )

    password_group = (
        parser.add_mutually_exclusive_group()
    )
    password_group.add_argument(
        "--must-change",
        dest="must_change",
        action="store_true",
        default=True,
        help=(
            "Exige cambiar la contrasena en el "
            "primer acceso."
        ),
    )
    password_group.add_argument(
        "--no-must-change",
        dest="must_change",
        action="store_false",
        help=(
            "Conserva la contrasena capturada."
        ),
    )

    return parser


def read_confirmed_password(password_reader) -> str:
    password = password_reader(
        "Nueva contrasena del usuario: "
    )
    confirmation = password_reader(
        "Confirma la contrasena: "
    )

    if not password:
        raise ValueError(
            "La contrasena no puede estar vacia."
        )

    if password != confirmation:
        raise ValueError(
            "Las contrasenas no coinciden."
        )

    return password


def main(
    argv: Sequence[str] | None = None,
    *,
    environ=None,
    password_reader=getpass,
    connection_factory_builder=(
        build_environment_connection_factory
    ),
    repository_factory=(
        PostgresUserProvisioningRepository
    ),
    credential_hasher_factory=(
        Argon2CredentialHasher
    ),
    output=print,
) -> int:
    parser = build_parser()
    arguments = parser.parse_args(argv)

    environment = dict(
        os.environ
        if environ is None
        else environ
    )

    if not environment.get("HEYTI_DB_PASSWORD"):
        database_password = password_reader(
            "Contrasena PostgreSQL para HEYTI: "
        )

        if database_password:
            environment[
                "HEYTI_DB_PASSWORD"
            ] = database_password

    try:
        password = read_confirmed_password(
            password_reader
        )

        connection_factory = (
            connection_factory_builder(
                environment
            )
        )
        repository = repository_factory(
            connection_factory
        )
        credential_hasher = (
            credential_hasher_factory()
        )
        service = UserProvisioningService(
            repository,
            credential_hasher,
        )

        result = service.provision(
            UserProvisioningRequest(
                username=arguments.username,
                display_name=(
                    arguments.display_name
                ),
                password=password,
                role=AccessRole(
                    arguments.role
                ),
                must_change=(
                    arguments.must_change
                ),
                assigned_by_user_id=(
                    arguments
                    .assigned_by_user_id
                ),
            )
        )
    except (TypeError, ValueError) as exc:
        parser.error(str(exc))

    output(
        "Usuario HEYTI creado correctamente."
    )
    output(f"ID: {result.user_id}")
    output(f"Usuario: {result.username}")
    output(f"Nombre: {result.display_name}")
    output(f"Rol: {result.role.value}")
    output(
        "Cambio de contrasena requerido: "
        f"{'SI' if result.must_change else 'NO'}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
