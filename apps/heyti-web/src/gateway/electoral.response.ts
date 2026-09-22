import {
  HeytiGatewayError,
} from './heyti.client'
import type {
  HeytiResponse,
} from './heyti.client'

export const ELECTORAL_CONTEST_IDS = [
  'A',
  'DL',
  'DF',
  'G',
  'S',
  'P',
] as const

export type ElectoralContestId =
  (typeof ELECTORAL_CONTEST_IDS)[number]

export const ELECTORAL_TRACKED_PARTIES = [
  'PAN',
  'PRI',
  'PVEM',
  'MORENA',
] as const

export type ElectoralTrackedParty =
  (typeof ELECTORAL_TRACKED_PARTIES)[number]

export type ElectoralDataStatus =
  | 'AVAILABLE'
  | 'ZERO_TOTAL'
  | 'INCOMPLETE'
  | 'INCONSISTENT'
  | 'TIED_TRACKED_LEAD'

export type ElectoralQualityStatus =
  | 'COMPLETE'
  | 'PARTIAL'

export type TrackedPartyVotes = {
  [Party in ElectoralTrackedParty]:
    number | null
}

export interface ElectoralContestView {
  contestId: ElectoralContestId
  dataStatus: ElectoralDataStatus
  votesByTrackedParty: TrackedPartyVotes
  totalVotes: number | null
  nominalList: number | null
  trackedVotes: number | null
  residualVotes: number | null
  participationRate: number | null
  leadingTrackedParty:
    | ElectoralTrackedParty
    | null
  trackedLeadMargin: number | null
}

export interface ElectoralResultsView {
  sectionId: string
  electionYear: number
  coverageScope: 'TRACKED_PARTIES_ONLY'
  trackedParties: ElectoralTrackedParty[]
  qualityStatus: ElectoralQualityStatus
  contests: Record<
    ElectoralContestId,
    ElectoralContestView
  >
}

function isRecord(
  value: unknown,
): value is Record<string, unknown> {
  return (
    typeof value === 'object' &&
    value !== null &&
    !Array.isArray(value)
  )
}

function invalidElectoralResults(
  message: string,
): never {
  throw new HeytiGatewayError(
    'INVALID_ELECTORAL_RESULTS',
    message,
  )
}

function requireString(
  value: unknown,
  fieldName: string,
): string {
  if (typeof value !== 'string' || !value.trim()) {
    invalidElectoralResults(
      `El bloque electoral no contiene un valor válido para ${fieldName}.`,
    )
  }

  return value.trim()
}

function requireNullableFiniteNumber(
  value: unknown,
  fieldName: string,
): number | null {
  if (value === null) {
    return null
  }

  if (
    typeof value !== 'number' ||
    !Number.isFinite(value)
  ) {
    invalidElectoralResults(
      `El bloque electoral no contiene un número válido para ${fieldName}.`,
    )
  }

  return value
}

function isContestId(
  value: string,
): value is ElectoralContestId {
  return (
    ELECTORAL_CONTEST_IDS as readonly string[]
  ).includes(value)
}

function isTrackedParty(
  value: string,
): value is ElectoralTrackedParty {
  return (
    ELECTORAL_TRACKED_PARTIES as readonly string[]
  ).includes(value)
}

function parseDataStatus(
  value: unknown,
): ElectoralDataStatus {
  const status = requireString(
    value,
    'data_status',
  )

  switch (status) {
    case 'AVAILABLE':
    case 'ZERO_TOTAL':
    case 'INCOMPLETE':
    case 'INCONSISTENT':
    case 'TIED_TRACKED_LEAD':
      return status

    default:
      return invalidElectoralResults(
        'El bloque electoral contiene un data_status no soportado.',
      )
  }
}

function parseQualityStatus(
  value: unknown,
): ElectoralQualityStatus {
  const status = requireString(
    value,
    'quality_status',
  )

  switch (status) {
    case 'COMPLETE':
    case 'PARTIAL':
      return status

    default:
      return invalidElectoralResults(
        'El bloque electoral contiene un quality_status no soportado.',
      )
  }
}

function parseTrackedParties(
  value: unknown,
): ElectoralTrackedParty[] {
  if (
    !Array.isArray(value) ||
    value.length !==
      ELECTORAL_TRACKED_PARTIES.length
  ) {
    invalidElectoralResults(
      'El bloque electoral no declara los partidos rastreados esperados.',
    )
  }

  const parties = value.map(
    (entry) => requireString(
      entry,
      'tracked_parties',
    ),
  )

  const expected = [
    ...ELECTORAL_TRACKED_PARTIES,
  ]

  if (
    parties.some(
      (party, index) =>
        party !== expected[index],
    )
  ) {
    invalidElectoralResults(
      'El orden o contenido de tracked_parties no corresponde al contrato.',
    )
  }

  return expected
}

function parsePartyVotes(
  value: unknown,
  contestId: ElectoralContestId,
): TrackedPartyVotes {
  if (!isRecord(value)) {
    invalidElectoralResults(
      `El concurso ${contestId} no contiene votes_by_tracked_party válido.`,
    )
  }

  const keys = Object.keys(value).sort()
  const expectedKeys = [
    ...ELECTORAL_TRACKED_PARTIES,
  ].sort()

  if (
    keys.length !== expectedKeys.length ||
    keys.some(
      (key, index) =>
        key !== expectedKeys[index],
    )
  ) {
    invalidElectoralResults(
      `El concurso ${contestId} no contiene exactamente los partidos rastreados.`,
    )
  }

  return {
    PAN: requireNullableFiniteNumber(
      value.PAN,
      `${contestId}.PAN`,
    ),
    PRI: requireNullableFiniteNumber(
      value.PRI,
      `${contestId}.PRI`,
    ),
    PVEM: requireNullableFiniteNumber(
      value.PVEM,
      `${contestId}.PVEM`,
    ),
    MORENA: requireNullableFiniteNumber(
      value.MORENA,
      `${contestId}.MORENA`,
    ),
  }
}

