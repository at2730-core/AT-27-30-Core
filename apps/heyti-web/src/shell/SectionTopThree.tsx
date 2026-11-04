import { useState } from 'react'
import { ELECTORAL_CONTEST_IDS, ELECTORAL_TRACKED_PARTIES } from '../gateway/electoral.response'
import type { ElectoralContestId, ElectoralResultsView } from '../gateway/electoral.response'

const labels: Record<ElectoralContestId, string> = {
  A: 'Ayuntamiento', DL: 'Diputación local', DF: 'Diputación federal',
  G: 'Gubernatura', S: 'Senaduría', P: 'Presidencia',
}
const colors = { PAN: '#1765b3', PRI: '#c83e48', PVEM: '#278348', MORENA: '#853641' }

export function SectionTopThree({ electoralResults }: { electoralResults: ElectoralResultsView }) {
  const [selected, setSelected] = useState<ElectoralContestId>('A')
  const contest = electoralResults.contests[selected]
  const ranking = ELECTORAL_TRACKED_PARTIES.map(party => ({ party, votes: contest.votesByTrackedParty[party] }))
    .sort((a, b) => (b.votes ?? -1) - (a.votes ?? -1))
  const complete = ranking.every(row => row.votes !== null && Number.isFinite(row.votes) && row.votes >= 0)
  const total = contest.totalVotes
  const sum = ranking.reduce((value, row) => value + (row.votes ?? 0), 0)
  const calculable = complete && total !== null && Number.isFinite(total) && total > 0 && sum <= total
    && contest.dataStatus !== 'NOT_CONTESTED' && ranking[0].votes! > 0
  const top = calculable ? ranking.filter(row => row.votes! >= ranking[2].votes!) : []
  const fmt = (value: number | null) => value === null ? 'N/D' : value.toLocaleString('es-MX')
  return <section aria-label="Top 3 de partidos rastreados">
    <h3>Sección {electoralResults.sectionId} · {electoralResults.electionYear}</h3>
    <label className="workspace-electoral-comparison-control"><span>Contienda</span>
      <select aria-label="Puesto para Top 3" value={selected} onChange={event => setSelected(event.target.value as ElectoralContestId)}>
        {ELECTORAL_CONTEST_IDS.map(id => <option key={id} value={id}>{labels[id]}</option>)}
      </select>
    </label>
    <p className="heyti-overview-note">Top 3 entre PAN, PRI, PVEM y MORENA. Cobertura parcial: no es el ranking de todos los participantes ni acredita un ganador absoluto. La autorización territorial no acredita la validación de todas las cifras electorales.</p>
    <p>Votos totales: <strong>{fmt(total)}</strong></p>
    {calculable ? <>
      {top.length > 3 ? <p>Empate en el corte del Top 3: se incluyen todos los partidos empatados.</p> : null}
      <div aria-label="Clasificación por votos">{top.map(row => {
        const rank = 1 + ranking.filter(other => other.votes! > row.votes!).length
        const tied = ranking.filter(other => other.votes === row.votes).length > 1
        return <article key={row.party} style={{ margin: '18px 0' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', gap: 10, flexWrap: 'wrap' }}>
            <strong>{rank}º · {row.party}{tied ? ' · Empate' : ''}</strong>
            <span>{fmt(row.votes)} votos · {(row.votes! / total! * 100).toFixed(1)}%</span>
          </div>
          <div aria-hidden="true" style={{ height: 10, background: '#edf2f8', borderRadius: 6, margin: '8px 0' }}>
            <div style={{ width: `${row.votes! / ranking[0].votes! * 100}%`, height: '100%', background: colors[row.party], borderRadius: 6 }} />
          </div>
          <small>Diferencia respecto al máximo rastreado: {fmt(ranking[0].votes! - row.votes!)} votos.</small>
        </article>
      })}</div>
      <p className="heyti-party-chart-note">Barras relativas al máximo rastreado. Porcentajes sobre los votos totales de la contienda.</p>
    </> : <div className="workspace-insight-empty"><strong>Top 3 no calculable</strong>
      <p>{contest.dataStatus === 'NOT_CONTESTED' ? 'Elección no celebrada.' : total === 0 ? 'Total de votos en cero: no se asignan posiciones.' : !complete ? 'Falta el desglose de uno o más partidos: no se asignan posiciones.' : 'Total no disponible o cifras inconsistentes: no se asignan posiciones.'}</p>
    </div>}
    <details><summary>Desglose de los cuatro partidos rastreados</summary>
      <table style={{ width: '100%' }}><thead><tr><th scope="col" style={{ textAlign: 'left' }}>Partido</th><th scope="col" style={{ textAlign: 'right' }}>Votos</th></tr></thead>
        <tbody>{ranking.map(row => <tr key={row.party}><th scope="row" style={{ textAlign: 'left', padding: '8px 0' }}>{row.party}</th><td style={{ textAlign: 'right' }}>{fmt(row.votes)}</td></tr>)}</tbody>
      </table>
    </details>
  </section>
}
