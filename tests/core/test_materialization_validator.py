import pytest

from heyti.materialization.contracts import (
    HeytiResponseContract,
    ResponseError,
    ResponseWarning,
)
from heyti.materialization.errors import (
    MaterializationValidationError,
    UnsupportedContractVersionError,
)
from heyti.materialization.validator import (
    ResponseContractValidator,
)


def test_valid_success_response_passes_validation():
    response = HeytiResponseContract(
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success",
    )

    validator = ResponseContractValidator()

    assert validator.validate(response) is response


def test_invalid_contract_name_is_rejected():
    response = HeytiResponseContract(
        contract="INVALID",
        version="1.0",
        capability_id="describe_section",
        status="success",
    )

    validator = ResponseContractValidator()

    with pytest.raises(MaterializationValidationError):
        validator.validate(response)


def test_unsupported_contract_version_is_rejected():
    response = HeytiResponseContract(
        contract="HEYTI_RESPONSE",
        version="2.0",
        capability_id="describe_section",
        status="success",
    )

    validator = ResponseContractValidator()

    with pytest.raises(UnsupportedContractVersionError):
        validator.validate(response)


def test_missing_capability_id_is_rejected():
    response = HeytiResponseContract(
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="",
        status="success",
    )

    validator = ResponseContractValidator()

    with pytest.raises(MaterializationValidationError):
        validator.validate(response)


def test_invalid_status_is_rejected():
    response = HeytiResponseContract(
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="unknown",
    )

    validator = ResponseContractValidator()

    with pytest.raises(MaterializationValidationError):
        validator.validate(response)


def test_error_status_requires_error_payload():
    response = HeytiResponseContract(
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="error",
    )

    validator = ResponseContractValidator()

    with pytest.raises(MaterializationValidationError):
        validator.validate(response)


def test_success_status_rejects_errors():
    response = HeytiResponseContract(
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success",
        errors=[
            ResponseError(
                code="TEST_ERROR",
                message="Error de prueba",
            )
        ],
    )

    validator = ResponseContractValidator()

    with pytest.raises(MaterializationValidationError):
        validator.validate(response)


def test_success_with_warnings_requires_warning():
    response = HeytiResponseContract(
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success_with_warnings",
    )

    validator = ResponseContractValidator()

    with pytest.raises(MaterializationValidationError):
        validator.validate(response)


def test_success_with_warning_is_valid():
    response = HeytiResponseContract(
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success_with_warnings",
        warnings=[
            ResponseWarning(
                code="TEST_WARNING",
                message="Advertencia de prueba",
            )
        ],
    )

    validator = ResponseContractValidator()

    assert validator.validate(response) is response