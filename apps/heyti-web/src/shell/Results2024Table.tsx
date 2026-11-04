import { SectionTableSearch } from './SectionTableSearch'
import { useState } from 'react'
import type { UniverseMap } from '../gateway/universe.client'
import { orderSections2024, type Results2024SortField } from './results2024'
import './WinScenarioTable.css'

const parties=['PAN','PRI','PVEM','MORENA'] as const
const num=(v:number|null|undefined)=>v==null?'N/D':v.toLocaleString('es-MX')
const percent=(v:number|null|undefined)=>v==null?'N/D':`${v.toFixed(3)}%`

export function Results2024Table({result,selectedSection,onSelectSection}:{result:UniverseMap;selectedSection?:string|null;onSelectSection?:(id:string)=>void}) {
 const [sortState, setSortState] = useState<{ field: Results2024SortField; direction: 'asc' | 'desc' }>({ field: 'section', direction: 'asc' })
 const selected=result.sections.find(s=>s.sectionId===selectedSection)
 const extra=selected?result.results2024?.[selected.sectionId]:null

 const handleSort = (field: Results2024SortField) => {
  setSortState(prev => prev.field === field
   ? { field, direction: prev.direction === 'asc' ? 'desc' : 'asc' }
   : { field, direction: 'asc' })
 }

 const orderedSections = orderSections2024(result.sections, sortState.direction === 'desc', sortState.field, result.results2024 ?? {})

 const renderSortButton = (field: Results2024SortField, label: string) => {
  const isActive = sortState.field === field
  const direction = isActive ? sortState.direction : null
  return (
   <button
    type="button"
    className={isActive ? 'heyti-sort-button heyti-sort-button-active' : 'heyti-sort-button'}
    data-direction={direction ?? 'none'}
    onClick={() => handleSort(field)}
    aria-label={`${label}${isActive ? `, orden ${direction === 'asc' ? 'ascendente' : 'descendente'}` : ', ordenar'}`}
   >
    <span>{label}</span>
    <span className="heyti-sort-indicator" aria-hidden="true">{isActive ? (direction === 'asc' ? '↑' : '↓') : '↕'}</span>
   </button>
  )
 }

 return <>
  <p>Resultados de 2024. Pulsa una fila para acercar el mapa y consultar su detalle. N/D significa dato no disponible; cero conserva el valor del archivo.</p>
  <SectionTableSearch><div className="heyti-win-table-scroll" tabIndex={0} role="region" aria-label="Resultados 2024 por sección"><table className="heyti-win-table heyti-section-table"><caption>{result.universe.label} · 2024</caption><thead><tr><th scope="col" aria-sort={sortState.field === 'section' ? (sortState.direction === 'asc' ? 'ascending' : 'descending') : 'none'} className={sortState.field === 'section' ? 'heyti-sort-column-active' : ''}>{renderSortButton('section', 'Sección')}</th><th scope="col" aria-sort={sortState.field === 'nominal' ? (sortState.direction === 'asc' ? 'ascending' : 'descending') : 'none'} className={sortState.field === 'nominal' ? 'heyti-sort-column-active' : ''}>{renderSortButton('nominal', 'Lista nominal')}</th><th scope="col" aria-sort={sortState.field === 'participation' ? (sortState.direction === 'asc' ? 'ascending' : 'descending') : 'none'} className={sortState.field === 'participation' ? 'heyti-sort-column-active' : ''}>{renderSortButton('participation', 'Participación')}</th><th scope="col" aria-sort={sortState.field === 'total' ? (sortState.direction === 'asc' ? 'ascending' : 'descending') : 'none'} className={sortState.field === 'total' ? 'heyti-sort-column-active' : ''}>{renderSortButton('total', 'Total de votos')}</th>{parties.map(p => <th scope="col" key={p} aria-sort={sortState.field === p ? (sortState.direction === 'asc' ? 'ascending' : 'descending') : 'none'} className={sortState.field === p ? 'heyti-sort-column-active' : ''}>{renderSortButton(p, p)}</th>)}<th scope="col">Datos</th></tr></thead><tbody>{orderedSections.map(s => {const e=result.results2024?.[s.sectionId];return <tr data-section-id={s.sectionId} key={s.sectionId} aria-selected={selectedSection===s.sectionId} onClick={()=>onSelectSection?.(s.sectionId)}><th scope="row"><button type="button" aria-label={`Acercar y consultar sección ${s.sectionId}`}>{s.sectionId}</button></th><td>{num(e?.nominal)}</td><td>{percent(e?.participation)}</td><td>{num(s.total)}</td>{parties.map(p=><td key={p}>{num(s.votes?.[p])}</td>)}<td>{s.status==='INCONSISTENT'?'Cifras por revisar':s.total===0?'Total en cero':s.total==null||parties.some(p=>s.votes?.[p]==null)||e?.nominal==null?'Datos incompletos':'Disponibles · sin certificar'}</td></tr>})}</tbody></table></div></SectionTableSearch>
  {selected?<section><h3>Sección {selected.sectionId} · 2024</h3><p>Lista nominal: {num(extra?.nominal)} · participación: {percent(extra?.participation)} · total de votos: {num(selected.total)}.</p><table style={{width:'100%'}}><thead><tr><th>Partido</th><th>Votos 2024</th></tr></thead><tbody>{parties.map(p=><tr key={p}><th scope="row">{p}</th><td>{num(selected.votes?.[p])}</td></tr>)}</tbody></table></section>:null}
  <details className="heyti-trace-disclosure"><summary>Información de los datos</summary><p>Fuentes pendientes de auditoría. Solo se desglosan PAN, PRI, PVEM y MORENA; el total puede incluir otros participantes y tipos de voto. La participación se calcula con total y lista nominal disponibles, sin rellenar faltantes. Municipios y distritos corresponden a la geometría actual. Orden disponible por sección, lista nominal, participación, total de votos y partido, con dirección ascendente o descendente como en Excel. No hay proyecciones, selección de las primeras 20 ni clasificación de prioridades.</p></details>
 </>
}
