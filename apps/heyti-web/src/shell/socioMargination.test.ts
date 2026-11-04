import { describe, expect, it } from 'vitest'
import { readFileSync } from 'node:fs'
import { parseMargination, marginationIds, marginationColor, MARGINATION_GRADES, MARGINATION_METRICS } from './socioMargination'
import type { UniverseMap } from '../gateway/universe.client'
const raw=JSON.parse(readFileSync(new URL('../../public/data/heyti-marginacion-urbana-2020.json',import.meta.url),'utf8'))
const data=parseMargination(raw)
const map=(level:string,ids:string[])=>({universe:{level},sections:ids.map(sectionId=>({sectionId}))}) as UniverseMap

describe('Marginación urbana oficial 2020',()=>{
 it('conserva todas las cifras y claves de la extracción, sin completar las 1500 geometrías sin índice',()=>{
  expect(Object.keys(data.rows)).toHaveLength(2214)
  expect(data.areas).toHaveLength(3714)
  expect(data.areas.filter(a=>!data.rows[a.id])).toHaveLength(1500)
  expect(Object.values(data.rows)).toEqual(raw.rows)
  expect(Object.keys(data.rows).filter(id=>!data.areas.some(a=>a.id===id))).toEqual([])
  expect(MARGINATION_GRADES.map(g=>Object.values(data.rows).filter(r=>r.GM_2020===g).length)).toEqual([405,598,694,359,158])
 })
 it('mantiene los ceros observados y porcentajes con su escala original',()=>{
  const values=Object.values(data.rows).flatMap(r=>MARGINATION_METRICS.map(([key])=>r[key]))
  expect(values.filter(v=>typeof v!=='number'||v<0||v>100)).toEqual([])
  expect(values).toContain(0)
  expect(values).toContain(100)
  expect(marginationColor()).toBe('#94a3b8')
  expect(marginationColor(Object.values(data.rows).find(r=>r.GM_2020==='Muy alto'))).toBe('#006d2c')
 })
 it('el universo estatal incluye geometrías sin índice; los distritos usan cruce, sin promediar ni repartir',()=>{
  expect(marginationIds(data,map('state',[]))).toHaveLength(3714)
  const first=data.areas.find(a=>data.sectionLinks[a.id].length>0)!
  const section=data.sectionLinks[first.id][0]
  const expected=data.areas.filter(a=>data.sectionLinks[a.id].includes(section)).map(a=>a.id).sort()
  expect(marginationIds(data,map('federal-district',[section]))).toEqual(expected)
  expect(marginationIds(data,map('local-district',['999999']))).toEqual([])
  const before=JSON.stringify(data.rows)
  marginationIds(data,map('municipality',[section]))
  expect(JSON.stringify(data.rows)).toBe(before)
 })
 it('rechaza datos parciales, duplicados y grados inventados',()=>{
  const row=raw.rows[0]
  for(const patch of [{GM_2020:'Prioritario'},{ENT:'12'},{OVSAE:101},{OVSINT:null},{POB_TOTAL:-1},{CVE_AGEB:row.CVE_AGEB.slice(1)}]){
   expect(()=>parseMargination({...raw,rows:[{...row,...patch}]})).toThrow()
  }
  expect(()=>parseMargination({...raw,rows:[row,row]})).toThrow()
  expect(()=>parseMargination({...raw,year:2024})).toThrow()
  expect(()=>parseMargination({...raw,sectionLinks:{}})).toThrow()
 })
 it('no acepta clave de geometría repetida ni anillos abiertos',()=>{
  const f=raw.geography.features[0]
  expect(()=>parseMargination({...raw,geography:{...raw.geography,features:[f,f]}})).toThrow()
  expect(()=>parseMargination({...raw,geography:{...raw.geography,features:[{...f,geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[1,1],[0,1]]]}}]}})).toThrow()
 })
})
