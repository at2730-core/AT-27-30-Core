import copy
import unittest
from types import SimpleNamespace
from unittest.mock import Mock
from heyti.capabilities.describe_universe.implementation import UniverseSource


def fixture():
    source = UniverseSource.__new__(UniverseSource)
    source.provenance = {'electoral_validation': 'AUDIT_PENDING'}
    source.members = {'228': {}}
    source.truth = SimpleNamespace(get_section_truth=Mock(return_value=SimpleNamespace(content={'publication_status': 'ALLOWED'})))
    source.geometry = SimpleNamespace(get_section_territorial=Mock(return_value={'geometry': {}}))
    c = {'data_status': 'INCOMPLETE', 'total_votes': 0, 'nominal_list': 100, 'votes_by_tracked_party': {'PAN': 0, 'PRI': None, 'PVEM': 0, 'MORENA': 0}}
    years = [{'election_year': y, 'contests': {cid: copy.deepcopy(c) for cid in ('A','DL','DF','G','S','P')}} for y in (2018,2021,2024)]
    data = {'section_id': '228', **years[-1], 'historical_elections': years[:2]}
    source.electoral = SimpleNamespace(get_section_electoral=Mock(return_value=data))
    return source, data


class SectionDemoTests(unittest.TestCase):
    def query(self, source, **extra):
        return source.query({'operation': 'section-demo', 'section_id': '228', **extra})

    def test_explicit_demo_preserves_zero_null_and_source(self):
        source, data = fixture()
        before = copy.deepcopy(data)
        result = self.query(source)
        self.assertEqual(result['source_mode'], 'DEMO_MASTER')
        self.assertEqual(result['modality'], 'UNSPECIFIED_IN_MASTER')
        self.assertEqual(result['provenance']['electoral_validation'], 'AUDIT_PENDING')
        self.assertEqual([y['year'] for y in result['years']], [2018,2021,2024])
        c = result['years'][2]['contests']['A']
        self.assertEqual(c['total'], 0)
        self.assertIsNone(c['votes']['PRI'])
        self.assertEqual(data, before)

    def test_territorial_block_never_reads_electoral(self):
        source, _ = fixture()
        source.truth.get_section_truth.return_value.content['publication_status'] = 'BLOCKED'
        self.assertEqual(self.query(source)['years'], [])
        source.electoral.get_section_electoral.assert_not_called()
        source.geometry.get_section_territorial.assert_not_called()

    def test_unknown_section_never_reads_sources(self):
        source, _ = fixture()
        self.assertEqual(self.query(source, section_id='999')['status'], 'TERRITORIAL_BLOCKED')
        source.truth.get_section_truth.assert_not_called()
        source.electoral.get_section_electoral.assert_not_called()

    def test_geometry_and_electoral_absence_no_numbers(self):
        for missing in ('geometry','electoral'):
            with self.subTest(missing=missing):
                source, _ = fixture()
                getattr(getattr(source, missing), 'get_section_territorial' if missing=='geometry' else 'get_section_electoral').return_value = None
                self.assertEqual(self.query(source)['years'], [])

    def test_identity_and_year_duplicates_rejected(self):
        for kind in ('identity','duplicate'):
            with self.subTest(kind=kind):
                source, data = fixture()
                if kind=='identity': data['section_id']='229'
                else: data['historical_elections'].append(copy.deepcopy(data['historical_elections'][0]))
                with self.assertRaises(ValueError): self.query(source)

    def test_invalid_ids_and_electoral_overrides_rejected(self):
        for extra in ({'section_id':0},{'section_id':'0'},{'section_id':'0228'},{'modality':'RP'},{'year':2024},{'release_id':'anything'}):
            source, _ = fixture()
            with self.subTest(extra=extra), self.assertRaises(ValueError): self.query(source, **extra)
            source.electoral.get_section_electoral.assert_not_called()

class SectionDemoHttpTests(unittest.TestCase):
    def test_real_http_route_keeps_explicit_demo_envelope(self):
        import json
        from threading import Thread
        from urllib.request import Request, urlopen
        from heyti.gateway.gateway import HeytiGateway
        from heyti.gateway.http_application import HeytiHttpApplication
        from heyti.gateway.http_server import create_http_server
        source, _ = fixture()
        class KernelBoundary:
            def execute(self, **kwargs):
                return source.query(kwargs['payload'])
        app = HeytiHttpApplication(HeytiGateway(KernelBoundary()), 'SYNTHETIC-DEMO')
        server = create_http_server(app, port=0)
        worker = Thread(target=server.serve_forever, daemon=True)
        worker.start()
        try:
            request = Request('http://127.0.0.1:%s/v1/universes/describe' % server.server_port,
                              data=json.dumps({'operation':'section-demo','section_id':'228'}).encode(),
                              headers={'Content-Type':'application/json'})
            with urlopen(request, timeout=10) as response:
                data = json.load(response)
                self.assertEqual(response.headers['Cache-Control'], 'no-store')
                self.assertEqual(data['view'], 'SECTION_DEMO')
                self.assertEqual(data['section_id'], '228')
                self.assertEqual(data['status'], 'DEMO_AVAILABLE')
        finally:
            server.shutdown(); server.server_close(); worker.join(timeout=5)
