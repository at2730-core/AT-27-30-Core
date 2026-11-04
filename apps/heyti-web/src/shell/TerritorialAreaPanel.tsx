import { SectionTableSearch } from './SectionTableSearch'
import { useEffect, useRef, useState } from 'react'
import { useWorkspace } from '../platform/useWorkspace'
import { fetchUniverseCatalog } from '../gateway/universe.client'
import type { UniverseMap, UniverseOption } from '../gateway/universe.client'
import { ELECTORAL_CONTEST_IDS } from '../gateway/electoral.response'
import type { ElectoralContestId } from '../gateway/electoral.response'
import { AREA_PARTIES, AREA_TITLES, areaReading, attachAreaReading, loadAreaReading, rankAreaSection, summarizeArea } from './territorialAreaAnalysis'
import type { AreaKind } from './territorialAreaAnalysis'
import './WinScenarioTable.css'
const contests: Record<ElectoralContestId,string> = { A:'Ayuntamiento', DL:'Diputaciones locales', DF:'Diputaciones federales', G:'Gubernatura', S:'Senado', P:'Presidencia' }
const number = (v: number | null | undefined) => v == null ? 'N/D' : v.toLocaleString('es-MX')
export function TerritorialAreaPanel({ kind, result, onResult, onPending, selectedSection, onSelectSection }: {
  kind: AreaKind; result: UniverseMap | null; onResult: (result: UniverseMap) => void; onPending: () => void; selectedSection?: string | null; onSelectSection?: (id: string) => void
}) {
  const { state } = useWorkspace()
  const [catalog,setCatalog] = useState<UniverseOption[]>([])
  const [choice,setChoice] = useState(() => result ? result.universe.level+':'+result.universe.id : state.universe && state.universe.level !== 'section' ? state.universe.level+':'+state.universe.id : '')
  const [contest,setContest] = useState<ElectoralContestId>(result?.contest ?? 'A')
  const [year,setYear] = useState(result?.year ?? 2024)
  const [loading,setLoading] = useState(false), [error,setError] = useState<string|null>(null)
  const controller = useRef<AbortController|null>(null)
  useEffect(() => {
    const abort = new AbortController()
    fetchUniverseCatalog(abort.signal).then(options => { if (!abort.signal.aborted) setCatalog(options) }).catch(cause => { if (!abort.signal.aborted) setError(cause instanceof Error ? cause.message : 'Catálogo no disponible.') })
    return () => { abort.abort(); controller.current?.abort() }
  }, [])
  useEffect(() => {
    if (state.mode !== 'individual' || state.activeModuleId !== 'territorial-analysis') {
      controller.current?.abort(); setLoading(false)
    }
  }, [state.mode, state.activeModuleId])
  const reading = result && areaReading(result)?.kind === kind ? areaReading(result) : null
  const shown = reading ? result : null
  const stale = shown && (choice !== shown.universe.level+':'+shown.universe.id || contest !== shown.contest || year !== shown.year)
  async function query() {
    const universe = catalog.find(item => item.level+':'+item.id === choice)
    if (!universe) { setError('Selecciona un DF, DL, municipio o estado disponible.'); return }
    controller.current?.abort(); const abort = new AbortController(); controller.current = abort
    setLoading(true); setError(null); onPending()
    try { const map = await loadAreaReading(universe, contest, kind, year, abort.signal); if (!abort.signal.aborted) onResult(map) }
    catch(cause) { if (!abort.signal.aborted) setError(cause instanceof Error ? cause.message : 'Consulta no disponible.') }
    finally { if (!abort.signal.aborted) setLoading(false) }
  }
  const rows = shown ? [...shown.sections].sort((a,b) => Number(a.sectionId)-Number(b.sectionId)) : []
  const eligible = rows.filter(section => kind === 'area-comparison' ? rankAreaSection(section).completeData : rankAreaSection(section).valid)
  return <section style={{padding:'20px 16px'}} aria-label={AREA_TITLES[kind]}>
    <p className="heyti-overview-note">{kind === 'area-comparison' ? 'Compara 2018, 2021 y 2024 del universo elegido. Las coberturas calculables pueden cambiar entre años; no acredita equivalencia de límites históricos.' : kind === 'area-competitiveness' ? 'Diferencia entre los dos máximos de votos rastreados por sección. Se expresa en votos y puntos porcentuales sobre el total disponible.' : 'Primeros tres lugares entre PAN, PRI, PVEM y MORENA por sección del universo elegido. Conserva empates; no clasifica secciones por prioridad.'} Fuente de demostración en auditoría; desglose parcial y sin modalidad MR/RP identificada.</p>
    <label className="workspace-electoral-comparison-control"><span>Universo</span><select value={choice} disabled={loading || !catalog.length} onChange={event => setChoice(event.target.value)}><option value="" disabled>Selecciona DF, DL, municipio o estado</option>{(['state','municipality','federal-district','local-district'] as const).map(level => <optgroup key={level} label={{state:'Estado',municipality:'Municipios','federal-district':'Distritos federales','local-district':'Distritos locales'}[level]}>{catalog.filter(item => item.level === level).map(item => <option key={item.level+':'+item.id} value={item.level+':'+item.id}>{item.label} · {item.sections} secciones geográficas</option>)}</optgroup>)}</select></label>
    <label className="workspace-electoral-comparison-control"><span>Contienda</span><select value={contest} disabled={loading} onChange={event => setContest(event.target.value as ElectoralContestId)}>{ELECTORAL_CONTEST_IDS.map(id => <option key={id} value={id}>{contests[id]}</option>)}</select></label>
    <label className="workspace-electoral-comparison-control"><span>{kind === 'area-comparison' ? 'Año del mapa y tabla por sección' : 'Año'}</span><select value={year} disabled={loading} onChange={event => setYear(Number(event.target.value))}>{[2018,2021,2024].map(y => <option key={y} value={y}>{y}</option>)}</select></label>
    <button type="button" className="workspace-action" style={{marginTop:12}} disabled={loading || !catalog.length || !choice} onClick={() => void query()}>{loading ? 'Consultando…' : 'Consultar universo y pintar mapa'}</button>
    {error ? <p role="alert">{error}</p> : null}
    {stale ? <p role="status">La selección cambió. Mapa y tabla conservan {shown.universe.label}, {contests[shown.contest]}, {shown.year}. Pulsa «Consultar universo y pintar mapa» para actualizar.</p> : null}
    {!shown ? <p>Selecciona universo y contienda para consultar. No es necesario seleccionar una sección individual.</p> : <>
      <h3>{shown.universe.label} · {contests[shown.contest]} · {kind === 'area-comparison' ? '2018–2024' : shown.year}</h3>
      <p>{shown.coverage.represented} secciones representadas de {shown.coverage.geographic}; {shown.coverage.blocked} bloqueadas o sin geometría publicada. {eligible.length} secciones calculables en {shown.year}; {rows.length-eligible.length} no calculables para esta lectura.</p>
      {kind === 'area-comparison' && reading ? <>
        <h4>Resumen histórico del universo · cobertura calculable por año</h4>
        <div className="heyti-win-table-scroll" role="region" aria-label="Resumen histórico por año" tabIndex={0}><table className="heyti-win-table"><thead><tr>{['Año','Calculables','Total de votos',...AREA_PARTIES,'Mapa y tabla'].map(text => <th key={text} scope="col">{text}</th>)}</tr></thead><tbody>{reading.maps.map(map => {const summary=summarizeArea(map);return <tr key={map.year}><th scope="row">{map.year}</th><td>{summary.calculable}</td><td>{number(summary.total)}</td>{AREA_PARTIES.map(party => <td key={party}>{number(summary.votes[party])}</td>)}<td><button type="button" disabled={!!stale || loading} aria-pressed={shown.year===map.year} onClick={() => {setYear(map.year);onResult(attachAreaReading(reading.maps,kind,map.year))}}>Ver {map.year}</button></td></tr>})}</tbody></table></div>
        <p>Sumas de votos únicamente sobre secciones con total positivo y desglose completo y consistente en cada año. N/D indica ausencia de cobertura calculable; no equivale a cero. El mapa y la siguiente tabla muestran {shown.year}.</p>
      </> : null}
      {kind === 'area-competitiveness' ? <p>Cortes descriptivos heredados de V1: menos de 5 pp, de 5 a menos de 10 pp y 10 pp o más. Son diferencias históricas entre cuatro partidos; no acreditan ganador absoluto ni garantizan elecciones futuras.</p> : null}
      {kind === 'area-top3' ? <p>Los empates comparten posición: 1, 1, 3. Se incluyen todos los partidos ubicados en los primeros tres lugares; por empate pueden aparecer cuatro. Total cero o desglose incompleto no asignan posiciones.</p> : null}
      <SectionTableSearch><div className="heyti-win-table-scroll" role="region" aria-label={`${AREA_TITLES[kind]} por sección, ${shown.year}`} tabIndex={0}><table className="heyti-win-table heyti-section-table"><caption>{shown.universe.label} · {contests[shown.contest]} · {shown.year} · todas las secciones representadas</caption><thead><tr><th scope="col">Sección</th><th scope="col">Total</th>{kind === 'area-competitiveness' ? <><th scope="col">Máximo rastreado</th><th scope="col">Segundo valor</th><th scope="col">Diferencia votos</th><th scope="col">Diferencia pp</th><th scope="col">Lectura</th></> : kind === 'area-top3' ? <th scope="col">Primeros tres lugares con empates</th> : AREA_PARTIES.map(party => <th key={party} scope="col">{party}</th>)}<th scope="col">Estado</th></tr></thead><tbody>{rows.map(section => {const ranked=rankAreaSection(section);return <tr data-section-id={section.sectionId} key={section.sectionId} aria-selected={selectedSection===section.sectionId} onClick={() => onSelectSection?.(section.sectionId)}><th scope="row"><button type="button" aria-label={'Acercar sección '+section.sectionId}>{section.sectionId}</button></th><td>{number(section.total)}</td>{kind === 'area-competitiveness' ? <><td>{ranked.valid ? ranked.rows.filter(row => row.rank===1).map(row => row.party).join(' / ')+' · '+number(ranked.rows[0].votes) : 'N/D'}</td><td>{ranked.valid ? number(ranked.rows[1].votes) : 'N/D'}</td><td>{number(ranked.margin)}</td><td>{ranked.points === null ? 'N/D' : ranked.points.toLocaleString('es-MX',{maximumFractionDigits:3})+' pp'}</td><td>{ranked.band ?? 'No calculable'}</td></> : kind === 'area-top3' ? <td>{ranked.valid ? ranked.top.map(row => `${row.rank}º ${row.party}: ${number(row.votes)}`).join(' · ') : 'N/D'}</td> : AREA_PARTIES.map(party => <td key={party}>{number(section.votes?.[party])}</td>)}<td>{ranked.reason}</td></tr>})}</tbody></table></div></SectionTableSearch>
      <p>El mapa muestra límites de secciones en tono neutro, con selección verde; las métricas se consultan en la tabla. Los datos faltantes permanecen visibles. El total no se reconstruye sumando cuatro partidos. Municipios y distritos corresponden a la geometría actual.</p>
      <details><summary>Fuente y trazabilidad</summary><dl>{Object.entries(shown.provenance).map(([key,value]) => <div key={key}><dt>{key}</dt><dd style={{overflowWrap:'anywhere'}}>{value}</dd></div>)}</dl></details>
    </>}
  </section>
}
