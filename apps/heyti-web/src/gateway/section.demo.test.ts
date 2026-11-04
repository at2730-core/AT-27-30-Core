import { describe, expect, it, vi, afterEach } from 'vitest'
import { DEMO_CONTESTS, demoParticipation, parseSectionDemo, fetchSectionDemo } from './section.demo'
function fixture() {
  const c={status:'INCOMPLETE',total:0,nominal:100,votes:{PAN:0,PRI:null,PVEM:0,MORENA:0}}
  return {contract:'HEYTI_UNIVERSE_RESPONSE',version:'1.0',capability_id:'describe_universe',section_id:'228',view:'SECTION_DEMO',source_mode:'DEMO_MASTER',modality:'UNSPECIFIED_IN_MASTER',status:'DEMO_AVAILABLE',provenance:{master_sha256:'a'.repeat(64),geometry_sha256:'b'.repeat(64),electoral_validation:'AUDIT_PENDING',electoral_scope:'TRACKED_PARTIES_ONLY',grouping_basis:'PROPERTIES_OF_CURRENT_GEOJSON'},years:[2018,2021,2024].map(year=>({year,contests:Object.fromEntries(DEMO_CONTESTS.map(cid=>[cid,structuredClone(c)]))}))}
}
afterEach(()=>vi.unstubAllGlobals())
describe('explicit section demonstration',()=>{
  it('preserves zero and missing votes separately',()=>{
    const r=parseSectionDemo(fixture(),'228'), c=r.years[2].contests.A
    expect(c.votes.PRI).toBeNull(); expect(c.total).toBe(0); expect(demoParticipation(c)).toBe(0)
  })
  it('rejects wrong section, selected source and RP relabeling',()=>{
    for(const change of [{section_id:'229'},{source_mode:'SELECTED_RESULT'},{modality:'RP'}]) expect(()=>parseSectionDemo({...fixture(),...change},'228')).toThrow()
  })
  it('rejects missing years, duplicates, parties and nonnumeric values',()=>{
    const a=fixture(); a.years.pop(); expect(()=>parseSectionDemo(a,'228')).toThrow()
    const b=fixture(); b.years[0].year=2021; expect(()=>parseSectionDemo(b,'228')).toThrow()
    const c=fixture(); Reflect.deleteProperty(c.years[0].contests.A.votes,'PRI'); expect(()=>parseSectionDemo(c,'228')).toThrow()
    const d=fixture(); Object.assign(d.years[0].contests.A,{total:'0'}); expect(()=>parseSectionDemo(d,'228')).toThrow()
  })
  it('blocked source has no numbers and cannot carry hidden results',()=>{
    expect(parseSectionDemo({...fixture(),status:'TERRITORIAL_BLOCKED',years:[]},'228').years).toEqual([])
    expect(()=>parseSectionDemo({...fixture(),status:'TERRITORIAL_BLOCKED'},'228')).toThrow()
  })
  it('requires pending provenance and source hashes',()=>{
    const f=fixture(); f.provenance.electoral_validation='CERTIFIED'; expect(()=>parseSectionDemo(f,'228')).toThrow()
  })
  it('does not calculate participation without valid denominator or for non-contested elections',()=>{
    const c=parseSectionDemo(fixture(),'228').years[2].contests.A
    for(const change of [{nominal:0},{total:null},{total:101},{status:'NOT_CONTESTED'},{status:'INCONSISTENT'}]) expect(demoParticipation({...c,...change})).toBeNull()
  })
  it('requests explicit demo operation and forwards abort signal',async()=>{
    const fetcher=vi.fn().mockResolvedValue({ok:true,json:async()=>fixture()}); vi.stubGlobal('fetch',fetcher)
    const signal=new AbortController().signal; await fetchSectionDemo('228',signal)
    const options=fetcher.mock.calls[0][1]; expect(options.signal).toBe(signal)
    expect(JSON.parse(options.body)).toEqual({operation:'section-demo',section_id:'228'})
  })
})
