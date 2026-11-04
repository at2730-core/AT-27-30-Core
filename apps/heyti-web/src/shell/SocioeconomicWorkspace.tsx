import { SectionTableSearch } from './SectionTableSearch'
import { useAreaSectionSource } from './AreaSectionSelection'
import { SocioEducationMap } from './SocioEducationMap'
import { SocioTraceabilitySummary } from './SocioTraceabilitySummary'
import { parseSocioReference, verifySocioSource, socioValueStatus, socioLinkLabel } from './socioTraceability'
import type { SocioReference, SocioVerification } from './socioTraceability'
import { useEffect, useMemo, useRef, useState } from 'react'
import { fetchUniverseCatalog, fetchUniverseMap } from '../gateway/universe.client'
import type { UniverseMap, UniverseOption } from '../gateway/universe.client'
import { useWorkspace } from '../platform/useWorkspace'
import { FloatingInsightPanel } from './FloatingInsightPanel'
import { parseSocio, SOCIO_INDICATORS, SOCIO_COLORS, socioBand, socioCuts } from './socioeconomic'
import type { SocioData, SocioKey } from './socioeconomic'
import './WinScenarioTable.css'
interface SocioResult { map: UniverseMap; data: SocioData; reference: SocioReference; verification: SocioVerification; key: SocioKey; groups: number }
const number = (v: number | null | undefined) => v == null ? 'N/D' : v.toLocaleString('es-MX', {maximumFractionDigits: 2})
export function SocioeconomicWorkspace({requestId=0}:{requestId?:number}) {
  const { state, selectUniverse } = useWorkspace()
  const [catalog, setCatalog] = useState<UniverseOption[]>([])
  const [choice,setChoice] = useState(state.universe && state.universe.level !== 'section' ? `${state.universe.level}:${state.universe.id}` : 'state:11')
  const [key,setKey] = useState<SocioKey>('POB_TOTAL'), [groups,setGroups] = useState(5)
  const [result,setResult] = useState<SocioResult | null>(null), [error,setError] = useState<string | null>(null)
  const [loading,setLoading] = useState(false), [selected,setSelected] = useState<string | null>(null)
  const [expanded,setExpanded] = useState(true)
  const request = useRef<AbortController | null>(null)
  useEffect(()=>{setExpanded(true)},[requestId])
  useEffect(()=>{
    const abort = new AbortController()
    fetchUniverseCatalog(abort.signal).then(setCatalog).catch(e=>{if(!abort.signal.aborted)setError(e instanceof Error?e.message:'Catálogo no disponible.')})
    return ()=>{abort.abort();request.current?.abort()}
  },[])
  async function query() {
    const universe = catalog.find(u=>`${u.level}:${u.id}`===choice)
    if (!universe) {setError('Selecciona un universo.');return}
    request.current?.abort(); const abort = new AbortController();request.current=abort
    setLoading(true);setError(null);setResult(null);setSelected(null)
    try {
      // La respuesta electoral se usa únicamente para sus geometrías autorizadas.
      const [map,response,referenceResponse] = await Promise.all([fetchUniverseMap(universe,2024,'A',abort.signal), fetch(`${import.meta.env.BASE_URL}data/heyti-socioeconomico.json`, {signal:abort.signal}), fetch(`${import.meta.env.BASE_URL}data/heyti-socioeconomico-referencia-2020.json`, {signal:abort.signal})])
      if (!response.ok) throw new Error('Archivo socioeconómico no disponible.')
      if (!referenceResponse.ok) throw new Error('Referencia oficial no disponible. Comprueba que se copiaron los archivos de datos de esta actualización.')
      const [rawData,rawReference] = await Promise.all([response.json(),referenceResponse.json()])
      const data = parseSocio(rawData), reference = parseSocioReference(rawReference)
      const verification = verifySocioSource(data,reference)
      if(abort.signal.aborted)return
      setResult({map,data,reference,verification,key,groups})
      selectUniverse({id:map.universe.id,label:map.universe.label,level:map.universe.level,parentId:map.universe.level==='state'?null:'11',truthStatus:'pending'})
    } catch(e) {if(!abort.signal.aborted)setError(e instanceof Error?e.message:'Consulta no disponible.')}
    finally {if(!abort.signal.aborted)setLoading(false)}
  }
  const rows = useMemo(()=>result ? [...result.map.sections].sort((a,b)=>Number(a.sectionId)-Number(b.sectionId)).map(s=>({...s,value:result.data[s.sectionId]?.[result.key]??null})) : [],[result])
  const cuts = useMemo(()=>socioCuts(rows.map(r=>r.value),result?.groups??5),[rows,result])
  const values = useMemo(()=>Object.fromEntries(rows.map(row=>[row.sectionId,row.value])),[rows])
  const indicator = SOCIO_INDICATORS.find(i=>i.key===(result?.key??key))!
  const valid = rows.filter(r=>r.value!==null)
  const sum = valid.reduce((n,r)=>n+r.value!,0)
  const stale = result && (result.key!==key || result.groups!==groups || `${result.map.universe.level}:${result.map.universe.id}`!==choice)
  const chosen = selected && result ? result.data[selected] : null
 const {selectSection}=useAreaSectionSource(result?.map)
  const focus = (id:string)=>{setSelected(id);setExpanded(true);selectSection(id)}
  return <main className="workspace-canvas" data-map-expanded="true"><div className="workspace-visual-grid">
    <section className="workspace-visual-panel" aria-labelledby="socio-map-title"><header><div><p>UNIVERSO SELECCIONADO</p><h2 id="socio-map-title">{result?.map.universe.label??state.universe?.label??'Sin selección'}</h2></div><span className="workspace-truth-status">{result ? result.verification.allMatch ? 'INEGI · Censo 2020 · límites pendientes de conciliar' : 'Referencia INEGI 2020 · cotejo con diferencias' : 'Socioeconómico · referencia Censo 2020'}</span></header>
    <div className={result?'workspace-visual-map':'workspace-visual-placeholder'}>
    {result ? <SocioEducationMap map={result.map} values={values} label={indicator.label} unit={indicator.unit} cuts={cuts} groups={result.groups} reference={result.reference} selected={selected} onSelect={focus}/> : <><strong>{loading?'Consultando geometrías y datos…':'Indicadores socioeconómicos'}</strong><small>Selecciona universo e indicador y pulsa «Pintar mapa».</small></>}
    </div></section>
    {expanded ? <FloatingInsightPanel title="Indicadores socioeconómicos · Censo 2020" comparative onClose={()=>setExpanded(false)}><section style={{padding:'20px 16px'}}>
      <p className="heyti-overview-note">Referencia: INEGI e INE, Censo 2020. Al consultar se cotejan las cifras del archivo con la referencia oficial. La correspondencia de límites con el mapa sigue pendiente; no se rellenan faltantes.</p>
      <label className="workspace-electoral-comparison-control"><span>Universo</span><select value={choice} disabled={loading||!catalog.length} onChange={e=>setChoice(e.target.value)}>{catalog.map(u=><option key={`${u.level}:${u.id}`} value={`${u.level}:${u.id}`}>{u.label} · {u.sections} secciones</option>)}</select></label>
      <label className="workspace-electoral-comparison-control"><span>Indicador</span><select value={key} disabled={loading} onChange={e=>setKey(e.target.value as SocioKey)}>{SOCIO_INDICATORS.map(i=><option key={i.key} value={i.key}>{i.label}</option>)}</select></label>
      <label className="workspace-electoral-comparison-control"><span>Clasificación descriptiva</span><select value={groups} disabled={loading} onChange={e=>setGroups(Number(e.target.value))}><option value={5}>Quintiles</option><option value={4}>Cuartiles</option><option value={3}>Tercios</option></select></label>
      <button type="button" className="workspace-action" disabled={loading||!catalog.length} onClick={()=>void query()}>{loading?'Consultando…':'Pintar mapa'}</button>
      {error?<p role="alert">{error}</p>:null}{stale?<p role="status">La selección cambió. Pulsa «Pintar mapa» para actualizar.</p>:null}
      {result?<><h3>{result.map.universe.label} · {indicator.label}</h3><SocioTraceabilitySummary map={result.map} reference={result.reference} verification={result.verification} indicator={result.key}/><p>{valid.length} secciones con valor; {rows.length-valid.length} N/D; {result.map.coverage.blocked} geometrías bloqueadas no representadas.</p>
      <p>{result.key==='ESCOLARIDAD_PROM' ? `Media no ponderada de valores seccionales: ${number(valid.length?sum/valid.length:null)} años · ${valid.length} secciones con dato. Cada sección con dato tiene el mismo peso. No es el promedio ponderado de la población ni un promedio oficial del territorio actual.` : `Suma de valores del archivo enlazados por clave: ${number(valid.length?sum:null)} ${indicator.unit}. Cobertura parcial; no es un total certificado del territorio actual.`}</p>
      {valid.length ? <ul style={{listStyle:'none',padding:0}}>{Array.from({length:result.groups},(_,band)=><li key={band} style={{margin:'8px 0'}}><span aria-hidden="true" style={{display:'inline-block',width:14,height:14,background:SOCIO_COLORS[Math.round(band*4/(result.groups-1))],marginRight:8}}/>Grupo {band+1}: {rows.filter(r=>socioBand(r.value,cuts)===band).length} secciones · {band===0?'desde el mínimo':`más de ${number(cuts[band-1])}`} {band<cuts.length?`hasta ${number(cuts[band])} inclusive`:'hasta el máximo'}</li>)}</ul> : <p>No hay valores disponibles para calcular rangos.</p>}
      <p className="heyti-overview-note">Cuantiles calculados solo con valores disponibles del universo. Los empates permanecen juntos: puede haber grupos vacíos o de distinto tamaño. Un conteo absoluto mayor no indica una tasa ni mayor bienestar.</p>
      <SectionTableSearch><div className="heyti-win-table-scroll"><table className="heyti-win-table heyti-section-table" style={{minWidth:650}}><thead><tr><th>Sección</th><th>{indicator.label}</th><th>Unidad</th><th>Estado del valor</th><th>Correspondencia territorial</th><th>Distrito federal en fuente 2020</th></tr></thead><tbody>{rows.map(r=><tr data-section-id={r.sectionId} key={r.sectionId} aria-selected={selected===r.sectionId} onClick={()=>focus(r.sectionId)}><td><button type="button" onClick={e=>{e.stopPropagation();focus(r.sectionId)}}>{r.sectionId}</button></td><td>{number(r.value)}</td><td>{indicator.unit}</td><td>{socioValueStatus(r.sectionId,result.key,result.data,result.reference)}</td><td>{socioLinkLabel(r.sectionId,result.reference)}</td><td>{result.reference.sections[r.sectionId]?.district??'N/D'}</td></tr>)}</tbody></table></div></SectionTableSearch>
      {selected?<><h3>Sección {selected} · detalle</h3><p>{socioLinkLabel(selected,result.reference)}. Las cifras se conservan sin reparto entre secciones.</p><dl>{SOCIO_INDICATORS.map(i=><div key={i.key} style={{margin:'10px 0'}}><dt>{i.label}</dt><dd>{number(chosen?.[i.key])} {chosen?.[i.key]==null?'':i.unit} · {socioValueStatus(selected,i.key,result.data,result.reference)}</dd></div>)}</dl></>:null}
      <p className="heyti-overview-note">Se conservan todas las filas representadas, incluso sin dato. Las sumas y cuantiles describen valores disponibles enlazados por clave, no una equivalencia territorial certificada. La referencia censal no sustituye los límites del CORE ni completa secciones nuevas por estimación.</p></>:null}
    </section></FloatingInsightPanel> : <button type="button" className="workspace-action" style={{position:'fixed',right:16,bottom:16,zIndex:30}} onClick={()=>setExpanded(true)}>Expandir indicadores socioeconómicos</button>}
  </div></main>
}
