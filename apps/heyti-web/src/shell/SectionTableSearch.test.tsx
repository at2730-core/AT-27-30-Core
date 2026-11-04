import {Children,isValidElement} from 'react'
import type {ReactElement,ReactNode} from 'react'
import {renderToStaticMarkup} from 'react-dom/server'
import {describe,it,expect} from 'vitest'
import {SectionTableSearch,sectionTableView} from './SectionTableSearch'

const click=()=>{}
const make=()=> <div className="heyti-win-table-scroll" role="region" aria-label="Resultados de prueba"><table className="heyti-win-table heyti-section-table"><caption>DF01 · 2024</caption><thead><tr><th>Sección</th><th>Dato</th></tr></thead><tbody>{[{id:'1467',value:'N/D'},{id:'1466',value:'0'},{id:'228',value:'42'}].map(row=><tr key={row.id} data-section-id={row.id} aria-selected={row.id==='1466'} onClick={click}><th><button type="button">{row.id}</button></th><td>{row.value}</td></tr>)}</tbody></table></div>
type Node=ReactElement<{children?:ReactNode;onClick?:()=>void;'aria-selected'?:boolean}>
const child=(node:Node,type:string)=>Children.toArray(node.props.children).find(c=>isValidElement(c)&&c.type===type) as Node
describe('Búsqueda de sección en tablas',()=>{
 it('muestra todas las filas y conserva el orden original sin filtro',()=>{
  const view=sectionTableView(make(),'')!
  expect(view.total).toBe(3);expect(view.visible).toBe(3)
  const html=renderToStaticMarkup(view.content)
  expect(html.indexOf('data-section-id="1467"')<html.indexOf('data-section-id="1466"')).toBe(true)
 })
 it('busca coincidencia exacta sin confundir secciones con prefijos',()=>{
  expect(sectionTableView(make(),'1466')!.visible).toBe(1)
  expect(sectionTableView(make(),'146')!.visible).toBe(0)
  expect(renderToStaticMarkup(sectionTableView(make(),'1466')!.content)).not.toContain('data-section-id="1467"')
 })
 it('conserva el cero y la identificación de la sección seleccionada',()=>{
  const html=renderToStaticMarkup(sectionTableView(make(),'1466')!.content)
  expect(html).toContain('<td>0</td>');expect(html).toContain('aria-selected="true"')
 })
 it('conserva N/D al filtrar una fila con dato ausente',()=>{
  expect(renderToStaticMarkup(sectionTableView(make(),'1467')!.content)).toContain('<td>N/D</td>')
 })
 it('no modifica la fuente y limpiar el filtro recupera todas las filas',()=>{
  const source=make(),before=renderToStaticMarkup(source)
  sectionTableView(source,'1466')
  expect(renderToStaticMarkup(source)).toBe(before)
  expect(sectionTableView(source,'')!.visible).toBe(3)
 })
 it('conserva el manejador de selección y el contenedor desplazable',()=>{
  const view=sectionTableView(make(),'1466')!
  const row=child(child(child(view.content,'table'),'tbody'),'tr')
  expect(row.props.onClick).toBe(click)
  expect(renderToStaticMarkup(view.content)).toContain('class="heyti-win-table-scroll"')
 })
 it('rechaza texto, años largos y claves con cero inicial sin inventar coincidencias',()=>{
  for(const query of ['abc','14666','0146','0']){const view=sectionTableView(make(),query)!;expect(view.valid).toBe(false);expect(view.visible).toBe(0)}
  expect(sectionTableView(make(),' 228 ')!.visible).toBe(1)
 })
 it('no ofrece búsqueda a tablas sin identidad seccional explícita',()=>{
  const table=<table><tbody><tr><td>2024</td></tr></tbody></table>
  expect(sectionTableView(table,'2024')).toBeNull()
  expect(renderToStaticMarkup(<SectionTableSearch enabled={false}>{make()}</SectionTableSearch>)).not.toContain('type="search"')
 })
 it('presenta búsqueda accesible con conteo sólo de la tabla',()=>{
  const html=renderToStaticMarkup(<SectionTableSearch>{make()}</SectionTableSearch>)
  expect(html).toContain('Buscar sección en esta tabla');expect(html).toContain('type="search"')
  expect(html).toContain('3 de 3 secciones de esta tabla');expect(html).toContain('no cambia el mapa')
 })
})
