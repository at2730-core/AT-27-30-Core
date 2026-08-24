class DeliveryException(Exception):
    """
    Error base de Runtime Response Delivery.
    """


class DeliveryValidationError(DeliveryException):
    """
    El candidato de Delivery no satisface las reglas contractuales.
    """


class UnsupportedDeliveryContractVersionError(DeliveryException):
    """
    La versión contractual de Delivery no está soportada.
    """