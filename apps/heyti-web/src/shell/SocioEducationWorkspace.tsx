import { useAreaSectionSource } from './AreaSectionSelection'
import { useEffect, useMemo, useRef, useState } from 'react'
import { useWorkspace } from '../platform/useWorkspace'
import { fetchUniverseCatalog, fetchUniverseMap } from '../gateway/universe.client'
import type { UniverseMap, UniverseOption } from '../gateway/universe.client'
import { FloatingInsightPanel } from './FloatingInsightPanel'
import { fitUniverseSection } from './MapSectionFocus'
import { parseSocioReference } from './socioTraceability'
import type { SocioReference } from './socioTraceability'
import { SOCIO_COLORS, socioCuts, socioBand } from './socioeconomic'
import { parseEducation, EDUCATION_METRICS, educationMeasure, educationSummary } from './socioEducation'
import type { EducationData, EducationSelection } from './socioEducation'
import { SocioEducationMap } from './SocioEducationMap'
import { SocioEducationDetails } from './SocioEducationDetails'
interface Result {map:UniverseMap;data:EducationData;reference:SocioReference;selection:EducationSelection;unit:'count'|'percent';groups:number}
const num=(n:number|null|undefined)=>n==null?'N/D':n.toLocaleString('es-MX',{maximumFractionDigits:3})
export function SocioEducationWorkspace({requestId=0}:{requestId?:number}){
 const {state,selectUniverse,setMapView}=useWorkspace()
 const [catalog,setCatalog]=useState<UniverseOption[]>([])
 const [choice,setChoice]=useState(state.universe&&state.universe.level!=='section'?state.universe.level+':'+state.universe.id:'state:11')
 const [selection,setSelection]=useState<EducationSelection>('illiteracy'),[unit,setUnit]=useState<'count'|'percent'>('percent'),[groups,setGroups]=useState(5)
 const [result,setResult]=useState<Result|null>(null),[loading,setLoading]=useState(false),[error,setError]=useState<string|null>(null),[selected,setSelected]=useState<string|null>(null),[expanded,setExpanded]=useState(true)
 const controller=useRef<AbortController|null>(null)
 useEffect(()=>{setExpanded(true)},[requestId])
 useEffect(()=>{const abort=new AbortController();fetchUniverseCatalog(abort.signal).then(setCatalog).catch(e=>{if(!abort.signal.aborted)setError(e instanceof Error?e.message:'Catálogo no disponible.')});return()=>{abort.abort();controller.current?.abort()}},[])
 async function query(){
  const universe=catalog.find(u=>u.level+':'+u.id===choice);if(!universe){setError('Selecciona un universo disponible.');return}
  controller.current?.abort();const abort=new AbortController();controller.current=abort;setLoading(true);setError(null);setResult(null);setSelected(null)
  try{
   const [map,refResponse,eduResponse]=await Promise.all([fetchUniverseMap(universe,2024,'A',abort.signal),fetch(import.meta.env.BASE_URL+'data/heyti-socioeconomico-referencia-2020.json',{signal:abort.signal}),fetch(import.meta.env.BASE_URL+'data/heyti-educacion-2020.json',{signal:abort.signal})])
   if(!refResponse.ok||!eduResponse.ok)throw new Error('Fuente educativa o referencia oficial no disponible. Revisa que se copiaron los archivos de datos de la actualización.')
   const [rawReference,rawData]=await Promise.all([refResponse.json(),eduResponse.json()])
   const reference=parseSocioReference(rawReference),data=parseEducation(rawData,reference)
   if(abort.signal.aborted)return
   setResult({map,data,reference,selection,unit,groups});setMapView({zoom:1,x:0,y:0})
   selectUniverse({id:map.universe.id,label:map.universe.label,level:map.universe.level,parentId:map.universe.level==='state'?null:'11',truthStatus:'pending'})
  }catch(e){if(!abort.signal.aborted)setError(e instanceof Error?e.message:'Consulta educativa no disponible.')}finally{if(!abort.signal.aborted)setLoading(false)}
 }
 const activeSelection=result?.selection??selection,activeUnit=result?.unit??unit
 const metric=EDUCATION_METRICS.find(m=>m.key===activeSelection)
 const label=activeSelection==='schooling'?'Grado promedio de escolaridad · 15 años y más':metric!.label
 const mapUnit=activeSelection==='schooling'?'años':activeUnit==='percent'?'%':'personas'
 const values=useMemo(()=>Object.fromEntries(result?result.map.sections.map(s=>{
  const row=result.data.sections[s.sectionId],m=metric?educationMeasure(row,metric):null
  return [s.sectionId,activeSelection==='schooling'?row?.GRAPROES.value??null:activeUnit==='percent'?m!.percent:m!.status==='INCONSISTENT'?null:m!.numerator]
 }):[]),[result,metric,activeSelection,activeUnit])
 const cuts=useMemo(()=>socioCuts(Object.values(values),result?.groups??5),[values,result])
 const validValues=Object.values(values).filter((v):v is number=>v!==null)
 const ids=result?.map.sections.map(s=>s.sectionId)??[]
 const summary=result&&metric?educationSummary(ids,result.data,metric):null
 const stale=result&&(choice!==result.map.universe.level+':'+result.map.universe.id||selection!==result.selection||(selection!=='schooling'&&unit!==result.unit)||groups!==result.groups)
 const {selectSection}=useAreaSectionSource(result?.map)
 const focus=(id:string)=>{setSelected(id);setExpanded(true);selectSection(id);if(result){const view=fitUniverseSection(result.map,id);if(view)setMapView(view)}}
 return <main className="workspace-canvas" data-map-expanded="true"><div className="workspace-visual-grid"><section className="workspace-visual-panel" aria-labelledby="education-map-title"><header><div><p>UNIVERSO SELECCIONADO</p><h2 id="education-map-title">{result?.map.universe.label??state.universe?.label??'Sin selección'}</h2></div><span className="workspace-truth-status">Educación · INEGI 2020 · límites pendientes de conciliar</span></header><div className={result?'workspace-visual-map':'workspace-visual-placeholder'}>{result?<SocioEducationMap map={result.map} values={values} label={label} unit={mapUnit} cuts={cuts} groups={result.groups} reference={result.reference} selected={selected} onSelect={id=>{setSelected(id);setExpanded(true);selectSection(id)}}/>:<><strong>{loading?'Consultando fuente educativa y geometrías…':'Rezago educativo · perfil descriptivo'}</strong><small>Selecciona universo, indicador y unidad; pulsa Consultar educación y pintar mapa.</small></>}</div></section>
 {expanded?<FloatingInsightPanel title="Rezago educativo · perfil INEGI 2020" comparative onClose={()=>setExpanded(false)}><section style={{padding:'20px 16px'}}><p>Nueve medidas descriptivas de educación y escolaridad promedio. Datos censales 2020 por sección; no es un índice compuesto ni la medición oficial de carencia por rezago educativo.</p>
  <label className="workspace-electoral-comparison-control"><span>Universo</span><select value={choice} disabled={loading||!catalog.length} onChange={e=>setChoice(e.target.value)}>{catalog.map(u=><option key={u.level+':'+u.id} value={u.level+':'+u.id}>{u.label} · {u.sections} secciones</option>)}</select></label>
  <label className="workspace-electoral-comparison-control"><span>Indicador del mapa</span><select value={selection} disabled={loading} onChange={e=>setSelection(e.target.value as EducationSelection)}><option value="schooling">Grado promedio de escolaridad</option>{EDUCATION_METRICS.map(m=><option key={m.key} value={m.key}>{m.label}</option>)}</select></label>
  <label className="workspace-electoral-comparison-control"><span>Unidad del mapa</span><select value={selection==='schooling'?'years':unit} disabled={loading||selection==='schooling'} onChange={e=>setUnit(e.target.value as 'count'|'percent')}>{selection==='schooling'?<option value="years">Años de escolaridad</option>:<><option value="percent">Porcentaje del grupo de referencia</option><option value="count">Cantidad de personas</option></>}</select></label>
  <label className="workspace-electoral-comparison-control"><span>Clasificación descriptiva</span><select value={groups} disabled={loading} onChange={e=>setGroups(Number(e.target.value))}><option value={5}>Quintiles</option><option value={4}>Cuartiles</option><option value={3}>Tercios</option></select></label>
  <button type="button" className="workspace-action" disabled={loading||!catalog.length} onClick={()=>void query()}>{loading?'Consultando…':'Consultar educación y pintar mapa'}</button>{loading?<p role="status">Puedes cerrar la consulta cambiando a otra vista para cancelar.</p>:null}{error?<p role="alert">{error}</p>:null}{stale?<p role="status">Cambiaste la selección. Tabla y mapa conservan la consulta anterior hasta volver a consultar.</p>:null}
  {result?<><h3>{result.map.universe.label} · {label}</h3><p>Mapa en {mapUnit}: {validValues.length} secciones calculables y {ids.length-validValues.length} N/D. Oscuro indica mayor valor del indicador, no mayor o menor bienestar de forma universal. Los grupos se recalculan solo sobre valores disponibles de este universo; empates juntos.</p>
   {summary?<section className="heyti-data-panel-detail"><h4>Resumen parcial del indicador seleccionado</h4><p>Población de referencia: {metric!.population}. Campos {metric!.numerator} / {metric!.denominator}.</p><p>Cantidad disponible: {num(summary.countAvailableSum)} personas en {summary.countsAvailable}/{summary.total} secciones. Para el porcentaje se usan {summary.pairs}/{summary.total} pares calculables: {num(summary.count)} / {num(summary.denominator)} = {num(summary.percent)}{summary.percent===null?'':'%'}. La cobertura del conteo y la del porcentaje pueden ser diferentes.</p><p>Sumas parciales de registros2020 enlazados por clave; no son totales certificados del territorio actual. El porcentaje se calcula con sumas de numerador/denominador en la misma cobertura, no promediando porcentajes locales.</p></section>:<p>Media no ponderada de valores seccionales: {num(validValues.length?validValues.reduce((n,v)=>n+v,0)/validValues.length:null)} años · {validValues.length} secciones con dato. Cada sección con dato tiene el mismo peso. No es el promedio ponderado de la población ni un promedio oficial del territorio actual.</p>}
   {validValues.length?<ul style={{listStyle:'none',padding:0}}>{Array.from({length:result.groups},(_,band)=><li key={band} style={{margin:'8px 0'}}><span aria-hidden="true" style={{display:'inline-block',width:14,height:14,background:SOCIO_COLORS[Math.round(band*4/(result.groups-1))],marginRight:8}}/>Grupo {band+1}: {Object.values(values).filter(v=>socioBand(v,cuts)===band).length} secciones · {band===0?'desde el mínimo':'más de '+num(cuts[band-1])} {band<cuts.length?'hasta '+num(cuts[band])+' inclusive':'hasta el máximo'} {mapUnit}</li>)}</ul>:<p>No hay valores calculables para formar rangos.</p>}
   <SocioEducationDetails map={result.map} data={result.data} reference={result.reference} selected={selected} onSelect={focus}/>
  </>:null}
 </section></FloatingInsightPanel>:<button type="button" className="workspace-action" style={{position:'fixed',right:16,bottom:16,zIndex:30}} onClick={()=>setExpanded(true)}>Expandir perfil educativo</button>}
 </div></main>
}
