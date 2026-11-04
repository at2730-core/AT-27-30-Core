import type { UniverseMap } from '../gateway/universe.client'
import { buildParticipationScenario } from './participationScenario'
import { comparePartyVotes } from './partyComparison'

// Descriptive output only: no chosen party, intervention thresholds or transfers.
export function buildDescriptiveScenario(maps: UniverseMap[]) {
  if (maps.length !== 4) throw new Error('Se requieren tres históricos y el desglose 2024.')
  const scenario = buildParticipationScenario(maps.slice(0, 3))
  return { ...scenario, comparison: comparePartyVotes(scenario, maps[3]) }
}