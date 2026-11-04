import { Children, cloneElement, isValidElement, useContext, useEffect, useId, useState } from 'react'
import type { ReactElement, ReactNode } from 'react'
import { WorkspaceContext } from '../platform/workspace.context'
import './SectionTableSearch.css'

interface ElementProps { children?:ReactNode; 'data-section-id'?:string|number }
const elements = (children:ReactNode) => Children.toArray(children).filter(isValidElement<ElementProps>)

// Filters rendered section rows only. Source arrays, ordering, handlers and
// universe/map summaries stay owned by their existing query components.
export function sectionTableView(container:ReactElement<ElementProps>, query:string) {
  const nested = container.type !== 'table'
  const table = nested ? elements(container.props.children).find(child=>child.type==='table') : container
  const body = table && elements(table.props.children).find(child=>child.type==='tbody')
  if (!table || !body) return null
  const rows = elements(body.props.children).filter(child=>child.type==='tr')
  if (rows.some(row=>!/^\d+$/.test(String(row.props['data-section-id']??'')))) return null
  const value=query.trim()
  const valid=value==='' || /^[1-9]\d{0,3}$/.test(value)
  const shown=value==='' ? rows : valid ? rows.filter(row=>String(row.props['data-section-id'])===value) : []
  const filteredBody=cloneElement(body,{},shown)
  // Children.toArray may normalize keys, so identify tbody/table by element type
  // while preserving their original keys and all existing event handlers.
  const tableContent=cloneElement(table,{},Children.map(table.props.children,child=>isValidElement(child)&&child.type==='tbody'?filteredBody:child))
  const content=nested ? cloneElement(container,{},Children.map(container.props.children,child=>isValidElement(child)&&child.type==='table'?tableContent:child)) : tableContent
  return {content,total:rows.length,visible:shown.length,valid}
}

export function SectionTableSearch({children,enabled=true}: {children:ReactElement<ElementProps>;enabled?:boolean}) {
  const workspace=useContext(WorkspaceContext)
  const universe=workspace?.state.universe
  const scope=`${workspace?.state.mode??''}:${workspace?.state.activeModuleId??''}:${universe?.level??''}:${universe?.id??''}`
  const [search,setSearch]=useState({scope,value:''})
  const query=search.scope===scope?search.value:''
  useEffect(()=>{setSearch(previous=>previous.scope===scope?previous:{scope,value:''})},[scope])
  const id=useId()
  const view=enabled?sectionTableView(children,query):null
  if(!view)return children
  return <section className="heyti-section-search">
    <div className="heyti-section-search-controls">
      <label htmlFor={id}>Buscar sección en esta tabla
        <input id={id} type="search" inputMode="numeric" maxLength={4} placeholder="Número exacto, ej. 1466" value={query} onChange={event=>setSearch({scope,value:event.target.value})}/>
      </label>
      {query?<button type="button" onClick={()=>setSearch({scope,value:''})}>Mostrar todas</button>:null}
    </div>
    <p role="status" aria-live="polite">{view.visible} de {view.total} secciones de esta tabla. El filtro no cambia el mapa ni los conteos del universo.</p>
    {!view.valid?<p>Escribe un número de sección de 1 a 4 dígitos, sin ceros iniciales.</p>:query&&view.visible===0?<p>Sin coincidencias en esta tabla. Prueba otro número o pulsa «Mostrar todas».</p>:null}
    {view.content}
  </section>
}
