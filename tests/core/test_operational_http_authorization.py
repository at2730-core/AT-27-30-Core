from unittest.mock import MagicMock

import pytest

from heyti.security.contracts import (
    AuthorizationDecision,
    DecisionReason,
    PermissionScope,
    PrivacyProjection,
)
from heyti.security.http_application import (
    SecurityHttpApplication,
)


def make_application(
    scope=PermissionScope.GLOBAL,
):
    authentication_service = MagicMock()
    authentication_service.authenticate = MagicMock()

    session_service = MagicMock()
    session_service.create_session = MagicMock()
    session_service.resolve = MagicMock()
    session_service.revoke = MagicMock()

    authorization_service = MagicMock()
    authorization_service.authorize.return_value = (
        AuthorizationDecision(
            allowed=True,
            permission_code="CONTROL_PERMISSION",
            reason=DecisionReason.AUTHORIZED,
            scope=scope,
            audit_required=False,
            privacy_projection=(
                PrivacyProjection.PUBLIC_OPERATIONAL
            ),
        )
    )

    application = SecurityHttpApplication(
        authentication_service=authentication_service,
        session_service=session_service,
        authorization_service=authorization_service,
    )

    return application, authorization_service


def test_section_uses_section_read_permission():
    application, authorization_service = (
        make_application(
            PermissionScope.ASSIGNED_TERRITORY
        )
    )

    application.authorize_section_operation(
        user_id=4,
        session_id="TOKEN-JOSE",
        section_code=" 1261 ",
    )

    call = authorization_service.authorize.call_args

    assert call.kwargs["user_id"] == 4
    assert call.kwargs["session_id"] == "TOKEN-JOSE"
    assert (
        call.kwargs["permission_code"]
        == "SECTION_READ"
    )

    resource = call.kwargs["resource"]

    assert resource.resource_type == "SECTION"
    assert resource.resource_ref == "1261"
    assert resource.section_code == "1261"
    assert resource.municipality_code is None


@pytest.mark.parametrize(
    "section_code",
    (
        None,
        "",
        " ",
        "ABC",
        "0",
        "-1",
    ),
)
def test_section_rejects_invalid_identity(
    section_code,
):
    application, authorization_service = (
        make_application()
    )

    with pytest.raises(ValueError):
        application.authorize_section_operation(
            user_id=4,
            session_id="TOKEN-JOSE",
            section_code=section_code,
        )

    authorization_service.authorize.assert_not_called()


def test_catalog_uses_catalog_permission():
    application, authorization_service = (
        make_application(
            PermissionScope.ASSIGNED_TERRITORY
        )
    )

    decision = application.authorize_universe_operation(
        user_id=4,
        session_id="TOKEN-JOSE",
        payload={"operation": "catalog"},
    )

    assert decision.allowed is True

    call = authorization_service.authorize.call_args

    assert (
        call.kwargs["permission_code"]
        == "UNIVERSE_CATALOG_READ"
    )

    resource = call.kwargs["resource"]

    assert resource.resource_type == (
        "UNIVERSE_CATALOG"
    )
    assert resource.resource_ref == "catalog"
    assert resource.municipality_code is None
    assert resource.section_code is None


def test_municipality_map_uses_assigned_municipality():
    application, authorization_service = (
        make_application(
            PermissionScope.ASSIGNED_TERRITORY
        )
    )

    decision = application.authorize_universe_operation(
        user_id=4,
        session_id="TOKEN-JOSE",
        payload={
            "operation": "map",
            "level": "municipality",
            "id": " 20 ",
        },
    )

    assert decision.allowed is True

    call = authorization_service.authorize.call_args

    assert (
        call.kwargs["permission_code"]
        == "UNIVERSE_MAP_READ"
    )

    resource = call.kwargs["resource"]

    assert resource.resource_type == "UNIVERSE_MAP"
    assert resource.resource_ref == "municipality:20"
    assert resource.municipality_code == "20"
    assert resource.section_code is None


@pytest.mark.parametrize(
    "level",
    (
        "state",
        "federal-district",
        "local-district",
    ),
)
def test_scoped_user_cannot_request_broader_map(
    level,
):
    application, _ = make_application(
        PermissionScope.ASSIGNED_TERRITORY
    )

    decision = application.authorize_universe_operation(
        user_id=4,
        session_id="TOKEN-JOSE",
        payload={
            "operation": "map",
            "level": level,
            "id": "11",
        },
    )

    assert decision.allowed is False
    assert decision.reason is (
        DecisionReason.RESOURCE_OUTSIDE_SCOPE
    )
    assert decision.audit_required is True
    assert decision.privacy_projection is (
        PrivacyProjection.REDACTED
    )


