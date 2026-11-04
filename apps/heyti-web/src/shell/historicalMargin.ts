import type { UniverseMap } from '../gateway/universe.client'
const parties = ['PAN', 'PRI', 'PVEM', 'MORENA']
export interface HistoricalMargin { status: string; first: string[]; second: string[]; firstVotes: number | null; secondVotes: number | null; votes: number | null; pp: number | null }
export function historicalMargin(row: UniverseMap['sections'][number]): HistoricalMargin {
  const empty = (status: string): HistoricalMargin => ({ status, first: [], second: [], firstVotes: null, secondVotes: null, votes: null, pp: null })
  if (!row.status.startsWith('HHI_')) return empty(row.status)
  if (row.total == null || row.total <= 0 || !row.votes || parties.some(p => row.votes![p] == null)) return empty('NO_DATA')
  const values = parties.map(p => ({ party: p, votes: row.votes![p]! })).sort((a,b)=>b.votes-a.votes)
  if (values.some(v=>!Number.isSafeInteger(v.votes)||v.votes<0)||values.reduce((n,v)=>n+v.votes,0)>row.total) throw new Error('Desglose histórico inválido.')
  if (values[0].votes === 0) return empty('NO_TRACKED_VOTES')
  const gap = values[0].votes-values[1].votes
  return { status: gap===0?'TIE':'AVAILABLE', first: values.filter(v=>v.votes===values[0].votes).map(v=>v.party), second: values.filter(v=>v.votes===values[1].votes).map(v=>v.party), firstVotes: values[0].votes, secondVotes: values[1].votes, votes: gap, pp: gap/row.total*100 }
}
export function marginLabel(row: UniverseMap['sections'][number]): string {
 const m=historicalMargin(row)
 return m.votes===null?`No calculable: ${m.status}`:`${m.first.join(' / ')}: ${m.firstVotes} votos · ${m.votes===0?'empate en máximo':`${m.second.join(' / ')}: ${m.secondVotes} votos`} · diferencia ${m.votes} votos (${m.pp!.toFixed(3)} pp)`
}
