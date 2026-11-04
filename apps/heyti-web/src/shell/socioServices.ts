import type { SocioReference } from './socioTraceability'
export const SERVICES_FIELDS=['VIVPARH_CV','VPH_C_ELEC','VPH_S_ELEC','VPH_AGUADV','VPH_AGUAFV','VPH_DRENAJ','VPH_NODREN','VPH_C_SERV','VPH_INTER','VPH_CEL','VPH_PC'] as const
export type ServicesField=typeof SERVICES_FIELDS[number]
export interface ServicesValue {value:number|null;state:'OBSERVED'|'MISSING'|'RESERVED'|'NOT_APPLICABLE'}
export type ServicesRecord=Record<ServicesField,ServicesValue>
export interface ServicesData {sections:Record<string,ServicesRecord>;officialCsvSha256:string}
export const SERVICES_METRICS=[
 {key:'electricity',label:'Con electricidad',numerator:'VPH_C_ELEC'},
 {key:'no-electricity',label:'Sin electricidad',numerator:'VPH_S_ELEC'},
 {key:'water',label:'Con agua entubada en vivienda o patio',numerator:'VPH_AGUADV'},
 {key:'no-water',label:'Sin agua entubada en el ámbito de la vivienda',numerator:'VPH_AGUAFV'},
 {key:'drainage',label:'Con drenaje',numerator:'VPH_DRENAJ'},
 {key:'no-drainage',label:'Sin drenaje',numerator:'VPH_NODREN'},
 {key:'combined',label:'Electricidad, agua y drenaje · conjunto oficial',numerator:'VPH_C_SERV'},
 {key:'internet',label:'Con internet',numerator:'VPH_INTER'},
 {key:'cellphone',label:'Con teléfono celular',numerator:'VPH_CEL'},
 {key:'computer',label:'Con computadora, laptop o tableta',numerator:'VPH_PC'},
] as const
export type ServicesMetric=typeof SERVICES_METRICS[number]
export type ServicesSelection=ServicesMetric['key']
export const SERVICES_DENOMINATOR='VIVPARH_CV'
export const SERVICES_POPULATION='viviendas particulares habitadas con características captadas'
function object(v:unknown):Record<string,unknown>{if(!v||typeof v!=='object'||Array.isArray(v))throw new Error('Archivo de servicios inválido.');return v as Record<string,unknown>}
export function parseServicesValue(raw:unknown):ServicesValue{
 if(raw===null||raw===undefined||raw==='')return {value:null,state:'MISSING'}
 if(raw==='*')return {value:null,state:'RESERVED'}
 if(raw==='N/A')return {value:null,state:'NOT_APPLICABLE'}
 if(typeof raw!=='string'||!/^\d+$/.test(raw))throw new Error('Conteo de viviendas inválido.')
 const value=Number(raw)
 if(!Number.isSafeInteger(value)||value<0)throw new Error('Conteo de viviendas inválido.')
 return {value,state:'OBSERVED'}
}
export function parseServices(input:unknown,reference:SocioReference):ServicesData{
 const v=object(input)
 if(v.schema!=='HEYTI_SERVICES_2020_1'||v.entity!=='11'||v.year!==2020||v.officialCsvSha256!==reference.officialCsvSha256||JSON.stringify(v.fields)!==JSON.stringify(SERVICES_FIELDS))throw new Error('Fuente de servicios incompatible con la referencia 2020.')
 const sections:Record<string,ServicesRecord>={}
 const overlaps={VPH_C_ELEC:'VIV_CON_ELECTRICIDAD',VPH_AGUADV:'VIV_CON_AGUA',VPH_DRENAJ:'VIV_CON_DRENAJE',VPH_INTER:'VIV_CON_INTERNET',VPH_CEL:'VIV_CON_CEL',VPH_PC:'VIV_CON_PC'} as const
 for(const [id,raw] of Object.entries(object(v.sections))){
  if(!reference.sections[id]||!Array.isArray(raw)||raw.length!==SERVICES_FIELDS.length)throw new Error('Identidad o campos de servicios incompatibles.')
  const row=Object.fromEntries(SERVICES_FIELDS.map((k,i)=>[k,parseServicesValue(raw[i])])) as ServicesRecord
  for(const [field,key] of Object.entries(overlaps))if(row[field as keyof typeof overlaps].value!==reference.sections[id].values[key as typeof overlaps[keyof typeof overlaps]])throw new Error('La fuente de servicios no coincide con las cifras censales compartidas.')
  sections[id]=row
 }
 if(Object.keys(sections).length!==Object.keys(reference.sections).length)throw new Error('Cobertura de servicios incompleta frente a la referencia.')
 return {sections,officialCsvSha256:reference.officialCsvSha256}
}
export interface ServicesMeasure {numerator:number|null;denominator:number|null;percent:number|null;status:'AVAILABLE'|'NO_RECORD'|'MISSING_NUMERATOR'|'MISSING_DENOMINATOR'|'ZERO_DENOMINATOR'|'INCONSISTENT';numeratorState:ServicesValue['state']|null;denominatorState:ServicesValue['state']|null}
export function servicesMeasure(row:ServicesRecord|undefined,metric:ServicesMetric):ServicesMeasure {
 if(!row)return {numerator:null,denominator:null,percent:null,status:'NO_RECORD',numeratorState:null,denominatorState:null}
 const n=row[metric.numerator],d=row[SERVICES_DENOMINATOR]
 const status=n.value===null?'MISSING_NUMERATOR':d.value===null?'MISSING_DENOMINATOR':n.value>d.value?'INCONSISTENT':d.value===0?'ZERO_DENOMINATOR':'AVAILABLE'
 return {numerator:n.value,denominator:d.value,percent:status==='AVAILABLE'?n.value!/d.value!*100:null,status,numeratorState:n.state,denominatorState:d.state}
}
export function servicesSummary(ids:readonly string[],data:ServicesData,metric:ServicesMetric){
 let count=0,denominator=0,pairs=0,countsAvailable=0,countAvailableSum=0
 for(const id of ids){const m=servicesMeasure(data.sections[id],metric);if(m.numerator!==null&&m.status!=='INCONSISTENT'){countsAvailable++;countAvailableSum+=m.numerator}if(m.status==='AVAILABLE'){pairs++;count+=m.numerator!;denominator+=m.denominator!}}
 return {pairs,total:ids.length,count:pairs?count:null,denominator:pairs?denominator:null,percent:denominator>0?count/denominator*100:null,countsAvailable,countAvailableSum:countsAvailable?countAvailableSum:null}
}
export const SERVICES_STATUS:Record<ServicesMeasure['status'],string>={AVAILABLE:'Porcentaje calculable',NO_RECORD:'Sin registro para esta clave',MISSING_NUMERATOR:'Sin cantidad disponible',MISSING_DENOMINATOR:'Sin denominador disponible',ZERO_DENOMINATOR:'Viviendas de referencia cero; porcentaje N/D',INCONSISTENT:'Cantidad mayor al denominador; porcentaje N/D'}
