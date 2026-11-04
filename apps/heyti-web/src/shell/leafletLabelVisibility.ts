export type SectionLabelMode = 'auto' | 'all' | 'hidden'
export interface LabelCandidate { id:string; x:number; y:number }

// Screen-space separation; selection first, then numeric identity. No votes,
// category, population or political data participate in label placement.
export function visibleSectionLabels(candidates:LabelCandidate[], selected:string|null|undefined, mode:SectionLabelMode, width:number, height:number, zoom:number):Set<string> {
  const inside=candidates.filter(p=>Number.isFinite(p.x)&&Number.isFinite(p.y)&&p.x>=0&&p.x<=width&&p.y>=0&&p.y<=height)
  if(mode==='all')return new Set(inside.map(p=>p.id))
  const ordered=[...inside].sort((a,b)=>a.id===selected?-1:b.id===selected?1:Number(a.id)-Number(b.id)||a.id.localeCompare(b.id))
  const kept:LabelCandidate[]=[]
  const limit=zoom<10?30:zoom<12?80:180
  for(const p of ordered){
    if(p.id===selected){kept.push(p);continue}
    if(mode==='hidden'||kept.length>=limit)continue
    const labelWidth=p.id.length*7+14
    if(kept.some(q=>Math.abs(q.x-p.x)<(labelWidth+q.id.length*7+14)/2+8&&Math.abs(q.y-p.y)<30))continue
    kept.push(p)
  }
  return new Set(kept.map(p=>p.id))
}
