import { SectionTableSearch } from './SectionTableSearch'
import { useAreaSectionSource } from './AreaSectionSelection'
import { useEffect, useMemo, useRef, useState } from 'react'
import { useWorkspace } from '../platform/useWorkspace'
import { fetchUniverseCatalog, fetchUniverseMap } from '../gateway/universe.client'
import type { UniverseMap, UniverseOption } from '../gateway/universe.client'
import { FloatingInsightPanel } from './FloatingInsightPanel'
import { GeographicMap } from './GeographicMap'
import { toGeoJsonFeatureCollection } from './mapGeoJson'
import { parseSocioReference, socioLinkLabel, SOCIO_OFFICIAL_URL } from './socioTraceability'
import type { SocioReference } from './socioTraceability'
import { parseAnnualRate, projectionRows, projectionLabel } from './socioProjection'
import type { ProjectionMode, ProjectionRow } from './socioProjection'
import { socioBand, socioCuts, SOCIO_COLORS } from './socioeconomic'
import './WinScenarioTable.css'

interface Result {maps:UniverseMap[];reference:SocioReference;mode:ProjectionMode;rate:number|null;inputRate:string;rows:ProjectionRow[]}
const number=(v:number|null|undefined,digits=0)=>v==null?'N/D':v.toLocaleString('es-MX',{maximumFractionDigits:digits})
export function SocioProjectionWorkspace({requestId=0}:{requestId?:number}){
 const {state,selectUniverse}=useWorkspace()
 const [catalog,setCatalog]=useState<UniverseOption[]>([])
 const [choice,setChoice]=useState(state.universe&&state.universe.level!=='section'?state.universe.level+':'+state.universe.id:'state:11')
 const [mode,setMode]=useState<ProjectionMode>('ln-history'),[rate,setRate]=useState('')
 const [result,setResult]=useState<Result|null>(null),[loading,setLoading]=useState(false),[error,setError]=useState<string|null>(null),[selected,setSelected]=useState<string|null>(null),[expanded,setExpanded]=useState(true)
 const controller=useRef<AbortController|null>(null)
 useEffect(()=>{setExpanded(true)},[requestId])
 useEffect(()=>{const abort=new AbortController();fetchUniverseCatalog(abort.signal).then(setCatalog).catch(e=>{if(!abort.signal.aborted)setError(e instanceof Error?e.message:'Catálogo no disponible.')});return()=>{abort.abort();controller.current?.abort()}},[])
 async function query(){
  const universe=catalog.find(u=>u.level+':'+u.id===choice);if(!universe){setError('Selecciona un universo disponible.');return}
  let annualRate:number|null=null
  try{if(mode!=='ln-history')annualRate=parseAnnualRate(rate)}catch(e){setError((e as Error).message);return}
  controller.current?.abort();const abort=new AbortController();controller.current=abort;setLoading(true);setError(null);setResult(null);setSelected(null)
  try{
   const [maps,response]=await Promise.all([Promise.all((mode==='ln-history'?[2018,2021,2024]:[2024]).map(year=>fetchUniverseMap(universe,year,'A',abort.signal,mode==='adult-rate'?'leaders':'abstention'))),fetch(import.meta.env.BASE_URL+'data/heyti-socioeconomico-referencia-2020.json',{signal:abort.signal})])
   if(!response.ok)throw new Error('Referencia censal no disponible. Comprueba que se copiaron todos los archivos de la actualización.')
   const reference=parseSocioReference(await response.json()),rows=projectionRows(maps,reference,mode,annualRate)
   if(abort.signal.aborted)return
   setResult({maps,reference,mode,rate:annualRate,inputRate:rate,rows});selectUniverse({id:universe.id,label:universe.label,level:universe.level,parentId:universe.level==='state'?null:'11',truthStatus:'pending'})
  }catch(e){if(!abort.signal.aborted)setError(e instanceof Error?e.message:'Consulta no disponible.')}finally{if(!abort.signal.aborted)setLoading(false)}
 }
 const base=result?.maps.find(m=>m.year===2024)
 const byId=useMemo(()=>Object.fromEntries((result?.rows??[]).map(r=>[r.id,r])),[result])
 const cuts=useMemo(()=>socioCuts((result?.rows??[]).map(r=>r.projected),5),[result])
 const geo=useMemo(()=>{if(!base||!result)return null;const collection=toGeoJsonFeatureCollection(base.sections);for(const f of collection.features){const row=byId[f.properties.sectionId];f.properties.featureLabel='Sección '+row.id+' · '+projectionLabel(result.mode)+' · escenario 2027: '+number(row.projected)+' personas · '+row.reason}return collection},[base,result,byId])
 const valid=result?.rows.filter(r=>r.projected!==null)??[]
 const projectedSum=valid.reduce((sum,r)=>sum+r.projected!,0),baseSum=valid.reduce((sum,r)=>sum+r.base!,0)
 const {selectSection}=useAreaSectionSource(base)
 const focus=(id:string)=>{setSelected(id);setExpanded(true);selectSection(id)}
 const chosen=selected?byId[selected]:null
 const stale=!!result&&(choice!==base!.universe.level+':'+base!.universe.id||mode!==result.mode||(mode!=='ln-history'&&rate!==result.inputRate))
 return <main className="workspace-canvas" data-map-expanded="true"><div className="workspace-visual-grid"><section className="workspace-visual-panel" aria-labelledby="projection-map-title"><header><div><p>UNIVERSO SELECCIONADO</p><h2 id="projection-map-title">{base?.universe.label??state.universe?.label??'Sin selección'}</h2></div><span className="workspace-truth-status">Escenario 2027 · no es una proyección oficial</span></header><div className={result?'workspace-visual-map':'workspace-visual-placeholder'}>{result&&geo?<figure className="section-geometry-map"><GeographicMap data={geo} mapAriaLabel="Mapa base del escenario socioeconómico 2027" showSectionLabels selectedSection={selected} onSelectSection={focus} style={feature=>{const id=String(feature?.properties?.sectionId??''),band=socioBand(byId[id]?.projected??null,cuts);return {fillColor:band===null?'#94a3b8':SOCIO_COLORS[band],fillOpacity:band===null?.2:.48,color:selected===id?'#111827':'#64748b',weight:selected===id?3:.8}}}/><figcaption><strong>{projectionLabel(result.mode)} · escenario condicional 2027. Colores por quintiles de conteos estimados; gris = N/D. No indican bienestar ni preferencias electorales.</strong></figcaption></figure>:<><strong>{loading?'Consultando bases y calculando escenario…':'Escenarios socioeconómicos 2027'}</strong><small>Selecciona el universo y el método para consultar.</small></>}</div></section>
 {expanded?<FloatingInsightPanel title="Proyección 2027 · escenarios condicionales" comparative onClose={()=>setExpanded(false)}><section style={{padding:'20px 16px'}}><p>Explora cómo cambiarían los conteos si se mantuviera una tasa anual. Son ejercicios matemáticos de HEYTI, no pronósticos oficiales ni recomendaciones para una campaña. La lista nominal y la población adulta son conceptos distintos: no se restan ni se suman entre sí.</p>
 <label className="workspace-electoral-comparison-control"><span>Universo</span><select value={choice} disabled={loading||!catalog.length} onChange={e=>setChoice(e.target.value)}>{catalog.map(u=><option key={u.level+':'+u.id} value={u.level+':'+u.id}>{u.label}</option>)}</select></label>
 <label className="workspace-electoral-comparison-control"><span>Serie y método</span><select value={mode} disabled={loading} onChange={e=>setMode(e.target.value as ProjectionMode)}><option value="ln-history">Lista nominal · extrapolación histórica 2018–2024</option><option value="ln-rate">Lista nominal · tasa anual propia desde 2024</option><option value="adult-rate">Población de 18 años y más · tasa anual propia desde Censo 2020</option></select></label>
 {mode!=='ln-history'?<label className="workspace-electoral-comparison-control"><span>Tasa anual del escenario (%) · obligatoria, cero permitido</span><input type="text" inputMode="decimal" value={rate} disabled={loading} onChange={e=>setRate(e.target.value)} placeholder="Escribe tu supuesto anual"/></label>:null}
 <p>{mode==='ln-history'?'Tasa por sección = (LN 2024 / LN 2018)^(1/6) − 1. Escenario 2027 = LN 2024 × (1 + tasa)^3. LN 2021 se muestra como contexto y no interviene en esta fórmula de V1. No se aplica una tasa de respaldo a los faltantes.':mode==='adult-rate'?'Escenario 2027 = población de 18 años y más de 2020 × (1 + tasa propia)^7. No hay una serie verificada de población adulta de 2018 y 2024 en los archivos revisados. El supuesto no modela envejecimiento, mortalidad ni migración.':'Escenario 2027 = LN 2024 × (1 + tasa propia)^3. Se aplica el mismo supuesto a las secciones con base disponible; no constituye una actualización del padrón.'}</p>
 <button type="button" className="workspace-action" disabled={loading||!catalog.length} onClick={()=>void query()}>{loading?'Calculando…':'Calcular escenario 2027 y pintar mapa'}</button>
 {error?<p role="alert">{error}</p>:null}{stale?<p role="status">Cambió la selección. Tabla y mapa conservan el escenario anterior hasta volver a calcular.</p>:null}
 {result&&base?<><h3>{base.universe.label} · {projectionLabel(result.mode)} · escenario 2027</h3><p>{valid.length} de {result.rows.length} secciones representadas con cálculo; {result.rows.length-valid.length} N/D. {base.coverage.blocked} geometrías bloqueadas, fuera de esta tabla. {result.rate!==null?'Tasa propia aplicada: '+number(result.rate*100,6)+'% anual.':''}</p>
 <p>Subtotal de las mismas {valid.length} secciones calculables: base {valid.length?number(baseSum):'N/D'} personas → escenario 2027 {valid.length?number(projectedSum):'N/D'} personas. {valid.length<result.rows.length?'Cobertura parcial; no es el total completo del universo.':''} Se suman los resultados sin redondear; solo se redondea su presentación.</p>
 <p className="heyti-overview-note">La lista nominal se toma de los registros de Ayuntamiento (A) de cada año del CORE; no se mezcla con listas de otras contiendas. Las claves y la agrupación corresponden al archivo territorial actual. Una clave coincidente no acredita límites históricos equivalentes. El cálculo por clave es condicional a esa equivalencia; no demuestra crecimiento demográfico. No se reparten cifras de una sección de origen entre secciones nuevas. La fuente electoral del CORE conserva auditoría pendiente.</p>
 <ul style={{listStyle:'none',padding:0}}>{SOCIO_COLORS.map((color,i)=><li key={color} style={{margin:'8px 0'}}><span aria-hidden="true" style={{display:'inline-block',width:14,height:14,background:color,marginRight:8}}/>Grupo {i+1}: {valid.filter(r=>socioBand(r.projected,cuts)===i).length} secciones · {valid.length?(i===0?'desde el mínimo':'más de '+number(cuts[i-1],2))+(i===4?' hasta el máximo':' hasta '+number(cuts[i],2)+' inclusive'):'sin valores'}</li>)}</ul><p>Quintiles calculados con estimaciones sin redondear. Los empates permanecen juntos; puede haber grupos vacíos. Mayor conteo no significa mayor bienestar.</p>
 <SectionTableSearch><div className="heyti-win-table-scroll"><table className="heyti-win-table heyti-section-table" style={{minWidth:1300}}><caption>Detalle por sección. Selecciona una clave para acercar el mapa y ver su ficha.</caption><thead><tr><th>Sección</th>{result.mode!=='adult-rate'?<><th>LN 2018</th><th>LN 2021</th><th>LN 2024 · base</th></>:<th>Población 18+ · Censo 2020</th>}<th>Tasa anual (%)</th><th>Años hasta 2027</th><th>Escenario 2027 · personas</th><th>Cambio vs base · personas</th><th>Estado y método</th><th>Correspondencia territorial</th></tr></thead><tbody>{result.rows.map(r=><tr data-section-id={r.id} key={r.id} aria-selected={selected===r.id}><td><button type="button" onClick={()=>focus(r.id)}>{r.id}</button></td>{result.mode!=='adult-rate'?r.history.map((v,i)=><td key={i}>{number(v)}</td>):<td>{number(r.adults2020)}</td>}<td>{number(r.rate===null?null:r.rate*100,6)}</td><td>{r.years}</td><td>{number(r.projected)}</td><td>{number(r.projected===null||r.base===null?null:r.projected-r.base)}</td><td>{r.reason}</td><td>{result.mode==='adult-rate'?socioLinkLabel(r.id,result.reference):'Enlace por clave; equivalencia histórica de límites pendiente'}</td></tr>)}</tbody></table></div></SectionTableSearch>
 {chosen?<section className="heyti-data-panel-detail"><h3>Sección {chosen.id} · escenario condicional</h3><p>Base {result.mode==='adult-rate'?'2020':'2024'}: {number(chosen.base)} personas. Tasa anual: {number(chosen.rate===null?null:chosen.rate*100,6)}%. Escenario 2027: {number(chosen.projected)} personas. {chosen.reason}.</p><p>La tasa se aplica durante {chosen.years} años. Los valores originales se conservan; este cálculo no modifica archivos de datos.</p></section>:null}
 <p>Procedencia electoral CORE: {Object.entries(base.provenance).map(([key,value])=>key+' = '+value).join(' · ')}.</p>
 <p><a href={SOCIO_OFFICIAL_URL} target="_blank" rel="noreferrer">INEGI/INE · Censo 2020 geoelectoral · población de 18 años y más</a>. El mapa usa la geometría disponible de V2; no reconstruye límites de 2020.</p>
 </>:null}</section></FloatingInsightPanel>:<button type="button" className="workspace-action" style={{position:'fixed',right:16,bottom:16,zIndex:30}} onClick={()=>setExpanded(true)}>Expandir proyección 2027</button>}
 </div></main>
}
