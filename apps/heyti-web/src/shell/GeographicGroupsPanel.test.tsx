import { describe, expect, it } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'
import { GeographicGroupsDetails } from './GeographicGroupsPanel'
import { buildGeographicGroups } from './geographicGroups'
import type { UniverseMap } from '../gateway/universe.client'
describe('tabla de colindancias',()=>{
 it('conserva todas las secciones, partidos, cobertura y detalle seleccionado',()=>{
  const sections=[1,2].map(n=>({sectionId:String(n),status:n===1?'HHI_MID':'NO_DATA',leader:null,total:n===1?100:null,nominal:200,votes:{PAN:n===1?0:null,PRI:30,PVEM:20,MORENA:10},geometry:{type:'Polygon' as const,coordinates:[[[n,0],[n+1,0],[n+1,1],[n,1],[n,0]] as [number,number][]]}}))
  const result={year:2024,contest:'DF',metric:'concentration',sections,universe:{label:'Prueba',level:'state',id:'11',sections:2},coverage:{geographic:2,represented:2,blocked:0},counts:{},provenance:{source:'fixture'},geographicGroups:buildGeographicGroups(sections)} as UniverseMap
  const html=renderToStaticMarkup(<GeographicGroupsDetails result={result} selectedSection="1" onSelectSection={()=>{}}/>)
  expect((html.match(/aria-selected=/g)||[]).length).toBe(2)
  for(const p of ['PAN','PRI','PVEM','MORENA'])expect(html).toContain(p+': votos 2024')
  expect(html).toContain('Detalle sección 1');expect(html).toContain('G-1');expect(html).toContain('suma disponible');expect(html).toContain('N/D')
  expect(html).toContain('no solo un punto');expect(html).toContain('fuentes en auditoría')
 })
})
