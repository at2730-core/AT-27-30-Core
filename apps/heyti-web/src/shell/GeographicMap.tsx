import { useEffect, useId, useRef, useState } from 'react'
import { visibleSectionLabels } from './leafletLabelVisibility'
import type { SectionLabelMode, LabelCandidate } from './leafletLabelVisibility'
import { GeoJSON, MapContainer, TileLayer, useMap } from 'react-leaflet'
import { DomEvent, geoJSON } from 'leaflet'
import type { GeoJSON as LeafletGeoJSON, PathOptions, Polygon as LeafletPolygon } from 'leaflet'
import type { Feature, GeoJsonObject } from 'geojson'
import type { GeoJsonFeatureCollection } from './mapGeoJson'
import 'leaflet/dist/leaflet.css'
import './GeographicMap.css'

interface GeographicMapProps {
  data: GeoJsonFeatureCollection
  contextData?: GeoJsonFeatureCollection
  mapAriaLabel?: string
  showSectionLabels?: boolean
  selectedSection?: string | null
  onSelectSection?: (id: string) => void
  style: (feature?: Feature) => PathOptions
}

function GeographicLayers({ data, contextData, selectedSection, onSelectSection, style, showSectionLabels = false }: GeographicMapProps) {
  const map = useMap()
  const layer = useRef<LeafletGeoJSON>(null)
  const recenter = useRef<HTMLButtonElement>(null)
  const labelControl = useRef<HTMLDivElement>(null)
  const labelControlId = useId()
  const [labelMode, setLabelMode] = useState<SectionLabelMode>('auto')
  const context = useRef<LeafletGeoJSON>(null)
  useEffect(() => {
    // Keep Leaflet's credit as text, without the decorative SVG flag.
    map.attributionControl?.setPrefix('<a href="https://leafletjs.com" title="Leaflet">Leaflet</a>')
  }, [map])

  useEffect(() => {
    if (!layer.current) return
    // React Leaflet does not update GeoJSON's data prop after mounting.
    layer.current.clearLayers().addData(data as GeoJsonObject)
    const bounds = layer.current.getBounds()
    if (bounds.isValid()) map.fitBounds(bounds, { padding: [24, 24], maxZoom: 16 })
  }, [data, map])

  useEffect(() => {
    if (!context.current || !contextData) return
    context.current.clearLayers().addData(contextData as GeoJsonObject)
    if (!data.features.length) {
      const bounds = context.current.getBounds()
      if (bounds.isValid()) map.fitBounds(bounds, {padding:[24,24],maxZoom:16})
    }
  }, [contextData, data, map])

  useEffect(() => {
    layer.current?.setStyle(style)
  }, [data, style])

  useEffect(() => {
    if (!selectedSection) return
    const feature = data.features.find(item => item.properties.sectionId === selectedSection)
    if (!feature) return
    const bounds = geoJSON(feature as GeoJsonObject).getBounds()
    if (bounds.isValid()) map.fitBounds(bounds, { padding: [32, 32], maxZoom: 16 })
  }, [data, map, selectedSection])

  useEffect(() => {
    if (!showSectionLabels) return
    const refresh = () => {
      if (!layer.current) return
      const polygons: {id:string; polygon:LeafletPolygon; feature:Feature}[] = []
      const candidates:LabelCandidate[] = []
      layer.current.eachLayer(item => {
        const polygon = item as LeafletPolygon & {feature?:Feature}
        const feature = polygon.feature
        const id = String(feature?.properties?.sectionId ?? '')
        if (!feature || !id || !polygon.getCenter) return
        const point = map.latLngToContainerPoint(polygon.getCenter())
        candidates.push({id, x:point.x, y:point.y})
        polygons.push({id, polygon, feature})
      })
      const size = map.getSize()
      const visible = visibleSectionLabels(candidates, selectedSection, labelMode, size.x, size.y, map.getZoom())
      for (const {id, polygon, feature} of polygons) {
        const permanent = visible.has(id)
        if (polygon.getTooltip()?.options.permanent === permanent) continue
        polygon.unbindTooltip()
        const label = document.createElement('span')
        const detail = feature.properties?.featureLabel ? String(feature.properties.featureLabel) : `Sección ${id}${feature.properties?.referenceLabel ? ' · '+String(feature.properties.referenceLabel) : ''}`
        label.textContent = permanent ? id : detail
        label.title = detail
        polygon.bindTooltip(label, permanent ? {permanent:true, direction:'center', className:'geographic-section-label'} : {sticky:true})
      }
    }
    refresh()
    map.on('zoomend moveend resize', refresh)
    return () => { map.off('zoomend moveend resize', refresh) }
  }, [data, map, showSectionLabels, labelMode, selectedSection])

  useEffect(() => {
    const observer = new ResizeObserver(() => map.invalidateSize({ pan: false }))
    observer.observe(map.getContainer())
    if (recenter.current) DomEvent.disableClickPropagation(recenter.current)
    if (labelControl.current) { DomEvent.disableClickPropagation(labelControl.current); DomEvent.disableScrollPropagation(labelControl.current) }
    return () => observer.disconnect()
  }, [map, showSectionLabels])

  return <>
    <TileLayer
      url="https://tile.openstreetmap.org/{z}/{x}/{y}.png"
      maxZoom={19}
      attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    />
    {contextData ? <GeoJSON ref={context} data={contextData as GeoJsonObject} interactive={false} style={{fill:false,color:'#334155',weight:1.5,dashArray:'5 4',opacity:.85}}/> : null}
    <GeoJSON
      ref={layer}
      data={data as GeoJsonObject}
      style={style}
      onEachFeature={(feature, sectionLayer) => {
        const label = document.createElement('span')
        label.textContent = feature.properties?.featureLabel ? String(feature.properties.featureLabel) : `Sección ${String(feature.properties?.sectionId ?? '')}${feature.properties?.referenceLabel ? ' · ' + String(feature.properties.referenceLabel) : ''}`
        sectionLayer.bindTooltip(label, { sticky: true })
      }}
      eventHandlers={{ click: event => {
        const id = String(event.layer?.feature?.properties?.sectionId ?? '')
        if (id) onSelectSection?.(id)
      } }}
    />
    {showSectionLabels ? <div ref={labelControl} className="geographic-label-control" onKeyDown={event=>event.stopPropagation()}>
      <label htmlFor={labelControlId}>Etiquetas de sección</label>
      <select id={labelControlId} value={labelMode} onChange={event=>setLabelMode(event.target.value as SectionLabelMode)}>
        <option value="auto">Automáticas</option><option value="all">Todas</option><option value="hidden">Ocultas</option>
      </select>
      <small>La seleccionada permanece visible.</small>
    </div> : null}
    <button ref={recenter} type="button" className="geographic-map-recenter" onClick={() => {
      const bounds = data.features.length ? layer.current?.getBounds() : context.current?.getBounds()
      if (bounds?.isValid()) map.fitBounds(bounds, { padding: [24, 24], maxZoom: 16 })
    }}>Recentrar</button>
  </>
}

export function GeographicMap(props: GeographicMapProps) {
  return <MapContainer
    className="geographic-map"
    aria-label={props.mapAriaLabel ?? "Mapa de calles y secciones electorales"}
    center={[21, -101]}
    zoom={8}
    maxZoom={19}
    scrollWheelZoom
  >
    <GeographicLayers {...props} />
  </MapContainer>
}
