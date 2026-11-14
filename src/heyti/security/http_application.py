from typing import Any

from heyti.security.authentication import (
    AuthenticationStatus,
)
from heyti.security.sessions import (
    AuthenticatedSession,
)


class InvalidCredentialsError(Exception):
    pass


class PasswordChangeRequiredError(Exception):
    pass


class AuthenticatedSessionRequiredError(Exception):
    pass


from dataclasses import replace

from heyti.security.contracts import (
    AuthorizationResource,
    DecisionReason,
    PermissionScope,
    PrivacyProjection,
)


class SecurityHttpApplication:
    def __init__(
        self,
        authentication_service,
        session_service,
        authorization_service=None,
        password_change_service=None,
        scope_profile_service=None,
    ):
        if not callable(
            getattr(
                authentication_service,
                "authenticate",
                None,
            )
        ):
            raise TypeError(
                "authentication_service incompatible"
            )

        for method in (
            "create_session",
            "resolve",
            "revoke",
        ):
            if not callable(
                getattr(
                    session_service,
                    method,
                    None,
                )
            ):
                raise TypeError(
                    "session_service incompatible"
                )

        self._authentication_service = (
            authentication_service
        )
        self._session_service = session_service

        if (
            authorization_service is not None
            and not callable(
                getattr(
                    authorization_service,
                    "authorize",
                    None,
                )
            )
        ):
            raise TypeError(
                "authorization_service incompatible"
            )

        self._authorization_service = (
            authorization_service
        )

        if (
            password_change_service is not None
            and not callable(
                getattr(
                    password_change_service,
                    "change_password",
                    None,
                )
            )
        ):
            raise TypeError(
                "password_change_service incompatible"
            )

        self._password_change_service = (
            password_change_service
        )

        if (
            scope_profile_service is not None
            and not callable(
                getattr(
                    scope_profile_service,
                    "profile",
                    None,
                )
            )
        ):
            raise TypeError(
                "scope_profile_service incompatible"
            )

        self._scope_profile_service = (
            scope_profile_service
        )

    def login(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError(
                "La solicitud de acceso debe ser un objeto"
            )

        username = payload.get("username")
        password = payload.get("password")

        if not isinstance(username, str):
            raise ValueError(
                "username debe ser una cadena"
            )

        if not username.strip():
            raise ValueError(
                "username no puede estar vacio"
            )

        if not isinstance(password, str):
            raise ValueError(
                "password debe ser una cadena"
            )

        if not password:
            raise ValueError(
                "password no puede estar vacio"
            )

        result = (
            self._authentication_service
            .authenticate(
                username.strip(),
                password,
            )
        )

        if result.status is (
            AuthenticationStatus
            .PASSWORD_CHANGE_REQUIRED
        ):
            raise PasswordChangeRequiredError(
                "Debe cambiarse la contrase?a"
            )

        if result.status is not (
            AuthenticationStatus.AUTHENTICATED
        ):
            raise InvalidCredentialsError(
                "Credenciales inv?lidas"
            )

        session = (
            self._session_service
            .create_session(result)
        )

        return self._session_payload(session)

    def change_password(
        self,
        payload: dict[str, Any],
    ) -> dict[str, Any]:
        if self._password_change_service is None:
            raise RuntimeError(
                "El cambio de contrasena no esta configurado"
            )

        if not isinstance(payload, dict):
            raise ValueError(
                "La solicitud debe ser un objeto"
            )

        result = (
            self._password_change_service
            .change_password(
                username=payload.get("username"),
                current_password=payload.get(
                    "current_password"
                ),
                new_password=payload.get(
                    "new_password"
                ),
                confirmation=payload.get(
                    "confirmation"
                ),
            )
        )

        return {
            "status": "PASSWORD_CHANGED",
            "user": {
                "user_id": result.user_id,
                "username": result.username,
                "display_name": result.display_name,
            },
        }

    def current_session(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        session = self._session_service.resolve(
            session_id
        )

        if session is None:
            raise AuthenticatedSessionRequiredError(
                "Se requiere una sesi?n autenticada"
            )

        return self._session_payload(session)

    def authorize_field_operation(
        self,
        *,
        user_id: int,
        session_id: str,
        payload: dict[str, Any],
    ):
        if self._authorization_service is None:
            raise RuntimeError(
                "La autorizacion no esta configurada"
            )

        if not isinstance(payload, dict):
            raise ValueError(
                "La consulta de Campo debe ser un objeto"
            )

        operation = payload.get("operation")

        permission_by_operation = {
            "summary": "FIELD_SUMMARY_READ",
            "map": "FIELD_MAP_READ",
        }

        permission_code = (
            permission_by_operation.get(operation)
        )

        if permission_code is None:
            raise ValueError(
                "Operacion de Campo no soportada"
            )

        section_code = None

        if operation == "map":
            raw_section_code = payload.get(
                "section_code"
            )

            if raw_section_code is not None:
                section_code = str(
                    raw_section_code
                ).strip()

                if not section_code:
                    raise ValueError(
                        "section_code no puede estar vacio"
                    )

        decision = (
            self._authorization_service.authorize(
                user_id=user_id,
                session_id=session_id,
                permission_code=permission_code,
                resource=AuthorizationResource(
                    resource_type=(
                        f"FIELD_{operation.upper()}"
                    ),
                    resource_ref=operation,
                    section_code=section_code,
                ),
            )
        )

        if (
            operation == "map"
            and section_code is None
            and decision.allowed
            and decision.scope
            is not PermissionScope.GLOBAL
        ):
            return replace(
                decision,
                allowed=False,
                reason=(
                    DecisionReason
                    .RESOURCE_OUTSIDE_SCOPE
                ),
                audit_required=True,
                privacy_projection=(
                    PrivacyProjection.REDACTED
                ),
            )

        return decision

    def authorize_section_operation(
        self,
        *,
        user_id: int,
        session_id: str,
        section_code: str,
    ):
        if self._authorization_service is None:
            raise RuntimeError(
                "La autorizacion no esta configurada"
            )

        if not isinstance(section_code, str):
            raise ValueError(
                "section_code debe ser una cadena"
            )

        normalized_section_code = (
            section_code.strip()
        )

        if (
            not normalized_section_code
            or not normalized_section_code.isdigit()
            or int(normalized_section_code) <= 0
        ):
            raise ValueError(
                "section_code debe ser positivo"
            )

        return self._authorization_service.authorize(
            user_id=user_id,
            session_id=session_id,
            permission_code="SECTION_READ",
            resource=AuthorizationResource(
                resource_type="SECTION",
                resource_ref=normalized_section_code,
                section_code=normalized_section_code,
            ),
        )

    def authorize_universe_operation(
        self,
        *,
        user_id: int,
        session_id: str,
        payload: dict[str, Any],
    ):
        if self._authorization_service is None:
            raise RuntimeError(
                "La autorizacion no esta configurada"
            )

        if not isinstance(payload, dict):
            raise ValueError(
                "La consulta de universo debe ser un objeto"
            )

        operation = payload.get("operation")

        if operation == "catalog":
            return self._authorization_service.authorize(
                user_id=user_id,
                session_id=session_id,
                permission_code=(
                    "UNIVERSE_CATALOG_READ"
                ),
                resource=AuthorizationResource(
                    resource_type="UNIVERSE_CATALOG",
                    resource_ref="catalog",
                ),
            )

        if operation == "section-demo":
            return self.authorize_section_operation(
                user_id=user_id,
                session_id=session_id,
                section_code=payload.get("section_id"),
            )

        if operation != "map":
            raise ValueError(
                "Operacion de universo no soportada"
            )

        level = payload.get("level")
        universe_id = payload.get("id")

        supported_levels = {
            "state",
            "municipality",
            "federal-district",
            "local-district",
        }

        if level not in supported_levels:
            raise ValueError(
                "Nivel de universo no soportado"
            )

        if not isinstance(universe_id, str):
            raise ValueError(
                "id de universo debe ser una cadena"
            )

        normalized_universe_id = (
            universe_id.strip()
        )

        if (
            not normalized_universe_id
            or not normalized_universe_id.isdigit()
            or int(normalized_universe_id) <= 0
        ):
            raise ValueError(
                "id de universo debe ser positivo"
            )

        municipality_code = (
            normalized_universe_id
            if level == "municipality"
            else None
        )

        decision = self._authorization_service.authorize(
            user_id=user_id,
            session_id=session_id,
            permission_code="UNIVERSE_MAP_READ",
            resource=AuthorizationResource(
                resource_type="UNIVERSE_MAP",
                resource_ref=(
                    f"{level}:{normalized_universe_id}"
                ),
                municipality_code=municipality_code,
            ),
        )

        if (
            level != "municipality"
            and decision.allowed
            and decision.scope
            is not PermissionScope.GLOBAL
        ):
            return replace(
                decision,
                allowed=False,
                reason=(
                    DecisionReason
                    .RESOURCE_OUTSIDE_SCOPE
                ),
                audit_required=True,
                privacy_projection=(
                    PrivacyProjection.REDACTED
                ),
            )

        return decision

    def filter_universe_catalog(
        self,
        *,
        user_id: int,
        response: dict[str, Any],
    ) -> dict[str, Any]:
        if self._scope_profile_service is None:
            raise RuntimeError(
                "El perfil territorial no esta configurado"
            )

        if not isinstance(response, dict):
            raise ValueError(
                "La respuesta de catalogo debe ser un objeto"
            )

        catalog = response.get("catalog")

        if not isinstance(catalog, list):
            raise ValueError(
                "El catalogo debe ser una lista"
            )

        normalized_catalog = []

        for item in catalog:
            if not isinstance(item, dict):
                raise ValueError(
                    "El catalogo contiene un elemento invalido"
                )

            level = item.get("level")
            universe_id = item.get("id")

            if (
                not isinstance(level, str)
                or not isinstance(universe_id, str)
                or not level.strip()
                or not universe_id.strip()
            ):
                raise ValueError(
                    "El catalogo contiene una identidad invalida"
                )

            normalized_catalog.append(dict(item))

        profile = self._scope_profile_service.profile(
            user_id=user_id
        )

        if profile.global_access:
            return {
                **response,
                "catalog": normalized_catalog,
            }

        municipality_codes = {
            str(scope.municipality_code)
            for scope in profile.scopes
            if scope.municipality_code is not None
        }

        filtered_catalog = [
            item
            for item in normalized_catalog
            if (
                item["level"] == "municipality"
                and item["id"] in municipality_codes
            )
        ]

        return {
            **response,
            "catalog": filtered_catalog,
        }

    def logout(
        self,
        session_id: str,
    ) -> dict[str, Any]:
        session = self._session_service.resolve(
            session_id
        )

        if session is None:
            raise AuthenticatedSessionRequiredError(
                "Se requiere una sesi?n autenticada"
            )

        self._session_service.revoke(
            session.session_id
        )

        return {
            "status": "SIGNED_OUT",
        }

    def _session_payload(
        self,
        session: AuthenticatedSession,
    ) -> dict[str, Any]:
        payload = {
            "status": "AUTHENTICATED",
            "session_token": session.session_id,
            "expires_at": (
                session.expires_at.isoformat()
            ),
            "user": {
                "user_id": session.user_id,
                "username": session.username,
                "display_name": (
                    session.display_name
                ),
                "role": session.role.value,
            },
        }

        if self._scope_profile_service is not None:
            territorial_access = (
                self._scope_profile_service.profile(
                    session.user_id
                )
            )
            payload["territorial_access"] = (
                territorial_access.to_dict()
            )

        return payload
