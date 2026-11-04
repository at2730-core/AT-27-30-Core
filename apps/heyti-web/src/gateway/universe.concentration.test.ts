import { afterEach, expect, it, vi } from 'vitest'
import { fetchUniverseMap } from './universe.client'
const u={level:'state' as const,id:'11',label:'Guanajuato',sections:1}
function data(){return {contract:'HEYTI_UNIVERSE_RESPONSE',version:'1.0',capability_id:'describe_universe',metric:'concentration',classification:'PARTIAL_HHI_V1_THRESHOLDS',universe:u,year:2024,contest:'A',sections:[{section_id:'1621',geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[1,1],[0,0]]]},crs:'OGC:CRS84',status:'HHI_LOW',leader:null,total:100,votes:{PAN:50,PRI:0,PVEM:0,MORENA:0},concentration:.25}],counts:{HHI_LOW:1},coverage:{geographic_sections:1,represented_sections:1,blocked_sections:0},provenance:{electoral_scope:'TRACKED_PARTIES_ONLY',grouping_basis:'PROPERTIES_OF_CURRENT_GEOJSON',electoral_validation:'AUDIT_PENDING'},summary:{valid_sections:1,total:100,votes:{PAN:50,PRI:0,PVEM:0,MORENA:0},index:.25,tracked_coverage:.5}}}
function mock(d:unknown){vi.stubEnv('VITE_HEYTI_GATEWAY_URL','http://127.0.0.1:8765');vi.stubGlobal('fetch',vi.fn().mockResolvedValue({ok:true,json:async()=>d}))}
afterEach(()=>{vi.unstubAllGlobals();vi.unstubAllEnvs()})
it('uses total rather than renormalizing four parties',async()=>{mock(data());const d=await fetchUniverseMap(u,2024,'A',undefined,'concentration');expect(d.summary?.index).toBe(.25);expect(d.summary?.trackedCoverage).toBe(.5)})
it('rejects fabricated index',async()=>{const d=data();d.sections[0].concentration=1;mock(d);await expect(fetchUniverseMap(u,2024,'A',undefined,'concentration')).rejects.toThrow()})
it('rejects aggregate not matching map',async()=>{const d=data();d.summary.votes.PAN=49;mock(d);await expect(fetchUniverseMap(u,2024,'A',undefined,'concentration')).rejects.toThrow()})
