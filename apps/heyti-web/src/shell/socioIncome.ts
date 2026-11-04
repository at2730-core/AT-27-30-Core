import { parseGeometry } from '../gateway/territorial.geometry'
import type { TerritorialGeometry } from '../gateway/territorial.geometry'
import type { UniverseMap } from '../gateway/universe.client'
export const INCOME_BANDS = [
 {label:'Muy bajo',range:'Menos de $35,000',color:'#edf8fb'},
 {label:'Bajo',range:'$35,000 a menos de $45,000',color:'#b2e2e2'},
 {label:'Medio',range:'$45,000 a menos de $60,000',color:'#66c2a4'},
 {label:'Alto',range:'$60,000 a menos de $80,000',color:'#2ca25f'},
 {label:'Muy alto',range:'$80,000 o más',color:'#006d2c'},
] as const
export interface IncomeRow {id:string;name:string;estimate:number|null;standardError:number|null;lower:number|null;upper:number|null;cv:number|null}
export interface IncomeData {rows:Record<string,IncomeRow>;areas:{id:string;name:string;geometry:TerritorialGeometry}[];sectionLinks:Record<string,string[]>;sourceZipSha256:string}
const invalid=():never=>{throw new Error('Fuente de ingresos o cartografía inválida. Comprueba los archivos de esta actualización.')}
function record(v:unknown):Record<string,unknown>{if(!v||typeof v!=='object'||Array.isArray(v))return invalid();return v as Record<string,unknown>}
export function parseIncomeNumber(v:unknown):number|null{
 if(v===null||v===undefined||v==='')return null
 if(typeof v!=='string'||! /^(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?$/.test(v))return invalid()
 const n=Number(v.replaceAll(',',''));if(!Number.isFinite(n)||n<0)return invalid();return n
}
export function incomeBand(v:number|null|undefined):number|null{
 if(v==null)return null
 if(!Number.isFinite(v)||v<0) return invalid()
 return v<35000?0:v<45000?1:v<60000?2:v<80000?3:4
}
export function incomePrecision(cv:number|null):string{
 if(cv===null)return 'N/D'
 if(!Number.isFinite(cv)||cv<0)return invalid()
 return cv===0?'CV igual a cero':cv<15?'Alta':cv<30?'Moderada':'Baja'
}
export function parseIncome(raw:unknown):IncomeData{
 const d=record(raw)
 if(d.schema!=='HEYTI_INGRESO_ICMM_2024_1'||d.entity!=='11'||d.year!==2024||d.mapYear!==2020||d.confidence!==90||d.intersectionRule!=='positive-area; full municipality values; no apportionment')return invalid()
 for(const key of ['sourceZipSha256','sourceCsvSha256','mapZipSha256','sectionGeoJsonSha256'])if(typeof d[key]!=='string'||! /^[a-f0-9]{64}$/.test(d[key] as string))return invalid()
 if(!Array.isArray(d.statistics))return invalid()
 const names=record(d.names),rows:Record<string,IncomeRow>={},seen=new Set<string>()
 const fields=['estimate','standardError','lower','upper','cv'] as const
 for(const value of d.statistics){
  const r=record(value),id=r.cvegeo,code=r.est
  if(typeof id!=='string'||! /^11\d{3}$/.test(id)||r.cve_ent!=='11'||r.cve_mun!==id.slice(2)||typeof code!=='string'||! /^[1-5]$/.test(code)||seen.has(id+':'+code)||typeof names[id]!=='string'||!names[id])return invalid()
  seen.add(id+':'+code)
  rows[id]??={id,name:names[id] as string,estimate:null,standardError:null,lower:null,upper:null,cv:null}
  rows[id][fields[Number(code)-1]]=parseIncomeNumber(r.icpth)
 }
 for(const r of Object.values(rows)){
  if(r.lower!==null&&r.upper!==null&&r.lower>r.upper)return invalid()
  if(r.estimate!==null&&((r.lower!==null&&r.lower>r.estimate)||(r.upper!==null&&r.upper<r.estimate)))return invalid()
  // Tolerance accounts only for the rounding in the published CSV.
  if(r.estimate!==null&&r.estimate>0&&r.standardError!==null&&r.cv!==null&&Math.abs(r.standardError/r.estimate*100-r.cv)>.02)return invalid()
 }
 const geo=record(d.geography);if(geo.type!=='FeatureCollection'||!Array.isArray(geo.features))return invalid()
 const areaIds=new Set<string>()
 const areas=geo.features.map(value=>{
  const f=record(value),p=record(f.properties),id=p.id
  if(f.type!=='Feature'||typeof id!=='string'||! /^11(?!000)\d{3}$/.test(id)||areaIds.has(id)||typeof p.name!=='string'||!p.name)return invalid()
  areaIds.add(id);return {id,name:p.name,geometry:parseGeometry(f.geometry)}
 })
 const links=record(d.sectionLinks),sectionLinks:Record<string,string[]>={}
 if(Object.keys(links).length!==areas.length)return invalid()
 for(const a of areas){const list=links[a.id];if(!Array.isArray(list)||list.some(id=>typeof id!=='string'||! /^[1-9]\d*$/.test(id))||new Set(list).size!==list.length)return invalid();sectionLinks[a.id]=list as string[]}
 if(!Object.keys(rows).length)return invalid()
 return {rows,areas,sectionLinks,sourceZipSha256:d.sourceZipSha256 as string}
}
export function incomeIds(data:IncomeData,map:UniverseMap):string[]{
 if(map.universe.level==='state')return [...new Set([...data.areas.map(a=>a.id),...Object.keys(data.rows).filter(id=>id!=='11000')])].sort()
 const ids=new Set(map.sections.map(s=>s.sectionId))
 return data.areas.filter(a=>data.sectionLinks[a.id].some(id=>ids.has(id))).map(a=>a.id).sort()
}
