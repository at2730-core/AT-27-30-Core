import { useEffect, useRef, useState } from 'react'
import { useWorkspace } from '../platform/useWorkspace'
import { fetchUniverseCatalog, fetchUniverseMap } from '../gateway/universe.client'
import type { UniverseOption } from '../gateway/universe.client'
import { ELECTORAL_CONTEST_IDS } from '../gateway/electoral.response'
import type { ElectoralContestId } from '../gateway/electoral.response'
import { buildElectoralStability, stabilityLabels } from './electoralStability'
import type { ElectoralStability } from './electoralStability'
import { outcomeColors } from './UniverseGeometryMap'
const contests = { A: 'Ayuntamiento', DL: 'Diputación local', DF: 'Diputación federal', G: 'Gubernatura', S: 'Senaduría', P: 'Presidencia' }
export function ElectoralStabilityPanel({ result, onPending, onResult }: { result: ElectoralStability | null; onPending: () => void; onResult: (result: ElectoralStability) => void }) {
  const { state } = useWorkspace()
  const [catalog, setCatalog] = useState<UniverseOption[]>([])
  const [choice, setChoice] = useState(result ? `${result.base.universe.level}:${result.base.universe.id}` : state.universe && state.universe.level !== 'section' ? `${state.universe.level}:${state.universe.id}` : 'state:11')
  const [contest, setContest] = useState<ElectoralContestId>(result?.base.contest ?? 'A')
  const [loading, setLoading] = useState(false), [error, setError] = useState<string | null>(null)
  const controller = useRef<AbortController | null>(null)
  useEffect(() => {
    const abort = new AbortController()
    fetchUniverseCatalog(abort.signal).then(setCatalog).catch(e => { if (!abort.signal.aborted) setError(e instanceof Error ? e.message : 'Catálogo no disponible.') })
    return () => { abort.abort(); controller.current?.abort() }
  }, [])
  async function query() {
    const universe = catalog.find(u => `${u.level}:${u.id}` === choice)
    if (!universe) { setError('Selecciona un universo disponible.'); return }
    controller.current?.abort(); const abort = new AbortController(); controller.current = abort
    setLoading(true); setError(null); onPending()
    try {
      const years = ['G', 'S', 'P'].includes(contest) ? [2018, 2024] : [2018, 2021, 2024]
      const maps = await Promise.all(years.map(year => fetchUniverseMap(universe, year, contest, abort.signal, 'leaders')))
      if (!abort.signal.aborted) onResult(buildElectoralStability(maps))
    } catch (e) { if (!abort.signal.aborted) { setError(e instanceof Error ? e.message : 'Consulta no disponible.'); abort.abort(); setLoading(false) } }
    finally { if (!abort.signal.aborted) setLoading(false) }
  }
  const stale = result && (choice !== `${result.base.universe.level}:${result.base.universe.id}` || contest !== result.base.contest)
  return <section style={{ padding: '20px 16px' }}>
    <p className="heyti-overview-note">Continuidad de la mayor votación entre PAN, PRI, PVEM y MORENA. Cobertura parcial: no identifica ganadores absolutos ni acredita bastiones. Fuentes en auditoría; agrupación por geometría actual.</p>
    <p className="heyti-overview-note">A/DL/DF: se requieren 2018, 2021 y 2024; G/S/P: 2018 y 2024. Alta = un mismo partido; media = dos distintos; baja = tres distintos. Se cuentan partidos distintos, no cambios consecutivos: PAN–MORENA–PAN se clasifica como media. Sin liderazgo único calculable en todos los años requeridos no se asigna estabilidad.</p>
    <label className="workspace-electoral-comparison-control"><span>Universo</span><select disabled={loading || !catalog.length} value={choice} onChange={e => setChoice(e.target.value)}>
      {['state', 'municipality', 'federal-district', 'local-district'].map(level => <optgroup key={level} label={{ state: 'Estado', municipality: 'Municipios', 'federal-district': 'Distritos federales', 'local-district': 'Distritos locales' }[level]}>{catalog.filter(u => u.level === level).map(u => <option key={u.id} value={`${u.level}:${u.id}`}>{u.label} · {u.sections} secciones geográficas</option>)}</optgroup>)}
    </select></label>
    <label className="workspace-electoral-comparison-control"><span>Periodo</span><select disabled value="2018–2024"><option>2018–2024</option></select></label>
    <label className="workspace-electoral-comparison-control"><span>Contienda</span><select disabled={loading} value={contest} onChange={e => setContest(e.target.value as ElectoralContestId)}>{ELECTORAL_CONTEST_IDS.map(c => <option key={c} value={c}>{contests[c]}</option>)}</select></label>
    <button type="button" className="workspace-action" style={{ marginTop: 12 }} disabled={loading || !catalog.length} onClick={() => void query()}>{loading ? 'Consultando históricos…' : 'Pintar mapa'}</button>
    {error ? <p role="alert">{error}</p> : null}
    {stale ? <p role="status">Cambiaste la selección. Pulsa «Pintar mapa» para actualizar el resultado.</p> : null}
    {result ? <>
      <h3>{result.base.universe.label} · Estabilidad 2018–2024 · {contests[result.base.contest]}</h3>
      <p>{result.base.coverage.represented} secciones representadas de {result.base.coverage.geographic}; {result.base.coverage.blocked} bloqueadas sin geometría publicada.</p>
      <p><strong>{result.validSections} calculables</strong>; {result.base.coverage.represented - result.validSections} no calculables. Años requeridos: {result.years.join(', ')}.</p>
      <ul style={{ listStyle: 'none', padding: 0 }}>{['STAB_HIGH', 'STAB_MID', 'STAB_LOW', 'INCONSISTENT', 'NO_DATA', 'ZERO_TOTAL', 'TIE', 'NO_TRACKED_VOTES', 'NOT_CONTESTED'].filter(k => result.counts[k]).map(k => <li key={k} style={{ display: 'flex', gap: 8, margin: '10px 0' }}><span aria-hidden="true" style={{ width: 14, height: 14, background: outcomeColors[k] }} />{stabilityLabels[k]}: <strong>{result.counts[k]}</strong></li>)}</ul>
      <p className="heyti-party-chart-note">Pulsa una sección en el mapa para revisar su secuencia por año. Las categorías describen continuidad entre partidos rastreados; no predicen una elección futura. Cuando hay más de una causa, se muestra primero: inconsistencia, faltantes, total cero, empate, sin votos rastreados o no celebrada. El detalle conserva cada año y su estado.</p>
      <details><summary>Método y trazabilidad</summary><p>Categorías de V1 por número de partidos distintos, con validación estricta de todos los años requeridos. Cálculo en la interfaz sobre respuestas históricas del CORE validadas, sin modificar fuentes.</p><dl className="workspace-truth-details">{Object.entries(result.base.provenance).map(([k, v]) => <div key={k}><dt>{k}</dt><dd style={{ overflowWrap: 'anywhere' }}>{v}</dd></div>)}</dl></details>
    </> : <p>Selecciona universo y contienda para consultar los históricos. Los faltantes no se convierten a cero ni se rellenan.</p>}
  </section>
}
