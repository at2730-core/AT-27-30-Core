import type { UniverseMap, UniverseOption, UniverseSection } from '../gateway/universe.client'
import { fetchUniverseMap } from '../gateway/universe.client'
import type { ElectoralContestId } from '../gateway/electoral.response'
export const AREA_PARTIES = ['PAN', 'PRI', 'PVEM', 'MORENA'] as const
export type AreaKind = 'area-comparison' | 'area-competitiveness' | 'area-top3'
export const AREA_TITLES: Record<AreaKind, string> = {
  'area-comparison': 'Comparativa histórica por universo',
  'area-competitiveness': 'Competitividad por universo · lectura parcial',
  'area-top3': 'Top 3 por universo · partidos rastreados',
}
export function isAreaKind(value: string | undefined): value is AreaKind {
  return value === 'area-comparison' || value === 'area-competitiveness' || value === 'area-top3'
}
export interface AreaReading { kind: AreaKind; maps: UniverseMap[] }
export function areaReading(map: UniverseMap | null | undefined): AreaReading | null {
  return (map as (UniverseMap & { areaReading?: AreaReading }) | null | undefined)?.areaReading ?? null
}
export function rankAreaSection(section: UniverseSection) {
  const ranked = AREA_PARTIES.map(party => ({ party, votes: section.votes?.[party] ?? null }))
    .sort((a, b) => (b.votes ?? -1) - (a.votes ?? -1) || AREA_PARTIES.indexOf(a.party) - AREA_PARTIES.indexOf(b.party))
  const total = section.total
  const complete = ranked.every(row => row.votes !== null && Number.isSafeInteger(row.votes) && row.votes >= 0)
  const completeData = !['NOT_CONTESTED', 'INCONSISTENT', 'NO_DATA'].includes(section.status) && total !== null && total > 0 && Number.isSafeInteger(total) && complete && ranked.reduce((sum, row) => sum + row.votes!, 0) <= total
  const valid = completeData && ranked[0].votes! > 0
  const reason = section.status === 'NOT_CONTESTED' ? 'Elección no celebrada' : section.status === 'INCONSISTENT' ? 'Cifras inconsistentes' : total === 0 ? 'Total en cero' : completeData && !valid ? 'Sin votos rastreados' : !valid ? 'Datos incompletos o inconsistentes' : 'Disponible · sin certificar'
  const rows = ranked.map(row => ({ ...row, rank: valid ? 1 + ranked.filter(other => other.votes! > row.votes!).length : null }))
  const margin = valid ? ranked[0].votes! - ranked[1].votes! : null
  const points = margin === null ? null : margin / total! * 100
  const band = points === null ? null : points < 5 ? 'Menos de 5 pp' : points < 10 ? 'De 5 a menos de 10 pp' : '10 pp o más'
  return { valid, completeData, reason, rows, margin, points, band, top: valid ? rows.filter(row => row.rank! <= 3) : [] }
}
export function summarizeArea(map: UniverseMap) {
  const eligible = map.sections.filter(section => rankAreaSection(section).completeData)
  return { year: map.year, calculable: eligible.length, total: eligible.length ? eligible.reduce((sum, section) => sum + section.total!, 0) : null,
    votes: Object.fromEntries(AREA_PARTIES.map(party => [party, eligible.length ? eligible.reduce((sum, section) => sum + section.votes![party]!, 0) : null])) as Record<string, number | null> }
}
export function attachAreaReading(maps: UniverseMap[], kind: AreaKind, year: number): UniverseMap {
  const expected = kind === 'area-comparison' ? [2018, 2021, 2024] : [year]
  if (maps.length !== expected.length || expected.some(y => maps.filter(map => map.year === y).length !== 1)) throw new Error('Cobertura anual de la consulta incompleta o duplicada.')
  const first = maps[0]
  const provenance = (map: UniverseMap) => JSON.stringify(Object.entries(map.provenance).sort(([a], [b]) => a.localeCompare(b)))
  const ids = (map: UniverseMap) => map.sections.map(s => s.sectionId).sort((a,b) => Number(a) - Number(b)).join(',')
  if (maps.some(map => (map.metric ?? 'leaders') !== 'leaders' || map.contest !== first.contest || map.universe.level !== first.universe.level || map.universe.id !== first.universe.id || provenance(map) !== provenance(first) || ids(map) !== ids(first) || map.coverage.geographic !== first.coverage.geographic || map.coverage.blocked !== first.coverage.blocked)) throw new Error('No se combinan universos, contiendas, coberturas o fuentes distintas.')
  const selected = maps.find(map => map.year === year)
  if (!selected) throw new Error('Año del mapa no disponible.')
  return { ...selected, areaReading: { kind, maps: [...maps].sort((a,b) => a.year - b.year) } } as UniverseMap & { areaReading: AreaReading }
}
export async function loadAreaReading(universe: UniverseOption, contest: ElectoralContestId, kind: AreaKind, year: number, signal: AbortSignal) {
  if (![2018,2021,2024].includes(year)) throw new Error('Año no disponible.')
  const years = kind === 'area-comparison' ? [2018,2021,2024] : [year]
  const maps = await Promise.all(years.map(y => fetchUniverseMap(universe, y, contest, signal, 'leaders')))
  signal.throwIfAborted()
  return attachAreaReading(maps, kind, year)
}
