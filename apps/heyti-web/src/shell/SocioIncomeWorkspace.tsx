import { GeographicDataScope } from './DataScopeNotes'
import { useEffect, useMemo, useRef, useState } from 'react'
import { useWorkspace } from '../platform/useWorkspace'
import { fetchUniverseCatalog, fetchUniverseMap } from '../gateway/universe.client'
import type { UniverseMap, UniverseOption } from '../gateway/universe.client'
import { FloatingInsightPanel } from './FloatingInsightPanel'
import { GeographicMap } from './GeographicMap'
import { toGeoJsonFeatureCollection } from './mapGeoJson'
import type { GeoJsonFeatureCollection } from './mapGeoJson'
import { parseIncome, incomeIds, incomeBand, incomePrecision, INCOME_BANDS } from './socioIncome'
import type { IncomeData, IncomeRow } from './socioIncome'
import './WinScenarioTable.css'
interface Result {map:UniverseMap;data:IncomeData}
const money=(v:number|null|undefined)=>v==null?'N/D':v.toLocaleString('es-MX',{style:'currency',currency:'MXN',minimumFractionDigits:2,maximumFractionDigits:2})
const percent=(v:number|null|undefined)=>v==null?'N/D':v.toLocaleString('es-MX',{maximumFractionDigits:3})+'%'
function IncomeStatistics({row}:{row:IncomeRow}){
 return <dl><div><dt>Ingreso corriente promedio trimestral por hogar</dt><dd>{money(row.estimate)}</dd></div><div><dt>Intervalo de confianza al 90%</dt><dd>{money(row.lower)} a {money(row.upper)}</dd></div><div><dt>Error estándar</dt><dd>{money(row.standardError)}</dd></div><div><dt>Coeficiente de variación</dt><dd>{percent(row.cv)} · precisión {incomePrecision(row.cv)}</dd></div></dl>
}
export function SocioIncomeWorkspace({requestId=0}:{requestId?:number}){
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
   const [map,response]=await Promise.all([fetchUniverseMap(universe,2024,'A',abort.signal),fetch(import.meta.env.BASE_URL+'data/heyti-ingreso-municipal-2024.json',{signal:abort.signal})])
   if(!response.ok)throw new Error('Fuente de ingresos no disponible. Revisa los archivos de datos de la actualización.')
   const data=parseIncome(await response.json());if(abort.signal.aborted)return
   setResult({map,data});selectUniverse({id:map.universe.id,label:map.universe.label,level:map.universe.level,parentId:map.universe.level==='state'?null:'11',truthStatus:'pending'})
  }catch(e){if(!abort.signal.aborted)setError(e instanceof Error?e.message:'Consulta no disponible.')}finally{if(!abort.signal.aborted)setLoading(false)}
 }
 const ids=useMemo(()=>result?incomeIds(result.data,result.map):[],[result])
 const idSet=useMemo(()=>new Set(ids),[ids])
 const areaIds=useMemo(()=>new Set(result?.data.areas.map(a=>a.id)??[]),[result])
 const geo=useMemo<GeoJsonFeatureCollection>(()=>({type:'FeatureCollection',features:result?result.data.areas.filter(a=>idSet.has(a.id)).map(a=>({type:'Feature',geometry:a.geometry,properties:{sectionId:a.id,status:null,leader:null,featureLabel:a.name+' · '+money(result.data.rows[a.id]?.estimate)+' por hogar/trimestre · ICMM 2024'}})):[]}),[result,idSet])
 const context=useMemo(()=>result?toGeoJsonFeatureCollection(result.map.sections):undefined,[result])
 const focus=(id:string)=>{setSelected(id);setExpanded(true)}
 const chosen=selected?result?.data.rows[selected]:undefined
 const stateReference=result?.data.rows['11000']
 const stale=result&&choice!==result.map.universe.level+':'+result.map.universe.id
 const withIncome=ids.filter(id=>result?.data.rows[id]?.estimate!=null)
 return <main className="workspace-canvas" data-map-expanded="true"><div className="workspace-visual-grid"><section className="workspace-visual-panel" aria-labelledby="income-map-title"><header><div><p>UNIVERSO SELECCIONADO</p><h2 id="income-map-title">{result?.map.universe.label??state.universe?.label??'Sin selección'}</h2></div><span className="workspace-truth-status">Ingreso municipal estimado · INEGI 2024 · límites 2020</span></header><div className={result?'workspace-visual-map':'workspace-visual-placeholder'}>{result?<figure className="section-geometry-map"><GeographicMap data={geo} contextData={showSections?context:undefined} mapAriaLabel="Mapa base con ingresos estimados por municipio y secciones de referencia" selectedSection={selected} onSelectSection={focus} style={feature=>{const id=String(feature?.properties?.sectionId??''),band=incomeBand(result.data.rows[id]?.estimate);return {fillColor:band===null?'#94a3b8':INCOME_BANDS[band].color,fillOpacity:band===null?.25:.5,color:selected===id?'#111827':'#64748b',weight:selected===id?3:1}}}/><figcaption><strong>Unidad del dato: municipio completo · Universo de referencia: {result.map.universe.label}. Ingreso promedio por hogar y trimestre, pesos de la publicación 2024. Oscuro = mayor ingreso estimado; gris = N/D. Municipios completos, límites INEGI 2020. Secciones discontinuas de referencia.</strong></figcaption></figure>:<><strong>{loading?'Consultando ingresos y cartografía…':'Ingreso estimado · municipios 2024'}</strong><small>Selecciona un universo y pulsa Consultar ingresos.</small></>}</div></section>
 {expanded?<FloatingInsightPanel title="Ingreso estimado municipal · INEGI ICMM 2024" comparative onClose={()=>setExpanded(false)}><section style={{padding:'20px 16px'}}><p>Estimaciones oficiales del ingreso corriente promedio trimestral por hogar, en pesos, para municipios. Se muestran el monto, el intervalo de confianza al 90% y las medidas de precisión de la fuente. El año del ingreso es 2024; la publicación es del 28 de septiembre de 2026.</p>
 <label className="workspace-electoral-comparison-control"><span>Universo de referencia</span><select value={choice} disabled={loading||!catalog.length} onChange={e=>setChoice(e.target.value)}>{catalog.map(u=><option key={u.level+':'+u.id} value={u.level+':'+u.id}>{u.label}</option>)}</select></label>
 <button type="button" className="workspace-action" disabled={loading||!catalog.length} onClick={()=>void query()}>{loading?'Consultando…':'Consultar ingresos y pintar mapa'}</button>
 <label style={{display:'block',margin:'12px 0'}}><input type="checkbox" checked={showSections} onChange={e=>setShowSections(e.target.checked)}/> Mostrar secciones electorales como referencia</label>
 {error?<p role="alert">{error}</p>:null}{stale?<p role="status">Cambió el universo. Vuelve a consultar para actualizar el resultado.</p>:null}
 {result?<><h3>{result.map.universe.label} · contexto municipal</h3><GeographicDataScope universe={result.map.universe.label} unit="municipio completo" year={2024} source="INEGI · ICMM" /><p>{ids.length} municipios en la tabla; {withIncome.length} con estimación disponible y {ids.length-withIncome.length} N/D. {ids.filter(id=>!areaIds.has(id)).length} sin geometría. {result.map.coverage.blocked} secciones bloqueadas no usadas en el cruce.</p>
 <p>{result.map.universe.level==='state'?'Se muestran todos los municipios de Guanajuato.':'Se muestran municipios cuya superficie cruza alguna sección representada del universo. Las diferencias entre cartografías pueden producir cruces pequeños en bordes.'} El ingreso pertenece al municipio completo. No se asigna a cada sección ni se calcula un ingreso para el distrito. La delimitación municipal es del Censo 2020; su correspondencia con la geografía del ingreso 2024 sigue pendiente de conciliar.</p>
 <ul style={{listStyle:'none',padding:0}}>{INCOME_BANDS.map((band,i)=><li key={band.label} style={{margin:'8px 0'}}><span aria-hidden="true" style={{display:'inline-block',width:14,height:14,background:band.color,marginRight:8}}/>{band.label}: {band.range} por hogar/trimestre · {ids.filter(id=>incomeBand(result.data.rows[id]?.estimate)===i).length} municipios</li>)}</ul>
 <p className="heyti-overview-note">Rangos de ingreso del reporte INEGI 2024, aplicados al valor estimado. No se recalculan con los municipios seleccionados. Los intervalos pueden cruzar rangos; el color por sí solo no demuestra una diferencia estadísticamente significativa.</p>
 {stateReference?<section className="heyti-data-panel-detail"><h4>Referencia estatal publicada · Guanajuato 2024</h4><IncomeStatistics row={stateReference}/><p>Estimación estatal de la fuente, presentada por separado. No es el promedio simple de los municipios ni una estimación del universo seleccionado.</p></section>:null}
 <div className="heyti-win-table-scroll"><table className="heyti-win-table" style={{minWidth:1450}}><caption>Municipios completos. Selecciona una fila para acercar el mapa. Importes trimestrales por hogar, pesos de la publicación 2024.</caption><thead><tr><th>Clave INEGI</th><th>Municipio</th><th>Ingreso estimado · MXN/hogar/trimestre</th><th>Límite inferior · IC 90% · MXN</th><th>Límite superior · IC 90% · MXN</th><th>Error estándar · MXN</th><th>CV · %</th><th>Precisión</th><th>Estrato según rangos 2024</th><th>Estado</th></tr></thead><tbody>{ids.map(id=>{const r=result.data.rows[id],band=incomeBand(r?.estimate);return <tr key={id} aria-selected={selected===id}><td><button type="button" onClick={()=>focus(id)}>{id}</button></td><td>{r?.name??result.data.areas.find(a=>a.id===id)?.name??'Nombre no disponible'}</td><td>{money(r?.estimate)}</td><td>{money(r?.lower)}</td><td>{money(r?.upper)}</td><td>{money(r?.standardError)}</td><td>{percent(r?.cv)}</td><td>{incomePrecision(r?.cv??null)}</td><td>{band===null?'N/D':INCOME_BANDS[band].label}</td><td>{r?.estimate!=null?'Estimación publicada · límites pendientes':'Sin estimación disponible'}</td></tr>})}</tbody></table></div>
 {selected?<section className="heyti-data-panel-detail"><h3>{chosen?.name??selected} · municipio {selected}</h3>{chosen?<IncomeStatistics row={chosen}/>:<p>Sin estimación disponible en esta fuente.</p>}<p>Los valores representan al conjunto de hogares del municipio. No son el salario de una persona ni el ingreso exacto de cada hogar. No se suman ni reparten los promedios entre secciones.</p></section>:null}
 <p>Precisión según el coeficiente de variación (CV): alta, mayor que 0 y menor que 15%; moderada, de 15% a menos de 30%; baja, 30% o más. Los intervalos y errores son los publicados por INEGI, sin recalcular. Los datos no se actualizan a precios de 2026 ni se comparan aquí con años anteriores.</p>
 <p><a href="https://www.inegi.org.mx/investigacion/icmm/" target="_blank" rel="noreferrer">INEGI · datos y metodología ICMM</a> · <a href="https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/icmm/ICMM2024_RR.pdf" target="_blank" rel="noreferrer">Reporte de resultados 2024</a></p>
 </>:null}</section></FloatingInsightPanel>:<button type="button" className="workspace-action" style={{position:'fixed',right:16,bottom:16,zIndex:30}} onClick={()=>setExpanded(true)}>Expandir ingreso estimado</button>}
 </div></main>
}
