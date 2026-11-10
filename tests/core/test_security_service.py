from unittest.mock import MagicMock

import pytest

from heyti.security.contracts import (
    AccessRole,
    AuthorizationResource,
    DecisionReason,
    PermissionGrant,
    PermissionScope,
    PrivacyProjection,
    SecurityIdentity,
    TerritorialAccess,
)
from heyti.security.service import (
    AuthorizationService,
)


def make_identity(
    *,
    active=True,
    role=AccessRole.COORDINATOR,
):
    return SecurityIdentity(
        user_id=7,
        session_id="SESSION-7",
        role=role,
        active=active,
        team_ids=frozenset({41}),
        territorial_access=TerritorialAccess(
            section_codes=frozenset({"1481"}),
        ),
    )


def make_resource():
    return AuthorizationResource(
        resource_type="FIELD_RECORD",
        resource_ref="ACTOR-1",
        owner_user_id=7,
        team_id=41,
        section_code="1481",
    )


def test_service_authorizes_from_source_data():
    source = MagicMock()
    source.identity.return_value = make_identity()
    source.grants.return_value = (
        PermissionGrant(
            permission_code="FIELD_MAP_READ",
            scope=(
                PermissionScope.ASSIGNED_TERRITORY
            ),
        ),
    )

    service = AuthorizationService(source)

    decision = service.authorize(
        user_id=7,
        session_id="SESSION-7",
        permission_code="FIELD_MAP_READ",
        resource=make_resource(),
    )

    assert decision.allowed is True
    assert decision.reason is DecisionReason.AUTHORIZED
    assert decision.scope is (
        PermissionScope.ASSIGNED_TERRITORY
    )
    assert decision.privacy_projection is (
        PrivacyProjection.PUBLIC_OPERATIONAL
    )

    source.identity.assert_called_once_with(
        user_id=7,
        session_id="SESSION-7",
    )
    source.grants.assert_called_once_with(
        AccessRole.COORDINATOR
    )


def test_service_denies_unknown_identity():
    source = MagicMock()
    source.identity.return_value = None

    service = AuthorizationService(source)

    decision = service.authorize(
        user_id=999,
        session_id="SESSION-999",
        permission_code="FIELD_MAP_READ",
        resource=make_resource(),
    )

    assert decision.allowed is False
    assert decision.reason is (
        DecisionReason.AUTHENTICATION_REQUIRED
    )
    assert decision.privacy_projection is (
        PrivacyProjection.REDACTED
    )
    source.grants.assert_not_called()


def test_service_denies_inactive_identity_without_grants():
    source = MagicMock()
    source.identity.return_value = make_identity(
        active=False
    )

    service = AuthorizationService(source)

    decision = service.authorize(
        user_id=7,
        session_id="SESSION-7",
        permission_code="FIELD_MAP_READ",
        resource=make_resource(),
    )

    assert decision.allowed is False
    assert decision.reason is (
        DecisionReason.USER_INACTIVE
    )
    source.grants.assert_not_called()


def test_service_preserves_audit_requirement():
    source = MagicMock()
    source.identity.return_value = make_identity(
        role=AccessRole.ADMINISTRATOR
    )
    source.grants.return_value = (
        PermissionGrant(
            permission_code=(
                "FIELD_PERSONAL_DATA_READ"
            ),
            scope=PermissionScope.GLOBAL,
            audit_required=True,
        ),
    )

    service = AuthorizationService(source)

    decision = service.authorize(
        user_id=7,
        session_id="SESSION-7",
        permission_code=(
            "FIELD_PERSONAL_DATA_READ"
        ),
        resource=make_resource(),
    )

    assert decision.allowed is True
    assert decision.audit_required is True
    assert decision.privacy_projection is (
        PrivacyProjection.FULL_PERSONAL
    )


def test_service_denies_resource_outside_scope():
    source = MagicMock()
    source.identity.return_value = make_identity()
    source.grants.return_value = (
        PermissionGrant(
            permission_code="FIELD_MAP_READ",
            scope=(
                PermissionScope.ASSIGNED_TERRITORY
            ),
        ),
    )

    service = AuthorizationService(source)

    resource = AuthorizationResource(
        resource_type="FIELD_RECORD",
        section_code="9999",
    )

    decision = service.authorize(
        user_id=7,
        session_id="SESSION-7",
        permission_code="FIELD_MAP_READ",
        resource=resource,
    )

    assert decision.allowed is False
    assert decision.reason is (
        DecisionReason.RESOURCE_OUTSIDE_SCOPE
    )


@pytest.mark.parametrize(
    "source",
    [
        None,
        object(),
    ],
)
def test_service_rejects_invalid_source(source):
    with pytest.raises(TypeError):
        AuthorizationService(source)


def test_service_rejects_invalid_evaluator():
    source = MagicMock()

    with pytest.raises(
        TypeError,
        match="evaluator debe proporcionar evaluate",
    ):
        AuthorizationService(
            source,
            evaluator=object(),
        )
