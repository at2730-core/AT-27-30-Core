import { SectionTableSearch } from './SectionTableSearch'
import { useState } from 'react'
import type { ParticipationScenario, ScenarioRow } from './participationScenario'
import './WinScenarioTable.css'

export type Participation2027SortField = 'section' | 'nominal' | 'percent' | 'total' | 'threePercent'

export function estimatedParticipationTotal(row: ScenarioRow): number | null {
 return row.reason!==null||row.percent===null||row.nominal===null||row.nominal<=0 ? null : Math.round(row.nominal*row.percent/100)
}
export function estimatedParticipationThreePercent(row: ScenarioRow): number | null {
 const total = estimatedParticipationTotal(row)
 return total===null ? null : Math.round(total * 0.03)
}

function sectionNumber(sectionId: string): number {
 const value = Number(sectionId)
 return Number.isFinite(value) ? value : Number.MAX_SAFE_INTEGER
}

export function sortParticipationRows(rows: ScenarioRow[], field: Participation2027SortField = 'section', descending = false): ScenarioRow[] {
 return [...rows].sort((a, b) => {
  const getValue = (row: ScenarioRow): number | null => {
   switch (field) {
    case 'section': return sectionNumber(row.sectionId)
    case 'nominal': return row.nominal ?? null
    case 'percent': return row.percent ?? null
    case 'total': return estimatedParticipationTotal(row)
    case 'threePercent': return estimatedParticipationThreePercent(row)
   }
  }
  const aValue = getValue(a)
  const bValue = getValue(b)
  if (aValue == null && bValue == null) return sectionNumber(a.sectionId) - sectionNumber(b.sectionId)
  if (aValue == null) return 1
  if (bValue == null) return -1
  const delta = aValue - bValue
  if (delta === 0) return sectionNumber(a.sectionId) - sectionNumber(b.sectionId)
  return (delta < 0 ? -1 : 1) * (descending ? -1 : 1)
 })
}

const num=(v:number|null)=>v===null?'N/D':v.toLocaleString('es-MX')
export function Participation2027Table({scenario,selectedSection,onSelectSection}:{scenario:ParticipationScenario;selectedSection?:string|null;onSelectSection?:(id:string)=>void}) {
 const [sortState, setSortState] = useState<{ field: Participation2027SortField; direction: 'asc' | 'desc' }>({ field: 'section', direction: 'asc' })
 const chosen=selectedSection?scenario.rows[selectedSection]:null
 const handleSort = (field: Participation2027SortField) => {
  setSortState(prev => prev.field === field ? { field, direction: prev.direction === 'asc' ? 'desc' : 'asc' } : { field, direction: 'asc' })
 }
 const orderedRows = sortParticipationRows(Object.values(scenario.rows), sortState.field, sortState.direction === 'desc')
 const renderSortButton = (field: Participation2027SortField, label: string) => {
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
 return <section className="heyti-data-panel">
  <header className="heyti-data-panel-header">
   <h3>Participación estimada 2027 por sección</h3>
   <span className="heyti-data-panel-badge">Escenario</span>
  </header>
  <p className="heyti-overview-note">Base: lista nominal de 2024; no incorpora crecimiento de la lista nominal. Total estimado = LN base × participación estimada, redondeado a votos enteros. El 3% se calcula sobre el total estimado 2027. N/D: no calculable.</p>
  <SectionTableSearch><div className="heyti-win-table-scroll" tabIndex={0} role="region" aria-label="Participación estimada 2027 por sección"><table className="heyti-win-table heyti-section-table" style={{minWidth:760}}><thead><tr><th scope="col" className={sortState.field === 'section' ? 'heyti-sort-column-active' : ''}>{renderSortButton('section', 'Sección')}</th><th scope="col" className={sortState.field === 'nominal' ? 'heyti-sort-column-active' : ''}>{renderSortButton('nominal', 'LN base 2024')}</th><th scope="col" className={sortState.field === 'percent' ? 'heyti-sort-column-active' : ''}>{renderSortButton('percent', 'Participación estimada 2027')}</th><th scope="col" className={sortState.field === 'total' ? 'heyti-sort-column-active' : ''}>{renderSortButton('total', 'Total estimado 2027')}</th><th scope="col" className={sortState.field === 'threePercent' ? 'heyti-sort-column-active' : ''}>{renderSortButton('threePercent', '3% del total estimado 2027')}</th></tr></thead><tbody>{orderedRows.map(row=><tr data-section-id={row.sectionId} key={row.sectionId} aria-selected={selectedSection===row.sectionId} onClick={()=>onSelectSection?.(row.sectionId)}><th scope="row"><button type="button" aria-label={`Acercar y consultar sección ${row.sectionId}`}>{row.sectionId}</button></th><td>{num(row.nominal)}</td><td>{row.reason===null&&row.percent!==null?`${row.percent.toFixed(3)}%`:'N/D'}</td><td>{num(estimatedParticipationTotal(row))}</td><td>{num(estimatedParticipationThreePercent(row))}</td></tr>)}</tbody></table></div></SectionTableSearch>
  {chosen?<section className="heyti-data-panel-detail"><h3>Sección {chosen.sectionId}</h3><p>LN base: {num(chosen.nominal)} · total estimado: {num(estimatedParticipationTotal(chosen))} · 3% del total estimado: {num(estimatedParticipationThreePercent(chosen))}. {chosen.reason?'No se estima con los datos disponibles.':`Años utilizados: ${chosen.years.join(', ')}.${chosen.clamped?' La estimación se limitó al rango de 0 a 100%.':''}`}</p></section>:null}
 </section>
}
