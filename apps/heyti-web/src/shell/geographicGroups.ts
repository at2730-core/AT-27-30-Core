import type { TerritorialGeometry, GeoPosition } from '../gateway/territorial.geometry'
import type { UniverseMap } from '../gateway/universe.client'
export const GEOGRAPHIC_TOLERANCE = 1e-7
interface Bounds {minX:number;minY:number;maxX:number;maxY:number}
interface Edge extends Bounds {a:GeoPosition;b:GeoPosition}
interface GeometrySection {sectionId:string;geometry:TerritorialGeometry}
export interface GeographicSection {sectionId:string;neighbours:string[];groupId:string|null;evaluable:boolean}
export interface GeographicGroup {id:string;sections:string[];color:string}
export interface GeographicGroups {rows:Record<string,GeographicSection>;groups:GeographicGroup[];evaluated:number;boundaryPairs:number;tolerance:number}
export type GeographicMap = UniverseMap & { geographicGroups:GeographicGroups }
const ordered=(a:string,b:string)=>Number(a)-Number(b)||a.localeCompare(b)
function overlaps(a:Bounds,b:Bounds){const e=GEOGRAPHIC_TOLERANCE;return a.minX<=b.maxX+e&&b.minX<=a.maxX+e&&a.minY<=b.maxY+e&&b.minY<=a.maxY+e}
function edgesOf(geometry:TerritorialGeometry):Edge[]{
 const polygons=geometry.type==='Polygon'?[geometry.coordinates]:geometry.coordinates
 const edges:Edge[]=[]
 for(const polygon of polygons)for(const ring of polygon){
  if(ring.length<4)continue
  if(ring.some(p=>!Number.isFinite(p[0])||!Number.isFinite(p[1])||Math.abs(p[0])>180||Math.abs(p[1])>90))continue
  if(ring[0][0]!==ring[ring.length-1][0]||ring[0][1]!==ring[ring.length-1][1])continue
  for(let i=1;i<ring.length;i++){
   const a=ring[i-1],b=ring[i]
   if(Math.hypot(b[0]-a[0],b[1]-a[1])<=GEOGRAPHIC_TOLERANCE)continue
   edges.push({a,b,minX:Math.min(a[0],b[0]),minY:Math.min(a[1],b[1]),maxX:Math.max(a[0],b[0]),maxY:Math.max(a[1],b[1])})
  }
 }
 return edges.sort((a,b)=>a.minX-b.minX)
}
function sharedSegment(a:Edge,b:Edge){
 if(!overlaps(a,b))return false
 const dx=a.b[0]-a.a[0],dy=a.b[1]-a.a[1],length=Math.hypot(dx,dy),e=GEOGRAPHIC_TOLERANCE
 const distance=(p:GeoPosition)=>Math.abs(dx*(p[1]-a.a[1])-dy*(p[0]-a.a[0]))/length
 if(distance(b.a)>e||distance(b.b)>e)return false
 const project=(p:GeoPosition)=>((p[0]-a.a[0])*dx+(p[1]-a.a[1])*dy)/length
 const start=project(b.a),end=project(b.b)
 return Math.min(length,Math.max(start,end))-Math.max(0,Math.min(start,end))>e
}
function boundariesTouch(a:Edge[],b:Edge[]){
 for(const one of a)for(const two of b){
  if(two.minX>one.maxX+GEOGRAPHIC_TOLERANCE)break
  if(sharedSegment(one,two))return true
 }
 return false
}
function boundsOf(edges:Edge[]):Bounds{return edges.reduce((b,e)=>({minX:Math.min(b.minX,e.minX),minY:Math.min(b.minY,e.minY),maxX:Math.max(b.maxX,e.maxX),maxY:Math.max(b.maxY,e.maxY)}),{minX:Infinity,minY:Infinity,maxX:-Infinity,maxY:-Infinity})}
function* scanGroups(sections:readonly GeometrySection[]):Generator<number,GeographicGroups>{
 if(new Set(sections.map(s=>s.sectionId)).size!==sections.length)throw new Error('Identidades de sección duplicadas.')
 const prepared=sections.map(s=>{const edges=edgesOf(s.geometry);return {...s,edges,bounds:boundsOf(edges)}}).sort((a,b)=>a.bounds.minX-b.bounds.minX||ordered(a.sectionId,b.sectionId))
 const graph=new Map(prepared.map(s=>[s.sectionId,new Set<string>()]))
 let boundaryPairs=0
 for(let i=0;i<prepared.length;i++){
  const a=prepared[i]
  if(a.edges.length)for(let j=i+1;j<prepared.length;j++){
   const b=prepared[j]
   if(b.bounds.minX>a.bounds.maxX+GEOGRAPHIC_TOLERANCE)break
   if(b.edges.length&&overlaps(a.bounds,b.bounds)&&boundariesTouch(a.edges,b.edges)){graph.get(a.sectionId)!.add(b.sectionId);graph.get(b.sectionId)!.add(a.sectionId);boundaryPairs++}
  }
  if(i%32===0)yield (i+1)/Math.max(1,prepared.length)
 }
 const rows:Record<string,GeographicSection>={}
 for(const s of prepared)rows[s.sectionId]={sectionId:s.sectionId,neighbours:[...graph.get(s.sectionId)!].sort(ordered),groupId:null,evaluable:s.edges.length>0}
 const groups:GeographicGroup[]=[]
 for(const id of Object.keys(rows).sort(ordered)){
  if(rows[id].groupId!==null||!rows[id].evaluable)continue
  const groupId=`G-${id}`,members:string[]=[],queue=[id];rows[id].groupId=groupId
  for(let i=0;i<queue.length;i++){const current=queue[i];members.push(current);for(const next of rows[current].neighbours)if(rows[next].groupId===null){rows[next].groupId=groupId;queue.push(next)}}
  // Category color is based only on the stable group position, never on votes.
  groups.push({id:groupId,sections:members.sort(ordered),color:`hsl(${Math.round(groups.length*137.508)%360} 48% 46%)`})
 }
 return {rows,groups,evaluated:prepared.filter(s=>s.edges.length>0).length,boundaryPairs,tolerance:GEOGRAPHIC_TOLERANCE}
}
export function buildGeographicGroups(sections:readonly GeometrySection[]):GeographicGroups{const scan=scanGroups(sections);let step=scan.next();while(!step.done)step=scan.next();return step.value}
export async function buildGeographicGroupsAsync(sections:readonly GeometrySection[],signal:AbortSignal,onProgress?:(fraction:number)=>void):Promise<GeographicGroups>{
 if(signal.aborted)throw new DOMException('Consulta cancelada','AbortError')
 const scan=scanGroups(sections);let step=scan.next()
 while(!step.done){if(signal.aborted)throw new DOMException('Consulta cancelada','AbortError');onProgress?.(step.value);await new Promise(resolve=>setTimeout(resolve,0));step=scan.next()}
 if(signal.aborted)throw new DOMException('Consulta cancelada','AbortError');onProgress?.(1);return step.value
}
export function geographicGroupsOf(result:UniverseMap):GeographicGroups|null{return (result as Partial<GeographicMap>).geographicGroups??null}
export function geographicLabel(row:GeographicSection){return `${row.groupId??'Sin grupo calculable'} · ${row.neighbours.length} colindantes: ${row.neighbours.join(', ')||'ninguna dentro del universo consultado'}`}
export interface GeographicSum {sum:number|null;availableSum:number;covered:number;expected:number}
export function geographicSum(result:UniverseMap,ids:readonly string[],field:'nominal'|'total'|string,indexed:ReadonlyMap<string,UniverseMap['sections'][number]>=new Map(result.sections.map(s=>[s.sectionId,s]))):GeographicSum{
 let covered=0,availableSum=0
 for(const id of ids){const row=indexed.get(id);if(!row||row.status==='INCONSISTENT'||row.status==='NOT_CONTESTED')continue
 const value=field==='nominal'?result.results2024?.[id]?.nominal??row.nominal:field==='total'?row.total:row.votes?.[field]
 if(value!=null&&Number.isSafeInteger(value)&&value>=0){covered++;availableSum+=value}
 }
 return {sum:covered===ids.length?availableSum:null,availableSum,covered,expected:ids.length}
}