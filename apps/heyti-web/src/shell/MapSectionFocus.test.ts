import { describe, expect, it } from 'vitest'
import { fitUniverseSection } from './MapSectionFocus'
import { collectPositions, geometryBounds, projection } from './mapGeometry'
import type { UniverseMap, UniverseSection } from '../gateway/universe.client'
function section(id: string, x: number, y: number, size: number): UniverseSection {
  return { sectionId: id, status: 'TRACKED_LEAD', leader: 'PAN', total: 100, geometry: { type: 'Polygon', coordinates: [[[x,y],[x+size,y],[x+size,y+size],[x,y+size],[x,y]]] } }
}
const result = { sections: [section('1',0,0,.01),section('2',10,10,.01),section('3',4,4,2)] } as UniverseMap
function positions(s: UniverseSection) { return collectPositions(s.geometry.type === 'Polygon' ? [s.geometry.coordinates] : s.geometry.coordinates) }
describe('zoom vinculado a fila', () => {
  it('centra secciones extremas aun con zoom 8 y conserva límites persistibles', () => {
    const project = projection(geometryBounds(result.sections.flatMap(positions)))
    for (const id of ['1','2','3']) {
      const view = fitUniverseSection(result,id)!
      const bounds = geometryBounds(positions(result.sections.find(s=>s.sectionId===id)!).map(project))
      const cx=(bounds.minX+bounds.maxX)/2, cy=(bounds.minY+bounds.maxY)/2
      expect(400+view.x+view.zoom*(cx-400)).toBeCloseTo(400)
      expect(250+view.y+view.zoom*(cy-250)).toBeCloseTo(250)
      expect(view.zoom).toBeGreaterThanOrEqual(1); expect(view.zoom).toBeLessThanOrEqual(8)
      expect(Math.abs(view.x)).toBeLessThanOrEqual(3200); expect(Math.abs(view.y)).toBeLessThanOrEqual(2000)
    }
    expect(fitUniverseSection(result,'1')!.zoom).toBe(8)
  })
  it('rechaza una sección ausente sin modificar la vista', () => {
    expect(fitUniverseSection(result,'999')).toBeNull()
  })
})
