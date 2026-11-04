import {afterEach,it,expect,vi} from 'vitest'
import {fetchUniverseMap} from './universe.client'
const universe={level:'local-district' as const,id:'6',label:'Distrito local 6',sections:1}
function response(){return {contract:'HEYTI_UNIVERSE_RESPONSE',version:'1.0',capability_id:'describe_universe',universe,year:2021,contest:'DL',sections:[{section_id:'1261',crs:'OGC:CRS84',geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[1,1],[0,0]]]},status:'NO_DATA',leader:null,total:100,missing_reason:'TRACKED_BREAKDOWN_MISSING',votes:{PAN:0,PRI:null,PVEM:20,MORENA:10}}],counts:{NO_DATA:1},coverage:{geographic_sections:1,represented_sections:1,blocked_sections:0},provenance:{electoral_scope:'TRACKED_PARTIES_ONLY',grouping_basis:'PROPERTIES_OF_CURRENT_GEOJSON',electoral_validation:'AUDIT_PENDING'}}}
function mock(data:unknown){vi.stubEnv('VITE_HEYTI_GATEWAY_URL','http://127.0.0.1:8765');vi.stubGlobal('fetch',vi.fn().mockResolvedValue({ok:true,json:async()=>data}))}
afterEach(()=>{vi.unstubAllGlobals();vi.unstubAllEnvs()})
it('preserva el desglose ya enviado por el CORE en leaders, incluyendo cero y N/D',async()=>{mock(response());const map=await fetchUniverseMap(universe,2021,'DL');expect(map.sections[0].votes).toEqual({PAN:0,PRI:null,PVEM:20,MORENA:10});expect(map.sections[0].total).toBe(100)})
it('rechaza un desglose con cifras negativas sin normalizarlo a cero',async()=>{const data=response();data.sections[0].votes.PAN=-1;mock(data);await expect(fetchUniverseMap(universe,2021,'DL')).rejects.toThrow()})
