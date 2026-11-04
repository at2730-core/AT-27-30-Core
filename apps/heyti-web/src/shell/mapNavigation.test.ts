import { describe,it,expect } from 'vitest'
import { clientToMap, zoomAt, zoomBox, limitView } from './mapNavigation'
describe('Navegación SVG',()=>{
 it('zoom mantiene fijo el punto bajo el cursor',()=>{const v={zoom:2,x:30,y:-20},p={x:100,y:150};const n=zoomAt(v,p,1.5);const world={x:400+(p.x-400-v.x)/v.zoom,y:250+(p.y-250-v.y)/v.zoom};expect(400+n.x+n.zoom*(world.x-400)).toBeCloseTo(p.x);expect(250+n.y+n.zoom*(world.y-250)).toBeCloseTo(p.y)})
 it('límites no provocan saltos al seguir usando la rueda',()=>{const v={zoom:8,x:0,y:0};expect(zoomAt(v,{x:50,y:30},2)).toEqual(v);expect(limitView({zoom:20,x:9000,y:-9000})).toEqual({zoom:8,x:3200,y:-2000})})
 it('descuenta bandas por relación de aspecto y adapta escala',()=>{expect(clientToMap({x:300,y:100},{left:100,top:100,width:1200,height:500})).toEqual({x:0,y:0});expect(clientToMap({x:500,y:350},{left:100,top:100,width:800,height:500})).toEqual({x:400,y:250});expect(clientToMap({x:0,y:0},{left:0,top:0,width:0,height:0})).toBeNull()})
 it('recuadro centra zona, funciona en ambas direcciones y conserva mínimo',()=>{const v={zoom:1,x:0,y:0};expect(zoomBox(v,{x:0,y:0},{x:400,y:250})).toEqual({zoom:2,x:400,y:250});expect(zoomBox(v,{x:400,y:250},{x:0,y:0})).toEqual({zoom:2,x:400,y:250});expect(zoomBox(v,{x:5,y:5},{x:7,y:7})).toBe(v)})
})
