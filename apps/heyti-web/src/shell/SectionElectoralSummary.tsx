import {
  ELECTORAL_CONTEST_IDS,
  ELECTORAL_TRACKED_PARTIES,
} from '../gateway/electoral.response'
import type {
  ElectoralContestId,
  ElectoralDataStatus,
  ElectoralResultsView,
} from '../gateway/electoral.response'

interface SectionElectoralSummaryProps {
  electoralResults: ElectoralResultsView
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

export function SectionElectoralSummary({
  electoralResults,
}: SectionElectoralSummaryProps) {
  return (
    <section
      className="workspace-electoral-summary"
      aria-labelledby="electoral-summary-title"
    >
      <header>
        <div>
          <p>LECTURA ELECTORAL</p>
          <h3 id="electoral-summary-title">
            Elección {electoralResults.electionYear}
          </h3>
        </div>

        <span data-quality={electoralResults.qualityStatus}>
          {electoralResults.qualityStatus === 'COMPLETE'
            ? 'Cobertura completa'
            : 'Cobertura parcial'}
        </span>
      </header>

      <p className="workspace-electoral-scope">
        Resultados limitados a PAN, PRI, PVEM y MORENA.
        La mayor votación rastreada no certifica un ganador
        absoluto.
      </p>

      <div className="workspace-electoral-contests">
        {ELECTORAL_CONTEST_IDS.map((contestId) => {
          const contest =
            electoralResults.contests[contestId]

          return (
            <article
              key={contestId}
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

              <ul aria-label="Votos por partido rastreado">
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
