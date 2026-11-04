import { describe, expect, it } from 'vitest'
import { allocateScenarioVotes, buildWinAnalysis, voteThresholds } from './winScenario'
import type { UniverseMap } from '../gateway/universe.client'
import type { ParticipationScenario } from './participationScenario'
function fixture(votes = { PAN: 60, PRI: 20, PVEM: 10, MORENA: 0 }, percent: number | null = 50) {
  const base = { year: 2024, contest: 'A', universe: { level: 'state', id: '11', label: 'Guanajuato', sections: 1 }, coverage: { represented: 1, geographic: 1, blocked: 0 }, provenance: { master: 'same' }, counts: {}, sections: [{ sectionId: '1', total: 100, status: 'ABS_MID', leader: null, geometry: { type: 'Polygon', coordinates: [[[0,0],[1,0],[0,1],[0,0]]] } }] } as UniverseMap
  const scenario = { base, counts: {}, validSections: percent === null ? 0 : 1, nominal: 200, percent, clampedSections: 0, reducedSections: 1, method: 'test', rows: { '1': { sectionId: '1', percent, raw: percent, clamped: false, nominal: 200, years: [2018, 2024], reason: percent === null ? 'NO_DATA' : null } } } as ParticipationScenario
  const source = { ...base, metric: 'concentration', sections: [{ ...base.sections[0], status: 'HHI_MID', votes }] } as UniverseMap
  return { scenario, source }
}
describe('umbrales del escenario parcial 2027', () => {
  it('no exige otro voto cuando el partido ya supera a todos', () => {
    const r = voteThresholds({ PAN: 60, PRI: 20, PVEM: 10, MORENA: 0 }, 'PAN')
    expect(r.additional).toBe(0); expect(r.transfer).toBe(0)
  })
  it('exige superar y conserva empate, sin elegir un ganador arbitrario', () => {
    expect(voteThresholds({ PAN: 50, PRI: 50, PVEM: 0, MORENA: 0 }, 'PAN').additional).toBe(1)
    const { scenario, source } = fixture({ PAN: 50, PRI: 50, PVEM: 0, MORENA: 0 })
    const result = buildWinAnalysis(scenario, source, 'PAN')
    expect(result.rows['1'].leaders).toEqual(['PAN', 'PRI']); expect(result.rows['1'].status).toBe('TIE')
    expect(result.aheadSections).toBe(0)
  })
  it('adición mínima supera al máximo rival y transferencia también a terceros', () => {
    const votes = { PAN: 10, PRI: 100, PVEM: 100, MORENA: 0 }
    const r = voteThresholds(votes, 'PAN')
    expect(r.additional).toBe(91); expect(r.transfer).toBe(91)
    expect(votes.PAN + r.additional).toBeGreaterThan(Math.max(votes.PRI, votes.PVEM))
    expect(votes.PAN + r.transfer!).toBeGreaterThan(votes.PVEM)
  })
  it('reparte enteros conservando total y residuo sin tratarlo como rival', () => {
    expect(allocateScenarioVotes(3, { PAN: .25, PRI: .25, PVEM: .25, MORENA: .25, RESIDUAL: 0 })).toEqual({ PAN: 1, PRI: 1, PVEM: 1, MORENA: 0, RESIDUAL: 0 })
    const { scenario, source } = fixture()
    const r = buildWinAnalysis(scenario, source, 'PRI').rows['1']
    expect(r.projectedTotal).toBe(100); expect(r.residual).toBe(10); expect(r.additional).toBe(41)
    expect(Object.values(r.projectedVotes!).reduce((n,v)=>n+v,0) + r.residual!).toBe(r.projectedTotal)
  })
  it('no convierte faltantes, ceros o inconsistencia en objetivos', () => {
    const missing = fixture(undefined, null)
    expect(buildWinAnalysis(missing.scenario, missing.source, 'PAN').rows['1'].additional).toBeNull()
    const zero = fixture(); zero.source.sections[0].total = 0; zero.scenario.base.sections[0].total = 0
    expect(buildWinAnalysis(zero.scenario, zero.source, 'PAN').rows['1'].status).toBe('ZERO_TOTAL')
    const bad = fixture(); bad.source.sections[0].status = 'INCONSISTENT'
    expect(buildWinAnalysis(bad.scenario, bad.source, 'PAN').validSections).toBe(0)
  })
  it('señala umbrales que exceden capacidad y proyección cero', () => {
    const full = fixture(undefined, 100)
    const row = buildWinAnalysis(full.scenario, full.source, 'PRI').rows['1']
    expect(row.capacity).toBe(0); expect(row.exceedsCapacity).toBe(true)
    const zero = fixture(undefined, 0)
    expect(buildWinAnalysis(zero.scenario, zero.source, 'PRI').rows['1'].status).toBe('ZERO_PROJECTED')
  })
  it('rechaza totales y procedencia distintos y shares inválidas', () => {
    const changed = fixture(); changed.source.sections[0].total = 101
    expect(() => buildWinAnalysis(changed.scenario, changed.source, 'PAN')).toThrow()
    const cut = fixture(); cut.source.provenance = { master: 'changed' }
    expect(() => buildWinAnalysis(cut.scenario, cut.source, 'PAN')).toThrow()
    expect(() => allocateScenarioVotes(100, { PAN: 2 })).toThrow()
  })
})
