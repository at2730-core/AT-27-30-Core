from unittest.mock import MagicMock

import pytest

from heyti.security.contracts import AccessRole
from heyti.security.provisioning import (
    ProvisionedUser,
)
from heyti.security.provisioning_cli import (
    main,
)


HASH = "$argon2id$test-hash"


def make_dependencies():
    captured = {}

    def connection_factory_builder(environment):
        captured["environment"] = dict(
            environment
        )
        return "connection-factory"

    repository = MagicMock()
    repository.create_user.return_value = (
        ProvisionedUser(
            user_id=7,
            user_uuid="user-uuid",
            username="alex",
            display_name="Alex",
            role=AccessRole.ADMINISTRATOR,
            must_change=True,
        )
    )

    def repository_factory(connection_factory):
        captured["connection_factory"] = (
            connection_factory
        )
        return repository

    hasher = MagicMock()
    hasher.hash_password.return_value = HASH

    return (
        captured,
        repository,
        hasher,
        connection_factory_builder,
        repository_factory,
    )


def run_cli(
    *,
    argv=None,
    secrets=None,
    environ=None,
):
    (
        captured,
        repository,
        hasher,
        connection_factory_builder,
        repository_factory,
    ) = make_dependencies()

    supplied_secrets = iter(
        secrets
        if secrets is not None
        else [
            "database-secret",
            "user-secret",
            "user-secret",
        ]
    )
    prompts = []
    output = []

    def password_reader(prompt):
        prompts.append(prompt)
        return next(supplied_secrets)

    exit_code = main(
        argv=(
            argv
            if argv is not None
            else [
                "--username",
                " ALEX ",
                "--display-name",
                " Alex ",
                "--role",
                "ADMINISTRATOR",
            ]
        ),
        environ=(
            {}
            if environ is None
            else environ
        ),
        password_reader=password_reader,
        connection_factory_builder=(
            connection_factory_builder
        ),
        repository_factory=repository_factory,
        credential_hasher_factory=(
            lambda: hasher
        ),
        output=output.append,
    )

    return {
        "exit_code": exit_code,
        "captured": captured,
        "repository": repository,
        "hasher": hasher,
        "prompts": prompts,
        "output": output,
    }


def test_cli_provisions_user_without_exposing_secrets():
    result = run_cli()

    assert result["exit_code"] == 0
    assert len(result["prompts"]) == 3
    assert (
        result["captured"]["environment"][
            "HEYTI_DB_PASSWORD"
        ]
        == "database-secret"
    )
    result[
        "hasher"
    ].hash_password.assert_called_once_with(
        "user-secret"
    )

    visible_output = "\n".join(
        result["output"]
    )

    assert "database-secret" not in visible_output
    assert "user-secret" not in visible_output
    assert "alex" in visible_output
    assert "ADMINISTRATOR" in visible_output


def test_cli_uses_existing_database_password():
    result = run_cli(
        secrets=[
            "user-secret",
            "user-secret",
        ],
        environ={
            "HEYTI_DB_PASSWORD": (
                "existing-secret"
            ),
        },
    )

    assert len(result["prompts"]) == 2
    assert (
        result["captured"]["environment"][
            "HEYTI_DB_PASSWORD"
        ]
        == "existing-secret"
    )


def test_cli_rejects_password_mismatch():
    with pytest.raises(SystemExit) as exc_info:
        run_cli(
            secrets=[
                "database-secret",
                "first-password",
                "second-password",
            ]
        )

    assert exc_info.value.code == 2


def test_cli_rejects_empty_password():
    with pytest.raises(SystemExit) as exc_info:
        run_cli(
            secrets=[
                "database-secret",
                "",
                "",
            ]
        )

    assert exc_info.value.code == 2


@pytest.mark.parametrize(
    ("role_code", "expected_role"),
    [
        (
            "ADMINISTRATOR",
            AccessRole.ADMINISTRATOR,
        ),
        (
            "COORDINATOR",
            AccessRole.COORDINATOR,
        ),
        (
            "PROMOTER",
            AccessRole.PROMOTER,
        ),
    ],
)
def test_cli_accepts_certified_roles(
    role_code,
    expected_role,
):
    result = run_cli(
        argv=[
            "--username",
            "alex",
            "--display-name",
            "Alex",
            "--role",
            role_code,
        ]
    )

    call_arguments = (
        result["repository"]
        .create_user
        .call_args
        .kwargs
    )

    assert call_arguments["role"] is expected_role


def test_cli_supports_no_must_change():
    result = run_cli(
        argv=[
            "--username",
            "alex",
            "--display-name",
            "Alex",
            "--role",
            "ADMINISTRATOR",
            "--no-must-change",
        ]
    )

    call_arguments = (
        result["repository"]
        .create_user
        .call_args
        .kwargs
    )

    assert call_arguments["must_change"] is False


def test_cli_supports_assigning_administrator():
    result = run_cli(
        argv=[
            "--username",
            "coordinator",
            "--display-name",
            "Coordinador",
            "--role",
            "COORDINATOR",
            "--assigned-by-user-id",
            "7",
        ]
    )

    call_arguments = (
        result["repository"]
        .create_user
        .call_args
        .kwargs
    )

    assert (
        call_arguments["assigned_by_user_id"]
        == 7
    )


def test_cli_requires_identity_arguments():
    with pytest.raises(SystemExit) as exc_info:
        main(
            argv=[],
            environ={},
            password_reader=MagicMock(),
        )

    assert exc_info.value.code == 2
