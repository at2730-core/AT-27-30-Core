import type { UniverseMap, UniverseSection } from '../gateway/universe.client'
export const REFERENCE_PARTIES = ['PAN', 'PRI', 'PVEM', 'MORENA'] as const
export type ReferenceParty = typeof REFERENCE_PARTIES[number]
export interface ReferenceSettings { party: ReferenceParty; unit: 'votes' | 'pp'; cap: number; emphasis: number }
export type ReferenceMap = UniverseMap & { historicalReference: ReferenceSettings }
export interface ReferenceRow { sectionId: string; status: string; selected: number | null; contrast: number | null; contrastParties: string[]; leaders: string[]; difference: number | null; pp: number | null; total: number | null }
export function referenceSettings(result: UniverseMap): ReferenceSettings | null {
  return (result as Partial<ReferenceMap>).historicalReference ?? null
}
export function historicalReference(section: UniverseSection, party: ReferenceParty): ReferenceRow {
  if (!REFERENCE_PARTIES.includes(party)) throw new Error('Selecciona una opción de referencia disponible.')
  const row: ReferenceRow = { sectionId: section.sectionId, status: section.status, selected: section.votes?.[party] ?? null, contrast: null, contrastParties: [], leaders: [], difference: null, pp: null, total: section.total }
  if (section.status === 'NOT_CONTESTED' || section.status === 'INCONSISTENT' || section.status === 'NO_DATA') return row
  const values = REFERENCE_PARTIES.map(p => ({ party: p, votes: section.votes?.[p] ?? null }))
  if (section.total == null || values.some(v => v.votes === null)) return { ...row, status: 'NO_DATA' }
  if (!Number.isSafeInteger(section.total) || section.total < 0 || values.some(v => !Number.isSafeInteger(v.votes) || v.votes! < 0) || values.reduce((n,v)=>n+v.votes!,0) > section.total) return { ...row, status: 'INCONSISTENT' }
  if (section.total === 0) return { ...row, status: 'ZERO_TOTAL' }
  const others = values.filter(v=>v.party !== party), maximumOther = Math.max(...others.map(v=>v.votes!)), maximum = Math.max(...values.map(v=>v.votes!))
  const difference = row.selected! - maximumOther
  return { ...row, status: maximum === 0 ? 'NO_TRACKED_VOTES' : 'AVAILABLE', contrast: maximumOther, contrastParties: others.filter(v=>v.votes===maximumOther).map(v=>v.party), leaders: maximum === 0 ? [] : values.filter(v=>v.votes===maximum).map(v=>v.party), difference, pp: difference / section.total * 100 }
}
export function referenceStyle(row: ReferenceRow, settings: ReferenceSettings) {
  const value = settings.unit === 'votes' ? row.difference : row.pp
  if (value === null || value === 0) return { fillColor: '#94a3b8', fillOpacity: 0.2 }
  const intensity = Math.min(1, Math.abs(value) / settings.cap) * (Math.abs(value) < settings.emphasis ? 0.25 : 1)
  return { fillColor: value > 0 ? '#2563eb' : '#c56a26', fillOpacity: 0.2 + intensity * 0.4 }
}
export function referenceLabel(row: ReferenceRow, settings: ReferenceSettings) {
  return row.difference === null ? `No calculable: ${row.status}` : `${settings.party}: ${row.selected} votos históricos; contraste ${row.contrastParties.join(' / ')}: ${row.contrast}; diferencia ${row.difference} votos (${row.pp!.toFixed(3)} pp)`
}
export function attachHistoricalReference(result: UniverseMap, settings: ReferenceSettings): ReferenceMap {
  if (result.year !== 2024 || result.metric !== 'concentration' || !REFERENCE_PARTIES.includes(settings.party) || !['votes','pp'].includes(settings.unit) || !Number.isFinite(settings.cap) || settings.cap <= 0 || !Number.isFinite(settings.emphasis) || settings.emphasis < 0) throw new Error('Parámetros históricos o de escala inválidos.')
  return { ...result, historicalReference: { ...settings } }
}
export const referenceStatusLabels: Record<string, string> = {
  AVAILABLE: 'Diferencia histórica calculable', NO_DATA: 'Datos insuficientes',
  INCONSISTENT: 'Cifras inconsistentes', NOT_CONTESTED: 'Contienda no celebrada',
  ZERO_TOTAL: 'Total observado cero; diferencia no calculada', NO_TRACKED_VOTES: 'Sin votos en las opciones rastreadas',
}