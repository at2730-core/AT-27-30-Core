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


def make_application(decision=None):
    authentication_service = MagicMock()
    authentication_service.authenticate = MagicMock()

    session_service = MagicMock()
    session_service.create_session = MagicMock()
    session_service.resolve = MagicMock()
    session_service.revoke = MagicMock()

    authorization_service = MagicMock()

    if decision is None:
        decision = AuthorizationDecision(
            allowed=True,
            permission_code="FIELD_MAP_READ",
            reason=DecisionReason.AUTHORIZED,
            scope=PermissionScope.GLOBAL,
            audit_required=False,
            privacy_projection=(
                PrivacyProjection.PUBLIC_OPERATIONAL
            ),
        )

    authorization_service.authorize.return_value = (
        decision
    )

    application = SecurityHttpApplication(
        authentication_service=authentication_service,
        session_service=session_service,
        authorization_service=authorization_service,
    )

    return application, authorization_service


def test_summary_uses_field_summary_permission():
    application, authorization_service = (
        make_application()
    )

    application.authorize_field_operation(
        user_id=3,
        session_id="TOKEN-ALEX",
        payload={"operation": "summary"},
    )

    call = authorization_service.authorize.call_args

    assert call.kwargs["user_id"] == 3
    assert call.kwargs["session_id"] == "TOKEN-ALEX"
    assert (
        call.kwargs["permission_code"]
        == "FIELD_SUMMARY_READ"
    )

    resource = call.kwargs["resource"]

    assert resource.resource_type == "FIELD_SUMMARY"
    assert resource.resource_ref == "summary"
    assert resource.section_code is None


def test_map_uses_field_map_permission_and_section():
    application, authorization_service = (
        make_application()
    )

    application.authorize_field_operation(
        user_id=7,
        session_id="TOKEN-7",
        payload={
            "operation": "map",
            "section_code": " 1481 ",
        },
    )

    call = authorization_service.authorize.call_args

    assert (
        call.kwargs["permission_code"]
        == "FIELD_MAP_READ"
    )

    resource = call.kwargs["resource"]

    assert resource.resource_type == "FIELD_MAP"
    assert resource.resource_ref == "map"
    assert resource.section_code == "1481"


def test_global_map_can_omit_section():
    application, _ = make_application()

    decision = application.authorize_field_operation(
        user_id=3,
        session_id="TOKEN-ALEX",
        payload={"operation": "map"},
    )

    assert decision.allowed is True
    assert decision.scope is PermissionScope.GLOBAL


def test_scoped_map_cannot_omit_section():
    scoped_decision = AuthorizationDecision(
        allowed=True,
        permission_code="FIELD_MAP_READ",
        reason=DecisionReason.AUTHORIZED,
        scope=PermissionScope.ASSIGNED_TERRITORY,
        audit_required=False,
        privacy_projection=(
            PrivacyProjection.PUBLIC_OPERATIONAL
        ),
    )

    application, _ = make_application(
        decision=scoped_decision
    )

    decision = application.authorize_field_operation(
        user_id=7,
        session_id="TOKEN-7",
        payload={"operation": "map"},
    )

    assert decision.allowed is False
    assert decision.reason is (
        DecisionReason.RESOURCE_OUTSIDE_SCOPE
    )
    assert decision.audit_required is True
    assert decision.privacy_projection is (
        PrivacyProjection.REDACTED
    )


@pytest.mark.parametrize(
    "payload",
    [
        {"operation": "unknown"},
        {"operation": "map", "section_code": ""},
        {"operation": "map", "section_code": "   "},
    ],
)
def test_invalid_field_request_is_rejected(payload):
    application, authorization_service = (
        make_application()
    )

    with pytest.raises(ValueError):
        application.authorize_field_operation(
            user_id=7,
            session_id="TOKEN-7",
            payload=payload,
        )

    authorization_service.authorize.assert_not_called()


def test_authorization_service_is_required():
    authentication_service = MagicMock()
    authentication_service.authenticate = MagicMock()

    session_service = MagicMock()
    session_service.create_session = MagicMock()
    session_service.resolve = MagicMock()
    session_service.revoke = MagicMock()

    application = SecurityHttpApplication(
        authentication_service=authentication_service,
        session_service=session_service,
    )

    with pytest.raises(
        RuntimeError,
        match="autorizacion no esta configurada",
    ):
        application.authorize_field_operation(
            user_id=3,
            session_id="TOKEN-ALEX",
            payload={"operation": "summary"},
        )
