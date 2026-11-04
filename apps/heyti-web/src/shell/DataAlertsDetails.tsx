import { SectionTableSearch } from './SectionTableSearch'
import { useAreaSectionSelection } from './AreaSectionSelection'
import './WinScenarioTable.css'
import {dataAlertStatus,dataAlertDetail,dataAlertLabels,dataAlertCounts} from './dataAlerts'
import type {UniverseMap} from '../gateway/universe.client'
import {useWorkspace} from '../platform/useWorkspace'
import {fitUniverseSection} from './MapSectionFocus'
const parties=['PAN','PRI','PVEM','MORENA']
const colors:Record<string,string>={AVAILABLE:'#2a9d8f',TRACKED_ZERO:'#cbd5e1',NO_DATA:'#94a3b8',ZERO_TOTAL:'#f2c85b',INCONSISTENT:'#f08a42',NOT_CONTESTED:'#e2e8f0'}
export function DataAlertsDetails({result}:{result:UniverseMap}) {
 const {select}=useAreaSectionSelection()
 const {setMapView}=useWorkspace(),counts=dataAlertCounts(result)
 return <section className="heyti-data-panel">
  <header className="heyti-data-panel-header">
   <h3>Alertas de datos · 2024</h3>
   <span className="heyti-data-panel-badge">Datos</span>
  </header>
  <p className="heyti-overview-note">Disponibilidad del total y del desglose de PAN, PRI, PVEM y MORENA. Disponible no equivale a dato electoral certificado ni a cobertura de todos los partidos. Fuentes en auditoría.</p>
  <ul style={{listStyle:'none',padding:0}}>{['AVAILABLE','TRACKED_ZERO','NO_DATA','ZERO_TOTAL','INCONSISTENT','NOT_CONTESTED'].filter(k=>counts[k]).map(k=><li key={k} style={{display:'flex',gap:8,margin:'10px 0'}}><span aria-hidden="true" style={{width:14,height:14,background:colors[k]}}/>{dataAlertLabels[k]}: <strong>{counts[k]}</strong></li>)}</ul>
  <p>{result.coverage.blocked} secciones geográficas bloqueadas no se publican en el mapa ni en esta tabla. Las identidades presentes solo en el maestro no se ubican en este universo geométrico.</p>
  <p className="heyti-overview-note">Un cero se conserva como cero. Un faltante se muestra N/D. La causa exacta de una inconsistencia requiere cotejo con la fuente. Un total cero puede coexistir con un desglose faltante; esta tabla conserva los cuatro valores para verlo. Cada alerta se revisará en la auditoría en modo usuario.</p>
  <SectionTableSearch><div className="heyti-win-table-scroll" tabIndex={0} role="region" aria-label="Alertas de datos por sección"><table className="heyti-win-table heyti-section-table"><thead><tr><th scope="col">Sección</th><th scope="col">Total 2024</th>{parties.map(p=><th scope="col" key={p}>{p}</th>)}<th scope="col">Disponibilidad</th><th scope="col">Detalle</th></tr></thead><tbody>{[...result.sections].sort((a,b)=>Number(a.sectionId)-Number(b.sectionId)).map(row=><tr data-section-id={row.sectionId} key={row.sectionId} onClick={()=>{const view=fitUniverseSection(result,row.sectionId);if(view){select(result,row.sectionId);setMapView(view)}}}><th scope="row"><button type="button" aria-label={`Acercar sección ${row.sectionId}`}>{row.sectionId}</button></th><td>{row.total??'N/D'}</td>{parties.map(p=><td key={p}>{row.votes?.[p]??'N/D'}</td>)}<td>{dataAlertLabels[dataAlertStatus(row)]}</td><td>{dataAlertDetail(row)}</td></tr>)}</tbody></table></div></SectionTableSearch>
  <p>Orden por sección. Pulsa una fila para acercar su geometría; pasa el puntero sobre el mapa para consultar el detalle.</p>
 </section>
}
