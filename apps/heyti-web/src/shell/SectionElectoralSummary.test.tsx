import {
  renderToStaticMarkup,
} from 'react-dom/server'
import {
  describe,
  expect,
  it,
} from 'vitest'

import type {
  ElectoralContestId,
  ElectoralContestView,
  ElectoralResultsView,
} from '../gateway/electoral.response'
import {
  SectionElectoralSummary,
} from './SectionElectoralSummary'

function availableContest(
  contestId: ElectoralContestId,
): ElectoralContestView {
  return {
    contestId,
    dataStatus: 'AVAILABLE',
    votesByTrackedParty: {
      PAN: 100,
      PRI: 50,
      PVEM: 20,
      MORENA: 80,
    },
    totalVotes: 280,
    nominalList: 500,
    trackedVotes: 250,
    residualVotes: 30,
    participationRate: 0.56,
    leadingTrackedParty: 'PAN',
    trackedLeadMargin: 20,
  }
}

function availableContests(): Record<
  ElectoralContestId,
  ElectoralContestView
> {
  return {
    A: availableContest('A'),
    DL: availableContest('DL'),
    DF: availableContest('DF'),
    G: availableContest('G'),
    S: availableContest('S'),
    P: availableContest('P'),
  }
}

function unavailableContest(
  contestId: ElectoralContestId,
  dataStatus:
    | 'SUMMARY_ONLY'
    | 'NOT_CONTESTED',
): ElectoralContestView {
  return {
    contestId,
    dataStatus,
    votesByTrackedParty: {
      PAN: null,
      PRI: null,
      PVEM: null,
      MORENA: null,
    },
    totalVotes:
      dataStatus === 'SUMMARY_ONLY'
        ? 877
        : null,
    nominalList:
      dataStatus === 'SUMMARY_ONLY'
        ? 1580
        : null,
    trackedVotes: null,
    residualVotes: null,
    participationRate:
      dataStatus === 'SUMMARY_ONLY'
        ? 877 / 1580
        : null,
    leadingTrackedParty: null,
    trackedLeadMargin: null,
  }
}

function electoralResults():
ElectoralResultsView {
  const contests2018 = availableContests()

  contests2018.DF = {
    ...contests2018.DF,
    dataStatus:
      'AVAILABLE_WITHOUT_NOMINAL_LIST',
    nominalList: null,
    participationRate: null,
  }

  const contests2021 = availableContests()

  contests2021.DF = unavailableContest(
    'DF',
    'SUMMARY_ONLY',
  )
  contests2021.G = unavailableContest(
    'G',
    'NOT_CONTESTED',
  )
  contests2021.S = unavailableContest(
    'S',
    'NOT_CONTESTED',
  )
  contests2021.P = unavailableContest(
    'P',
    'NOT_CONTESTED',
  )

  return {
    sectionId: '1',
    electionYear: 2024,
    coverageScope: 'TRACKED_PARTIES_ONLY',
    trackedParties: [
      'PAN',
      'PRI',
      'PVEM',
      'MORENA',
    ],
    qualityStatus: 'COMPLETE',
    contests: availableContests(),
    historicalElections: [
      {
        electionYear: 2018,
        qualityStatus: 'PARTIAL',
        contests: contests2018,
      },
      {
        electionYear: 2021,
        qualityStatus: 'PARTIAL',
        contests: contests2021,
      },
    ],
  }
}

describe(
  'SectionElectoralSummary history',
  () => {
    it(
      'renders certified historical elections',
      () => {
        const markup = renderToStaticMarkup(
          <SectionElectoralSummary
            electoralResults={electoralResults()}
          />,
        )

        expect(markup).toContain(
          'Historial electoral',
        )
        expect(markup).toContain(
          'Elección 2018',
        )
        expect(markup).toContain(
          'Elección 2021',
        )
        expect(markup).toContain(
          'Disponible sin lista nominal',
        )
        expect(markup).toContain(
          'Solo resumen',
        )
        expect(markup).toContain(
          'No celebrada',
        )
      },
    )

    it(
      'renders the historical comparison under review',
      () => {
        const markup = renderToStaticMarkup(
          <SectionElectoralSummary
            electoralResults={electoralResults()}
          />,
        )

        expect(markup).toContain(
          'Comparativa histórica',
        )
        expect(markup).toContain(
          'Serie histórica en revisión 2018–2024',
        )
        expect(markup).toContain(
          'aria-label="Contienda comparada"',
        )
        expect(markup).toContain(
          'Mayor votación rastreada por año',
        )
        expect(markup).toContain(
          'No certifica un ganador absoluto',
        )
        expect(markup).toContain(
          'workspace-electoral-comparison',
        )
      },
    )
  },
)