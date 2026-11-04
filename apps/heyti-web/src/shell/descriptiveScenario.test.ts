import { describe, expect, it } from 'vitest'
import { buildDescriptiveScenario } from './descriptiveScenario'
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
describe('escenario descriptivo consolidado', () => {
  it('conserva LN histórica, totales y cobertura sin producir umbrales partidistas', () => {
    const { source } = fixture()
    const result = buildDescriptiveScenario([map(2018,30), map(2021,40), map(2024,50), source])
    expect(result.rows['1'].nominal).toBe(200)
    expect(result.comparison.rows['1'].total).toBe(120)
    expect(Object.values(result.comparison.rows['1'].estimated!).reduce((n,v)=>n+v,0) + result.comparison.rows['1'].residual!).toBe(120)
    expect('win' in result).toBe(false)
    expect('party' in result).toBe(false)
    expect('additional' in result.comparison.rows['1']).toBe(false)
    expect('transfer' in result.comparison.rows['1']).toBe(false)
  })
  it('rechaza conjuntos incompletos y procedencias incompatibles', () => {
    expect(() => buildDescriptiveScenario([map(2018,30), map(2021,40), map(2024,50)])).toThrow()
    const { source } = fixture()
    source.provenance = { master: 'different' }
    expect(() => buildDescriptiveScenario([map(2018,30), map(2021,40), map(2024,50), source])).toThrow()
  })
  it('conserva filas no calculables sin reemplazar sus estimaciones por cero', () => {
    const { source } = fixture()
    const result = buildDescriptiveScenario([map(2018,null), map(2021,null), map(2024,50), source])
    expect(result.comparison.valid).toBe(0)
    expect(result.comparison.rows['1'].estimated).toBeNull()
    expect(result.comparison.rows['1'].difference).toBeNull()
  })
})