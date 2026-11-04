import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { compound, parseAnnualRate, projectionRows } from './socioProjection'
import { parseSocioReference } from './socioTraceability'
import type { UniverseMap } from '../gateway/universe.client'
const reference=parseSocioReference(JSON.parse(readFileSync(new URL('../../public/data/heyti-socioeconomico-referencia-2020.json',import.meta.url),'utf8')))
const id=Object.keys(reference.sections)[0]
function map(year:number,nominal:number|null):UniverseMap {
 return {year,metric:'abstention',contest:'A',universe:{id:'11',level:'state',label:'Guanajuato de prueba',sections:1},counts:{ABS_LOW:1},coverage:{geographic:1,represented:1,blocked:0},provenance:{cut:'same'},sections:[{sectionId:id,nominal,status:'ABS_LOW',leader:null,total:50,geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[1,1],[0,0]]]}}]}
}
const history=()=>[map(2018,100),map(2021,130),map(2024,200)]
describe('Escenarios socioeconómicos 2027',()=>{
 it('requiere tasa explícita, admite coma, cero y decrecimiento sin convertir vacíos en cero',()=>{
  expect(parseAnnualRate('0')).toBe(0);expect(parseAnnualRate('1,5')).toBe(.015);expect(parseAnnualRate(' -2 ')).toBe(-.02)
  for(const value of ['', ' ', 'NaN', '1e2','1.2.3','-100','101','Infinity'])expect(()=>parseAnnualRate(value)).toThrow()
 })
 it('distingue base cero de faltante, conserva precisión y rechaza desbordamiento',()=>{
  expect(compound(0,.02,7)).toBe(0);expect(compound(null,.02,7)).toBeNull();expect(compound(100,null,3)).toBeNull()
  expect(compound(100,.01,3)).toBeCloseTo(103.0301,8)
  expect(compound(100,-.1,3)).toBeCloseTo(72.9)
  expect(compound(Number.MAX_SAFE_INTEGER,1,7)).toBeNull()
 })
 it('conserva CAGR V1 con 6 años de historial y 3 de extrapolación; 2021 es contexto',()=>{
  const maps=history(),r=projectionRows(maps,reference,'ln-history',null)[0]
  expect(r.rate).toBeCloseTo(2**(1/6)-1);expect(r.projected).toBeCloseTo(200*Math.sqrt(2));expect(r.history).toEqual([100,130,200]);expect(r.years).toBe(3)
  maps[1].sections[0].nominal=9999
  expect(projectionRows(maps,reference,'ln-history',null)[0].projected).toBe(r.projected)
 })
 it('no usa tasa de respaldo ni calcula CAGR con base cero, faltantes o registro inconsistente',()=>{
  for(const value of [null,0]){const maps=history();maps[0].sections[0].nominal=value;expect(projectionRows(maps,reference,'ln-history',.02)[0].projected).toBeNull()}
  const maps=history();maps[2].sections[0].status='INCONSISTENT';expect(projectionRows(maps,reference,'ln-history',null)[0].projected).toBeNull()
 })
 it('usa 2020 durante 7 años para adultos, sin inventar bases 2018/2024 ni cambiar la fuente',()=>{
  const m=map(2024,null);m.metric='leaders';const before=JSON.stringify(reference)
  const r=projectionRows([m],reference,'adult-rate',.01)[0]
  expect(r.base).toBe(reference.sections[id].values.POB_18MAS);expect(r.projected).toBeCloseTo(r.base!*1.01**7);expect(r.years).toBe(7);expect(r.history).toEqual([null,null,null]);expect(JSON.stringify(reference)).toBe(before)
  m.sections[0].sectionId=Object.keys(reference.relations)[0]
  expect(projectionRows([m],reference,'adult-rate',.01)[0].projected).toBeNull()
 })
 it('admite escenario LN con tasa propia y base cero sin exigir serie histórica',()=>{
  const r=projectionRows([map(2024,200)],reference,'ln-rate',-.01)[0];expect(r.projected).toBeCloseTo(200*.99**3)
  expect(projectionRows([map(2024,0)],reference,'ln-rate',0)[0].projected).toBe(0)
  expect(()=>projectionRows([map(2024,200)],reference,'ln-rate',null)).toThrow()
 })
 it('rechaza mezclas de universo, corte, años y métrica y excluye geometrías distintas',()=>{
  for(const change of [(m:UniverseMap)=>{m.universe={...m.universe,id:'12'}},(m:UniverseMap)=>{m.provenance={cut:'other'}},(m:UniverseMap)=>{m.year=2024},(m:UniverseMap)=>{m.metric='leaders'}]){const maps=history();change(maps[0]);expect(()=>projectionRows(maps,reference,'ln-history',null)).toThrow()}
  const maps=history();maps[0].sections[0].geometry.coordinates[0][0]=[.1,0]
  expect(projectionRows(maps,reference,'ln-history',null)[0].reason).toMatch(/Geometrías distintas/)
  expect(projectionRows(maps,reference,'ln-history',null)[0].projected).toBeNull()
 })
 it('conserva las filas 2024 aunque no haya historial propio, sin herencia por origen',()=>{
  const maps=history();maps[0].sections=[]
  const r=projectionRows(maps,reference,'ln-history',null)[0];expect(r.base).toBe(200);expect(r.projected).toBeNull();expect(r.history[0]).toBeNull()
 })
})
