import pytest

from heyti.capabilities.describe_section.implementation import (
    DescribeSectionCapability,
)
from heyti.events.event_bus import EventBus
from heyti.materialization.describe_section.materializer import (
    DescribeSectionMaterializer,
)

from heyti.registry.registry import CapabilityRegistry
from heyti.runtime.capability_runtime import CapabilityRuntime
from heyti.session.session_manager import SessionManager

from heyti.materialization.base import Materializer
from heyti.materialization.context import MaterializationContext
from heyti.materialization.contracts import (
    HeytiResponseContract,
)
from heyti.materialization.errors import (
    MaterializationError,
    MaterializationValidationError,
    UnsupportedContractVersionError,
    UnsupportedMaterializationError,
)
from heyti.materialization.validator import (
    ResponseContractValidator,
)
from heyti.materialization.registry import (
    MaterializationRegistry,
)


class CountingDescribeSectionCapability(
    DescribeSectionCapability
):
    """
    DescribeSection instrumentada para demostrar que Runtime
    la ejecuta exactamente una vez.
    """

    def __init__(self) -> None:
        super().__init__()
        self.execution_count = 0

    def execute(
        self,
        session=None,
        payload=None,
        section_id=None,
    ):
        self.execution_count += 1

        return super().execute(
            session=session,
            payload=payload,
            section_id=section_id,
        )


def build_runtime(capability):
    registry = CapabilityRegistry()
    sessions = SessionManager()
    events = EventBus()

    sessions.create(
        "SESSION-001",
        object(),
    )

    registry.register(
        "describe_section",
        capability,
    )

    runtime = CapabilityRuntime(
        registry=registry,
        session_manager=sessions,
        event_bus=events,
    )

    return runtime, events

def build_runtime_with_materialization_registry(capability):
    registry = CapabilityRegistry()
    sessions = SessionManager()
    events = EventBus()
    materialization_registry = MaterializationRegistry()

    sessions.create(
        "SESSION-001",
        object(),
    )

    registry.register(
        "describe_section",
        capability,
    )

    materialization_registry.register(
        capability_id="describe_section",
        contract_version="1.0",
        materializer=DescribeSectionMaterializer(),
    )

    runtime = CapabilityRuntime(
        registry=registry,
        session_manager=sessions,
        event_bus=events,
        materialization_registry=materialization_registry,
    )

    return runtime, events

def test_runtime_materializes_describe_section():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    response = runtime.execute_materialized(
        capability_name="describe_section",
        session_id="SESSION-001",
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
    )

    assert response.contract == "HEYTI_RESPONSE"
    assert response.version == "1.0"
    assert response.capability_id == "describe_section"
    assert response.status == "success"

    section_block = next(
        block
        for block in response.blocks
        if block.role == "section_identity"
    )

    assert section_block.content == {
        "section_id": "1234"
    }


def test_runtime_executes_capability_once_when_materializing():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    runtime.execute_materialized(
        capability_name="describe_section",
        session_id="SESSION-001",
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
    )

    assert capability.execution_count == 1


def test_runtime_materialization_preserves_session_trace():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    response = runtime.execute_materialized(
        capability_name="describe_section",
        session_id="SESSION-001",
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
    )

    assert response.trace.session_id == "SESSION-001"


def test_runtime_materialization_preserves_optional_traceability():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    response = runtime.execute_materialized(
        capability_name="describe_section",
        session_id="SESSION-001",
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
        request_id="REQ-001",
        execution_id="EXE-001",
        knowledge_version="K-001",
    )

    assert response.trace.request_id == "REQ-001"
    assert response.trace.execution_id == "EXE-001"
    assert response.trace.knowledge_version == "K-001"


def test_runtime_materialization_keeps_capability_event():
    capability = CountingDescribeSectionCapability()
    runtime, events = build_runtime(capability)

    published_events = []

    events.subscribe(
        "capability_executed",
        published_events.append,
    )

    runtime.execute_materialized(
        capability_name="describe_section",
        session_id="SESSION-001",
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
    )

    assert len(published_events) == 1
    assert (
        published_events[0]["capability_name"]
        == "describe_section"
    )
    assert (
        published_events[0]["session_id"]
        == "SESSION-001"
    )


def test_runtime_does_not_fallback_to_raw_result():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    with pytest.raises(
        UnsupportedContractVersionError
    ):
        runtime.execute_materialized(
            capability_name="describe_section",
            session_id="SESSION-001",
            payload={
                "section_id": "1234",
            },
            materializer=DescribeSectionMaterializer(),
            contract_version="2.0",
        )

    assert capability.execution_count == 1


