import unittest
from test_describe_universe import UniverseMapTests
from heyti.capabilities.describe_universe.municipalities import MUNICIPALITY_NAMES

class MunicipalityNamesTests(unittest.TestCase):
    setUpClass = classmethod(UniverseMapTests.setUpClass.__func__)
    tearDownClass = classmethod(UniverseMapTests.tearDownClass.__func__)
    post = UniverseMapTests.post
    def test_names_and_identity(self):
        self.assertEqual(set(MUNICIPALITY_NAMES),{str(i) for i in range(1,47)})
        options=[u for u in self.post({'operation':'catalog'})['catalog'] if u['level']=='municipality']
        self.assertEqual(len(options),46)
        self.assertEqual({u['id']:u['label'] for u in options},MUNICIPALITY_NAMES)
        self.assertEqual([u['id'] for u in options[:3]],['1','2','4'])
        self.assertEqual(sum(u['sections'] for u in options),3266)
        for metric in ['leaders','abstention','concentration']:
            data=self.post({'operation':'map','level':'municipality','id':'20','year':2024,'contest':'A','metric':metric})
            self.assertEqual(data['universe']['label'],'León')
            self.assertEqual(data['universe']['id'],'20')
            self.assertEqual(data['universe']['sections'],787)
            self.assertEqual(data['coverage']['represented_sections'],775)
            self.assertEqual(data['coverage']['blocked_sections'],12)

if __name__=='__main__':unittest.main()
