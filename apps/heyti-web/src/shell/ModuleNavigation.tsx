import './NavigationSubmenus.css'
import './NavigationTypography.css'
import { useEffect, useState } from 'react'
import { HEYTI_MODULES } from '../platform/module.catalog'
import type { HeytiModuleId } from '../platform/platform.types'
import { useWorkspace } from '../platform/useWorkspace'
import { ModuleIcon } from './ModuleIcon'

interface ModuleNavigationProps {
  onOpenSocioQuery: (view:'indicators'|'education'|'services'|'margination'|'income'|'poverty'|'rural'|'projection') => void
  socioProjectionOpen: boolean
  socioRuralOpen: boolean
  socioPovertyOpen: boolean
  socioIncomeOpen: boolean
  socioMarginationOpen: boolean
  socioServicesOpen: boolean
  socioEducationOpen: boolean
  onOpenUniverseMap: () => void
  universeMapKind: 'leaders' | 'abstention' | 'concentration' | 'participation' | 'margin' | 'data-alerts' | 'results2024' | 'reference' | 'geographic' | 'area-comparison' | 'area-competitiveness' | 'area-top3'
  onOpenParticipationTable: () => void
  onOpenResults2024: () => void
  onOpenDataAlerts: () => void
  onOpenDistribution: () => void
  distributionOpen: boolean
  onOpenMultiScenario: () => void
  multiScenarioOpen: boolean
  onOpenSensitivity: () => void
  sensitivityOpen: boolean
  onOpenGeographic: () => void
  onOpenReference: () => void
  onOpenHistoricalMargin: () => void
  onOpenPartyComparison: () => void
  partyComparisonOpen: boolean
  onOpenParticipationGoals: () => void
  participationGoalsOpen: boolean
  onOpenStability: () => void
  stabilityOpen: boolean
  onOpenParticipationScenario: () => void
  participationScenarioOpen: boolean
  onOpenParticipation: () => void
  onOpenConcentration: () => void
  onOpenAbstention: () => void
  universeMapOpen: boolean
  onOpenTopThree: () => void
  topThreeOpen: boolean
  onOpenCompetitiveness: () => void
  competitivenessOpen: boolean
  onOpenHistoricalComparison: () => void
  historicalComparisonOpen: boolean
  activeInsightTab: number
  onSelectInsightTab: (index: number) => void
  onOpenUniverse: () => void
}

const pendingQueries: Partial<Record<HeytiModuleId, readonly string[]>> = {
  'territorial-analysis': [
    'Abstención', 'Índice de concentración 2024',
  ],
}

