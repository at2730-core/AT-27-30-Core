"""DB-API adapter for SEC v0.1 + CAS v0.2, owning a fresh read-only session.

No driver import, connection string, DDL, ETL or implicit release selection.
Connection factories must return dedicated idle connections with tuple rows.
"""

from dataclasses import dataclass
import json
from typing import Any, Callable, Iterable

from heyti.capabilities.describe_section.versioned_electoral_source import (
    ReadRequest, ReleaseRegistry,
)


@dataclass(frozen=True)
class StagingCutBinding:
    audit_release_id: str
    db_cut_label: str
    evidence_ref: str

    def __post_init__(self) -> None:
        if not all(isinstance(v, str) and v.strip() for v in (
            self.audit_release_id, self.db_cut_label, self.evidence_ref,
        )):
            raise ValueError("Explicit staging cut binding and evidence required")


class StagingReadError(RuntimeError):
    """Failure is explicit; it cannot silently fall back to the legacy master."""


RESOLVE_SQL = """
SELECT sr.release_id, es.series_id, sec.member_id, cas.member_id,
       sr.cut_label, sr.certification_status, es.selection_status
FROM electoral_stage.source_release sr
JOIN electoral_stage.source_member sec ON sec.release_id = sr.release_id
JOIN electoral_stage.election_series es ON es.member_id = sec.member_id
JOIN electoral_stage.series_cas_member link
  ON link.series_id = es.series_id AND link.release_id = sr.release_id
 AND link.section_member_id = sec.member_id
JOIN electoral_stage.source_member cas
  ON cas.member_id = link.cas_member_id AND cas.release_id = sr.release_id
WHERE sr.outer_zip_sha256 = %s AND sr.cut_label = %s
  AND sec.member_path = %s AND sec.member_sha256 = %s
  AND cas.member_path = %s AND cas.member_sha256 = %s
  AND es.election_year = %s AND es.election_type = %s AND es.modality = %s
  AND es.geography = 'GTO' AND es.aggregation_level = 'SECTION'
  AND es.judicial_cut = 'SOURCE_AS_PUBLISHED'
"""


SNAPSHOT_SQL = """
SELECT jsonb_build_object(
 'identity', jsonb_build_object(
   'year', es.election_year, 'type', es.election_type, 'modality', es.modality,
   'unit_kind', u.unit_kind, 'unit_key', u.unit_key, 'section_literal', u.section_code,
   'state_code', u.state_code, 'district_federal_code', u.district_federal_code,
   'district_local_code', u.district_local_code, 'municipality_code', u.municipality_code,
   'original_identity', u.original_identity, 'territorial_status', u.territorial_status,
   'genealogy_status', u.genealogy_status, 'current_section_fk', u.territorial_section_id),
 'result', jsonb_build_object(
   'total_votes', t.total_votes, 'total_raw', t.total_raw,
   'total_status', t.total_truth_status, 'total_missing_cause', t.total_cause,
   'nominal_list', t.nominal_list, 'nominal_raw', t.nominal_raw,
   'nominal_status', t.nominal_truth_status, 'nominal_missing_cause', t.nominal_cause,
   'options', COALESCE((
     SELECT jsonb_agg(jsonb_build_object(
       'raw_column', o.literal_header, 'ordinal', o.column_ordinal,
       'option_kind', o.option_type, 'votes', v.votes, 'raw_value', v.raw_value,
       'truth_status', v.truth_status, 'missing_cause', v.missing_cause)
       ORDER BY o.column_ordinal)
     FROM electoral_stage.option_vote v
     JOIN electoral_stage.option_column o ON o.option_id=v.option_id AND o.series_id=v.series_id
     WHERE v.series_id=t.series_id AND v.tally_id=t.tally_id), '[]'::jsonb)),
 'sec_source', jsonb_build_object('member_id', t.member_id,
   'source_line', rr.source_line, 'raw_row_id', rr.raw_row_id,
   'raw_line_sha256', rr.raw_line_sha256, 'raw_cells', rr.raw_cells),
 'cas_evidence', COALESCE((
   SELECT jsonb_agg(jsonb_build_object(
     'member_id', c.cas_member_id, 'source_line', cr.source_line,
     'raw_row_id', cr.raw_row_id, 'raw_line_sha256', cr.raw_line_sha256,
     'raw_cells', cr.raw_cells, 'casilla_key', c.casilla_key,
     'original_identity', c.original_identity, 'total_votes', c.total_votes,
     'total_raw', c.total_raw, 'nominal_list', c.nominal_list, 'nominal_raw', c.nominal_raw,
     'ESTATUS_ACTA', c.estatus_acta, 'TRIBUNAL', c.tribunal, 'JUICIO', c.juicio,
     'OBSERVACIONES', c.observaciones, 'RUTA_ACTA', c.ruta_acta,
     'acta_file_verification', 'NOT_VERIFIED_BY_READER',
     'options', COALESCE((
       SELECT jsonb_agg(jsonb_build_object(
         'raw_column', co.literal_header, 'ordinal', co.column_ordinal,
         'option_kind', co.option_type, 'votes', cv.votes,
         'raw_value', cv.raw_value, 'missing_cause', cv.missing_cause)
         ORDER BY co.column_ordinal)
       FROM electoral_stage.casilla_option_vote cv
       JOIN electoral_stage.option_column co ON co.option_id=cv.option_id AND co.series_id=cv.series_id
       WHERE cv.series_id=c.series_id AND cv.casilla_id=c.casilla_id), '[]'::jsonb))
     ORDER BY c.cas_member_id, cr.source_line)
   FROM electoral_stage.casilla_tally c
   JOIN electoral_stage.raw_row cr ON cr.raw_row_id=c.raw_row_id AND cr.member_id=c.cas_member_id
   WHERE c.series_id=u.series_id AND c.unit_id=u.unit_id), '[]'::jsonb),
 'issues', COALESCE((
   SELECT jsonb_agg(jsonb_build_object(
     'issue_id', i.issue_id, 'run_id', i.run_id, 'code', i.issue_code,
     'field_name', i.field_name, 'expected_value', i.expected_value,
     'observed_value', i.observed_value, 'evidence', i.evidence,
     'resolution_status', i.resolution_status) ORDER BY i.issue_id)
   FROM electoral_stage.reconciliation_issue i
   JOIN electoral_stage.audit_run ar ON ar.run_id=i.run_id
   WHERE ar.release_id=sm.release_id AND i.resolution_status <> 'RESOLVED'
     AND (i.series_id IS NULL OR i.series_id=u.series_id)
     AND (i.unit_id IS NULL OR i.unit_id=u.unit_id)), '[]'::jsonb),
 'coverage', jsonb_build_object(
   'status', 'SOURCE_ROWS_ONLY_NOT_CERTIFIED',
   'expected_option_columns', (SELECT count(*) FROM electoral_stage.option_column oc
                              WHERE oc.series_id=u.series_id),
   'loaded_option_cells', (SELECT count(*) FROM electoral_stage.option_vote ov
                          WHERE ov.series_id=t.series_id AND ov.tally_id=t.tally_id),
   'cas_rows', (SELECT count(*) FROM electoral_stage.casilla_tally ct
                WHERE ct.series_id=u.series_id AND ct.unit_id=u.unit_id)))
FROM electoral_stage.computation_unit u
JOIN electoral_stage.election_series es ON es.series_id=u.series_id
JOIN electoral_stage.section_tally t ON t.series_id=u.series_id AND t.unit_id=u.unit_id
JOIN electoral_stage.source_member sm ON sm.member_id=t.member_id
JOIN electoral_stage.raw_row rr ON rr.member_id=t.member_id AND rr.raw_row_id=t.raw_row_id
WHERE u.series_id=%s AND u.unit_kind=%s AND u.unit_key=%s
"""


