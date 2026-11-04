import { describe, expect, it } from 'vitest'
import { participationBand, participationCounts, participationValue } from './participation'
import type { UniverseMap } from '../gateway/universe.client'
describe('participación histórica', () => {
  it('conserva faltantes y distingue cero de 100%', () => {
    expect(participationValue(null)).toBeNull()
    expect(participationValue(undefined)).toBeNull()
    expect(participationValue(100)).toBe(0)
    expect(participationValue(0)).toBe(100)
    expect(participationValue(55.7)).toBeCloseTo(44.3)
  })
  it('clasifica límites 30 y 50 y conserva errores y no celebradas', () => {
    expect(participationBand(70.1, 'ABS_HIGH')).toBe('PART_LOW')
    expect(participationBand(70, 'ABS_HIGH')).toBe('PART_MID')
    expect(participationBand(50, 'ABS_HIGH')).toBe('PART_HIGH')
    for (const status of ['NO_DATA', 'INCONSISTENT', 'NOT_CONTESTED']) expect(participationBand(null, status)).toBe(status)
  })
  it('recuenta desde los porcentajes sin reutilizar bandas de abstención', () => {
    const result = { sections: [
      { abstention: 80, status: 'ABS_VERY_HIGH' },
      { abstention: 70, status: 'ABS_HIGH' },
      { abstention: 55, status: 'ABS_HIGH' },
      { abstention: 50, status: 'ABS_HIGH' },
      { abstention: null, status: 'NO_DATA' },
    ] } as UniverseMap
    expect(participationCounts(result)).toEqual({ PART_LOW: 1, PART_MID: 2, PART_HIGH: 1, NO_DATA: 1 })
  })
})
