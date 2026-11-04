import {
  useState,
  useId,
} from 'react'

import {
  ELECTORAL_CONTEST_IDS,
  ELECTORAL_TRACKED_PARTIES,
} from '../gateway/electoral.response'
import type {
  ElectoralContestId,
  ElectoralContestView,
  ElectoralDataStatus,
  ElectoralQualityStatus,
  ElectoralResultsView,
} from '../gateway/electoral.response'

interface SectionElectoralSummaryProps {
  electoralResults: ElectoralResultsView
  view?: 'all' | 'current' | 'history'
}

interface ElectoralContestGridProps {
  contests: ElectoralResultsView['contests']
  single?: boolean
}

interface ElectoralContestCardProps {
  contestId: ElectoralContestId
  contest: ElectoralContestView
}

const integerFormatter = new Intl.NumberFormat(
  'es-MX',
  {
    maximumFractionDigits: 0,
  },
)

const percentageFormatter = new Intl.NumberFormat(
  'es-MX',
  {
    maximumFractionDigits: 2,
  },
)

function contestLabel(
  contestId: ElectoralContestId,
): string {
  switch (contestId) {
    case 'A':
      return 'Ayuntamiento'
    case 'DL':
      return 'Diputación local'
    case 'DF':
      return 'Diputación federal'
    case 'G':
      return 'Gubernatura'
    case 'S':
      return 'Senaduría'
    case 'P':
      return 'Presidencia'
  }
}

function dataStatusLabel(
  status: ElectoralDataStatus,
): string {
  switch (status) {
    case 'AVAILABLE':
      return 'Disponible'
    case 'AVAILABLE_WITHOUT_NOMINAL_LIST':
      return 'Disponible sin lista nominal'
    case 'SUMMARY_ONLY':
      return 'Solo resumen'
    case 'NOT_CONTESTED':
      return 'No celebrada'
    case 'ZERO_TOTAL':
      return 'Total en cero'
    case 'INCOMPLETE':
      return 'Incompleto'
    case 'INCONSISTENT':
      return 'Inconsistente'
    case 'TIED_TRACKED_LEAD':
      return 'Empate rastreado'
  }
}

function qualityStatusLabel(
  status: ElectoralQualityStatus,
): string {
  return status === 'COMPLETE'
    ? 'Datos disponibles en todas las contiendas consultadas'
    : 'Cobertura parcial'
}

function formatNumber(
  value: number | null,
): string {
  return value === null
    ? 'No disponible'
    : integerFormatter.format(value)
}

function formatPercentage(
  value: number | null,
): string {
  return value === null
    ? 'No disponible'
    : `${percentageFormatter.format(value * 100)} %`
}

function ElectoralPartyBars({
  contest,
}: {
  contest: ElectoralContestView
}) {
  if (contest.dataStatus === 'NOT_CONTESTED') {
    return (
      <p className="heyti-party-chart-note">
        Contienda no celebrada. No se representa una gráfica de votos.
      </p>
    )
  }

  const maximum = Math.max(
    0,
    ...ELECTORAL_TRACKED_PARTIES.map(
      party => contest.votesByTrackedParty[party] ?? 0,
    ),
  )

  return (
    <section className="heyti-party-chart" aria-label="Votos por partido rastreado">
      <p className="heyti-party-chart-title">Votos por partido rastreado</p>
      <ul className="heyti-party-bars">
        {ELECTORAL_TRACKED_PARTIES.map(party => {
          const votes = contest.votesByTrackedParty[party]
          const width = votes !== null && maximum > 0
            ? (votes / maximum) * 100
            : 0

          return (
            <li key={party} data-party={party}>
              <div className="heyti-party-bar-label">
                <span>{party}</span>
                <strong>{formatNumber(votes)}</strong>
              </div>
              {votes !== null ? (
                <div className="heyti-party-bar-track" aria-hidden="true">
                  <span style={{ width: `${width}%` }} />
                </div>
              ) : (
                <div className="heyti-party-bar-missing" aria-hidden="true" />
              )}
            </li>
          )
        })}
      </ul>
      <p className="heyti-party-chart-note">
        {ELECTORAL_TRACKED_PARTIES.every(
          party => contest.votesByTrackedParty[party] === null,
        )
          ? 'Sin datos por partido para graficar.'
          : `Escala desde cero hasta ${formatNumber(maximum)} votos en esta tarjeta.`}
        Solo incluye los cuatro partidos rastreados; no determina un ganador absoluto.
      </p>
    </section>
  )
}
function ElectoralContestCard({
  contestId,
  contest,
}: ElectoralContestCardProps) {
  return (
    <article
      className="workspace-electoral-contest"
      data-status={contest.dataStatus}
    >
      <header>
        <strong>{contestLabel(contestId)}</strong>
        <span>
          {dataStatusLabel(contest.dataStatus)}
        </span>
      </header>

      <dl>
        <div>
          <dt>Votos totales</dt>
          <dd>
            {formatNumber(contest.totalVotes)}
          </dd>
        </div>
        <div>
          <dt>Lista nominal</dt>
          <dd>
            {formatNumber(contest.nominalList)}
          </dd>
        </div>
        <div>
          <dt>Participación</dt>
          <dd>
            {formatPercentage(
              contest.participationRate,
            )}
          </dd>
        </div>
        <div>
          <dt>Mayor votación rastreada</dt>
          <dd>
            {contest.leadingTrackedParty ??
              'No calculable'}
          </dd>
        </div>
        <div>
          <dt>Margen rastreado</dt>
          <dd>
            {formatNumber(
              contest.trackedLeadMargin,
            )}
          </dd>
        </div>
        <div>
          <dt>Votos no desglosados</dt>
          <dd>
            {formatNumber(
              contest.residualVotes,
            )}
          </dd>
        </div>
      </dl>

      <ElectoralPartyBars contest={contest} />
    </article>
  )
}

