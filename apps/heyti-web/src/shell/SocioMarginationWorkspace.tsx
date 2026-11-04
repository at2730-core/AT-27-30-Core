import { GeographicDataScope } from './DataScopeNotes'
import { useEffect, useMemo, useRef, useState } from 'react'
import { useWorkspace } from '../platform/useWorkspace'
import { fetchUniverseCatalog, fetchUniverseMap } from '../gateway/universe.client'
import type { UniverseMap, UniverseOption } from '../gateway/universe.client'
import { FloatingInsightPanel } from './FloatingInsightPanel'
import { GeographicMap } from './GeographicMap'
import { toGeoJsonFeatureCollection } from './mapGeoJson'
import type { GeoJsonFeatureCollection } from './mapGeoJson'
import { parseMargination, marginationIds, marginationColor, MARGINATION_GRADES, MARGINATION_COLORS, MARGINATION_METRICS } from './socioMargination'
import type { MarginationData } from './socioMargination'
import './WinScenarioTable.css'
interface Result { map:UniverseMap; data:MarginationData }
const num=(n:unknown)=>typeof n==='number'?n.toLocaleString('es-MX',{maximumFractionDigits:3}):'N/D'
const source='https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372'
export function SocioMarginationWorkspace({requestId=0}:{requestId?:number}){
 const {state,selectUniverse}=useWorkspace()
 const [catalog,setCatalog]=useState<UniverseOption[]>([])
 const [choice,setChoice]=useState(state.universe&&state.universe.level!=='section'?state.universe.level+':'+state.universe.id:'state:11')
 const [result,setResult]=useState<Result|null>(null),[loading,setLoading]=useState(false),[error,setError]=useState<string|null>(null),[selected,setSelected]=useState<string|null>(null),[expanded,setExpanded]=useState(true),[showSections,setShowSections]=useState(true)
 const controller=useRef<AbortController|null>(null)
 useEffect(()=>{setExpanded(true)},[requestId])
 useEffect(()=>{const abort=new AbortController();fetchUniverseCatalog(abort.signal).then(setCatalog).catch(e=>{if(!abort.signal.aborted)setError(e instanceof Error?e.message:'Catálogo no disponible.')});return()=>{abort.abort();controller.current?.abort()}},[])
 async function query(){
  const universe=catalog.find(u=>u.level+':'+u.id===choice);if(!universe){setError('Selecciona un universo disponible.');return}
  controller.current?.abort();const abort=new AbortController();controller.current=abort;setLoading(true);setError(null);setResult(null);setSelected(null)
  try{
   const [map,response]=await Promise.all([fetchUniverseMap(universe,2024,'A',abort.signal),fetch(import.meta.env.BASE_URL+'data/heyti-marginacion-urbana-2020.json',{signal:abort.signal})])
   if(!response.ok)throw new Error('Base de marginación no disponible. Comprueba que copiaste los archivos de datos de esta actualización.')
   const data=parseMargination(await response.json());if(abort.signal.aborted)return
   setResult({map,data});selectUniverse({id:map.universe.id,label:map.universe.label,level:map.universe.level,parentId:map.universe.level==='state'?null:'11',truthStatus:'pending'})
  }catch(e){if(!abort.signal.aborted)setError(e instanceof Error?e.message:'Consulta no disponible.')}finally{if(!abort.signal.aborted)setLoading(false)}
 }
 const ids=useMemo(()=>result?marginationIds(result.data,result.map):[],[result])
 const idSet=useMemo(()=>new Set(ids),[ids])
 const areaSet=useMemo(()=>new Set(result?.data.areas.map(a=>a.id)??[]),[result])
 const names=useMemo(()=>{
  const municipalities:Record<string,string>={},localities:Record<string,string>={}
  for(const r of Object.values(result?.data.rows??{})){municipalities[r.CVE_AGEB.slice(0,5)]=r.NOM_MUN;localities[r.CVE_AGEB.slice(0,9)]=r.NOM_LOC}
  return {municipalities,localities}
 },[result])
 const geo=useMemo<GeoJsonFeatureCollection>(()=>({type:'FeatureCollection',features:result?result.data.areas.filter(a=>idSet.has(a.id)).map(a=>({type:'Feature',geometry:a.geometry,properties:{sectionId:a.id,status:null,leader:null,featureLabel:'AGEB '+a.id+' · '+(result.data.rows[a.id]?.GM_2020??'Sin índice disponible')+' · CONAPO 2020'}})):[]}),[result,idSet])
 const context=useMemo(()=>result?toGeoJsonFeatureCollection(result.map.sections):undefined,[result])
 const focus=(id:string)=>{setSelected(id);setExpanded(true)}
 const chosen=selected?result?.data.rows[selected]:undefined
 const withIndex=ids.filter(id=>result?.data.rows[id])
 const stale=result&&choice!==result.map.universe.level+':'+result.map.universe.id
 const currentSections=useMemo(()=>new Set(result?.map.sections.map(s=>s.sectionId)??[]),[result])
 const linkedSections=useMemo(()=>new Set(ids.flatMap(id=>result?.data.sectionLinks[id]??[]).filter(id=>currentSections.has(id))),[ids,result,currentSections])
 return <main className="workspace-canvas" data-map-expanded="true"><div className="workspace-visual-grid"><section className="workspace-visual-panel" aria-labelledby="margination-map-title"><header><div><p>UNIVERSO SELECCIONADO</p><h2 id="margination-map-title">{result?.map.universe.label??state.universe?.label??'Sin selección'}</h2></div><span className="workspace-truth-status">Marginación urbana · CONAPO 2020 · áreas geoestadísticas</span></header><div className={result?'workspace-visual-map':'workspace-visual-placeholder'}>{result?<figure className="section-geometry-map"><GeographicMap data={geo} contextData={showSections?context:undefined} mapAriaLabel="Mapa base con marginación por AGEB urbana y secciones de referencia" selectedSection={selected} onSelectSection={focus} style={feature=>{const id=String(feature?.properties?.sectionId??'');return {fillColor:marginationColor(result.data.rows[id]),fillOpacity:result.data.rows[id] ? .55:.25,color:selected===id?'#111827':'#64748b',weight:selected===id?3:.7}}}/><figcaption><strong>Unidad del dato: AGEB urbana completa · Universo de referencia: {result.map.universe.label}. Grado oficial por AGEB urbana, 2020. Oscuro = mayor grado de marginación; gris = sin índice disponible. Líneas discontinuas: secciones de referencia. Fuera de las AGEB mostradas no se asigna grado.</strong></figcaption></figure>:<><strong>{loading?'Consultando marginación y cartografía…':'Marginación urbana · CONAPO 2020'}</strong><small>Selecciona un universo y pulsa Consultar marginación.</small></>}</div></section>
 {expanded?<FloatingInsightPanel title="Marginación urbana · CONAPO 2020" comparative onClose={()=>setExpanded(false)}><section style={{padding:'20px 16px'}}><p>El Área Geoestadística Básica (AGEB) es la unidad de esta consulta. Se conservan los índices y grados publicados por CONAPO con base en el Censo 2020 y los límites geoestadísticos del INEGI de ese año.</p>
 <label className="workspace-electoral-comparison-control"><span>Universo de referencia</span><select value={choice} disabled={loading||!catalog.length} onChange={e=>setChoice(e.target.value)}>{catalog.map(u=><option key={u.level+':'+u.id} value={u.level+':'+u.id}>{u.label}</option>)}</select></label>
 <button type="button" className="workspace-action" disabled={loading||!catalog.length} onClick={()=>void query()}>{loading?'Consultando…':'Consultar marginación y pintar mapa'}</button>
 <label style={{display:'block',margin:'12px 0'}}><input type="checkbox" checked={showSections} onChange={e=>setShowSections(e.target.checked)}/> Mostrar límites de secciones electorales como referencia</label>
 {error?<p role="alert">{error}</p>:null}{stale?<p role="status">Cambió el universo. La consulta anterior se conserva hasta volver a consultar.</p>:null}
 {result?<><h3>{result.map.universe.label} · cobertura urbana 2020</h3><GeographicDataScope universe={result.map.universe.label} unit="AGEB urbana completa" year={2020} source="CONAPO" /><p>{ids.length.toLocaleString('es-MX')} AGEB en la tabla: {withIndex.length.toLocaleString('es-MX')} con índice y {(ids.length-withIndex.length).toLocaleString('es-MX')} sin índice disponible. {ids.filter(id=>!areaSet.has(id)).length} registros sin geometría. {result.map.coverage.blocked} secciones bloqueadas no usadas en el cruce.</p>
 <p>{result.map.universe.level==='state'?'Se muestran todas las AGEB urbanas del archivo de Guanajuato.':'Se incluyen AGEB con intersección de superficie positiva con alguna sección representada del universo. Una AGEB puede cruzar límites y aparecer en varios universos.'} Se muestra la AGEB completa y sus cifras completas de 2020. El cruce espacial orienta la consulta; no certifica equivalencia de límites ni produce un índice por sección o distrito.</p>
 <ul style={{listStyle:'none',padding:0}}>{MARGINATION_GRADES.map((grade,i)=><li key={grade} style={{margin:'8px 0'}}><span aria-hidden="true" style={{display:'inline-block',width:14,height:14,background:MARGINATION_COLORS[i],marginRight:8}}/>{grade}: {ids.filter(id=>result.data.rows[id]?.GM_2020===grade).length} AGEB</li>)}<li>Gris: sin índice disponible. Los grados son los publicados por CONAPO; no se sustituyen por cuantiles locales.</li></ul>
 <p className="heyti-overview-note">Cobertura rural: este producto mide AGEB urbanas. Las zonas rurales requieren otra fuente y escala. {result.map.sections.length-linkedSections.size} secciones representadas sin cruce con AGEB de esta capa; esto no demuestra que sean rurales. No se rellenan vacíos con el promedio municipal ni con cero.</p>
 <div className="heyti-win-table-scroll"><table className="heyti-win-table" style={{minWidth:2500}}><caption>Todas las AGEB de la consulta. Selecciona una clave para acercar el mapa y ver su ficha. Porcentajes publicados, sin sumar columnas.</caption><thead><tr><th>Clave completa AGEB</th><th>Municipio</th><th>Localidad</th><th>Población 2020 · personas</th><th>Grado oficial</th><th>Índice IM 2020</th><th>Índice normalizado</th><th>Estado</th>{MARGINATION_METRICS.map(([key,label])=><th key={key}>{label} · %</th>)}</tr></thead><tbody>{ids.map(id=>{const r=result.data.rows[id];return <tr key={id} aria-selected={selected===id}><td><button type="button" onClick={()=>focus(id)}>{id}</button></td><td>{r?.NOM_MUN??names.municipalities[id.slice(0,5)]??'N/D'} · {id.slice(2,5)}</td><td>{r?.NOM_LOC??names.localities[id.slice(0,9)]??'Nombre no disponible'} · {id.slice(5,9)}</td><td>{num(r?.POB_TOTAL)}</td><td>{r?.GM_2020??'N/D'}</td><td>{num(r?.IM_2020)}</td><td>{num(r?.IMN_2020)}</td><td>{r?(areaSet.has(id)?'Índice publicado · geometría enlazada por clave':'Índice publicado · sin geometría'):'Geometría disponible · sin registro en esta base'}</td>{MARGINATION_METRICS.map(([key])=><td key={key}>{num(r?.[key])}</td>)}</tr>})}</tbody></table></div>
 {selected?<section className="heyti-data-panel-detail"><h3>AGEB {selected} · detalle 2020</h3><p>{chosen?chosen.NOM_MUN+' · '+chosen.NOM_LOC+' · grado '+chosen.GM_2020:'Sin índice disponible en la base de CONAPO proporcionada. No se infiere la causa.'}</p><dl>{chosen?Object.entries(chosen).map(([key,value])=><div key={key} style={{margin:'8px 0'}}><dt>{key}</dt><dd>{typeof value==='number'?num(value):value}</dd></div>):null}</dl><p>Secciones de referencia con cruce espacial en este universo: {(result.data.sectionLinks[selected]??[]).filter(id=>currentSections.has(id)).join(', ')||'Ninguna'}. Estos números no convierten el índice de la AGEB en un índice de sección.</p></section>:null}
 <p>Los porcentajes tienen diferentes poblaciones de referencia, indicadas en cada encabezado. El archivo publica porcentajes, no los denominadores necesarios para agregarlos: no se calculan tasas conjuntas ni promedios de índices. La población corresponde a cada AGEB completa, incluso si cruza un límite del universo.</p>
 <p><a href={source} target="_blank" rel="noreferrer">CONAPO · fuente y metodología 2020</a> · <a href="https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=889463807469" target="_blank" rel="noreferrer">INEGI · cartografía del Censo 2020</a></p>
 </>:null}</section></FloatingInsightPanel>:<button type="button" className="workspace-action" style={{position:'fixed',right:16,bottom:16,zIndex:30}} onClick={()=>setExpanded(true)}>Expandir marginación urbana</button>}
 </div></main>
}
