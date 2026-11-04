"""Synthetic HTTP integration: does not certify data or access PostgreSQL."""
import json
import unittest
from pathlib import Path
from threading import Thread
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from heyti.capabilities.describe_section.presentation_electoral_source import build_unselected_electoral_source
from heyti.capabilities.describe_section.implementation import DescribeSectionCapability
from heyti.capabilities.describe_section.provider import DescribeSectionProvider
from heyti.capabilities.describe_section.models import SectionTruthSnapshot
from heyti.gateway.gateway import HeytiGateway
from heyti.gateway.http_application import HeytiHttpApplication
from heyti.gateway.http_server import create_http_server
from heyti.materialization.context import MaterializationContext
from heyti.materialization.describe_section.materializer import DescribeSectionMaterializer

ROOT = Path(__file__).resolve().parents[2]
MATRIX = ROOT / "docs/auditoria/HEYTI_Matriz_Seleccion_Cortes_23_Series_v0_1.csv"
SERIES = [("A","UNICA"),("G","UNICA"),("P","UNICA"),("DL","MR"),("DL","RP"),("DF","MR"),("DF","RP"),("S","MR"),("S","RP")]

class Truth:
    def get_section_truth(self, section_id):
        return SectionTruthSnapshot({"publication_status":"ALLOWED"})

class Legacy:
    def get_section_electoral(self, section_id):
        raise AssertionError("Legacy source accessed by versioned query")

class KernelBoundary:
    # Real capability and materializer; synthetic kernel boundary for HTTP tests.
    def __init__(self, source):
        self.calls = []
        self.capability = DescribeSectionCapability(DescribeSectionProvider(
            truth_source=Truth(), electoral_source=Legacy(), versioned_electoral_source=source))
    def execute_materialized(self, **kwargs):
        self.calls.append(kwargs["payload"])
        result = self.capability.execute(payload=kwargs["payload"])
        return DescribeSectionMaterializer().materialize(result, MaterializationContext("describe_section"))

class HttpPresentation2024Tests(unittest.TestCase):
    def setUp(self):
        self.db_calls = 0
        def forbidden_connection():
            self.db_calls += 1
            raise AssertionError("Unselected presentation touched database")
        self.source = build_unselected_electoral_source(MATRIX, forbidden_connection)
        self.kernel = KernelBoundary(self.source)
        self.application = HeytiHttpApplication(HeytiGateway(self.kernel),"SYNTHETIC-SESSION")
        self.server = create_http_server(self.application,port=0)
        self.thread = Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()
    def tearDown(self):
        self.server.shutdown(); self.server.server_close(); self.thread.join()
    def post(self,payload):
        request = Request("http://127.0.0.1:%s/v1/sections/describe" % self.server.server_port,
            data=json.dumps(payload).encode(),headers={"Content-Type":"application/json"})
        with urlopen(request,timeout=10) as response:
            return json.load(response)
    def test_all_nine_series_through_http_without_fallback(self):
        for typ,mode in SERIES:
            with self.subTest(series=(typ,mode)):
                query={"year":2024,"type":typ,"modality":mode}
                response=self.post({"section_id":"1080","electoral_query":query})
                self.assertEqual(self.kernel.calls[-1]["electoral_query"],query)
                blocks=response["blocks"]
                self.assertFalse(any(b["role"]=="electoral" for b in blocks))
                envelope=next(b["content"] for b in blocks if b["role"]=="electoral_versioned")
                self.assertEqual(envelope["status"],"NO_RELEASE_SELECTED")
                self.assertIsNone(envelope["data"])
        self.assertEqual(self.db_calls,0)
    def test_invalid_query_never_reaches_kernel(self):
        for query in (None,[],{}, {"year":2024,"type":"DL","modality":"UNICA"},
                      {"year":2024,"type":"A","modality":"UNICA","purpose":"AUDIT"}):
            with self.subTest(query=query), self.assertRaises(HTTPError) as caught:
                self.post({"section_id":"1080","electoral_query":query})
            self.assertEqual(caught.exception.code,400)
        self.assertEqual(self.kernel.calls,[])
        self.assertEqual(self.db_calls,0)
    def test_explicit_query_is_copied(self):
        query={"year":2024,"type":"A","modality":"UNICA"}
        self.application.describe_section("1080",electoral_query=query)
        query["year"]=2015
        self.assertEqual(self.kernel.calls[-1]["electoral_query"]["year"],2024)

if __name__ == "__main__": unittest.main()
