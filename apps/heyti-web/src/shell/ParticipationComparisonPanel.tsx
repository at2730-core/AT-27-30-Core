import { SectionTableSearch } from './SectionTableSearch'
import { useEffect, useRef, useState } from 'react'
import { useWorkspace } from '../platform/useWorkspace'
import { fetchUniverseCatalog, fetchUniverseMap } from '../gateway/universe.client'
import type { UniverseOption } from '../gateway/universe.client'
import { ELECTORAL_CONTEST_IDS } from '../gateway/electoral.response'
import type { ElectoralContestId } from '../gateway/electoral.response'
import type { ParticipationScenario } from './participationScenario'
import { buildParticipationComparison, comparisonPoints, selectParticipationComparison } from './participationComparison'
import { COMPARISON_PARTIES } from './partyComparison'
import './WinScenarioTable.css'
const num=(n:number|null|undefined)=>n==null?'N/D':n.toLocaleString('es-MX',{maximumFractionDigits:3})
const signed=(n:number|null)=>n==null?'N/D':(n>0?'+':'')+num(n)
const label=(delta:number)=>delta===0?'Base (0 pp)':signed(delta)+' pp'
const contests={A:'Ayuntamiento',DL:'Diputación local',DF:'Diputación federal',G:'Gubernatura',S:'Senaduría',P:'Presidencia'}
const reason=(value:string)=>({NO_DATA:'Históricos insuficientes',INCONSISTENT:'Cifras inconsistentes',ZERO_TOTAL:'Total histórico cero',NOT_CONTESTED:'Contienda no celebrada'}[value]??'Datos insuficientes')

