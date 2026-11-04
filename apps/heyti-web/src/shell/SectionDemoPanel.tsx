import { SectionHistoryCharts } from './SectionHistoryCharts'
import { createContext, useContext, useEffect, useState } from 'react'
import type { ReactNode } from 'react'
import { DEMO_CONTESTS, DEMO_PARTIES, demoParticipation, fetchSectionDemo } from '../gateway/section.demo'
import type { DemoContest, DemoContestId, SectionDemo } from '../gateway/section.demo'

const labels: Record<DemoContestId,string>={A:'Ayuntamiento',DL:'Diputaciones locales',DF:'Diputaciones federales',G:'Gubernatura',S:'Senado',P:'Presidencia'}
const statuses: Record<string,string>={AVAILABLE:'Disponible · sin certificar',AVAILABLE_WITHOUT_NOMINAL_LIST:'Lista nominal no disponible',SUMMARY_ONLY:'Solo resumen',NOT_CONTESTED:'Elección no celebrada',ZERO_TOTAL:'Total en cero',INCOMPLETE:'Datos incompletos',INCONSISTENT:'Datos inconsistentes',TIED_TRACKED_LEAD:'Empate entre partidos rastreados'}
interface DemoState { result: SectionDemo | null; error: string | null }
const Context=createContext<DemoState>({result:null,error:null})
export function SectionDemoProvider({sectionId,children}:{sectionId:string;children:ReactNode}) {
  const [state,setState]=useState<DemoState>({result:null,error:null})
  useEffect(()=>{
    const controller=new AbortController()
    setState({result:null,error:null})
    fetchSectionDemo(sectionId,controller.signal).then(result=>{
      if(!controller.signal.aborted) setState({result,error:null})
    }).catch((cause:unknown)=>{
      if(!controller.signal.aborted) setState({result:null,error:cause instanceof Error?cause.message:'Consulta de demostración no disponible.'})
    })
    return ()=>controller.abort()
  },[sectionId])
  return <Context.Provider value={state}>{children}</Context.Provider>
}
const format=(v:number|null)=>v===null?'N/D':v.toLocaleString('es-MX')
function percent(c:DemoContest) { const p=demoParticipation(c);return p===null?'N/D':`${p.toLocaleString('es-MX',{maximumFractionDigits:3})}%` }
function Row({title,c}:{title:string;c:DemoContest}) {
  return <tr><th scope="row">{title}</th><td>{format(c.nominal)}</td><td>{format(c.total)}</td><td>{percent(c)}</td>{DEMO_PARTIES.map(p=><td key={p}>{format(c.votes[p])}</td>)}<td>{statuses[c.status]}</td></tr>
}
function Table({children}:{children:ReactNode}) {
  return <div style={{overflowX:'auto',marginTop:16}}><table className="heyti-demo-section-table" style={{width:'100%',borderCollapse:'collapse'}}><thead><tr>{['Contienda / año','Lista nominal','Total de votos','Participación',...DEMO_PARTIES,'Estado'].map(h=><th key={h} scope="col" style={{padding:8,textAlign:'left',borderBottom:'1px solid #cbd5e1'}}>{h}</th>)}</tr></thead><tbody>{children}</tbody></table></div>
}
export function SectionDemoPanel({view,initialContest='A'}:{view:'summary'|'current'|'history'|'trace';initialContest?:DemoContestId}) {
  const {result,error}=useContext(Context)
  const [contest,setContest]=useState<DemoContestId>(initialContest)
  const notice=<p className="heyti-overview-note"><strong>Datos de demostración · validación pendiente.</strong> Fuente: maestro electoral usado por las consultas por universo. Desglose parcial: PAN, PRI, PVEM y MORENA; no acredita ganadores absolutos. La fuente no identifica MR/RP; no se presentan resultados como RP. N/D significa dato no disponible; cero conserva el valor del archivo.</p>
  if(error) return <div role="alert">{notice}<p>{error}</p></div>
  if(!result) return <p role="status">Consultando datos de demostración de la sección…</p>
  if(view==='trace') return <section><h3>Fuente electoral de demostración · Sección {result.sectionId}</h3>{notice}<p>Estado: {result.status}. Modalidad: no especificada en el maestro. Años: 2018, 2021 y 2024. No se ha seleccionado ni certificado una fuente del lector auditado.</p><dl>{Object.entries(result.provenance).map(([k,v])=><div key={k}><dt>{k}</dt><dd style={{overflowWrap:'anywhere'}}>{v}</dd></div>)}</dl></section>
  if(result.status!=='DEMO_AVAILABLE') return <section>{notice}<p>La sección no tiene datos de demostración disponibles para esta consulta ({result.status}). No se sustituyen por ceros.</p></section>
  const current=result.years.find(y=>y.year===2024)!
  if(view==='summary') return <section><h3>Resumen electoral 2024 · Sección {result.sectionId}</h3>{notice}<Table>{DEMO_CONTESTS.map(cid=><Row key={cid} title={labels[cid]} c={current.contests[cid]}/>)}</Table></section>
  return <section><h3>{view==='history'?'Historial 2018–2024':'Elección 2024'} · Sección {result.sectionId}</h3>{notice}<label>Contienda del maestro <select value={contest} onChange={e=>setContest(e.target.value as DemoContestId)}>{DEMO_CONTESTS.map(cid=><option key={cid} value={cid}>{labels[cid]}</option>)}</select></label>{view==='history'?<><SectionHistoryCharts years={result.years} contest={contest}/><details className="heyti-section-history-table"><summary>Ver tabla con las cifras exactas de 2018, 2021 y 2024</summary><Table>{result.years.map(y=><Row key={y.year} title={String(y.year)} c={y.contests[contest]}/>)}</Table></details></>:<Table><Row title={labels[contest]} c={current.contests[contest]}/></Table>}{view==='history'?<p>Comparación por clave de sección. La correspondencia de límites históricos no está certificada; una elección no celebrada no equivale a cero votos.</p>:null}<p>Participación = total de votos / lista nominal × 100, solo con valores calculables. El total incluye conceptos fuera de los cuatro partidos mostrados; no se reconstruye sumándolos.</p></section>
}
