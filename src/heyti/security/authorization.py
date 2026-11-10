from collections.abc import Iterable

from heyti.security.contracts import (
    AuthorizationDecision,
    AuthorizationRequest,
    DecisionReason,
    PermissionGrant,
    PermissionScope,
    PrivacyProjection,
)


PERSONAL_DATA_PERMISSION = "FIELD_PERSONAL_DATA_READ"


class AuthorizationEvaluator:
    def evaluate(
        self,
        request: AuthorizationRequest,
        grants: Iterable[PermissionGrant],
    ) -> AuthorizationDecision:
        if not isinstance(request, AuthorizationRequest):
            raise TypeError(
                "request debe ser AuthorizationRequest"
            )

        identity = request.identity

        if identity is None:
            return self._deny(
                request,
                DecisionReason.AUTHENTICATION_REQUIRED,
            )

        if request.session_id != identity.session_id:
            return self._deny(
                request,
                DecisionReason.SESSION_INVALID,
            )

        if not identity.active:
            return self._deny(
                request,
                DecisionReason.USER_INACTIVE,
            )

        grant = self._find_grant(
            request.permission_code,
            grants,
        )

        if grant is None:
            return self._deny(
                request,
                DecisionReason.PERMISSION_NOT_GRANTED,
            )

        if not self._within_scope(
            request,
            grant,
        ):
            return self._deny(
                request,
                DecisionReason.RESOURCE_OUTSIDE_SCOPE,
                scope=grant.scope,
            )

        return AuthorizationDecision(
            allowed=True,
            permission_code=request.permission_code,
            reason=DecisionReason.AUTHORIZED,
            scope=grant.scope,
            audit_required=grant.audit_required,
            privacy_projection=self._privacy_projection(
                request,
                grant,
            ),
        )

    @staticmethod
    def _find_grant(
        permission_code: str,
        grants: Iterable[PermissionGrant],
    ) -> PermissionGrant | None:
        for grant in grants:
            if not isinstance(grant, PermissionGrant):
                raise TypeError(
                    "grants debe contener PermissionGrant"
                )

            if grant.permission_code == permission_code:
                return grant

        return None

    @staticmethod
    def _within_scope(
        request: AuthorizationRequest,
        grant: PermissionGrant,
    ) -> bool:
        identity = request.identity

        if identity is None:
            return False

        resource = request.resource

        if grant.scope is PermissionScope.GLOBAL:
            return True

        if (
            grant.scope
            is PermissionScope.ASSIGNED_TERRITORY
        ):
            if (
                resource.municipality_code is None
                and resource.section_code is None
            ):
                return (
                    identity.territorial_access
                    .has_assignments()
                )

            return identity.territorial_access.contains(
                resource.municipality_code,
                resource.section_code,
            )

        if grant.scope is PermissionScope.ASSIGNED_TEAM:
            return (
                resource.team_id is not None
                and resource.team_id in identity.team_ids
            )

        if grant.scope in (
            PermissionScope.OWN_RECORDS,
            PermissionScope.OWN_ACTIVITY,
        ):
            return (
                resource.owner_user_id
                == identity.user_id
            )

        return False

    @staticmethod
    def _privacy_projection(
        request: AuthorizationRequest,
        grant: PermissionGrant,
    ) -> PrivacyProjection:
        if (
            request.permission_code
            != PERSONAL_DATA_PERMISSION
        ):
            return PrivacyProjection.PUBLIC_OPERATIONAL

        if grant.scope is PermissionScope.GLOBAL:
            return PrivacyProjection.FULL_PERSONAL

        return PrivacyProjection.ASSIGNED_PERSONAL

    @staticmethod
    def _deny(
        request: AuthorizationRequest,
        reason: DecisionReason,
        scope: PermissionScope | None = None,
    ) -> AuthorizationDecision:
        return AuthorizationDecision(
            allowed=False,
            permission_code=request.permission_code,
            reason=reason,
            scope=scope,
            audit_required=True,
            privacy_projection=PrivacyProjection.REDACTED,
        )