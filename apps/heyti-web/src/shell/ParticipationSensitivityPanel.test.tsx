import { describe, expect, it } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'
import type { UniverseMap } from '../gateway/universe.client'
import { buildParticipationSensitivity } from './participationSensitivity'
import { ParticipationSensitivityDetails } from './ParticipationSensitivityPanel'
function fixture():UniverseMap[]{
 const section={sectionId:'0002',status:'ABS_MID' as const,leader:null,total:600,nominal:1000,abstention:40,geometry:{type:'Polygon' as const,coordinates:[[[0,0],[1,0],[0,1],[0,0]]] as [number,number][][]}}
 const map=(year:number):UniverseMap=>({year,metric:'abstention',contest:'DF',universe:{level:'federal-district',id:'1',label:'Distrito de prueba',sections:2},provenance:{source:'fixture'},coverage:{geographic:2,represented:2,blocked:0},counts:{},sections:[section,{...section,sectionId:'0001',status:'NO_DATA',total:null,abstention:null}]})
 const source:UniverseMap={...map(2024),metric:'concentration',sections:map(2024).sections.map(s=>({...s,status:s.total===null?'NO_DATA':'HHI_MID',votes:s.total===null?{PAN:null,PRI:null,PVEM:null,MORENA:null}:{PAN:300,PRI:120,PVEM:60,MORENA:60}}))}
 return [map(2018),map(2021),map(2024),source]
}
describe('tabla detallada de sensibilidad',()=>{
 it('mantiene todas las filas, orden por sección, desglose y faltantes',()=>{
  const html=renderToStaticMarkup(<ParticipationSensitivityDetails scenario={buildParticipationSensitivity(fixture(),2)} selectedSection={null}/>)
  expect((html.match(/aria-selected=/g)||[]).length).toBe(2)
  expect(html.indexOf('Ver sensibilidad de sección 0001')).toBeLessThan(html.indexOf('Ver sensibilidad de sección 0002'))
  for(const party of ['PAN','PRI','PVEM','MORENA'])expect(html).toContain(`${party}: base / modificado / cambio`)
  expect(html).toContain('N/D');expect(html).toContain('Variación aplicada (pp)');expect(html).toContain('Total modificado estimado')
 })
 it('incluye históricos y detalle de opciones para la sección elegida',()=>{
  const html=renderToStaticMarkup(<ParticipationSensitivityDetails scenario={buildParticipationSensitivity(fixture(),2)} selectedSection="0002"/>)
  expect(html).toContain('Detalle sección 0002');expect(html).toContain('Total histórico');expect(html).toContain('Cambio estimado')
  expect(html).not.toContain('Voltea a tu favor');expect(html).not.toContain('Transferencia mínima')
 })
})