import { MasterOnlyCoverageNote } from './DataScopeNotes'
import { Results2024Table } from './Results2024Table'
import { attachResults2024 } from './results2024'
import { DataAlertsDetails } from './DataAlertsDetails'
import { HistoricalMarginDetails } from './HistoricalMarginDetails'
import { participationValue, participationCounts } from './participation'
import { useEffect, useRef, useState } from 'react'
import { useWorkspace } from '../platform/useWorkspace'
import { fetchUniverseCatalog, fetchUniverseMap } from '../gateway/universe.client'
import type { UniverseMap, UniverseOption } from '../gateway/universe.client'
import { ELECTORAL_CONTEST_IDS } from '../gateway/electoral.response'
import type { ElectoralContestId } from '../gateway/electoral.response'
import { outcomeColors, sectionOutcomeLabel } from './UniverseGeometryMap'
const labels = { A: 'Ayuntamiento', DL: 'Diputación local', DF: 'Diputación federal', G: 'Gubernatura', S: 'Senaduría', P: 'Presidencia' }
export function UniverseQueryPanel({ result, onResult, onPending, metric = 'leaders', participation = false, historicalMarginMode = false, dataAlertsMode = false, results2024Mode = false, selectedSection, onSelectSection }: { results2024Mode?: boolean; selectedSection?: string | null; onSelectSection?: (id: string) => void; dataAlertsMode?: boolean; historicalMarginMode?: boolean; participation?: boolean; metric?: 'leaders' | 'abstention' | 'concentration'; result: UniverseMap | null; onResult: (result: UniverseMap) => void; onPending: () => void }) {
  const { state } = useWorkspace()
  const [catalog, setCatalog] = useState<UniverseOption[]>([])
  const [choice, setChoice] = useState(() => result ? `${result.universe.level}:${result.universe.id}` : state.universe && state.universe.level !== 'section' ? `${state.universe.level}:${state.universe.id}` : 'state:11')
  const [year, setYear] = useState(metric === 'concentration' ? 2024 : result?.year ?? 2024)
  const [contest, setContest] = useState<ElectoralContestId>(result?.contest ?? 'A')
  const [loading, setLoading] = useState(false), [error, setError] = useState<string | null>(null)
  const controller = useRef<AbortController | null>(null)
  useEffect(() => {
    const abort = new AbortController()
    fetchUniverseCatalog(abort.signal).then(setCatalog).catch(e => { if (!abort.signal.aborted) setError(e instanceof Error ? e.message : 'Catálogo no disponible.') })
    return () => { abort.abort(); controller.current?.abort() }
  }, [])
  const actionLabel = results2024Mode ? 'Consultar resultados 2024' : 'Pintar mapa'
  const stale = result && (choice !== `${result.universe.level}:${result.universe.id}` || year !== result.year || contest !== result.contest)
  async function query() {
    const universe = catalog.find(u => `${u.level}:${u.id}` === choice)
    if (!universe) { setError('Selecciona un universo disponible.'); return }
    controller.current?.abort()
    const abort = new AbortController(); controller.current = abort
    setLoading(true); setError(null); onPending()
    try { const data = results2024Mode ? attachResults2024(...await Promise.all([fetchUniverseMap(universe,2024,contest,abort.signal,'concentration'),fetchUniverseMap(universe,2024,contest,abort.signal,'abstention')])) : await fetchUniverseMap(universe, year, contest, abort.signal, metric); if (!abort.signal.aborted) onResult(data) }
    catch (e) { if (!abort.signal.aborted) setError(e instanceof Error ? e.message : 'Consulta no disponible.') }
    finally { if (!abort.signal.aborted) setLoading(false) }
  }
  return <section style={{ padding: '20px 16px' }}>
    <p className="heyti-overview-note">{results2024Mode ? 'Consulta los resultados de 2024 por universo y contienda. Datos pendientes de validación; sin estimaciones.' : dataAlertsMode ? 'Revisa total, desglose rastreado, faltantes, ceros e inconsistencias de 2024 por sección. No son alertas de riesgo de campaña. Disponible no significa certificado. Geometría actual; fuentes en auditoría.' : historicalMarginMode ? 'Compara los dos máximos de votación entre PAN, PRI, PVEM y MORENA para 2024. Votos y puntos porcentuales; cobertura parcial y fuentes en auditoría. No acredita ganador absoluto. No usa proyecciones 2027 ni calcula objetivos de campaña.' : participation ? 'Participación = votos totales / lista nominal × 100. Usa los totales y lista nominal validados por el CORE, sin sustituir faltantes por sumas de partidos. Geometría actual; fuentes en auditoría. Este bloque muestra 2018, 2021 y 2024; los escenarios 2027 se integrarán por separado.' : metric === 'concentration' ? 'Índice parcial = suma de (votos de cada partido rastreado / votos totales)². Solo PAN, PRI, PVEM y MORENA; no es el HHI completo. Año 2024 y geometría actual.' : metric === 'abstention' ? 'Abstención = (lista nominal − votos totales) / lista nominal × 100. Usa el total de la contienda, sin sustituirlo por la suma de cuatro partidos. Municipios y distritos corresponden a la geometría actual.' : 'Mayor votación entre PAN, PRI, PVEM y MORENA. No acredita ganadores absolutos. Municipios y distritos corresponden al GeoJSON actual, también al consultar años anteriores.'}</p>
    <label className="workspace-electoral-comparison-control"><span>Universo</span><select value={choice} disabled={loading || !catalog.length} onChange={e => setChoice(e.target.value)}>
      {['state', 'municipality', 'federal-district', 'local-district'].map(level => <optgroup key={level} label={{ state: 'Estado', municipality: 'Municipios', 'federal-district': 'Distritos federales', 'local-district': 'Distritos locales' }[level]}>
        {catalog.filter(u => u.level === level).map(u => <option key={u.id} value={`${level}:${u.id}`}>{u.label} · {u.sections} secciones geográficas</option>)}
      </optgroup>)}
    </select></label>
    {!results2024Mode ? <label className="workspace-electoral-comparison-control"><span>Año</span><select value={year} disabled={loading || metric === 'concentration'} onChange={e => setYear(Number(e.target.value))}>{[2018, 2021, 2024].map(y => <option key={y}>{y}</option>)}</select></label> : null}
    <label className="workspace-electoral-comparison-control"><span>Contienda</span><select value={contest} disabled={loading} onChange={e => setContest(e.target.value as ElectoralContestId)}>{ELECTORAL_CONTEST_IDS.map(c => <option key={c} value={c}>{labels[c]}</option>)}</select></label>
    <button type="button" className="workspace-action" style={{ marginTop: 12 }} disabled={loading || !catalog.length} onClick={() => void query()}>{loading ? 'Consultando…' : actionLabel}</button>
    {error ? <p role="alert">{error}</p> : null}
    {stale ? <p role="status">La selección cambió. Pulsa «{actionLabel}» para actualizar. El resultado mostrado conserva sus parámetros anteriores.</p> : null}
    {result ? <>
      <h3>{result.universe.label} · {result.year} · {labels[result.contest]}</h3>
      <p>Universo actual ({result.universe.label}): {result.coverage.represented} secciones representadas de {result.coverage.geographic}; {result.coverage.blocked} bloqueadas sin geometría publicada.</p>
      {results2024Mode ? <Results2024Table result={result} selectedSection={selectedSection} onSelectSection={onSelectSection} /> : dataAlertsMode ? <DataAlertsDetails result={result} /> : historicalMarginMode ? <HistoricalMarginDetails result={result} /> : <>
      <ul style={{ listStyle: 'none', padding: 0 }}>{Object.entries(participation ? participationCounts(result) : result.counts).sort(([a], [b]) => participation ? ['PART_LOW', 'PART_MID', 'PART_HIGH', 'INCONSISTENT', 'NO_DATA', 'NOT_CONTESTED'].indexOf(a) - ['PART_LOW', 'PART_MID', 'PART_HIGH', 'INCONSISTENT', 'NO_DATA', 'NOT_CONTESTED'].indexOf(b) : metric === 'concentration' ? ['HHI_LOW', 'HHI_MID', 'HHI_HIGH', 'INCONSISTENT', 'ZERO_TOTAL', 'NO_DATA', 'NOT_CONTESTED'].indexOf(a) - ['HHI_LOW', 'HHI_MID', 'HHI_HIGH', 'INCONSISTENT', 'ZERO_TOTAL', 'NO_DATA', 'NOT_CONTESTED'].indexOf(b) : 0).map(([k, n]) => <li key={k} style={{ display: 'flex', gap: 8, margin: '10px 0' }}><span aria-hidden="true" style={{ width: 14, height: 14, background: outcomeColors[k] }} />{sectionOutcomeLabel(metric, k, k === 'NO_DATA' && result.sections.filter(s => s.status === 'NO_DATA').every(s => s.missingReason === 'TRACKED_BREAKDOWN_MISSING') ? 'TRACKED_BREAKDOWN_MISSING' : undefined)}: <strong>{n}</strong></li>)}</ul>
      {metric === 'concentration' && result.summary ? <>
        <h3>Concentración del universo · parcial</h3>
        <p><strong>Índice: {result.summary.index === null ? 'No calculable' : result.summary.index.toFixed(3)}</strong></p>
        <p>{result.summary.validSections} secciones calculables · {result.summary!.total.toLocaleString('es-MX')} votos totales</p>
        <p>Votos cubiertos por los cuatro partidos: {result.summary.trackedCoverage === null ? 'N/D' : `${(result.summary.trackedCoverage*100).toFixed(1)}%`}</p>
        {Object.entries(result.summary.votes).map(([party,votes]) => <div key={party} style={{ marginBottom: 12 }}><strong>{party}: {votes.toLocaleString('es-MX')}</strong>
          {result.summary!.total > 0 ? <div style={{ height: 10, background: '#edf2f7', marginTop: 6 }}><div style={{ width: `${votes/result.summary!.total*100}%`, height: '100%', background: outcomeColors[party] }} /></div> : null}
        </div>)}
        <p className="heyti-party-chart-note">El índice del universo se calcula con las sumas de votos; no promedia los índices del mapa. Los votos no desglosados no se inventan ni se agrupan como un partido. No se calcula ENP con este índice parcial. Cortes descriptivos de V1: 0.30 y 0.45; no certifican competitividad.</p>
      </> : null}
      </>}
      {metric === 'abstention' && result.trend ? <>
        <h3>Tendencia 2018–2024</h3>
        <p className="heyti-overview-note">Porcentaje ponderado: suma de votos y lista nominal solo de secciones calculables en cada año. La cobertura puede cambiar entre años.</p>
        {result.trend.map(t => <div key={t.year} style={{ marginBottom: 16 }}>
          <strong>{t.year} · {t.abstention === null ? 'No calculable' : `${(participation ? participationValue(t.abstention)! : t.abstention).toFixed(1)}%`}</strong>
          <p>{t.validSections} secciones calculables · LN {t.nominal.toLocaleString('es-MX')} · votos {t.votes.toLocaleString('es-MX')}</p>
          {t.abstention !== null ? <div style={{ height: 10, background: '#edf2f7', borderRadius: 5 }}><div style={{ width: `${participation ? participationValue(t.abstention) : t.abstention}%`, height: '100%', background: '#2a9d8f', borderRadius: 5 }} /></div> : null}
        </div>)}
        <p className="heyti-party-chart-note">{participation ? 'Escala fija de 0 a 100%. Rangos descriptivos de V1: menos de 30%, de 30% a menos de 50%, de 50% a 100%; no son un semáforo certificado. Un total cero con lista nominal válida produce 0%; requiere auditoría para interpretar su causa.' : 'Escala fija de 0 a 100%. Rangos descriptivos de 25 puntos; no son un semáforo certificado. Un total cero con lista nominal válida produce 100%; no confirma por sí mismo ausencia de votantes.'} Sin lista nominal válida no se calcula. Las cifras siguen pendientes de auditoría.</p>
      </> : null}
      {!results2024Mode ? <p className="heyti-party-chart-note">Los ceros se conservan y no asignan partido. Los datos faltantes, empates y elecciones no celebradas tienen categorías propias. </p> : null}
      <MasterOnlyCoverageNote count={result.coverage.masterOnlyUnmapped} />
      <details><summary>Trazabilidad del mapa</summary><dl className="workspace-truth-details">{Object.entries(result.provenance).map(([k, v]) => <div key={k}><dt>{k}</dt><dd style={{ overflowWrap: 'anywhere' }}>{v}</dd></div>)}</dl></details>
    </> : <p>{results2024Mode ? 'Selecciona universo y contienda para consultar 2024.' : 'Selecciona universo, año y puesto para consultar el CORE.'} Los resultados no se guardan en almacenamiento local.</p>}
  </section>
}