def test_global_user_can_request_state_map():
    application, _ = make_application(
        PermissionScope.GLOBAL
    )

    decision = application.authorize_universe_operation(
        user_id=3,
        session_id="TOKEN-ALEX",
        payload={
            "operation": "map",
            "level": "state",
            "id": "11",
        },
    )

    assert decision.allowed is True
    assert decision.scope is PermissionScope.GLOBAL


def test_section_demo_uses_section_permission():
    application, authorization_service = (
        make_application(
            PermissionScope.ASSIGNED_TERRITORY
        )
    )

    application.authorize_universe_operation(
        user_id=4,
        session_id="TOKEN-JOSE",
        payload={
            "operation": "section-demo",
            "section_id": "1261",
        },
    )

    call = authorization_service.authorize.call_args

    assert (
        call.kwargs["permission_code"]
        == "SECTION_READ"
    )
    assert (
        call.kwargs["resource"].section_code
        == "1261"
    )


@pytest.mark.parametrize(
    "payload",
    (
        None,
        {},
        {"operation": "unknown"},
        {
            "operation": "map",
            "level": "county",
            "id": "20",
        },
        {
            "operation": "map",
            "level": "municipality",
            "id": "",
        },
        {
            "operation": "map",
            "level": "municipality",
            "id": 20,
        },
    ),
)
def test_universe_rejects_invalid_request(
    payload,
):
    application, authorization_service = (
        make_application()
    )

    with pytest.raises(ValueError):
        application.authorize_universe_operation(
            user_id=4,
            session_id="TOKEN-JOSE",
            payload=payload,
        )

    authorization_service.authorize.assert_not_called()

def catalog_response():
    return {
        "contract": "HEYTI_UNIVERSE_RESPONSE",
        "version": "1.0",
        "catalog": [
            {
                "level": "state",
                "id": "11",
                "label": "Guanajuato",
                "sections": 3266,
            },
            {
                "level": "municipality",
                "id": "20",
                "label": "Leon",
                "sections": 787,
            },
            {
                "level": "municipality",
                "id": "1",
                "label": "Abasolo",
                "sections": 50,
            },
            {
                "level": "local-district",
                "id": "5",
                "label": "Distrito local 5",
                "sections": 100,
            },
        ],
    }


def test_global_catalog_preserves_all_universes():
    application, _ = make_application()

    profile_service = MagicMock()
    profile_service.profile.return_value.global_access = (
        True
    )
    application._scope_profile_service = profile_service

    original = catalog_response()

    filtered = application.filter_universe_catalog(
        user_id=3,
        response=original,
    )

    assert filtered["catalog"] == original["catalog"]
    assert filtered is not original
    profile_service.profile.assert_called_once_with(
        user_id=3
    )


def test_scoped_catalog_contains_only_assigned_municipality():
    application, _ = make_application(
        PermissionScope.ASSIGNED_TERRITORY
    )

    municipality_scope = MagicMock()
    municipality_scope.municipality_code = "20"

    section_scope = MagicMock()
    section_scope.municipality_code = None

    profile = MagicMock()
    profile.global_access = False
    profile.scopes = (
        municipality_scope,
        section_scope,
    )

    profile_service = MagicMock()
    profile_service.profile.return_value = profile
    application._scope_profile_service = profile_service

    filtered = application.filter_universe_catalog(
        user_id=4,
        response=catalog_response(),
    )

    assert filtered["catalog"] == [
        {
            "level": "municipality",
            "id": "20",
            "label": "Leon",
            "sections": 787,
        }
    ]


def test_section_set_catalog_does_not_expand_to_municipality():
    application, _ = make_application(
        PermissionScope.ASSIGNED_TERRITORY
    )

    section_scope = MagicMock()
    section_scope.municipality_code = None

    profile = MagicMock()
    profile.global_access = False
    profile.scopes = (section_scope,)

    profile_service = MagicMock()
    profile_service.profile.return_value = profile
    application._scope_profile_service = profile_service

    filtered = application.filter_universe_catalog(
        user_id=8,
        response=catalog_response(),
    )

    assert filtered["catalog"] == []


@pytest.mark.parametrize(
    "response",
    (
        None,
        {},
        {"catalog": None},
        {"catalog": ["invalid"]},
        {
            "catalog": [
                {
                    "level": "municipality",
                    "id": "",
                }
            ]
        },
    ),
)
def test_catalog_filter_rejects_invalid_contract(
    response,
):
    application, _ = make_application()

    profile_service = MagicMock()
    profile_service.profile.return_value.global_access = (
        True
    )
    application._scope_profile_service = profile_service

    with pytest.raises(ValueError):
        application.filter_universe_catalog(
            user_id=3,
            response=response,
        )


def test_catalog_filter_requires_scope_profile():
    application, _ = make_application()

    with pytest.raises(
        RuntimeError,
        match="perfil territorial no esta configurado",
    ):
        application.filter_universe_catalog(
            user_id=3,
            response=catalog_response(),
        )
