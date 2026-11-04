"""DB-API boundary tests with synthetic rows, not a PostgreSQL integration trial."""

from copy import deepcopy
from dataclasses import replace
import json
import unittest

from test_versioned_electoral_source import fixture
from heyti.capabilities.describe_section.versioned_electoral_source import (
    ReleaseRegistry, VersionedElectoralSource,
)
from heyti.capabilities.describe_section.staging_electoral_repository import (
    RESOLVE_SQL, SNAPSHOT_SQL, StagingCutBinding, StagingElectoralRepository, StagingReadError,
)


class Cursor:
    def __init__(self, matches, snapshots, fail=False):
        self.matches, self.snapshots, self.fail = matches, snapshots, fail
        self.executed = []
        self.closed = False

    def execute(self, sql, params=None):
        self.executed.append((sql, params))
        if self.fail and sql == SNAPSHOT_SQL:
            raise RuntimeError("synthetic database failure")

    def fetchall(self):
        return self.matches if self.executed[-1][0] == RESOLVE_SQL else self.snapshots

    def close(self):
        self.closed = True


class Connection:
    def __init__(self, cursor):
        self._cursor, self.rolled_back, self.closed = cursor, False, False

    def cursor(self):
        return self._cursor

    def rollback(self):
        self.rolled_back = True

    def close(self):
        self.closed = True


class StagingRepositoryTests(unittest.TestCase):
    def setUp(self):
        self.release, self.request, self.decision, self.snapshot = fixture()
        self.snapshot["coverage"].update(expected_option_columns=2, loaded_option_cells=2, cas_rows=1)
        self.registry = ReleaseRegistry([self.release])
        self.cursor = Cursor([(10, 20, 30, 40, "SOURCE_AS_PUBLISHED", "UNREVIEWED", "UNREVIEWED")],
                             [(deepcopy(self.snapshot),)])
        self.connection = Connection(self.cursor)
        self.calls = 0

    def factory(self):
        self.calls += 1
        return self.connection

    def repository(self, bindings=None):
        if bindings is None:
            bindings = [StagingCutBinding("synthetic", "SOURCE_AS_PUBLISHED", "synthetic-binding-evidence")]
        return StagingElectoralRepository(self.registry, self.factory, bindings)

    def test_read_only_transaction_and_cleanup(self):
        snapshot = self.repository().get_snapshot("synthetic", self.request)
        self.assertEqual(self.cursor.executed[0],
                         ("BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ READ ONLY", None))
        self.assertTrue(self.connection.rolled_back)
        self.assertTrue(self.connection.closed)
        self.assertTrue(self.cursor.closed)
        self.assertEqual(snapshot["provenance"], self.release.provenance())
        self.assertEqual(snapshot["staging_binding"]["db_release_id"], 10)
        self.assertEqual(snapshot["staging_binding"]["db_cut_label"], "SOURCE_AS_PUBLISHED")
        self.assertIsNone(snapshot["result"]["total_votes"])
        self.assertEqual(snapshot["cas_evidence"][0]["ESTATUS_ACTA"], "ANULADA")

    def test_parameters_bind_hashes_members_series_and_unit_without_interpolation(self):
        malicious_key = "SEC:1'; DELETE FROM electoral_stage.raw_row; --"
        self.repository().get_snapshot("synthetic", replace(self.request, unit_key=malicious_key))
        self.assertEqual(self.cursor.executed[1][1], (
            "a" * 64, "SOURCE_AS_PUBLISHED", "sec.csv", "b" * 64,
            "cas.csv", "c" * 64, 2021, "DL", "RP",
        ))
        self.assertEqual(self.cursor.executed[2][1], (20, "SECTION", malicious_key))
        self.assertNotIn(malicious_key, self.cursor.executed[2][0])

    def test_unbound_release_never_connects(self):
        with self.assertRaisesRegex(StagingReadError, "NO_STAGING_CUT_BINDING"):
            self.repository([]).get_snapshot("synthetic", self.request)
        self.assertEqual(self.calls, 0)

    def test_wrong_series_never_connects(self):
        from heyti.capabilities.describe_section.versioned_electoral_source import SeriesKey
        with self.assertRaisesRegex(StagingReadError, "RELEASE_IDENTITY_MISMATCH"):
            self.repository().get_snapshot("synthetic", replace(self.request, series=SeriesKey(2021, "DL", "MR")))
        self.assertEqual(self.calls, 0)

    def test_absent_or_ambiguous_release_fail_with_cleanup(self):
        for matches in ([], self.cursor.matches * 2):
            with self.subTest(matches=matches):
                self.cursor.matches = matches
                with self.assertRaisesRegex(StagingReadError, "STAGING_RELEASE_NOT_UNIQUE_OR_ABSENT"):
                    self.repository().get_snapshot("synthetic", self.request)
                self.assertTrue(self.connection.closed)
                self.assertTrue(self.connection.rolled_back)

    def test_missing_unit_does_not_return_zero(self):
        self.cursor.snapshots = []
        self.assertIsNone(self.repository().get_snapshot("synthetic", self.request))
        self.assertTrue(self.connection.closed)

    def test_duplicate_unit_fails_instead_of_picking_first(self):
        self.cursor.snapshots *= 2
        with self.assertRaisesRegex(StagingReadError, "AMBIGUOUS_UNIT"):
            self.repository().get_snapshot("synthetic", self.request)

    def test_query_failure_rolls_back_and_closes(self):
        self.cursor.fail = True
        with self.assertRaisesRegex(RuntimeError, "synthetic database failure"):
            self.repository().get_snapshot("synthetic", self.request)
        self.assertTrue(self.connection.closed)
        self.assertTrue(self.connection.rolled_back)
        self.assertTrue(self.cursor.closed)

    def test_json_text_driver_payload(self):
        self.cursor.snapshots = [(json.dumps(self.snapshot),)]
        snapshot = self.repository().get_snapshot("synthetic", self.request)
        self.assertIsNone(snapshot["result"]["total_votes"])

    def test_db_block_remains_visible_and_blocks_reader(self):
        self.cursor.matches = [(10, 20, 30, 40, "SOURCE_AS_PUBLISHED", "BLOCKED_JUDICIAL_CUT_CONFLICT", "UNREVIEWED")]
        source = VersionedElectoralSource(self.registry, self.repository(), [self.decision])
        self.assertEqual(source.read(self.request)["status"], "OPEN_UNIT_ISSUES")

    def test_incomplete_option_coverage_is_not_certified(self):
        self.cursor.snapshots[0][0]["coverage"]["loaded_option_cells"] = 1
        source = VersionedElectoralSource(self.registry, self.repository(), [self.decision])
        self.assertEqual(source.read(self.request)["status"], "OPEN_UNIT_ISSUES")

    def test_without_presentation_selection_reader_never_connects(self):
        source = VersionedElectoralSource(self.registry, self.repository())
        self.assertEqual(source.read(self.request)["status"], "NO_RELEASE_SELECTED")
        self.assertEqual(self.calls, 0)

    def test_invalid_and_duplicate_bindings_rejected(self):
        with self.assertRaises(ValueError):
            StagingCutBinding("synthetic", "SOURCE_AS_PUBLISHED", "")
        binding = StagingCutBinding("synthetic", "SOURCE_AS_PUBLISHED", "evidence")
        with self.assertRaises(ValueError):
            self.repository([binding, binding])


if __name__ == "__main__":
    unittest.main()
