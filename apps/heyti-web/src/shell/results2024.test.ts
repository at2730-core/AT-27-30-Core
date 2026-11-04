import {describe,it,expect} from 'vitest'
import type {UniverseMap} from '../gateway/universe.client'
import {attachResults2024,orderSections2024} from './results2024'
const base = ():UniverseMap=>({metric:'concentration',universe:{id:'6',level:'federal-district',label:'Distrito federal 6',sections:1},year:2024,contest:'A',sections:[{sectionId:'1297',geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[1,1],[0,0]]]},status:'ZERO_TOTAL',leader:null,total:0,votes:{PAN:0,PRI:null,PVEM:0,MORENA:0}}],counts:{ZERO_TOTAL:1},coverage:{geographic:1,represented:1,blocked:0},provenance:{source:'a',geometry:'b'}})
const nominal=():UniverseMap=>{const m=base();return {...m,metric:'abstention',sections:m.sections.map(s=>({...s,status:'ABS_VERY_HIGH',nominal:100,abstention:100})),provenance:{geometry:'b',source:'a'}}}
describe('Resultados 2024 completos',()=>{
 it('preserva ceros y faltantes; permite participación cero sin inventar desglose',()=>{const m=attachResults2024(base(),nominal());expect(m.results2024?.['1297']).toEqual({nominal:100,participation:0});expect(m.sections[0].votes?.PRI).toBeNull();expect(m.sections[0].votes?.PAN).toBe(0)})
 it('impide combinar fuentes, totales o contiendas diferentes',()=>{for(const change of [{provenance:{source:'otro'}},{contest:'DF' as const},{year:2021},{sections:[]}])expect(()=>attachResults2024(base(),{...nominal(),...change})).toThrow();const n=nominal();n.sections[0].total=1;expect(()=>attachResults2024(base(),n)).toThrow()})
 it('no calcula participación sobre datos inconsistentes',()=>{const n=nominal();n.sections[0].status='INCONSISTENT';n.sections[0].abstention=null;expect(attachResults2024(base(),n).results2024?.['1297'].participation).toBeNull()})
 it('ordena numéricamente y conserva todas las filas sin mutar entrada',()=>{const rows=[{sectionId:'12'},{sectionId:'2'},{sectionId:'100'}];expect(orderSections2024(rows,false).map(r=>r.sectionId)).toEqual(['2','12','100']);expect(orderSections2024(rows,true).map(r=>r.sectionId)).toEqual(['100','12','2']);expect(rows[0].sectionId).toBe('12')})
 it('ordena columnas de resultados por valor numérico en cada partido y metrica',()=>{
  const rows=[{sectionId:'101', total:200, votes:{PAN:50,PRI:30,PVEM:20,MORENA:10}},{sectionId:'102', total:140, votes:{PAN:90,PRI:10,PVEM:0,MORENA:40}},{sectionId:'103', total:300, votes:{PAN:10,PRI:5,PVEM:5,MORENA:15}}]
  const nominal = { '101': { nominal: 500, participation: 40 }, '102': { nominal: 350, participation: 50 }, '103': { nominal: 1000, participation: 30 } }
  expect(orderSections2024(rows,false,'nominal',nominal).map(r=>r.sectionId)).toEqual(['102','101','103'])
  expect(orderSections2024(rows,true,'PAN').map(r=>r.sectionId)).toEqual(['102','101','103'])
  expect(orderSections2024(rows,false,'total').map(r=>r.sectionId)).toEqual(['102','101','103'])
 })
})
