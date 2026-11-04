import { describe, expect, it } from 'vitest'
import { distributionGap } from './distributionScenario'
import type { ComparisonRow } from './partyComparison'
const fixture=(estimated:Record<string,number>|null={PAN:60,PRI:20,PVEM:10,MORENA:0},total:number|null=100,residual:number|null=10):ComparisonRow=>({sectionId:'0001',status:'PAN',historical:{},estimated,difference:null,total,residual,leaders:[]})
describe('separación descriptiva entre máximos estimados',()=>{
 it('muestra diferencia de cifras sin ajustar un voto ni generar umbrales',()=>{
  const result=distributionGap(fixture())
  expect(result.first).toEqual(['PAN']);expect(result.second).toEqual(['PRI']);expect(result.votes).toBe(40);expect(result.pp).toBe(40)
  expect('additional' in result).toBe(false);expect('transfer' in result).toBe(false)
 })
 it('conserva todas las opciones empatadas y separación cero',()=>{
  const result=distributionGap(fixture({PAN:30,PRI:30,PVEM:10,MORENA:10},100,20))
  expect(result.status).toBe('TIE');expect(result.first).toEqual(['PAN','PRI']);expect(result.second).toEqual(['PAN','PRI']);expect(result.votes).toBe(0)
 })
 it('conserva empates en el segundo máximo sin escoger un contraste arbitrario',()=>{
  const result=distributionGap(fixture({PAN:50,PRI:20,PVEM:20,MORENA:0},100,10))
  expect(result.second).toEqual(['PRI','PVEM']);expect(result.votes).toBe(30)
 })
 it('distingue total cero, ausencia de votos rastreados y datos insuficientes',()=>{
  expect(distributionGap(fixture({PAN:0,PRI:0,PVEM:0,MORENA:0},0,0)).status).toBe('ZERO_PROJECTED')
  expect(distributionGap(fixture({PAN:0,PRI:0,PVEM:0,MORENA:0},100,100)).status).toBe('NO_TRACKED_VOTES')
  expect(distributionGap({...fixture(null,null,null),status:'NO_DATA'}).votes).toBeNull()
 })
 it('rechaza cifras imposibles y no usa un total incompatible',()=>{
  expect(distributionGap(fixture({PAN:60,PRI:20,PVEM:10,MORENA:0},90,10)).status).toBe('INCONSISTENT')
  expect(distributionGap(fixture({PAN:-1,PRI:20,PVEM:10,MORENA:0},100,71)).status).toBe('INCONSISTENT')
  expect(distributionGap(fixture({PAN:1,PRI:0,PVEM:0,MORENA:0},0,0)).status).toBe('INCONSISTENT')
 })
 it('usa el total de contienda con residuo, sin normalizar solo cuatro opciones',()=>{
  const result=distributionGap(fixture({PAN:30,PRI:10,PVEM:5,MORENA:0},100,55))
  expect(result.votes).toBe(20);expect(result.pp).toBe(20)
 })
})