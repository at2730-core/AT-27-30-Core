import { useState } from 'react'
import { ELECTORAL_CONTEST_IDS, ELECTORAL_TRACKED_PARTIES } from '../gateway/electoral.response'
import type { ElectoralContestId, ElectoralResultsView } from '../gateway/electoral.response'

const labels: Record<ElectoralContestId, string> = {
  A: 'Ayuntamiento', DL: 'Diputación local', DF: 'Diputación federal',
  G: 'Gubernatura', S: 'Senaduría', P: 'Presidencia',
}

export function SectionCompetitiveness({ electoralResults }: { electoralResults: ElectoralResultsView }) {
  const [selected, setSelected] = useState<ElectoralContestId>('A')
  const contest = electoralResults.contests[selected]
  const ranking = ELECTORAL_TRACKED_PARTIES.map(party => ({ party, votes: contest.votesByTrackedParty[party] }))
    .sort((a, b) => (b.votes ?? -1) - (a.votes ?? -1))
  const complete = ranking.every(row => row.votes !== null && Number.isFinite(row.votes) && row.votes >= 0)
  const total = contest.totalVotes
  const sum = ranking.reduce((value, row) => value + (row.votes ?? 0), 0)
  const calculable = complete && total !== null && Number.isFinite(total) && total > 0 && sum <= total
    && contest.dataStatus !== 'NOT_CONTESTED'
  const margin = calculable ? ranking[0].votes! - ranking[1].votes! : null
  const percent = margin !== null && total !== null ? margin / total * 100 : null
  const status = percent === null ? 'No calculable' : percent >= 10 ? 'Margen amplio' : percent >= 5 ? 'Competida' : 'Muy competida'
  const color = percent === null ? '#f1f5f9' : percent >= 10 ? '#e6f7ec' : percent >= 5 ? '#fff7e6' : '#fff1f2'
  const fmt = (value: number | null) => value === null ? 'N/D' : value.toLocaleString('es-MX')
  return <section aria-label="Competitividad de la sección">
    <h3>Sección {electoralResults.sectionId} · {electoralResults.electionYear}</h3>
    <label className="workspace-electoral-comparison-control"><span>Contienda</span>
      <select aria-label="Puesto para competitividad" value={selected} onChange={event => setSelected(event.target.value as ElectoralContestId)}>
        {ELECTORAL_CONTEST_IDS.map(id => <option key={id} value={id}>{labels[id]}</option>)}
      </select>
    </label>
    <p className="heyti-overview-note">Lectura parcial entre PAN, PRI, PVEM y MORENA. No identifica un ganador absoluto ni garantiza una elección futura. La autorización territorial no acredita la validación de todas las cifras electorales.</p>
    <div style={{ background: color, padding: 16, borderRadius: 12 }}>
      <strong>{status}</strong>
      <p>Margen entre los dos primeros partidos rastreados: {fmt(margin)} votos{percent !== null ? ` (${percent.toFixed(1)} puntos porcentuales)` : ''}.</p>
      {!calculable ? <p>{contest.dataStatus === 'NOT_CONTESTED' ? 'Elección no celebrada.' : total === 0 ? 'Total de votos en cero: no se asigna semáforo.' : !complete ? 'Falta el desglose de uno o más partidos.' : 'Total no disponible o cifras inconsistentes: no se asigna semáforo.'}</p> : null}
    </div>
    <p>Votos totales: {fmt(total)}</p>
    <table style={{ width: '100%', borderCollapse: 'collapse' }}><caption>Votos por partido rastreado</caption>
      <thead><tr><th scope="col" style={{ textAlign: 'left' }}>Partido</th><th scope="col" style={{ textAlign: 'right' }}>Votos</th></tr></thead>
      <tbody>{ranking.map(row => <tr key={row.party}><th scope="row" style={{ textAlign: 'left', padding: '8px 0' }}>{row.party}</th><td style={{ textAlign: 'right' }}>{fmt(row.votes)}</td></tr>)}</tbody>
    </table>
    <p className="heyti-party-chart-note">Criterio de la V1: margen dividido entre votos totales. Menos de 5 pp: muy competida; de 5 a menos de 10 pp: competida; desde 10 pp: margen amplio. Se sustituye la etiqueta «Segura» para evitar interpretarla como garantía.</p>
  </section>
}
