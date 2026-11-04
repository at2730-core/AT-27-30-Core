import type { DemoContestId, SectionDemo } from '../gateway/section.demo'
import { DEMO_PARTIES, demoParticipation } from '../gateway/section.demo'
import './SectionHistoryCharts.css'

const colors = { PAN: '#1765b3', PRI: '#c83e48', PVEM: '#278348', MORENA: '#853641' }
const number = (value: number | null) => value === null ? 'N/D' : value.toLocaleString('es-MX')
const states: Record<string, string> = {
  AVAILABLE: 'Disponible · sin certificar',
  AVAILABLE_WITHOUT_NOMINAL_LIST: 'Lista nominal no disponible',
  SUMMARY_ONLY: 'Solo resumen · desglose no disponible',
  NOT_CONTESTED: 'Elección no celebrada',
  ZERO_TOTAL: 'Total en cero',
  INCOMPLETE: 'Datos incompletos',
  INCONSISTENT: 'Cifras inconsistentes · revisar tabla',
  TIED_TRACKED_LEAD: 'Empate entre partidos rastreados',
}

export function sectionHistoryChartModel(years: SectionDemo['years'], contest: DemoContestId) {
  const charts = [2018, 2021, 2024].map(year => {
    const data = years.find(item => item.year === year)?.contests[contest]
    const suppressed = !data || data.status === 'NOT_CONTESTED' || data.status === 'INCONSISTENT'
    return {
      year, data,
      bars: DEMO_PARTIES.map(party => ({ party, value: suppressed ? null : data.votes[party] ?? null })),
    }
  })
  const maximum = Math.max(0, ...charts.flatMap(chart => chart.bars.map(bar => bar.value ?? 0)))
  const rawStep = maximum / 4
  const power = rawStep > 0 ? 10 ** Math.floor(Math.log10(rawStep)) : 1
  const step = Math.max(1, ([1, 2, 5, 10].find(factor => factor * power >= rawStep) ?? 10) * power)
  const axisMax = Math.max(step, Math.ceil(maximum / step) * step)
  const ticks = Array.from({ length: Math.round(axisMax / step) + 1 }, (_, i) => i * step)
  return { charts, axisMax, ticks }
}

export function SectionHistoryCharts({ years, contest }: { years: SectionDemo['years']; contest: DemoContestId }) {
  const { charts, axisMax, ticks } = sectionHistoryChartModel(years, contest)
  const baseline = 220, plotHeight = 170
  return <section className="heyti-section-history" aria-label="Tres gráficas de votos por año">
    <p className="heyti-section-history-explanation">Votos por partido rastreado · misma escala vertical en los tres años. En un panel estrecho, desplázate horizontalmente o amplíalo para ver las tres gráficas en línea.</p>
    <div className="heyti-section-history-scroll" role="region" aria-label="Gráficas 2018, 2021 y 2024; desplazamiento horizontal" tabIndex={0}>
      <div className="heyti-section-history-row">
        {charts.map(({ year, data, bars }) => {
          const participation = data ? demoParticipation(data) : null
          const status = data ? states[data.status] ?? 'Sin dato disponible' : 'Sin dato disponible'
          const description = data?.status === 'NOT_CONTESTED' ? 'Elección no celebrada; no se representan ceros.' : data?.status === 'INCONSISTENT' ? 'Cifras inconsistentes; las barras se omiten. Consulta los valores originales en la tabla.' : bars.map(bar => `${bar.party}: ${number(bar.value)} votos`).join('; ')
          return <figure key={year} className="heyti-section-history-year">
            <figcaption><strong>{year}</strong><span>{status}</span></figcaption>
            <svg viewBox="0 0 320 260" role="img" aria-label={`${year}. ${description}`}>
              <text x="46" y="16" className="heyti-section-history-unit">Votos</text>
              {ticks.map(tick => {
                const y = baseline - tick / axisMax * plotHeight
                return <g key={tick}><line x1="46" x2="310" y1={y} y2={y} className="heyti-section-history-grid" /><text x="39" y={y + 4} textAnchor="end" className="heyti-section-history-tick">{number(tick)}</text></g>
              })}
              <line x1="46" x2="46" y1="50" y2={baseline} className="heyti-section-history-axis" />
              {bars.map((bar, index) => {
                const x = 76 + index * 66, height = bar.value === null ? 0 : bar.value / axisMax * plotHeight
                return <g key={bar.party}>
                  {bar.value !== null && bar.value > 0 ? <rect x={x - 19} y={baseline - height} width="38" height={height} rx="2" fill={colors[bar.party]} /> : null}
                  {bar.value === 0 ? <line x1={x - 14} x2={x + 14} y1={baseline} y2={baseline} stroke={colors[bar.party]} strokeWidth="3" /> : null}
                  <text x={x} y={bar.value === null ? baseline - 8 : baseline - height - 8} textAnchor="middle" className="heyti-section-history-value">{number(bar.value)}</text>
                  <text x={x} y="244" textAnchor="middle" className="heyti-section-history-party">{bar.party}</text>
                </g>
              })}
            </svg>
            <p className="heyti-section-history-metrics">Total: <strong>{number(data?.total ?? null)}</strong> · LN: <strong>{number(data?.nominal ?? null)}</strong><br />Participación: <strong>{participation === null ? 'N/D' : participation.toLocaleString('es-MX', { maximumFractionDigits: 3 }) + '%'}</strong></p>
          </figure>
        })}
      </div>
    </div>
    <p className="heyti-section-history-explanation">N/D no se dibuja como cero. Una elección no celebrada o con cifras inconsistentes no genera barras. Los cuatro partidos no necesariamente suman el total de votos.</p>
  </section>
}
