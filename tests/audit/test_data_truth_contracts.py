from dataclasses import FrozenInstanceError

import pytest

from heyti.audit.data_truth.contracts import (
    AUDIT_STATUS_BLOCKED,
    AUDIT_STATUS_PASSED,
    DATA_TRUTH_CONTRACT,
    DATA_TRUTH_CONTRACT_VERSION,
    PUBLICATION_ALLOWED,
    PUBLICATION_BLOCKED,
    SEVERITY_CRITICAL,
    SEVERITY_INFO,
    TRUTH_OBSERVED,
    TRUTH_UNRESOLVED,
    DataTruthAuditResult,
    DataTruthEvidence,
    DataTruthFinding,
)


def test_evidence_preserves_source_identity_and_hash():
    evidence = DataTruthEvidence(
        source_id="electoral-master",
        description="Maestro electoral integrado",
        sha256="ABC123",
        metadata={
            "path": "datasets/electoral/master.json",
        },
    )

    data = evidence.to_dict()

    assert data["source_id"] == "electoral-master"
    assert data["sha256"] == "ABC123"
    assert data["metadata"]["path"].endswith(
        "master.json"
    )


def test_finding_defaults_to_unresolved_and_blocked():
    finding = DataTruthFinding(
        code="UNRESOLVED_SOURCE",
        message="La procedencia no está certificada",
        severity=SEVERITY_CRITICAL,
        entity_type="SECTION",
        entity_id="9042",
    )

    assert finding.truth_status == TRUTH_UNRESOLVED
    assert finding.publication_status == PUBLICATION_BLOCKED


def test_observed_finding_can_allow_publication():
    finding = DataTruthFinding(
        code="OBSERVED_SECTION",
        message="Sección observada en fuente certificada",
        severity=SEVERITY_INFO,
        entity_type="SECTION",
        entity_id="2788",
        truth_status=TRUTH_OBSERVED,
        publication_status=PUBLICATION_ALLOWED,
    )

    assert finding.truth_status == TRUTH_OBSERVED
    assert finding.publication_status == PUBLICATION_ALLOWED


def test_finding_serializes_nested_evidence():
    evidence = DataTruthEvidence(
        source_id="geojson-current",
        description="Geometría territorial vigente",
    )

    finding = DataTruthFinding(
        code="MISSING_CURRENT_GEOMETRY",
        message="La sección no tiene geometría vigente",
        severity=SEVERITY_CRITICAL,
        entity_type="SECTION",
        entity_id="343",
        evidence=(evidence,),
    )

    data = finding.to_dict()

    assert data["evidence"][0]["source_id"] == "geojson-current"


def test_audit_result_uses_contract_version_one():
    result = DataTruthAuditResult(
        audit_id="AUDIT-001",
        status=AUDIT_STATUS_PASSED,
    )

    assert result.contract == DATA_TRUTH_CONTRACT
    assert result.version == DATA_TRUTH_CONTRACT_VERSION


def test_blocking_findings_returns_only_blocked_items():
    allowed = DataTruthFinding(
        code="CURRENT_SECTION",
        message="Sección territorial vigente",
        severity=SEVERITY_INFO,
        entity_type="SECTION",
        entity_id="1",
        truth_status=TRUTH_OBSERVED,
        publication_status=PUBLICATION_ALLOWED,
    )

    blocked = DataTruthFinding(
        code="ORPHAN_SOURCE_ROW",
        message="Fila sin identidad territorial",
        severity=SEVERITY_CRITICAL,
        entity_type="SECTION",
        entity_id="9042",
    )

    result = DataTruthAuditResult(
        audit_id="AUDIT-002",
        status=AUDIT_STATUS_BLOCKED,
        findings=(allowed, blocked),
    )

    assert result.blocking_findings == (blocked,)


def test_audit_result_serializes_findings_and_metadata():
    finding = DataTruthFinding(
        code="STRICT_JSON_FAILURE",
        message="La fuente contiene NaN no válido",
        severity=SEVERITY_CRITICAL,
        entity_type="DATASET",
        entity_id="electoral-master",
    )

    result = DataTruthAuditResult(
        audit_id="AUDIT-003",
        status=AUDIT_STATUS_BLOCKED,
        findings=(finding,),
        metadata={
            "records": 3310,
            "nan_literals": 15869,
        },
    )

    data = result.to_dict()

    assert data["findings"][0]["code"] == "STRICT_JSON_FAILURE"
    assert data["metadata"]["records"] == 3310
    assert data["metadata"]["nan_literals"] == 15869


def test_contract_objects_are_immutable():
    result = DataTruthAuditResult(
        audit_id="AUDIT-004",
        status=AUDIT_STATUS_PASSED,
    )

    with pytest.raises(FrozenInstanceError):
        result.status = AUDIT_STATUS_BLOCKED
