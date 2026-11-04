import {afterEach,describe,expect,it,vi} from 'vitest'
import {fetchUniverseMap} from './universe.client'
const universe={level:'local-district' as const,id:'6',label:'Distrito local 6',sections:1}
const source=()=>({contract:'HEYTI_UNIVERSE_RESPONSE',version:'1.0',capability_id:'describe_universe',universe,year:2024,contest:'A',sections:[{section_id:'1466',crs:'OGC:CRS84',geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[1,1],[0,0]]]},status:'ZERO_TOTAL',leader:null,total:0}],counts:{ZERO_TOTAL:1},coverage:{geographic_sections:1,represented_sections:1,blocked_sections:0},provenance:{electoral_scope:'TRACKED_PARTIES_ONLY',grouping_basis:'PROPERTIES_OF_CURRENT_GEOJSON',electoral_validation:'AUDIT_PENDING'}})
function mock(value:unknown){vi.stubEnv('VITE_HEYTI_GATEWAY_URL','http://127.0.0.1:8765');vi.stubGlobal('fetch',vi.fn().mockResolvedValue({ok:true,json:async()=>value}))}
afterEach(()=>{vi.unstubAllGlobals();vi.unstubAllEnvs()})
describe('Cobertura global separada del universo',()=>{
 it('conserva una cifra global mayor que la cobertura local sin atribuirla al distrito',async()=>{
  const raw=source();mock({...raw,coverage:{...raw.coverage,master_only_unmapped:80}})
  const result=await fetchUniverseMap(universe,2024,'A')
  expect(result.coverage.masterOnlyUnmapped).toBe(80)
  expect(result.coverage.geographic).toBe(1);expect(result.coverage.blocked).toBe(0)
 })
 it('conserva cero informado por el CORE',async()=>{
  const raw=source();mock({...raw,coverage:{...raw.coverage,master_only_unmapped:0}})
  expect((await fetchUniverseMap(universe,2024,'A')).coverage.masterOnlyUnmapped).toBe(0)
 })
 it('no inventa 80 ni cero cuando una respuesta anterior omite el dato global',async()=>{
  mock(source());expect((await fetchUniverseMap(universe,2024,'A')).coverage.masterOnlyUnmapped).toBe(undefined)
 })
 it('rechaza conteos globales negativos, fraccionarios, nulos o de texto',async()=>{
  for(const value of [-1,1.5,null,'80']){
   const raw=source();mock({...raw,coverage:{...raw.coverage,master_only_unmapped:value}})
   await expect(fetchUniverseMap(universe,2024,'A')).rejects.toThrow('Conteo')
  }
 })
})
