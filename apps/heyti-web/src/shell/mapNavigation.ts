export interface MapView { zoom: number; x: number; y: number }
export interface MapPoint { x: number; y: number }
export function limitView(view: MapView): MapView {
  return { zoom: Math.max(1,Math.min(8,view.zoom)), x: Math.max(-3200,Math.min(3200,view.x)), y: Math.max(-2000,Math.min(2000,view.y)) }
}
export function zoomAt(view: MapView, point: MapPoint, factor: number): MapView {
  const zoom = Math.max(1,Math.min(8,view.zoom*factor)), ratio=zoom/view.zoom
  return limitView({zoom,x:point.x-400-(point.x-400-view.x)*ratio,y:point.y-250-(point.y-250-view.y)*ratio})
}
export function zoomBox(view: MapView, start: MapPoint, end: MapPoint): MapView {
  const width=Math.abs(end.x-start.x),height=Math.abs(end.y-start.y)
  if(width<6||height<6)return view
  const zoom=Math.max(1,Math.min(8,view.zoom*Math.min(800/width,500/height))),ratio=zoom/view.zoom
  return limitView({zoom,x:-( (start.x+end.x)/2-400-view.x)*ratio,y:-((start.y+end.y)/2-250-view.y)*ratio})
}
// SVG preserveAspectRatio=xMidYMid meet: descontar las bandas laterales/superiores.
export function clientToMap(client: MapPoint, bounds: {left:number;top:number;width:number;height:number}): MapPoint | null {
  if(bounds.width<=0||bounds.height<=0)return null
  const scale=Math.min(bounds.width/800,bounds.height/500)
  return {x:(client.x-bounds.left-(bounds.width-800*scale)/2)/scale,y:(client.y-bounds.top-(bounds.height-500*scale)/2)/scale}
}
