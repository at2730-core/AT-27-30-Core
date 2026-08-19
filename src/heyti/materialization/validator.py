import json

from heyti.materialization.contracts import (
    HeytiResponseContract,
    ResponseBlock,
    ResponseError,
    ResponseWarning,
)
from heyti.materialization.errors import (
    MaterializationValidationError,
    UnsupportedContractVersionError,
)


SUPPORTED_CONTRACT = "HEYTI_RESPONSE"
SUPPORTED_CONTRACT_VERSION = "1.0"

SUPPORTED_STATUSES = {
    "success",
    "success_with_warnings",
    "partial",
    "error",
}


class ResponseContractValidator:
    """
    Valida la estructura contractual base de una respuesta HEYTI.

    No crea, corrige ni completa contenido.
    Sólo verifica que el candidato satisfaga las reglas
    de la versión contractual soportada.
    """

    def validate(
        self,
        response: HeytiResponseContract,
    ) -> HeytiResponseContract:
        if not isinstance(response, HeytiResponseContract):
            raise MaterializationValidationError(
                "La respuesta no es un HeytiResponseContract"
            )

        if response.contract != SUPPORTED_CONTRACT:
            raise MaterializationValidationError(
                f"Contrato no soportado: {response.contract}"
            )

        if response.version != SUPPORTED_CONTRACT_VERSION:
            raise UnsupportedContractVersionError(
                f"Versión contractual no soportada: "
                f"{response.version}"
            )

        if not response.capability_id:
            raise MaterializationValidationError(
                "capability_id es obligatorio"
            )

        if response.status not in SUPPORTED_STATUSES:
            raise MaterializationValidationError(
                f"Status no soportado: {response.status}"
            )

        self._validate_blocks(response.blocks)
        self._validate_warnings(response.warnings)
        self._validate_errors(response.errors)
        self._validate_status_consistency(response)
        self._validate_json_serializable(response)

        return response

    def _validate_blocks(
        self,
        blocks: list[ResponseBlock],
    ) -> None:
        if not isinstance(blocks, list):
            raise MaterializationValidationError(
                "blocks debe ser una lista"
            )

        for block in blocks:
            if not isinstance(block, ResponseBlock):
                raise MaterializationValidationError(
                    "Todos los blocks deben ser ResponseBlock"
                )

            if not block.type:
                raise MaterializationValidationError(
                    "ResponseBlock.type es obligatorio"
                )

            if not block.role:
                raise MaterializationValidationError(
                    "ResponseBlock.role es obligatorio"
                )

    def _validate_warnings(
        self,
        warnings: list[ResponseWarning],
    ) -> None:
        if not isinstance(warnings, list):
            raise MaterializationValidationError(
                "warnings debe ser una lista"
            )

        for warning in warnings:
            if not isinstance(warning, ResponseWarning):
                raise MaterializationValidationError(
                    "Todos los warnings deben ser ResponseWarning"
                )

            if not warning.code:
                raise MaterializationValidationError(
                    "ResponseWarning.code es obligatorio"
                )

            if not warning.message:
                raise MaterializationValidationError(
                    "ResponseWarning.message es obligatorio"
                )

    def _validate_errors(
        self,
        errors: list[ResponseError],
    ) -> None:
        if not isinstance(errors, list):
            raise MaterializationValidationError(
                "errors debe ser una lista"
            )

        for error in errors:
            if not isinstance(error, ResponseError):
                raise MaterializationValidationError(
                    "Todos los errors deben ser ResponseError"
                )

            if not error.code:
                raise MaterializationValidationError(
                    "ResponseError.code es obligatorio"
                )

            if not error.message:
                raise MaterializationValidationError(
                    "ResponseError.message es obligatorio"
                )

    def _validate_status_consistency(
        self,
        response: HeytiResponseContract,
    ) -> None:
        if response.status == "error" and not response.errors:
            raise MaterializationValidationError(
                "Una respuesta con status='error' "
                "debe contener al menos un error"
            )

        if response.status == "success" and response.errors:
            raise MaterializationValidationError(
                "Una respuesta con status='success' "
                "no puede contener errores"
            )

        if (
            response.status == "success_with_warnings"
            and not response.warnings
        ):
            raise MaterializationValidationError(
                "Una respuesta con status='success_with_warnings' "
                "debe contener al menos una advertencia"
            )

    def _validate_json_serializable(
        self,
        response: HeytiResponseContract,
    ) -> None:
        try:
            json.dumps(response.to_dict())
        except (TypeError, ValueError) as exc:
            raise MaterializationValidationError(
                "El Response Contract contiene valores "
                "no serializables a JSON"
            ) from exc
