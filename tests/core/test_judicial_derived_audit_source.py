"""Synthetic SEC fixtures using the documented delta; no fixture is official SEC data."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from heyti.capabilities.describe_section.judicial_derived_audit_source import JudicialDerivedAuditSource, digest
from heyti.capabilities.describe_section.versioned_electoral_source import ReadRequest, SeriesKey

ROOT = Path(__file__).resolve().parents[2]
MANIFEST = ROOT / 'docs/auditoria/HEYTI_Manifiesto_Candidato_SanMiguel_A2024_v0_1.json'

def fixtures():
    m = json.loads(MANIFEST.read_text(encoding='utf-8'))
    keys = ['SEC:156','SEC:172','SEC:191','SEC:200'] + ['SEC:SYNTHETIC_' + str(i) for i in range(101)] + [m['special_unit']['unit_key']]
    vectors = [[0]*17 for _ in keys]
    for i, total in enumerate([1515,1964,296,1301]):
        vectors[i][0] = total
        vectors[i][14] = total
    vectors[4] = [v - sum(row[i] for row in vectors[:4]) for i,v in enumerate(m['base_vector'])]
    provenance = dict(m['source'], release_id='synthetic-base', cut_label='SOURCE_AS_PUBLISHED_UNVERIFIED_DATE', cut_date=None, cut_date_status='UNVERIFIED')
    responses = []
    for idx,key in enumerate(keys):
        vector = vectors[idx]
        options = [dict(col,votes=v,raw_value=str(v),missing_cause=None) for col,v in zip(m['columns'],vector)]
        cas = []
        for rule in m['restorations']+m['exclusions']:
            if rule['unit_key'] != key:
                continue
            cas.append({'original_identity':{'ACTA_CASILLA-MEC':rule['acta_literal'],'SECCION':key.split(':')[1],'ID_MUNICIPIO':'3'},'source_line':rule['source_line'],'raw_line_sha256':rule['raw_line_sha256'],'TRIBUNAL':'ANULADA','total_votes':rule['total'],'total_raw':str(rule['total']),'options':[dict(col,votes=v,raw_value=str(v),missing_cause=None) for col,v in zip(m['columns'],rule.get('votes',[0]*17))]})
        total = sum(v for v,col in zip(vector,m['columns']) if col['option_kind']!='VALID_VOTE_TOTAL')
        snapshot={'identity':dict(m['series'],unit_key=key,unit_kind='SPECIAL_SECTION_ROW' if idx==105 else 'ORDINARY_SECTION',municipality_code='3'),'provenance':deepcopy(provenance),'result':{'total_votes':total,'total_raw':str(total),'total_status':'NUMERIC','total_missing_cause':None,'nominal_list':None,'nominal_raw':'','nominal_status':'MISSING','nominal_missing_cause':'SYNTHETIC','options':options},'cas_evidence':cas,'issues':[{'code':'SYNTHETIC_OPEN_ISSUE'}],'coverage':{'status':'SYNTHETIC'}}
        if idx==105:
            snapshot['identity'].update(deepcopy(m['special_unit']),current_section_fk=None)
        responses.append({'status':'AUDIT_SOURCE_AS_PUBLISHED','purpose':'AUDIT','metric_scope':'RESULT','data':snapshot,'provenance':deepcopy(provenance)})
    return m,responses

class JudicialCandidateTests(unittest.TestCase):
    def setUp(self):
        self.m,self.rows=fixtures()
    def build(self):
        return JudicialDerivedAuditSource(self.m,digest(self.m),self.rows)
    def test_exact_vector_scope_and_exclusion(self):
        c=self.build()
        totals=[]
        for row in self.rows:
            identity=row['data']['identity']
            data=c.read(ReadRequest(SeriesKey(2024,'A','UNICA'),identity['unit_kind'],identity['unit_key'],purpose='AUDIT'),candidate_id=c.candidate_id)['data']
            totals.append(data['derived_result']['total_votes'])
            if identity['unit_key']=='SEC:156':
                self.assertEqual(data['derived_result']['total_votes'],1876)
                self.assertEqual([r['acta_literal'] for r in data['restoration_evidence']],['C01'])
            if identity['unit_key']=='SEC:SYNTHETIC_0':
                self.assertEqual(data['base_vector'],[o['votes'] for o in data['derived_result']['options']])
        self.assertEqual(sum(totals),76757)
    def test_input_and_returned_data_cannot_mutate_candidate(self):
        original=deepcopy(self.rows); c=self.build(); self.assertEqual(self.rows,original)
        req=ReadRequest(SeriesKey(2024,'A','UNICA'),'ORDINARY_SECTION','SEC:156',purpose='AUDIT')
        first=c.read(req,candidate_id=c.candidate_id); first['data']['derived_result']['total_votes']=1
        self.rows[0]['data']['result']['total_votes']=1
        self.assertEqual(c.read(req,candidate_id=c.candidate_id)['data']['derived_result']['total_votes'],1876)
    def test_presentation_stays_blocked_for_both_metrics(self):
        c=self.build()
        for metric in ['RESULT','NOMINAL_LIST']:
            out=c.read(ReadRequest(SeriesKey(2024,'A','UNICA'),'ORDINARY_SECTION','SEC:156',metric_scope=metric,policy_id='cannot-bypass'),candidate_id=c.candidate_id)
            self.assertEqual(out['status'],'NO_RELEASE_SELECTED'); self.assertIsNone(out['data'])
    def test_wrong_candidate_series_scope_and_metric_rejected(self):
        c=self.build()
        for req,cid,status in [
            (ReadRequest(SeriesKey(2024,'A','UNICA'),'ORDINARY_SECTION','SEC:156',purpose='AUDIT'),'wrong','DERIVED_IDENTITY_MISMATCH'),
            (ReadRequest(SeriesKey(2024,'DL','MR'),'ORDINARY_SECTION','SEC:156',purpose='AUDIT'),c.candidate_id,'DERIVED_IDENTITY_MISMATCH'),
            (ReadRequest(SeriesKey(2024,'A','UNICA'),'ORDINARY_SECTION','SEC:99999',purpose='AUDIT'),c.candidate_id,'UNIT_OUTSIDE_DERIVED_SCOPE'),
            (ReadRequest(SeriesKey(2024,'A','UNICA'),'ORDINARY_SECTION','SEC:156',purpose='AUDIT',metric_scope='NOMINAL_LIST'),c.candidate_id,'DERIVED_METRIC_NOT_SUPPORTED'),
            (ReadRequest(SeriesKey(2024,'A','UNICA'),'ORDINARY_SECTION','SEC:156',purpose='AUDIT',release_id='wrong'),c.candidate_id,'DERIVED_IDENTITY_MISMATCH')]:
            self.assertEqual(c.read(req,candidate_id=cid)['status'],status)
    def test_manifest_hash_and_output_identity(self):
        c=self.build(); self.assertEqual(c.candidate_id,self.build().candidate_id)
        self.m['base_total']=1
        with self.assertRaisesRegex(ValueError,'MANIFEST_HASH'): JudicialDerivedAuditSource(self.m,'0'*64,self.rows)
    def test_missing_duplicate_or_wrong_municipality_units(self):
        for mutation in ['missing','duplicate','municipality','purpose','source']:
            with self.subTest(mutation=mutation):
                self.m,self.rows=fixtures()
                if mutation=='missing':self.rows.pop()
                if mutation=='duplicate':self.rows[1]=deepcopy(self.rows[0])
                if mutation=='municipality':self.rows[0]['data']['identity']['municipality_code']='4'
                if mutation=='purpose':self.rows[0]['purpose']='PRESENTATION'
                if mutation=='source':self.rows[0]['data']['provenance']['zip_sha256']='0'*64
                with self.assertRaises(ValueError):self.build()
    def test_null_option_missing_cell_or_total_rejected(self):
        for mutation in ['null','missing','total']:
            with self.subTest(mutation=mutation):
                self.m,self.rows=fixtures(); r=self.rows[0]['data']['result']
                if mutation=='null':r['options'][0].update(votes=None,raw_value='',missing_cause='SYNTHETIC')
                if mutation=='missing':r['options'].pop()
                if mutation=='total':r.update(total_votes=None,total_raw='',total_missing_cause='SYNTHETIC')
                with self.assertRaises(ValueError):self.build()
    def test_cas_hash_vector_or_ambiguity_rejected(self):
        for mutation in ['hash','vector','duplicate','excluded']:
            with self.subTest(mutation=mutation):
                self.m,self.rows=fixtures(); cas=self.rows[0]['data']['cas_evidence']
                if mutation=='hash':cas[0]['raw_line_sha256']='0'*64
                if mutation=='vector':cas[0]['options'][0]['votes']=71
                if mutation=='duplicate':cas.append(deepcopy(cas[0]))
                if mutation=='excluded':cas[1]['total_votes']=344
                with self.assertRaises(ValueError):self.build()
    def test_base_and_derived_arithmetic_fail_closed(self):
        self.rows[0]['data']['result']['total_votes']+=1
        with self.assertRaises(ValueError):self.build()
    def test_nominal_null_raw_and_issues_preserved(self):
        c=self.build(); out=c.read(ReadRequest(SeriesKey(2024,'A','UNICA'),'ORDINARY_SECTION','SEC:156',purpose='AUDIT'),candidate_id=c.candidate_id)
        self.assertIsNone(out['data']['base_snapshot']['result']['nominal_list'])
        self.assertEqual(out['data']['base_snapshot']['issues'],[{'code':'SYNTHETIC_OPEN_ISSUE'}])
        self.assertEqual(out['certification_status'],'NOT_CERTIFIED')

    def test_special_section_row_identity_is_exact_and_not_coerced(self):
        c=self.build(); special=self.m['special_unit']
        out=c.read(ReadRequest(SeriesKey(2024,'A','UNICA'),special['unit_kind'],special['unit_key'],purpose='AUDIT'),candidate_id=c.candidate_id)
        self.assertEqual(out['data']['base_snapshot']['identity']['original_identity'],special['original_identity'])
        self.assertEqual(out['data']['delta_total'],0)
        for mutation in ['kind','key','section','original','fk']:
            with self.subTest(mutation=mutation):
                self.m,self.rows=fixtures(); i=self.rows[-1]['data']['identity']
                if mutation=='kind':i['unit_kind']='SPECIAL_AGGREGATE'
                if mutation=='key':i['unit_key']='SEC:0'
                if mutation=='section':i['section_literal']='1'
                if mutation=='original':i['original_identity']['ID_MUNICIPIO']='4'
                if mutation=='fk':i['current_section_fk']=1
                with self.assertRaises(ValueError):self.build()
