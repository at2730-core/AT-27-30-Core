from unittest.mock import MagicMock

import pytest

from heyti.security.scope_assignment import (
    AssignedTerritorialScope,
    TerritorialScopeType,
)
from heyti.security.scope_assignment_cli import (
    build_parser,
    main,
)


def make_result(
    scope_type,
    section_count,
):
    return AssignedTerritorialScope(
        assignment_id=30,
        scope_id=20,
        user_id=7,
        scope_name="Alcance de prueba",
        scope_type=scope_type,
        section_count=section_count,
    )


def run_cli(
    arguments,
    *,
    result,
    environment=None,
):
    repository = MagicMock()
    repository.assign_scope.return_value = result

    connection_factory = MagicMock()
    builder = MagicMock(
        return_value=connection_factory
    )
    repository_factory = MagicMock(
        return_value=repository
    )
    output = MagicMock()
    password_reader = MagicMock(
        return_value="database-secret"
    )

    exit_code = main(
        arguments,
        environ=(
            {}
            if environment is None
            else environment
        ),
        password_reader=password_reader,
        connection_factory_builder=builder,
        repository_factory=repository_factory,
        output=output,
    )

    return {
        "exit_code": exit_code,
        "repository": repository,
        "builder": builder,
        "repository_factory": (
            repository_factory
        ),
        "output": output,
        "password_reader": password_reader,
    }


def test_assigns_municipality_from_cli():
    execution = run_cli(
        [
            "--user-id",
            "7",
            "--scope-name",
            "Abasolo",
            "--assigned-by-user-id",
            "3",
            "--municipality-id",
            "1",
        ],
        result=make_result(
            TerritorialScopeType.MUNICIPALITY,
            50,
        ),
    )

    assert execution["exit_code"] == 0

    call = (
        execution["repository"]
        .assign_scope.call_args
    )

    assert call.kwargs["user_id"] == 7
    assert call.kwargs["scope_name"] == "Abasolo"
    assert call.kwargs["scope_type"] is (
        TerritorialScopeType.MUNICIPALITY
    )
    assert call.kwargs["municipality_id"] == 1
    assert call.kwargs["section_codes"] == ()
    assert call.kwargs[
        "assigned_by_user_id"
    ] == 3


def test_assigns_section_set_from_cli():
    execution = run_cli(
        [
            "--user-id",
            "8",
            "--scope-name",
            "Prioritarias",
            "--assigned-by-user-id",
            "3",
            "--section-code",
            "1482",
            "--section-code",
            "1481",
        ],
        result=make_result(
            TerritorialScopeType.SECTION_SET,
            2,
        ),
    )

    call = (
        execution["repository"]
        .assign_scope.call_args
    )

    assert call.kwargs["scope_type"] is (
        TerritorialScopeType.SECTION_SET
    )
    assert call.kwargs["municipality_id"] is None
    assert call.kwargs["section_codes"] == (
        "1481",
        "1482",
    )


def test_assigns_global_from_cli():
    execution = run_cli(
        [
            "--user-id",
            "3",
            "--scope-name",
            "Acceso estatal",
            "--assigned-by-user-id",
            "3",
            "--global",
        ],
        result=make_result(
            TerritorialScopeType.GLOBAL,
            0,
        ),
    )

    call = (
        execution["repository"]
        .assign_scope.call_args
    )

    assert call.kwargs["scope_type"] is (
        TerritorialScopeType.GLOBAL
    )
    assert call.kwargs["municipality_id"] is None
    assert call.kwargs["section_codes"] == ()


def test_prompts_for_database_password():
    execution = run_cli(
        [
            "--user-id",
            "7",
            "--scope-name",
            "Abasolo",
            "--assigned-by-user-id",
            "3",
            "--municipality-id",
            "1",
        ],
        result=make_result(
            TerritorialScopeType.MUNICIPALITY,
            50,
        ),
    )

    execution[
        "password_reader"
    ].assert_called_once_with(
        "Contrasena PostgreSQL para HEYTI: "
    )

    environment = (
        execution["builder"].call_args.args[0]
    )

    assert (
        environment["HEYTI_DB_PASSWORD"]
        == "database-secret"
    )


def test_uses_existing_database_password():
    execution = run_cli(
        [
            "--user-id",
            "7",
            "--scope-name",
            "Abasolo",
            "--assigned-by-user-id",
            "3",
            "--municipality-id",
            "1",
        ],
        result=make_result(
            TerritorialScopeType.MUNICIPALITY,
            50,
        ),
        environment={
            "HEYTI_DB_PASSWORD": "existing-secret",
        },
    )

    execution[
        "password_reader"
    ].assert_not_called()


def test_outputs_non_sensitive_result():
    execution = run_cli(
        [
            "--user-id",
            "7",
            "--scope-name",
            "Abasolo",
            "--assigned-by-user-id",
            "3",
            "--municipality-id",
            "1",
        ],
        result=make_result(
            TerritorialScopeType.MUNICIPALITY,
            50,
        ),
    )

    messages = [
        call.args[0]
        for call in execution["output"].call_args_list
    ]

    assert "database-secret" not in " ".join(
        messages
    )
    assert "Secciones: 50" in messages


@pytest.mark.parametrize(
    "arguments",
    [
        [
            "--user-id",
            "7",
            "--scope-name",
            "Sin alcance",
            "--assigned-by-user-id",
            "3",
        ],
        [
            "--user-id",
            "7",
            "--scope-name",
            "Conflicto",
            "--assigned-by-user-id",
            "3",
            "--global",
            "--municipality-id",
            "1",
        ],
    ],
)
def test_requires_exactly_one_scope_shape(
    arguments,
):
    parser = build_parser()

    with pytest.raises(SystemExit):
        parser.parse_args(arguments)


def test_repository_validation_is_reported():
    repository = MagicMock()
    repository.assign_scope.side_effect = ValueError(
        "El municipio solicitado no existe"
    )

    with pytest.raises(SystemExit):
        main(
            [
                "--user-id",
                "7",
                "--scope-name",
                "Invalido",
                "--assigned-by-user-id",
                "3",
                "--municipality-id",
                "999",
            ],
            environ={
                "HEYTI_DB_PASSWORD": "secret",
            },
            connection_factory_builder=MagicMock(),
            repository_factory=MagicMock(
                return_value=repository
            ),
        )