def test_legacy_execute_still_returns_cognitive_result():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    result = runtime.execute(
        capability_name="describe_section",
        session_id="SESSION-001",
        payload={
            "section_id": "1234",
        },
    )

    assert result.section_id == "1234"
    assert capability.execution_count == 1


class FailingMaterializer(Materializer):
    def materialize(
        self,
        cognitive_result,
        context: MaterializationContext,
    ):
        raise MaterializationError(
            "materialization failure"
        )


class InvalidContractMaterializer(Materializer):
    def materialize(
        self,
        cognitive_result,
        context: MaterializationContext,
    ):
        return HeytiResponseContract(
            response_id="RESP-INVALID-001",
            contract="HEYTI_RESPONSE",
            version="1.0",
            capability_id=context.capability_id,
            status="invalid_status",
        )


def test_runtime_propagates_materialization_failure():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    with pytest.raises(MaterializationError):
        runtime.execute_materialized(
            capability_name="describe_section",
            session_id="SESSION-001",
            payload={
                "section_id": "1234",
            },
            materializer=FailingMaterializer(),
        )

    assert capability.execution_count == 1


def test_runtime_does_not_return_raw_result_on_materialization_failure():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    with pytest.raises(MaterializationError):
        result = runtime.execute_materialized(
            capability_name="describe_section",
            session_id="SESSION-001",
            payload={
                "section_id": "1234",
            },
            materializer=FailingMaterializer(),
        )

        assert result is None

    assert capability.execution_count == 1


def test_runtime_propagates_validation_failure():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    with pytest.raises(MaterializationValidationError):
        runtime.execute_materialized(
            capability_name="describe_section",
            session_id="SESSION-001",
            payload={
                "section_id": "1234",
            },
            materializer=InvalidContractMaterializer(),
            validator=ResponseContractValidator(),
        )

    assert capability.execution_count == 1


def test_runtime_publishes_capability_event_before_materialization_failure():
    capability = CountingDescribeSectionCapability()
    runtime, events = build_runtime(capability)

    published_events = []

    events.subscribe(
        "capability_executed",
        published_events.append,
    )

    with pytest.raises(MaterializationError):
        runtime.execute_materialized(
            capability_name="describe_section",
            session_id="SESSION-001",
            payload={
                "section_id": "1234",
            },
            materializer=FailingMaterializer(),
        )

    assert len(published_events) == 1
    assert (
        published_events[0]["capability_name"]
        == "describe_section"
    )


def test_runtime_publishes_capability_event_before_validation_failure():
    capability = CountingDescribeSectionCapability()
    runtime, events = build_runtime(capability)

    published_events = []

    events.subscribe(
        "capability_executed",
        published_events.append,
    )

    with pytest.raises(MaterializationValidationError):
        runtime.execute_materialized(
            capability_name="describe_section",
            session_id="SESSION-001",
            payload={
                "section_id": "1234",
            },
            materializer=InvalidContractMaterializer(),
        )

    assert len(published_events) == 1

def test_runtime_resolves_materializer_from_registry():
    capability = CountingDescribeSectionCapability()

    runtime, _ = (
        build_runtime_with_materialization_registry(
            capability
        )
    )

    response = runtime.execute_materialized(
        capability_name="describe_section",
        session_id="SESSION-001",
        payload={
            "section_id": "1234",
        },
    )

    assert response.contract == "HEYTI_RESPONSE"
    assert response.version == "1.0"
    assert response.capability_id == "describe_section"
    assert capability.execution_count == 1


def test_explicit_materializer_remains_supported():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    response = runtime.execute_materialized(
        capability_name="describe_section",
        session_id="SESSION-001",
        payload={
            "section_id": "1234",
        },
        materializer=DescribeSectionMaterializer(),
    )

    assert response.status == "success"
    assert capability.execution_count == 1


def test_runtime_requires_materializer_or_registry():
    capability = CountingDescribeSectionCapability()
    runtime, _ = build_runtime(capability)

    with pytest.raises(
        UnsupportedMaterializationError
    ):
        runtime.execute_materialized(
            capability_name="describe_section",
            session_id="SESSION-001",
            payload={
                "section_id": "1234",
            },
        )

    assert capability.execution_count == 0


def test_unknown_registry_version_does_not_execute_capability():
    capability = CountingDescribeSectionCapability()

    runtime, _ = (
        build_runtime_with_materialization_registry(
            capability
        )
    )

    with pytest.raises(
        UnsupportedContractVersionError
    ):
        runtime.execute_materialized(
            capability_name="describe_section",
            session_id="SESSION-001",
            payload={
                "section_id": "1234",
            },
            contract_version="2.0",
        )

    assert capability.execution_count == 0
