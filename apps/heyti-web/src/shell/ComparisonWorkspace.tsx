import { SectionTableSearch } from './SectionTableSearch'
import {fetchUniverseCatalog} from '../gateway/universe.client'
import type {UniverseOption} from '../gateway/universe.client'
import {changeComparisonUniverse} from './comparisonUniverse'
import {scopeKey} from './contextQueries'
import {useEffect,useRef,useState} from 'react'
import type {ReactNode} from 'react'
import {useWorkspace} from '../platform/useWorkspace'
import {DEMO_CONTESTS,DEMO_PARTIES} from '../gateway/section.demo'
import type {DemoContestId} from '../gateway/section.demo'
import {COMPARISON_MODULES,comparisonModules,supportedUniverse} from './contextQueries'
import {comparisonSignature,loadComparison} from './comparisonData'
import type {ComparisonData} from './comparisonData'
import {SOCIO_INDICATORS} from './socioeconomic'
import type {SocioKey} from './socioeconomic'
import {socioLinkLabel,socioValueStatus} from './socioTraceability'
import './ContextQueries.css'
const labels:Record<DemoContestId,string>={A:'Ayuntamiento',DL:'Diputaciones locales',DF:'Diputaciones federales',G:'Gubernatura',S:'Senado',P:'Presidencia'}
const number=(v:number|null|undefined)=>v==null?'N/D':v.toLocaleString('es-MX',{maximumFractionDigits:3})
const percent=(v:number|null|undefined)=>v==null?'N/D':`${number(v)}%`
const rowStatus=(status:string,total:number|null)=>status==='NOT_CONTESTED'?'Elección no celebrada':['INCONSISTENT'].includes(status)?'Cifras por revisar':total===null?'N/D':total===0?'Total en cero':['NO_DATA','INCOMPLETE','SUMMARY_ONLY'].includes(status)?'Datos incompletos':'Sin certificar'
function Trace({provenance}:{provenance:Record<string,string>}){return <details><summary>Fuente y trazabilidad</summary><dl>{Object.entries(provenance).map(([k,v])=><div key={k}><dt>{k}</dt><dd>{v}</dd></div>)}</dl></details>}
function Table({label,head,children}:{label:string;head:string[];children:ReactNode}) {return <SectionTableSearch enabled={head[0]==='Sección'}><div className="heyti-perspective-scroll" tabIndex={0} role="region" aria-label={label}><table className={head[0]==='Sección'?'heyti-section-table':undefined}><caption>{label}</caption><thead><tr>{head.map(h=><th scope="col" key={h}>{h}</th>)}</tr></thead><tbody>{children}</tbody></table></div></SectionTableSearch>}
export function ComparisonWorkspace({onConfigure,onUniverseChange}:{onConfigure:()=>void;onUniverseChange?:()=>void}) {
 const {state,setMode,selectUniverse}=useWorkspace()
 const [catalog,setCatalog]=useState<UniverseOption[]>([]),[catalogError,setCatalogError]=useState<string|null>(null)
 const [universeChoice,setUniverseChoice]=useState(scopeKey(state.universe))
 const activeScope=scopeKey(state.universe)
 useEffect(()=>{setUniverseChoice(activeScope)},[activeScope])
 useEffect(()=>{
  const abort=new AbortController()
  fetchUniverseCatalog(abort.signal).then(options=>{if(!abort.signal.aborted)setCatalog(options)}).catch(e=>{if(!abort.signal.aborted)setCatalogError(e instanceof Error?e.message:'Catálogo no disponible.')})
  return ()=>abort.abort()
 },[])
 const [contest,setContest]=useState<DemoContestId>('A'),[indicator,setIndicator]=useState<SocioKey>('ESCOLARIDAD_PROM')
 const [snapshot,setSnapshot]=useState<{signature:string;data:ComparisonData}|null>(null)
 const [loading,setLoading]=useState(false),[error,setError]=useState<string|null>(null)
 const controller=useRef<AbortController|null>(null)
 let configurationError:string|null=null
 try{comparisonModules(state.comparisonModuleIds)}catch(e){configurationError=e instanceof Error?e.message:'Configura los módulos.'}
 const signature=comparisonSignature(state.universe,state.comparisonModuleIds,contest)
 useEffect(()=>{controller.current?.abort();setSnapshot(null);setError(null);setLoading(false);return ()=>controller.current?.abort()},[signature])
 const result=snapshot?.signature===signature?snapshot.data:null
 async function query(){
  if(!state.universe||!supportedUniverse(state.universe)||configurationError)return
  controller.current?.abort();const abort=new AbortController();controller.current=abort
  setSnapshot(null);setError(null);setLoading(true)
  try{const data=await loadComparison(state.universe,state.comparisonModuleIds,contest,abort.signal);if(!abort.signal.aborted)setSnapshot({signature,data})}
  catch(e){if(!abort.signal.aborted)setError(e instanceof Error?e.message:'No fue posible comparar.')}
  finally{if(!abort.signal.aborted)setLoading(false)}
 }
 const meta=SOCIO_INDICATORS.find(i=>i.key===indicator)!
 return <main className="workspace-canvas"><section className="workspace-introduction"><div><p className="workspace-eyebrow">CONTEXTO COMPARTIDO</p><h1>Comparar perspectivas</h1><p>Vista tabular · mismo universo · fuentes separadas.</p></div><button type="button" className="workspace-action" onClick={onConfigure}>Configurar módulos</button></section>
  <h2>{state.universe?.label??'Sin universo seleccionado'}</h2>
  <div className="heyti-comparison-controls">
   <label className="heyti-context-control">Universo para comparar<select value={universeChoice} disabled={!catalog.length} onChange={e=>setUniverseChoice(e.target.value)}>
    <option value="none" disabled>Selecciona un universo</option>
    {state.universe?.level==='section'?<option value={activeScope}>{state.universe.label} · universo activo</option>:null}
    {(['state','municipality','federal-district','local-district'] as const).map(level=><optgroup key={level} label={{state:'Estado',municipality:'Municipios','federal-district':'Distritos federales','local-district':'Distritos locales'}[level]}>{catalog.filter(u=>u.level===level).map(u=><option key={`${u.level}:${u.id}`} value={`${u.level}:${u.id}`}>{u.label} · {u.sections} secciones</option>)}</optgroup>)}
   </select></label>
   <button type="button" className="workspace-action" disabled={!catalog.length||universeChoice===activeScope||universeChoice==='none'} onClick={()=>{
    try{changeComparisonUniverse(state.universe,universeChoice,catalog,()=>{controller.current?.abort();setSnapshot(null);setError(null);setLoading(false);onUniverseChange?.()},selectUniverse)}catch(e){setCatalogError(e instanceof Error?e.message:'Universo no disponible.')}
   }}>Usar este universo</button>
  </div>
  {catalogError?<p role="alert">{catalogError}</p>:null}
  {universeChoice!==activeScope&&universeChoice!=='none'?<p role="status">Pulsa «Usar este universo» para cambiar el contexto; después «Consultar perspectivas».</p>:null}
  {!supportedUniverse(state.universe)?<p role="status">Selecciona un estado, municipio, distrito o sección en Universo activo.</p>:null}
  {configurationError?<p role="status">{configurationError} Pulsa «Configurar módulos».</p>:null}
  <div className="heyti-comparison-controls"><label className="heyti-context-control">Contienda electoral · sin modalidad MR/RP<select value={contest} onChange={e=>setContest(e.target.value as DemoContestId)}>{DEMO_CONTESTS.map(c=><option key={c} value={c}>{labels[c]}</option>)}</select></label>
   {state.comparisonModuleIds.includes('socioeconomic')?<label className="heyti-context-control">Indicador censal · 2020<select value={indicator} onChange={e=>setIndicator(e.target.value as SocioKey)}>{SOCIO_INDICATORS.map(i=><option key={i.key} value={i.key}>{i.label}</option>)}</select></label>:null}
   <button type="button" className="workspace-action" disabled={loading||!!configurationError||!supportedUniverse(state.universe)} onClick={()=>void query()}>{loading?'Consultando…':'Consultar perspectivas'}</button>
   <button type="button" className="workspace-action" onClick={()=>setMode('individual')}>Volver a Individual</button>
  </div>
  <p className="heyti-overview-note">Demostración descriptiva con fuentes pendientes de validación. La colocación de cifras en paralelo no prueba relaciones causales ni equivale a un cruce estadístico. Los años y la cobertura se indican por columna. N/D no equivale a cero.</p>
  {error?<p role="alert">{error}</p>:null}
  {result?<><p>{result.rows.length} secciones representadas de {result.geographic}; {result.blocked} bloqueadas o sin geometría disponible. Las columnas usan las mismas identidades autorizadas; la cobertura calculable puede variar.</p>
   <div className="heyti-perspectives">{result.modules.map(module=><section className="heyti-perspective" key={module}><h2>{COMPARISON_MODULES.find(m=>m.id===module)?.label}</h2><p>{state.universe!.label}</p>
    {module==='territorial-analysis'?<><p>{labels[contest]} · 2024. Cuatro partidos rastreados; el total incluye otros conceptos. Sin atribución de ganador absoluto.</p><Table label="Resultados 2024 por sección" head={['Sección','Total','LN',...DEMO_PARTIES,'Estado']}>{result.rows.map(r=><tr data-section-id={r.id} key={r.id}><th scope="row">{r.id}</th><td>{number(r.total)}</td><td>{number(r.nominal)}</td>{DEMO_PARTIES.map(p=><td key={p}>{number(r.votes[p])}</td>)}<td>{rowStatus(r.status,r.total)}</td></tr>)}</Table><Trace provenance={result.provenance}/></>:null}
    {module==='win-all'?<><p>{labels[contest]} · participación = total de votos / lista nominal × 100.</p><Table label="Participación histórica · cobertura por año" head={['Año','Calculables','Votos','LN','Participación']}>{result.trend.map(t=><tr key={t.year}><th scope="row">{t.year}</th><td>{t.validSections}</td><td>{t.validSections?number(t.votes):'N/D'}</td><td>{t.validSections?number(t.nominal):'N/D'}</td><td>{percent(t.abstention===null?null:100-t.abstention)}</td></tr>)}</Table><p>Las coberturas cambian entre años. Se conserva la clave actual; no certifica equivalencia de límites históricos. Cero con denominador válido se conserva como 0%.</p><Trace provenance={result.provenance}/></>:null}
    {module==='socioeconomic'?result.socioError?<p role="alert">{result.socioError} No se muestran cifras censales.</p>:result.socio&&result.reference?<><p>{meta.label} · {meta.unit}. Censo 2020, publicado el 18 de agosto de 2021.</p><p>{result.rows.filter(r=>result.socio![r.id]?.[indicator]!=null).length} secciones con valor de {result.rows.length}. {indicator==='ESCOLARIDAD_PROM'?'Aquí se muestran valores por sección. La media no ponderada de valores seccionales que muestran Individual y Educación es una medida descriptiva; no es el promedio ponderado de la población ni un promedio oficial del territorio actual.':'Aquí se muestran los valores del indicador por sección.'}</p><Table label="Indicador censal por sección" head={['Sección',meta.label, 'Estado de cifra','Correspondencia territorial']}>{result.rows.map(r=><tr data-section-id={r.id} key={r.id}><th scope="row">{r.id}</th><td>{number(result.socio![r.id]?.[indicator])}</td><td>{socioValueStatus(r.id,indicator,result.socio!,result.reference!)}</td><td>{socioLinkLabel(r.id,result.reference!)}</td></tr>)}</Table><p>Enlace por clave; límites pendientes de conciliación. Sin reparto de cifras a secciones nuevas ni totales certificados del territorio actual.</p><p>Cotejo del archivo completo de Guanajuato con referencia incluida: {result.verification?.matched} valores coincidentes; {result.verification?.different} diferentes; {result.verification?.missing} faltantes.</p><Trace provenance={{fuente:'INEGI / INE · Censo 2020',referencia_csv_sha256:result.reference.officialCsvSha256,geometria_sha256:result.provenance.geometry_sha256,correspondencia:'Enlace por clave; límites pendientes de conciliación'}}/></>:<p>Sin registros censales mostrables para este universo.</p>:null}
   </section>)}</div></>:!loading?<p>Configura los módulos y pulsa «Consultar perspectivas». Cada cambio de universo, contienda o módulos descarta la lectura anterior.</p>:null}
 </main>
}
