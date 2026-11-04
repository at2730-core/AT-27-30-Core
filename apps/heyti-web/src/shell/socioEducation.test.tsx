/// <reference types="node" />
import { readFileSync } from 'node:fs'
import { describe, expect, it } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'
import { parseSocioReference } from './socioTraceability'
import { parseEducation, parseEducationValue, EDUCATION_FIELDS, EDUCATION_METRICS, educationMeasure, educationSummary } from './socioEducation'
import type { EducationData, EducationRecord } from './socioEducation'
import { SocioEducationDetails } from './SocioEducationDetails'
import type { UniverseMap } from '../gateway/universe.client'
const raw=JSON.parse(readFileSync(new URL('../../public/data/heyti-educacion-2020.json',import.meta.url),'utf8'))
const reference=parseSocioReference(JSON.parse(readFileSync(new URL('../../public/data/heyti-socioeconomico-referencia-2020.json',import.meta.url),'utf8')))
const data=parseEducation(raw,reference),metric=EDUCATION_METRICS[0]
function record(n:number|null,d:number|null):EducationRecord{
 const r=Object.fromEntries(EDUCATION_FIELDS.map(k=>[k,{value:0,state:'OBSERVED'}])) as EducationRecord
 r[metric.numerator]={value:n,state:n===null?'MISSING':'OBSERVED'};r[metric.denominator]={value:d,state:d===null?'MISSING':'OBSERVED'}
 return r
}
describe('perfil educativo descriptivo 2020',()=>{
 it('carga los 16 campos de las 3161 secciones y conserva escolares observados',()=>{
  expect(Object.keys(data.sections)).toHaveLength(3161);expect(data.sections['1'].GRAPROES.value).toBe(9.12)
  expect(data.sections['1'].P15YM_AN.value).toBe(56);expect(data.sections['1'].P_15YMAS.value).toBe(1609)
  expect(data.sections['3180']).toBeUndefined()
 })
 it('distingue los denominadores correctos de cada grupo de edad',()=>{
  const lookup=Object.fromEntries(EDUCATION_METRICS.map(m=>[m.key,m.denominator]))
  expect(lookup).toMatchObject({'illiteracy':'P_15YMAS','nonattendance-6-11':'P_6A11','nonattendance-12-14':'P_12A14','attendance-15-17':'P_15A17','attendance-18-24':'P_18A24',postbasic:'P_18YMAS'})
  expect(educationMeasure(data.sections['1'],metric).percent).toBeCloseTo(56/1609*100)
 })
 it('calcula agregado como razón de sumas, no promedio de porcentajes',()=>{
  const fixture:EducationData={officialCsvSha256:'test',sections:{'1':record(1,10),'2':record(90,100)}}
  const summary=educationSummary(['1','2'],fixture,metric)
  expect(summary.percent).toBeCloseTo(91/110*100);expect(summary.percent).not.toBe(50)
  expect(summary).toMatchObject({pairs:2,count:91,denominator:110})
 })
 it('conserva cero observado y distingue denominador cero de ausencia de registro',()=>{
  expect(educationMeasure(record(0,10),metric)).toMatchObject({numerator:0,percent:0,status:'AVAILABLE'})
  expect(educationMeasure(record(0,0),metric)).toMatchObject({numerator:0,percent:null,status:'ZERO_DENOMINATOR'})
  expect(educationMeasure(undefined,metric).status).toBe('NO_RECORD')
 })
 it('conserva cantidad cuando falta denominador y muestra coberturas diferentes',()=>{
  const fixture:EducationData={officialCsvSha256:'test',sections:{'1':record(2,null),'2':record(4,10)}}
  expect(educationMeasure(fixture.sections['1'],metric)).toMatchObject({numerator:2,percent:null,status:'MISSING_DENOMINATOR'})
  expect(educationSummary(['1','2','3'],fixture,metric)).toMatchObject({pairs:1,total:3,count:4,denominator:10,countsAvailable:2,countAvailableSum:6})
 })
 it('no produce porcentaje ni suma una cantidad mayor que el denominador',()=>{
  const row=record(11,10),fixture:EducationData={officialCsvSha256:'test',sections:{'1':row}}
  expect(educationMeasure(row,metric)).toMatchObject({numerator:11,denominator:10,percent:null,status:'INCONSISTENT'})
  expect(educationSummary(['1'],fixture,metric)).toMatchObject({pairs:0,percent:null,countAvailableSum:null})
 })
 it('distingue reservado, faltante y no aplica sin convertirlos en cero',()=>{
  expect(parseEducationValue('*','P15YM_AN')).toEqual({value:null,state:'RESERVED'})
  expect(parseEducationValue('','P15YM_AN')).toEqual({value:null,state:'MISSING'})
  expect(parseEducationValue('N/A','P15YM_AN')).toEqual({value:null,state:'NOT_APPLICABLE'})
  expect(parseEducationValue('0','P15YM_AN')).toEqual({value:0,state:'OBSERVED'})
 })
 it('rechaza conteos fraccionarios, negativos y tokens desconocidos',()=>{
  for(const v of ['1.5','-1','abc',true,Infinity])expect(()=>parseEducationValue(v,'P15YM_AN')).toThrow()
  expect(parseEducationValue('9.12','GRAPROES').value).toBe(9.12)
 })
 it('rechaza cortes, huellas, identidades o cifras compartidas incompatibles',()=>{
  const hash=structuredClone(raw);hash.officialCsvSha256='otra';expect(()=>parseEducation(hash,reference)).toThrow('incompatible')
  const altered=structuredClone(raw);altered.sections['1'][0]='8.1';expect(()=>parseEducation(altered,reference)).toThrow('no coincide')
  const missing=structuredClone(raw);delete missing.sections['1'];expect(()=>parseEducation(missing,reference)).toThrow('incompleta')
  const unknown=structuredClone(raw);unknown.sections['99999']=unknown.sections['1'];expect(()=>parseEducation(unknown,reference)).toThrow('Identidad')
 })
 it('no altera los archivos de entrada al preparar datos',()=>{
  const snapshot=JSON.stringify(raw);parseEducation(raw,reference);expect(JSON.stringify(raw)).toBe(snapshot)
 })
 it('cada porcentaje real usa conteos compatibles o muestra su estado',()=>{
  for(const row of Object.values(data.sections))for(const m of EDUCATION_METRICS){
   const result=educationMeasure(row,m)
   if(result.percent!==null){expect(result.percent).toBeGreaterThanOrEqual(0);expect(result.percent).toBeLessThanOrEqual(100)}
   expect('winner' in result).toBe(false);expect('priority' in result).toBe(false)
  }
 })
 it('la tabla conserva todas las filas, nueve medidas, denominadores y detalle',()=>{
  const map:UniverseMap={universe:{level:'state',id:'11',label:'Prueba',sections:3},year:2024,contest:'A',provenance:{source:'test'},counts:{},coverage:{geographic:3,represented:3,blocked:0},sections:['3180','2','1'].map(sectionId=>({sectionId,status:'NO_DATA',leader:null,total:null,geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[0,1],[0,0]]]}}))}
  const html=renderToStaticMarkup(<SocioEducationDetails map={map} data={data} reference={reference} selected="1" onSelect={()=>{}}/>)
  expect((html.match(/aria-selected=/g)||[]).length).toBe(3)
  for(const m of EDUCATION_METRICS)expect(html).toContain(m.label+': cantidad / referencia / %')
  expect(html).toContain('N/D');expect(html).toContain('origen documentado 2514')
  expect(html).toContain('Detalle educativo');expect(html).toContain('No es la medición oficial')
  expect(html).toContain('no sumar columnas');expect(html).toContain('P_15YMAS')
  expect(html.indexOf('Ver perfil educativo de sección 1')).toBeLessThan(html.indexOf('Ver perfil educativo de sección 2'))
 })
})
