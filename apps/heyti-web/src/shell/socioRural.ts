import type { TerritorialGeometry } from '../gateway/territorial.geometry'
import type { UniverseMap } from '../gateway/universe.client'
import type { SocioReference } from './socioTraceability'
export const SECTION_KINDS = [
 {code:'2',label:'Urbana',color:'#00897b'},
 {code:'3',label:'Mixta',color:'#8b5cf6'},
 {code:'4',label:'Rural',color:'#a16207'},
] as const
export type SectionKind = typeof SECTION_KINDS[number]['code']
export type RuralSource = 'census'|'snapshot'
export interface RuralCensus {type:SectionKind;population:number;district:string;municipality:string;municipalityName:string}
export interface RuralSnapshot {type:SectionKind;geometryFingerprint:string}
export interface RuralData {census:Record<string,RuralCensus>;snapshot:Record<string,RuralSnapshot>;snapshotGeoJsonSha256:string}
export interface RuralRow {id:string;inMap:boolean;census:RuralCensus|null;snapshot:RuralSnapshot|null;geometryMatch:boolean|null}
const invalid=():never=>{throw new Error('Fuente del tipo de sección no compatible. Comprueba los archivos de datos de la actualización.')}
function record(v:unknown):Record<string,unknown>{if(!v||typeof v!=='object'||Array.isArray(v))return invalid();return v as Record<string,unknown>}
const isId=(v:unknown):v is string=>typeof v==='string'&&/^[1-9]\d*$/.test(v)
const isKind=(v:unknown):v is SectionKind=>v==='2'||v==='3'||v==='4'
export function sectionKindLabel(kind:SectionKind|null|undefined):string{return SECTION_KINDS.find(k=>k.code===kind)?.label??'N/D'}
export function geometryFingerprint(geometry:TerritorialGeometry):string{
 let hash=2166136261
 const buffer=new DataView(new ArrayBuffer(8))
 const byte=(v:number)=>{hash=Math.imul(hash^v,16777619)>>>0}
 function walk(value:unknown){
  if(Array.isArray(value)){byte(91);for(const item of value)walk(item);byte(93)}
  else{if(typeof value!=='number'||!Number.isFinite(value))return invalid();buffer.setFloat64(0,value,false);for(let i=0;i<8;i++)byte(buffer.getUint8(i))}
 }
 for(const char of geometry.type)byte(char.charCodeAt(0))
 walk(geometry.coordinates)
 return hash.toString(16).padStart(8,'0')
}
export function parseRural(raw:unknown,reference:SocioReference):RuralData{
 const d=record(raw),classification=record(d.classification)
 if(d.schema!=='HEYTI_TIPO_SECCION_2020_1'||d.entity!=='11'||d.censusYear!==2020||d.censusMapCut!=='2021-01'||d.snapshotDate!==null||d.officialCsvSha256!==reference.officialCsvSha256||SECTION_KINDS.some(k=>classification[k.code]!==k.label))return invalid()
 for(const key of ['officialCsvSha256','catalogSha256','snapshotGeoJsonSha256'])if(typeof d[key]!=='string'||! /^[a-f0-9]{64}$/.test(d[key] as string))return invalid()
 const census:Record<string,RuralCensus>={}
 for(const [id,value] of Object.entries(record(d.census))){
  const r=record(value),ref=reference.sections[id]
  if(!isId(id)||!isKind(r.type)||!ref||typeof r.population!=='number'||!Number.isSafeInteger(r.population)||r.population<0||r.population!==ref.values.POB_TOTAL||r.district!==ref.district||r.municipality!==ref.municipality||typeof r.municipalityName!=='string'||!r.municipalityName)return invalid()
  census[id]={type:r.type,population:r.population,district:r.district as string,municipality:r.municipality as string,municipalityName:r.municipalityName}
 }
 if(Object.keys(census).length!==Object.keys(reference.sections).length)return invalid()
 const snapshot:Record<string,RuralSnapshot>={}
 for(const [id,value] of Object.entries(record(d.snapshot))){const r=record(value);if(!isId(id)||!isKind(r.type)||typeof r.geometryFingerprint!=='string'||! /^[a-f0-9]{8}$/.test(r.geometryFingerprint))return invalid();snapshot[id]={type:r.type,geometryFingerprint:r.geometryFingerprint}}
 if(!Object.keys(snapshot).length)return invalid()
 return {census,snapshot,snapshotGeoJsonSha256:d.snapshotGeoJsonSha256 as string}
}
export function ruralRows(map:UniverseMap,data:RuralData):RuralRow[]{
 const rows: RuralRow[]=map.sections.map(s=>({id:s.sectionId,inMap:true,census:data.census[s.sectionId]??null,snapshot:data.snapshot[s.sectionId]??null,geometryMatch:data.snapshot[s.sectionId]?geometryFingerprint(s.geometry)===data.snapshot[s.sectionId].geometryFingerprint:null}))
 if(map.universe.level==='state'){
  const represented=new Set(rows.map(r=>r.id))
  for(const id of Object.keys(data.census))if(!data.snapshot[id]&&!represented.has(id))rows.push({id,inMap:false,census:data.census[id],snapshot:null,geometryMatch:null})
 }
 return rows.sort((a,b)=>Number(a.id)-Number(b.id))
}
export function ruralType(row:RuralRow,source:RuralSource):SectionKind|null{return source==='census'?row.census?.type??null:row.geometryMatch?row.snapshot?.type??null:null}
export function ruralComparison(row:RuralRow):string{
 if(!row.census)return 'Sin registro censal 2020'
 if(!row.snapshot)return 'Sin registro en archivo territorial V2'
 if(!row.geometryMatch)return 'Cotejo geométrico pendiente'
 return row.census.type===row.snapshot.type?'Coinciden códigos':'Clasificaciones distintas'
}
export function ruralSummary(rows:RuralRow[],source:RuralSource){
 const represented=rows.filter(r=>r.inMap),known=represented.filter(r=>ruralType(r,source)!==null).length
 return {represented:represented.length,known,missing:represented.length-known,withoutGeometry:rows.length-represented.length,bands:SECTION_KINDS.map(k=>{
  const count=represented.filter(r=>ruralType(r,source)===k.code).length
  return {...k,count,percent:known?count*100/known:null}
 })}
}
