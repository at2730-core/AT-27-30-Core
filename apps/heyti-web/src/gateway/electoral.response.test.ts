import {
  describe,
  expect,
  it,
} from 'vitest'

import {
  readElectoralResults,
} from './electoral.response'
import type {
  ElectoralContestId,
} from './electoral.response'
import type {
  HeytiResponse,
} from './heyti.client'

type RawContest = Record<string, unknown>

function availableContest(
  contestId: ElectoralContestId,
): RawContest {
  return {
    contest_id: contestId,
    votes_by_tracked_party: {
      PAN: 100,
      PRI: 50,
      PVEM: 20,
      MORENA: 80,
    },
    total_votes: 280,
    nominal_list: 500,
    tracked_votes: 250,
    residual_votes: 30,
    participation_rate: 0.56,
    leading_tracked_party: 'PAN',
    tracked_lead_margin: 20,
    data_status: 'AVAILABLE',
  }
}

function availableContests(): Record<
  ElectoralContestId,
  RawContest
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

function historicalResponse(): HeytiResponse {
  const contests2018 = availableContests()

  contests2018.DF = {
    ...contests2018.DF,
    nominal_list: null,
    participation_rate: null,
    data_status:
      'AVAILABLE_WITHOUT_NOMINAL_LIST',
  }

  const contests2021 = availableContests()

  contests2021.DF = {
    contest_id: 'DF',
    votes_by_tracked_party: {
      PAN: null,
      PRI: null,
      PVEM: null,
      MORENA: null,
    },
    total_votes: 877,
    nominal_list: 1580,
    tracked_votes: null,
    residual_votes: null,
    participation_rate: 877 / 1580,
    leading_tracked_party: null,
    tracked_lead_margin: null,
    data_status: 'SUMMARY_ONLY',
  }

  for (const contestId of [
    'G',
    'S',
    'P',
  ] as const) {
    contests2021[contestId] = {
      contest_id: contestId,
      votes_by_tracked_party: {
        PAN: null,
        PRI: null,
        PVEM: null,
        MORENA: null,
      },
      total_votes: null,
      nominal_list: null,
      tracked_votes: null,
      residual_votes: null,
      participation_rate: null,
      leading_tracked_party: null,
      tracked_lead_margin: null,
      data_status: 'NOT_CONTESTED',
    }
  }

  return {
    response_id: 'RESP-HISTORY-001',
    contract: 'HEYTI_RESPONSE',
    version: '1.0',
    capability_id: 'describe_section',
    status: 'success',
    warnings: [],
    errors: [],
    trace: {
      request_id: 'REQ-HISTORY-001',
      session_id: null,
      execution_id: null,
      knowledge_version: 'GUANAJUATO_2023:1.0',
    },
    blocks: [
      {
        type: 'domain',
        role: 'electoral',
        content: {
          section_id: '1',
          election_year: 2024,
          coverage_scope:
            'TRACKED_PARTIES_ONLY',
          tracked_parties: [
            'PAN',
            'PRI',
            'PVEM',
            'MORENA',
          ],
          quality_status: 'COMPLETE',
          contests: availableContests(),
          historical_elections: [
            {
              election_year: 2018,
              quality_status: 'PARTIAL',
              contests: contests2018,
            },
            {
              election_year: 2021,
              quality_status: 'PARTIAL',
              contests: contests2021,
            },
          ],
        },
      },
    ],
  }
}

describe(
  'readElectoralResults historical elections',
  () => {
    it(
      'parses certified 2018 and 2021 history',
      () => {
        const results = readElectoralResults(
          historicalResponse(),
        )

        expect(results).not.toBeNull()
        expect(
          results?.historicalElections.map(
            (election) => election.electionYear,
          ),
        ).toEqual([2018, 2021])

        expect(
          results?.historicalElections[0]
            .contests.DF.dataStatus,
        ).toBe(
          'AVAILABLE_WITHOUT_NOMINAL_LIST',
        )

        expect(
          results?.historicalElections[1]
            .contests.DF.dataStatus,
        ).toBe('SUMMARY_ONLY')

        expect(
          results?.historicalElections[1]
            .contests.G.dataStatus,
        ).toBe('NOT_CONTESTED')
      },
    )
  },
)

describe(
  'readElectoralResults historical validation',
  () => {
    it(
      'rejects a missing certified history',
      () => {
        const response = historicalResponse()
        const content = response.blocks[0]
          .content as Record<string, unknown>

        delete content.historical_elections

        expect(
          () => readElectoralResults(response),
        ).toThrowError(
          'El bloque electoral no contiene exactamente las elecciones históricas certificadas.',
        )
      },
    )

    it(
      'rejects historical years outside certified order',
      () => {
        const response = historicalResponse()
        const content = response.blocks[0]
          .content as Record<string, unknown>

        const history =
          content.historical_elections as unknown[]

        content.historical_elections = [
          ...history,
        ].reverse()

        expect(
          () => readElectoralResults(response),
        ).toThrowError(
          'Las elecciones históricas no corresponden al orden certificado 2018, 2021.',
        )
      },
    )
  },
)