export function ParticipationComparisonDetails({result,selectedSection,onSelectSection,onSelectScenario}:{result:ParticipationScenario;selectedSection?:string|null;onSelectSection?:(id:string)=>void;onSelectScenario?:(delta:number)=>void}){
 const comparison=result.participationComparison!, points=comparisonPoints(result), variants=comparison.scenarios
 const historicalRows=new Map(result.base.sections.map(s=>[s.sectionId,s]))
 const rows=Object.keys(result.rows).sort((a,b)=>Number(a)-Number(b))
 const selected=selectedSection?result.rows[selectedSection]:null
 const available=points.filter((p):p is typeof p & {percent:number;total:number}=>p.percent!==null&&p.total!==null)
 const xmin=Math.min(...available.map(p=>p.percent)), xmax=Math.max(...available.map(p=>p.percent))
 const ymin=Math.min(...available.map(p=>p.total)), ymax=Math.max(...available.map(p=>p.total))
 const x=(v:number)=>70+(xmax===xmin?0.5:(v-xmin)/(xmax-xmin))*570
 const y=(v:number)=>185-(ymax===ymin?0.5:(v-ymin)/(ymax-ymin))*135
 return <section className="heyti-data-panel">
  <h3>Comparador de escenarios de participación · 2027 hipotético</h3>
  <p>{result.base.universe.label} · {contests[result.base.contest]}. {rows.length} secciones representadas; {result.base.coverage.blocked} bloqueadas sin geometría publicada. Todos los escenarios utilizan la misma cobertura calculable.</p>
  <p>Mapa activo: <strong>{label(comparison.activeDelta)}</strong>. Colores por cambio de volumen frente a la base: azul aumento, ocre disminución, gris sin cambio o no calculable. Cambiar el escenario del mapa conserva todas las columnas de comparación.</p>
  <label className="workspace-electoral-comparison-control"><span>Escenario que se muestra en el mapa</span><select value={comparison.activeDelta} onChange={e=>onSelectScenario?.(Number(e.target.value))}>{comparison.deltas.map(d=><option key={d} value={d}>{label(d)}</option>)}</select></label>
  <h4>Participación frente a volumen total estimado</h4>
  <p>Resumen complementario de las secciones calculables: participación ponderada = suma de totales estimados redondeados / suma de LN 2024. No se suman porcentajes locales. La curva conecta únicamente los escenarios calculados; no expresa probabilidades ni un intervalo de confianza.</p>
  {available.length?<figure style={{margin:0}}><svg role="img" aria-label="Participación ponderada frente al total estimado: valores en la tabla de escenarios" viewBox="0 0 700 245" style={{width:'100%',height:'auto',maxHeight:300,background:'#fff',color:'#182334'}}>
   <line x1="70" y1="185" x2="655" y2="185" stroke="#526173"/><line x1="70" y1="35" x2="70" y2="185" stroke="#526173"/>
   <polyline points={available.map(p=>x(p.percent)+','+y(p.total)).join(' ')} fill="none" stroke="#4058b5" strokeWidth="2"/>
   {available.map(p=><g key={p.delta}><circle cx={x(p.percent)} cy={y(p.total)} r={comparison.activeDelta===p.delta?7:4} fill="#4058b5"><title>{label(p.delta)+': '+num(p.percent)+'%; '+num(p.total)+' votos estimados'}</title></circle><text x={x(p.percent)} y={y(p.total)-13} fontSize="11" textAnchor="middle" fill="#182334">{label(p.delta)}</text></g>)}
   <text x="70" y="205" fontSize="11" fill="#182334">{num(xmin)}%</text><text x="640" y="205" textAnchor="end" fontSize="11" fill="#182334">{num(xmax)}%</text>
   <text x="75" y="25" fontSize="12" fill="#182334">Total estimado: {num(ymin)} a {num(ymax)}</text><text x="355" y="232" textAnchor="middle" fontSize="12" fill="#182334">Participación ponderada (%)</text>
  </svg><figcaption>Valores exactos y cobertura en la siguiente tabla.</figcaption></figure>:<p role="status">Gráfica no calculable: sin secciones con volumen estimable. Las filas se conservan.</p>}
  <div className="heyti-win-table-scroll" tabIndex={0} role="region" aria-label="Resumen de todos los escenarios"><table className="heyti-win-table"><thead><tr>{['Escenario','Participación ponderada (%)','Total estimado','Cambio frente a base','Secciones calculables / representadas','LN de cobertura calculable','Secciones limitadas a 0–100%','Mostrar mapa'].map(t=><th key={t} scope="col">{t}</th>)}</tr></thead><tbody>{points.map((point,i)=><tr key={point.delta}><th scope="row">{label(point.delta)}</th><td>{num(point.percent)}</td><td>{num(point.total)}</td><td>{signed(point.valid?variants[i].sensitivity!.modifiedTotal-variants[i].sensitivity!.baseTotal:null)}</td><td>{point.valid} / {rows.length}</td><td>{point.valid?num(point.nominal):'N/D'}</td><td>{point.valid?point.limited:'N/D'}</td><td><button type="button" aria-pressed={comparison.activeDelta===point.delta} onClick={()=>onSelectScenario?.(point.delta)}>Ver {label(point.delta)}</button></td></tr>)}</tbody></table></div>
  <h4>Tabla completa por sección y escenario</h4>
  <p>Orden por sección. Cada escenario conserva participación, volumen, cambio respecto a base, desglose y residuo. Los valores N/D son faltantes o no calculables; los ceros se conservan. Usa el desplazamiento horizontal para revisar todas las columnas.</p>
  <SectionTableSearch><div className="heyti-win-table-scroll" tabIndex={0} role="region" aria-label="Comparación completa por sección y todos los escenarios"><table className="heyti-win-table heyti-section-table"><thead><tr>{['Sección','LN base 2024','Total observado 2024',...COMPARISON_PARTIES.map(p=>p+': observado 2024'),...variants.flatMap(v=>{const l=label(v.sensitivity!.delta);return ['Participación (%)','Variación aplicada (pp)','Total estimado','Cambio de volumen',...COMPARISON_PARTIES.map(p=>p+': estimado / cambio vs base'),'Residuo estimado','Estado del volumen y desglose','Límite 0–100%'].map(t=>l+' · '+t)})].map(t=><th key={t} scope="col">{t}</th>)}</tr></thead><tbody>{rows.map(id=>{
   const base=result.sensitivity!.rows[id], historical=historicalRows.get(id)
   return <tr data-section-id={id} key={id} aria-selected={selectedSection===id} onClick={()=>onSelectSection?.(id)}><th scope="row"><button type="button" aria-label={'Ver comparación de sección '+id}>{id}</button></th><td>{num(base.nominal)}</td><td>{num(historical?.total)}</td>{COMPARISON_PARTIES.map(p=><td key={p}>{num(base.before.historical[p])}</td>)}{variants.map(v=>{const row=v.sensitivity!.rows[id];return <ScenarioCells key={v.sensitivity!.delta} row={row}/>})}</tr>
  })}</tbody></table></div></SectionTableSearch>
  {selected&&selectedSection?<section className="heyti-data-panel-detail"><h4>Detalle sección {selectedSection} · históricos utilizados</h4><p>Años usados: {selected.years.join(', ')||'Ninguno'}. Participación base: {num(selected.percent)}%. {selected.clamped?'La base ya estaba limitada a 0–100%.':''}</p><div className="heyti-win-table-scroll" tabIndex={0} role="region" aria-label="Históricos de la sección seleccionada"><table className="heyti-win-table"><thead><tr><th>Año</th><th>Total observado</th><th>LN histórica</th><th>Participación (%)</th></tr></thead><tbody>{selected.history?.map(h=><tr key={h.year}><th scope="row">{h.year}</th><td>{num(h.total)}</td><td>{num(h.nominal)}</td><td>{num(h.percent)}</td></tr>)}</tbody></table></div><p>La fila seleccionada muestra simultáneamente los valores de todos los escenarios.</p></section>:<p>Selecciona una sección en tabla o mapa para consultar sus históricos.</p>}
  <details><summary>Supuestos, límites y fuentes</summary><p>Variación común en puntos porcentuales sobre el escenario histórico base. +2 pp significa pasar de 50% a 52%, antes del límite 0–100%. El escenario base 0 pp se incluye siempre y los duplicados se reúnen. No se estiman crecimiento nominal ni cambios de preferencias; LN fija 2024 y proporciones 2024 constantes. Desglose parcial de PAN, PRI, PVEM y MORENA; residuo no identificado como partido.</p><p>{result.method}. {result.reducedSections} bases usan solo dos años en contiendas trienales; {result.clampedSections} bases ya estaban limitadas. Los totales se redondean por sección; desglose por restos mayores y desempate fijo PAN, PRI, PVEM, MORENA y residuo. Un total calculable no se elimina por falta de desglose. Total histórico cero no permite inventar proporciones. El año hipotético 2027 no acredita celebración de la contienda.</p><p>Los escenarios no asignan votos a un partido, no seleccionan territorios ni calculan cambios de ganador. Fuentes en auditoría; geometría actual. Se requiere comprobar comparabilidad territorial histórica; no es un pronóstico certificado.</p><dl>{Object.entries(result.base.provenance).map(([k,v])=><div key={k}><dt>{k}</dt><dd style={{overflowWrap:'anywhere'}}>{v}</dd></div>)}</dl></details>
 </section>
}
function ScenarioCells({row}:{row:import('./participationSensitivity').SensitivityRow}){
 return <><td>{num(row.modifiedPercent)}</td><td>{signed(row.appliedPP)}</td><td>{num(row.modifiedTotal)}</td><td>{signed(row.difference)}</td>{COMPARISON_PARTIES.map(p=><td key={p}>{num(row.after.estimated?.[p])} / {signed(row.before.estimated&&row.after.estimated?row.after.estimated[p]-row.before.estimated[p]:null)}</td>)}<td>{num(row.after.residual)}</td><td>{row.modifiedTotal===null?reason(row.status):'Volumen calculable'}; {row.after.estimated?'desglose calculable':reason(row.after.status)}</td><td>{row.modifiedTotal===null?'N/D':row.limited?'Sí':'Sin recorte'}</td></>
}
export function ParticipationComparisonPanel({result,onResult,onPending,selectedSection,onSelectSection}:{result:ParticipationScenario|null;onResult:(s:ParticipationScenario)=>void;onPending:()=>void;selectedSection?:string|null;onSelectSection?:(id:string)=>void}){
 const {state}=useWorkspace()
 const [catalog,setCatalog]=useState<UniverseOption[]>([])
 const [choice,setChoice]=useState(result?result.base.universe.level+':'+result.base.universe.id:state.universe&&state.universe.level!=='section'?state.universe.level+':'+state.universe.id:'state:11')
 const [contest,setContest]=useState<ElectoralContestId>(result?.base.contest??'A')
 const [variations,setVariations]=useState<string[]>(result?.participationComparison?.deltas.filter(d=>d!==0).map(String)??['-4','4'])
 const [loading,setLoading]=useState(false),[error,setError]=useState<string|null>(null)
 const controller=useRef<AbortController|null>(null)
 useEffect(()=>{const abort=new AbortController();fetchUniverseCatalog(abort.signal).then(setCatalog).catch(e=>{if(!abort.signal.aborted)setError(String(e))});return()=>{abort.abort();controller.current?.abort()}},[])
 async function query(){
  const universe=catalog.find(u=>u.level+':'+u.id===choice)
  const deltas=variations.map(Number)
  if(!universe||variations.some(v=>!v.trim())||deltas.some(d=>!Number.isFinite(d)||d< -8||d>8||!Number.isInteger(d*2))||deltas.every(d=>d===0)){setError('Elige universo y variaciones entre −8 y +8 pp, en pasos de 0.5; al menos una debe ser distinta de cero.');return}
  controller.current?.abort();const abort=new AbortController();controller.current=abort;setLoading(true);setError(null);onPending()
  try{const maps=await Promise.all([...([2018,2021,2024].map(year=>fetchUniverseMap(universe,year,contest,abort.signal,'abstention'))),fetchUniverseMap(universe,2024,contest,abort.signal,'concentration')]);if(!abort.signal.aborted)onResult(buildParticipationComparison(maps,deltas))}
  catch(e){if(!abort.signal.aborted){setError(e instanceof Error?e.message:'Comparación no disponible.');abort.abort();setLoading(false)}}finally{if(!abort.signal.aborted)setLoading(false)}
 }
 const currentDeltas=[...new Set([0,...variations.map(Number)])].sort((a,b)=>a-b)
 const stale=result&&(choice!==result.base.universe.level+':'+result.base.universe.id||contest!==result.base.contest||variations.some(v=>!v.trim())||JSON.stringify(currentDeltas)!==JSON.stringify(result.participationComparison!.deltas))
 return <section style={{padding:'20px 16px'}}><h3>Comparador de escenarios de participación</h3><p>Compara de dos a cinco escenarios simultáneamente, incluida la base 0 pp. Elige hasta cuatro variaciones comunes; no son incrementos dirigidos a partidos o secciones.</p><label className="workspace-electoral-comparison-control"><span>Universo</span><select disabled={loading} value={choice} onChange={e=>setChoice(e.target.value)}>{catalog.map(u=><option key={u.level+':'+u.id} value={u.level+':'+u.id}>{u.label} · {u.sections} secciones</option>)}</select></label><label className="workspace-electoral-comparison-control"><span>Contienda</span><select disabled={loading} value={contest} onChange={e=>setContest(e.target.value as ElectoralContestId)}>{ELECTORAL_CONTEST_IDS.map(c=><option key={c} value={c}>{contests[c]}</option>)}</select></label>
  {variations.map((v,i)=><div key={i}><label className="workspace-electoral-comparison-control"><span>Variación {i+1} (puntos porcentuales)</span><input type="number" min="-8" max="8" step="0.5" disabled={loading} value={v} onChange={e=>setVariations(values=>values.map((x,j)=>i===j?e.target.value:x))}/></label><button type="button" disabled={loading||variations.length===1} onClick={()=>setVariations(values=>values.filter((_,j)=>j!==i))}>Quitar variación {i+1}</button></div>)}
  <button type="button" disabled={loading||variations.length>=4} onClick={()=>setVariations(v=>[...v,'2'])}>Añadir variación</button><p>La base se añade automáticamente. Variaciones repetidas se muestran una sola vez. Cambiar parámetros requiere volver a calcular; cambiar el escenario del mapa utiliza el último cálculo.</p>
  <button type="button" className="workspace-action" disabled={loading||!catalog.length} onClick={()=>void query()}>{loading?'Consultando históricos…':'Comparar escenarios y pintar mapa'}</button>{loading?<p role="status">Puedes cerrar la consulta para cancelar.</p>:null}{error?<p role="alert">{error}</p>:null}{stale?<p role="status">Los parámetros cambiaron: tabla y mapa conservan la comparación anterior. Vuelve a calcular para actualizarlos.</p>:null}{result?.participationComparison?<ParticipationComparisonDetails result={result} selectedSection={selectedSection} onSelectSection={onSelectSection} onSelectScenario={delta=>onResult(selectParticipationComparison(result,delta))}/>:null}</section>
}
