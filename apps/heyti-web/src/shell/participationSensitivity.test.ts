import { describe, expect, it } from 'vitest'
import type { UniverseMap } from '../gateway/universe.client'
import { buildParticipationSensitivity, sensitivityStyle } from './participationSensitivity'
export function sensitivityFixture(percent=60):UniverseMap[]{
  const map=(year:number):UniverseMap=>({year,metric:'abstention',contest:'A',universe:{level:'federal-district',id:'1',label:'Distrito de prueba',sections:1},provenance:{source:'fixture'},coverage:{geographic:1,represented:1,blocked:0},counts:{},sections:[{sectionId:'0001',status:'ABS_MID',leader:null,total:percent*10,nominal:1000,abstention:100-percent,geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[0,1],[0,0]]]}}]})
  const historical=map(2024),total=historical.sections[0].total!
  const source:UniverseMap={...historical,metric:'concentration',sections:[{...historical.sections[0],status:total===0?'ZERO_TOTAL':'HHI_MID',votes:{PAN:Math.floor(total*.5),PRI:Math.floor(total*.2),PVEM:Math.floor(total*.1),MORENA:Math.floor(total*.1)}}]}
  return [map(2018),map(2021),historical,source]
}
describe('sensibilidad descriptiva de participación',()=>{
  it('aplica puntos porcentuales y conserva el escenario base sin mutarlo',()=>{
    const maps=sensitivityFixture(),snapshot=JSON.stringify(maps),scenario=buildParticipationSensitivity(maps,2),row=scenario.sensitivity!.rows['0001']
    expect(row.basePercent).toBeCloseTo(60);expect(row.modifiedPercent).toBeCloseTo(62);expect(row.appliedPP).toBeCloseTo(2)
    expect(row.baseTotal).toBe(600);expect(row.modifiedTotal).toBe(620);expect(row.difference).toBe(20)
    expect(JSON.stringify(maps)).toBe(snapshot);expect(scenario.rows['0001'].percent).toBeCloseTo(60)
  })
  it('delta cero conserva todos los valores estimados por opción y el residuo',()=>{
    const row=buildParticipationSensitivity(sensitivityFixture(),0).sensitivity!.rows['0001']
    expect(row.difference).toBe(0);expect(row.before.estimated).toEqual(row.after.estimated);expect(row.before.residual).toBe(row.after.residual)
    expect(sensitivityStyle(row).fillColor).toBe('#94a3b8')
  })
  it('marca el límite superior y la variación realmente aplicada',()=>{
    const result=buildParticipationSensitivity(sensitivityFixture(98),8).sensitivity!,row=result.rows['0001']
    expect(row.rawModified).toBeCloseTo(106);expect(row.modifiedPercent).toBe(100);expect(row.appliedPP).toBeCloseTo(2);expect(row.limited).toBe(true)
    expect(row.modifiedTotal).toBe(1000);expect(result.limited).toBe(1)
  })
  it('conserva cero en el límite inferior y reparte ceros si existen proporciones válidas',()=>{
    const row=buildParticipationSensitivity(sensitivityFixture(2),-8).sensitivity!.rows['0001']
    expect(row.modifiedPercent).toBe(0);expect(row.modifiedTotal).toBe(0);expect(row.limited).toBe(true)
    expect(Object.values(row.after.estimated!)).toEqual([0,0,0,0]);expect(row.after.residual).toBe(0)
  })
  it('reconcilia total y residuo en ambos escenarios sin campos de intervención',()=>{
    const row=buildParticipationSensitivity(sensitivityFixture(),2).sensitivity!.rows['0001']
    for(const value of [row.before,row.after])expect(Object.values(value.estimated!).reduce((n,v)=>n+v,0)+value.residual!).toBe(value.total)
    expect('additional' in row).toBe(false);expect('transfer' in row).toBe(false);expect('winner' in row).toBe(false)
  })
  it('no pierde el volumen cuando falta desglose por opción',()=>{
    const maps=sensitivityFixture();maps[3].sections[0].status='NO_DATA';maps[3].sections[0].votes!.PAN=null
    const row=buildParticipationSensitivity(maps,2).sensitivity!.rows['0001']
    expect(row.modifiedTotal).toBe(620);expect(row.before.estimated).toBeNull();expect(row.after.estimated).toBeNull()
  })
  it('conserva filas sin históricos suficientes y sus estimaciones nulas',()=>{
    const maps=sensitivityFixture()
    for(const map of maps){map.sections.push({...map.sections[0],sectionId:'0002',status:'NO_DATA',total:null,abstention:null,votes:{PAN:null,PRI:null,PVEM:null,MORENA:null}});map.universe={...map.universe,sections:2};map.coverage={geographic:2,represented:2,blocked:0}}
    const value=buildParticipationSensitivity(maps,2).sensitivity!
    expect(Object.keys(value.rows)).toEqual(['0001','0002']);expect(value.valid).toBe(1);expect(value.rows['0002'].modifiedTotal).toBeNull()
  })
  it('no inventa proporciones con total histórico cero',()=>{
    const row=buildParticipationSensitivity(sensitivityFixture(0),2).sensitivity!.rows['0001']
    expect(row.baseTotal).toBe(0);expect(row.modifiedTotal).toBe(20);expect(row.after.estimated).toBeNull()
  })
  it('rechaza variaciones no válidas y cambios de procedencia',()=>{
    for(const delta of [-8.5,8.5,NaN,Infinity,.1])expect(()=>buildParticipationSensitivity(sensitivityFixture(),delta)).toThrow()
    const maps=sensitivityFixture();maps[3].provenance={source:'different'}
    expect(()=>buildParticipationSensitivity(maps,2)).toThrow()
  })
})