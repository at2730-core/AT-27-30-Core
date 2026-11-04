import {afterEach,beforeEach,describe,expect,it,vi} from 'vitest'
import {loadComparison,comparisonSignature} from './comparisonData'
import {fetchUniverseCatalog,fetchUniverseMap} from '../gateway/universe.client'
import {fetchSectionDemo} from '../gateway/section.demo'
import type {UniverseSelection} from '../platform/platform.types'
import type {UniverseMap,UniverseOption} from '../gateway/universe.client'
vi.mock('../gateway/universe.client',()=>({fetchUniverseCatalog:vi.fn(),fetchUniverseMap:vi.fn()}))
vi.mock('../gateway/section.demo',async importOriginal=>{
 const original=await importOriginal<typeof import('../gateway/section.demo')>()
 return {...original,fetchSectionDemo:vi.fn()}
})
const df:UniverseSelection={id:'1',level:'federal-district',label:'Distrito federal 1',parentId:'11',truthStatus:'pending'}
const option:UniverseOption={level:'federal-district',id:'1',label:'Distrito federal 1',sections:2}
const provenance={electoral_validation:'AUDIT_PENDING',master_sha256:'a'.repeat(64),geometry_sha256:'b'.repeat(64)}
function map(metric:'concentration'|'abstention'):UniverseMap {
 return {universe:option,year:2024,contest:'A',metric,counts:{},coverage:{geographic:2,represented:1,blocked:1},provenance,
  sections:[{sectionId:'228',geometry:{type:'Polygon',coordinates:[]} as never,status:metric==='concentration'?'ZERO_TOTAL':'ABS_VERY_HIGH',leader:null,total:0,nominal:100,abstention:100,votes:{PAN:0,PRI:null,PVEM:0,MORENA:0}}],
  trend:metric==='abstention'?[{year:2024,validSections:1,nominal:100,votes:0,abstention:100}]:undefined}
}
beforeEach(()=>{vi.resetAllMocks();vi.mocked(fetchUniverseCatalog).mockResolvedValue([option]);vi.mocked(fetchUniverseMap).mockImplementation(async(_u,_y,_c,_s,metric)=>map(metric as 'concentration'|'abstention'))})
afterEach(()=>vi.unstubAllGlobals())
describe('descriptive perspectives read boundary',()=>{
 it('uses the same explicit district and contest and preserves zero, null and blocked count',async()=>{
  const signal=new AbortController().signal
  const result=await loadComparison(df,['territorial-analysis','win-all'],'A',signal)
  expect(result.scope).toBe('federal-district:1');expect(result.blocked).toBe(1)
  expect(result.rows[0].total).toBe(0);expect(result.rows[0].votes.PRI).toBeNull();expect(result.rows[0].participation).toBe(0)
  expect(fetchUniverseMap).toHaveBeenCalledWith(option,2024,'A',signal,'concentration')
  expect(fetchUniverseMap).toHaveBeenCalledWith(option,2024,'A',signal,'abstention')
 })
 it('rejects incompatible source provenance before combining responses',async()=>{
  vi.mocked(fetchUniverseMap).mockImplementation(async(_u,_y,_c,_s,metric)=>({...map(metric as 'concentration'|'abstention'),provenance:{...provenance,master_sha256:metric==='concentration'?'c'.repeat(64):'a'.repeat(64)}}))
  await expect(loadComparison(df,['territorial-analysis','win-all'],'A',new AbortController().signal)).rejects.toThrow()
 })
 it('never substitutes state when active district is absent from catalog',async()=>{
  vi.mocked(fetchUniverseCatalog).mockResolvedValue([])
  await expect(loadComparison(df,['territorial-analysis','win-all'],'A',new AbortController().signal)).rejects.toThrow()
  expect(fetchUniverseMap).not.toHaveBeenCalled()
 })
 it('section path uses explicit demo and does not read area maps',async()=>{
  const section={...df,id:'228',level:'section' as const}
  vi.mocked(fetchSectionDemo).mockResolvedValue({sectionId:'228',status:'TERRITORIAL_BLOCKED',years:[],provenance})
  const result=await loadComparison(section,['territorial-analysis','socioeconomic'],'A',new AbortController().signal)
  expect(result.rows).toEqual([]);expect(result.blocked).toBe(1);expect(fetchUniverseMap).not.toHaveBeenCalled()
 })
 it('displays independent socioeconomic error without discarding electoral data',async()=>{
  vi.stubGlobal('fetch',vi.fn().mockResolvedValue({ok:false}))
  const result=await loadComparison(df,['territorial-analysis','socioeconomic'],'A',new AbortController().signal)
  expect(result.socioError).toBeTruthy();expect(result.socio).toBeNull();expect(result.rows).toHaveLength(1)
 })
 it('cancelled reading cannot complete with data',async()=>{
  const controller=new AbortController();controller.abort()
  await expect(loadComparison(df,['territorial-analysis','win-all'],'A',controller.signal)).rejects.toThrow()
 })
 it('result signature changes on universe, modules and contest',()=>{
  const sig=comparisonSignature(df,['territorial-analysis','win-all'],'A')
  expect(sig).not.toBe(comparisonSignature({...df,id:'2'},['territorial-analysis','win-all'],'A'))
  expect(sig).not.toBe(comparisonSignature(df,['territorial-analysis','socioeconomic'],'A'))
  expect(sig).not.toBe(comparisonSignature(df,['territorial-analysis','win-all'],'G'))
 })
})
