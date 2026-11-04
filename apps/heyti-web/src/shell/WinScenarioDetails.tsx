import { SectionTableSearch } from './SectionTableSearch'
import './WinScenarioTable.css'
import { useEffect, useRef } from 'react'
import { WIN_PARTIES, winLabels } from './winScenario'
import type { ParticipationScenario } from './participationScenario'
import { outcomeColors } from './UniverseGeometryMap'
const num = (v: number | null) => v === null ? 'N/D' : v.toLocaleString('es-MX')
export function WinScenarioDetails({ scenario, selectedSection, onSelectSection }: { scenario: ParticipationScenario; selectedSection?: string | null; onSelectSection?: (id: string) => void }) {
  const detailRef = useRef<HTMLDivElement>(null)
  useEffect(() => { if (selectedSection) detailRef.current?.scrollIntoView({ block: 'nearest', behavior: 'smooth' }) }, [selectedSection])
  const win = scenario.win!
  const selected = selectedSection ? win.rows[selectedSection] : null
  return <section className="heyti-data-panel">
    <header className="heyti-data-panel-header">
      <h3>Comparación parcial para {win.party}</h3>
      <span className="heyti-data-panel-badge">Escenario</span>
    </header>
    <p><strong>{win.validSections} secciones calculables</strong>; {scenario.base.coverage.represented - win.validSections} no calculables. {win.aheadSections} con liderazgo único de {win.party} en el escenario rastreado.</p>
    <p>Suma aritmética de adiciones mínimas entre calculables: <strong>{num(win.additionalTotal)}</strong>. Incluye {win.exceedsCapacity} secciones cuyo umbral excede la capacidad restante de LN 2024; no es una meta garantizada ni suma de un universo completo si hay faltantes.</p>
    <ul style={{ listStyle: 'none', padding: 0 }}>{Object.entries(win.counts).map(([k, n]) => <li key={k} style={{ display: 'flex', gap: 8, margin: '10px 0' }}><span aria-hidden="true" style={{ width: 14, height: 14, background: outcomeColors[k] ?? '#94a3b8' }} />{winLabels[k] ?? `${k}: liderazgo rastreado estimado`}: <strong>{n}</strong></li>)}</ul>
    <details open><summary>Supuestos, cálculo y límites</summary>
      <p>1. Participación 2027: escenario histórico descrito arriba. Lista nominal utilizada: 2024, sin proyectarla a 2027.</p>
      <p>2. Total estimado = LN 2024 × participación estimada / 100, redondeado al entero más próximo.</p>
      <p>3. Se conservan las proporciones de votos de 2024 respecto al total de la contienda. Los cuatro partidos y el residuo se reparten por restos mayores; las sumas enteras coinciden con el total estimado. Los empates de restos se resuelven por PAN, PRI, PVEM, MORENA y residuo. El residuo incluye lo no desglosado entre esos cuatro: no es un partido ni un rival identificado.</p>
      <p>4. Adición mínima: max(0, votos del rival rastreado más alto − votos del partido elegido + 1). Supone rivales sin cambios y votos nuevos para el partido elegido. Si ya lidera de forma única, es cero. Empatar no basta.</p>
      <p>5. Transferencia hipotética: votos trasladados desde un único rival rastreado más alto al partido elegido, manteniendo fijo el total. Debe superar también a los otros rivales. Se muestra como alternativa a la adición, sin sumarlas. No representa votantes identificados ni una recomendación de campaña.</p>
      <p>Estos umbrales solo superan a los partidos rastreados. No prueban ganar una sección, elección o distrito frente a todos los participantes. Cambios de candidaturas, coaliciones, preferencias, participación o lista nominal alteran el escenario. Fuentes en auditoría.</p>
    </details>
    <h3>Tabla completa del universo</h3>
    <p className="heyti-overview-note">{scenario.base.coverage.represented} filas: todas las secciones representadas, incluidas las no calculables. LN es la base de 2024; no una proyección de LN 2027. Desplaza horizontalmente para ver las columnas. Pulsa una fila para acercar su geometría y abrir el detalle. Orden por sección.</p>
    <SectionTableSearch><div className="heyti-win-table-scroll" tabIndex={0} role="region" aria-label="Tabla de escenarios por sección, desplazamiento horizontal">
      <table className="heyti-win-table heyti-section-table"><caption>{scenario.base.universe.label} · {scenario.base.contest} · escenario parcial 2027 · {win.party}</caption>
        <thead><tr>{['Sección', 'LN base 2024', 'Participación estimada 2027', 'Total estimado 2027', 'PAN estimado', 'PRI estimado', 'PVEM estimado', 'MORENA estimado', 'Residuo estimado', 'Liderazgo rastreado', `Adición mínima ${win.party}`, 'Capacidad LN base', 'Estado'].map(label => <th scope="col" key={label}>{label}</th>)}</tr></thead>
        <tbody>{Object.values(win.rows).sort((a,b) => Number(a.sectionId)-Number(b.sectionId)).map(row => <tr data-section-id={row.sectionId} key={row.sectionId} aria-selected={selectedSection === row.sectionId} onClick={() => onSelectSection?.(row.sectionId)}>
          <th scope="row"><button type="button" aria-label={`Ver detalle y acercar sección ${row.sectionId}`}>{row.sectionId}</button></th>
          <td>{num(row.nominal)}</td><td>{row.percent === null ? 'N/D' : `${row.percent.toFixed(3)}%`}</td><td>{num(row.projectedTotal)}</td>
          {WIN_PARTIES.map(p => <td key={p}>{num(row.projectedVotes?.[p] ?? null)}</td>)}
          <td>{num(row.residual)}</td><td>{row.leaders.join(' / ') || 'N/D'}</td><td>{num(row.additional)}</td><td>{num(row.capacity)}</td>
          <td>{row.projectedVotes ? row.exceedsCapacity ? 'Umbral excede capacidad LN base' : 'Escenario parcial calculable' : winLabels[row.status]}</td>
        </tr>)}</tbody>
      </table>
    </div></SectionTableSearch>
    <h3>Detalle por sección</h3>
    <p>Selecciona una sección en el mapa o en esta lista. Orden por número de sección.</p>
    <label className="workspace-electoral-comparison-control"><span>Sección</span><select value={selectedSection ?? ''} onChange={e => onSelectSection?.(e.target.value)}><option value="">Seleccionar…</option>{Object.keys(win.rows).sort((a,b) => Number(a)-Number(b)).map(id => <option key={id}>{id}</option>)}</select></label>
    {selected ? <div ref={detailRef}>
      <h4>Sección {selected.sectionId} · {selected.projectedVotes ? 'escenario estimado' : winLabels[selected.status]}</h4>
      <p>Años con participación calculable: {selected.years.join(', ') || 'Ninguno'}. Participación estimada: {selected.percent === null ? 'N/D' : `${selected.percent.toFixed(3)}%`}.</p>
      <div className="heyti-win-table-scroll" tabIndex={0} role="region" aria-label="Participación histórica utilizada en la sección"><table className="heyti-win-table"><caption>Participación histórica utilizada</caption><thead><tr><th scope="col">Año</th><th scope="col">Total</th><th scope="col">LN</th><th scope="col">Participación</th></tr></thead><tbody>{scenario.rows[selected.sectionId].history?.map(h => <tr key={h.year}><th scope="row">{h.year}</th><td>{num(h.total)}</td><td>{num(h.nominal)}</td><td>{h.percent === null ? `N/D (${h.status})` : `${h.percent.toFixed(3)}%`}</td></tr>)}</tbody></table></div>
      <p>Estimación antes de limitar a 0–100%: {scenario.rows[selected.sectionId].raw === null ? 'N/D' : `${scenario.rows[selected.sectionId].raw!.toFixed(3)}%`}. {scenario.rows[selected.sectionId].clamped ? 'Se limitó al rango 0–100%.' : 'No se aplicó recorte.'}</p>
      <p>LN 2024: {num(selected.nominal)} · votos totales 2024: {num(selected.historicalTotal)}.</p>
      <p>Total estimado antes de redondear: {selected.rawTotal === null ? 'N/D' : selected.rawTotal.toFixed(3)} · total entero estimado: {num(selected.projectedTotal)}.</p>
      <div className="heyti-win-table-scroll" tabIndex={0} role="region" aria-label="Detalle de votos por partido en la sección"><table className="heyti-win-table"><thead><tr><th scope="col">Partido</th><th scope="col">Votos 2024</th><th scope="col">% del total 2024</th><th scope="col">Votos estimados</th></tr></thead><tbody>{WIN_PARTIES.map(p => <tr key={p}><th scope="row">{p}</th><td>{num(selected.historicalVotes[p])}</td><td>{selected.historicalTotal && selected.historicalVotes[p] !== null ? `${(selected.historicalVotes[p]! / selected.historicalTotal * 100).toFixed(3)}%` : 'N/D'}</td><td>{num(selected.projectedVotes?.[p] ?? null)}</td></tr>)}</tbody></table></div>
      <p>Residuo estimado no desglosado: {num(selected.residual)}. No se le asigna ganador.</p>
      {selected.projectedVotes ? <>
        <p>Liderazgo rastreado: <strong>{selected.leaders.join(' / ')}</strong> · rival de referencia para {win.party}: {selected.rival}, {num(selected.rivalVotes)} votos estimados.</p>
        <p><strong>Adición mínima parcial: {num(selected.additional)} votos.</strong> Votos del partido después de la adición: {num(selected.selectedVotes! + selected.additional!)}.</p>
        <p>Capacidad restante usando LN 2024: {num(selected.capacity)}. {selected.exceedsCapacity ? 'El umbral excede esa capacidad: no es factible por esta vía dentro de la base utilizada.' : 'El umbral cabe aritméticamente en esa capacidad; no demuestra disponibilidad real de votantes.'}</p>
        <p>Transferencia hipotética mínima desde {selected.rival}: {selected.transfer === null ? 'No factible con un único rival de referencia' : `${num(selected.transfer)} votos`}. Alternativa matemática a la adición.</p>
      </> : <p>No se calcula un umbral con esta cobertura; revisa el estado y las fuentes.</p>}
    </div> : null}
  </section>
}
