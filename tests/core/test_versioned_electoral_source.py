"""Synthetic boundary fixtures; no electoral value here is an official result."""

from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import unittest

from heyti.capabilities.describe_section.versioned_electoral_source import (
    ReadRequest, Release, ReleaseRegistry, SelectionDecision, SeriesKey,
    VersionedElectoralSource,
)


MATRIX = (Path(__file__).resolve().parents[2] / "docs" / "auditoria"
          / "HEYTI_Matriz_Seleccion_Cortes_23_Series_v0_1.csv")


class Repository:
    def __init__(self, snapshot):
        self.snapshot = snapshot
        self.calls = 0

    def get_snapshot(self, release_id, request):
        self.calls += 1
        return self.snapshot


def fixture():
    series = SeriesKey(2021, "DL", "RP")
    release = Release(
        "synthetic", series, "SYNTHETIC_TEST", "fixture.zip", "a" * 64,
        "sec.csv", "b" * 64, "cas.csv", "c" * 64, "SYNTHETIC",
        "VERIFIED", "PASSED_ISOLATED", "UNDECIDED",
        "PENDING_SOURCE_ADJUDICATION", "", "2021-06-06",
    )
    request = ReadRequest(series, "SECTION", "1080", policy_id="synthetic-v1")
    decision = SelectionDecision(
        "synthetic-v1", series, "SECTION", "1080", "RESULT", "synthetic",
        "SELECTED", "CERTIFIED", ("synthetic-evidence-not-official",),
    )
    snapshot = {
        "identity": {"year": 2021, "type": "DL", "modality": "RP",
                     "unit_kind": "SECTION", "unit_key": "1080",
                     "section_literal": "1080", "territorial_status": "HISTORICAL"},
        "provenance": release.provenance(),
        "result": {
            "total_votes": None, "total_raw": "", "total_status": "MISSING",
            "total_missing_cause": "SYNTHETIC_MISSING",
            "nominal_list": 0, "nominal_raw": "0", "nominal_status": "NUMERIC",
            "nominal_missing_cause": None,
            "options": [
                {"raw_column": "SYNTHETIC_PARTY", "ordinal": 0, "option_kind": "PARTY",
                 "votes": 0, "raw_value": "0", "missing_cause": None},
                {"raw_column": "SYNTHETIC_COMBINATION", "ordinal": 1,
                 "option_kind": "COMBINATION", "votes": None, "raw_value": "",
                 "missing_cause": "SYNTHETIC_MISSING"},
            ],
        },
        "cas_evidence": [{"member_id": "cas.csv", "source_line": 2,
                          "ESTATUS_ACTA": "ANULADA", "raw_votes": {"SYNTHETIC_PARTY": 5}}],
        "issues": [], "coverage": {"status": "SYNTHETIC_ONLY"},
    }
    return release, request, decision, snapshot


