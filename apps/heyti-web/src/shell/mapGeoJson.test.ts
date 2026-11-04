import { describe, expect, it } from 'vitest'
import { toGeoJsonFeatureCollection } from './mapGeoJson'

describe('toGeoJsonFeatureCollection', () => {
  it('converts section geometries into a GeoJSON feature collection with section metadata', () => {
    const collection = toGeoJsonFeatureCollection([
      {
        sectionId: '101',
        status: 'TRACKED_LEAD',
        leader: 'PAN',
        geometry: { type: 'Polygon', coordinates: [[[0, 0], [1, 0], [1, 1], [0, 0]]] },
      },
      {
        sectionId: '102',
        status: 'ABS_MID',
        geometry: { type: 'MultiPolygon', coordinates: [[[[0, 0], [2, 0], [2, 2], [0, 0]]]] },
      },
    ] as any)

    expect(collection.type).toBe('FeatureCollection')
    expect(collection.features).toHaveLength(2)
    expect(collection.features[0].properties).toMatchObject({ sectionId: '101', status: 'TRACKED_LEAD', leader: 'PAN' })
    expect(collection.features[1].properties).toMatchObject({ sectionId: '102', status: 'ABS_MID', leader: null })
  })
})
