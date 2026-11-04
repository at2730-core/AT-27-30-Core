import { describe, it, expect } from 'vitest'
import { parseSocio, socioCuts, socioBand } from './socioeconomic'
describe('Socioeconómico sin valores inventados',()=>{
 it('conserva cero y diferencia faltante; convierte cifras textuales',()=>{const d=parseSocio({'1':{POB_TOTAL:'0',ESCOLARIDAD_PROM:'9.12'},'2':{POB_TOTAL:null}});expect(d['1'].POB_TOTAL).toBe(0);expect(d['1'].ESCOLARIDAD_PROM).toBe(9.12);expect(d['2'].POB_TOTAL).toBeNull();expect(d['1'].POB_18MAS).toBeNull()})
 it('rechaza identidades, tipos, negativos y conteos fraccionarios',()=>{for(const raw of [{'0':{}},{'1':{POB_TOTAL:true}},{'1':{POB_TOTAL:'-1'}},{'1':{POB_TOTAL:'1.5'}},{}])expect(()=>parseSocio(raw)).toThrow()})
 it('los faltantes no cambian cuantiles ni se clasifican como cero',()=>{expect(socioCuts([0,10,20,null],3)).toEqual([0,10]);expect(socioBand(null,[0,10])).toBeNull();expect(socioBand(0,[0,10])).toBe(0);expect(socioBand(11,[0,10])).toBe(2)})
 it('mantiene empates juntos incluso si deja grupos vacíos',()=>{const cuts=socioCuts([7,7,7,7],5);expect(cuts).toEqual([7,7,7,7]);expect(socioBand(7,cuts)).toBe(0);expect(socioCuts([null],5)).toEqual([])})
})
