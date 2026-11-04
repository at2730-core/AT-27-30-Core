import { describe, expect, it, vi } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'
import type { UniverseMap, UniverseSection } from '../gateway/universe.client'
import { HistoricalReferencePanel } from './HistoricalReferencePanel'
import { attachHistoricalReference } from './historicalReference'
vi.mock('../platform/useWorkspace',()=>({useWorkspace:()=>({state:{universe:null}})}))
function fixture() {
  const section: UniverseSection = {sectionId:'0002',status:'HHI_MID',leader:null,total:200,votes:{PAN:80,PRI:60,PVEM:20,MORENA:10},geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[0,1],[0,0]]]}}
  const data: UniverseMap = {year:2024,metric:'concentration',contest:'DF',universe:{level:'federal-district',id:'1',label:'Distrito de prueba',sections:3},coverage:{geographic:3,represented:3,blocked:0},counts:{},provenance:{source:'fixture'},sections:[section,{...section,sectionId:'0001',votes:{PAN:0,PRI:null,PVEM:20,MORENA:10},status:'NO_DATA'},{...section,sectionId:'0003',votes:{PAN:70,PRI:70,PVEM:20,MORENA:10}}]}
  return attachHistoricalReference(data,{party:'PAN',unit:'votes',cap:1000,emphasis:0})
}
describe('presentación histórica con detalle completo',()=>{
  it('incluye todas las filas, conserva N/D y las ordena por sección',()=>{
    const html=renderToStaticMarkup(<HistoricalReferencePanel result={fixture()} onResult={()=>{}} onPending={()=>{}} selectedSection={null} onSelectSection={()=>{}}/>)
    expect((html.match(/aria-selected=/g)||[]).length).toBe(3)
    expect(html.indexOf('Ver sección 0001')).toBeLessThan(html.indexOf('Ver sección 0002'))
    expect(html.indexOf('Ver sección 0002')).toBeLessThan(html.indexOf('Ver sección 0003'))
    expect(html).toContain('N/D');expect(html).toContain('Datos insuficientes')
    expect(html).toContain('Diferencia (pp)');expect(html).toContain('Opción de referencia histórica')
    expect(html).not.toContain('Ociosos');expect(html).not.toContain('Adición mínima')
  })
  it('presenta el detalle de las cuatro opciones y el empate sin inventar un ganador',()=>{
    const html=renderToStaticMarkup(<HistoricalReferencePanel result={fixture()} onResult={()=>{}} onPending={()=>{}} selectedSection="0003" onSelectSection={()=>{}}/>)
    expect(html).toContain('Detalle sección 0003');expect(html).toContain('PAN / PRI')
    expect(html).toContain('Votos observados 2024');expect(html).toContain('MORENA')
  })
})