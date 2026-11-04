import type { SocioReference } from './socioTraceability'
export const EDUCATION_FIELDS=['GRAPROES','P_15YMAS','P15YM_AN','P15YM_SE','P15PRI_IN','P15SEC_IN','P_6A11','P6A11_NOA','P_12A14','P12A14NOA','P_15A17','P15A17A','P_18A24','P18A24A','P_18YMAS','P18YM_PB'] as const
export type EducationField=typeof EDUCATION_FIELDS[number]
export interface EducationValue {value:number|null;state:'OBSERVED'|'MISSING'|'RESERVED'|'NOT_APPLICABLE'}
export type EducationRecord=Record<EducationField,EducationValue>
export interface EducationData {sections:Record<string,EducationRecord>;officialCsvSha256:string}
export const EDUCATION_METRICS=[
 {key:'illiteracy',label:'Analfabetismo · 15 años y más',numerator:'P15YM_AN',denominator:'P_15YMAS',population:'personas de 15 años y más'},
 {key:'no-schooling',label:'Sin escolaridad · 15 años y más',numerator:'P15YM_SE',denominator:'P_15YMAS',population:'personas de 15 años y más'},
 {key:'primary-incomplete',label:'Primaria incompleta · 15 años y más',numerator:'P15PRI_IN',denominator:'P_15YMAS',population:'personas de 15 años y más'},
 {key:'secondary-incomplete',label:'Secundaria incompleta · 15 años y más',numerator:'P15SEC_IN',denominator:'P_15YMAS',population:'personas de 15 años y más'},
 {key:'nonattendance-6-11',label:'No asiste a la escuela · 6 a 11 años',numerator:'P6A11_NOA',denominator:'P_6A11',population:'personas de 6 a 11 años'},
 {key:'nonattendance-12-14',label:'No asiste a la escuela · 12 a 14 años',numerator:'P12A14NOA',denominator:'P_12A14',population:'personas de 12 a 14 años'},
 {key:'attendance-15-17',label:'Asiste a la escuela · 15 a 17 años',numerator:'P15A17A',denominator:'P_15A17',population:'personas de 15 a 17 años'},
 {key:'attendance-18-24',label:'Asiste a la escuela · 18 a 24 años',numerator:'P18A24A',denominator:'P_18A24',population:'personas de 18 a 24 años'},
 {key:'postbasic',label:'Educación posbásica · 18 años y más',numerator:'P18YM_PB',denominator:'P_18YMAS',population:'personas de 18 años y más'},
] as const
export type EducationMetric=typeof EDUCATION_METRICS[number]
export type EducationSelection=EducationMetric['key']|'schooling'
function object(v:unknown):Record<string,unknown>{if(!v||typeof v!=='object'||Array.isArray(v))throw new Error('Archivo educativo inválido.');return v as Record<string,unknown>}
export function parseEducationValue(raw:unknown,field:EducationField):EducationValue{
 if(raw===null||raw===undefined||raw==='')return {value:null,state:'MISSING'}
 if(raw==='*')return {value:null,state:'RESERVED'}
 if(raw==='N/A')return {value:null,state:'NOT_APPLICABLE'}
 if(typeof raw!=='string'||!/^\d+(?:\.\d+)?$/.test(raw))throw new Error('Cifra educativa inválida.')
 const value=Number(raw)
 if(!Number.isFinite(value)||value<0||(field!=='GRAPROES'&&!Number.isSafeInteger(value)))throw new Error('Cifra educativa inválida.')
 return {value,state:'OBSERVED'}
}
export function parseEducation(input:unknown,reference:SocioReference):EducationData{
 const v=object(input)
 if(v.schema!=='HEYTI_EDUCATION_2020_1'||v.entity!=='11'||v.year!==2020||v.officialCsvSha256!==reference.officialCsvSha256||JSON.stringify(v.fields)!==JSON.stringify(EDUCATION_FIELDS))throw new Error('Fuente educativa incompatible con la referencia 2020.')
 const sections:Record<string,EducationRecord>={}
 const overlaps={GRAPROES:'ESCOLARIDAD_PROM',P15YM_AN:'ANALFABETAS_15MAS',P_15A17:'POB_15_17',P_18YMAS:'POB_18MAS'} as const
 for(const [id,raw] of Object.entries(object(v.sections))){
  if(!reference.sections[id]||!Array.isArray(raw)||raw.length!==EDUCATION_FIELDS.length)throw new Error('Identidad o campos educativos incompatibles.')
  const row=Object.fromEntries(EDUCATION_FIELDS.map((k,i)=>[k,parseEducationValue(raw[i],k)])) as EducationRecord
  for(const [field,key] of Object.entries(overlaps))if(row[field as keyof typeof overlaps].value!==reference.sections[id].values[key as typeof overlaps[keyof typeof overlaps]])throw new Error('La fuente educativa no coincide con las cifras censales compartidas.')
  sections[id]=row
 }
 if(Object.keys(sections).length!==Object.keys(reference.sections).length)throw new Error('Cobertura educativa incompleta frente a la referencia.')
 return {sections,officialCsvSha256:reference.officialCsvSha256}
}
export interface EducationMeasure {numerator:number|null;denominator:number|null;percent:number|null;status:'AVAILABLE'|'NO_RECORD'|'MISSING_NUMERATOR'|'MISSING_DENOMINATOR'|'ZERO_DENOMINATOR'|'INCONSISTENT';numeratorState:EducationValue['state']|null;denominatorState:EducationValue['state']|null}
export function educationMeasure(row:EducationRecord|undefined,metric:EducationMetric):EducationMeasure {
 if(!row)return {numerator:null,denominator:null,percent:null,status:'NO_RECORD',numeratorState:null,denominatorState:null}
 const n=row[metric.numerator],d=row[metric.denominator]
 const status=n.value===null?'MISSING_NUMERATOR':d.value===null?'MISSING_DENOMINATOR':n.value>d.value?'INCONSISTENT':d.value===0?'ZERO_DENOMINATOR':'AVAILABLE'
 return {numerator:n.value,denominator:d.value,percent:status==='AVAILABLE'?n.value!/d.value!*100:null,status,numeratorState:n.state,denominatorState:d.state}
}
export function educationSummary(ids:readonly string[],data:EducationData,metric:EducationMetric){
 let count=0,denominator=0,pairs=0,countsAvailable=0,countAvailableSum=0
 for(const id of ids){const m=educationMeasure(data.sections[id],metric);if(m.numerator!==null&&m.status!=='INCONSISTENT'){countsAvailable++;countAvailableSum+=m.numerator}if(m.status==='AVAILABLE'){pairs++;count+=m.numerator!;denominator+=m.denominator!}}
 return {pairs,total:ids.length,count:pairs?count:null,denominator:pairs?denominator:null,percent:denominator>0?count/denominator*100:null,countsAvailable,countAvailableSum:countsAvailable?countAvailableSum:null}
}
export const EDUCATION_STATUS:Record<EducationMeasure['status'],string>={AVAILABLE:'Porcentaje calculable',NO_RECORD:'Sin registro para esta clave',MISSING_NUMERATOR:'Sin cantidad disponible',MISSING_DENOMINATOR:'Sin denominador disponible',ZERO_DENOMINATOR:'Población de referencia cero; porcentaje N/D',INCONSISTENT:'Cantidad mayor al denominador; porcentaje N/D'}
