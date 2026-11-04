import type { UniverseMap } from '../gateway/universe.client'

export interface AreaSectionSelection {
  map: UniverseMap
  sectionId: string
  scope: string
  request: number
}

// Membership is checked against the represented, authorized geometry, not a
// numeric-looking municipality/locality/AGEB identifier.
export function selectAreaSection(previous: AreaSectionSelection | null, map: UniverseMap, sectionId: string, scope: string): AreaSectionSelection | null {
  if (!/^[1-9]\d{0,3}$/.test(sectionId) || !map.sections.some(section => section.sectionId === sectionId)) return previous
  return { map, sectionId, scope, request: (previous?.request ?? 0) + 1 }
}

export function selectionForScope(selection: AreaSectionSelection | null, scope: string): AreaSectionSelection | null {
  return selection?.scope === scope ? selection : null
}

export function clearAreaSource(selection: AreaSectionSelection | null, map: UniverseMap): AreaSectionSelection | null {
  return selection?.map === map ? null : selection
}
