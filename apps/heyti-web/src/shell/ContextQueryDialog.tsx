import {useEffect,useRef,useState} from 'react'
import type {ReactNode} from 'react'
import type {HeytiModuleId} from '../platform/platform.types'
import {useWorkspace} from '../platform/useWorkspace'
import {availableCrossQueries,COMPARISON_MODULES,comparisonModules,scopeKey} from './contextQueries'
import type {CrossQueryId} from './contextQueries'
import {SectionDemoProvider,SectionDemoPanel} from './SectionDemoPanel'
import './ContextQueries.css'
function Dialog({title,onClose,children}:{title:string;onClose:()=>void;children:ReactNode}) {
 const ref=useRef<HTMLElement>(null),closeRef=useRef(onClose)
 closeRef.current=onClose
 useEffect(()=>{
  const previous=document.activeElement as HTMLElement|null
  ref.current?.querySelector<HTMLButtonElement>('button')?.focus()
  const keyboard=(e:KeyboardEvent)=>{
   if(e.key==='Escape'){e.preventDefault();closeRef.current();return}
   if(e.key!=='Tab')return
   const controls=[...(ref.current?.querySelectorAll<HTMLElement>('button:not(:disabled),select:not(:disabled),input:not(:disabled),[tabindex="0"]')??[])]
   const first=controls[0],last=controls[controls.length-1]
   if(e.shiftKey&&document.activeElement===first){e.preventDefault();last?.focus()}
   else if(!e.shiftKey&&document.activeElement===last){e.preventDefault();first?.focus()}
  }
  document.addEventListener('keydown',keyboard)
  return ()=>{document.removeEventListener('keydown',keyboard);previous?.focus()}
 },[])
 return <div className="shell-dialog-layer heyti-context-layer"><section className="shell-dialog heyti-context-dialog" ref={ref} role="dialog" aria-modal="true" aria-label={title}><button type="button" className="shell-dialog-close" aria-label="Cerrar" onClick={onClose}>×</button><h2>{title}</h2>{children}</section></div>
}
export function ContextQueryDialog({kind,onClose,onLaunch}:{kind:'cross-query'|'comparison';onClose:()=>void;onLaunch:(id:CrossQueryId)=>void}) {
 const {state,setComparisonModules,setMode}=useWorkspace()
 const choices=availableCrossQueries(state.universe)
 const [selected,setSelected]=useState<string>(choices[0]?.id??'')
 const [opened,setOpened]=useState<CrossQueryId|null>(null)
 const [modules,setModules]=useState<HeytiModuleId[]>(()=>{
  try{return comparisonModules(state.comparisonModuleIds)}catch{return COMPARISON_MODULES.map(m=>m.id)}
 })
 const [error,setError]=useState<string|null>(null)
 const available=choices.find(q=>q.id===selected)
 return <Dialog title={kind==='cross-query'?'Consulta cruzada · consultas disponibles':'Configurar comparación descriptiva'} onClose={onClose}>
  <p><strong>Universo activo: {state.universe?.label??'Sin seleccionar'}</strong></p>
  {kind==='comparison'?<>
   <p>Selecciona dos o tres módulos. Cada columna conserva su fuente, año, cobertura y reservas. Vista tabular; sin cruces automáticos ni proyecciones.</p>
   <fieldset className="heyti-context-options"><legend>Módulos descriptivos</legend>{COMPARISON_MODULES.map(m=><label key={m.id}><input type="checkbox" checked={modules.includes(m.id)} onChange={e=>{setError(null);setModules(previous=>e.target.checked?[...previous,m.id]:previous.filter(id=>id!==m.id))}}/>{m.label}</label>)}</fieldset>
   {error?<p role="alert">{error}</p>:null}
   <button type="button" className="workspace-action" onClick={()=>{try{setComparisonModules(comparisonModules(modules));setMode('comparison');onClose()}catch(e){setError(e instanceof Error?e.message:'Configuración inválida.')}}}>Aplicar configuración</button>
  </>:<>
   <p>Abre una consulta descriptiva existente conservando el universo. Este selector no interpreta preguntas libres ni genera análisis automáticos.</p>
   {!choices.length?<p role="status">Selecciona primero un estado, municipio, distrito o sección mediante Universo activo.</p>:<>
    <label className="heyti-context-control">Consulta<select value={selected} onChange={e=>{setSelected(e.target.value);setOpened(null)}}>{choices.map(q=><option key={q.id} value={q.id}>{q.label}</option>)}</select></label>
    <button type="button" className="workspace-action" disabled={!available} onClick={()=>{
     if(!available)return
     if(available.scope==='section')setOpened(available.id)
     else onLaunch(available.id)
    }}>Abrir consulta</button>
    <p className="heyti-overview-note">Para estados, municipios y distritos, la consulta abre el formulario del módulo: pulsa su botón de consulta para obtener datos. Para una sección se muestran las lecturas disponibles de demostración; no se cambia a otro universo.</p>
    {opened&&state.universe?.level==='section'?<SectionDemoProvider key={`${scopeKey(state.universe)}:${opened}`} sectionId={state.universe.id}><SectionDemoPanel view={opened==='section-summary'?'summary':opened==='section-history'?'history':opened==='section-trace'?'trace':'current'}/></SectionDemoProvider>:null}
   </>}
  </>}
 </Dialog>
}
