import argparse
import os
from getpass import getpass
from typing import Sequence

from heyti.capabilities.describe_field.postgres_source import (
    build_environment_connection_factory,
)
from heyti.security.postgres_scope_assignment import (
    PostgresTerritorialScopeRepository,
)
from heyti.security.scope_assignment import (
    ScopeAssignmentRequest,
    TerritorialScopeAssignmentService,
    TerritorialScopeType,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="heyti-assign-scope",
        description=(
            "Asigna un alcance territorial atomico "
            "a un usuario HEYTI."
        ),
    )
    parser.add_argument(
        "--user-id",
        required=True,
        type=int,
        help="Identificador del usuario objetivo.",
    )
    parser.add_argument(
        "--scope-name",
        required=True,
        help="Nombre descriptivo del alcance.",
    )
    parser.add_argument(
        "--assigned-by-user-id",
        required=True,
        type=int,
        help=(
            "Identificador del administrador "
            "que realiza la asignacion."
        ),
    )

    scope_group = (
        parser.add_mutually_exclusive_group(
            required=True
        )
    )
    scope_group.add_argument(
        "--global",
        dest="global_scope",
        action="store_true",
        help=(
            "Asigna alcance global. Solo es valido "
            "para ADMINISTRATOR."
        ),
    )
    scope_group.add_argument(
        "--municipality-id",
        type=int,
        help=(
            "Asigna todas las secciones de un "
            "municipio operativo."
        ),
    )
    scope_group.add_argument(
        "--section-code",
        action="append",
        dest="section_codes",
        help=(
            "Asigna una seccion. Puede repetirse "
            "para formar un conjunto."
        ),
    )

    return parser


def _scope_arguments(arguments):
    if arguments.global_scope:
        return (
            TerritorialScopeType.GLOBAL,
            None,
            (),
        )

    if arguments.municipality_id is not None:
        return (
            TerritorialScopeType.MUNICIPALITY,
            arguments.municipality_id,
            (),
        )

    return (
        TerritorialScopeType.SECTION_SET,
        None,
        tuple(arguments.section_codes or ()),
    )


def main(
    argv: Sequence[str] | None = None,
    *,
    environ=None,
    password_reader=getpass,
    connection_factory_builder=(
        build_environment_connection_factory
    ),
    repository_factory=(
        PostgresTerritorialScopeRepository
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

    (
        scope_type,
        municipality_id,
        section_codes,
    ) = _scope_arguments(arguments)

    try:
        connection_factory = (
            connection_factory_builder(
                environment
            )
        )
        repository = repository_factory(
            connection_factory
        )
        service = (
            TerritorialScopeAssignmentService(
                repository
            )
        )

        result = service.assign(
            ScopeAssignmentRequest(
                user_id=arguments.user_id,
                scope_name=arguments.scope_name,
                scope_type=scope_type,
                municipality_id=municipality_id,
                section_codes=section_codes,
                assigned_by_user_id=(
                    arguments.assigned_by_user_id
                ),
            )
        )
    except (TypeError, ValueError) as exc:
        parser.error(str(exc))

    output(
        "Alcance territorial asignado correctamente."
    )
    output(f"Asignacion ID: {result.assignment_id}")
    output(f"Alcance ID: {result.scope_id}")
    output(f"Usuario ID: {result.user_id}")
    output(f"Nombre: {result.scope_name}")
    output(f"Tipo: {result.scope_type.value}")
    output(
        f"Secciones: {result.section_count}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
