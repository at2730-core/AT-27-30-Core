import type { UniverseMap } from '../gateway/universe.client'
import type { SocioReference } from './socioTraceability'
import { geometryFingerprint } from './socioRural'

export type ProjectionMode = 'ln-history' | 'ln-rate' | 'adult-rate'
export interface ProjectionRow {
 id:string; history:(number|null)[]; adults2020:number|null; base:number|null;
 rate:number|null; projected:number|null; reason:string; years:number;
}
export function parseAnnualRate(text:string):number {
 const clean=text.trim().replace(',','.')
 if(!/^[+-]?(?:\d+(?:\.\d*)?|\.\d+)$/.test(clean))throw new Error('Escribe una tasa anual explícita; cero también es una tasa válida.')
 const percent=Number(clean)
 if(!Number.isFinite(percent)||percent<=-100||percent>100)throw new Error('La tasa debe ser mayor de −100% y no mayor de 100% anual.')
 return percent/100
}
export function compound(base:number|null,rate:number|null,years:number):number|null {
 if(base===null||rate===null||!Number.isSafeInteger(base)||base<0||!Number.isFinite(rate)||rate<=-1||!Number.isInteger(years)||years<1)return null
 const value=base*(1+rate)**years
 return Number.isFinite(value)&&value<=Number.MAX_SAFE_INTEGER?value:null
}
const count=(value:number|null|undefined)=>value!=null&&Number.isSafeInteger(value)&&value>=0?value:null
export function projectionRows(maps:UniverseMap[],reference:SocioReference,mode:ProjectionMode,manualRate:number|null):ProjectionRow[] {
 const base=maps.find(m=>m.year===2024)
 const years=mode==='ln-history'?[2018,2021,2024]:[2024]
 if(!base||maps.length!==years.length||new Set(maps.map(m=>m.year)).size!==years.length||maps.some(m=>!years.includes(m.year)||m.universe.id!==base.universe.id||m.universe.level!==base.universe.level||m.contest!==base.contest||m.metric!==(mode==='adult-rate'?'leaders':'abstention')||JSON.stringify(Object.entries(m.provenance).sort())!==JSON.stringify(Object.entries(base.provenance).sort())))throw new Error('Las fuentes no corresponden al mismo universo, contienda y corte.')
 if(mode!=='ln-history'&&(manualRate===null||!Number.isFinite(manualRate)||manualRate<=-1||manualRate>1))throw new Error('Falta una tasa anual válida para el escenario.')
 const indexed=new Map(maps.map(m=>[m.year,new Map(m.sections.map(s=>[s.sectionId,s]))]))
 return base.sections.map(section=>{
  const id=section.sectionId,series=[2018,2021,2024].map(y=>indexed.get(y)?.get(id)),history=series.map(s=>count(s?.nominal))
  const adults2020=count(reference.sections[id]?.values.POB_18MAS),value=mode==='adult-rate'?adults2020:history[2],span=mode==='adult-rate'?7:3
  let rate=manualRate,reason='Escenario con tasa introducida por el usuario'
  if(mode==='ln-history'){
   rate=null
   if(series.some(s=>s&&geometryFingerprint(s.geometry)!==geometryFingerprint(section.geometry)))reason='Geometrías distintas entre respuestas; sin extrapolación'
   else if(series[0]?.status==='INCONSISTENT'||series[2]?.status==='INCONSISTENT')reason='Registro inconsistente en 2018 o 2024; sin extrapolación'
   else if(history[0]===null||history[2]===null)reason='Falta lista nominal en 2018 o 2024'
   else if(history[0]<=0||history[2]<=0)reason='CAGR requiere bases positivas en 2018 y 2024'
   else {rate=(history[2]/history[0])**(1/6)-1;reason='Extrapolación de LN por clave · CAGR 2018–2024'}
  } else if(mode==='ln-rate'&&section.status==='INCONSISTENT'){rate=null;reason='Registro 2024 inconsistente; sin escenario'}
  if(value===null)reason=mode==='adult-rate'?'Sin registro censal propio de 2020':'Sin lista nominal base de 2024'
  const projected=compound(value,rate,span)
  if(value!==null&&rate!==null&&projected===null)reason='Resultado fuera del rango calculable'
  return {id,history,adults2020,base:value,rate,projected,reason,years:span}
 })
}
export const projectionLabel=(mode:ProjectionMode)=>mode==='adult-rate'?'Población de 18 años y más': 'Lista nominal'
