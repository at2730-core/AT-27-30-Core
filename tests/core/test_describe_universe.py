import json
import threading
import unittest
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from heyti.capabilities.describe_universe.implementation import tracked_outcome
from heyti.gateway.guanajuato_2023_http_host import build_guanajuato_2023_http_host

ROOT = Path(__file__).resolve().parents[2]

class UniverseMapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.host = build_guanajuato_2023_http_host(ROOT/'datasets/electoral/Datos_Electoral_con_2015.json', ROOT/'datasets/spatial/secciones.geojson', port=0)
        cls.thread = threading.Thread(target=cls.host.serve_forever, daemon=True)
        cls.thread.start()
        cls.url = 'http://%s:%s' % cls.host.address

    @classmethod
    def tearDownClass(cls):
        cls.host.shutdown()
        cls.thread.join(timeout=5)

    def post(self, payload, origin='http://localhost:5173'):
        req = Request(self.url+'/v1/universes/describe', data=json.dumps(payload).encode(), headers={'Content-Type':'application/json','Origin':origin})
        with urlopen(req, timeout=60) as response:
            self.assertEqual(response.headers['Cache-Control'], 'no-store')
            return json.load(response)

    def test_catalog_groups(self):
        data = self.post({'operation':'catalog'})
        self.assertEqual(data['contract'], 'HEYTI_UNIVERSE_RESPONSE')
        for level, count in [('state',1),('municipality',46),('federal-district',15),('local-district',22)]:
            group = [u for u in data['catalog'] if u['level']==level]
            self.assertEqual(len(group), count)
            self.assertEqual(sum(u['sections'] for u in group),3266)

    def test_real_state_zero_and_blocked(self):
        data = self.post({'operation':'map','level':'state','id':'11','year':2024,'contest':'A'})
        self.assertEqual(data['coverage']['geographic_sections'],3266)
        self.assertEqual(data['coverage']['represented_sections'],3230)
        self.assertEqual(data['coverage']['blocked_sections'],36)
        self.assertEqual(sum(data['counts'].values()),3230)
        ids = {s['section_id']: s for s in data['sections']}
        self.assertEqual(ids['1524']['status'],'ZERO_TOTAL')
        self.assertIsNone(ids['1524']['leader'])
        self.assertEqual(ids['1621']['leader'],'PAN')
        self.assertNotIn('3300',ids)
        self.assertEqual(data['provenance']['electoral_validation'],'AUDIT_PENDING')

    def test_missing_and_not_contested(self):
        payload = {'operation':'map','level':'municipality','id':'20','year':2021,'contest':'DF'}
        data = self.post(payload)
        self.assertTrue(data['sections'])
        self.assertTrue(all(s['leader'] is None and s['status'] in ('NO_DATA','INCONSISTENT') for s in data['sections']))
        data = self.post({**payload,'contest':'G'})
        self.assertEqual(set(data['counts']),{'NOT_CONTESTED'})

    def test_invalid_and_cors(self):
        for payload in [{'operation':'map','level':'state','id':'11','year':2015,'contest':'A'}, {'operation':'map','level':'state','id':'20','year':2024,'contest':'A'}]:
            with self.assertRaises(HTTPError) as err:
                self.post(payload)
            self.assertEqual(err.exception.code,400)
        with self.assertRaises(HTTPError) as err:
            self.post({'operation':'catalog'},origin='https://example.com')
        self.assertEqual(err.exception.code,403)

    def test_outcome_boundaries(self):
        row = {'data_status':'AVAILABLE','total_votes':200,'votes_by_tracked_party':{'PAN':100,'PRI':100,'PVEM':0,'MORENA':0}}
        self.assertEqual(tracked_outcome(row),('TIE',None))
        self.assertEqual(tracked_outcome({**row,'total_votes':0,'votes_by_tracked_party':dict.fromkeys(row['votes_by_tracked_party'],0)}),('ZERO_TOTAL',None))
        self.assertEqual(tracked_outcome({**row,'data_status':'INCONSISTENT'}),('INCONSISTENT',None))
        self.assertEqual(tracked_outcome({**row,'votes_by_tracked_party':dict.fromkeys(row['votes_by_tracked_party'],None)}),('NO_DATA',None))

if __name__ == '__main__':
    unittest.main()
