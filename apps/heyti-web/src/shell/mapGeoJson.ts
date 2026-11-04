import type { TerritorialGeometry } from '../gateway/territorial.geometry'

export interface GeoJsonFeatureCollection {
  type: 'FeatureCollection'
  features: Array<{
    type: 'Feature'
    geometry: {
      type: 'Polygon' | 'MultiPolygon'
      coordinates: unknown
    }
    properties: {
      sectionId: string
      status: string | null
      leader: string | null
      [key: string]: unknown
    }
  }>
}

export interface MapGeoJsonSection {
  sectionId: string
  status?: string
  leader?: string | null
  geometry: TerritorialGeometry
}

export function toGeoJsonFeatureCollection(sections: MapGeoJsonSection[]): GeoJsonFeatureCollection {
  return {
    type: 'FeatureCollection',
    features: sections.map((section) => ({
      type: 'Feature',
      geometry: {
        type: section.geometry.type,
        coordinates: section.geometry.coordinates,
      },
      properties: {
        sectionId: section.sectionId,
        status: section.status ?? null,
        leader: section.leader ?? null,
      },
    })),
  }
}
