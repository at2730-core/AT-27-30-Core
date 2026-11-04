import {describe,it,expect} from 'vitest'
import {visibleSectionLabels} from './leafletLabelVisibility'
import type {LabelCandidate} from './leafletLabelVisibility'
const labels:LabelCandidate[]=[{id:'1466',x:100,y:100},{id:'1467',x:105,y:103},{id:'1501',x:300,y:100}]
describe('Etiquetas de sección en Leaflet',()=>{
 it('separa etiquetas cercanas y mantiene las alejadas',()=>{
  expect([...visibleSectionLabels(labels,null,'auto',800,500,11)]).toEqual(['1466','1501'])
 })
 it('prioriza siempre la sección seleccionada sobre su vecina',()=>{
  expect([...visibleSectionLabels(labels,'1467','auto',800,500,11)]).toEqual(['1467','1501'])
 })
 it('Todas permite ver también las claves superpuestas',()=>{
  expect(visibleSectionLabels(labels,null,'all',800,500,8).size).toBe(3)
 })
 it('Ocultas conserva únicamente la seleccionada',()=>{
  expect([...visibleSectionLabels(labels,'1467','hidden',800,500,12)]).toEqual(['1467'])
  expect(visibleSectionLabels(labels,null,'hidden',800,500,12).size).toBe(0)
 })
 it('filtra puntos fuera del encuadre y coordenadas inválidas',()=>{
  const points=[...labels,{id:'2',x:-20,y:100},{id:'3',x:820,y:100},{id:'4',x:20,y:NaN}]
  expect([...visibleSectionLabels(points,null,'all',800,500,11)]).toEqual(labels.map(p=>p.id))
 })
 it('al acercar permite más etiquetas sin limitar la sección seleccionada',()=>{
  const many=Array.from({length:200},(_,i)=>({id:String(i+1),x:20+(i%20)*100,y:20+Math.floor(i/20)*100}))
  expect(visibleSectionLabels(many,'200','auto',2500,1500,8).size).toBe(30)
  expect(visibleSectionLabels(many,'200','auto',2500,1500,11).size).toBe(80)
  const close=visibleSectionLabels(many,'200','auto',2500,1500,14)
  expect(close.size).toBe(180);expect(close.has('200')).toBe(true)
 })
 it('el orden de llegada no cambia la selección automática ni altera la fuente',()=>{
  const before=JSON.stringify(labels)
  expect([...visibleSectionLabels([...labels].reverse(),null,'auto',800,500,11)]).toEqual([...visibleSectionLabels(labels,null,'auto',800,500,11)])
  expect(JSON.stringify(labels)).toBe(before)
 })
 it('distingue el criterio por zoom del modo Todas',()=>{
  const many=Array.from({length:45},(_,i)=>({id:String(i+1),x:20+i*80,y:20}))
  expect(visibleSectionLabels(many,null,'all',4000,100,8).size).toBe(45)
  expect(visibleSectionLabels(many,null,'auto',4000,100,8).size).toBe(30)
 })
})
