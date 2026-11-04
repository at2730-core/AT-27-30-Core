/// <reference types="node" />
import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'
import { parseSocio } from './socioeconomic'
import type { SocioData } from './socioeconomic'
import { parseSocioReference, verifySocioSource, socioValueStatus, socioLinkLabel, socioUniverseCoverage } from './socioTraceability'
import { SocioTraceabilitySummary } from './SocioTraceabilitySummary'
import type { UniverseMap } from '../gateway/universe.client'
const raw=JSON.parse(readFileSync(new URL('../../public/data/heyti-socioeconomico-referencia-2020.json',import.meta.url),'utf8'))
const reference=parseSocioReference(raw)
const data=parseSocio(JSON.parse(readFileSync(new URL('../../public/data/heyti-socioeconomico.json',import.meta.url),'utf8')))
function map(level:'state'|'federal-district'='state'):UniverseMap{
 return {universe:{level,id:level==='state'?'11':'1',label:'Universo de prueba',sections:4},year:2024,contest:'A',provenance:{source:'test'},counts:{},coverage:{geographic:4,represented:3,blocked:1},sections:['1','3179','3180'].map(sectionId=>({sectionId,status:'NO_DATA',leader:null,total:null,geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[0,1],[0,0]]]}}))}
}
describe('fuente y correspondencia socioeconómica',()=>{
 it('coteja exactamente los 44254 valores reales con la referencia oficial separada',()=>{
  expect(verifySocioSource(data,reference)).toEqual({allMatch:true,matched:44254,different:0,missing:0,withoutReference:0,referenceWithoutRecord:0,comparisons:44254})
 })
 it('detecta un cambio sin modificar la cifra ni afirmar que coincide',()=>{
  const changed={...data,'1':{...data['1'],POB_TOTAL:data['1'].POB_TOTAL!+1}}
  expect(verifySocioSource(changed,reference)).toMatchObject({allMatch:false,matched:44253,different:1})
  expect(socioValueStatus('1','POB_TOTAL',changed,reference)).toContain('Difiere')
  expect(data['1'].POB_TOTAL).toBe(2149)
 })
 it('distingue falta de registro, falta de valor y ausencia de referencia',()=>{
  const changed:SocioData={...data,'1':{...data['1'],POB_TOTAL:null},'9999':{...data['1']}};delete changed['2']
  expect(verifySocioSource(changed,reference)).toMatchObject({allMatch:false,missing:1,withoutReference:1,referenceWithoutRecord:1})
  expect(socioValueStatus('1','POB_TOTAL',changed,reference)).toContain('N/D')
  expect(socioValueStatus('9999','POB_TOTAL',changed,reference)).toContain('sin referencia')
 })
 it('conserva cero oficial como coincidencia y no como faltante',()=>{
  const id=Object.keys(data).find(id=>data[id].DESOCUPADOS_12MAS===0)!
  expect(id).toBeDefined();expect(socioValueStatus(id,'DESOCUPADOS_12MAS',data,reference)).toBe('Coincide con INEGI 2020')
 })
 it('rechaza referencia incompleta, cifras inventadas por conversión y mapeos incompatibles',()=>{
  const missing=structuredClone(raw);delete missing.sections['1'];expect(()=>parseSocioReference(missing)).toThrow('incompleta')
  const invalid=structuredClone(raw);invalid.sections['1'].values[0]=null;expect(()=>parseSocioReference(invalid)).toThrow('Cifra')
  const swapped=structuredClone(raw);swapped.mapping.POB_TOTAL='P_18YMAS';expect(()=>parseSocioReference(swapped)).toThrow('Correspondencias')
 })
 it('rechaza relaciones cuyo origen no exista en la referencia',()=>{
  const invalid=structuredClone(raw);invalid.relations['3180'].origin='999999'
  expect(()=>parseSocioReference(invalid)).toThrow('Relación')
 })
 it('separa origen documentado de valor propio sin transferir población',()=>{
  expect(socioLinkLabel('3180',reference)).toContain('origen documentado 2514, sin reparto')
  expect(reference.sections['3180']).toBeUndefined();expect(data['3180']).toBeUndefined()
  expect(socioLinkLabel('3179',reference)).toContain('origen pendiente')
  expect(socioLinkLabel('3313',reference)).toContain('correspondencia pendiente')
  expect(socioLinkLabel('1',reference)).toContain('equivalencia de límites pendiente')
 })
 it('calcula cobertura del universo representado y distingue distritos de distintos cortes',()=>{
  expect(socioUniverseCoverage(map(),reference)).toEqual({matched:1,withoutRecord:2,documentedOrigins:1,districtDifferences:null})
  expect(socioUniverseCoverage(map('federal-district'),reference).districtDifferences).toBe(1)
  const same=map('federal-district');same.universe.id='13'
  expect(socioUniverseCoverage(same,reference).districtDifferences).toBe(0)
 })
 it('muestra fuente, límites, cobertura y definición precisa sin repetir un total estatal como local',()=>{
  const html=renderToStaticMarkup(<SocioTraceabilitySummary map={map()} reference={reference} verification={verifySocioSource(data,reference)} indicator="VIV_CON_AGUA"/>)
  expect(html).toContain('Censo 2020');expect(html).toContain('Cotejo de cifras correcto')
  expect(html).toContain('1 secciones enlazadas por clave y 2 sin registro')
  expect(html).toContain('no certifica la equivalencia de límites')
  expect(html).toContain('potabilidad');expect(html).toContain('VPH_AGUADV')
  expect(html).not.toContain('135 geometrías');expect(html).not.toContain('distrito federal distinto')
 })
 it('una discrepancia visible no se presenta como cotejo correcto',()=>{
  const v=verifySocioSource({...data,'1':{...data['1'],POB_TOTAL:0}},reference)
  const html=renderToStaticMarkup(<SocioTraceabilitySummary map={map('federal-district')} reference={reference} verification={v} indicator="POB_TOTAL"/>)
  expect(html).toContain('Cotejo con diferencias o faltantes');expect(html).toContain('1 diferencias')
  expect(html).not.toContain('Cotejo de cifras correcto');expect(html).toContain('distrito federal distinto')
 })
})
