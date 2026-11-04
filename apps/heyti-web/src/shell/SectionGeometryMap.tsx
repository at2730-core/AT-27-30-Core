import { useMemo } from 'react'
import { GeographicMap } from './GeographicMap'
import { toGeoJsonFeatureCollection } from './mapGeoJson'
import type { TerritorialGeometryView } from '../gateway/territorial.geometry'

interface SectionGeometryMapProps {
  queryDescription?: string
  territorialGeometry: TerritorialGeometryView
}
export function SectionGeometryMap({
  queryDescription,
  territorialGeometry,
}: SectionGeometryMapProps) {
  const data = useMemo(() => toGeoJsonFeatureCollection([{
    sectionId: territorialGeometry.sectionId,
    geometry: territorialGeometry.geometry,
  }]), [territorialGeometry])

  return (
    <figure className="section-geometry-map">
      <GeographicMap
        data={data}
        style={() => ({ color: '#111111', weight: 1.2, opacity: 1, fillColor: '#777777', fillOpacity: 0.15 })}
      />
      <figcaption>
        <strong>
          {queryDescription ?? `Mapa territorial: sección ${territorialGeometry.sectionId}.`}
        </strong>
        <span>Mapa base OpenStreetMap · Secciones electorales · {territorialGeometry.crs}</span>
      </figcaption>
    </figure>
  )
}