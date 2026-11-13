from unittest.mock import MagicMock

import pytest

from heyti.security.scope_assignment import (
    AssignedTerritorialScope,
    ScopeAssignmentRequest,
    TerritorialScopeAssignmentService,
    TerritorialScopeType,
)


def assigned_scope(
    *,
    scope_type=TerritorialScopeType.MUNICIPALITY,
    section_count=50,
):
    return AssignedTerritorialScope(
        assignment_id=10,
        scope_id=20,
        user_id=7,
        scope_name="Abasolo",
        scope_type=scope_type,
        section_count=section_count,
    )


def make_service(result=None):
    repository = MagicMock()

    if result is None:
        result = assigned_scope()

    repository.assign_scope.return_value = result

    return (
        TerritorialScopeAssignmentService(
            repository
        ),
        repository,
    )


def test_assigns_normalized_municipality():
    service, repository = make_service()

    result = service.assign(
        ScopeAssignmentRequest(
            user_id=7,
            scope_name="  Abasolo  ",
            scope_type=(
                TerritorialScopeType.MUNICIPALITY
            ),
            municipality_id=1,
            assigned_by_user_id=3,
        )
    )

    assert result == assigned_scope()

    repository.assign_scope.assert_called_once_with(
        user_id=7,
        scope_name="Abasolo",
        scope_type=(
            TerritorialScopeType.MUNICIPALITY
        ),
        municipality_id=1,
        section_codes=(),
        assigned_by_user_id=3,
    )


def test_assigns_normalized_section_set():
    result = assigned_scope(
        scope_type=(
            TerritorialScopeType.SECTION_SET
        ),
        section_count=3,
    )
    service, repository = make_service(result)

    actual = service.assign(
        ScopeAssignmentRequest(
            user_id=8,
            scope_name="Secciones prioritarias",
            scope_type=(
                TerritorialScopeType.SECTION_SET
            ),
            section_codes=(
                " 1481 ",
                "100",
                "1481",
                "99",
            ),
        )
    )

    assert actual == result

    call = repository.assign_scope.call_args

    assert call.kwargs["section_codes"] == (
        "99",
        "100",
        "1481",
    )
    assert call.kwargs["municipality_id"] is None


def test_assigns_global_without_resources():
    result = assigned_scope(
        scope_type=TerritorialScopeType.GLOBAL,
        section_count=0,
    )
    service, repository = make_service(result)

    actual = service.assign(
        ScopeAssignmentRequest(
            user_id=3,
            scope_name="Acceso estatal",
            scope_type=TerritorialScopeType.GLOBAL,
        )
    )

    assert actual == result
    assert (
        repository.assign_scope.call_args
        .kwargs["section_codes"]
        == ()
    )


@pytest.mark.parametrize(
    "scope_request",
    [
        ScopeAssignmentRequest(
            user_id=7,
            scope_name="Global invalido",
            scope_type=TerritorialScopeType.GLOBAL,
            municipality_id=1,
        ),
        ScopeAssignmentRequest(
            user_id=7,
            scope_name="Global invalido",
            scope_type=TerritorialScopeType.GLOBAL,
            section_codes=("1481",),
        ),
        ScopeAssignmentRequest(
            user_id=7,
            scope_name="Municipio invalido",
            scope_type=(
                TerritorialScopeType.MUNICIPALITY
            ),
        ),
        ScopeAssignmentRequest(
            user_id=7,
            scope_name="Municipio invalido",
            scope_type=(
                TerritorialScopeType.MUNICIPALITY
            ),
            municipality_id=1,
            section_codes=("1481",),
        ),
        ScopeAssignmentRequest(
            user_id=7,
            scope_name="Conjunto invalido",
            scope_type=(
                TerritorialScopeType.SECTION_SET
            ),
        ),
        ScopeAssignmentRequest(
            user_id=7,
            scope_name="Conjunto invalido",
            scope_type=(
                TerritorialScopeType.SECTION_SET
            ),
            municipality_id=1,
            section_codes=("1481",),
        ),
    ],
)
def test_rejects_incompatible_scope_shape(
    scope_request,
):
    service, repository = make_service()

    with pytest.raises(
        (TypeError, ValueError)
    ):
        service.assign(scope_request)

    repository.assign_scope.assert_not_called()


@pytest.mark.parametrize(
    "user_id",
    [
        None,
        True,
        0,
        -1,
        "7",
    ],
)
def test_rejects_invalid_user_id(user_id):
    service, repository = make_service()

    with pytest.raises(
        (TypeError, ValueError)
    ):
        service.assign(
            ScopeAssignmentRequest(
                user_id=user_id,
                scope_name="Abasolo",
                scope_type=(
                    TerritorialScopeType.MUNICIPALITY
                ),
                municipality_id=1,
            )
        )

    repository.assign_scope.assert_not_called()


@pytest.mark.parametrize(
    "scope_name",
    [
        None,
        "",
        "   ",
    ],
)
def test_rejects_invalid_scope_name(scope_name):
    service, repository = make_service()

    with pytest.raises(
        (TypeError, ValueError)
    ):
        service.assign(
            ScopeAssignmentRequest(
                user_id=7,
                scope_name=scope_name,
                scope_type=(
                    TerritorialScopeType.MUNICIPALITY
                ),
                municipality_id=1,
            )
        )

    repository.assign_scope.assert_not_called()


def test_rejects_non_tuple_section_codes():
    service, repository = make_service()

    with pytest.raises(
        TypeError,
        match="section_codes debe ser una tupla",
    ):
        service.assign(
            ScopeAssignmentRequest(
                user_id=7,
                scope_name="Secciones",
                scope_type=(
                    TerritorialScopeType.SECTION_SET
                ),
                section_codes=["1481"],
            )
        )

    repository.assign_scope.assert_not_called()


def test_rejects_incompatible_repository():
    with pytest.raises(TypeError):
        TerritorialScopeAssignmentService(
            object()
        )
