/// <reference types="node" />
import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'
import { parseSocioReference } from './socioTraceability'
import { parseServices, parseServicesValue, SERVICES_FIELDS, SERVICES_METRICS, servicesMeasure, servicesSummary } from './socioServices'
import type { ServicesData, ServicesRecord } from './socioServices'
import { SocioServicesDetails } from './SocioServicesDetails'
import type { UniverseMap } from '../gateway/universe.client'
const raw=JSON.parse(readFileSync(new URL('../../public/data/heyti-servicios-2020.json',import.meta.url),'utf8'))
const reference=parseSocioReference(JSON.parse(readFileSync(new URL('../../public/data/heyti-socioeconomico-referencia-2020.json',import.meta.url),'utf8')))
const data=parseServices(raw,reference),metric=SERVICES_METRICS[0]
function record(n:number|null,d:number|null):ServicesRecord{
 const row=Object.fromEntries(SERVICES_FIELDS.map(k=>[k,{value:0,state:'OBSERVED'}])) as ServicesRecord
 row.VPH_C_ELEC={value:n,state:n===null?'MISSING':'OBSERVED'};row.VIVPARH_CV={value:d,state:d===null?'MISSING':'OBSERVED'}
 return row
}
describe('servicios y tecnologías en viviendas INEGI2020',()=>{
 it('lee los 11 campos de 3161 secciones y coteja seis campos existentes',()=>{
  expect(Object.keys(data.sections)).toHaveLength(3161)
  expect(data.sections['1'].VIVPARH_CV.value).toBe(518)
  expect(data.sections['1'].VPH_C_ELEC.value).toBe(515)
  expect(data.sections['3180']).toBeUndefined()
 })
 it('usa viviendas con características como denominador, no viviendas totales ni personas',()=>{
  const result=servicesMeasure(data.sections['1'],metric)
  expect(result.denominator).toBe(518);expect(result.percent).toBeCloseTo(515/518*100)
  expect(result.percent).not.toBeCloseTo(515/597*100)
  expect(result.percent).not.toBeCloseTo(515/2149*100)
 })
 it('conserva el campo conjunto oficial sin inferirlo de los otros servicios',()=>{
  const row=data.sections['1'],combined=SERVICES_METRICS.find(m=>m.key==='combined')!
  const result=servicesMeasure(row,combined)
  expect(result.numerator).toBe(490)
  expect(result.numerator).not.toBe(Math.min(row.VPH_C_ELEC.value!,row.VPH_AGUADV.value!,row.VPH_DRENAJ.value!))
 })
 it('agrega con razón de sumas y una misma cobertura calculable',()=>{
  const fixture:ServicesData={officialCsvSha256:'test',sections:{'1':record(1,10),'2':record(90,100)}}
  expect(servicesSummary(['1','2'],fixture,metric)).toMatchObject({count:91,denominator:110,pairs:2})
  expect(servicesSummary(['1','2'],fixture,metric).percent).toBeCloseTo(91/110*100)
  expect(servicesSummary(['1','2'],fixture,metric).percent).not.toBe(50)
 })
 it('conserva cero observado y distingue base cero y registro ausente',()=>{
  expect(servicesMeasure(record(0,10),metric)).toMatchObject({numerator:0,percent:0,status:'AVAILABLE'})
  expect(servicesMeasure(record(0,0),metric)).toMatchObject({numerator:0,percent:null,status:'ZERO_DENOMINATOR'})
  expect(servicesMeasure(undefined,metric).status).toBe('NO_RECORD')
 })
 it('conserva conteo aunque falte denominador e indica coberturas distintas',()=>{
  const fixture:ServicesData={officialCsvSha256:'test',sections:{'1':record(2,null),'2':record(4,10)}}
  expect(servicesMeasure(fixture.sections['1'],metric)).toMatchObject({numerator:2,percent:null,status:'MISSING_DENOMINATOR'})
  expect(servicesSummary(['1','2','3'],fixture,metric)).toMatchObject({pairs:1,total:3,count:4,denominator:10,countsAvailable:2,countAvailableSum:6})
 })
 it('señala incoherencias y evita agregarlas o generar porcentajes imposibles',()=>{
  const row=record(11,10),fixture:ServicesData={officialCsvSha256:'test',sections:{'1':row}}
  expect(servicesMeasure(row,metric)).toMatchObject({numerator:11,percent:null,status:'INCONSISTENT'})
  expect(servicesSummary(['1'],fixture,metric)).toMatchObject({pairs:0,percent:null,countAvailableSum:null})
 })
 it('separa reservado, no aplica, faltante y cero; rechaza conteos inválidos',()=>{
  expect(parseServicesValue('*')).toEqual({value:null,state:'RESERVED'})
  expect(parseServicesValue('')).toEqual({value:null,state:'MISSING'})
  expect(parseServicesValue('N/A')).toEqual({value:null,state:'NOT_APPLICABLE'})
  expect(parseServicesValue('0')).toEqual({value:0,state:'OBSERVED'})
  for(const v of ['-1','1.5','abc',true,Infinity])expect(()=>parseServicesValue(v)).toThrow()
 })
 it('rechaza huellas, coberturas o cifras compartidas incompatibles',()=>{
  const hash=structuredClone(raw);hash.officialCsvSha256='otra';expect(()=>parseServices(hash,reference)).toThrow('incompatible')
  const changed=structuredClone(raw);changed.sections['1'][1]='1';expect(()=>parseServices(changed,reference)).toThrow('no coincide')
  const missing=structuredClone(raw);delete missing.sections['1'];expect(()=>parseServices(missing,reference)).toThrow('incompleta')
 })
 it('no modifica el archivo y conserva porcentajes reales en rango o estados explícitos',()=>{
  const snapshot=JSON.stringify(raw);parseServices(raw,reference);expect(JSON.stringify(raw)).toBe(snapshot)
  const outOfRange:string[]=[]
  for(const [id,row] of Object.entries(data.sections))for(const m of SERVICES_METRICS){
   const result=servicesMeasure(row,m)
   if(result.percent!==null&&(!Number.isFinite(result.percent)||result.percent<0||result.percent>100))outOfRange.push(id+':'+m.key)
  }
  expect(outOfRange).toEqual([])
 })
 it('conserva las filas y diez medidas, denominador, detalle y significado de agua/drenaje',()=>{
  const map:UniverseMap={universe:{level:'state',id:'11',label:'Prueba',sections:3},year:2024,contest:'A',provenance:{source:'test'},counts:{},coverage:{geographic:3,represented:3,blocked:0},sections:['3180','2','1'].map(sectionId=>({sectionId,status:'NO_DATA',leader:null,total:null,geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[0,1],[0,0]]]}}))}
  const html=renderToStaticMarkup(<SocioServicesDetails map={map} data={data} reference={reference} selected="1" onSelect={()=>{}}/>)
  expect((html.match(/aria-selected=/g)||[]).length).toBe(3)
  for(const m of SERVICES_METRICS)expect(html).toContain(m.label+': cantidad / %')
  expect(html).toContain('N/D');expect(html).toContain('origen documentado 2514')
  expect(html).toContain('Detalle de servicios');expect(html).toContain('VIVPARH_CV')
  expect(html).toContain('potabilidad');expect(html).toContain('fosa séptica')
  expect(html).toContain('no sumarlas');expect(html).toContain('laptop o tableta')
  expect(html.indexOf('Ver servicios de sección 1')).toBeLessThan(html.indexOf('Ver servicios de sección 2'))
 })
})
