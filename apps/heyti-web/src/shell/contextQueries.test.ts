import {describe,it,expect} from 'vitest'
import {availableCrossQueries,comparisonModules,scopeKey,supportedUniverse} from './contextQueries'
import type {UniverseSelection} from '../platform/platform.types'
const section:UniverseSelection={id:'228',level:'section',label:'Sección 228',parentId:null,truthStatus:'pending'}
describe('cross query and comparison scope',()=>{
 it('offers only section queries for an active section, never silently state',()=>{
  expect(availableCrossQueries(section).length).toBe(4)
  expect(availableCrossQueries(section).every(q=>q.scope==='section')).toBe(true)
 })
 it('offers five existing area queries for a district without mutation',()=>{
  const df={...section,id:'1',level:'federal-district' as const}, before=structuredClone(df)
  expect(availableCrossQueries(df).map(q=>q.id)).toEqual(['results2024','leaders','participation','socio-indicators','socio-education'])
  expect(df).toEqual(before)
 })
 it('requires explicit supported universe',()=>{
  expect(availableCrossQueries(null)).toEqual([])
  expect(supportedUniverse({...section,level:'country'})).toBe(false)
  expect(supportedUniverse({...section,id:'0'})).toBe(false)
 })
 it('allows two or three supported distinct perspectives',()=>{
  expect(comparisonModules(['territorial-analysis','socioeconomic'])).toEqual(['territorial-analysis','socioeconomic'])
  expect(comparisonModules(['territorial-analysis','win-all','socioeconomic'])).toHaveLength(3)
 })
 it('rejects unsupported, duplicated, empty and oversized selections',()=>{
  for(const ids of [[],['field','win-all'],['win-all','win-all'],['territorial-analysis'],['territorial-analysis','win-all','socioeconomic','field']] as const)expect(()=>comparisonModules([...ids])).toThrow()
 })
 it('distinguishes scope level and missing scope',()=>{
  expect(scopeKey(section)).not.toBe(scopeKey({...section,level:'federal-district'}))
  expect(scopeKey(null)).toBe('none')
 })
})
