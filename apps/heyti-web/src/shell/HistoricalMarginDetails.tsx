import { SectionTableSearch } from './SectionTableSearch'
import { useAreaSectionSelection } from './AreaSectionSelection'
import './WinScenarioTable.css'
import { historicalMargin } from './historicalMargin'
import type { UniverseMap } from '../gateway/universe.client'
import { useWorkspace } from '../platform/useWorkspace'
import { fitUniverseSection } from './MapSectionFocus'
export function HistoricalMarginDetails({result}:{result:UniverseMap}) {
 const {select}=useAreaSectionSelection()
 const {setMapView}=useWorkspace(), rows=result.sections.map(s=>({id:s.sectionId,total:s.total,...historicalMargin(s)}))
 return <section className="heyti-data-panel">
  <header className="heyti-data-panel-header">
   <h3>Diferencia histórica 2024 · lectura parcial</h3>
   <span className="heyti-data-panel-badge">Histórico</span>
  </header>
  <p>{rows.filter(r=>r.votes!==null).length} secciones calculables, incluidas las empatadas. No calcula votos necesarios ni probabilidades futuras.</p>
  <p className="heyti-overview-note">Diferencia = primer máximo − segundo máximo entre PAN, PRI, PVEM y MORENA. Puntos porcentuales = diferencia / votos totales de la contienda × 100. El total incluye más que esos cuatro partidos. En empate máximo, diferencia cero; no se asigna un ganador. Sin votos rastreados no se calcula.</p>
  <p className="heyti-overview-note">Azul más intenso indica una diferencia porcentual mayor; empate en morado; no calculables conservan su categoría. Es una escala descriptiva continua, sin semáforo ni clasificación estratégica.</p>
  <SectionTableSearch><div className="heyti-win-table-scroll" tabIndex={0} role="region" aria-label="Diferencias históricas por sección"><table className="heyti-win-table heyti-section-table"><thead><tr>{['Sección','Primer máximo rastreado','Votos primer máximo','Segundo máximo rastreado','Votos segundo máximo','Total de la contienda','Diferencia en votos','Diferencia (pp)','Estado'].map(k=><th scope="col" key={k}>{k}</th>)}</tr></thead><tbody>{rows.sort((a,b)=>Number(a.id)-Number(b.id)).map(row=><tr data-section-id={row.id} key={row.id} onClick={()=>{const view=fitUniverseSection(result,row.id);if(view){select(result,row.id);setMapView(view)}}}><th scope="row"><button type="button" aria-label={`Acercar sección ${row.id}`}>{row.id}</button></th><td>{row.first.join(' / ')||'N/D'}</td><td>{row.firstVotes??'N/D'}</td><td>{row.votes===0?'Empate en máximo':row.second.join(' / ')||'N/D'}</td><td>{row.secondVotes??'N/D'}</td><td>{row.total??'N/D'}</td><td>{row.votes??'N/D'}</td><td>{row.pp===null?'N/D':row.pp.toFixed(3)}</td><td>{row.votes===null?`No calculable: ${row.status}`:row.status==='TIE'?'Empate rastreado':'Diferencia histórica calculable'}</td></tr>)}</tbody></table></div></SectionTableSearch>
  <p>Orden por sección; pulsa una fila para acercar el mapa y pasa el puntero sobre la geometría para ver su diferencia.</p>
 </section>
}