function ElectoralContestGrid({
  contests,
  single = false,
}: ElectoralContestGridProps) {
  const [selectedContestId, setSelectedContestId] = useState<ElectoralContestId>('A')
  if (single) {
    return (
      <div className="heyti-single-contest">
        <label className="workspace-electoral-comparison-control">
          <span>Contienda</span>
          <select aria-label="Contienda de la elección" value={selectedContestId}
            onChange={event => setSelectedContestId(event.target.value as ElectoralContestId)}>
            {ELECTORAL_CONTEST_IDS.map(id => <option key={id} value={id}>{contestLabel(id)}</option>)}
          </select>
        </label>
        <ElectoralContestCard contestId={selectedContestId} contest={contests[selectedContestId]} />
      </div>
    )
  }
  return (
    <div className="workspace-electoral-contests">
      {ELECTORAL_CONTEST_IDS.map((contestId) => (
        <details key={contestId} className="heyti-contest-disclosure">
          <summary>
            <strong>{contestLabel(contestId)}</strong>
            <span>{dataStatusLabel(contests[contestId].dataStatus)}</span>
          </summary>
          <ElectoralContestCard
          key={contestId}
          contestId={contestId}
          contest={contests[contestId]}
        />
        </details>
      ))}
    </div>
  )
}

function ElectoralGroupedHistory({
  elections,
  contestId,
}: {
  elections: Array<{
    electionYear: number
    contests: ElectoralResultsView['contests']
  }>
  contestId: ElectoralContestId
}) {
  const colors = ['#1765b3', '#c83e48', '#278348', '#853641']
  const series = [...elections]
    .sort((a, b) => a.electionYear - b.electionYear)
    .map(election => ({
      year: election.electionYear,
      contest: election.contests[contestId],
    }))

  const values = series.flatMap(({ contest }) =>
    contest.dataStatus === 'NOT_CONTESTED'
      ? []
      : ELECTORAL_TRACKED_PARTIES.map(
          party => contest.votesByTrackedParty[party],
        ).filter((value): value is number => value !== null),
  )
  const maximum = Math.max(0, ...values)
  const scale = maximum > 0 ? maximum : 1
  const groupWidth = 160
  const chartWidth = 80 + series.length * groupWidth

  return (
    <section
      className="heyti-history-chart"
      aria-label={`Comparativa histórica de ${contestLabel(contestId)}`}
    >
      <h5>{contestLabel(contestId)} · Votos por partido y año</h5>
      <ul className="heyti-history-legend" aria-label="Partidos">
        {ELECTORAL_TRACKED_PARTIES.map((party, index) => (
          <li key={party}>
            <span style={{ background: colors[index] }} aria-hidden="true" />
            {party}
          </li>
        ))}
      </ul>

      {values.length === 0 ? (
        <p>Sin datos por partido para graficar esta contienda.</p>
      ) : (
        <div className="heyti-history-chart-scroll">
          <svg
            viewBox={`0 0 ${chartWidth} 320`}
            style={{ minWidth: chartWidth }}
            role="img"
            aria-label={
              `${contestLabel(contestId)}: comparación de votos por partido ` +
              `entre ${series.map(item => item.year).join(', ')}. ` +
              'Las cifras exactas aparecen en las tablas debajo.'
            }
          >
            {[0, 0.25, 0.5, 0.75, 1].map(fraction => {
              const y = 250 - fraction * 200
              return (
                <g key={fraction}>
                  <line x1="65" x2={chartWidth - 10} y1={y} y2={y} stroke="#dbe3ef" />
                  <text x="58" y={y + 4} textAnchor="end" fontSize="11" fill="#64748b">
                    {integerFormatter.format(scale * fraction)}
                  </text>
                </g>
              )
            })}

            {series.map(({ year, contest }, yearIndex) => {
              const start = 80 + yearIndex * groupWidth
              const notContested = contest.dataStatus === 'NOT_CONTESTED'
              return (
                <g key={year}>
                  {notContested ? (
                    <text x={start + 65} y="150" textAnchor="middle" fontSize="12" fill="#64748b">
                      No celebrada
                    </text>
                  ) : ELECTORAL_TRACKED_PARTIES.map((party, partyIndex) => {
                    const votes = contest.votesByTrackedParty[party]
                    const x = start + partyIndex * 34
                    const height = votes === null ? 0 : (votes / scale) * 200
                    return (
                      <g key={party}>
                        <title>{`${year}, ${party}: ${formatNumber(votes)}`}</title>
                        {votes === null ? (
                          <text x={x + 12} y="238" textAnchor="middle" fontSize="10" fill="#64748b">
                            N/D
                          </text>
                        ) : (
                          <>
                            <rect x={x} y={250 - height} width="24" height={height} fill={colors[partyIndex]} rx="2" />
                            <text x={x + 12} y={242 - height} textAnchor="middle" fontSize="10" fill="#334155">
                              {formatNumber(votes)}
                            </text>
                          </>
                        )}
                      </g>
                    )
                  })}
                  <text x={start + 63} y="277" textAnchor="middle" fontSize="14" fontWeight="700" fill="#334155">
                    {year}
                  </text>
                  <text x={start + 63} y="300" textAnchor="middle" fontSize="10" fill="#64748b">
                    {dataStatusLabel(contest.dataStatus)}
                  </text>
                </g>
              )
            })}
          </svg>
        </div>
      )}

      <p className="heyti-party-chart-note">
        Escala común entre años, desde cero.
        N/D significa dato no disponible y no equivale a cero.
        Solo se comparan los cuatro partidos rastreados.
      </p>
    </section>
  )
}
export function ElectoralHistoricalComparison({
  electoralResults, independent = false,
}: SectionElectoralSummaryProps & { independent?: boolean }) {
  const titleId = useId()
  const [selectedContestId, setSelectedContestId] =
    useState<ElectoralContestId>('A')

  const elections = [
    ...electoralResults.historicalElections,
    {
      electionYear: electoralResults.electionYear,
      qualityStatus: electoralResults.qualityStatus,
      contests: electoralResults.contests,
    },
  ]

  return (
    <section
      className="workspace-electoral-comparison"
      aria-labelledby={titleId}
    >
      <header>
        <div>
          <p>{independent ? "ANÁLISIS TERRITORIAL" : "COMPARATIVA CERTIFICADA"}</p>
          <h4 id={titleId}>
            Comparativa histórica
          </h4>
        </div>

        <span>{independent ? "Resultados de la respuesta del CORE" : "Serie histórica en revisión 2018–2024"}</span>
      </header>

      <p className="workspace-electoral-comparison-note">
        Mayor votación rastreada por año. No certifica un
        ganador absoluto.
      </p>

      <label className="workspace-electoral-comparison-control">
        <span>Contienda</span>
        <select
          aria-label="Contienda comparada"
          value={selectedContestId}
          onChange={(event) => {
            setSelectedContestId(
              event.target.value as ElectoralContestId,
            )
          }}
        >
          {ELECTORAL_CONTEST_IDS.map((contestId) => (
            <option
              key={contestId}
              value={contestId}
            >
              {contestLabel(contestId)}
            </option>
          ))}
        </select>
      </label>

      <ElectoralGroupedHistory
        elections={elections}
        contestId={selectedContestId}
      />

      <div className="workspace-electoral-comparison-years">
        {elections.map((election) => {
          const contest =
            election.contests[selectedContestId]

          return (
            <article
              key={election.electionYear}
              className="workspace-electoral-comparison-year"
              data-status={contest.dataStatus}
            >
              <header>
                <strong>{election.electionYear}</strong>
                <span>
                  {dataStatusLabel(contest.dataStatus)}
                </span>
              </header>

              <dl>
                <div>
                  <dt>Mayor votación rastreada</dt>
                  <dd>
                    {contest.leadingTrackedParty ??
                      'No calculable'}
                  </dd>
                </div>
                <div>
                  <dt>Margen rastreado</dt>
                  <dd>
                    {formatNumber(
                      contest.trackedLeadMargin,
                    )}
                  </dd>
                </div>
                <div>
                  <dt>Votos totales</dt>
                  <dd>
                    {formatNumber(contest.totalVotes)}
                  </dd>
                </div>
                <div>
                  <dt>Participación</dt>
                  <dd>
                    {formatPercentage(
                      contest.participationRate,
                    )}
                  </dd>
                </div>
              </dl>

              <ul aria-label={
                `Votos rastreados en ${
                  election.electionYear
                }`
              }>
                {ELECTORAL_TRACKED_PARTIES.map(
                  (party) => (
                    <li key={party}>
                      <span>{party}</span>
                      <strong>
                        {formatNumber(
                          contest
                            .votesByTrackedParty[party],
                        )}
                      </strong>
                    </li>
                  ),
                )}
              </ul>
            </article>
          )
        })}
      </div>
    </section>
  )
}

