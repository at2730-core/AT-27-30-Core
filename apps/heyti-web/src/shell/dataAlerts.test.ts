import {describe,expect,it} from 'vitest'
import {dataAlertCounts,dataAlertDetail,dataAlertStatus} from './dataAlerts'
import type {UniverseMap,UniverseSection} from '../gateway/universe.client'
function row(status:UniverseSection['status'],votes:Record<string,number|null>,reason?:string):UniverseSection{return {sectionId:'1',status,leader:null,total:100,votes,missingReason:reason,geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[0,1],[0,0]]]}}}
describe('alertas de datos',()=>{
 it('distingue desglose cero de faltantes y total cero',()=>{
 const zero=row('HHI_LOW',{PAN:0,PRI:0,PVEM:0,MORENA:0})
 expect(dataAlertStatus(zero)).toBe('TRACKED_ZERO')
 expect(dataAlertStatus({...zero,status:'ZERO_TOTAL',total:0})).toBe('ZERO_TOTAL')
 const missing=row('NO_DATA',{PAN:null,PRI:0,PVEM:0,MORENA:0},'TRACKED_BREAKDOWN_MISSING')
 expect(dataAlertDetail(missing)).toBe('Desglose por partido faltante')
 })
 it('recuenta categorías sin convertir disponibles en certificados',()=>{
 const result={sections:[row('HHI_MID',{PAN:60,PRI:10,PVEM:10,MORENA:10}),row('NO_DATA',{PAN:null,PRI:null,PVEM:null,MORENA:null}),row('INCONSISTENT',{PAN:200,PRI:0,PVEM:0,MORENA:0})]} as UniverseMap
 expect(dataAlertCounts(result)).toEqual({AVAILABLE:1,NO_DATA:1,INCONSISTENT:1})
 })
})
