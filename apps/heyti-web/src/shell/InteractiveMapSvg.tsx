import { useEffect, useRef, useState } from 'react'
import type { PointerEvent as ReactPointerEvent, SVGProps } from 'react'
import { useWorkspace } from '../platform/useWorkspace'
import { clientToMap, limitView, zoomAt, zoomBox } from './mapNavigation'
import type { MapPoint, MapView } from './mapNavigation'
import './MapMouse.css'
interface Gesture { id:number; start:MapPoint; last:MapPoint; client:MapPoint; view:MapView; box:boolean; moved:boolean }
export function InteractiveMapSvg({children,style,...props}: SVGProps<SVGSVGElement>) {
  const {state,setMapView}=useWorkspace()
  const view=state.mapView??{zoom:1,x:0,y:0}
  const current=useRef(view);current.current=view
  const update=useRef(setMapView);update.current=setMapView
  const svg=useRef<SVGSVGElement|null>(null), gesture=useRef<Gesture|null>(null), suppressClick=useRef(false)
  const [box,setBox]=useState<{start:MapPoint;end:MapPoint}|null>(null),[dragging,setDragging]=useState(false)
  const point=(x:number,y:number)=>svg.current ? clientToMap({x,y},svg.current.getBoundingClientRect()) : null
  useEffect(()=>{
    const node=svg.current;if(!node)return
    const wheel=(event:WheelEvent)=>{
      if(event.ctrlKey||event.metaKey||gesture.current)return
      const p=clientToMap({x:event.clientX,y:event.clientY},node.getBoundingClientRect());if(!p)return
      event.preventDefault()
      const delta=event.deltaY*(event.deltaMode===1?16:event.deltaMode===2?500:1)
      const next=zoomAt(current.current,p,Math.exp(-Math.max(-150,Math.min(150,delta))*.002))
      current.current=next;update.current(next)
    }
    node.addEventListener('wheel',wheel,{passive:false})
    return ()=>node.removeEventListener('wheel',wheel)
  },[])
  function down(event:ReactPointerEvent<SVGSVGElement>){
    if(event.button!==0||event.isPrimary===false)return
    const p=point(event.clientX,event.clientY);if(!p)return
    suppressClick.current=false
    gesture.current={id:event.pointerId,start:p,last:p,client:{x:event.clientX,y:event.clientY},view:current.current,box:event.shiftKey,moved:false}
    event.currentTarget.focus({preventScroll:true})
  }
  function move(event:ReactPointerEvent<SVGSVGElement>){
    const g=gesture.current;if(!g||g.id!==event.pointerId)return
    const p=point(event.clientX,event.clientY);if(!p)return
    if(!g.moved&&Math.hypot(event.clientX-g.client.x,event.clientY-g.client.y)<4)return
    if(!g.moved){g.moved=true;event.currentTarget.setPointerCapture?.(event.pointerId);suppressClick.current=true;setDragging(true)}
    event.preventDefault();g.last=p
    if(g.box)setBox({start:g.start,end:p})
    else {const next=limitView({...g.view,x:g.view.x+p.x-g.start.x,y:g.view.y+p.y-g.start.y});current.current=next;setMapView(next)}
  }
  function end(event:ReactPointerEvent<SVGSVGElement>,cancel=false){
    const g=gesture.current;if(!g||g.id!==event.pointerId)return
    if(g.moved){
      event.preventDefault();suppressClick.current=true
      const next=cancel?g.view:g.box?zoomBox(g.view,g.start,point(event.clientX,event.clientY)??g.last):current.current
      current.current=next;setMapView(next)
    }
    gesture.current=null;setDragging(false);setBox(null)
    if(event.currentTarget.hasPointerCapture?.(event.pointerId))event.currentTarget.releasePointerCapture(event.pointerId)
  }
  return <svg {...props} ref={svg} tabIndex={0} preserveAspectRatio="xMidYMid meet" data-map-dragging={dragging} className={`heyti-interactive-map ${props.className??''}`} style={{...style,touchAction:'none',userSelect:'none'}}
    onPointerDown={down} onPointerMove={move} onPointerUp={e=>end(e)} onPointerCancel={e=>end(e,true)}
    onClickCapture={e=>{if(suppressClick.current){e.preventDefault();e.stopPropagation();suppressClick.current=false}}}
    onDoubleClick={e=>{const p=point(e.clientX,e.clientY);if(p){e.preventDefault();const next=zoomAt(current.current,p,1.5);current.current=next;setMapView(next)}}}
    onKeyDown={e=>{if(e.key==='Escape'&&gesture.current){const g=gesture.current;gesture.current=null;suppressClick.current=g.moved;current.current=g.view;setMapView(g.view);setBox(null);setDragging(false);if(svg.current?.hasPointerCapture?.(g.id))svg.current.releasePointerCapture(g.id)}}}>
    {children}
    {box?<rect x={Math.min(box.start.x,box.end.x)} y={Math.min(box.start.y,box.end.y)} width={Math.abs(box.end.x-box.start.x)} height={Math.abs(box.end.y-box.start.y)} fill="#3452d5" fillOpacity={.15} stroke="#3452d5" strokeWidth={1.5} strokeDasharray="6 3" vectorEffect="non-scaling-stroke" pointerEvents="none"/>:null}
  </svg>
}
