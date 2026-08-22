import pytest

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
from heyti.materialization.validator import (
    ResponseContractValidator,
)


def test_valid_success_response_passes_validation():
    response = HeytiResponseContract(
        response_id="RESP-TEST-001",
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success",
    )

    validator = ResponseContractValidator()

    assert validator.validate(response) is response


def test_invalid_contract_name_is_rejected():
    response = HeytiResponseContract(
        response_id="RESP-TEST-001",
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
        response_id="RESP-TEST-001",
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
        response_id="RESP-TEST-001",
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
        response_id="RESP-TEST-001",
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
        response_id="RESP-TEST-001",
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
        response_id="RESP-TEST-001",
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
        response_id="RESP-TEST-001",
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
        response_id="RESP-TEST-001",
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




def test_block_without_type_is_rejected():
    response = HeytiResponseContract(
        response_id="RESP-TEST-001",
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success",
        blocks=[
            ResponseBlock(
                type="",
                role="section_identity",
                content={"section_id": "1234"},
            )
        ],
    )

    with pytest.raises(MaterializationValidationError):
        ResponseContractValidator().validate(response)


def test_block_without_role_is_rejected():
    response = HeytiResponseContract(
        response_id="RESP-TEST-001",
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success",
        blocks=[
            ResponseBlock(
                type="text",
                role="",
                content={"section_id": "1234"},
            )
        ],
    )

    with pytest.raises(MaterializationValidationError):
        ResponseContractValidator().validate(response)


def test_non_response_block_is_rejected():
    response = HeytiResponseContract(
        response_id="RESP-TEST-001",
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success",
        blocks=["invalid"],
    )

    with pytest.raises(MaterializationValidationError):
        ResponseContractValidator().validate(response)


def test_warning_without_code_is_rejected():
    response = HeytiResponseContract(
        response_id="RESP-TEST-001",
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success_with_warnings",
        warnings=[
            ResponseWarning(
                code="",
                message="Warning",
            )
        ],
    )

    with pytest.raises(MaterializationValidationError):
        ResponseContractValidator().validate(response)


def test_warning_without_message_is_rejected():
    response = HeytiResponseContract(
        response_id="RESP-TEST-001",
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success_with_warnings",
        warnings=[
            ResponseWarning(
                code="TEST_WARNING",
                message="",
            )
        ],
    )

    with pytest.raises(MaterializationValidationError):
        ResponseContractValidator().validate(response)


def test_error_without_code_is_rejected():
    response = HeytiResponseContract(
        response_id="RESP-TEST-001",
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="error",
        errors=[
            ResponseError(
                code="",
                message="Error",
            )
        ],
    )

    with pytest.raises(MaterializationValidationError):
        ResponseContractValidator().validate(response)


def test_error_without_message_is_rejected():
    response = HeytiResponseContract(
        response_id="RESP-TEST-001",
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="error",
        errors=[
            ResponseError(
                code="TEST_ERROR",
                message="",
            )
        ],
    )

    with pytest.raises(MaterializationValidationError):
        ResponseContractValidator().validate(response)

def test_json_serializable_content_is_accepted():
    response = HeytiResponseContract(
        response_id="RESP-TEST-001",
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success",
        blocks=[
            ResponseBlock(
                type="domain",
                role="electoral",
                content={
                    "votes": 0,
                    "competitive": False,
                    "name": None,
                    "items": [1, 2, 3],
                },
            )
        ],
    )

    assert ResponseContractValidator().validate(response) is response


def test_non_json_serializable_block_content_is_rejected():
    class NonSerializable:
        pass

    response = HeytiResponseContract(
        response_id="RESP-TEST-001",
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success",
        blocks=[
            ResponseBlock(
                type="domain",
                role="electoral",
                content=NonSerializable(),
            )
        ],
    )

    with pytest.raises(MaterializationValidationError):
        ResponseContractValidator().validate(response)


def test_non_json_serializable_traceability_is_rejected():
    response = HeytiResponseContract(
        response_id="RESP-TEST-001",
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success",
    )

    object.__setattr__(
        response.trace,
        "request_id",
        object(),
    )

    with pytest.raises(MaterializationValidationError):
        ResponseContractValidator().validate(response)

def test_missing_response_id_is_rejected():
    response = HeytiResponseContract(
        response_id="",
        contract="HEYTI_RESPONSE",
        version="1.0",
        capability_id="describe_section",
        status="success",
    )

    with pytest.raises(MaterializationValidationError):
        ResponseContractValidator().validate(response)