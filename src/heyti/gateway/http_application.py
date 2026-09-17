from typing import Any

from heyti.gateway.gateway import HeytiGateway
from heyti.materialization.contracts import (
    HeytiResponseContract,
)


class HeytiHttpApplication:
    """
    Frontera de aplicación para el transporte HTTP de HEYTI.

    Traduce operaciones HTTP previstas hacia el Gateway oficial.
    No abre sockets, no construye el Runtime y no accede a fuentes.
    """

    def __init__(
        self,
        gateway: HeytiGateway,
        session_id: str,
    ) -> None:
        if not isinstance(gateway, HeytiGateway):
            raise TypeError(
                "gateway debe ser una instancia de HeytiGateway"
            )

        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError(
                "session_id debe ser una cadena no vacía"
            )

        self._gateway = gateway
        self._session_id = session_id.strip()

    @property
    def gateway(self) -> HeytiGateway:
        """Devuelve el Gateway asociado."""

        return self._gateway

    @property
    def session_id(self) -> str:
        """Devuelve el identificador de sesión del transporte."""

        return self._session_id

    def health(self) -> dict[str, Any]:
        """
        Ejecuta la capability oficial de salud mediante el Gateway.
        """

        result = self._gateway.execute(
            capability_name="health",
            session_id=self._session_id,
        )

        if not isinstance(result, dict):
            raise TypeError(
                "La capability health debe devolver un diccionario"
            )

        return dict(result)

    def describe_section(
        self,
        section_id: str,
        request_id: str | None = None,
        execution_id: str | None = None,
        knowledge_version: str | None = None,
    ) -> dict[str, Any]:
        """
        Ejecuta y materializa DescribeSection mediante el Gateway.
        """

        if not isinstance(section_id, str) or not section_id.strip():
            raise ValueError(
                "section_id debe ser una cadena no vacía"
            )

        response = self._gateway.execute_materialized(
            capability_name="describe_section",
            session_id=self._session_id,
            payload={
                "section_id": section_id.strip(),
            },
            request_id=request_id,
            execution_id=execution_id,
            knowledge_version=knowledge_version,
        )

        if not isinstance(response, HeytiResponseContract):
            raise TypeError(
                "DescribeSection debe devolver "
                "HeytiResponseContract"
            )

        return response.to_dict()
