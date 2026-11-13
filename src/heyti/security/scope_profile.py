from dataclasses import dataclass

from heyti.security.scope_assignment import (
    TerritorialScopeType,
)


@dataclass(frozen=True)
class TerritorialScopeProfile:
    scope_id: int
    scope_name: str
    scope_type: TerritorialScopeType
    municipality_id: int | None
    municipality_code: str | None
    municipality_name: str | None
    section_count: int

    def __post_init__(self) -> None:
        self._positive_id(
            self.scope_id,
            "scope_id",
        )
        self._text(
            self.scope_name,
            "scope_name",
        )

        if not isinstance(
            self.scope_type,
            TerritorialScopeType,
        ):
            raise TypeError(
                "scope_type debe ser TerritorialScopeType"
            )

        if self.municipality_id is not None:
            self._positive_id(
                self.municipality_id,
                "municipality_id",
            )

        for field_name, value in (
            (
                "municipality_code",
                self.municipality_code,
            ),
            (
                "municipality_name",
                self.municipality_name,
            ),
        ):
            if value is not None:
                self._text(
                    value,
                    field_name,
                )

        if (
            isinstance(self.section_count, bool)
            or not isinstance(self.section_count, int)
        ):
            raise TypeError(
                "section_count debe ser entero"
            )

        if self.section_count < 0:
            raise ValueError(
                "section_count no puede ser negativo"
            )

        if (
            self.scope_type
            is TerritorialScopeType.GLOBAL
        ):
            if any(
                value is not None
                for value in (
                    self.municipality_id,
                    self.municipality_code,
                    self.municipality_name,
                )
            ):
                raise ValueError(
                    "GLOBAL no admite municipio"
                )

            if self.section_count != 0:
                raise ValueError(
                    "GLOBAL no materializa secciones"
                )

        if (
            self.scope_type
            is TerritorialScopeType.MUNICIPALITY
        ):
            if any(
                value is None
                for value in (
                    self.municipality_id,
                    self.municipality_code,
                    self.municipality_name,
                )
            ):
                raise ValueError(
                    "MUNICIPALITY requiere municipio"
                )

            if self.section_count <= 0:
                raise ValueError(
                    "MUNICIPALITY requiere secciones"
                )

    def to_dict(self) -> dict:
        return {
            "scope_id": self.scope_id,
            "name": self.scope_name,
            "type": self.scope_type.value,
            "municipality": (
                None
                if self.municipality_id is None
                else {
                    "municipality_id": (
                        self.municipality_id
                    ),
                    "code": self.municipality_code,
                    "name": self.municipality_name,
                }
            ),
            "section_count": self.section_count,
        }

    @staticmethod
    def _positive_id(value, field_name) -> None:
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

    @staticmethod
    def _text(value, field_name) -> None:
        if not isinstance(value, str):
            raise TypeError(
                f"{field_name} debe ser una cadena"
            )

        if not value.strip():
            raise ValueError(
                f"{field_name} no puede estar vacio"
            )


@dataclass(frozen=True)
class TerritorialAccessProfile:
    scopes: tuple[TerritorialScopeProfile, ...]

    def __post_init__(self) -> None:
        if not isinstance(self.scopes, tuple):
            raise TypeError(
                "scopes debe ser una tupla"
            )

        if not all(
            isinstance(scope, TerritorialScopeProfile)
            for scope in self.scopes
        ):
            raise TypeError(
                "scopes contiene un perfil incompatible"
            )

        scope_ids = [
            scope.scope_id
            for scope in self.scopes
        ]

        if len(scope_ids) != len(set(scope_ids)):
            raise ValueError(
                "scopes contiene alcances duplicados"
            )

    @property
    def global_access(self) -> bool:
        return any(
            scope.scope_type
            is TerritorialScopeType.GLOBAL
            for scope in self.scopes
        )

    def to_dict(self) -> dict:
        return {
            "global_access": self.global_access,
            "scopes": [
                scope.to_dict()
                for scope in self.scopes
            ],
        }


class TerritorialScopeProfileService:
    def __init__(self, source):
        if not callable(
            getattr(source, "active_scopes", None)
        ):
            raise TypeError(
                "source debe proporcionar active_scopes"
            )

        self._source = source

    def profile(
        self,
        user_id: int,
    ) -> TerritorialAccessProfile:
        if (
            isinstance(user_id, bool)
            or not isinstance(user_id, int)
        ):
            raise TypeError(
                "user_id debe ser entero"
            )

        if user_id <= 0:
            raise ValueError(
                "user_id debe ser positivo"
            )

        scopes = self._source.active_scopes(
            user_id=user_id
        )

        if not isinstance(scopes, tuple):
            raise TypeError(
                "active_scopes debe devolver una tupla"
            )

        return TerritorialAccessProfile(
            scopes=scopes
        )
