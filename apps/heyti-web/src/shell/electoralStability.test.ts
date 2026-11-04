import { describe, expect, it } from 'vitest'
import { buildElectoralStability, stabilityRowLabel } from './electoralStability'
import type { UniverseMap, MapStatus } from '../gateway/universe.client'
import type { ElectoralTrackedParty } from '../gateway/electoral.response'
function map(year: number, party: ElectoralTrackedParty | null, status: MapStatus = 'TRACKED_LEAD', contest: UniverseMap['contest'] = 'A'): UniverseMap {
  return { year, contest, universe: { level: 'state', id: '11', label: 'Guanajuato', sections: 1 }, provenance: { master: 'same', geometry: 'same' }, coverage: { represented: 1, geographic: 1, blocked: 0 }, counts: {}, sections: [{ sectionId: '1', geometry: { type: 'Polygon', coordinates: [[[0, 0], [1, 0], [0, 1], [0, 0]]] }, leader: party, status, total: 100 }] }
}
describe('estabilidad parcial 2018–2024', () => {
  it('clasifica uno, dos y tres partidos distintos', () => {
    for (const [parties, expected] of [[['PAN', 'PAN', 'PAN'], 'STAB_HIGH'], [['PAN', 'MORENA', 'PAN'], 'STAB_MID'], [['PAN', 'PRI', 'MORENA'], 'STAB_LOW']] as [ElectoralTrackedParty[], string][]) {
      const result = buildElectoralStability([2018, 2021, 2024].map((y, i) => map(y, parties[i])))
      expect(result.rows['1'].status).toBe(expected); expect(result.validSections).toBe(1)
    }
  })
  it('usa dos años para contiendas sexenales y no exige 2021', () => {
    const same = buildElectoralStability([map(2018, 'PAN', 'TRACKED_LEAD', 'G'), map(2024, 'PAN', 'TRACKED_LEAD', 'G')])
    expect(same.rows['1'].status).toBe('STAB_HIGH'); expect(same.years).toEqual([2018, 2024])
    expect(buildElectoralStability([map(2018, 'PAN', 'TRACKED_LEAD', 'P'), map(2024, 'MORENA', 'TRACKED_LEAD', 'P')]).rows['1'].status).toBe('STAB_MID')
  })
  it('no asigna estabilidad a ceros, empates ni faltantes de un año', () => {
    for (const status of ['ZERO_TOTAL', 'TIE', 'NO_DATA', 'NO_TRACKED_VOTES', 'NOT_CONTESTED', 'INCONSISTENT'] as MapStatus[]) {
      const result = buildElectoralStability([map(2018, 'PAN'), map(2021, null, status), map(2024, 'PAN')])
      expect(result.validSections).toBe(0); expect(result.counts[status]).toBe(1)
      expect(stabilityRowLabel(result.rows['1'])).toContain('2021:')
    }
  })
  it('conserva varias causas en secuencia y prioriza inconsistencia', () => {
    const result = buildElectoralStability([map(2018, null, 'NO_DATA'), map(2021, null, 'INCONSISTENT'), map(2024, 'PAN')])
    expect(result.rows['1'].status).toBe('INCONSISTENT')
    expect(result.rows['1'].leaders.map(l => l.status)).toEqual(['NO_DATA', 'INCONSISTENT', 'TRACKED_LEAD'])
  })
  it('rechaza año faltante o duplicado, corte, contienda y cobertura distintos', () => {
    expect(() => buildElectoralStability([map(2018, 'PAN'), map(2024, 'PAN')])).toThrow()
    expect(() => buildElectoralStability([map(2018, 'PAN'), map(2018, 'PAN'), map(2024, 'PAN')])).toThrow()
    const changed = map(2021, 'PAN'); changed.provenance.master = 'changed'
    expect(() => buildElectoralStability([map(2018, 'PAN'), changed, map(2024, 'PAN')])).toThrow()
    expect(() => buildElectoralStability([map(2018, 'PAN'), map(2021, 'PAN', 'TRACKED_LEAD', 'DF'), map(2024, 'PAN')])).toThrow()
    const coverage = map(2021, 'PAN'); coverage.sections[0].sectionId = '2'
    expect(() => buildElectoralStability([map(2018, 'PAN'), coverage, map(2024, 'PAN')])).toThrow()
  })
  it('acepta procedencia equivalente sin depender del orden de claves', () => {
    const middle = map(2021, 'PAN'); middle.provenance = { geometry: 'same', master: 'same' }
    expect(buildElectoralStability([map(2018, 'PAN'), middle, map(2024, 'PAN')]).validSections).toBe(1)
  })
})
