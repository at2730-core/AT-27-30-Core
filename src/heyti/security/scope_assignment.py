from dataclasses import dataclass
from enum import Enum


class TerritorialScopeType(str, Enum):
    GLOBAL = "GLOBAL"
    MUNICIPALITY = "MUNICIPALITY"
    SECTION_SET = "SECTION_SET"


@dataclass(frozen=True)
class ScopeAssignmentRequest:
    user_id: int
    scope_name: str
    scope_type: TerritorialScopeType
    municipality_id: int | None = None
    section_codes: tuple[str, ...] = ()
    assigned_by_user_id: int | None = None


@dataclass(frozen=True)
class AssignedTerritorialScope:
    assignment_id: int
    scope_id: int
    user_id: int
    scope_name: str
    scope_type: TerritorialScopeType
    section_count: int


class TerritorialScopeAssignmentService:
    def __init__(self, repository):
        if not callable(
            getattr(
                repository,
                "assign_scope",
                None,
            )
        ):
            raise TypeError(
                "repository debe proporcionar assign_scope"
            )

        self._repository = repository

    def assign(
        self,
        request: ScopeAssignmentRequest,
    ) -> AssignedTerritorialScope:
        if not isinstance(
            request,
            ScopeAssignmentRequest,
        ):
            raise TypeError(
                "request debe ser ScopeAssignmentRequest"
            )

        user_id = self._positive_id(
            request.user_id,
            "user_id",
        )

        scope_name = self._normalize_text(
            request.scope_name,
            "scope_name",
        )

        if not isinstance(
            request.scope_type,
            TerritorialScopeType,
        ):
            raise TypeError(
                "scope_type debe ser TerritorialScopeType"
            )

        assigned_by_user_id = (
            request.assigned_by_user_id
        )

        if assigned_by_user_id is not None:
            assigned_by_user_id = self._positive_id(
                assigned_by_user_id,
                "assigned_by_user_id",
            )

        municipality_id = request.municipality_id
        section_codes = self._section_codes(
            request.section_codes
        )

        if (
            request.scope_type
            is TerritorialScopeType.GLOBAL
        ):
            if (
                municipality_id is not None
                or section_codes
            ):
                raise ValueError(
                    "GLOBAL no admite municipio "
                    "ni secciones"
                )

        elif (
            request.scope_type
            is TerritorialScopeType.MUNICIPALITY
        ):
            municipality_id = self._positive_id(
                municipality_id,
                "municipality_id",
            )

            if section_codes:
                raise ValueError(
                    "MUNICIPALITY no admite "
                    "section_codes"
                )

        elif (
            request.scope_type
            is TerritorialScopeType.SECTION_SET
        ):
            if municipality_id is not None:
                raise ValueError(
                    "SECTION_SET no admite "
                    "municipality_id"
                )

            if not section_codes:
                raise ValueError(
                    "SECTION_SET requiere "
                    "al menos una seccion"
                )

        return self._repository.assign_scope(
            user_id=user_id,
            scope_name=scope_name,
            scope_type=request.scope_type,
            municipality_id=municipality_id,
            section_codes=section_codes,
            assigned_by_user_id=(
                assigned_by_user_id
            ),
        )

    @staticmethod
    def _positive_id(value, field_name) -> int:
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
        ):
            raise TypeError(
                f"{field_name} debe ser entero"
            )

        if value <= 0:
            raise ValueError(
                f"{field_name} debe ser positivo"
            )

        return value

    @staticmethod
    def _normalize_text(value, field_name) -> str:
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} debe ser una cadena"
            )

        normalized = value.strip()

        if not normalized:
            raise ValueError(
                f"{field_name} no puede estar vacio"
            )

        return normalized

    @classmethod
    def _section_codes(
        cls,
        values,
    ) -> tuple[str, ...]:
        if not isinstance(values, tuple):
            raise TypeError(
                "section_codes debe ser una tupla"
            )

        normalized = []

        for value in values:
            code = cls._normalize_text(
                value,
                "section_code",
            )

            normalized.append(code)

        return tuple(
            sorted(
                set(normalized),
                key=lambda code: (
                    0,
                    int(code),
                )
                if code.isdigit()
                else (
                    1,
                    code,
                ),
            )
        )
