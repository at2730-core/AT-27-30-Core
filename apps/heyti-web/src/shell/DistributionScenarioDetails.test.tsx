import { describe, expect, it } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'
import type { UniverseMap } from '../gateway/universe.client'
import { buildDescriptiveScenario } from './descriptiveScenario'
import { DistributionScenarioDetails } from './DistributionScenarioDetails'
function fixture(){
 const map=(year:number):UniverseMap=>({year,metric:'abstention',contest:'DF',universe:{level:'federal-district',id:'1',label:'Distrito de prueba',sections:2},provenance:{source:'fixture'},coverage:{geographic:2,represented:2,blocked:0},counts:{},sections:[{sectionId:'0002',status:'ABS_MID',leader:null,total:600,nominal:1000,abstention:40,geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[0,1],[0,0]]]}},{sectionId:'0001',status:'NO_DATA',leader:null,total:null,nominal:1000,abstention:null,geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[0,1],[0,0]]]}}]})
 const source:UniverseMap={...map(2024),metric:'concentration',sections:map(2024).sections.map(s=>({...s,status:s.total===null?'NO_DATA':'HHI_MID',votes:s.total===null?{PAN:null,PRI:null,PVEM:null,MORENA:null}:{PAN:200,PRI:200,PVEM:60,MORENA:60}}))}
 return {...buildDescriptiveScenario([map(2018),map(2021),map(2024),source]),distributionOnly:true}
}
describe('tabla de distribución para revisión como usuario final',()=>{
 it('mantiene cada sección y las columnas acordadas, incluidos datos no calculables',()=>{
  const html=renderToStaticMarkup(<DistributionScenarioDetails scenario={fixture()} selectedSection={null}/>)
  expect((html.match(/aria-selected=/g)||[]).length).toBe(2)
  expect(html.indexOf('Ver distribución de sección 0001')).toBeLessThan(html.indexOf('Ver distribución de sección 0002'))
  for(const year of [2018,2021,2024])expect(html).toContain(`Participación ${year} (%)`)
  for(const party of ['PAN','PRI','PVEM','MORENA'])expect(html).toContain(`${party}: 2024 / estimado / variación`)
  expect(html).toContain('N/D');expect(html).toContain('Diferencia entre máximos (pp)');expect(html).toContain('Empate en máximo rastreado')
 })
 it('incluye históricos y desglose de la sección seleccionada',()=>{
  const html=renderToStaticMarkup(<DistributionScenarioDetails scenario={fixture()} selectedSection="0002"/>)
  expect(html).toContain('Detalle sección 0002');expect(html).toContain('Lista nominal histórica');expect(html).toContain('2024 observado');expect(html).toContain('Variación estimada')
  expect(html).not.toContain('Candidata del plan');expect(html).not.toContain('Adición mínima')
 })
})