import { parseGeometry } from '../gateway/territorial.geometry'
import type { TerritorialGeometry } from '../gateway/territorial.geometry'
import type { UniverseMap } from '../gateway/universe.client'
export const MARGINATION_GRADES = ['Muy bajo','Bajo','Medio','Alto','Muy alto'] as const
export type MarginationGrade = typeof MARGINATION_GRADES[number]
export const MARGINATION_COLORS = ['#edf8e9','#bae4b3','#74c476','#31a354','#006d2c']
export const MARGINATION_METRICS = [
 ['P6A14NAE','Población de 6 a 14 años que no asiste a la escuela'],
 ['SBASC','Población de 15 años o más sin educación básica'],
 ['PSDSS','Población sin derechohabiencia a servicios de salud'],
 ['OVSDE','Ocupantes en viviendas sin drenaje ni excusado'],
 ['OVSEE','Ocupantes en viviendas sin energía eléctrica'],
 ['OVSAE','Ocupantes en viviendas sin agua entubada'],
 ['OVPT','Ocupantes en viviendas con piso de tierra'],
 ['OVSREF','Ocupantes en viviendas sin refrigerador'],
 ['OVSINT','Ocupantes en viviendas sin internet'],
 ['OVSCEL','Ocupantes en viviendas sin celular'],
 ['OVHAC','Ocupantes en viviendas con hacinamiento'],
] as const
export interface MarginationRow {
 CVE_AGEB:string; ENT:string; NOM_ENT:string; MUN:string; NOM_MUN:string; LOC:string; NOM_LOC:string; AGEB:string;
 POB_TOTAL:number; IM_2020:number; GM_2020:MarginationGrade; IMN_2020:number;
 [key:string]:string|number
}
export interface MarginationArea {id:string;geometry:TerritorialGeometry}
export interface MarginationData {
 rows:Record<string,MarginationRow>; areas:MarginationArea[]; sectionLinks:Record<string,string[]>;
 xlsSha256:string;mapZipSha256:string;sectionGeoJsonSha256:string
}
const invalid=():never=>{throw new Error('Base o cartografía de marginación no válida. Revisa los archivos de la actualización.')}
function record(v:unknown):Record<string,unknown>{if(!v||typeof v!=='object'||Array.isArray(v))return invalid();return v as Record<string,unknown>}
function text(v:unknown):string{if(typeof v!=='string'||!v)return invalid();return v}
function numeric(v:unknown,min:number,max=Infinity):number{if(typeof v!=='number'||!Number.isFinite(v)||v<min||v>max)return invalid();return v}
export function parseMargination(raw:unknown):MarginationData{
 const d=record(raw)
 if(d.schema!=='HEYTI_MARGINACION_2020_1'||d.entity!=='11'||d.year!==2020||d.intersectionRule!=='positive-area; full AGEB values; no apportionment')return invalid()
 const hashes=['xlsSha256','mapZipSha256','sectionGeoJsonSha256'].map(k=>text(d[k]))
 if(hashes.some(h=>! /^[a-f0-9]{64}$/.test(h)))return invalid()
 if(!Array.isArray(d.rows)||!Array.isArray(record(d.geography).features)||record(d.geography).type!=='FeatureCollection')return invalid()
 const rows:Record<string,MarginationRow>={}
 for(const value of d.rows){
  const row=record(value),id=text(row.CVE_AGEB)
  if(!/^11\d{7}[0-9A-Z]{4}$/.test(id)||rows[id]||row.ENT!=='11'||row.MUN!==id.slice(2,5)||row.LOC!==id.slice(5,9)||row.AGEB!==id.slice(9)||!MARGINATION_GRADES.includes(row.GM_2020 as MarginationGrade))return invalid()
  for(const key of ['NOM_ENT','NOM_MUN','NOM_LOC'])text(row[key])
  if(!Number.isSafeInteger(numeric(row.POB_TOTAL,0)))return invalid()
  numeric(row.IM_2020,0);numeric(row.IMN_2020,0,1)
  for(const [key] of MARGINATION_METRICS)numeric(row[key],0,100)
  rows[id]=row as unknown as MarginationRow
 }
 const seen=new Set<string>()
 const areas=(record(d.geography).features as unknown[]).map(value=>{
  const f=record(value),p=record(f.properties),id=text(p.id)
  if(f.type!=='Feature'||!/^11\d{7}[0-9A-Z]{4}$/.test(id)||seen.has(id)||p.municipality!==id.slice(2,5)||p.locality!==id.slice(5,9)||p.ageb!==id.slice(9))return invalid()
  seen.add(id)
  return {id,geometry:parseGeometry(f.geometry)}
 })
 const sourceLinks=record(d.sectionLinks),sectionLinks:Record<string,string[]>={}
 if(Object.keys(sourceLinks).length!==areas.length)return invalid()
 for(const a of areas){const links=sourceLinks[a.id];if(!Array.isArray(links)||links.some(s=>typeof s!=='string'||! /^[1-9]\d*$/.test(s))||new Set(links).size!==links.length)return invalid();sectionLinks[a.id]=links as string[]}
 return {rows,areas,sectionLinks,xlsSha256:hashes[0],mapZipSha256:hashes[1],sectionGeoJsonSha256:hashes[2]}
}
export function marginationIds(data:MarginationData,map:UniverseMap):string[]{
 if(map.universe.level==='state')return [...new Set([...data.areas.map(a=>a.id),...Object.keys(data.rows)])].sort()
 const sections=new Set(map.sections.map(s=>s.sectionId))
 return data.areas.filter(a=>data.sectionLinks[a.id].some(id=>sections.has(id))).map(a=>a.id).sort()
}
export function marginationColor(row?:MarginationRow):string{return row?MARGINATION_COLORS[MARGINATION_GRADES.indexOf(row.GM_2020)]:'#94a3b8'}
