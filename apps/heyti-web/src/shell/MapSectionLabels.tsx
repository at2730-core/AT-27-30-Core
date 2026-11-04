import { useWorkspace } from '../platform/useWorkspace'
import type { GeoMultiPolygonCoordinates, GeoPosition } from '../gateway/territorial.geometry'
export interface SectionLabel { id:string; x:number; y:number }
function inside(p:GeoPosition,ring:GeoPosition[]):boolean {
 let yes=false
 for(let i=0,j=ring.length-1;i<ring.length;j=i++) {const a=ring[i],b=ring[j];if((a[1]>p[1])!==(b[1]>p[1])&&p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0])yes=!yes}
 return yes
}
// Punto interior de la mayor componente; no colocar etiquetas en huecos.
export function labelPoint(polygons:GeoMultiPolygonCoordinates,project:(p:GeoPosition)=>GeoPosition):GeoPosition|null {
 const projected=polygons.map(poly=>poly.map(r=>r.map(project)))
 const area=(ring:GeoPosition[])=>Math.abs(ring.reduce((sum,a,i)=>{const b=ring[(i+1)%ring.length];return sum+a[0]*b[1]-b[0]*a[1]},0)/2)
 const poly=projected.sort((a,b)=>area(b[0])-area(a[0]))[0];if(!poly?.[0]?.length)return null
 const ring=poly[0],xs=ring.map(p=>p[0]),ys=ring.map(p=>p[1]),minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys)
 const contains=(p:GeoPosition)=>inside(p,ring)&&!poly.slice(1).some(hole=>inside(p,hole))
 const center:GeoPosition=[(minX+maxX)/2,(minY+maxY)/2];if(contains(center))return center
 for(let n=8;n<=32;n*=2)for(let j=1;j<n;j++)for(let i=1;i<n;i++){const p:GeoPosition=[minX+(maxX-minX)*i/n,minY+(maxY-minY)*j/n];if(contains(p))return p}
 return null
}
export function MapSectionLabels({labels,selected}:{labels:SectionLabel[];selected?:string|null}) {
 const {state}=useWorkspace();const v=state.mapView??{zoom:1,x:0,y:0}
 const visible:{id:string;x:number;y:number;width:number}[]=[]
 // Priorizar la seleccion; luego orden seccional, nunca votos o partido.
 for(const label of [...labels].sort((a,b)=>(a.id===selected?-1:b.id===selected?1:Number(a.id)-Number(b.id)))) {
  const x=400+v.x+v.zoom*(label.x-400),y=250+v.y+v.zoom*(label.y-250),width=label.id.length*7+14
  if(x<width/2||x>800-width/2||y<12||y>488)continue
  if(visible.some(p=>Math.abs(p.x-x)<(p.width+width)/2+4&&Math.abs(p.y-y)<26))continue
  visible.push({id:label.id,x,y,width})
 }
 return <g pointerEvents="none" aria-hidden="true">{visible.map(p=><g key={p.id} transform={`translate(${p.x} ${p.y})`}><rect x={-p.width/2} y={-10} width={p.width} height={20} rx={4} fill="#ffffff" fillOpacity={.96} stroke="#334155" strokeWidth={.8}/><text x={0} y={0} textAnchor="middle" dominantBaseline="central" fill="#111827" fontFamily="Arial, sans-serif" fontSize={12} fontWeight={700}>{p.id}</text></g>)}</g>
}
