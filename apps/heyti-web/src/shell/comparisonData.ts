import type { UniverseSelection, HeytiModuleId } from '../platform/platform.types'
import {fetchUniverseCatalog,fetchUniverseMap} from '../gateway/universe.client'
import {fetchSectionDemo,demoParticipation} from '../gateway/section.demo'
import type {DemoContestId} from '../gateway/section.demo'
import type {AbstentionSummary} from '../gateway/universe.client'
import {attachResults2024} from './results2024'
import {parseSocio} from './socioeconomic'
import type {SocioData} from './socioeconomic'
import {parseSocioReference,verifySocioSource} from './socioTraceability'
import type {SocioReference, SocioVerification} from './socioTraceability'
import {comparisonModules,scopeKey,supportedUniverse} from './contextQueries'
export interface ComparisonRow {id:string;total:number|null;nominal:number|null;participation:number|null;votes:Record<string,number|null>;status:string}
export interface ComparisonData {scope:string;modules:HeytiModuleId[];contest:DemoContestId;rows:ComparisonRow[];trend:AbstentionSummary[];provenance:Record<string,string>;geographic:number;blocked:number;socio:SocioData|null;reference:SocioReference|null;verification:SocioVerification|null;socioError:string|null}
async function jsonFile(name:string,signal:AbortSignal) {
 const response=await fetch(`${import.meta.env.BASE_URL}data/${name}`,{signal})
 if(!response.ok)throw new Error('Archivo socioeconómico o referencia no disponible.')
 return response.json()
}
export async function loadComparison(universe:UniverseSelection,modules:HeytiModuleId[],contest:DemoContestId,signal:AbortSignal):Promise<ComparisonData> {
 comparisonModules(modules)
 if(!supportedUniverse(universe))throw new Error('Selecciona un universo disponible para comparar.')
 const data:ComparisonData={scope:scopeKey(universe),modules:[...modules],contest,rows:[],trend:[],provenance:{},geographic:0,blocked:0,socio:null,reference:null,verification:null,socioError:null}
 if(universe.level==='section') {
  const section=await fetchSectionDemo(universe.id,signal)
  data.geographic=1;data.provenance=section.provenance
  if(['TERRITORIAL_BLOCKED','GEOMETRY_UNAVAILABLE'].includes(section.status)) data.blocked=1
  else {
   const c=section.years.find(y=>y.year===2024)?.contests[contest]
   data.rows=[{id:universe.id,total:c?.total??null,nominal:c?.nominal??null,participation:c?demoParticipation(c):null,votes:c?.votes??{},status:c?.status??'NO_DATA'}]
   data.trend=section.years.map(y=>{const c=y.contests[contest],p=demoParticipation(c);return {year:y.year,validSections:p===null?0:1,nominal:p===null?0:c.nominal!,votes:p===null?0:c.total!,abstention:p===null?null:100-p}})
  }
 } else {
  const catalog=await fetchUniverseCatalog(signal)
  const option=catalog.find(o=>o.level===universe.level&&o.id===universe.id)
  if(!option)throw new Error('El universo activo no está en el catálogo; no se sustituye por otro.')
  const [base,nominal]=await Promise.all([fetchUniverseMap(option,2024,contest,signal,'concentration'),fetchUniverseMap(option,2024,contest,signal,'abstention')])
  const map=attachResults2024(base,nominal)
  data.provenance=map.provenance;data.geographic=map.coverage.geographic;data.blocked=map.coverage.blocked;data.trend=nominal.trend??[]
  data.rows=map.sections.map(s=>({id:s.sectionId,total:s.total,nominal:map.results2024![s.sectionId].nominal,participation:map.results2024![s.sectionId].participation,votes:s.votes??{},status:s.status}))
 }
 if(modules.includes('socioeconomic')&&data.rows.length) {
  try {
   const [raw,ref]=await Promise.all([jsonFile('heyti-socioeconomico.json',signal),jsonFile('heyti-socioeconomico-referencia-2020.json',signal)])
   data.socio=parseSocio(raw);data.reference=parseSocioReference(ref);data.verification=verifySocioSource(data.socio,data.reference)
  }catch(e){if(signal.aborted)throw e;data.socioError=e instanceof Error?e.message:'Datos censales no disponibles.'}
 }
 signal.throwIfAborted()
 return data
}
export function comparisonSignature(universe:UniverseSelection|null,modules:readonly HeytiModuleId[],contest:DemoContestId):string {
 return `${scopeKey(universe)}|${modules.join(',')}|${contest}`
}
