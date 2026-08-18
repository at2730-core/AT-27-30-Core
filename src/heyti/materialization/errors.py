class MaterializationError(Exception):
    """
    Error base de la capa de Materialization.
    """


class UnsupportedMaterializationError(MaterializationError):
    """
    El resultado o capability no posee una materialización soportada.
    """


class MaterializationValidationError(MaterializationError):
    """
    El contrato candidato no satisface las reglas de validación.
    """


class UnsupportedContractVersionError(MaterializationError):
    """
    La versión contractual solicitada no está soportada.
    """