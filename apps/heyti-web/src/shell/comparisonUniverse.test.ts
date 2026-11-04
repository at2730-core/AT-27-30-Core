import {describe,it,expect,vi} from 'vitest'
import {changeComparisonUniverse} from './comparisonUniverse'
import type {UniverseSelection} from '../platform/platform.types'
import type {UniverseOption} from '../gateway/universe.client'
const current:UniverseSelection={id:'228',level:'section',label:'Sección 228',parentId:null,truthStatus:'pending'}
const df:UniverseOption={id:'1',level:'federal-district',label:'Distrito federal 1',sections:190}
describe('explicit comparison universe selection',()=>{
 it('resets old data before applying DF01 and keeps pending validation',()=>{
  const order:string[]=[];let selected:UniverseSelection|null=null
  changeComparisonUniverse(current,'federal-district:1',[df],()=>order.push('reset'),u=>{order.push('select');selected=u})
  expect(order).toEqual(['reset','select']);expect(selected).toEqual({id:'1',level:'federal-district',label:'Distrito federal 1',parentId:'11',truthStatus:'pending'})
 })
 it('does not reset the current scope',()=>{
  const reset=vi.fn(),select=vi.fn()
  expect(changeComparisonUniverse(current,'section:228',[df],reset,select)).toBe(false)
  expect(reset).not.toHaveBeenCalled();expect(select).not.toHaveBeenCalled()
 })
 it('rejects absent and duplicated choices before changing state',()=>{
  for(const catalog of [[],[df,df]]){
   const reset=vi.fn(),select=vi.fn()
   expect(()=>changeComparisonUniverse(current,'federal-district:1',catalog,reset,select)).toThrow()
   expect(reset).not.toHaveBeenCalled();expect(select).not.toHaveBeenCalled()
  }
 })
 it('handles same numeric id at different territorial levels',()=>{
  const reset=vi.fn(),select=vi.fn()
  expect(changeComparisonUniverse({...current,id:'1',level:'municipality'},'federal-district:1',[df],reset,select)).toBe(true)
  expect(select).toHaveBeenCalledWith(expect.objectContaining({level:'federal-district',id:'1'}))
 })
 it('state selection has no invented parent',()=>{
  const select=vi.fn()
  changeComparisonUniverse(null,'state:11',[{...df,id:'11',level:'state',label:'Guanajuato'}],vi.fn(),select)
  expect(select).toHaveBeenCalledWith(expect.objectContaining({level:'state',parentId:null}))
 })
})
