import { describe, expect, it } from 'vitest'
import type { FieldPoint } from '../gateway/field.client'
import {
  fieldRoleLabel,
  filterFieldPoints,
} from './fieldWorkspace.logic'

const points: FieldPoint[] = [
  {
    actorRef: 'FIELD-001',
    sectionCode: '1464',
    roleCode: 'LIDER',
    geometryStatus: 'AVAILABLE',
    longitude: -101.68,
    latitude: 21.12,
  },
  {
    actorRef: 'FIELD-002',
    sectionCode: '1465',
    roleCode: 'SIMPATIZANTE',
    geometryStatus: 'AVAILABLE',
    longitude: -101.67,
    latitude: 21.13,
  },
  {
    actorRef: 'FIELD-003',
    sectionCode: '1464',
    roleCode: 'SIMPATIZANTE',
    geometryStatus: 'AVAILABLE',
    longitude: -101.66,
    latitude: 21.14,
  },
]

describe('field workspace logic', () => {
  it('shows the public label for a certified role', () => {
    expect(fieldRoleLabel('LIDER')).toBe('Líder')
  })

  it('filters points by role', () => {
    expect(
      filterFieldPoints(
        points,
        'SIMPATIZANTE',
        '',
      ).map((point) => point.actorRef),
    ).toEqual(['FIELD-002', 'FIELD-003'])
  })

  it('combines role and section filters', () => {
    expect(
      filterFieldPoints(
        points,
        'SIMPATIZANTE',
        '1464',
      ).map((point) => point.actorRef),
    ).toEqual(['FIELD-003'])
  })
})
