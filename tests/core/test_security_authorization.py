import unittest

from heyti.security import (
    AccessRole,
    AuthorizationEvaluator,
    AuthorizationRequest,
    AuthorizationResource,
    DecisionReason,
    PermissionGrant,
    PermissionScope,
    PrivacyProjection,
    SecurityIdentity,
    TerritorialAccess,
)


def identity(
    *,
    user_id=10,
    session_id="SESSION-SECURITY",
    role=AccessRole.PROMOTER,
    active=True,
    team_ids=frozenset({20}),
    municipalities=frozenset({"20"}),
    sections=frozenset({"1481"}),
):
    return SecurityIdentity(
        user_id=user_id,
        session_id=session_id,
        role=role,
        active=active,
        team_ids=team_ids,
        territorial_access=TerritorialAccess(
            municipality_codes=municipalities,
            section_codes=sections,
        ),
    )


def request(
    permission_code,
    *,
    security_identity=None,
    session_id="SESSION-SECURITY",
    owner_user_id=None,
    team_id=None,
    municipality_code=None,
    section_code=None,
):
    return AuthorizationRequest(
        permission_code=permission_code,
        session_id=session_id,
        identity=security_identity,
        resource=AuthorizationResource(
            resource_type="FIELD_RECORD",
            resource_ref="FIELD-TEST",
            owner_user_id=owner_user_id,
            team_id=team_id,
            municipality_code=municipality_code,
            section_code=section_code,
        ),
    )


class AuthorizationEvaluatorTests(unittest.TestCase):
    def setUp(self):
        self.evaluator = AuthorizationEvaluator()

    def test_missing_identity_is_denied(self):
        decision = self.evaluator.evaluate(
            request("FIELD_MAP_READ"),
            [],
        )

        self.assertFalse(decision.allowed)
        self.assertEqual(
            decision.reason,
            DecisionReason.AUTHENTICATION_REQUIRED,
        )
        self.assertEqual(
            decision.privacy_projection,
            PrivacyProjection.REDACTED,
        )

    def test_mismatched_session_is_denied(self):
        decision = self.evaluator.evaluate(
            request(
                "FIELD_MAP_READ",
                security_identity=identity(),
                session_id="ANOTHER-SESSION",
            ),
            [
                PermissionGrant(
                    "FIELD_MAP_READ",
                    PermissionScope.ASSIGNED_TERRITORY,
                )
            ],
        )

        self.assertEqual(
            decision.reason,
            DecisionReason.SESSION_INVALID,
        )

    def test_inactive_user_is_denied(self):
        decision = self.evaluator.evaluate(
            request(
                "FIELD_MAP_READ",
                security_identity=identity(active=False),
            ),
            [
                PermissionGrant(
                    "FIELD_MAP_READ",
                    PermissionScope.ASSIGNED_TERRITORY,
                )
            ],
        )

        self.assertEqual(
            decision.reason,
            DecisionReason.USER_INACTIVE,
        )

    def test_ungranted_permission_is_denied_by_default(self):
        decision = self.evaluator.evaluate(
            request(
                "FIELD_EXPORT_PERSONAL",
                security_identity=identity(),
            ),
            [],
        )

        self.assertEqual(
            decision.reason,
            DecisionReason.PERMISSION_NOT_GRANTED,
        )

    def test_administrator_global_access_is_authorized(self):
        administrator = identity(
            role=AccessRole.ADMINISTRATOR,
            team_ids=frozenset(),
            municipalities=frozenset(),
            sections=frozenset(),
        )

        decision = self.evaluator.evaluate(
            request(
                "FIELD_PERSONAL_DATA_READ",
                security_identity=administrator,
            ),
            [
                PermissionGrant(
                    "FIELD_PERSONAL_DATA_READ",
                    PermissionScope.GLOBAL,
                    audit_required=True,
                )
            ],
        )

        self.assertTrue(decision.allowed)
        self.assertEqual(
            decision.privacy_projection,
            PrivacyProjection.FULL_PERSONAL,
        )

    def test_coordinator_accesses_assigned_team(self):
        coordinator = identity(
            role=AccessRole.COORDINATOR,
        )

        decision = self.evaluator.evaluate(
            request(
                "FIELD_RECORD_UPDATE",
                security_identity=coordinator,
                team_id=20,
            ),
            [
                PermissionGrant(
                    "FIELD_RECORD_UPDATE",
                    PermissionScope.ASSIGNED_TEAM,
                    audit_required=True,
                )
            ],
        )

        self.assertTrue(decision.allowed)

    def test_coordinator_cannot_access_another_team(self):
        decision = self.evaluator.evaluate(
            request(
                "FIELD_RECORD_UPDATE",
                security_identity=identity(
                    role=AccessRole.COORDINATOR,
                ),
                team_id=99,
            ),
            [
                PermissionGrant(
                    "FIELD_RECORD_UPDATE",
                    PermissionScope.ASSIGNED_TEAM,
                )
            ],
        )

        self.assertEqual(
            decision.reason,
            DecisionReason.RESOURCE_OUTSIDE_SCOPE,
        )

    def test_promoter_accesses_own_record_only(self):
        grant = PermissionGrant(
            "FIELD_RECORD_UPDATE",
            PermissionScope.OWN_RECORDS,
            audit_required=True,
        )

        own_decision = self.evaluator.evaluate(
            request(
                "FIELD_RECORD_UPDATE",
                security_identity=identity(user_id=10),
                owner_user_id=10,
            ),
            [grant],
        )

        other_decision = self.evaluator.evaluate(
            request(
                "FIELD_RECORD_UPDATE",
                security_identity=identity(user_id=10),
                owner_user_id=11,
            ),
            [grant],
        )

        self.assertTrue(own_decision.allowed)
        self.assertFalse(other_decision.allowed)

    def test_assigned_section_is_authorized(self):
        grant = PermissionGrant(
            "FIELD_MAP_READ",
            PermissionScope.ASSIGNED_TERRITORY,
        )

        allowed = self.evaluator.evaluate(
            request(
                "FIELD_MAP_READ",
                security_identity=identity(),
                section_code="1481",
            ),
            [grant],
        )

        denied = self.evaluator.evaluate(
            request(
                "FIELD_MAP_READ",
                security_identity=identity(),
                section_code="9999",
            ),
            [grant],
        )

        self.assertTrue(allowed.allowed)
        self.assertFalse(denied.allowed)

    def test_decision_contract_is_serializable(self):
        decision = self.evaluator.evaluate(
            request(
                "FIELD_MAP_READ",
                security_identity=identity(),
                section_code="1481",
            ),
            [
                PermissionGrant(
                    "FIELD_MAP_READ",
                    PermissionScope.ASSIGNED_TERRITORY,
                )
            ],
        )

        self.assertEqual(
            decision.to_dict(),
            {
                "contract": "HEYTI_AUTHORIZATION_DECISION",
                "version": "1.0",
                "allowed": True,
                "permission": "FIELD_MAP_READ",
                "scope": "ASSIGNED_TERRITORY",
                "reason_code": "AUTHORIZED",
                "audit_required": False,
                "privacy_projection": "PUBLIC_OPERATIONAL",
            },
        )


if __name__ == "__main__":
    unittest.main()