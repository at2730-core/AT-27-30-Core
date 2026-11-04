import { SectionTableSearch } from './SectionTableSearch'
import { useAreaSectionSource } from './AreaSectionSelection'
import { useEffect, useMemo, useRef, useState } from 'react'
import { useWorkspace } from '../platform/useWorkspace'
import { fetchUniverseCatalog, fetchUniverseMap } from '../gateway/universe.client'
import type { UniverseMap, UniverseOption } from '../gateway/universe.client'
import { FloatingInsightPanel } from './FloatingInsightPanel'
import { GeographicMap } from './GeographicMap'
import { toGeoJsonFeatureCollection } from './mapGeoJson'
import { parseSocioReference, socioLinkLabel, SOCIO_OFFICIAL_URL, SOCIO_METHOD_URL } from './socioTraceability'
import type { SocioReference } from './socioTraceability'
import { parseRural, ruralRows, ruralType, ruralSummary, ruralComparison, sectionKindLabel, SECTION_KINDS } from './socioRural'
import type { RuralData, RuralSource } from './socioRural'
import './WinScenarioTable.css'
interface Result {map:UniverseMap;data:RuralData;reference:SocioReference;source:RuralSource}
const number=(v:number|null|undefined)=>v==null?'N/D':v.toLocaleString('es-MX',{maximumFractionDigits:2})
export function SocioRuralWorkspace({requestId=0}:{requestId?:number}){
 const {state,selectUniverse}=useWorkspace()
 const [catalog,setCatalog]=useState<UniverseOption[]>([])
 const [choice,setChoice]=useState(state.universe&&state.universe.level!=='section'?state.universe.level+':'+state.universe.id:'state:11')
 const [source,setSource]=useState<RuralSource>('census')
 const [result,setResult]=useState<Result|null>(null),[loading,setLoading]=useState(false),[error,setError]=useState<string|null>(null),[selected,setSelected]=useState<string|null>(null),[expanded,setExpanded]=useState(true)
 const controller=useRef<AbortController|null>(null)
 useEffect(()=>{setExpanded(true)},[requestId])
 useEffect(()=>{const abort=new AbortController();fetchUniverseCatalog(abort.signal).then(setCatalog).catch(e=>{if(!abort.signal.aborted)setError(e instanceof Error?e.message:'Catálogo no disponible.')});return()=>{abort.abort();controller.current?.abort()}},[])
 async function query(){
  const universe=catalog.find(u=>u.level+':'+u.id===choice);if(!universe){setError('Selecciona un universo disponible.');return}
  controller.current?.abort();const abort=new AbortController();controller.current=abort;setLoading(true);setError(null);setResult(null);setSelected(null)
  try{
   const [map,response,refResponse]=await Promise.all([fetchUniverseMap(universe,2024,'A',abort.signal),fetch(import.meta.env.BASE_URL+'data/heyti-tipo-seccion-2020.json',{signal:abort.signal}),fetch(import.meta.env.BASE_URL+'data/heyti-socioeconomico-referencia-2020.json',{signal:abort.signal})])
   if(!response.ok||!refResponse.ok)throw new Error('Tipo de sección o referencia no disponible. Comprueba que se copiaron todos los archivos de datos de esta actualización.')
   const [raw,rawRef]=await Promise.all([response.json(),refResponse.json()])
   const reference=parseSocioReference(rawRef),data=parseRural(raw,reference)
   if(abort.signal.aborted)return
   setResult({map,data,reference,source});selectUniverse({id:map.universe.id,label:map.universe.label,level:map.universe.level,parentId:map.universe.level==='state'?null:'11',truthStatus:'pending'})
  }catch(e){if(!abort.signal.aborted)setError(e instanceof Error?e.message:'Consulta no disponible.')}finally{if(!abort.signal.aborted)setLoading(false)}
 }
 const rows=useMemo(()=>result?ruralRows(result.map,result.data):[],[result])
 const summary=useMemo(()=>ruralSummary(rows,result?.source??source),[rows,result,source])
 const byId=useMemo(()=>Object.fromEntries(rows.map(r=>[r.id,r])),[rows])
 const activeSource=result?.source??source
 const sourceLabel=activeSource==='census'?'INEGI/INE · Censo 2020':'Archivo territorial de V2 · fecha no acreditada'
 const geo=useMemo(()=>{
  if(!result)return null
  const collection=toGeoJsonFeatureCollection(result.map.sections)
  for(const f of collection.features){const row=byId[f.properties.sectionId];f.properties.featureLabel='Sección '+row.id+' · '+sectionKindLabel(ruralType(row,result.source))+' · '+(result.source==='census'?'Censo 2020':'Archivo territorial V2, fecha no acreditada')}
  return collection
 },[result,byId])
 const {selectSection}=useAreaSectionSource(result?.map)
 const focus=(id:string)=>{setSelected(id);setExpanded(true);selectSection(id)}
 const chosen=selected?byId[selected]:null
 const stale=result&&(choice!==result.map.universe.level+':'+result.map.universe.id||source!==result.source)
 const comparable=rows.filter(r=>r.inMap&&r.census&&r.snapshot&&r.geometryMatch)
 const different=comparable.filter(r=>r.census!.type!==r.snapshot!.type).length
 return <main className="workspace-canvas" data-map-expanded="true"><div className="workspace-visual-grid"><section className="workspace-visual-panel" aria-labelledby="rural-map-title"><header><div><p>UNIVERSO SELECCIONADO</p><h2 id="rural-map-title">{result?.map.universe.label??state.universe?.label??'Sin selección'}</h2></div><span className="workspace-truth-status">Tipo de sección · {sourceLabel}</span></header><div className={result?'workspace-visual-map':'workspace-visual-placeholder'}>{result&&geo?<figure className="section-geometry-map"><GeographicMap data={geo} mapAriaLabel="Mapa base con secciones urbanas, mixtas y rurales" showSectionLabels selectedSection={selected} onSelectSection={focus} style={feature=>{const id=String(feature?.properties?.sectionId??''),row=byId[id],kind=row?ruralType(row,result.source):null;return {fillColor:SECTION_KINDS.find(k=>k.code===kind)?.color??'#94a3b8',fillOpacity:kind===null?.22:.43,color:selected===id?'#111827':'#64748b',weight:selected===id?3:.8}}}/><figcaption><strong>Urbana, mixta y rural: categorías del tipo de sección. Colores para distinguir categorías. Gris = sin clasificación utilizable de la fuente elegida. Enlace censal por clave; equivalencia de límites pendiente.</strong></figcaption></figure>:<><strong>{loading?'Consultando clasificación y geometrías…':'Tipo urbano-rural · secciones'}</strong><small>Selecciona universo y fuente y pulsa Consultar tipo de sección.</small></>}</div></section>
 {expanded?<FloatingInsightPanel title="Tipo urbano-rural · secciones electorales" comparative onClose={()=>setExpanded(false)}><section style={{padding:'20px 16px'}}><p>Clasificación territorial en tres categorías: urbana (código 2), mixta (3) y rural (4). Los códigos identifican categorías y no son una puntuación. Una sección mixta reúne localidades urbanas y rurales; este dato no indica cómo se reparte su población entre ambos ámbitos.</p>
 <label className="workspace-electoral-comparison-control"><span>Universo</span><select value={choice} disabled={loading||!catalog.length} onChange={e=>setChoice(e.target.value)}>{catalog.map(u=><option key={u.level+':'+u.id} value={u.level+':'+u.id}>{u.label}</option>)}</select></label>
 <label className="workspace-electoral-comparison-control"><span>Fuente para colorear el mapa</span><select value={source} disabled={loading} onChange={e=>setSource(e.target.value as RuralSource)}><option value="census">INEGI/INE · Censo 2020 · cartografía enero 2021</option><option value="snapshot">Archivo territorial aportado de V2 · fecha no acreditada</option></select></label>
 <button type="button" className="workspace-action" disabled={loading||!catalog.length} onClick={()=>void query()}>{loading?'Consultando…':'Consultar tipo de sección y pintar mapa'}</button>
 {error?<p role="alert">{error}</p>:null}{stale?<p role="status">Cambió la selección. Tabla y mapa conservan la consulta anterior hasta volver a consultar.</p>:null}
 {result?<><h3>{result.map.universe.label} · {sourceLabel}</h3><p>{summary.represented} secciones representadas: {summary.known} con tipo utilizable y {summary.missing} N/D para la fuente elegida. {result.map.coverage.blocked} geometrías bloqueadas no representadas.</p>
 <ul style={{listStyle:'none',padding:0}}>{summary.bands.map(b=><li key={b.code} style={{margin:'10px 0'}}><span aria-hidden="true" style={{display:'inline-block',width:14,height:14,background:b.color,marginRight:8}}/>{b.label}: {b.count} secciones · {number(b.percent)}{b.percent===null?'':'% de las secciones con tipo disponible'}</li>)}</ul>
 <p className="heyti-overview-note">Los porcentajes cuentan secciones de la fuente elegida. No representan el porcentaje de personas que vive en localidades urbanas o rurales. No se reparte la población de secciones mixtas.</p>
 <p>Cotejo entre fuentes en {comparable.length} claves representadas: {comparable.length-different} con el mismo código y {different} con clasificaciones distintas. Son diferencias entre registros; no demuestran por sí solas un proceso de urbanización o un cambio histórico.</p>
 <p>Clasificación censal: Censo 2020, cartografía electoral de enero de 2021. Se conserva por clave, con equivalencia de límites pendiente. Clasificación del archivo V2: se conserva como dato de ese archivo; su fecha oficial no está acreditada. Para usarla en el mapa se coteja la geometría del CORE con la del archivo aportado. Una geometría distinta queda N/D en esa vista y mantiene el tipo original visible en la tabla.</p>
 {summary.withoutGeometry?<p>La consulta estatal conserva además {summary.withoutGeometry} registros censales ausentes del archivo territorial de referencia. Se muestran en la tabla como «Sin geometría en esta consulta» y quedan fuera del mapa y de los porcentajes anteriores.</p>:null}
 <SectionTableSearch><div className="heyti-win-table-scroll"><table className="heyti-win-table heyti-section-table" style={{minWidth:1600}}><caption>Todas las secciones de la consulta. Selecciona una clave para ver el detalle y acercar el mapa cuando tenga geometría.</caption><thead><tr><th>Sección</th><th>Tipo Censo 2020</th><th>Tipo del archivo V2</th><th>Cotejo de tipos</th><th>Población total Censo 2020</th><th>Municipio en fuente 2020</th><th>DF en fuente 2020</th><th>Geometría vs archivo V2</th><th>Correspondencia territorial</th></tr></thead><tbody>{rows.map(r=><tr data-section-id={r.id} key={r.id} aria-selected={selected===r.id}><td><button type="button" onClick={()=>focus(r.id)}>{r.id}</button></td><td>{sectionKindLabel(r.census?.type)}{r.census?' · código '+r.census.type:''}</td><td>{sectionKindLabel(r.snapshot?.type)}{r.snapshot?' · código '+r.snapshot.type:''}</td><td>{ruralComparison(r)}</td><td>{number(r.census?.population)}</td><td>{r.census?r.census.municipalityName+' · '+r.census.municipality:'N/D'}</td><td>{r.census?.district??'N/D'}</td><td>{!r.inMap?'Sin geometría en esta consulta':r.geometryMatch===null?'Sin registro en archivo V2':r.geometryMatch?'Coincide con el archivo aportado':'Difiere; tipo del archivo no aplicado al mapa'}</td><td>{r.inMap?socioLinkLabel(r.id,result.reference):'Registro censal sin polígono en esta consulta'}</td></tr>)}</tbody></table></div></SectionTableSearch>
 {chosen?<section className="heyti-data-panel-detail"><h3>Sección {chosen.id} · detalle</h3><dl><div><dt>Clasificación en Censo 2020</dt><dd>{sectionKindLabel(chosen.census?.type)}</dd></div><div><dt>Clasificación original del archivo territorial V2</dt><dd>{sectionKindLabel(chosen.snapshot?.type)} · fecha no acreditada</dd></div><div><dt>Población total de la sección en Censo 2020</dt><dd>{number(chosen.census?.population)} personas</dd></div><div><dt>Comparación</dt><dd>{ruralComparison(chosen)}</dd></div></dl><p>{chosen.inMap?socioLinkLabel(chosen.id,result.reference):'Sin geometría en esta consulta. Se conserva el registro censal, sin reconstruir un polígono ni asignarlo a un distrito actual.'}</p></section>:null}
 <p>Se conserva la población como contexto por sección; no se presenta una tasa de urbanización ni un índice de bienestar. Secciones nuevas sin registro propio de 2020 permanecen sin clasificación censal, incluso cuando exista un origen documentado.</p>
 <p><a href={SOCIO_OFFICIAL_URL} target="_blank" rel="noreferrer">INEGI/INE · fuente geoelectoral 2020</a> · <a href={SOCIO_METHOD_URL} target="_blank" rel="noreferrer">Metodología y corte cartográfico</a></p>
 </>:null}</section></FloatingInsightPanel>:<button type="button" className="workspace-action" style={{position:'fixed',right:16,bottom:16,zIndex:30}} onClick={()=>setExpanded(true)}>Expandir tipo urbano-rural</button>}
 </div></main>
}
