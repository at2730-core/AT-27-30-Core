import type { UniverseMap } from '../gateway/universe.client'
export interface StabilityRow { sectionId: string; status: string; leaders: { year: number; party: string | null; status: string }[] }
export interface ElectoralStability { base: UniverseMap; rows: Record<string, StabilityRow>; counts: Record<string, number>; years: number[]; validSections: number }
export const stabilityLabels: Record<string, string> = {
  STAB_HIGH: 'Alta: mismo partido rastreado', STAB_MID: 'Media: dos partidos rastreados distintos', STAB_LOW: 'Baja: tres partidos rastreados distintos',
  INCONSISTENT: 'No calculable: cifras inconsistentes', NO_DATA: 'No calculable: datos faltantes', ZERO_TOTAL: 'No calculable: total en cero', TIE: 'No calculable: empate rastreado', NO_TRACKED_VOTES: 'No calculable: sin votos rastreados', NOT_CONTESTED: 'No calculable: elección no celebrada',
}
export function buildElectoralStability(maps: UniverseMap[]): ElectoralStability {
  const base = maps.find(m => m.year === 2024)
  if (!base) throw new Error('Falta la respuesta de 2024.')
  const years = ['G', 'S', 'P'].includes(base.contest) ? [2018, 2024] : [2018, 2021, 2024]
  const sameProvenance = (m: UniverseMap) => Object.keys({ ...m.provenance, ...base.provenance }).every(k => m.provenance[k] === base.provenance[k])
  if (maps.length !== years.length || new Set(maps.map(m => m.year)).size !== years.length || maps.some(m => !years.includes(m.year) || (m.metric ?? 'leaders') !== 'leaders' || m.universe.level !== base.universe.level || m.universe.id !== base.universe.id || m.contest !== base.contest || !sameProvenance(m))) throw new Error('Históricos incompatibles: universo, años, contienda o corte distintos.')
  const ids = base.sections.map(s => s.sectionId).sort().join(',')
  if (maps.some(m => m.sections.map(s => s.sectionId).sort().join(',') !== ids)) throw new Error('Cambió la cobertura territorial entre respuestas.')
  const indexed = new Map(maps.map(m => [m.year, new Map(m.sections.map(s => [s.sectionId, s]))]))
  const rows: Record<string, StabilityRow> = {}, counts: Record<string, number> = {}
  let validSections = 0
  for (const b of base.sections) {
    const leaders = years.map(year => { const s = indexed.get(year)!.get(b.sectionId)!; return { year, party: s.leader, status: s.status } })
    // Require every applicable election; a gap cannot certify continuity.
    let status = ['INCONSISTENT', 'NO_DATA', 'ZERO_TOTAL', 'TIE', 'NO_TRACKED_VOTES', 'NOT_CONTESTED'].find(reason => leaders.some(s => s.status === reason))
    if (!status) {
      if (leaders.some(s => s.status !== 'TRACKED_LEAD' || !s.party)) throw new Error('Clasificación histórica inválida para estabilidad.')
      const distinct = new Set(leaders.map(s => s.party)).size
      status = distinct === 1 ? 'STAB_HIGH' : distinct === 2 ? 'STAB_MID' : 'STAB_LOW'
      validSections++
    }
    rows[b.sectionId] = { sectionId: b.sectionId, status, leaders }
    counts[status] = (counts[status] ?? 0) + 1
  }
  return { base, rows, counts, years, validSections }
}
export function stabilityRowLabel(row: StabilityRow): string {
  return `${stabilityLabels[row.status]} · ${row.leaders.map(l => `${l.year}: ${l.party ?? stabilityLabels[l.status]?.replace('No calculable: ', '') ?? l.status}`).join(' · ')}`
}
