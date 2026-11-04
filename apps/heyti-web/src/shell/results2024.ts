import type { UniverseMap } from '../gateway/universe.client'

export type Results2024SortField = 'section' | 'nominal' | 'participation' | 'total' | 'PAN' | 'PRI' | 'PVEM' | 'MORENA'

export interface Result2024Extra { nominal: number | null; participation: number | null }

function sectionNumber(sectionId: string): number {
  const value = Number(sectionId)
  return Number.isFinite(value) ? value : Number.MAX_SAFE_INTEGER
}

function compareSectionIds(a: string, b: string): number {
  return sectionNumber(a) - sectionNumber(b)
}

function getSortableValue<T extends { sectionId: string; total?: number | null; votes?: Record<string, number | null> }>(
  row: T,
  field: Results2024SortField,
  extra: Record<string, { nominal: number | null; participation: number | null }> = {}
): number | null {
  if (field === 'section') return sectionNumber(row.sectionId)
  if (field === 'nominal') return extra[row.sectionId]?.nominal ?? null
  if (field === 'participation') return extra[row.sectionId]?.participation ?? null
  if (field === 'total') return row.total ?? null
  return row.votes?.[field] ?? null
}

export function attachResults2024(base: UniverseMap, nominalMap: UniverseMap): UniverseMap {
  const provenance=(m:UniverseMap)=>JSON.stringify(Object.entries(m.provenance).sort(([a],[b])=>a.localeCompare(b)))
  if(base.metric!=='concentration'||nominalMap.metric!=='abstention'||base.year!==2024||nominalMap.year!==2024||base.contest!==nominalMap.contest||base.universe.id!==nominalMap.universe.id||base.universe.level!==nominalMap.universe.level||provenance(base)!==provenance(nominalMap))throw new Error('Las respuestas no comparten universo, contienda o fuente.')
  const rows=new Map(nominalMap.sections.map(s=>[s.sectionId,s]))
  if(rows.size!==base.sections.length)throw new Error('Coberturas de las respuestas diferentes.')
  const results2024=Object.fromEntries(base.sections.map(s=>{
    const n=rows.get(s.sectionId)
    if(!n||n.total!==s.total)throw new Error('Las cifras o identidades de las respuestas no coinciden.')
    return [s.sectionId,{nominal:n.nominal??null,participation:n.status.startsWith('ABS_')&&n.abstention!=null?100-n.abstention:null}]
  }))
  return {...base,results2024}
}

export function orderSections2024<T extends { sectionId: string; total?: number | null; votes?: Record<string, number | null> }>(
  rows: T[],
  descending: boolean,
  field: Results2024SortField = 'section',
  extra: Record<string, { nominal: number | null; participation: number | null }> = {}
): T[] {
  return [...rows].sort((a, b) => {
    const aValue = getSortableValue(a, field, extra)
    const bValue = getSortableValue(b, field, extra)

    if (aValue == null && bValue == null) return compareSectionIds(a.sectionId, b.sectionId) * (descending ? -1 : 1)
    if (aValue == null) return 1
    if (bValue == null) return -1

    const delta = aValue - bValue
    if (delta === 0) return compareSectionIds(a.sectionId, b.sectionId) * (descending ? -1 : 1)
    return (delta < 0 ? -1 : 1) * (descending ? -1 : 1)
  })
}