class StagingElectoralRepository:
    def __init__(self, registry: ReleaseRegistry, connection_factory: Callable[[], Any],
                 bindings: Iterable[StagingCutBinding]) -> None:
        self.registry = registry
        self.connection_factory = connection_factory
        self.bindings = {}
        for binding in bindings:
            if binding.audit_release_id in self.bindings:
                raise ValueError("Duplicate staging binding")
            self.bindings[binding.audit_release_id] = binding

    def get_snapshot(self, release_id: str, request: ReadRequest) -> dict[str, Any] | None:
        release = self.registry.get(release_id)
        binding = self.bindings.get(release_id)
        if release is None or release.series != request.series:
            raise StagingReadError("RELEASE_IDENTITY_MISMATCH")
        if binding is None:
            raise StagingReadError("NO_STAGING_CUT_BINDING")
        connection = self.connection_factory()
        cursor = None
        try:
            cursor = connection.cursor()
            cursor.execute("BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY")
            cursor.execute(RESOLVE_SQL, (
                release.zip_sha256, binding.db_cut_label, release.section_member,
                release.section_sha256, release.casilla_member, release.casilla_sha256,
                release.series.year, release.series.election_type, release.series.modality,
            ))
            matches = cursor.fetchall()
            if len(matches) != 1:
                raise StagingReadError("STAGING_RELEASE_NOT_UNIQUE_OR_ABSENT")
            db_release, series_id, sec_member, cas_member, cut, cert, selection = matches[0]
            cursor.execute(SNAPSHOT_SQL, (series_id, request.unit_kind, request.unit_key))
            rows = cursor.fetchall()
            if not rows:
                return None
            if len(rows) != 1:
                raise StagingReadError("AMBIGUOUS_UNIT")
            snapshot = rows[0][0]
            if isinstance(snapshot, str):
                snapshot = json.loads(snapshot)
            if not isinstance(snapshot, dict):
                raise StagingReadError("INVALID_SNAPSHOT_PAYLOAD")
            snapshot["provenance"] = release.provenance()
            snapshot["staging_binding"] = {
                "db_release_id": db_release, "series_id": series_id,
                "section_member_id": sec_member, "cas_member_id": cas_member,
                "db_cut_label": cut, "binding_evidence": binding.evidence_ref,
                "db_certification_status": cert, "db_selection_status": selection,
            }
            # Preserve DB confidence separately; never upgrade it from the matrix.
            if cert.startswith("BLOCKED") or cert == "REJECTED":
                snapshot["issues"].append({"code": "STAGING_RELEASE_BLOCKED", "status": cert})
            coverage = snapshot["coverage"]
            if coverage["expected_option_columns"] != coverage["loaded_option_cells"]:
                snapshot["issues"].append({"code": "INCOMPLETE_OPTION_COVERAGE"})
            return snapshot
        finally:
            try:
                connection.rollback()
            finally:
                try:
                    if cursor is not None:
                        cursor.close()
                finally:
                    connection.close()