export function ModuleNavigation({
  onOpenSocioQuery, socioProjectionOpen, socioRuralOpen, socioPovertyOpen, socioIncomeOpen, socioMarginationOpen, socioServicesOpen, socioEducationOpen, activeInsightTab, onSelectInsightTab, onOpenUniverse, onOpenHistoricalComparison, historicalComparisonOpen, onOpenCompetitiveness, competitivenessOpen, onOpenTopThree, topThreeOpen, onOpenUniverseMap, universeMapOpen, universeMapKind, onOpenParticipationTable, onOpenResults2024, onOpenDataAlerts, onOpenDistribution, distributionOpen, onOpenMultiScenario, multiScenarioOpen, onOpenSensitivity, sensitivityOpen, onOpenGeographic, onOpenReference, onOpenHistoricalMargin, onOpenPartyComparison, partyComparisonOpen, onOpenParticipationGoals, participationGoalsOpen, onOpenStability, stabilityOpen, onOpenParticipationScenario, participationScenarioOpen, onOpenParticipation, onOpenAbstention, onOpenConcentration,
}: ModuleNavigationProps) {
  const { state, selectModule, setMapView } = useWorkspace()
  const [expandedId, setExpandedId] = useState<HeytiModuleId | null>(state.activeModuleId)
  const [openGroup, setOpenGroup] = useState<string | null>(null)
  useEffect(() => { setExpandedId(state.activeModuleId); setOpenGroup(null) }, [state.activeModuleId])
  const sharedQueries = ['Resumen de sección', 'Elección actual', 'Historial comparativo', 'Trazabilidad']

  return (
    <aside className="module-navigation">
      <div className="module-navigation-brand">
        <span className="module-navigation-mark" aria-hidden="true">H</span>
        <span><strong>HEYTI CORE</strong><small>V 2.0</small></span>
      </div>
      <p className="module-navigation-status">Plataforma operativa</p>
      <nav aria-label="Módulos HEYTI">
        <ul className="module-navigation-list">
          {HEYTI_MODULES.map(module => {
            const active = state.activeModuleId === module.id
            const expanded = expandedId === module.id
            const queries = pendingQueries[module.id] ?? []
            return (
              <li key={module.id}>
                <button type="button" className="module-navigation-button"
                  data-accent={module.accentKey} data-active={active}
                  aria-current={active ? 'page' : undefined}
                  aria-expanded={expanded} aria-controls={`queries-${module.id}`}
                  onClick={() => {
                    setOpenGroup(null)
                    if (active) setExpandedId(expanded ? null : module.id)
                    else { selectModule(module.id); setExpandedId(module.id) }
                  }}>
                  <span className="heyti-module-icon"><ModuleIcon moduleId={module.id} /></span>
                  <span className="module-navigation-label">{module.label}</span>
                  <span className="heyti-module-chevron" aria-hidden="true">{expanded ? '⌄' : '›'}</span>
                </button>
                <div id={`queries-${module.id}`} className="heyti-module-queries" hidden={!expanded}>
                  {module.id === 'territorial-analysis' ? <>
                  <button type="button" className="heyti-submenu-toggle" aria-expanded={openGroup === `${module.id}:section`} aria-controls={`section-queries-${module.id}`} onClick={() => setOpenGroup(current => current === `${module.id}:section` ? null : `${module.id}:section`)}><span>Sección · contexto compartido</span><span aria-hidden="true">{openGroup === `${module.id}:section` ? '⌄' : '›'}</span></button>
                  <div id={`section-queries-${module.id}`} className="heyti-submenu-content" hidden={openGroup !== `${module.id}:section`}>
                  <ul aria-label={`Contexto de sección en ${module.label}`}>
                    <li><button type="button" onClick={onOpenUniverse}>Seleccionar sección</button></li>
                    {sharedQueries.map((label, index) => (
                      <li key={label}><button type="button"
                        disabled={state.mode === 'comparison'}
                        aria-current={active && activeInsightTab === index ? 'true' : undefined}
                        title={state.mode === 'comparison' ? 'Disponible en modo Individual' : undefined}
                        onClick={() => onSelectInsightTab(index)}>{label}</button></li>
                    ))}
                    <li><button type="button" onClick={() => setMapView({ zoom: 1, x: 0, y: 0 })}>Recentrar mapa</button></li>
                  </ul>
                  </div>
                  </> : null}
                  <button type="button" className="heyti-submenu-toggle" aria-expanded={openGroup === `${module.id}:module`} aria-controls={`module-queries-${module.id}`} onClick={() => setOpenGroup(current => current === `${module.id}:module` ? null : `${module.id}:module`)}><span>Consultas del módulo</span><span aria-hidden="true">{openGroup === `${module.id}:module` ? '⌄' : '›'}</span></button>
                  <div id={`module-queries-${module.id}`} className="heyti-submenu-content" hidden={openGroup !== `${module.id}:module`}>
                  {module.id === 'socioeconomic' ? <ul aria-label="Consultas disponibles de Socioeconómico"><li><button type="button" disabled={state.mode === 'comparison'} aria-current={!socioEducationOpen && !socioServicesOpen && !socioMarginationOpen && !socioIncomeOpen && !socioPovertyOpen && !socioRuralOpen && !socioProjectionOpen ? 'true' : undefined} onClick={()=>onOpenSocioQuery('indicators')}>Indicadores generales · 14 indicadores</button></li><li><button type="button" disabled={state.mode === 'comparison'} aria-current={socioEducationOpen ? 'true' : undefined} onClick={()=>onOpenSocioQuery('education')}>Rezago educativo · perfil 2020</button></li><li><button type="button" disabled={state.mode === 'comparison'} aria-current={socioServicesOpen ? 'true' : undefined} onClick={()=>onOpenSocioQuery('services')}>Acceso a servicios · viviendas 2020</button></li><li><button type="button" disabled={state.mode === 'comparison'} aria-current={socioMarginationOpen ? 'true' : undefined} onClick={()=>onOpenSocioQuery('margination')}>Marginación urbana · AGEB 2020</button></li><li><button type="button" disabled={state.mode === 'comparison'} aria-current={socioIncomeOpen ? 'true' : undefined} onClick={()=>onOpenSocioQuery('income')}>Ingreso estimado · municipios 2024</button></li><li><button type="button" disabled={state.mode === 'comparison'} aria-current={socioPovertyOpen ? 'true' : undefined} onClick={()=>onOpenSocioQuery('poverty')}>Pobreza · CONEVAL 2020 e historial</button></li><li><button type="button" disabled={state.mode === 'comparison'} aria-current={socioRuralOpen ? 'true' : undefined} onClick={()=>onOpenSocioQuery('rural')}>Tipo urbano-rural · secciones</button></li><li><button type="button" disabled={state.mode === 'comparison'} aria-current={socioProjectionOpen ? 'true' : undefined} onClick={()=>onOpenSocioQuery('projection')}>Proyección 2027 · escenarios</button></li></ul> : null}
                  {module.id === 'territorial-analysis' ? (
                    <ul aria-label="Consultas disponibles de Análisis Territorial">
                      <li><button type="button" disabled={state.mode === 'comparison'} aria-current={universeMapOpen && universeMapKind === 'results2024' ? 'true' : undefined} onClick={onOpenResults2024}>Top 20 Secciones</button></li>
                      <li><button type="button" disabled={state.mode === 'comparison'}
                        aria-current={historicalComparisonOpen ? 'true' : undefined}
                        onClick={onOpenHistoricalComparison}>Comparativa</button></li>
                      <li><button type="button" disabled={state.mode === 'comparison'} aria-current={competitivenessOpen ? 'true' : undefined} onClick={onOpenCompetitiveness}>Competitividad</button></li>
                      <li><button type="button" disabled={state.mode === 'comparison'} aria-current={topThreeOpen ? 'true' : undefined} onClick={onOpenTopThree}>Top 3</button></li>
                      <li><button type="button" disabled={state.mode === 'comparison'} aria-current={universeMapOpen && universeMapKind === 'leaders' ? 'true' : undefined} onClick={onOpenUniverseMap}>Ganadores por año</button></li>
                      <li><button type="button" disabled={state.mode === 'comparison'} aria-current={universeMapOpen && universeMapKind === 'abstention' ? 'true' : undefined} onClick={onOpenAbstention}>Abstención</button></li>
                      <li><button type="button" disabled={state.mode === 'comparison'} aria-current={universeMapOpen && universeMapKind === 'concentration' ? 'true' : undefined} onClick={onOpenConcentration}>Índice de concentración 2024</button></li>
                    </ul>
                  ) : null}
                  {module.id === 'win-all' ? <ul aria-label="Consultas disponibles de Ganar Todo">
                    <li><button type="button" disabled={state.mode === 'comparison'} onClick={onOpenParticipationTable}>Participación estimada 3%...</button></li>
                    <li><button type="button" disabled={state.mode === 'comparison'} aria-current={universeMapOpen && universeMapKind === 'participation' ? 'true' : undefined} onClick={onOpenParticipation}>Participación histórica</button></li>
                    <li><button type="button" disabled={state.mode === 'comparison'} aria-current={participationScenarioOpen ? 'true' : undefined} onClick={onOpenParticipationScenario}>Escenario de participación 2027</button></li>
                    <li><button type="button" disabled={state.mode === 'comparison'} aria-current={stabilityOpen ? 'true' : undefined} onClick={onOpenStability}>Estabilidad 2018–2024</button></li>
                    <li><button type="button" disabled={state.mode === 'comparison'} aria-current={participationGoalsOpen ? 'true' : undefined} onClick={onOpenParticipationGoals}>Metas de participación 2027</button></li>
                    <li><button type="button" disabled={state.mode === 'comparison'} aria-current={partyComparisonOpen ? 'true' : undefined} onClick={onOpenPartyComparison}>Escenario descriptivo 2027 · votos y participación</button></li>
                    <li><button type="button" disabled={state.mode === 'comparison'} aria-current={universeMapOpen && universeMapKind === 'margin' ? 'true' : undefined} onClick={onOpenHistoricalMargin}>Diferencia entre partidos · 2024</button></li>
                    <li><button type="button" disabled={state.mode === 'comparison'} aria-current={universeMapOpen && universeMapKind === 'data-alerts' ? 'true' : undefined} onClick={onOpenDataAlerts}>Alertas de datos · 2024</button></li>
                    <li><button type="button" disabled={state.mode === 'comparison'} aria-current={universeMapOpen && universeMapKind === 'reference' ? 'true' : undefined} onClick={onOpenReference}>Eficiencia del voto · histórica 2024</button></li>
                    <li><button type="button" disabled={state.mode === 'comparison'} aria-current={universeMapOpen && universeMapKind === 'geographic' ? 'true' : undefined} onClick={onOpenGeographic}>Colindancias y agrupaciones</button></li>
                    <li><button type="button" disabled={state.mode === 'comparison'} aria-current={sensitivityOpen ? 'true' : undefined} onClick={onOpenSensitivity}>Sensibilidad a participación</button></li>
                    <li><button type="button" disabled={state.mode === 'comparison'} aria-current={multiScenarioOpen ? 'true' : undefined} onClick={onOpenMultiScenario}>Comparador de escenarios de participación</button></li>
                    <li><button type="button" disabled={state.mode === 'comparison'} aria-current={distributionOpen ? 'true' : undefined} onClick={onOpenDistribution}>Distribución de votación por sección</button></li>
                  </ul> : null}
                  {queries.length > 0 ? (
                    <ul aria-label={`Consultas pendientes de ${module.label}`}>
                      {queries.filter(label => !(module.id === 'territorial-analysis' && ['Abstención','Índice de concentración 2024'].includes(label))).map(label => (
                        <li key={label}><button type="button" disabled title="Pendiente de integración en HEYTI V2">
                          <span>{label}</span><small>Pendiente</small>
                        </button></li>
                      ))}
                    </ul>
                  ) : ['win-all','socioeconomic'].includes(module.id) ? null : <p className="heyti-query-pending-note">Pendientes de integración.</p>}
                  </div>
                </div>
              </li>
            )
          })}
        </ul>
      </nav>
      <div className="module-navigation-footer">
        <span aria-hidden="true" /><span><strong>Runtime</strong><small>Estado disponible en diagnóstico</small></span>
      </div>
    </aside>
  )
}
