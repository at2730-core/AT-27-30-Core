import { SectionTableSearch } from './SectionTableSearch'
import { useEffect, useRef, useState } from 'react'
import { useWorkspace } from '../platform/useWorkspace'
import { fetchUniverseCatalog, fetchUniverseMap } from '../gateway/universe.client'
import type { UniverseMap, UniverseOption } from '../gateway/universe.client'
import { ELECTORAL_CONTEST_IDS } from '../gateway/electoral.response'
import type { ElectoralContestId } from '../gateway/electoral.response'
import { attachHistoricalReference, historicalReference, referenceSettings, referenceStatusLabels, REFERENCE_PARTIES } from './historicalReference'
import type { ReferenceParty } from './historicalReference'
import './WinScenarioTable.css'
const num = (v: number | null | undefined) => v == null ? 'N/D' : v.toLocaleString('es-MX', { maximumFractionDigits: 3 })
const signed = (v: number | null) => v === null ? 'N/D' : `${v > 0 ? '+' : ''}${num(v)}`
const contests = { A: 'Ayuntamiento', DL: 'Diputación local', DF: 'Diputación federal', G: 'Gubernatura', S: 'Senaduría', P: 'Presidencia' }
export function HistoricalReferencePanel({ result, onResult, onPending, selectedSection, onSelectSection }: { result: UniverseMap | null; onResult: (r: UniverseMap) => void; onPending: () => void; selectedSection: string | null; onSelectSection: (id: string) => void }) {
  const { state } = useWorkspace()
  const initial = result ? referenceSettings(result) : null
  const [catalog, setCatalog] = useState<UniverseOption[]>([])
  const [choice, setChoice] = useState(result ? `${result.universe.level}:${result.universe.id}` : state.universe && state.universe.level !== 'section' ? `${state.universe.level}:${state.universe.id}` : 'state:11')
  const [contest, setContest] = useState<ElectoralContestId>(result?.contest ?? 'A')
  const [party, setParty] = useState<ReferenceParty | ''>(initial?.party ?? '')
  const [unit, setUnit] = useState<'votes'|'pp'>(initial?.unit ?? 'votes')
  const [cap, setCap] = useState(String(initial?.cap ?? 1000)), [emphasis, setEmphasis] = useState(String(initial?.emphasis ?? 0))
  const [loading, setLoading] = useState(false), [error, setError] = useState<string | null>(null)
  const controller = useRef<AbortController | null>(null)
  useEffect(() => { const abort = new AbortController(); fetchUniverseCatalog(abort.signal).then(setCatalog).catch(e=>{ if (!abort.signal.aborted) setError(String(e)) }); return ()=>{ abort.abort(); controller.current?.abort() } }, [])
  const settings = result ? referenceSettings(result) : null
  const rows = result && settings ? [...result.sections].sort((a,b)=>Number(a.sectionId)-Number(b.sectionId)).map(s=>({ section: s, row: historicalReference(s, settings.party) })) : []
  const valid = rows.filter(r=>r.row.difference !== null)
  const selected = rows.find(r=>r.section.sectionId===selectedSection)
  const stale = result && settings && (choice!==`${result.universe.level}:${result.universe.id}` || contest!==result.contest || party!==settings.party || unit!==settings.unit || Number(cap)!==settings.cap || Number(emphasis)!==settings.emphasis)
  async function query() {
    const universe = catalog.find(u=>`${u.level}:${u.id}`===choice)
    if (!universe || !party || !cap.trim() || !emphasis.trim() || !Number.isFinite(Number(cap)) || Number(cap)<=0 || !Number.isFinite(Number(emphasis)) || Number(emphasis)<0) { setError('Selecciona universo y opción; la escala debe ser positiva y la atenuación no negativa.'); return }
    controller.current?.abort(); const abort = new AbortController(); controller.current=abort
    setLoading(true); setError(null); onPending()
    try { const data = await fetchUniverseMap(universe,2024,contest,abort.signal,'concentration'); if (!abort.signal.aborted) onResult(attachHistoricalReference(data,{party,unit,cap:Number(cap),emphasis:Number(emphasis)})) }
    catch(e) { if (!abort.signal.aborted) setError(e instanceof Error ? e.message : 'Consulta no disponible.') }
    finally { if (!abort.signal.aborted) setLoading(false) }
  }
  return <section style={{padding:'20px 16px'}}>
    <h3>Eficiencia del voto · comparación histórica por sección</h3>
    <p>Datos observados de 2024. Compara una opción con la mayor votación entre las otras tres rastreadas. No calcula votos requeridos, proyecciones, transferencias ni prioridades. Cobertura parcial y fuentes en auditoría.</p>
    <label className="workspace-electoral-comparison-control"><span>Universo</span><select value={choice} disabled={loading} onChange={e=>setChoice(e.target.value)}>{catalog.map(u=><option key={`${u.level}:${u.id}`} value={`${u.level}:${u.id}`}>{u.label} · {u.level} · {u.sections} secciones</option>)}</select></label>
    <label className="workspace-electoral-comparison-control"><span>Contienda · 2024</span><select value={contest} disabled={loading} onChange={e=>setContest(e.target.value as ElectoralContestId)}>{ELECTORAL_CONTEST_IDS.map(c=><option key={c} value={c}>{contests[c]}</option>)}</select></label>
    <label className="workspace-electoral-comparison-control"><span>Opción de referencia histórica</span><select value={party} disabled={loading} onChange={e=>setParty(e.target.value as ReferenceParty|'')}><option value="">Seleccionar…</option>{REFERENCE_PARTIES.map(p=><option key={p}>{p}</option>)}</select></label>
    <label className="workspace-electoral-comparison-control"><span>Unidad del mapa</span><select value={unit} disabled={loading} onChange={e=>{setUnit(e.target.value as 'votes'|'pp');setCap(e.target.value==='pp'?'10':'1000');setEmphasis('0')}}><option value="votes">Votos</option><option value="pp">Puntos porcentuales</option></select></label>
    <label className="workspace-electoral-comparison-control"><span>Saturación de color ({unit==='votes'?'votos':'pp'})</span><input type="number" min="0.001" step="any" value={cap} disabled={loading} onChange={e=>setCap(e.target.value)}/></label>
    <label className="workspace-electoral-comparison-control"><span>Atenuar diferencias menores a ({unit==='votes'?'votos':'pp'})</span><input type="number" min="0" step="any" value={emphasis} disabled={loading} onChange={e=>setEmphasis(e.target.value)}/></label>
    <p>Estos controles solo cambian intensidad de color: no filtran filas ni alteran cifras. Azul: diferencia positiva; ocre: negativa; gris: cero o no calculable, según su estado. La escala es la misma para cualquier opción elegida.</p>
    <button type="button" className="workspace-action" disabled={loading||!catalog.length} onClick={()=>void query()}>{loading?'Consultando…':'Consultar y pintar mapa'}</button>
    {error?<p role="alert">{error}</p>:null}
    {stale?<p role="status">Cambiaste parámetros. La tabla y el mapa conservan la consulta anterior hasta pulsar «Consultar y pintar mapa».</p>:null}
    {result&&settings?<>
      <h3>{result.universe.label} · {contests[result.contest]} · 2024 · referencia {settings.party}</h3>
      <p>{rows.length} filas representadas de {result.coverage.geographic} secciones geográficas; {result.coverage.blocked} bloqueadas sin geometría publicada. {valid.length} diferencias calculables; {rows.length-valid.length} no calculables.</p>
      <p>Diferencia positiva: {valid.filter(x=>x.row.difference!>0).length} secciones; cero: {valid.filter(x=>x.row.difference===0).length}; negativa: {valid.filter(x=>x.row.difference!<0).length}. Son conteos descriptivos, no una clasificación de objetivos.</p>
      <p>Diferencia = votos observados de {settings.party} − máximo observado entre las otras opciones incluidas. pp = diferencia / total de la contienda × 100. Sin ajuste de un voto. No se suman los puntos porcentuales de distintas secciones. Mayor votación rastreada no acredita ganador absoluto.</p>
      <SectionTableSearch><div className="heyti-win-table-scroll" role="region" aria-label="Comparación histórica completa por sección" tabIndex={0}><table className="heyti-win-table heyti-section-table"><caption>Todas las secciones representadas, incluidas las no calculables. Orden por número de sección.</caption><thead><tr>{['Sección',`${settings.party}: votos 2024`,'Contraste histórico (otras opciones)','Votos de contraste','Diferencia (votos)','Diferencia (pp)','Máximo rastreado','Total contienda','Estado'].map(t=><th key={t} scope="col">{t}</th>)}</tr></thead><tbody>{rows.map(({row})=><tr data-section-id={row.sectionId} key={row.sectionId} aria-selected={selectedSection===row.sectionId} onClick={()=>onSelectSection(row.sectionId)}><th scope="row"><button type="button" aria-label={`Ver sección ${row.sectionId} en mapa y detalle`}>{row.sectionId}</button></th><td>{num(row.selected)}</td><td>{row.contrastParties.join(' / ')||'N/D'}</td><td>{num(row.contrast)}</td><td>{signed(row.difference)}</td><td>{signed(row.pp)}</td><td>{row.leaders.join(' / ')||(row.status==='NO_TRACKED_VOTES'?'Sin votos rastreados':'N/D')}</td><td>{num(row.total)}</td><td>{referenceStatusLabels[row.status] ?? 'Estado no calculable'}</td></tr>)}</tbody></table></div></SectionTableSearch>
      {selected?<section className="heyti-data-panel-detail"><h3>Detalle sección {selected.row.sectionId}</h3><p>Opciones con igual máximo se conservan juntas. Un cero observado no se convierte en faltante.</p><table className="heyti-win-table"><thead><tr><th scope="col">Opción incluida</th><th scope="col">Votos observados 2024</th></tr></thead><tbody>{REFERENCE_PARTIES.map(p=><tr key={p}><th scope="row">{p}</th><td>{num(selected.section.votes?.[p])}</td></tr>)}</tbody></table><p>Total de la contienda: {num(selected.section.total)}. Estado de la diferencia: {referenceStatusLabels[selected.row.status] ?? 'Estado no calculable'}. El resto de opciones no desglosadas no se trata como un único competidor.</p></section>:<p>Selecciona una fila o sección del mapa para ver sus datos.</p>}
      <details><summary>Fuentes y cobertura</summary><p>Solo PAN, PRI, PVEM y MORENA en este desglose. No se reconstruyen totales ni se imputan votos ausentes. Geometría actual; no se certifica equivalencia histórica territorial.</p><dl>{Object.entries(result.provenance).map(([k,v])=><div key={k}><dt>{k}</dt><dd style={{overflowWrap:'anywhere'}}>{v}</dd></div>)}</dl></details>
    </>:<p>Selecciona los parámetros para consultar. No se guarda el resultado en almacenamiento local.</p>}
  </section>
}