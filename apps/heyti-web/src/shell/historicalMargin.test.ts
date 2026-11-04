import { describe, expect, it } from 'vitest'
import { historicalMargin } from './historicalMargin'
import type { UniverseSection } from '../gateway/universe.client'
function row(votes:Record<string,number|null>,status:UniverseSection['status']='HHI_MID'):UniverseSection { return { sectionId:'1',status,leader:null,total:1000,votes,geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[0,1],[0,0]]]}} }
describe('diferencia histórica',()=>{
 it('usa total de contienda y no la suma de partidos',()=>{
  const result=historicalMargin(row({PAN:400,PRI:100,PVEM:50,MORENA:200}))
  expect(result.first).toEqual(['PAN']);expect(result.second).toEqual(['MORENA']);expect(result.votes).toBe(200);expect(result.pp).toBe(20)
 })
 it('conserva empates máximos sin ganador y segundo máximo compartido',()=>{
  const tie=historicalMargin(row({PAN:300,PRI:300,PVEM:0,MORENA:0}))
  expect(tie.status).toBe('TIE');expect(tie.votes).toBe(0);expect(tie.first).toEqual(['PAN','PRI'])
  expect(historicalMargin(row({PAN:400,PRI:100,PVEM:100,MORENA:0})).second).toEqual(['PRI','PVEM'])
 })
 it('no calcula con faltantes, ceros o inconsistencia',()=>{
  expect(historicalMargin(row({PAN:null,PRI:100,PVEM:0,MORENA:0})).votes).toBeNull()
  expect(historicalMargin(row({PAN:0,PRI:0,PVEM:0,MORENA:0})).status).toBe('NO_TRACKED_VOTES')
  expect(historicalMargin(row({PAN:400,PRI:100,PVEM:0,MORENA:0},'INCONSISTENT')).votes).toBeNull()
 })
})
