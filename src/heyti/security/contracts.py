from dataclasses import dataclass, field
from enum import Enum
from typing import Any


AUTHORIZATION_CONTRACT = "HEYTI_AUTHORIZATION_DECISION"
AUTHORIZATION_VERSION = "1.0"


class AccessRole(str, Enum):
    ADMINISTRATOR = "ADMINISTRATOR"
    COORDINATOR = "COORDINATOR"
    PROMOTER = "PROMOTER"


class PermissionScope(str, Enum):
    GLOBAL = "GLOBAL"
    ASSIGNED_TERRITORY = "ASSIGNED_TERRITORY"
    ASSIGNED_TEAM = "ASSIGNED_TEAM"
    OWN_RECORDS = "OWN_RECORDS"
    OWN_ACTIVITY = "OWN_ACTIVITY"


class DecisionReason(str, Enum):
    AUTHORIZED = "AUTHORIZED"
    AUTHENTICATION_REQUIRED = "AUTHENTICATION_REQUIRED"
    SESSION_INVALID = "SESSION_INVALID"
    USER_INACTIVE = "USER_INACTIVE"
    PERMISSION_NOT_GRANTED = "PERMISSION_NOT_GRANTED"
    RESOURCE_OUTSIDE_SCOPE = "RESOURCE_OUTSIDE_SCOPE"
    PERSONAL_DATA_RESTRICTED = "PERSONAL_DATA_RESTRICTED"
    JUSTIFICATION_REQUIRED = "JUSTIFICATION_REQUIRED"
    DENIED_BY_DEFAULT = "DENIED_BY_DEFAULT"


class PrivacyProjection(str, Enum):
    PUBLIC_OPERATIONAL = "PUBLIC_OPERATIONAL"
    ASSIGNED_PERSONAL = "ASSIGNED_PERSONAL"
    FULL_PERSONAL = "FULL_PERSONAL"
    REDACTED = "REDACTED"


def _validate_non_empty(value: str, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(
            f"{field_name} debe ser una cadena no vacía"
        )


def _validate_positive_identifier(
    value: int,
    field_name: str,
) -> None:
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise ValueError(
            f"{field_name} debe ser un entero positivo"
        )


@dataclass(frozen=True)
class TerritorialAccess:
    global_access: bool = False
    municipality_codes: frozenset[str] = field(
        default_factory=frozenset
    )
    section_codes: frozenset[str] = field(
        default_factory=frozenset
    )

    def __post_init__(self) -> None:
        if not isinstance(self.global_access, bool):
            raise TypeError(
                "global_access debe ser booleano"
            )

        for field_name, values in (
            ("municipality_codes", self.municipality_codes),
            ("section_codes", self.section_codes),
        ):
            if not isinstance(values, frozenset):
                raise TypeError(
                    f"{field_name} debe ser frozenset"
                )

            for value in values:
                _validate_non_empty(value, field_name)

    def has_assignments(self) -> bool:
        return bool(
            self.global_access
            or self.municipality_codes
            or self.section_codes
        )

    def contains(
        self,
        municipality_code: str | None,
        section_code: str | None,
    ) -> bool:
        if self.global_access:
            return True

        if (
            section_code is not None
            and section_code in self.section_codes
        ):
            return True

        if (
            municipality_code is not None
            and municipality_code in self.municipality_codes
        ):
            return True

        return False


@dataclass(frozen=True)
class SecurityIdentity:
    user_id: int
    session_id: str
    role: AccessRole
    active: bool = True
    team_ids: frozenset[int] = field(
        default_factory=frozenset
    )
    territorial_access: TerritorialAccess = field(
        default_factory=TerritorialAccess
    )

    def __post_init__(self) -> None:
        _validate_positive_identifier(
            self.user_id,
            "user_id",
        )
        _validate_non_empty(
            self.session_id,
            "session_id",
        )

        if not isinstance(self.role, AccessRole):
            raise TypeError(
                "role debe ser AccessRole"
            )

        if not isinstance(self.active, bool):
            raise TypeError(
                "active debe ser booleano"
            )

        if not isinstance(self.team_ids, frozenset):
            raise TypeError(
                "team_ids debe ser frozenset"
            )

        for team_id in self.team_ids:
            _validate_positive_identifier(
                team_id,
                "team_id",
            )


@dataclass(frozen=True)
class AuthorizationResource:
    resource_type: str
    resource_ref: str | None = None
    owner_user_id: int | None = None
    team_id: int | None = None
    municipality_code: str | None = None
    section_code: str | None = None

    def __post_init__(self) -> None:
        _validate_non_empty(
            self.resource_type,
            "resource_type",
        )

        if self.resource_ref is not None:
            _validate_non_empty(
                self.resource_ref,
                "resource_ref",
            )

        for field_name, value in (
            ("owner_user_id", self.owner_user_id),
            ("team_id", self.team_id),
        ):
            if value is not None:
                _validate_positive_identifier(
                    value,
                    field_name,
                )

        for field_name, value in (
            ("municipality_code", self.municipality_code),
            ("section_code", self.section_code),
        ):
            if value is not None:
                _validate_non_empty(
                    value,
                    field_name,
                )


@dataclass(frozen=True)
class PermissionGrant:
    permission_code: str
    scope: PermissionScope
    audit_required: bool = False

    def __post_init__(self) -> None:
        _validate_non_empty(
            self.permission_code,
            "permission_code",
        )

        if not isinstance(self.scope, PermissionScope):
            raise TypeError(
                "scope debe ser PermissionScope"
            )

        if not isinstance(self.audit_required, bool):
            raise TypeError(
                "audit_required debe ser booleano"
            )


@dataclass(frozen=True)
class AuthorizationRequest:
    permission_code: str
    session_id: str
    resource: AuthorizationResource
    identity: SecurityIdentity | None = None

    def __post_init__(self) -> None:
        _validate_non_empty(
            self.permission_code,
            "permission_code",
        )
        _validate_non_empty(
            self.session_id,
            "session_id",
        )

        if not isinstance(
            self.resource,
            AuthorizationResource,
        ):
            raise TypeError(
                "resource debe ser AuthorizationResource"
            )


@dataclass(frozen=True)
class AuthorizationDecision:
    allowed: bool
    permission_code: str
    reason: DecisionReason
    scope: PermissionScope | None
    audit_required: bool
    privacy_projection: PrivacyProjection

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract": AUTHORIZATION_CONTRACT,
            "version": AUTHORIZATION_VERSION,
            "allowed": self.allowed,
            "permission": self.permission_code,
            "scope": (
                self.scope.value
                if self.scope is not None
                else None
            ),
            "reason_code": self.reason.value,
            "audit_required": self.audit_required,
            "privacy_projection": (
                self.privacy_projection.value
            ),
        }