import {describe,it,expect} from 'vitest'
import {labelPoint} from './MapSectionLabels'
import type {GeoMultiPolygonCoordinates} from '../gateway/territorial.geometry'
const identity=(p:[number,number])=>p
const square:GeoMultiPolygonCoordinates=[[[[0,0],[10,0],[10,10],[0,10],[0,0]]]]
describe('Etiquetas interiores',()=>{
 it('coloca etiqueta en centro interior',()=>expect(labelPoint(square,identity)).toEqual([5,5]))
 it('evita hueco central',()=>{const p=labelPoint([[square[0][0],[[4,4],[6,4],[6,6],[4,6],[4,4]]]],identity)!;expect(p).not.toBeNull();expect(p[0]<4||p[0]>6||p[1]<4||p[1]>6).toBe(true)})
 it('elige componente mayor y conserva vacio sin inventar coordenadas',()=>{const small:GeoMultiPolygonCoordinates=[[[[20,20],[21,20],[21,21],[20,21],[20,20]]],square[0]];expect(labelPoint(small,identity)).toEqual([5,5]);expect(labelPoint([],identity)).toBeNull()})
})
