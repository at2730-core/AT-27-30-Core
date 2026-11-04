import unittest
from test_describe_universe import UniverseMapTests
from heyti.capabilities.describe_universe.implementation import abstention_outcome

class AbstentionTests(unittest.TestCase):
    setUpClass = classmethod(UniverseMapTests.setUpClass.__func__)
    tearDownClass = classmethod(UniverseMapTests.tearDownClass.__func__)
    post = UniverseMapTests.post
    def test_abstention_zero_and_summary_only(self):
        c = {'data_status': 'AVAILABLE', 'total_votes': 0, 'nominal_list': 620}
        self.assertEqual(abstention_outcome(c), ('ABS_VERY_HIGH', 100))
        self.assertEqual(abstention_outcome({**c, 'total_votes': None}), ('NO_DATA', None))
        self.assertEqual(abstention_outcome({**c, 'nominal_list': 0}), ('INCONSISTENT', None))
        self.assertEqual(abstention_outcome({**c, 'total_votes': 621}), ('INCONSISTENT', None))
        self.assertEqual(abstention_outcome({**c, 'data_status': 'NOT_CONTESTED'}), ('NOT_CONTESTED', None))
        for votes, band in [(76,'ABS_LOW'),(75,'ABS_MID'),(50,'ABS_HIGH'),(25,'ABS_VERY_HIGH')]:
            self.assertEqual(abstention_outcome({**c,'nominal_list':100,'total_votes':votes})[0],band)

    def test_real_abstention_and_history(self):
        payload = {'operation':'map','metric':'abstention','level':'municipality','id':'20','year':2024,'contest':'A'}
        data = self.post(payload)
        ids = {s['section_id']:s for s in data['sections']}
        self.assertEqual(ids['1524']['abstention'],100)
        self.assertAlmostEqual(ids['1621']['abstention'], (1093-799)*100/1093)
        self.assertEqual(data['metric'],'abstention')
        summary = data['trend'][2]
        valid = [s for s in data['sections'] if s['abstention'] is not None]
        self.assertEqual(summary['valid_sections'],len(valid))
        self.assertEqual(summary['votes'],sum(s['total'] for s in valid))
        self.assertEqual(summary['nominal'],sum(s['nominal'] for s in valid))
        self.assertEqual(sum(data['counts'].values()),data['coverage']['represented_sections'])
        data = self.post({**payload,'year':2021,'contest':'DF'})
        self.assertGreater(data['trend'][1]['valid_sections'],0)
        self.assertTrue(any(s['abstention'] is not None for s in data['sections']))
        data = self.post({**payload,'year':2021,'contest':'G'})
        self.assertEqual(set(data['counts']),{'NOT_CONTESTED'})
        self.assertIsNone(data['trend'][1]['abstention'])

if __name__ == '__main__':
    unittest.main()
