import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { parseIncome, parseIncomeNumber, incomeBand, incomePrecision, incomeIds } from './socioIncome'
import type { UniverseMap } from '../gateway/universe.client'
const raw=JSON.parse(readFileSync(new URL('../../public/data/heyti-ingreso-municipal-2024.json',import.meta.url),'utf8'))
const data=parseIncome(raw)
const map=(level:string,ids:string[])=>({universe:{level},sections:ids.map(sectionId=>({sectionId}))}) as UniverseMap

describe('Ingreso municipal ICMM 2024',()=>{
 it('preserva las cinco estadísticas originales de 46 municipios y la referencia estatal separada',()=>{
  expect(data.areas).toHaveLength(46)
  expect(Object.keys(data.rows)).toHaveLength(47)
  const fields=['estimate','standardError','lower','upper','cv'] as const
  const errors=raw.statistics.filter((s:{cvegeo:string;est:string;icpth:string})=>data.rows[s.cvegeo][fields[Number(s.est)-1]]!==Number(s.icpth.replaceAll(',','')))
  expect(errors).toEqual([])
  expect(data.rows['11000']).toMatchObject({estimate:74544.75,standardError:1590.25,lower:71929.02,upper:77160.47,cv:2.133})
 })
 it('conserva ceros y distingue dato faltante de formato monetario inválido',()=>{
  expect(parseIncomeNumber('0')).toBe(0)
  expect(parseIncomeNumber('74,544.75')).toBe(74544.75)
  expect(parseIncomeNumber(null)).toBeNull()
  expect(parseIncomeNumber('')).toBeNull()
  for(const v of ['7,45.00','-1','N/D','NaN',0])expect(()=>parseIncomeNumber(v)).toThrow()
 })
 it('clasifica por los umbrales del reporte, incluyendo sus límites',()=>{
  expect([0,34999.99,35000,44999.99,45000,59999.99,60000,79999.99,80000,null].map(incomeBand)).toEqual([0,0,1,1,2,2,3,3,4,null])
  expect([null,0,14.999,15,29.999,30].map(incomePrecision)).toEqual(['N/D','CV igual a cero','Alta','Moderada','Moderada','Baja'])
 })
 it('conserva el municipio en la consulta cuando falta su estimación, sin completarla con el valor estatal',()=>{
  const id='11001'
  const partial=parseIncome({...raw,statistics:raw.statistics.filter((s:{cvegeo:string;est:string})=>s.cvegeo!==id||s.est!=='1')})
  expect(partial.rows[id].estimate).toBeNull()
  expect(partial.rows[id].lower).toBe(data.rows[id].lower)
  expect(incomeBand(partial.rows[id].estimate)).toBeNull()
  expect(incomeIds(partial,map('state',[]))).toContain(id)
 })
 it('filtra por cruce espacial sin sumar o repartir promedios ni incluir la fila estatal como municipio',()=>{
  expect(incomeIds(data,map('state',[]))).toHaveLength(46)
  expect(incomeIds(data,map('state',[]))).not.toContain('11000')
  const sid=data.sectionLinks[data.areas[0].id][0]
  const expected=data.areas.filter(a=>data.sectionLinks[a.id].includes(sid)).map(a=>a.id).sort()
  const before=JSON.stringify(data.rows)
  expect(incomeIds(data,map('federal-district',[sid]))).toEqual(expected)
  expect(incomeIds(data,map('local-district',['999999']))).toEqual([])
  expect(JSON.stringify(data.rows)).toBe(before)
 })
 it('rechaza estadísticas duplicadas, entidades ajenas e intervalos contradictorios',()=>{
  expect(()=>parseIncome({...raw,statistics:[...raw.statistics,raw.statistics[0]]})).toThrow()
  expect(()=>parseIncome({...raw,statistics:[{...raw.statistics[0],cve_ent:'12'}]})).toThrow()
  const bad=raw.statistics.map((s:{cvegeo:string;est:string})=>s.cvegeo==='11001'&&s.est==='3'?{...s,icpth:'999999'}:s)
  expect(()=>parseIncome({...raw,statistics:bad})).toThrow()
  expect(()=>parseIncome({...raw,confidence:95})).toThrow()
  expect(()=>parseIncome({...raw,sectionLinks:{}})).toThrow()
 })
 it('mantiene las coordenadas geográficas y la correspondencia entre claves de fuente y geometrías',()=>{
  expect(data.areas.filter(a=>!data.rows[a.id])).toEqual([])
  const bad=data.areas.filter(a=>{
   const coords=a.geometry.type==='Polygon'?a.geometry.coordinates.flat():a.geometry.coordinates.flat(2)
   return coords.some(([x,y])=>x < -103 || x > -99 || y < 19 || y > 23)
  })
  expect(bad).toEqual([])
 })
})
