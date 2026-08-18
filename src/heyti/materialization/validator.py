from heyti.materialization.contracts import (
    HeytiResponseContract,
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

    No crea ni corrige contenido.
    Únicamente comprueba que el contrato candidato satisface
    las reglas mínimas definidas para la versión soportada.
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

        return response