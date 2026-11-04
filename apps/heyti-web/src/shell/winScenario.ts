import type { ParticipationScenario } from './participationScenario'
import type { UniverseMap } from '../gateway/universe.client'
export const WIN_PARTIES = ['PAN', 'PRI', 'PVEM', 'MORENA'] as const
export type WinParty = typeof WIN_PARTIES[number]
export interface WinRow { sectionId: string; status: string; historicalVotes: Record<string, number | null>; historicalTotal: number | null; nominal: number | null; projectedTotal: number | null; rawTotal: number | null; projectedVotes: Record<string, number> | null; residual: number | null; leaders: string[]; selectedVotes: number | null; rivalVotes: number | null; rival: string | null; additional: number | null; transfer: number | null; capacity: number | null; exceedsCapacity: boolean; years: number[]; percent: number | null }
export interface WinAnalysis { party: WinParty; rows: Record<string, WinRow>; counts: Record<string, number>; validSections: number; aheadSections: number; additionalTotal: number; transferTotal: number; exceedsCapacity: number }
export const winLabels: Record<string, string> = { TIE: 'Empate entre partidos rastreados', NO_DATA: 'No calculable: datos insuficientes', INCONSISTENT: 'No calculable: cifras inconsistentes', ZERO_TOTAL: 'No calculable: total histórico cero', ZERO_PROJECTED: 'No calculable: total estimado cero', NO_TRACKED_VOTES: 'No calculable: sin votos rastreados', NOT_CONTESTED: 'No calculable: contienda no celebrada' }
export function allocateScenarioVotes(total: number, shares: Record<string, number>): Record<string, number> {
  if (!Number.isSafeInteger(total) || total < 0 || Object.values(shares).some(s => !Number.isFinite(s) || s < 0) || Math.abs(Object.values(shares).reduce((a, b) => a + b, 0) - 1) > 1e-8) throw new Error('Reparto estimado inválido.')
  const keys = Object.keys(shares), rows = keys.map((key, index) => { const value = total * shares[key]; return { key, index, count: Math.floor(value), remainder: value - Math.floor(value) } })
  const extra = total - rows.reduce((sum, row) => sum + row.count, 0)
  if (extra < 0 || extra > rows.length) throw new Error('Redondeo inválido.')
  const sorted = [...rows].sort((a, b) => b.remainder - a.remainder || a.index - b.index)
  for (let i = 0; i < extra; i++) sorted[i].count++
  return Object.fromEntries(rows.map(r => [r.key, r.count]))
}
export function voteThresholds(votes: Record<string, number>, party: WinParty): { additional: number; transfer: number | null; rival: string; rivalVotes: number } {
  if (WIN_PARTIES.some(p => !Number.isSafeInteger(votes[p]) || votes[p] < 0)) throw new Error('Votos estimados inválidos.')
  const others = WIN_PARTIES.filter(p => p !== party).sort((a, b) => votes[b] - votes[a] || WIN_PARTIES.indexOf(a) - WIN_PARTIES.indexOf(b))
  const rival = others[0], x = votes[party], rivalVotes = votes[rival]
  const additional = Math.max(0, rivalVotes - x + 1)
  // Transfer removes each vote from one rival and adds it to the selected party.
  // It must also surpass the other rivals, which remain unchanged.
  const transferRequired = Math.max(0, Math.ceil((rivalVotes - x + 1) / 2), ...others.slice(1).map(p => votes[p] - x + 1))
  return { additional, transfer: transferRequired <= rivalVotes ? transferRequired : null, rival, rivalVotes }
}
export function buildWinAnalysis(scenario: ParticipationScenario, source: UniverseMap, party: WinParty): WinAnalysis {
  if (!WIN_PARTIES.includes(party) || source.metric !== 'concentration' || source.year !== 2024 || source.universe.level !== scenario.base.universe.level || source.universe.id !== scenario.base.universe.id || source.contest !== scenario.base.contest || Object.keys({ ...source.provenance, ...scenario.base.provenance }).some(k => source.provenance[k] !== scenario.base.provenance[k])) throw new Error('El desglose no corresponde al escenario y corte consultados.')
  if (source.sections.map(s => s.sectionId).sort().join(',') !== scenario.base.sections.map(s => s.sectionId).sort().join(',')) throw new Error('Cobertura del desglose incompatible.')
  const rows: Record<string, WinRow> = {}, counts: Record<string, number> = {}, baseRows = new Map(scenario.base.sections.map(s => [s.sectionId, s]))
  let validSections = 0, aheadSections = 0, additionalTotal = 0, transferTotal = 0, exceedsCapacity = 0
  for (const s of source.sections) {
    const projection = scenario.rows[s.sectionId], base = baseRows.get(s.sectionId)!
    if (s.total !== base.total) throw new Error('Total histórico distinto entre respuestas.')
    const historicalVotes = Object.fromEntries(WIN_PARTIES.map(p => [p, s.votes?.[p] ?? null]))
    let reason: string | null = s.status === 'INCONSISTENT' || projection.reason === 'INCONSISTENT' ? 'INCONSISTENT' : s.status === 'NOT_CONTESTED' ? 'NOT_CONTESTED' : s.total === 0 ? 'ZERO_TOTAL' : s.status === 'NO_DATA' || projection.percent === null || s.total == null || WIN_PARTIES.some(p => historicalVotes[p] === null) ? 'NO_DATA' : null
    let row: WinRow = { sectionId: s.sectionId, status: reason ?? '', historicalVotes, historicalTotal: s.total, nominal: projection.nominal, projectedTotal: null, rawTotal: null, projectedVotes: null, residual: null, leaders: [], selectedVotes: null, rivalVotes: null, rival: null, additional: null, transfer: null, capacity: null, exceedsCapacity: false, years: projection.years, percent: projection.percent }
    if (!reason) {
      const total = s.total!, nominal = projection.nominal!, sum = Object.values(historicalVotes).reduce<number>((n, v) => n + v!, 0)
      if (total <= 0 || !nominal || sum > total || Object.values(historicalVotes).some(v => !Number.isSafeInteger(v) || v! < 0)) throw new Error('Base de votos inválida.')
      if (sum === 0) reason = 'NO_TRACKED_VOTES'
      else {
        const rawTotal = nominal * projection.percent! / 100, projectedTotal = Math.round(rawTotal)
        if (projectedTotal === 0) reason = 'ZERO_PROJECTED'
        else {
          const shares = Object.fromEntries(WIN_PARTIES.map(p => [p, historicalVotes[p]! / total])); shares.RESIDUAL = (total - sum) / total
          const allocated = allocateScenarioVotes(projectedTotal, shares)
          const projectedVotes = Object.fromEntries(WIN_PARTIES.map(p => [p, allocated[p]]))
          const maximum = Math.max(...Object.values(projectedVotes)), leaders = WIN_PARTIES.filter(p => projectedVotes[p] === maximum)
          const thresholds = voteThresholds(projectedVotes, party), capacity = nominal - projectedTotal
          row = { ...row, status: leaders.length > 1 ? 'TIE' : leaders[0], projectedTotal, rawTotal, projectedVotes, residual: allocated.RESIDUAL, leaders, selectedVotes: projectedVotes[party], ...thresholds, capacity, exceedsCapacity: thresholds.additional > capacity }
          validSections++; if (leaders.length === 1 && leaders[0] === party) aheadSections++
          additionalTotal += thresholds.additional; transferTotal += thresholds.transfer ?? 0; if (row.exceedsCapacity) exceedsCapacity++
        }
      }
    }
    if (reason) row.status = reason
    rows[s.sectionId] = row; counts[row.status] = (counts[row.status] ?? 0) + 1
  }
  return { party, rows, counts, validSections, aheadSections, additionalTotal, transferTotal, exceedsCapacity }
}
export function winRowLabel(row: WinRow, party: WinParty): string {
  return row.projectedVotes === null ? winLabels[row.status] : `Escenario 2027 · liderazgo rastreado ${row.leaders.join(' / ')} · ${party}: ${row.selectedVotes} votos estimados · adición mínima parcial: ${row.additional}${row.exceedsCapacity ? ' · excede LN 2024 disponible' : ''}`
}
