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
}

interface ElectoralContestGridProps {
  contests: ElectoralResultsView['contests']
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
    ? 'Cobertura completa'
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
}

function ElectoralContestGrid({
  contests,
}: ElectoralContestGridProps) {
  return (
    <div className="workspace-electoral-contests">
      {ELECTORAL_CONTEST_IDS.map((contestId) => (
        <ElectoralContestCard
          key={contestId}
          contestId={contestId}
          contest={contests[contestId]}
        />
      ))}
    </div>
  )
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
        Resultados limitados a PAN, PRI, PVEM y MORENA.
        La mayor votación rastreada no certifica un ganador
        absoluto.
      </p>

      <ElectoralContestGrid
        contests={electoralResults.contests}
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
    </section>
  )
}
