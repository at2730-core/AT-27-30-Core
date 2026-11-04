import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { parsePoverty, povertyIds, povertyBand, povertyRangeBand, povertyDisplay, povertyNumber, metricHasDeprivations, POVERTY_YEARS, POVERTY_KEYS } from './socioPoverty'
import type { UniverseMap } from '../gateway/universe.client'
const raw=JSON.parse(readFileSync(new URL('../../public/data/heyti-pobreza-2020.json',import.meta.url),'utf8'))
const data=parsePoverty(raw)
const map=(level:string,ids:string[])=>({universe:{level},sections:ids.map(sectionId=>({sectionId}))}) as UniverseMap

describe('Pobreza CONEVAL municipal y urbana',()=>{
 it('preserva 46 municipios, los 16 indicadores y tres años sin recalcular las cifras publicadas',()=>{
  expect(Object.keys(data.municipalRows)).toHaveLength(46)
  expect(data.metrics).toHaveLength(16)
  expect(data.municipalAreas).toHaveLength(46)
  expect(Object.values(data.municipalRows)).toEqual(raw.municipalRows)
  expect(data.stateRow).toEqual(raw.stateRow)
  expect(data.municipalRows['11001'].years[2020].indicators.poverty).toMatchObject({percent:47.7769037516,persons:43055,deprivations:2.0091799734})
 })
 it('conserva las 180 localidades y sus intervalos exactos, sin usar puntos medios',()=>{
  expect(Object.keys(data.urbanRows)).toHaveLength(180)
  expect(data.urbanAreas).toHaveLength(180)
  expect(Object.values(data.urbanRows)).toEqual(raw.urbanRows)
  expect([0,1,2,3,4].map(b=>Object.values(data.urbanRows).filter(r=>povertyRangeBand(r.range)===b).length)).toEqual([2,24,80,65,9])
  expect(data.urbanAreas.filter(a=>a.cartographicScope==='Rural').map(a=>a.id).sort()).toEqual(['110150034','110201294','110270133','110460044'])
 })
 it('trata los intervalos publicados como rangos y separa cero, sin estimación y no aplica',()=>{
  expect(povertyRangeBand('[ 0, 20)')).toBe(0)
  expect(povertyRangeBand('[80, 100]')).toBe(4)
  expect(povertyRangeBand('n.d.')).toBeNull()
  expect(povertyRangeBand('-')).toBeNull()
  expect(()=>povertyRangeBand('[20, 60)')).toThrow()
  expect([0,20,40,60,80,100,null,'n.d.','n.a.'].map(v=>povertyBand(v as any))).toEqual([0,1,2,3,4,4,null,null,null])
  expect(povertyDisplay(0,'%')).toBe('0%')
  expect(povertyDisplay('n.a.')).toBe('No aplica')
  expect(povertyDisplay('n.d.')).toBe('Sin estimación')
  expect(povertyDisplay(null)).toBe('Sin dato')
  expect(povertyNumber('n.a.')).toBeNull()
 })
 it('valida unidades y conserva separadas las carencias que la fuente no publica',()=>{
  const invalid=[]
  for(const r of [...Object.values(data.municipalRows),data.stateRow])for(const y of POVERTY_YEARS)for(const k of POVERTY_KEYS){
   const m=r.years[y].indicators[k]
   if(typeof m.percent==='number'&&(m.percent<0||m.percent>100))invalid.push(r.id)
   if(typeof m.persons==='number'&&!Number.isSafeInteger(m.persons))invalid.push(r.id)
   if(!metricHasDeprivations(k)&&m.deprivations!==null)invalid.push(r.id)
  }
  expect(invalid).toEqual([])
  expect(metricHasDeprivations('poverty')).toBe(true)
  expect(metricHasDeprivations('vulnerable_income')).toBe(false)
 })
 it('filtra unidades completas por intersección, sin sumar columnas o prorratear por distrito',()=>{
  expect(povertyIds(data,map('state',[]),'urban')).toHaveLength(180)
  expect(povertyIds(data,map('state',[]),'municipal')).toHaveLength(46)
  const sid=data.urbanLinks[data.urbanAreas[0].id][0]
  const before=JSON.stringify(data.urbanRows)
  expect(povertyIds(data,map('federal-district',[sid]),'urban')).toEqual(data.urbanAreas.filter(a=>data.urbanLinks[a.id].includes(sid)).map(a=>a.id).sort())
  expect(povertyIds(data,map('local-district',['999999']),'urban')).toEqual([])
  expect(JSON.stringify(data.urbanRows)).toBe(before)
 })
 it('mantiene filas sin geometría o sin dato en la consulta estatal, sin imputación',()=>{
  const u=raw.urbanRows[0]
  const d=parsePoverty({...raw,urbanRows:[{...u,range:'n.d.'},...raw.urbanRows.slice(1)],urbanGeography:{...raw.urbanGeography,features:raw.urbanGeography.features.filter((f:any)=>f.properties.id!==u.id)},urbanLinks:Object.fromEntries(Object.entries(raw.urbanLinks).filter(([id])=>id!==u.id))})
  expect(povertyIds(d,map('state',[]),'urban')).toContain(u.id)
  expect(povertyRangeBand(d.urbanRows[u.id].range)).toBeNull()
 })
 it('rechaza duplicados, porcentajes imposibles, rangos ajenos y cartografía inconsistente',()=>{
  expect(()=>parsePoverty({...raw,urbanRows:[...raw.urbanRows,raw.urbanRows[0]]})).toThrow()
  expect(()=>parsePoverty({...raw,municipalRows:[...raw.municipalRows,raw.municipalRows[0]]})).toThrow()
  const r=structuredClone(raw.municipalRows[0]);r.years[2020].indicators.poverty.percent=101
  expect(()=>parsePoverty({...raw,municipalRows:[r]})).toThrow()
  expect(()=>parsePoverty({...raw,years:[2020,2024]})).toThrow()
  expect(()=>parsePoverty({...raw,urbanLinks:{}})).toThrow()
 })
})
