"""Synthetic integration cases, never electoral certification."""
from copy import deepcopy
from dataclasses import replace
import unittest

from test_versioned_electoral_source import fixture, Repository
from heyti.capabilities.describe_section.electoral_query import parse_electoral_query
from heyti.capabilities.describe_section.implementation import DescribeSectionCapability
from heyti.capabilities.describe_section.models import SectionTruthSnapshot
from heyti.capabilities.describe_section.provider import DescribeSectionProvider
from heyti.capabilities.describe_section.versioned_electoral_source import (
    VersionedElectoralSource, ReleaseRegistry,
)
from heyti.materialization.describe_section.materializer import DescribeSectionMaterializer
from heyti.materialization.context import MaterializationContext


class Truth:
    def __init__(self, status="ALLOWED"):
        self.status = status

    def get_section_truth(self, section_id):
        return SectionTruthSnapshot({"publication_status": self.status})


class Legacy:
    def __init__(self):
        self.calls = 0

    def get_section_electoral(self, section_id):
        self.calls += 1
        return {"legacy": "synthetic"}


class DescribeSectionVersionedTests(unittest.TestCase):
    def setUp(self):
        release, self.request, self.decision, self.snapshot = fixture()
        self.request = replace(self.request, unit_kind="ORDINARY_SECTION", unit_key="SEC:1080")
        self.decision = replace(self.decision, unit_kind="ORDINARY_SECTION", unit_key="SEC:1080")
        self.snapshot["identity"].update(unit_kind="ORDINARY_SECTION", unit_key="SEC:1080")
        self.registry = ReleaseRegistry([release])
        self.repo = Repository(self.snapshot)
        self.legacy = Legacy()
        self.query = {"year": 2021, "type": "DL", "modality": "RP",
                      "policy_id": "synthetic-v1"}

    def provider(self, selected=False, truth="ALLOWED"):
        source = VersionedElectoralSource(
            self.registry, self.repo, [self.decision] if selected else [],
        )
        return DescribeSectionProvider(
            truth_source=Truth(truth), electoral_source=self.legacy,
            versioned_electoral_source=source,
        )

    def execute(self, provider, query=None):
        return DescribeSectionCapability(provider).execute(payload={
            "section_id": "1080", "electoral_query": query or self.query,
        })

    def test_legacy_request_preserved_without_query(self):
        result = DescribeSectionCapability(self.provider()).execute(section_id="1080")
        self.assertEqual(result.electoral, {"legacy": "synthetic"})
        self.assertIsNone(result.electoral_versioned)
        self.assertEqual(self.legacy.calls, 1)

    def test_unselected_query_never_falls_back_to_legacy(self):
        result = self.execute(self.provider())
        self.assertEqual(result.electoral_versioned["status"], "NO_RELEASE_SELECTED")
        self.assertIsNone(result.electoral)
        self.assertEqual(self.legacy.calls, 0)
        self.assertEqual(self.repo.calls, 0)

    def test_selected_query_preserves_literal_result_and_provenance(self):
        result = self.execute(self.provider(True))
        response = result.electoral_versioned
        self.assertEqual(response["status"], "SELECTED_RESULT")
        self.assertIsNone(response["data"]["result"]["total_votes"])
        self.assertEqual(response["data"]["result"]["nominal_list"], 0)
        self.assertEqual(response["data"]["provenance"], self.snapshot["provenance"])
        response["data"]["result"]["options"].clear()
        self.assertEqual(len(self.snapshot["result"]["options"]), 2)

    def test_data_truth_denial_prevents_repository_read(self):
        result = self.execute(self.provider(True, "BLOCKED"))
        self.assertEqual(result.electoral_versioned["status"], "DATA_TRUTH_NOT_ALLOWED")
        self.assertIsNone(result.electoral_versioned["data"])
        self.assertEqual(self.repo.calls, 0)

    def test_missing_truth_prevents_repository_read(self):
        result = self.execute(DescribeSectionProvider())
        self.assertEqual(result.electoral_versioned["status"], "DATA_TRUTH_NOT_ALLOWED")

    def test_missing_versioned_source_is_explicit(self):
        provider = DescribeSectionProvider(truth_source=Truth(), electoral_source=self.legacy)
        result = self.execute(provider)
        self.assertEqual(result.electoral_versioned["status"], "VERSIONED_SOURCE_NOT_CONFIGURED")
        self.assertEqual(self.legacy.calls, 0)

    def test_audit_payload_and_implicit_modality_rejected(self):
        for query in ({**self.query, "purpose": "AUDIT"},
                      {"year": 2021, "type": "DL"}, {**self.query, "unit_key": "SEC:0"}):
            with self.subTest(query=query), self.assertRaises(ValueError):
                self.execute(self.provider(), query)

    def test_direct_audit_and_other_unit_rejected(self):
        for request in (replace(self.request, purpose="AUDIT"),
                        replace(self.request, unit_key="SEC:1"),
                        replace(self.request, unit_kind="SPECIAL_AGGREGATE")):
            with self.subTest(request=request), self.assertRaises(ValueError):
                self.provider().get_section("1080", request)

    def test_sec0_and_bad_section_rejected(self):
        for section in ("0", 0, True, "1.5", "SEC:1080", "-1"):
            with self.subTest(section=section), self.assertRaises(ValueError):
                parse_electoral_query(section, self.query)

    def test_leading_zero_section_canonicalized_in_request(self):
        self.assertEqual(parse_electoral_query("01080", self.query).unit_key, "SEC:1080")

    def test_materializer_keeps_blocked_state_in_metadata_without_votes(self):
        result = self.execute(self.provider())
        response = DescribeSectionMaterializer().materialize(result, MaterializationContext("describe_section"))
        blocks = [b for b in response.blocks if b.role == "electoral_versioned"]
        self.assertEqual(len(blocks), 1)
        self.assertEqual(blocks[0].type, "metadata")
        self.assertIsNone(blocks[0].content["data"])
        self.assertEqual(response.status, "success_with_warnings")

    def test_materializer_preserves_selected_envelope(self):
        result = self.execute(self.provider(True))
        expected = deepcopy(result.electoral_versioned)
        response = DescribeSectionMaterializer().materialize(result, MaterializationContext("describe_section"))
        block = next(b for b in response.blocks if b.role == "electoral_versioned")
        self.assertEqual(block.type, "domain")
        self.assertEqual(block.content, expected)
        result.electoral_versioned["data"].clear()
        self.assertEqual(block.content, expected)

    def test_uncertified_payload_cannot_enter_capability(self):
        class BadSource:
            def read(self, request):
                return {"status": "AUDIT_SOURCE_AS_PUBLISHED", "purpose": "PRESENTATION",
                        "metric_scope": "RESULT", "data": {"votes": 999}}
        provider = DescribeSectionProvider(truth_source=Truth(), versioned_electoral_source=BadSource())
        with self.assertRaises(ValueError):
            self.execute(provider)

    def test_nominal_scope_does_not_publish_votes(self):
        decision = replace(self.decision, metric_scope="NOMINAL_LIST")
        source = VersionedElectoralSource(self.registry, self.repo, [decision])
        provider = DescribeSectionProvider(truth_source=Truth(), versioned_electoral_source=source)
        result = self.execute(provider, {**self.query, "metric_scope": "NOMINAL_LIST"})
        self.assertNotIn("options", result.electoral_versioned["data"]["result"])
        self.assertNotIn("cas_evidence", result.electoral_versioned["data"])


if __name__ == "__main__":
    unittest.main()
