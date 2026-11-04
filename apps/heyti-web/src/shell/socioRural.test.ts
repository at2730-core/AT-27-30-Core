import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { parseSocioReference } from './socioTraceability'
import { parseRural, ruralRows, ruralSummary, ruralType, ruralComparison, geometryFingerprint, sectionKindLabel } from './socioRural'
import type { UniverseMap } from '../gateway/universe.client'
import type { TerritorialGeometry } from '../gateway/territorial.geometry'
const raw=JSON.parse(readFileSync(new URL('../../public/data/heyti-tipo-seccion-2020.json',import.meta.url),'utf8'))
const reference=parseSocioReference(JSON.parse(readFileSync(new URL('../../public/data/heyti-socioeconomico-referencia-2020.json',import.meta.url),'utf8')))
const data=parseRural(raw,reference)
const geometry:TerritorialGeometry={type:'Polygon',coordinates:[[[-101,21],[-100,21],[-100,22],[-101,21]]]}
const map=(ids:string[],level='federal-district')=>({universe:{level},sections:ids.map(sectionId=>({sectionId,geometry}))}) as UniverseMap

describe('Tipo urbano-rural de sección',()=>{
 it('preserva la clasificación censal completa y el archivo V2 como fuentes distintas',()=>{
  expect(Object.keys(data.census)).toHaveLength(3161)
  expect(Object.keys(data.snapshot)).toHaveLength(3266)
  expect(data.census).toEqual(raw.census)
  expect(data.snapshot).toEqual(raw.snapshot)
  expect(['2','3','4'].map(k=>Object.values(data.census).filter(r=>r.type===k).length)).toEqual([1873,224,1064])
  expect(['2','3','4'].map(k=>Object.values(data.snapshot).filter(r=>r.type===k).length)).toEqual([1969,235,1062])
  expect(Object.keys(data.census).filter(id=>data.snapshot[id]&&data.census[id].type!==data.snapshot[id].type)).toHaveLength(13)
 })
 it('separa desconocido de urbano/mixto/rural y coteja el código publicado',()=>{
  expect(sectionKindLabel('2')).toBe('Urbana')
  expect(sectionKindLabel('3')).toBe('Mixta')
  expect(sectionKindLabel('4')).toBe('Rural')
  expect(sectionKindLabel(null)).toBe('N/D')
  const row=ruralRows(map(['331']),data)[0]
  expect(row.census!.population).toBe(reference.sections['331'].values.POB_TOTAL)
 })
 it('conserva la fecha no acreditada del archivo y rechaza códigos o población alterados',()=>{
  expect(()=>parseRural({...raw,snapshotDate:'2026-10-22'},reference)).toThrow()
  expect(()=>parseRural({...raw,officialCsvSha256:'0'.repeat(64)},reference)).toThrow()
  expect(()=>parseRural({...raw,classification:{'2':'Rural','3':'Mixta','4':'Urbana'}},reference)).toThrow()
  const id=Object.keys(raw.census)[0]
  for(const patch of [{type:'0'},{type:2},{population:raw.census[id].population+1}])expect(()=>parseRural({...raw,census:{...raw.census,[id]:{...raw.census[id],...patch}}},reference)).toThrow()
 })
 it('usa el tipo del archivo solo si la geometría coincide; una clave igual no basta',()=>{
  const id='96',adjusted={...data,snapshot:{...data.snapshot,[id]:{...data.snapshot[id],geometryFingerprint:geometryFingerprint(geometry)}}}
  const row=ruralRows(map([id]),adjusted)[0]
  expect(row.geometryMatch).toBe(true)
  expect(ruralType(row,'snapshot')).toBe(adjusted.snapshot[id].type)
  expect(ruralComparison(row)).toBe('Clasificaciones distintas')
  const changed=structuredClone(geometry);changed.coordinates[0][1][0]-=.1
  const changedMap=map([id]);changedMap.sections[0].geometry=changed
  const mismatch=ruralRows(changedMap,adjusted)[0]
  expect(mismatch.geometryMatch).toBe(false)
  expect(ruralType(mismatch,'snapshot')).toBeNull()
  expect(mismatch.snapshot!.type).toBe(adjusted.snapshot[id].type)
  expect(ruralType(mismatch,'census')).toBe(data.census[id].type)
  expect(ruralComparison(mismatch)).toBe('Cotejo geométrico pendiente')
 })
 it('no hereda el tipo de la sección de origen para claves sin registro censal propio',()=>{
  const id=Object.keys(data.snapshot).find(id=>!data.census[id])!
  const row=ruralRows(map([id]),data)[0]
  expect(row.census).toBeNull()
  expect(ruralType(row,'census')).toBeNull()
  expect(ruralComparison(row)).toBe('Sin registro censal 2020')
 })
 it('los porcentajes cuentan secciones con tipo disponible, sin distribuir población mixta',()=>{
  const matched=Object.keys(data.census).filter(id=>data.snapshot[id]).slice(0,20)
  const unknown=Object.keys(data.snapshot).find(id=>!data.census[id])!
  const rows=ruralRows(map([...matched,unknown]),data),summary=ruralSummary(rows,'census')
  expect(summary).toMatchObject({represented:21,known:20,missing:1})
  expect(summary.bands.reduce((n,b)=>n+b.count,0)).toBe(20)
  expect(summary.bands.reduce((n,b)=>n+(b.percent??0),0)).toBeCloseTo(100)
  expect(ruralSummary([], 'census').bands.every(b=>b.percent===null)).toBe(true)
 })
 it('conserva los 30 registros censales sin polígono en la consulta estatal, fuera del mapa y del denominador',()=>{
  const rows=ruralRows(map(['331'],'state'),data)
  const summary=ruralSummary(rows,'census')
  expect(rows.filter(r=>!r.inMap)).toHaveLength(30)
  expect(summary).toMatchObject({represented:1,known:1,withoutGeometry:30})
  expect(ruralRows(map(['331'],'local-district'),data)).toHaveLength(1)
 })
 it('la huella distingue geometría, orden y coordenadas sin modificar los datos de entrada',()=>{
  const before=JSON.stringify(geometry),other=structuredClone(geometry)
  other.coordinates[0].reverse()
  expect(geometryFingerprint(geometry)).toBe(geometryFingerprint(structuredClone(geometry)))
  expect(geometryFingerprint(other)).not.toBe(geometryFingerprint(geometry))
  expect(JSON.stringify(geometry)).toBe(before)
 })
})
