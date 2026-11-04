import { describe, expect, it } from 'vitest'
import { buildParticipationGoals, classifyGoal } from './participationGoals'
import type { ParticipationScenario, ScenarioRow } from './participationScenario'
function scenario(rows: ScenarioRow[]): ParticipationScenario { return { rows: Object.fromEntries(rows.map(r => [r.sectionId, r])) } as ParticipationScenario }
function row(id: number, percent: number | null, reason: string | null = null): ScenarioRow { return { sectionId: String(id), percent, reason, raw: percent, clamped: false, years: [2018, 2024], nominal: 1000 } }
describe('metas de participación 2027', () => {
  it('incluye igualdad con meta y borde de tolerancia sin redondear', () => {
    expect(classifyGoal(50, 50, 3)).toBe('GOAL_PASS')
    expect(classifyGoal(49.999, 50, 3)).toBe('GOAL_NEAR')
    expect(classifyGoal(47, 50, 3)).toBe('GOAL_NEAR')
    expect(classifyGoal(46.999, 50, 3)).toBe('GOAL_FAIL')
  })
  it('tolera límites cero y cien y rechaza entradas inválidas', () => {
    expect(classifyGoal(0, 0, 0)).toBe('GOAL_PASS')
    expect(classifyGoal(99, 100, 0)).toBe('GOAL_FAIL')
    expect(classifyGoal(0, 100, 100)).toBe('GOAL_NEAR')
    for (const n of [NaN, Infinity, -1, 101]) {
      expect(() => classifyGoal(50, n, 3)).toThrow()
      expect(() => classifyGoal(50, 50, n)).toThrow()
    }
  })
  it('conserva faltantes e inconsistencias y excluye no calculables de brechas', () => {
    const result = buildParticipationGoals(scenario([row(1, null, 'NO_DATA'), row(2, null, 'INCONSISTENT'), row(3, 0), row(4, 70)]), 50, 3)
    expect(result.counts).toEqual({ NO_DATA: 1, INCONSISTENT: 1, GOAL_FAIL: 1, GOAL_PASS: 1 })
    expect(result.worst.map(r => r.sectionId)).toEqual(['3'])
    expect(result.rows['1'].gap).toBeNull(); expect(result.rows['4'].gap).toBe(0)
  })
  it('prioriza hasta 20 brechas descendentes con empate por sección', () => {
    const source = scenario(Array.from({ length: 25 }, (_, i) => row(25 - i, 10)))
    const result = buildParticipationGoals(source, 50, 3)
    expect(result.worst).toHaveLength(20)
    expect(result.worst[0].sectionId).toBe('1'); expect(result.worst[19].sectionId).toBe('20')
    expect(source.rows['1'].percent).toBe(10)
  })
})
