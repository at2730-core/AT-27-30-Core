import { SectionTableSearch } from './SectionTableSearch'
import { DistributionScenarioDetails } from './DistributionScenarioDetails'
import { Participation2027Table } from './Participation2027Table'
import { buildDescriptiveScenario } from './descriptiveScenario'
import { PartyComparisonDetails } from './PartyComparisonDetails'
import { buildParticipationGoals, goalLabels } from './participationGoals'
import { useEffect, useRef, useState } from 'react'
import { useWorkspace } from '../platform/useWorkspace'
import { fetchUniverseCatalog, fetchUniverseMap } from '../gateway/universe.client'
import type { UniverseOption } from '../gateway/universe.client'
import { ELECTORAL_CONTEST_IDS } from '../gateway/electoral.response'
import type { ElectoralContestId } from '../gateway/electoral.response'
import { buildParticipationScenario, scenarioLabels } from './participationScenario'
import type { ParticipationScenario } from './participationScenario'
import { outcomeColors } from './UniverseGeometryMap'
const contests = { A: 'Ayuntamiento', DL: 'Diputación local', DF: 'Diputación federal', G: 'Gubernatura', S: 'Senaduría', P: 'Presidencia' }
export function ParticipationScenarioPanel({ result, onPending, onResult, goalsMode = false, distributionMode = false, comparisonMode = false, tableMode = false, selectedSection, onSelectSection }: { distributionMode?: boolean; tableMode?: boolean; comparisonMode?: boolean; selectedSection?: string | null; onSelectSection?: (id: string) => void; goalsMode?: boolean; result: ParticipationScenario | null; onPending: () => void; onResult: (result: ParticipationScenario) => void }) {
  const { state } = useWorkspace()
  const [catalog, setCatalog] = useState<UniverseOption[]>([])
  const [choice, setChoice] = useState(result ? `${result.base.universe.level}:${result.base.universe.id}` : state.universe && state.universe.level !== 'section' ? `${state.universe.level}:${state.universe.id}` : 'state:11')
  const [contest, setContest] = useState<ElectoralContestId>(result?.base.contest ?? 'A')
  const [target, setTarget] = useState(String(result?.goals?.target ?? 50))
  const [tolerance, setTolerance] = useState(String(result?.goals?.tolerance ?? 3))
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
    if (goalsMode && (!target.trim() || !tolerance.trim() || ![Number(target), Number(tolerance)].every(n => Number.isFinite(n) && n >= 0 && n <= 100))) { setError('Meta y tolerancia deben ser números de 0 a 100.'); return }
    controller.current?.abort(); const abort = new AbortController(); controller.current = abort
    setLoading(true); setError(null); onPending()
    try {
      const maps = await Promise.all([...([2018, 2021, 2024].map(year => fetchUniverseMap(universe, year, contest, abort.signal, 'abstention'))), ...((comparisonMode || distributionMode) ? [fetchUniverseMap(universe, 2024, contest, abort.signal, 'concentration')] : [])])
      if (!abort.signal.aborted) {
        const scenario = buildParticipationScenario(maps.slice(0, 3))
        onResult(tableMode ? { ...scenario, tableOnly: true } : distributionMode ? { ...buildDescriptiveScenario(maps), distributionOnly: true } : comparisonMode ? buildDescriptiveScenario(maps) : goalsMode ? { ...scenario, goals: buildParticipationGoals(scenario, Number(target), Number(tolerance)) } : scenario)
      }
    } catch (e) { if (!abort.signal.aborted) { setError(e instanceof Error ? e.message : 'Escenario no disponible.'); abort.abort(); setLoading(false) } }
    finally { if (!abort.signal.aborted) setLoading(false) }
  }
  const stale = result && (choice !== `${result.base.universe.level}:${result.base.universe.id}` || contest !== result.base.contest || (goalsMode && (Number(target) !== result.goals?.target || Number(tolerance) !== result.goals?.tolerance)))
  return <section style={{ padding: '20px 16px' }}>
    <p><strong>{tableMode ? 'Tabla de participación estimada 2027' : distributionMode ? 'Distribución de votación por sección · escenario 2027' : comparisonMode ? 'Escenario descriptivo 2027 · comparación con 2024' : goalsMode ? 'Metas de participación 2027 · escenario estimado' : 'Escenario 2027 · estimación'}</strong></p>
    <p className="heyti-overview-note">Extrapola participación histórica disponible. No es resultado electoral, probabilidad ni garantía. Fuentes en auditoría; geometría actual. No se proyecta lista nominal 2027. El año del escenario no implica que esa contienda se celebre en 2027.</p>
    <p className="heyti-overview-note">A/DL/DF: regresión ponderada (2018: 1, 2021: 1.5, 2024: 2). G/S/P: p2024 + 0.3 × (p2024 − p2018). Se requieren 2024 y al menos otro año válido; G/S/P requieren 2018 y 2024. Una cifra inconsistente en un año utilizado bloquea el cálculo. Valores fuera de rango se limitan a 0–100% y se señalan.</p>
    <label className="workspace-electoral-comparison-control"><span>Universo</span><select disabled={loading || !catalog.length} value={choice} onChange={e => setChoice(e.target.value)}>
      {['state', 'municipality', 'federal-district', 'local-district'].map(level => <optgroup key={level} label={{ state: 'Estado', municipality: 'Municipios', 'federal-district': 'Distritos federales', 'local-district': 'Distritos locales' }[level]}>{catalog.filter(u => u.level === level).map(u => <option key={u.id} value={`${u.level}:${u.id}`}>{u.label} · {u.sections} secciones geográficas</option>)}</optgroup>)}
    </select></label>
    <label className="workspace-electoral-comparison-control"><span>Año del escenario</span><select disabled value="2027"><option>2027</option></select></label>
    <label className="workspace-electoral-comparison-control"><span>Contienda</span><select disabled={loading} value={contest} onChange={e => setContest(e.target.value as ElectoralContestId)}>{ELECTORAL_CONTEST_IDS.map(c => <option key={c} value={c}>{contests[c]}</option>)}</select></label>
    {goalsMode ? <>
      <label className="workspace-electoral-comparison-control"><span>Meta de participación (%)</span><input type="number" min="0" max="100" step="0.1" value={target} disabled={loading} onChange={e => setTarget(e.target.value)} /></label>
      <label className="workspace-electoral-comparison-control"><span>Tolerancia debajo de la meta (pp)</span><input type="number" min="0" max="100" step="0.1" value={tolerance} disabled={loading} onChange={e => setTolerance(e.target.value)} /></label>
      <p className="heyti-overview-note">Cumple: estimación ≥ meta. Cerca: debajo de la meta, hasta la tolerancia inclusive. Debajo: brecha mayor que la tolerancia. Las categorías son descriptivas, sin garantía de cumplimiento real. Cambiar parámetros requiere volver a calcular.</p>
    </> : null}
    <button type="button" className="workspace-action" style={{ marginTop: 12 }} disabled={loading || !catalog.length} onClick={() => void query()}>{loading ? 'Consultando históricos…' : distributionMode ? 'Calcular distribución y pintar mapa' : comparisonMode ? 'Calcular comparación' : goalsMode ? 'Calcular y pintar metas' : 'Calcular y pintar escenario'}</button>
    {error ? <p role="alert">{error}</p> : null}
    {stale ? <p role="status">Cambiaste la selección. Calcula el escenario para actualizarlo.</p> : null}
    {result ? <>
      <h3>{result.base.universe.label} · {result.distributionOnly ? 'Distribución de votación por sección' : result.comparison ? 'Comparación descriptiva 2027' : result.goals ? 'Metas 2027' : 'Escenario 2027'} · {contests[result.base.contest]}</h3>
      <p><strong>Participación estimada: {result.percent === null ? 'No calculable' : `${result.percent.toFixed(1)}%`}</strong></p>
      <p>{result.validSections} secciones calculables; {result.base.coverage.represented - result.validSections} no calculables. {result.base.coverage.blocked} bloqueadas sin geometría publicada.</p>
      <p className="heyti-overview-note">Promedio ponderado por lista nominal 2024 solo de secciones calculables: {result.nominal.toLocaleString('es-MX')}. No se compara automáticamente con promedios históricos de distinta cobertura.</p>
      {tableMode ? <Participation2027Table scenario={result} selectedSection={selectedSection} onSelectSection={onSelectSection} /> : result.distributionOnly ? <DistributionScenarioDetails scenario={result} selectedSection={selectedSection} onSelectSection={onSelectSection} /> : result.comparison ? <PartyComparisonDetails scenario={result} selectedSection={selectedSection} onSelectSection={onSelectSection} /> : result.goals ? <>
        <p><strong>Meta: {result.goals.target}% · tolerancia: {result.goals.tolerance} pp</strong></p>
        <ul style={{ listStyle: 'none', padding: 0 }}>{['GOAL_PASS', 'GOAL_NEAR', 'GOAL_FAIL', 'INCONSISTENT', 'NO_DATA'].filter(k => result.goals!.counts[k]).map(k => <li key={k} style={{ display: 'flex', gap: 8, margin: '10px 0' }}><span aria-hidden="true" style={{ width: 14, height: 14, background: outcomeColors[k] }} />{goalLabels[k]}: <strong>{result.goals!.counts[k]}</strong></li>)}</ul>
        <h3>Hasta 20 secciones con mayor brecha</h3>
        <p className="heyti-overview-note">Brecha en puntos porcentuales = meta − participación estimada. Solo secciones calculables por debajo de la meta. No equivale a votos adicionales ni a una probabilidad.</p>
        {result.goals.worst.length ? <SectionTableSearch><table className="heyti-section-table" style={{ width: '100%', borderCollapse: 'collapse' }}><thead><tr><th scope="col">Sección</th><th scope="col">Estimación</th><th scope="col">Brecha (pp)</th></tr></thead><tbody>{result.goals.worst.map(row => <tr data-section-id={row.sectionId} key={row.sectionId} aria-selected={selectedSection===row.sectionId} onClick={()=>onSelectSection?.(row.sectionId)}><td><button type="button" aria-label={`Ver sección ${row.sectionId}`}>{row.sectionId}</button></td><td>{row.percent!.toFixed(1)}%</td><td>{row.gap!.toFixed(1)}</td></tr>)}</tbody></table></SectionTableSearch> : <p>Sin brechas calculables por debajo de la meta.</p>}
      </> : <ul style={{ listStyle: 'none', padding: 0 }}>{['PART_LOW', 'PART_MID', 'PART_HIGH', 'INCONSISTENT', 'NO_DATA'].filter(k => result.counts[k]).map(k => <li key={k} style={{ display: 'flex', gap: 8, margin: '10px 0' }}><span aria-hidden="true" style={{ width: 14, height: 14, background: outcomeColors[k] }} />{scenarioLabels[k]}: <strong>{result.counts[k]}</strong></li>)}</ul>}
      <p>{result.reducedSections} estimaciones con solo dos años en contiendas trienales; {result.clampedSections} estimaciones limitadas a 0–100%.</p>
      <details><summary>Método y trazabilidad del escenario</summary><p>{result.method}. Cálculo de escenario en la interfaz a partir de respuestas históricas del CORE validadas; no modifica los históricos.</p><dl className="workspace-truth-details">{Object.entries(result.base.provenance).map(([k, v]) => <div key={k}><dt>{k}</dt><dd style={{ overflowWrap: 'anywhere' }}>{v}</dd></div>)}</dl></details>
    </> : <p>Selecciona universo y contienda para calcular el escenario. Sin datos suficientes no se estima. No se guarda el resultado en almacenamiento local.</p>}
  </section>
}
