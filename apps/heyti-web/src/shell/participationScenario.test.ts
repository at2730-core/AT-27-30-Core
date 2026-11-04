import { describe, expect, it } from 'vitest'
import { buildParticipationScenario, projectParticipation } from './participationScenario'
import type { UniverseMap } from '../gateway/universe.client'
function map(year: number, percent: number | null, status = 'ABS_MID', contest: UniverseMap['contest'] = 'A'): UniverseMap {
  return { metric: 'abstention', year, contest, universe: { level: 'state', id: '11', label: 'Guanajuato', sections: 1 }, provenance: { master_sha256: 'same', geometry_sha256: 'same' }, coverage: { represented: 1, geographic: 1, blocked: 0 }, counts: {}, sections: [{ sectionId: '1', geometry: { type: 'Polygon', coordinates: [[[0, 0], [1, 0], [0, 1], [0, 0]]] }, leader: null, status: percent === null ? status as 'NO_DATA' : 'ABS_MID', nominal: 1000, total: percent === null ? null : percent * 10, abstention: percent === null ? null : 100 - percent }] }
}
describe('escenario de participación 2027', () => {
  it('extrapola tendencia lineal ponderada y señala límites', () => {
    expect(projectParticipation([{ year: 2018, percent: 40 }, { year: 2021, percent: 50 }, { year: 2024, percent: 60 }], false)?.percent).toBeCloseTo(70)
    const clipped = projectParticipation([{ year: 2021, percent: 10 }, { year: 2024, percent: 90 }], false)!
    expect(clipped.percent).toBe(100); expect(clipped.raw).toBeCloseTo(170); expect(clipped.clamped).toBe(true)
  })
  it('usa amortiguación sexenal y exige ambos años', () => {
    expect(projectParticipation([{ year: 2018, percent: 50 }, { year: 2024, percent: 60 }], true)?.percent).toBe(63)
    expect(projectParticipation([{ year: 2021, percent: 50 }, { year: 2024, percent: 60 }], true)).toBeNull()
  })
  it('no proyecta con un solo año, sin 2024 o con duplicados', () => {
    expect(projectParticipation([{ year: 2024, percent: 40 }], false)).toBeNull()
    expect(projectParticipation([{ year: 2018, percent: 40 }, { year: 2021, percent: 50 }], false)).toBeNull()
    expect(() => projectParticipation([{ year: 2024, percent: 40 }, { year: 2024, percent: 50 }], false)).toThrow()
  })
  it('conserva cero y cuenta cobertura reducida sin rellenar faltantes', () => {
    const result = buildParticipationScenario([map(2018, 0), map(2021, null, 'NO_DATA'), map(2024, 0)])
    expect(result.percent).toBe(0); expect(result.validSections).toBe(1); expect(result.reducedSections).toBe(1)
    expect(result.rows['1'].years).toEqual([2018, 2024]); expect(result.counts.PART_LOW).toBe(1)
  })
  it('bloquea inconsistencias y la falta de la base', () => {
    const inconsistent = buildParticipationScenario([map(2018, 40), map(2021, null, 'INCONSISTENT'), map(2024, 50)])
    expect(inconsistent.percent).toBeNull(); expect(inconsistent.counts.INCONSISTENT).toBe(1)
    expect(buildParticipationScenario([map(2018, 40), map(2021, 50), map(2024, null, 'NO_DATA')]).validSections).toBe(0)
  })
  it('rechaza cortes, universos, contiendas y coberturas distintos', () => {
    const series = [map(2018, 40), map(2021, 50), map(2024, 60)]
    series[0].provenance.master_sha256 = 'changed'
    expect(() => buildParticipationScenario(series)).toThrow()
    expect(() => buildParticipationScenario([map(2018, 40, 'ABS_MID', 'DF'), map(2021, 50), map(2024, 60)])).toThrow()
    const other = map(2018, 40); other.sections[0].sectionId = '2'
    expect(() => buildParticipationScenario([other, map(2021, 50), map(2024, 60)])).toThrow()
  })
})
