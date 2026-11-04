import type { ParticipationScenario, ScenarioRow } from './participationScenario'
export interface GoalRow { sectionId: string; status: string; percent: number | null; gap: number | null }
export interface ParticipationGoals { target: number; tolerance: number; rows: Record<string, GoalRow>; counts: Record<string, number>; worst: GoalRow[] }
export const goalLabels: Record<string, string> = { GOAL_PASS: 'Cumple o supera la meta', GOAL_NEAR: 'Por debajo, dentro de la tolerancia', GOAL_FAIL: 'Por debajo, fuera de la tolerancia', NO_DATA: 'No calculable: datos insuficientes', INCONSISTENT: 'No calculable: cifras inconsistentes' }
export function classifyGoal(percent: number, target: number, tolerance: number): string {
  if (![percent, target, tolerance].every(Number.isFinite) || percent < 0 || percent > 100 || target < 0 || target > 100 || tolerance < 0 || tolerance > 100) throw new Error('Meta o tolerancia inválidas; usa valores de 0 a 100.')
  // Compare against the actual boundaries rather than a rounded difference.
  return percent >= target ? 'GOAL_PASS' : percent >= target - tolerance ? 'GOAL_NEAR' : 'GOAL_FAIL'
}
export function buildParticipationGoals(scenario: ParticipationScenario, target: number, tolerance: number): ParticipationGoals {
  classifyGoal(0, target, tolerance)
  const rows: Record<string, GoalRow> = {}, counts: Record<string, number> = {}
  for (const s of Object.values(scenario.rows)) {
    const status = s.percent === null ? s.reason ?? 'NO_DATA' : classifyGoal(s.percent, target, tolerance)
    const row = { sectionId: s.sectionId, status, percent: s.percent, gap: s.percent === null ? null : Math.max(0, target - s.percent) }
    rows[s.sectionId] = row; counts[status] = (counts[status] ?? 0) + 1
  }
  const worst = Object.values(rows).filter(r => r.gap !== null && r.gap > 0).sort((a, b) => b.gap! - a.gap! || Number(a.sectionId) - Number(b.sectionId)).slice(0, 20)
  return { target, tolerance, rows, counts, worst }
}
export function goalRowLabel(row: ScenarioRow, goals: ParticipationGoals): string {
  const goal = goals.rows[row.sectionId]
  return `${goalLabels[goal.status]}${row.percent === null ? '' : ` · ${row.percent.toFixed(1)}% estimado · meta ${goals.target}% · brecha ${goal.gap!.toFixed(1)} pp`}`
}
