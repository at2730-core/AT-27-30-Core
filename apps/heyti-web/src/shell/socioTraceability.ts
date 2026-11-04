import { SOCIO_INDICATORS } from './socioeconomic'
import type { SocioData, SocioKey } from './socioeconomic'
import type { UniverseMap } from '../gateway/universe.client'

export const SOCIO_OFFICIAL_URL = 'https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/geoelectorales/eceg_2020_csv.zip'
export const SOCIO_METHOD_URL = 'https://gaia.inegi.org.mx/mdm6/docs/geoelectorales/Metodolog%C3%ADa_de_Estad%C3%ADsticas_Censales_a_escalas_Geoelectorales.pdf'
export const SOCIO_FIELD_MAPPING: Record<SocioKey, string> = {
 POB_TOTAL:'POBTOT', POB_15_17:'P_15A17', POB_18MAS:'P_18YMAS', ESCOLARIDAD_PROM:'GRAPROES', ANALFABETAS_15MAS:'P15YM_AN',
 PEA_12MAS:'PEA', OCUPADOS_12MAS:'POCUPADA', DESOCUPADOS_12MAS:'PDESOCUP', VIV_CON_ELECTRICIDAD:'VPH_C_ELEC',
 VIV_CON_AGUA:'VPH_AGUADV', VIV_CON_DRENAJE:'VPH_DRENAJ', VIV_CON_INTERNET:'VPH_INTER', VIV_CON_CEL:'VPH_CEL', VIV_CON_PC:'VPH_PC',
}
interface SocioReferenceSection { district:string; municipality:string; values: Record<SocioKey,number> }
export interface SocioReference {year:2020; published:string; audited:string; officialCsvSha256:string; sections:Record<string,SocioReferenceSection>; relations:Record<string,{origin:string;evidence:string}>; creationOnly:string[]}
const isId=(v:unknown):v is string=>typeof v==='string'&&/^[1-9]\d*$/.test(v)
function object(v:unknown):Record<string,unknown>{if(!v||typeof v!=='object'||Array.isArray(v))throw new Error('Referencia socioeconómica inválida.');return v as Record<string,unknown>}
export function parseSocioReference(input:unknown):SocioReference {
 const v=object(input), keys=SOCIO_INDICATORS.map(i=>i.key)
 if(v.schema!=='HEYTI_SOCIO_REFERENCE_1'||v.entity!=='11'||v.year!==2020||!Array.isArray(v.keys)||JSON.stringify(v.keys)!==JSON.stringify(keys)||typeof v.officialCsvSha256!=='string'||!/^[a-f0-9]{64}$/.test(v.officialCsvSha256)||v.published!=='2021-08-18'||v.audited!=='2026-10-21')throw new Error('Referencia censal no compatible con esta revisión.')
 const mapping=object(v.mapping)
 if(keys.some(k=>mapping[k]!==SOCIO_FIELD_MAPPING[k]))throw new Error('Correspondencias de indicadores no compatibles.')
 const sections:SocioReference['sections']={}
 for(const [id,value] of Object.entries(object(v.sections))){
  const row=object(value)
  if(!isId(id)||!isId(row.district)||!isId(row.municipality)||!Array.isArray(row.values)||row.values.length!==keys.length)throw new Error('Registro de referencia censal inválido.')
  const values=row.values
  for(let i=0;i<keys.length;i++)if(typeof values[i]!=='number'||!Number.isFinite(values[i])||values[i]<0||(keys[i]!=='ESCOLARIDAD_PROM'&&!Number.isSafeInteger(values[i])))throw new Error('Cifra de referencia censal inválida.')
  sections[id]={district:row.district,municipality:row.municipality,values:Object.fromEntries(keys.map((k,i)=>[k,values[i]])) as Record<SocioKey,number>}
 }
 if(Object.keys(sections).length!==3161)throw new Error('Referencia censal incompleta para Guanajuato.')
 const relations:SocioReference['relations']={}
 for(const [child,value] of Object.entries(object(v.relations))){const row=object(value);if(!isId(child)||sections[child]||!isId(row.origin)||!sections[row.origin]||!['reseccionamiento_2021','caso_145'].includes(String(row.evidence)))throw new Error('Relación territorial de referencia inválida.');relations[child]={origin:row.origin,evidence:String(row.evidence)}}
 if(!Array.isArray(v.creationOnly)||v.creationOnly.some(id=>!isId(id)||sections[id]))throw new Error('Referencia de creación territorial inválida.')
 return {year:2020,published:v.published,audited:v.audited,officialCsvSha256:v.officialCsvSha256,sections,relations,creationOnly:v.creationOnly as string[]}
}
export interface SocioVerification {allMatch:boolean; matched:number; different:number; missing:number; withoutReference:number; referenceWithoutRecord:number; comparisons:number}
export function verifySocioSource(data:SocioData, reference:SocioReference):SocioVerification {
 let matched=0,different=0,missing=0,withoutReference=0,comparisons=0
 for(const [id,row] of Object.entries(data)){
  const source=reference.sections[id]
  if(!source){withoutReference++;continue}
  for(const {key} of SOCIO_INDICATORS){comparisons++;if(row[key]==null)missing++;else if(row[key]===source.values[key])matched++;else different++}
 }
 const referenceWithoutRecord=Object.keys(reference.sections).filter(id=>!data[id]).length
 return {allMatch:!different&&!missing&&!withoutReference&&!referenceWithoutRecord,matched,different,missing,withoutReference,referenceWithoutRecord,comparisons}
}
export function socioValueStatus(id:string,key:SocioKey,data:SocioData,reference:SocioReference):string {
 const value=data[id]?.[key]
 if(value==null)return 'N/D · sin cifra disponible'
 const source=reference.sections[id]
 if(!source)return 'Valor del archivo sin referencia censal para esta clave'
 return value===source.values[key]?'Coincide con INEGI 2020':'Difiere de la referencia INEGI 2020'
}
export function socioLinkLabel(id:string,reference:SocioReference):string {
 if(reference.sections[id])return 'Enlace por clave; equivalencia de límites pendiente'
 const relation=reference.relations[id]
 if(relation)return `Sin registro censal propio; origen documentado ${relation.origin}, sin reparto de cifras`
 if(reference.creationOnly.includes(id))return 'Sin registro censal propio; creación documentada, origen pendiente'
 return 'Sin registro censal para esta clave; correspondencia pendiente'
}
export function socioUniverseCoverage(map:UniverseMap,reference:SocioReference){
 const matches=map.sections.filter(s=>reference.sections[s.sectionId])
 return {matched:matches.length,withoutRecord:map.sections.length-matches.length,
  documentedOrigins:map.sections.filter(s=>reference.relations[s.sectionId]).length,
  districtDifferences:map.universe.level==='federal-district'?matches.filter(s=>reference.sections[s.sectionId].district!==map.universe.id).length:null}
}
