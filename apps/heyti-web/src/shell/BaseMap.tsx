import { geographicGroupsOf, geographicLabel } from './geographicGroups'
import { sensitivityLabel, sensitivityStyle } from './participationSensitivity'
import type { ParticipationSensitivity } from './participationSensitivity'
import { historicalReference, referenceLabel, referenceSettings, referenceStyle } from './historicalReference'
import { useMemo } from 'react'
import { GeographicMap } from './GeographicMap'
import { toGeoJsonFeatureCollection } from './mapGeoJson'
import type { UniverseMap } from '../gateway/universe.client'
import { outcomeColors } from './UniverseGeometryMap'

interface BaseMapProps {
  result: UniverseMap
  selectedSection?: string | null
  onSelectSection?: (id: string) => void
  sensitivity?: ParticipationSensitivity
  neutral?: boolean
}

function styleFeature(sectionId: string, selectedSection: string | null | undefined) {
  return {
    color: selectedSection === sectionId ? '#059669' : '#111111',
    weight: selectedSection === sectionId ? 2.4 : 1.2,
    opacity: 1,
    fillOpacity: 0.15,
    fillColor: '#777777',
  }
}

export function BaseMap({ result, selectedSection, onSelectSection, sensitivity, neutral = false }: BaseMapProps) {
  const featureCollection = useMemo(() => {
    const sections = result.sections.map((section) => ({
      sectionId: section.sectionId,
      status: section.leader ?? section.status,
      leader: section.leader,
      geometry: section.geometry,
    }))

    const collection = toGeoJsonFeatureCollection(sections)
    const settings = referenceSettings(result)
    if (settings) collection.features.forEach((feature, index) => {
      feature.properties.referenceLabel = referenceLabel(historicalReference(result.sections[index], settings.party), settings)
    })
    if (sensitivity) collection.features.forEach(feature => {
      const row = sensitivity.rows[feature.properties.sectionId]
      if (row) feature.properties.referenceLabel = sensitivityLabel(row)
    })
    const groups = geographicGroupsOf(result)
    if (groups) collection.features.forEach(feature => {
      const row = groups.rows[feature.properties.sectionId]
      if (row) feature.properties.referenceLabel = geographicLabel(row)
    })
    return collection
  }, [result, sensitivity])

  const geographic = geographicGroupsOf(result)
  const groupColors = useMemo(() => new Map(geographic?.groups.map(g => [g.id, g.color]) ?? []), [geographic])
  const reference = referenceSettings(result)
  const referenceRows = useMemo(() => new Map(result.sections.map(s => [s.sectionId, s])), [result])
  return (
      <GeographicMap
        data={featureCollection}
        showSectionLabels
        selectedSection={selectedSection}
        onSelectSection={onSelectSection}
        style={(feature) => {
          const sectionId = String(feature?.properties?.sectionId ?? '')
          const status = String(feature?.properties?.status ?? 'NO_DATA')
          const fill = outcomeColors[status] ?? '#2a9d8f'

          return {
            ...styleFeature(sectionId, selectedSection),
            fillColor: neutral ? '#777777' : fill,
            fillOpacity: neutral ? 0.15 : 0.3,
            ...(sensitivity?.rows[sectionId] ? sensitivityStyle(sensitivity.rows[sectionId]) : {}),
            ...(geographic ? {fillColor: groupColors.get(geographic.rows[sectionId]?.groupId ?? '') ?? '#777777', fillOpacity: 0.35} : {}),
            ...(reference && referenceRows.has(sectionId) ? referenceStyle(historicalReference(referenceRows.get(sectionId)!, reference.party), reference) : {}),
          }
        }}
      />
  )
}
