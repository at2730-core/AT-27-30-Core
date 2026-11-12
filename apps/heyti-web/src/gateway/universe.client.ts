import { authenticatedHeaders } from './auth.transport'
import { gatewayBaseUrl } from './heyti.client'
import { parseGeometry } from './territorial.geometry'
import type { TerritorialGeometry } from './territorial.geometry'
import type { ElectoralContestId, ElectoralTrackedParty } from './electoral.response'
export type MapLevel = 'state' | 'municipality' | 'federal-district' | 'local-district'
export interface UniverseOption { level: MapLevel; id: string; label: string; sections: number }
export type MapStatus = 'HHI_LOW' | 'HHI_MID' | 'HHI_HIGH' | 'ABS_LOW' | 'ABS_MID' | 'ABS_HIGH' | 'ABS_VERY_HIGH' | 'TRACKED_LEAD' | 'TIE' | 'ZERO_TOTAL' | 'NO_DATA' | 'NOT_CONTESTED' | 'INCONSISTENT' | 'NO_TRACKED_VOTES'
export interface UniverseSection { sectionId: string; geometry: TerritorialGeometry; status: MapStatus; leader: ElectoralTrackedParty | null; total: number | null; nominal?: number | null; abstention?: number | null; concentration?: number | null; missingReason?: string | null; votes?: Record<string, number | null> }
export interface AbstentionSummary { year: number; validSections: number; nominal: number; votes: number; abstention: number | null }
export interface UniverseMap { results2024?: Record<string, { nominal: number | null; participation: number | null }>; metric?: 'leaders' | 'abstention' | 'concentration'; trend?: AbstentionSummary[]; summary?: { validSections: number; total: number; votes: Record<string, number>; index: number | null; trackedCoverage: number | null }; universe: UniverseOption; year: number; contest: ElectoralContestId; sections: UniverseSection[]; counts: Record<string, number>; coverage: { geographic: number; represented: number; blocked: number; masterOnlyUnmapped?: number }; provenance: Record<string, string> }
const levels = ['state', 'municipality', 'federal-district', 'local-district']
const statuses = ['HHI_LOW', 'HHI_MID', 'HHI_HIGH', 'ABS_LOW', 'ABS_MID', 'ABS_HIGH', 'ABS_VERY_HIGH', 'TRACKED_LEAD', 'TIE', 'ZERO_TOTAL', 'NO_DATA', 'NOT_CONTESTED', 'INCONSISTENT', 'NO_TRACKED_VOTES']
const parties = ['PAN', 'PRI', 'PVEM', 'MORENA']
function record(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Contrato de universo inválido.')
  return value as Record<string, unknown>
}
function str(value: unknown): string { if (typeof value !== 'string' || !value) throw new Error('Identidad de universo inválida.'); return value }
function count(value: unknown): number { if (typeof value !== 'number' || !Number.isSafeInteger(value) || value < 0) throw new Error('Conteo de universo inválido.'); return value }
function option(value: unknown): UniverseOption {
  const o = record(value), level = str(o.level)
  if (!levels.includes(level) || !/^[1-9]\d*$/.test(str(o.id))) throw new Error('Universo no soportado.')
  return { level: level as MapLevel, id: str(o.id), label: str(o.label), sections: count(o.sections) }
}
async function request(payload: unknown, signal?: AbortSignal) {
  const response = await fetch(`${gatewayBaseUrl()}/v1/universes/describe`, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json', ...authenticatedHeaders() }, body: JSON.stringify(payload), signal })
  if (!response.ok) throw new Error(`CORE no pudo consultar el universo (HTTP ${response.status}). Reinicia el CORE si acabas de aplicar este bloque.`)
  const data = record(await response.json())
  if (data.contract !== 'HEYTI_UNIVERSE_RESPONSE' || data.version !== '1.0' || data.capability_id !== 'describe_universe') throw new Error('Contrato de universo no soportado.')
  return data
}
export async function fetchUniverseCatalog(signal?: AbortSignal): Promise<UniverseOption[]> {
  const data = await request({ operation: 'catalog' }, signal)
  if (!Array.isArray(data.catalog)) throw new Error('Catálogo no disponible.')
  const catalog = data.catalog.map(option)
  if (new Set(catalog.map(o => `${o.level}:${o.id}`)).size !== catalog.length) throw new Error('Catálogo con duplicados.')
  return catalog
}
export async function fetchUniverseMap(universe: UniverseOption, year: number, contest: ElectoralContestId, signal?: AbortSignal, metric: 'leaders' | 'abstention' | 'concentration' = 'leaders'): Promise<UniverseMap> {
  const data = await request({ operation: 'map', level: universe.level, id: universe.id, year, contest, metric }, signal)
  if (metric === 'abstention' && (data.metric !== metric || data.classification !== 'FIXED_25_PERCENT_BANDS')) throw new Error('Métrica de abstención inválida.')
  if (metric === 'concentration' && (year !== 2024 || data.metric !== metric || data.classification !== 'PARTIAL_HHI_V1_THRESHOLDS')) throw new Error('Métrica de concentración inválida.')
  const actual = option(data.universe)
  if (actual.level !== universe.level || actual.id !== universe.id || data.year !== year || data.contest !== contest) throw new Error('La respuesta no corresponde al universo solicitado.')
  if (!Array.isArray(data.sections)) throw new Error('Secciones no disponibles.')
  const sections = data.sections.map(value => {
    const row = record(value), status = str(row.status), leader = row.leader === null ? null : str(row.leader)
    if (!statuses.includes(status) || (status === 'TRACKED_LEAD' ? !parties.includes(leader ?? '') : leader !== null) || row.crs !== 'OGC:CRS84') throw new Error('Clasificación o geometría de sección inválida.')
    const sectionId = str(row.section_id)
    if (!/^[1-9]\d*$/.test(sectionId)) throw new Error('Identidad seccional inválida.')
    const total = row.total === null ? null : count(row.total)
    let extra = {}
    if (metric === 'abstention') {
      const nominal = row.nominal === null ? null : count(row.nominal)
      const value = row.abstention
      const valid = status.startsWith('ABS_')
      if (leader !== null || !['ABS_LOW', 'ABS_MID', 'ABS_HIGH', 'ABS_VERY_HIGH', 'NO_DATA', 'NOT_CONTESTED', 'INCONSISTENT'].includes(status)) throw new Error('Categoría de abstención inválida.')
      if (valid) {
        if (total === null || nominal === null || nominal <= 0 || total > nominal || typeof value !== 'number' || !Number.isFinite(value)) throw new Error('Base de abstención inválida.')
        const expected = (nominal - total) * 100 / nominal
        const band = expected < 25 ? 'ABS_LOW' : expected < 50 ? 'ABS_MID' : expected < 75 ? 'ABS_HIGH' : 'ABS_VERY_HIGH'
        if (Math.abs(value - expected) > 1e-8 || band !== status) throw new Error('Abstención no corresponde a sus cifras.')
      } else if (value !== null) throw new Error('Abstención no calculable con porcentaje.')
      extra = { nominal, abstention: value as number | null }
    } else if (status.startsWith('ABS_')) throw new Error('Métrica inesperada.')
    const missingReason = row.missing_reason == null ? null : str(row.missing_reason)
    if (missingReason !== null && !['TOTAL_OR_NOMINAL_MISSING','TOTAL_MISSING','TRACKED_BREAKDOWN_MISSING'].includes(missingReason)) throw new Error('Causa de faltante inválida.')
    if (metric === 'concentration') {
      if (leader !== null || !['HHI_LOW','HHI_MID','HHI_HIGH','NO_DATA','INCONSISTENT','ZERO_TOTAL','NOT_CONTESTED'].includes(status)) throw new Error('Categoría de concentración inválida.')
      const votes = Object.fromEntries(parties.map(p => { const value = record(row.votes)[p]; return [p, value === null ? null : count(value)] }))
      if (status.startsWith('HHI_')) {
        if (total === null || total <= 0 || Object.values(votes).some(v => v === null) || Object.values(votes).reduce<number>((n,v)=>n+(v??0),0) > total) throw new Error('Base de concentración inválida.')
        const expected = Object.values(votes).reduce<number>((n,v)=>n+((v??0)/total)**2,0)
        const band = expected >= .45 ? 'HHI_HIGH' : expected >= .30 ? 'HHI_MID' : 'HHI_LOW'
        if (typeof row.concentration !== 'number' || !Number.isFinite(row.concentration) || Math.abs(row.concentration-expected)>1e-8 || band !== status) throw new Error('Índice no corresponde a los votos.')
      } else if (row.concentration !== null) throw new Error('Índice no calculable con valor.')
      extra = { concentration: row.concentration as number | null, votes }
    } else if (status.startsWith('HHI_')) throw new Error('Métrica inesperada.')
    // Las lecturas de área necesitan el desglose que el CORE ya entrega en leaders.
    // Respuestas antiguas sin desglose conservan N/D; no se completan cifras.
    if (metric === 'leaders' && row.votes !== undefined) {
      const rawVotes = record(row.votes)
      const votes = Object.fromEntries(parties.map(p => [p, rawVotes[p] === null ? null : count(rawVotes[p])]))
      extra = { ...extra, votes }
    }
    return { ...extra, missingReason, sectionId, geometry: parseGeometry(row.geometry), status: status as MapStatus, leader: leader as ElectoralTrackedParty | null, total: row.total === null ? null : count(row.total) }
  })
  if (new Set(sections.map(s => s.sectionId)).size !== sections.length) throw new Error('Secciones duplicadas.')
  const cov = record(data.coverage), coverage = { geographic: count(cov.geographic_sections), represented: count(cov.represented_sections), blocked: count(cov.blocked_sections), ...(cov.master_only_unmapped === undefined ? {} : {masterOnlyUnmapped: count(cov.master_only_unmapped)}) }
  if (coverage.represented !== sections.length || coverage.represented + coverage.blocked !== coverage.geographic || coverage.geographic !== actual.sections) throw new Error('Cobertura de universo inconsistente.')
  const computed: Record<string, number> = {}
  sections.forEach(s => { const k = s.leader ?? s.status; computed[k] = (computed[k] ?? 0) + 1 })
  const counts = Object.fromEntries(Object.entries(record(data.counts)).map(([k, v]) => [k, count(v)]))
  if (JSON.stringify(Object.entries(computed).sort()) !== JSON.stringify(Object.entries(counts).sort())) throw new Error('Leyenda no corresponde al mapa.')
  const provenance = Object.fromEntries(Object.entries(record(data.provenance)).map(([k, v]) => [k, str(v)]))
  if (provenance.electoral_scope !== 'TRACKED_PARTIES_ONLY' || provenance.grouping_basis !== 'PROPERTIES_OF_CURRENT_GEOJSON' || provenance.electoral_validation !== 'AUDIT_PENDING') throw new Error('Procedencia no soportada.')
  let trend: AbstentionSummary[] | undefined
  if (metric === 'abstention') {
    if (!Array.isArray(data.trend) || data.trend.length !== 3) throw new Error('Historial de abstención incompleto.')
    trend = data.trend.map((value, index) => {
      const row = record(value), y = count(row.year), validSections = count(row.valid_sections), nominal = count(row.nominal), votes = count(row.votes)
      if (y !== [2018, 2021, 2024][index] || validSections > coverage.represented || votes > nominal) throw new Error('Historial inconsistente.')
      const expected = nominal > 0 ? (nominal - votes) * 100 / nominal : null
      if (expected === null ? row.abstention !== null || validSections !== 0 || votes !== 0 : typeof row.abstention !== 'number' || Math.abs(row.abstention - expected) > 1e-8 || validSections === 0) throw new Error('Porcentaje histórico inválido.')
      return { year: y, validSections, nominal, votes, abstention: expected }
    })
    const selected = trend.find(t => t.year === year)!
    const valid = sections.filter(s => s.status.startsWith('ABS_'))
    if (selected.validSections !== valid.length || selected.votes !== valid.reduce((n,s) => n + (s.total ?? 0), 0) || selected.nominal !== valid.reduce((n,s) => n + (('nominal' in s ? s.nominal : 0) as number ?? 0), 0)) throw new Error('Resumen no corresponde al mapa.')
  }
  let summary: UniverseMap['summary']
  if (metric === 'concentration') {
    const row = record(data.summary), valid = sections.filter(s => s.status.startsWith('HHI_'))
    const votes = Object.fromEntries(parties.map(p => [p,count(record(row.votes)[p])]))
    const total = count(row.total), validSections = count(row.valid_sections)
    if (validSections !== valid.length || total !== valid.reduce((n,s)=>n+(s.total??0),0) || parties.some(p=>votes[p]!==valid.reduce((n,s)=>n+('votes' in s ? (s.votes as Record<string,number>)[p] : 0),0))) throw new Error('Resumen de concentración no corresponde al mapa.')
    const index = total ? Object.values(votes).reduce((n,v)=>n+(v/total)**2,0) : null
    const trackedCoverage = total ? Object.values(votes).reduce((n,v)=>n+v,0)/total : null
    for (const [key, expected] of [['index',index],['tracked_coverage',trackedCoverage]] as const) {
      if (expected === null ? row[key] !== null : typeof row[key] !== 'number' || !Number.isFinite(row[key]) || Math.abs((row[key] as number)-expected)>1e-8) throw new Error('Índice agregado inválido.')
    }
    summary = { validSections,total,votes,index,trackedCoverage }
  }
  return { universe: actual, year, contest, sections, counts, coverage, provenance, metric, trend, summary }
}
