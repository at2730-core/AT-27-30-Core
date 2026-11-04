import type { ParticipationComparison } from './participationComparison'
import type { ParticipationSensitivity } from './participationSensitivity'
import type { PartyComparison } from './partyComparison'
import type { WinAnalysis } from './winScenario'
import type { ParticipationGoals } from './participationGoals'
import type { UniverseMap } from '../gateway/universe.client'
export interface ScenarioRow { history?: { year: number; total: number | null; nominal: number | null; percent: number | null; status: string }[]; sectionId: string; percent: number | null; raw: number | null; clamped: boolean; years: number[]; reason: string | null; nominal: number | null }
export interface ParticipationScenario { participationComparison?: ParticipationComparison; distributionOnly?: boolean; sensitivity?: ParticipationSensitivity; tableOnly?: boolean; comparison?: PartyComparison; win?: WinAnalysis; goals?: ParticipationGoals; base: UniverseMap; rows: Record<string, ScenarioRow>; counts: Record<string, number>; validSections: number; nominal: number; percent: number | null; clampedSections: number; reducedSections: number; method: string }
export function projectParticipation(points: { year: number; percent: number }[], sexennial: boolean): { raw: number; percent: number; clamped: boolean } | null {
  const ordered = [...points].sort((a, b) => a.year - b.year)
  if (new Set(ordered.map(p => p.year)).size !== ordered.length || ordered.some(p => ![2018, 2021, 2024].includes(p.year) || !Number.isFinite(p.percent) || p.percent < 0 || p.percent > 100)) throw new Error('Serie de participación inválida.')
  const p24 = ordered.find(p => p.year === 2024), p18 = ordered.find(p => p.year === 2018)
  if (!p24 || ordered.length < 2 || (sexennial && !p18)) return null
  let raw: number
  if (sexennial) raw = p24.percent + 0.3 * (p24.percent - p18!.percent)
  else {
    const weight = (year: number) => year === 2018 ? 1 : year === 2021 ? 1.5 : 2
    const w = ordered.reduce((sum, p) => sum + weight(p.year), 0)
    const tbar = ordered.reduce((sum, p) => sum + weight(p.year) * (p.year - 2018), 0) / w
    const ybar = ordered.reduce((sum, p) => sum + weight(p.year) * p.percent, 0) / w
    const denominator = ordered.reduce((sum, p) => sum + weight(p.year) * (p.year - 2018 - tbar) ** 2, 0)
    const slope = ordered.reduce((sum, p) => sum + weight(p.year) * (p.year - 2018 - tbar) * (p.percent - ybar), 0) / denominator
    raw = ybar + slope * (9 - tbar)
  }
  return { raw, percent: Math.max(0, Math.min(100, raw)), clamped: raw < 0 || raw > 100 }
}
export const scenarioLabels: Record<string, string> = { PART_LOW: 'Estimación menor de 30%', PART_MID: 'Estimación de 30% a menos de 50%', PART_HIGH: 'Estimación de 50% a 100%', NO_DATA: 'Datos insuficientes', INCONSISTENT: 'Cifras inconsistentes en un año utilizado' }
export function buildParticipationScenario(maps: UniverseMap[]): ParticipationScenario {
  const base = maps.find(m => m.year === 2024)
  if (!base || maps.length !== 3 || new Set(maps.map(m => m.year)).size !== 3 || maps.some(m => m.metric !== 'abstention' || ![2018, 2021, 2024].includes(m.year) || m.universe.id !== base.universe.id || m.universe.level !== base.universe.level || m.contest !== base.contest || JSON.stringify(m.provenance) !== JSON.stringify(base.provenance))) throw new Error('Las fuentes del escenario no corresponden al mismo universo, contienda y corte.')
  const expected = base.sections.map(s => s.sectionId).sort().join(',')
  if (maps.some(m => m.sections.map(s => s.sectionId).sort().join(',') !== expected)) throw new Error('Cambió la cobertura territorial entre respuestas.')
  const sexennial = ['G', 'S', 'P'].includes(base.contest), wanted = sexennial ? [2018, 2024] : [2018, 2021, 2024]
  const indexed = new Map(maps.map(m => [m.year, new Map(m.sections.map(s => [s.sectionId, s]))]))
  const rows: Record<string, ScenarioRow> = {}, counts: Record<string, number> = {}
  let nominal = 0, weighted = 0, validSections = 0, clampedSections = 0, reducedSections = 0
  for (const b of base.sections) {
    const series = wanted.map(year => ({ year, row: indexed.get(year)!.get(b.sectionId)! }))
    const points = series.filter(p => p.row.abstention != null).map(p => ({ year: p.year, percent: 100 - p.row.abstention! }))
    const inconsistent = series.some(p => p.row.status === 'INCONSISTENT')
    const projected = inconsistent ? null : projectParticipation(points, sexennial)
    const reason = projected ? null : inconsistent ? 'INCONSISTENT' : 'NO_DATA'
    rows[b.sectionId] = { history: series.map(p => ({ year: p.year, total: p.row.total, nominal: p.row.nominal ?? null, percent: p.row.abstention == null ? null : 100 - p.row.abstention, status: p.row.status })), sectionId: b.sectionId, percent: projected?.percent ?? null, raw: projected?.raw ?? null, clamped: projected?.clamped ?? false, years: points.map(p => p.year), nominal: b.nominal ?? null, reason }
    const band = reason ?? (projected!.percent < 30 ? 'PART_LOW' : projected!.percent < 50 ? 'PART_MID' : 'PART_HIGH')
    counts[band] = (counts[band] ?? 0) + 1
    if (projected) {
      if (!b.nominal || b.nominal <= 0) throw new Error('Lista nominal base inválida.')
      validSections++; nominal += b.nominal; weighted += projected.percent * b.nominal
      if (projected.clamped) clampedSections++
      if (points.length < wanted.length) reducedSections++
    }
  }
  return { base, rows, counts, validSections, nominal, percent: nominal ? weighted / nominal : null, clampedSections, reducedSections, method: sexennial ? 'V1: p2024 + 0.3 × (p2024 − p2018)' : 'V1: regresión lineal 2018/2021/2024 con pesos 1/1.5/2, evaluada en 2027' }
}
export function scenarioRowLabel(row: ScenarioRow): string {
  return row.percent === null ? scenarioLabels[row.reason ?? 'NO_DATA'] : `${row.percent.toFixed(1)}% de participación estimada 2027${row.clamped ? ' · limitada a 0–100%' : ''} · años utilizados: ${row.years.join(', ')}`
}
