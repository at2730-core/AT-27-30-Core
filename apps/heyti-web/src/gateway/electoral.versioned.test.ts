import { describe, expect, it, vi, afterEach } from 'vitest'
import { describeSection } from './heyti.client'
import type { HeytiResponse } from './heyti.client'
import { readVersionedElectoral } from './electoral.versioned'

function response(content: unknown): HeytiResponse {
  return {response_id:'test', contract:'HEYTI_RESPONSE', version:'1.0', capability_id:'describe_section', status:'success_with_warnings',
    blocks:[{type:'metadata',role:'electoral_versioned',content}], warnings:[],errors:[],
    trace:{request_id:null,session_id:null,execution_id:null,knowledge_version:null}}
}
const blocked = {status:'NO_RELEASE_SELECTED',purpose:'PRESENTATION',metric_scope:'RESULT',data:null,selection_status:'UNDECIDED'}
afterEach(() => vi.unstubAllGlobals())
describe('versioned presentation boundary', () => {
  it('preserves blocked status without numeric fallback', () => {
    expect(readVersionedElectoral(response(blocked))).toEqual({status:'NO_RELEASE_SELECTED',selectionStatus:'UNDECIDED',certificationStatus:null})
  })
  it('rejects missing, duplicate and competing legacy blocks', () => {
    const missing=response(blocked); missing.blocks=[]
    const duplicate=response(blocked); duplicate.blocks.push(duplicate.blocks[0])
    const legacy=response(blocked); legacy.blocks.push({type:'domain',role:'electoral',content:{}})
    for (const value of [missing,duplicate,legacy]) expect(() => readVersionedElectoral(value)).toThrow()
  })
  it('rejects audit data and unselected numbers', () => {
    for (const value of [{...blocked,purpose:'AUDIT'},{...blocked,data:{total_votes:999}}, {...blocked,status:'SELECTED_RESULT'}]) {
      expect(() => readVersionedElectoral(response(value))).toThrow()
    }
  })
  it('sends explicit year, election and modality and preserves abort signal', async () => {
    const fetchMock=vi.fn().mockResolvedValue(new Response(JSON.stringify(response(blocked)),{status:200,headers:{'Content-Type':'application/json'}}))
    vi.stubGlobal('fetch',fetchMock)
    const controller=new AbortController()
    await describeSection('1080',controller.signal,{year:2024,type:'DF',modality:'RP'})
    const init=fetchMock.mock.calls[0][1]
    expect(JSON.parse(init.body)).toEqual({section_id:'1080',electoral_query:{year:2024,type:'DF',modality:'RP'}})
    expect(init.signal).toBe(controller.signal)
  })
  it('default section query is explicit A2024, not legacy', async () => {
    const fetchMock=vi.fn().mockResolvedValue(new Response(JSON.stringify(response(blocked)),{status:200}))
    vi.stubGlobal('fetch',fetchMock)
    await describeSection('1080')
    expect(JSON.parse(fetchMock.mock.calls[0][1].body).electoral_query).toEqual({year:2024,type:'A',modality:'UNICA'})
  })
})
