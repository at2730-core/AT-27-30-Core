import type { UniverseMap } from '../gateway/universe.client'
import { collectPositions, geometryBounds, projection } from './mapGeometry'
export function fitUniverseSection(result: UniverseMap, sectionId: string): { zoom: number; x: number; y: number } | null {
  const selected = result.sections.find(s => s.sectionId === sectionId)
  if (!selected) return null
  const polygons = (geometry: UniverseMap['sections'][number]['geometry']) => geometry.type === 'Polygon' ? [geometry.coordinates] : geometry.coordinates
  const all = result.sections.flatMap(s => collectPositions(polygons(s.geometry)))
  if (!all.length) return null
  const project = projection(geometryBounds(all))
  const positions = collectPositions(polygons(selected.geometry)).map(project)
  if (!positions.length) return null
  const bounds = geometryBounds(positions)
  const width = bounds.maxX - bounds.minX, height = bounds.maxY - bounds.minY
  const zoom = Math.max(1, Math.min(8, width > 0 ? 560 / width : 8, height > 0 ? 350 / height : 8))
  const centerX = (bounds.minX + bounds.maxX) / 2, centerY = (bounds.minY + bounds.maxY) / 2
  return { zoom, x: Math.max(-3200, Math.min(3200, zoom * (400 - centerX))), y: Math.max(-2000, Math.min(2000, zoom * (250 - centerY))) }
}
