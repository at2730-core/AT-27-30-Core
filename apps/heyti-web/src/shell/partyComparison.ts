import type { UniverseMap } from '../gateway/universe.client'
import type { ParticipationScenario } from './participationScenario'
import { allocateScenarioVotes } from './winScenario'
export const COMPARISON_PARTIES = ['PAN', 'PRI', 'PVEM', 'MORENA'] as const
export interface ComparisonRow { sectionId: string; status: string; historical: Record<string, number | null>; estimated: Record<string, number> | null; difference: Record<string, number> | null; total: number | null; residual: number | null; leaders: string[] }
export interface PartyComparison { rows: Record<string, ComparisonRow>; valid: number; totals: Record<string, { historical: number; estimated: number; difference: number }> }
export function comparePartyVotes(scenario: ParticipationScenario, source: UniverseMap): PartyComparison {
  const base = scenario.base
  if (source.metric !== 'concentration' || source.year !== 2024 || source.contest !== base.contest || source.universe.id !== base.universe.id || source.universe.level !== base.universe.level || Object.keys({ ...source.provenance, ...base.provenance }).some(k => source.provenance[k] !== base.provenance[k]) || source.sections.map(s=>s.sectionId).sort().join(',') !== base.sections.map(s=>s.sectionId).sort().join(',')) throw new Error('Desglose incompatible con el escenario histórico.')
  const baseRows = new Map(base.sections.map(s=>[s.sectionId,s])), rows: Record<string, ComparisonRow> = {}
  const totals = Object.fromEntries(COMPARISON_PARTIES.map(p=>[p,{ historical: 0, estimated: 0, difference: 0 }]))
  let valid=0
  for (const s of source.sections) {
    const projection=scenario.rows[s.sectionId]
    if (s.total !== baseRows.get(s.sectionId)!.total) throw new Error('Totales históricos incompatibles.')
    const historical=Object.fromEntries(COMPARISON_PARTIES.map(p=>[p,s.votes?.[p]??null]))
    const row: ComparisonRow={sectionId:s.sectionId,status:'NO_DATA',historical,estimated:null,difference:null,total:null,residual:null,leaders:[]}
    if (s.status === 'INCONSISTENT' || projection.reason === 'INCONSISTENT') row.status='INCONSISTENT'
    else if (s.total === 0) row.status='ZERO_TOTAL'
    else if (s.status.startsWith('HHI_') && projection.percent !== null && projection.nominal != null && projection.nominal > 0 && s.total != null && s.total > 0 && Object.values(historical).every(v=>v!==null)) {
      const sum=Object.values(historical).reduce<number>((n,v)=>n+v!,0)
      if (sum>s.total) throw new Error('Desglose excede total histórico.')
      const shares=Object.fromEntries(COMPARISON_PARTIES.map(p=>[p,historical[p]!/s.total!]));shares.RESIDUAL=(s.total-sum)/s.total
      row.total=Math.round(projection.nominal*projection.percent/100)
      const allocation=allocateScenarioVotes(row.total,shares)
      row.estimated=Object.fromEntries(COMPARISON_PARTIES.map(p=>[p,allocation[p]]));row.residual=allocation.RESIDUAL
      row.difference=Object.fromEntries(COMPARISON_PARTIES.map(p=>[p,allocation[p]-historical[p]!]))
      const maximum=Math.max(...Object.values(row.estimated));row.leaders=maximum>0?COMPARISON_PARTIES.filter(p=>allocation[p]===maximum):[]
      row.status=row.leaders.length===1?row.leaders[0]:row.leaders.length>1?'TIE':'NO_TRACKED_VOTES';valid++
      for (const p of COMPARISON_PARTIES) { totals[p].historical+=historical[p]!;totals[p].estimated+=allocation[p];totals[p].difference+=row.difference[p] }
    }
    rows[s.sectionId]=row
  }
  return {rows,valid,totals}
}
export function comparisonRowLabel(row: ComparisonRow): string { return row.estimated ? `Comparación descriptiva 2027 · ${COMPARISON_PARTIES.map(p=>`${p}: ${row.estimated![p]} estimados`).join(' · ')} · mayor votación rastreada: ${row.leaders.join(' / ')||'sin votos rastreados'}` : `No calculable: ${row.status}` }