class VersionedElectoralTests(unittest.TestCase):
    def setUp(self):
        self.release, self.request, self.decision, self.snapshot = fixture()
        self.repo = Repository(self.snapshot)

    def source(self, decisions=(), release=None):
        return VersionedElectoralSource(
            ReleaseRegistry([release or self.release]), self.repo, decisions,
        )

    def test_real_matrix_has_23_unselected_series(self):
        registry = ReleaseRegistry.from_matrix(MATRIX)
        self.assertEqual(len(registry.releases), 23)
        self.assertEqual(len({r.series for r in registry.releases}), 23)
        self.assertEqual(len({r.source_zip for r in registry.releases}), 15)
        source = VersionedElectoralSource(registry, self.repo)
        for release in registry.releases:
            with self.subTest(series=release.series):
                self.assertEqual(release.selection_status, "UNDECIDED")
                self.assertEqual(release.cut_date_status, "UNVERIFIED")
                response = source.read(ReadRequest(release.series, "SECTION", "1"))
                self.assertEqual(response["status"], "NO_RELEASE_SELECTED")
                self.assertIsNone(response["data"])
        self.assertEqual(self.repo.calls, 0)

    def test_explicit_release_without_policy_cannot_present(self):
        response = self.source().read(replace(self.request, release_id="synthetic"))
        self.assertEqual(response["status"], "NO_RELEASE_SELECTED")
        self.assertEqual(self.repo.calls, 0)

    def test_technical_success_cannot_certify(self):
        pending = replace(self.decision, certification_status="PENDING_SOURCE_ADJUDICATION")
        self.assertEqual(self.source([pending]).read(self.request)["status"], "NO_RELEASE_SELECTED")

    def test_selection_requires_evidence(self):
        for refs in ((), ("",), (" ",)):
            with self.subTest(refs=refs):
                decision = replace(self.decision, evidence_refs=refs)
                self.assertEqual(self.source([decision]).read(self.request)["status"], "NO_RELEASE_SELECTED")

    def test_ambiguous_policy_does_not_pick_first(self):
        source = self.source([self.decision, replace(self.decision, release_id="other")])
        self.assertEqual(source.read(self.request)["status"], "NO_RELEASE_SELECTED")

    def test_nominal_authorization_does_not_authorize_result(self):
        decision = replace(self.decision, metric_scope="NOMINAL_LIST")
        source = self.source([decision])
        self.assertEqual(source.read(self.request)["status"], "NO_RELEASE_SELECTED")
        response = source.read(replace(self.request, metric_scope="NOMINAL_LIST"))
        self.assertEqual(response["status"], "SELECTED_RESULT")
        self.assertEqual(set(response["data"]["result"]), {
            "nominal_list", "nominal_raw", "nominal_status", "nominal_missing_cause",
        })
        self.assertNotIn("cas_evidence", response["data"])

    def test_judicial_conflict_blocks_selected_release(self):
        release = replace(self.release, certification_status="BLOCKED_JUDICIAL_CUT_CONFLICT")
        response = self.source([self.decision], release).read(self.request)
        self.assertEqual(response["status"], "BLOCKED_JUDICIAL_CUT_CONFLICT")
        self.assertIsNone(response["data"])
        self.assertEqual(self.repo.calls, 0)

    def test_unverified_cut_blocks_presentation(self):
        release = replace(self.release, cut_date_status="UNVERIFIED", cut_date=None)
        response = self.source([self.decision], release).read(self.request)
        self.assertEqual(response["status"], "UNVERIFIED_CUT")
        self.assertEqual(self.repo.calls, 0)

    def test_verified_cut_needs_date(self):
        with self.assertRaises(ValueError):
            replace(self.release, cut_date=None)

    def test_audit_preserves_null_zero_raw_annulled_and_options(self):
        request = replace(self.request, purpose="AUDIT", release_id="synthetic", policy_id=None)
        before = deepcopy(self.snapshot)
        response = self.source().read(request)
        self.assertEqual(response["status"], "AUDIT_SOURCE_AS_PUBLISHED")
        self.assertEqual(response["data"], before)
        self.assertIsNone(response["data"]["result"]["total_votes"])
        self.assertEqual(response["data"]["result"]["nominal_list"], 0)
        self.assertIsNone(response["winner"])
        response["data"]["result"]["options"].clear()
        self.assertEqual(self.snapshot, before)

    def test_audit_can_inspect_blocked_source_without_certifying(self):
        release = replace(self.release, certification_status="BLOCKED_JUDICIAL_CUT_CONFLICT")
        request = replace(self.request, purpose="AUDIT", release_id="synthetic")
        response = self.source(release=release).read(request)
        self.assertEqual(response["status"], "AUDIT_SOURCE_AS_PUBLISHED")
        self.assertEqual(response["certification_status"], "BLOCKED_JUDICIAL_CUT_CONFLICT")

    def test_mr_rp_cannot_share_release(self):
        request = replace(self.request, purpose="AUDIT", release_id="synthetic",
                          series=SeriesKey(2021, "DL", "MR"))
        self.assertEqual(self.source().read(request)["status"], "RELEASE_IDENTITY_MISMATCH")

    def test_no_latest_release_fallback(self):
        request = replace(self.request, purpose="AUDIT", release_id="unknown")
        self.assertEqual(self.source().read(request)["status"], "RELEASE_IDENTITY_MISMATCH")
        self.assertEqual(self.repo.calls, 0)

    def test_selected_release_must_match_explicit_request(self):
        request = replace(self.request, release_id="other")
        self.assertEqual(self.source([self.decision]).read(request)["status"], "SELECTION_RELEASE_MISMATCH")

    def test_snapshot_identity_and_hash_are_checked(self):
        for area, key, value in (
            ("identity", "modality", "MR"), ("identity", "unit_key", "other"),
            ("provenance", "section_sha256", "d" * 64),
        ):
            with self.subTest(area=area, key=key):
                self.repo.snapshot = deepcopy(self.snapshot)
                self.repo.snapshot[area][key] = value
                self.assertEqual(self.source([self.decision]).read(self.request)["status"],
                                 "SNAPSHOT_IDENTITY_MISMATCH")

    def test_open_unit_issue_blocks_presentation_but_not_audit(self):
        self.snapshot["issues"] = [{"code": "UNRESOLVED_UNIT", "scope": "RESULT"}]
        source = self.source([self.decision])
        self.assertEqual(source.read(self.request)["status"], "OPEN_UNIT_ISSUES")
        self.assertEqual(source.read(replace(self.request, purpose="AUDIT", release_id="synthetic"))["status"],
                         "AUDIT_SOURCE_AS_PUBLISHED")

    def test_missing_unit_is_distinct_from_zero(self):
        self.repo.snapshot = None
        self.assertEqual(self.source([self.decision]).read(self.request)["status"], "UNIT_NOT_AVAILABLE")

    def test_missing_contract_fields_fail_closed(self):
        del self.snapshot["result"]["total_raw"]
        self.assertEqual(self.source([self.decision]).read(self.request)["status"],
                         "INCOMPLETE_SNAPSHOT_CONTRACT")

    def test_invalid_votes_and_unexplained_null_are_rejected(self):
        for value, cause in ((-1, None), (True, None), (1.5, None), (None, None)):
            with self.subTest(value=value):
                self.snapshot["result"]["options"][0].update(votes=value, missing_cause=cause)
                self.assertEqual(self.source([self.decision]).read(self.request)["status"],
                                 "INVALID_LITERAL_RESULT")

    def test_special_identity_is_not_coerced_to_current_section(self):
        request = replace(self.request, purpose="AUDIT", release_id="synthetic",
                          unit_kind="SPECIAL_ACTA", unit_key="SEC0:district:22:VA31")
        self.snapshot["identity"].update(unit_kind=request.unit_kind, unit_key=request.unit_key,
                                         section_literal="0", current_section_fk=None)
        data = self.source().read(request)["data"]
        self.assertEqual(data["identity"]["unit_key"], request.unit_key)
        self.assertIsNone(data["identity"]["current_section_fk"])

    def test_duplicate_release_is_rejected(self):
        with self.assertRaises(ValueError):
            ReleaseRegistry([self.release, self.release])

    def test_malformed_repository_payloads_fail_closed(self):
        for malformed in ([], {"identity": None}, {"identity": {}, "provenance": None}):
            with self.subTest(snapshot=malformed):
                self.repo.snapshot = malformed
                self.assertEqual(self.source([self.decision]).read(self.request)["status"],
                                 "INCOMPLETE_SNAPSHOT_CONTRACT")

    def test_2015_and_implicit_modality_are_rejected(self):
        for args in ((2015, "A", "UNICA"), (2024, "DF", "UNICA"), (2024, "P", "MR")):
            with self.subTest(args=args), self.assertRaises(ValueError):
                SeriesKey(*args)


if __name__ == "__main__":
    unittest.main()
