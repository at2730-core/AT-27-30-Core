import unittest
from test_describe_universe import UniverseMapTests
from heyti.capabilities.describe_universe.implementation import concentration_outcome

class ConcentrationTests(unittest.TestCase):
    setUpClass = classmethod(UniverseMapTests.setUpClass.__func__)
    tearDownClass = classmethod(UniverseMapTests.tearDownClass.__func__)
    post = UniverseMapTests.post
    def test_formula_and_zero(self):
        c={'data_status':'AVAILABLE','total_votes':100,'votes_by_tracked_party':{'PAN':50,'PRI':0,'PVEM':0,'MORENA':0}}
        self.assertEqual(concentration_outcome(c),('HHI_LOW',.25))
        self.assertEqual(concentration_outcome({**c,'total_votes':0,'votes_by_tracked_party':dict.fromkeys(c['votes_by_tracked_party'],0)}),('ZERO_TOTAL',None))
        self.assertEqual(concentration_outcome({**c,'votes_by_tracked_party':dict.fromkeys(c['votes_by_tracked_party'],None)}),('NO_DATA',None))
    def test_real_map_and_aggregate(self):
        q={'operation':'map','metric':'concentration','level':'municipality','id':'20','year':2024,'contest':'A'}
        d=self.post(q);ids={s['section_id']:s for s in d['sections']}
        self.assertIsNone(ids['1524']['concentration'])
        self.assertEqual(ids['1524']['status'],'ZERO_TOTAL')
        self.assertAlmostEqual(ids['1621']['concentration'],sum((v/799)**2 for v in [465,17,23,173]))
        valid=[s for s in d['sections'] if s['concentration'] is not None]
        a=d['summary'];self.assertEqual(a['valid_sections'],len(valid))
        self.assertEqual(a['total'],sum(s['total'] for s in valid))
        self.assertAlmostEqual(a['index'],sum((v/a['total'])**2 for v in a['votes'].values()))
        self.assertLessEqual(a['tracked_coverage'],1)
        missing=self.post({**q,'metric':'leaders','year':2021,'contest':'DF'})
        self.assertTrue(any(s['missing_reason']=='TRACKED_BREAKDOWN_MISSING' for s in missing['sections']))

if __name__=='__main__':unittest.main()
