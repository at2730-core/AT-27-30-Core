import { describe, expect, it } from 'vitest'
import { comparePartyVotes } from './partyComparison'
import { buildParticipationScenario } from './participationScenario'
import type { UniverseMap } from '../gateway/universe.client'
function map(year:number, percent:number|null):UniverseMap {
 return {metric:'abstention',year,contest:'A',universe:{level:'state',id:'11',label:'Guanajuato',sections:1},provenance:{master:'same'},coverage:{geographic:1,represented:1,blocked:0},counts:{},sections:[{sectionId:'1',status:percent===null?'NO_DATA':'ABS_MID',leader:null,total:percent===null?null:percent*2,nominal:200,abstention:percent===null?null:100-percent,geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[0,1],[0,0]]]}}]}
}
function fixture() {
 const scenario=buildParticipationScenario([map(2018,30),map(2021,40),map(2024,50)])
 const source:UniverseMap={...map(2024,50),metric:'concentration',sections:[{...map(2024,50).sections[0],status:'HHI_MID',votes:{PAN:60,PRI:20,PVEM:10,MORENA:0}}]}
 return {scenario,source}
}
describe('comparación descriptiva',()=>{
 it('conserva proporciones, total y calcula diferencias sin umbrales',()=>{
  const {scenario,source}=fixture(),result=comparePartyVotes(scenario,source),row=result.rows['1']
  expect(row.total).toBe(120);expect(row.estimated).toEqual({PAN:72,PRI:24,PVEM:12,MORENA:0})
  expect(row.difference).toEqual({PAN:12,PRI:4,PVEM:2,MORENA:0});expect(row.residual).toBe(12)
  expect(Object.values(row.estimated!).reduce((n,v)=>n+v,0)+row.residual!).toBe(row.total)
  expect('additional' in row).toBe(false);expect('transfer' in row).toBe(false)
 })
 it('excluye incomparables de ambas sumas sin convertir faltantes a cero',()=>{
  const {scenario,source}=fixture();scenario.rows['1'].percent=null
  const result=comparePartyVotes(scenario,source)
  expect(result.valid).toBe(0);expect(result.rows['1'].estimated).toBeNull();expect(result.rows['1'].difference).toBeNull()
  expect(result.totals.PAN.historical).toBe(0)
 })
 it('rechaza totales y cortes que no corresponden',()=>{
  const {scenario,source}=fixture();source.sections[0].total=101
  expect(()=>comparePartyVotes(scenario,source)).toThrow()
  const other=fixture();other.source.provenance={master:'changed'}
  expect(()=>comparePartyVotes(other.scenario,other.source)).toThrow()
 })
})