export function SectionElectoralSummary({
  electoralResults,
  view = 'all',
}: SectionElectoralSummaryProps) {
  return (
    <section
      className="workspace-electoral-summary"
      aria-labelledby={view === 'history' ? undefined : 'electoral-summary-title'}
      aria-label={view === 'history' ? 'Historial electoral de la sección' : undefined}
    >
      {view !== 'history' ? (<>
      <header>
        <div>
          <p>LECTURA ELECTORAL</p>
          <h3 id="electoral-summary-title">
            Elección {electoralResults.electionYear}
          </h3>
        </div>

        <span
          data-quality={
            electoralResults.qualityStatus
          }
        >
          {qualityStatusLabel(
            electoralResults.qualityStatus,
          )}
        </span>
      </header>

      <p className="workspace-electoral-scope">
        Este panel muestra los votos de PAN, PRI, PVEM y MORENA.
        Para identificar al ganador de la elección se necesitan los resultados de todos los participantes.
      </p>

      <ElectoralContestGrid
        contests={electoralResults.contests}
        single={view === 'current'}
      />
      </>) : null}

      {view !== 'current' ? (<>

      <ElectoralHistoricalComparison
        electoralResults={electoralResults}
      />

      <section
        className="workspace-electoral-history"
        aria-labelledby="electoral-history-title"
      >
        <header>
          <div>
            <p>EVOLUCIÓN CERTIFICADA</p>
            <h4 id="electoral-history-title">
              Historial electoral
            </h4>
          </div>
        </header>

        <p className="workspace-electoral-history-note">
          Consulta los resultados históricos disponibles.
          Los estados parciales identifican datos que la
          fuente oficial no desglosa completamente.
        </p>

        <div className="workspace-electoral-history-years">
          {electoralResults.historicalElections.map(
            (election) => (
              <details
                key={election.electionYear}
                className="workspace-electoral-history-year"
              >
                <summary>
                  <strong>
                    Elección {election.electionYear}
                  </strong>
                  <span
                    data-quality={
                      election.qualityStatus
                    }
                  >
                    {qualityStatusLabel(
                      election.qualityStatus,
                    )}
                  </span>
                </summary>

                <div className="workspace-electoral-history-content">
                  <ElectoralContestGrid
                    contests={election.contests}
                  />
                </div>
              </details>
            ),
          )}
        </div>
      </section>
      </>) : null}
    </section>
  )
}
