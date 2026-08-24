import pytest

from heyti.delivery.contracts import (
    DELIVERY_STATUS_DELIVERED,
    DELIVERY_STATUS_FAILED,
    DELIVERY_STATUS_REJECTED,
    DeliveryEnvelope,
    DeliveryError,
    DeliveryResult,
)
from heyti.delivery.errors import DeliveryValidationError
from heyti.delivery.validator import DeliveryContractValidator
from heyti.materialization.contracts import HeytiResponseContract


def build_response(
    response_id: str = "RESP-001",
) -> HeytiResponseContract:
    return HeytiResponseContract(
        response_id=response_id,
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success",
    )


def test_valid_delivery_envelope_passes():
    response = build_response()

    envelope = DeliveryEnvelope(
        delivery_id="DEL-001",
        response_id=response.response_id,
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
        response=response,
    )

    validated = DeliveryContractValidator().validate_envelope(
        envelope
    )

    assert validated is envelope


@pytest.mark.parametrize(
    "field_name",
    [
        "delivery_id",
        "response_id",
        "consumer_id",
        "adapter_id",
    ],
)
def test_missing_required_envelope_field_is_rejected(field_name):
    values = {
        "delivery_id": "DEL-001",
        "response_id": "RESP-001",
        "consumer_id": "TEST_CONSUMER",
        "adapter_id": "IN_MEMORY",
    }
    values[field_name] = ""

    envelope = DeliveryEnvelope(**values)

    with pytest.raises(DeliveryValidationError):
        DeliveryContractValidator().validate_envelope(envelope)


def test_envelope_response_identity_mismatch_is_rejected():
    response = build_response("RESP-001")

    envelope = DeliveryEnvelope(
        delivery_id="DEL-001",
        response_id="RESP-999",
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
        response=response,
    )

    with pytest.raises(DeliveryValidationError):
        DeliveryContractValidator().validate_envelope(envelope)


def test_valid_delivered_result_passes():
    result = DeliveryResult(
        delivery_id="DEL-001",
        response_id="RESP-001",
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
        status=DELIVERY_STATUS_DELIVERED,
    )

    validated = DeliveryContractValidator().validate_result(result)

    assert validated is result


def test_unknown_delivery_status_is_rejected():
    result = DeliveryResult(
        delivery_id="DEL-001",
        response_id="RESP-001",
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
        status="UNKNOWN",
    )

    with pytest.raises(DeliveryValidationError):
        DeliveryContractValidator().validate_result(result)


def test_delivered_result_rejects_fatal_error():
    result = DeliveryResult(
        delivery_id="DEL-001",
        response_id="RESP-001",
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
        status=DELIVERY_STATUS_DELIVERED,
        error=DeliveryError(
            code="TEST_ERROR",
            message="Error de prueba",
        ),
    )

    with pytest.raises(DeliveryValidationError):
        DeliveryContractValidator().validate_result(result)


@pytest.mark.parametrize(
    "status",
    [
        DELIVERY_STATUS_FAILED,
        DELIVERY_STATUS_REJECTED,
    ],
)
def test_non_success_terminal_status_requires_error(status):
    result = DeliveryResult(
        delivery_id="DEL-001",
        response_id="RESP-001",
        consumer_id="TEST_CONSUMER",
        adapter_id="IN_MEMORY",
        status=status,
    )

    with pytest.raises(DeliveryValidationError):
        DeliveryContractValidator().validate_result(result)