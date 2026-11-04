import type { ComparisonRow } from './partyComparison'
import { COMPARISON_PARTIES } from './partyComparison'
export interface DistributionGap { status:string; first:string[]; second:string[]; firstVotes:number|null; secondVotes:number|null; votes:number|null; pp:number|null }
export function distributionGap(row:ComparisonRow):DistributionGap {
 const empty=(status:string):DistributionGap=>({status,first:[],second:[],firstVotes:null,secondVotes:null,votes:null,pp:null})
 if(!row.estimated||row.total===null)return empty(row.status)
 if(!Number.isSafeInteger(row.total)||row.total<0)return empty('INCONSISTENT')
 const values=COMPARISON_PARTIES.map(p=>({party:p,votes:row.estimated![p]})).sort((a,b)=>b.votes-a.votes)
 if(values.some(v=>!Number.isSafeInteger(v.votes)||v.votes<0)||row.residual===null||!Number.isSafeInteger(row.residual)||row.residual<0||values.reduce((n,v)=>n+v.votes,0)+row.residual!==row.total)return empty('INCONSISTENT')
 if(row.total===0)return empty('ZERO_PROJECTED')
 if(values[0].votes===0)return empty('NO_TRACKED_VOTES')
 const firstVotes=values[0].votes,secondVotes=values[1].votes,votes=firstVotes-secondVotes
 return {status:votes===0?'TIE':'AVAILABLE',first:values.filter(v=>v.votes===firstVotes).map(v=>v.party),second:values.filter(v=>v.votes===secondVotes).map(v=>v.party),firstVotes,secondVotes,votes,pp:votes/row.total*100}
}