from unittest.mock import Mock

from heyti.gateway.gateway import HeytiGateway


def test_gateway_delegates_execute_to_kernel():
    kernel = Mock()
    kernel.execute.return_value = "kernel-result"

    gateway = HeytiGateway(kernel)

    result = gateway.execute(
        capability_name="describe_section",
        session_id="SESSION-001",
        payload={"section_id": "1234"},
    )

    kernel.execute.assert_called_once_with(
        capability_name="describe_section",
        session_id="SESSION-001",
        payload={"section_id": "1234"},
    )

    assert result == "kernel-result"


def test_gateway_does_not_start_kernel_during_execute():
    kernel = Mock()

    gateway = HeytiGateway(kernel)

    gateway.execute(
        capability_name="describe_section",
        session_id="SESSION-001",
    )

    kernel.start.assert_not_called()

def test_gateway_delegates_materialized_execution_to_kernel():
    kernel = Mock()
    kernel.execute_materialized.return_value = "materialized-result"

    gateway = HeytiGateway(kernel)

    result = gateway.execute_materialized(
        capability_name="describe_section",
        session_id="SESSION-001",
        payload={"section_id": "1234"},
        contract_version="1.0",
        request_id="REQ-001",
        execution_id="EXE-001",
        knowledge_version="K-001",
    )

    kernel.execute_materialized.assert_called_once_with(
        capability_name="describe_section",
        session_id="SESSION-001",
        materializer=None,
        payload={"section_id": "1234"},
        contract_version="1.0",
        request_id="REQ-001",
        execution_id="EXE-001",
        knowledge_version="K-001",
        validator=None,
    )

    assert result == "materialized-result"


def test_gateway_materialized_execution_does_not_start_kernel():
    kernel = Mock()

    gateway = HeytiGateway(kernel)

    gateway.execute_materialized(
        capability_name="describe_section",
        session_id="SESSION-001",
    )

    kernel.start.assert_not_called()

def test_gateway_delegates_delivered_execution_to_kernel():
    kernel = Mock()
    kernel.execute_delivered.return_value = "delivery-result"

    gateway = HeytiGateway(kernel)

    result = gateway.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="PORTAL",
        adapter_id="IN_MEMORY",
        payload={"section_id": "1234"},
        contract_version="1.0",
        request_id="REQ-001",
        execution_id="EXE-001",
        knowledge_version="K-001",
    )

    kernel.execute_delivered.assert_called_once_with(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="PORTAL",
        adapter=None,
        adapter_id="IN_MEMORY",
        materializer=None,
        payload={"section_id": "1234"},
        contract_version="1.0",
        request_id="REQ-001",
        execution_id="EXE-001",
        knowledge_version="K-001",
        validator=None,
        delivery_service=None,
    )

    assert result == "delivery-result"


def test_gateway_delivered_execution_does_not_start_kernel():
    kernel = Mock()

    gateway = HeytiGateway(kernel)

    gateway.execute_delivered(
        capability_name="describe_section",
        session_id="SESSION-001",
        consumer_id="PORTAL",
        adapter_id="IN_MEMORY",
    )

    kernel.start.assert_not_called()