import { describe, expect, it } from 'vitest'
import { renderToStaticMarkup } from 'react-dom/server'
import type { UniverseMap } from '../gateway/universe.client'
import { buildParticipationComparison, comparisonPoints, selectParticipationComparison } from './participationComparison'
import { ParticipationComparisonDetails } from './ParticipationComparisonPanel'
function fixture(percent=60):UniverseMap[]{
 const map=(year:number):UniverseMap=>({year,metric:'abstention',contest:'DF',universe:{level:'federal-district',id:'1',label:'Distrito de prueba',sections:2},provenance:{source:'fixture'},coverage:{geographic:2,represented:2,blocked:0},counts:{},sections:['0001','0002'].map((id,i)=>({sectionId:id,status:i?'NO_DATA':'ABS_MID',leader:null,total:i?null:percent*10,nominal:1000,abstention:i?null:100-percent,geometry:{type:'Polygon',coordinates:[[[i,0],[i+1,0],[i+1,1],[i,1],[i,0]]]}}))})
 const source:UniverseMap={...map(2024),metric:'concentration',sections:map(2024).sections.map((s,i)=>({...s,status:i?'NO_DATA':percent===0?'ZERO_TOTAL':'HHI_MID',votes:i?{PAN:null,PRI:null,PVEM:null,MORENA:null}:{PAN:percent*5,PRI:percent*2,PVEM:percent,MORENA:percent}}))}
 return [map(2018),map(2021),map(2024),source]
}
describe('comparador de escenarios simultáneos',()=>{
 it('añade base, elimina duplicados y ordena sin modificar fuentes',()=>{
  const maps=fixture(),snapshot=JSON.stringify(maps),r=buildParticipationComparison(maps,[4,-4,4])
  expect(r.participationComparison!.deltas).toEqual([-4,0,4]);expect(r.participationComparison!.activeDelta).toBe(0)
  expect(JSON.stringify(maps)).toBe(snapshot)
  expect(r.participationComparison!.scenarios.every(s=>!s.participationComparison)).toBe(true)
 })
 it('calcula puntos sobre idéntica cobertura nominal, sin sumar porcentajes',()=>{
  const r=buildParticipationComparison(fixture(),[-4,4]),points=comparisonPoints(r)
  expect(points.map(p=>p.total)).toEqual([560,600,640])
  expect(points.map(p=>p.percent)).toEqual([56.00000000000001,60,64])
  expect(points.every(p=>p.valid===1&&p.nominal===1000)).toBe(true)
 })
 it('cambiar mapa conserva referencias de todas las variantes y no recalcula históricos',()=>{
  const r=buildParticipationComparison(fixture(),[-4,4]),changed=selectParticipationComparison(r,4)
  expect(changed.sensitivity!.delta).toBe(4);expect(changed.participationComparison!.activeDelta).toBe(4)
  expect(changed.participationComparison!.scenarios).toBe(r.participationComparison!.scenarios)
  expect(r.participationComparison!.activeDelta).toBe(0)
  expect(()=>selectParticipationComparison(r,2)).toThrow('no pertenece')
 })
 it('mantiene todas las filas y reconcilia opciones más residuo por escenario',()=>{
  const r=buildParticipationComparison(fixture(),[-4,4])
  for(const s of r.participationComparison!.scenarios){
   const rows=s.sensitivity!.rows
   expect(Object.keys(rows)).toEqual(['0001','0002']);expect(rows['0002'].modifiedTotal).toBeNull()
   expect(Object.values(rows['0001'].after.estimated!).reduce((n,v)=>n+v,0)+rows['0001'].after.residual!).toBe(rows['0001'].modifiedTotal)
  }
 })
 it('conserva volumen cuando falta desglose, con cifras partidistas no calculables',()=>{
  const maps=fixture();maps[3].sections[0].status='NO_DATA';maps[3].sections[0].votes!.PAN=null
  const r=buildParticipationComparison(maps,[4])
  expect(comparisonPoints(r)[1].total).toBe(640)
  expect(r.participationComparison!.scenarios[1].sensitivity!.rows['0001'].after.estimated).toBeNull()
 })
 it('señala recorte 0–100% por variante sin exceder LN',()=>{
  const r=buildParticipationComparison(fixture(98),[8])
  const row=r.participationComparison!.scenarios[1].sensitivity!.rows['0001']
  expect(row.modifiedPercent).toBe(100);expect(row.appliedPP).toBeCloseTo(2);expect(row.limited).toBe(true)
  expect(row.modifiedTotal).toBe(1000)
 })
 it('sin cobertura devuelve N/D y no inventa cero agregado',()=>{
  const maps=fixture();for(const map of maps)for(const s of map.sections){s.status='NO_DATA';s.total=null;s.abstention=null;s.votes={PAN:null,PRI:null,PVEM:null,MORENA:null}}
  const r=buildParticipationComparison(maps,[4])
  expect(comparisonPoints(r).every(p=>p.total===null&&p.percent===null&&p.valid===0)).toBe(true)
  const html=renderToStaticMarkup(<ParticipationComparisonDetails result={r}/>)
  expect(html).toContain('Gráfica no calculable');expect(html).toContain('N/D')
 })
 it('rechaza parámetros inválidos y fuentes incompatibles',()=>{
  for(const variations of [[],[0],[9],[.1],[NaN],[-8,-4,0,4,8]])expect(()=>buildParticipationComparison(fixture(),variations)).toThrow()
  const maps=fixture();maps[3].provenance={source:'otra'}
  expect(()=>buildParticipationComparison(maps,[4])).toThrow()
 })
 it('distingue cero calculable de datos faltantes',()=>{
  const r=buildParticipationComparison(fixture(2),[-8])
  expect(comparisonPoints(r)[0]).toMatchObject({total:0,percent:0,valid:1,limited:1})
  expect(r.participationComparison!.scenarios[0].sensitivity!.rows['0002'].modifiedTotal).toBeNull()
 })
 it('presenta todas las columnas, escenarios, históricos, gráfico y selección',()=>{
  const result=selectParticipationComparison(buildParticipationComparison(fixture(),[-4,4]),4)
  const html=renderToStaticMarkup(<ParticipationComparisonDetails result={result} selectedSection="0001"/>)
  expect((html.match(/aria-selected=/g)||[]).length).toBe(2)
  for(const p of ['PAN','PRI','PVEM','MORENA']){
   expect(html).toContain(p+': observado 2024')
   for(const l of ['−4','Base (0 pp)','+4'])if(l==='−4')expect(html).toContain('-4 pp · '+p);else expect(html).toContain((l==='Base (0 pp)'?l:l+' pp')+' · '+p)
  }
  expect(html).toContain('Detalle sección 0001');expect(html).toContain('role="img"');expect(html).toContain('Mapa activo')
  expect(html).toContain('cobertura calculable');expect(html).toContain('Fuentes en auditoría')
  expect(html).not.toContain('Secciones ganadas');expect(html).not.toContain('Presupuesto K')
 })
})