function parseLeadingParty(
  value: unknown,
  contestId: ElectoralContestId,
): ElectoralTrackedParty | null {
  if (value === null) {
    return null
  }

  const party = requireString(
    value,
    `${contestId}.leading_tracked_party`,
  )

  if (!isTrackedParty(party)) {
    invalidElectoralResults(
      `El concurso ${contestId} contiene un partido líder no soportado.`,
    )
  }

  return party
}

function parseContest(
  value: unknown,
  expectedContestId: ElectoralContestId,
): ElectoralContestView {
  if (!isRecord(value)) {
    invalidElectoralResults(
      `El concurso ${expectedContestId} no contiene un objeto válido.`,
    )
  }

  if (
    Object.prototype.hasOwnProperty.call(
      value,
      'winner',
    )
  ) {
    invalidElectoralResults(
      `El concurso ${expectedContestId} contiene un ganador no certificado.`,
    )
  }

  const contestId = requireString(
    value.contest_id,
    'contest_id',
  )

  if (
    !isContestId(contestId) ||
    contestId !== expectedContestId
  ) {
    invalidElectoralResults(
      `El identificador del concurso ${expectedContestId} no corresponde al contrato.`,
    )
  }

  const dataStatus = parseDataStatus(
    value.data_status,
  )
  const leadingTrackedParty =
    parseLeadingParty(
      value.leading_tracked_party,
      contestId,
    )

  if (
    dataStatus === 'AVAILABLE' &&
    leadingTrackedParty === null
  ) {
    invalidElectoralResults(
      `El concurso ${contestId} disponible no declara líder rastreado.`,
    )
  }

  if (
    dataStatus !== 'AVAILABLE' &&
    leadingTrackedParty !== null
  ) {
    invalidElectoralResults(
      `El concurso ${contestId} no disponible declara un líder rastreado.`,
    )
  }

  return {
    contestId,
    dataStatus,
    votesByTrackedParty: parsePartyVotes(
      value.votes_by_tracked_party,
      contestId,
    ),
    totalVotes: requireNullableFiniteNumber(
      value.total_votes,
      `${contestId}.total_votes`,
    ),
    nominalList: requireNullableFiniteNumber(
      value.nominal_list,
      `${contestId}.nominal_list`,
    ),
    trackedVotes: requireNullableFiniteNumber(
      value.tracked_votes,
      `${contestId}.tracked_votes`,
    ),
    residualVotes: requireNullableFiniteNumber(
      value.residual_votes,
      `${contestId}.residual_votes`,
    ),
    participationRate:
      requireNullableFiniteNumber(
        value.participation_rate,
        `${contestId}.participation_rate`,
      ),
    leadingTrackedParty,
    trackedLeadMargin:
      requireNullableFiniteNumber(
        value.tracked_lead_margin,
        `${contestId}.tracked_lead_margin`,
      ),
  }
}

function parseContests(
  value: unknown,
): Record<
  ElectoralContestId,
  ElectoralContestView
> {
  if (!isRecord(value)) {
    invalidElectoralResults(
      'El bloque electoral no contiene contests válido.',
    )
  }

  const keys = Object.keys(value).sort()
  const expectedKeys = [
    ...ELECTORAL_CONTEST_IDS,
  ].sort()

  if (
    keys.length !== expectedKeys.length ||
    keys.some(
      (key, index) =>
        key !== expectedKeys[index],
    )
  ) {
    invalidElectoralResults(
      'El bloque electoral no contiene exactamente los seis concursos esperados.',
    )
  }

  return {
    A: parseContest(value.A, 'A'),
    DL: parseContest(value.DL, 'DL'),
    DF: parseContest(value.DF, 'DF'),
    G: parseContest(value.G, 'G'),
    S: parseContest(value.S, 'S'),
    P: parseContest(value.P, 'P'),
  }
}

export function readElectoralResults(
  response: HeytiResponse,
): ElectoralResultsView | null {
  const electoralBlocks = response.blocks.filter(
    (block) => block.role === 'electoral',
  )

  if (electoralBlocks.length === 0) {
    return null
  }

  if (electoralBlocks.length !== 1) {
    invalidElectoralResults(
      'La respuesta contiene múltiples bloques electorales.',
    )
  }

  const content = electoralBlocks[0].content

  if (!isRecord(content)) {
    invalidElectoralResults(
      'El bloque electoral no contiene un objeto válido.',
    )
  }

  const sectionId = requireString(
    content.section_id,
    'section_id',
  )

  if (!/^[1-9]\d*$/.test(sectionId)) {
    invalidElectoralResults(
      'El bloque electoral contiene una sección inválida.',
    )
  }

  if (
    typeof content.election_year !== 'number' ||
    !Number.isInteger(content.election_year)
  ) {
    invalidElectoralResults(
      'El bloque electoral contiene un año inválido.',
    )
  }

  const coverageScope = requireString(
    content.coverage_scope,
    'coverage_scope',
  )

  if (coverageScope !== 'TRACKED_PARTIES_ONLY') {
    invalidElectoralResults(
      'El alcance electoral no corresponde a TRACKED_PARTIES_ONLY.',
    )
  }

  return {
    sectionId,
    electionYear: content.election_year,
    coverageScope,
    trackedParties: parseTrackedParties(
      content.tracked_parties,
    ),
    qualityStatus: parseQualityStatus(
      content.quality_status,
    ),
    contests: parseContests(
      content.contests,
    ),
  }
}
