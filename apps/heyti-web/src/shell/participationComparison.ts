import type { UniverseMap } from '../gateway/universe.client'
import type { ParticipationScenario } from './participationScenario'
import { buildParticipationSensitivity } from './participationSensitivity'

export interface ParticipationComparison { deltas: number[]; scenarios: ParticipationScenario[]; activeDelta: number }
export function buildParticipationComparison(maps: UniverseMap[], variations: number[]): ParticipationScenario {
  if (!variations.length || variations.length > 4 || variations.some(d => !Number.isFinite(d) || d < -8 || d > 8 || !Number.isInteger(d * 2))) throw new Error('Elige de una a cuatro variaciones entre −8 y +8 pp, en pasos de 0.5.')
  const deltas = [...new Set([0, ...variations])].sort((a,b) => a-b)
  if (deltas.length < 2) throw new Error('Incluye al menos una variación distinta de cero para comparar con la base.')
  const scenarios = deltas.map(delta => buildParticipationSensitivity(maps, delta))
  const value: ParticipationComparison = {deltas, scenarios, activeDelta: 0}
  return {...scenarios[deltas.indexOf(0)], participationComparison: value}
}
export function selectParticipationComparison(result: ParticipationScenario, delta: number): ParticipationScenario {
  const comparison = result.participationComparison
  const selected = comparison?.scenarios.find(s => s.sensitivity?.delta === delta)
  if (!comparison || !selected) throw new Error('El escenario solicitado no pertenece a esta comparación.')
  return {...selected, participationComparison: {...comparison, activeDelta: delta}}
}
export function comparisonPoints(result: ParticipationScenario) {
  return result.participationComparison!.scenarios.map(s => {
    const v = s.sensitivity!
    return {delta: v.delta, percent: v.valid > 0 && v.nominal > 0 ? v.modifiedTotal / v.nominal * 100 : null,
      total: v.valid > 0 ? v.modifiedTotal : null, valid: v.valid, nominal: v.nominal, limited: v.limited}
  })
}
