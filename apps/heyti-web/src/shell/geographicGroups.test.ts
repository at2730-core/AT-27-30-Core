import { describe, expect, it } from 'vitest'
import { buildGeographicGroups, buildGeographicGroupsAsync, geographicSum } from './geographicGroups'
import type { TerritorialGeometry } from '../gateway/territorial.geometry'
import type { UniverseMap } from '../gateway/universe.client'
const square=(x:number,y:number):TerritorialGeometry=>({type:'Polygon',coordinates:[[[x,y],[x+1,y],[x+1,y+1],[x,y+1],[x,y]]]})
const row=(id:string,x:number,y:number)=>({sectionId:id,geometry:square(x,y)})
describe('colindancias exclusivamente geométricas',()=>{
 it('forma componentes y conserva aisladas; excluye contacto por vértice',()=>{
  const result=buildGeographicGroups([row('3',3,3),row('2',1,0),row('1',0,0),row('4',2,1)])
  expect(result.rows['1'].neighbours).toEqual(['2'])
  expect(result.rows['2'].neighbours).toEqual(['1'])
  expect(result.groups.map(g=>g.sections)).toEqual([['1','2'],['3'],['4']])
 })
 it('acepta segmentación distinta y dirección invertida del límite',()=>{
  const b={sectionId:'2',geometry:{type:'Polygon',coordinates:[[[1,0],[1,0.5],[1,1],[2,1],[2,0],[1,0]]]} as TerritorialGeometry}
  expect(buildGeographicGroups([row('1',0,0),b]).boundaryPairs).toBe(1)
 })
 it('incluye MultiPolygon y límites de anillos interiores',()=>{
  const outer:TerritorialGeometry={type:'Polygon',coordinates:[[[0,0],[3,0],[3,3],[0,3],[0,0]],[[1,1],[2,1],[2,2],[1,2],[1,1]]]}
  const multi:TerritorialGeometry={type:'MultiPolygon',coordinates:[(square(1,1) as Extract<TerritorialGeometry,{type:'Polygon'}>).coordinates]}
  expect(buildGeographicGroups([{sectionId:'1',geometry:outer},{sectionId:'2',geometry:multi}]).boundaryPairs).toBe(1)
 })
 it('no inventa límites para anillos abiertos o geometrías vacías',()=>{
  const invalid:TerritorialGeometry={type:'Polygon',coordinates:[[[0,0],[1,0],[1,1],[0,1]]]}
  const r=buildGeographicGroups([{sectionId:'1',geometry:invalid},{sectionId:'2',geometry:{type:'MultiPolygon',coordinates:[]}}])
  expect(r.evaluated).toBe(0);expect(r.groups).toEqual([]);expect(r.rows['1'].groupId).toBeNull()
 })
 it('mantiene grupos y colores al cambiar orden o votos asociados',()=>{
  const source=[row('2',1,0),row('1',0,0)]
  expect(buildGeographicGroups(source)).toEqual(buildGeographicGroups([...source].reverse().map(s=>({...s,votes:{PAN:999}}))))
  expect(()=>buildGeographicGroups([source[0],source[0]])).toThrow('duplicadas')
 })
 it('permite cancelación antes del cálculo',async()=>{
  const abort=new AbortController();abort.abort()
  await expect(buildGeographicGroupsAsync([row('1',0,0)],abort.signal)).rejects.toMatchObject({name:'AbortError'})
 })
 it('resuelve una malla de 2500 secciones sin perder vecinos',()=>{
  const sections=Array.from({length:2500},(_,i)=>row(String(i),i%50,Math.floor(i/50)))
  const r=buildGeographicGroups(sections)
  expect(r.groups).toHaveLength(1);expect(r.boundaryPairs).toBe(4900);expect(r.rows['51'].neighbours).toHaveLength(4)
 })
 it('distingue cero de faltante y excluye cifras inconsistentes de sumas',()=>{
  const result={sections:[{...row('1',0,0),status:'HHI_MID',votes:{PAN:0},total:20},{...row('2',1,0),status:'NO_DATA',votes:{PAN:null},total:null}]} as unknown as UniverseMap
  expect(geographicSum(result,['1'],'PAN')).toMatchObject({sum:0,covered:1})
  expect(geographicSum(result,['1','2'],'PAN')).toEqual({sum:null,availableSum:0,covered:1,expected:2})
  result.sections[0].status='INCONSISTENT'
  expect(geographicSum(result,['1'],'total').sum).toBeNull()
 })
})
