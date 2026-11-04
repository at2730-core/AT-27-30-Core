import { parseGeometry } from '../gateway/territorial.geometry'
import type { TerritorialGeometry } from '../gateway/territorial.geometry'
import type { UniverseMap } from '../gateway/universe.client'
export const POVERTY_YEARS = [2010,2015,2020] as const
export type PovertyYear = typeof POVERTY_YEARS[number]
export type PovertyMode = 'urban'|'municipal'
export const POVERTY_KEYS = ['poverty','extreme','moderate','vulnerable_social','vulnerable_income','not_poor','education','health','social_security','housing','services','food','one_deprivation','three_deprivations','income_poverty','income_extreme'] as const
export type PovertyKey = typeof POVERTY_KEYS[number]
export const POVERTY_METRICS = POVERTY_KEYS.map((key,i)=>({key,label:[
 'Pobreza','Pobreza extrema','Pobreza moderada','Vulnerables por carencia social','Vulnerables por ingreso','No pobre y no vulnerable','Rezago educativo','Carencia por acceso a los servicios de salud','Carencia por acceso a la seguridad social','Carencia por calidad y espacios de la vivienda','Carencia por acceso a los servicios básicos en la vivienda','Carencia por acceso a la alimentación','Población con al menos una carencia social','Población con tres o más carencias sociales','Población con ingreso inferior a la línea de pobreza por ingresos','Población con ingreso inferior a la línea de pobreza extrema por ingresos'
][i]}))
export type PovertyValue = number|'n.d.'|'n.a.'|null
export interface PovertyMeasure {percent:PovertyValue;persons:PovertyValue;deprivations:PovertyValue}
export interface PovertyMunicipality {id:string;name:string;years:Record<PovertyYear,{population:PovertyValue;indicators:Record<PovertyKey,PovertyMeasure>}>}
export interface PovertyLocality {id:string;municipalityId:string;municipality:string;name:string;population:PovertyValue;range:string|null}
interface PovertyArea {id:string;name:string;geometry:TerritorialGeometry;cartographicScope:string|null}
export interface PovertyData {
 metrics:{key:PovertyKey;label:string}[];municipalRows:Record<string,PovertyMunicipality>;stateRow:PovertyMunicipality;urbanRows:Record<string,PovertyLocality>;
 municipalAreas:PovertyArea[];urbanAreas:PovertyArea[];municipalLinks:Record<string,string[]>;urbanLinks:Record<string,string[]>
}
export const POVERTY_COLORS=['#fff7bc','#fee391','#fec44f','#fe9929','#cc4c02']
export const POVERTY_RANGE_LABELS=['0% a menos de 20%','20% a menos de 40%','40% a menos de 60%','60% a menos de 80%','80% a 100%']
const invalid=():never=>{throw new Error('Fuente o cartografía de pobreza inválida. Revisa los archivos de la actualización.')}
function record(v:unknown):Record<string,unknown>{if(!v||typeof v!=='object'||Array.isArray(v))return invalid();return v as Record<string,unknown>}
function text(v:unknown):string{if(typeof v!=='string'||!v)return invalid();return v}
function value(v:unknown,unit:'percent'|'persons'|'deprivations'):PovertyValue{
 if(v===null||v==='n.d.'||v==='n.a.')return v
 if(typeof v!=='number'||!Number.isFinite(v)||v<0||(unit==='percent'&&v>100)||(unit==='deprivations'&&v>6)||(unit==='persons'&&!Number.isSafeInteger(v)))return invalid()
 return v
}
export function povertyNumber(v:PovertyValue|undefined):number|null{return typeof v==='number'?v:null}
export function povertyDisplay(v:PovertyValue|undefined,unit=''):string{
 if(v==='n.a.')return 'No aplica'
 if(v==='n.d.')return 'Sin estimación'
 return typeof v==='number'?v.toLocaleString('es-MX',{maximumFractionDigits:3})+unit:'Sin dato'
}
export function povertyBand(v:PovertyValue|undefined):number|null{
 const n=povertyNumber(v);if(n===null)return null
 if(n<0||n>100||!Number.isFinite(n))return invalid()
 return Math.min(4,Math.floor(n/20))
}
export function povertyRangeBand(v:string|null):number|null{
 if(v===null||v==='n.d.'||v==='-')return null
 const ranges=['[0,20)','[20,40)','[40,60)','[60,80)','[80,100]']
 const band=ranges.indexOf(v.replace(/\s/g,''));if(band<0)return invalid();return band
}
export function metricHasDeprivations(key:PovertyKey):boolean{return key!=='vulnerable_income'&&key!=='not_poor'}
function parseMunicipality(raw:unknown,state=false):PovertyMunicipality{
 const r=record(raw),id=text(r.id),name=text(r.name),source=record(r.years)
 if(state?id!=='11':!/^11(?!000)\d{3}$/.test(id))return invalid()
 const years={} as PovertyMunicipality['years']
 for(const year of POVERTY_YEARS){
  const y=record(source[year]),indicators=record(y.indicators),parsed={} as Record<PovertyKey,PovertyMeasure>
  for(const key of POVERTY_KEYS){const m=record(indicators[key]);parsed[key]={percent:value(m.percent,'percent'),persons:value(m.persons,'persons'),deprivations:value(m.deprivations,'deprivations')}}
  years[year]={population:value(y.population,'persons'),indicators:parsed}
 }
 return {id,name,years}
}
function parseAreas(raw:unknown,width:number):PovertyArea[]{
 const geo=record(raw);if(geo.type!=='FeatureCollection'||!Array.isArray(geo.features))return invalid()
 const seen=new Set<string>()
 return geo.features.map(raw=>{const f=record(raw),p=record(f.properties),id=text(p.id);if(f.type!=='Feature'||!new RegExp('^11[0-9]{'+(width-2)+'}$').test(id)||seen.has(id))return invalid();seen.add(id);return {id,name:text(p.name),geometry:parseGeometry(f.geometry),cartographicScope:p.cartographicScope==null?null:text(p.cartographicScope)}})
}
function parseLinks(raw:unknown,areas:PovertyArea[]):Record<string,string[]>{
 const links=record(raw),result:Record<string,string[]>={}
 if(Object.keys(links).length!==areas.length)return invalid()
 for(const a of areas){const list=links[a.id];if(!Array.isArray(list)||list.some(id=>typeof id!=='string'||! /^[1-9]\d*$/.test(id))||new Set(list).size!==list.length)return invalid();result[a.id]=list as string[]}
 return result
}
export function parsePoverty(raw:unknown):PovertyData{
 const d=record(raw)
 if(d.schema!=='HEYTI_POBREZA_CONEVAL_2020_1'||d.entity!=='11'||d.mapYear!==2020||JSON.stringify(d.years)!==JSON.stringify(POVERTY_YEARS)||d.intersectionRule!=='positive-area; complete source units; no apportionment')return invalid()
 for(const key of ['municipalZipSha256','urbanZipSha256','mapZipSha256','sectionGeoJsonSha256'])if(typeof d[key]!=='string'||! /^[a-f0-9]{64}$/.test(d[key] as string))return invalid()
 if(!Array.isArray(d.metrics)||!Array.isArray(d.municipalRows)||!Array.isArray(d.urbanRows))return invalid()
 const metrics=d.metrics.map((raw,i)=>{const m=record(raw);if(m.key!==POVERTY_KEYS[i])return invalid();return {key:m.key as PovertyKey,label:text(m.label)}})
 if(metrics.length!==16)return invalid()
 const municipalRows:Record<string,PovertyMunicipality>={}
 for(const raw of d.municipalRows){const row=parseMunicipality(raw);if(municipalRows[row.id])return invalid();municipalRows[row.id]=row}
 const urbanRows:Record<string,PovertyLocality>={}
 for(const raw of d.urbanRows){
  const r=record(raw),id=text(r.id),municipalityId=text(r.municipalityId),range=r.range===null?null:text(r.range)
  if(! /^11\d{7}$/.test(id)||municipalityId!==id.slice(0,5)||urbanRows[id])return invalid()
  povertyRangeBand(range)
  urbanRows[id]={id,municipalityId,municipality:text(r.municipality),name:text(r.name),population:value(r.population,'persons'),range}
 }
 const municipalAreas=parseAreas(d.municipalGeography,5),urbanAreas=parseAreas(d.urbanGeography,9)
 return {metrics,municipalRows,stateRow:parseMunicipality(d.stateRow,true),urbanRows,municipalAreas,urbanAreas,municipalLinks:parseLinks(d.municipalLinks,municipalAreas),urbanLinks:parseLinks(d.urbanLinks,urbanAreas)}
}
export function povertyIds(data:PovertyData,map:UniverseMap,mode:PovertyMode):string[]{
 const areas=mode==='urban'?data.urbanAreas:data.municipalAreas,links=mode==='urban'?data.urbanLinks:data.municipalLinks,rows=mode==='urban'?data.urbanRows:data.municipalRows
 if(map.universe.level==='state')return [...new Set([...areas.map(a=>a.id),...Object.keys(rows)])].sort()
 const ids=new Set(map.sections.map(s=>s.sectionId))
 return areas.filter(a=>links[a.id].some(id=>ids.has(id))).map(a=>a.id).sort()
}
