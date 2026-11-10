import { AreaSectionSelectionProvider, useAreaSectionSelection, useAreaSectionSource } from './AreaSectionSelection'
import { TerritorialAreaPanel } from './TerritorialAreaPanel'
import { areaReading, AREA_TITLES, isAreaKind } from './territorialAreaAnalysis'
import { ComparisonWorkspace } from './ComparisonWorkspace'
import { SocioWorkspaceHost } from './SocioWorkspaceHost'
import { FieldWorkspace } from './FieldWorkspace'
import { advanceSocioScope } from './socioWorkspaceMemory'
import { VersionedElectoralPanel } from './VersionedElectoralPanel'
import { SectionDemoProvider, SectionDemoPanel } from './SectionDemoPanel'
import { ParticipationComparisonPanel } from './ParticipationComparisonPanel'
import { GeographicGroupsPanel } from './GeographicGroupsPanel'
import { geographicGroupsOf } from './geographicGroups'
import { ParticipationSensitivityPanel } from './ParticipationSensitivityPanel'
import { HistoricalReferencePanel } from './HistoricalReferencePanel'
import { referenceSettings } from './historicalReference'
import { fitUniverseSection } from './MapSectionFocus'
import { useEffect, useState } from 'react'
import { ElectoralStabilityPanel } from './ElectoralStabilityPanel'
import type { ElectoralStability } from './electoralStability'
import { ParticipationScenarioPanel } from './ParticipationScenarioPanel'
import type { ParticipationScenario } from './participationScenario'
import { queryDescriptions } from './QueryDescription'
import './MapViewport.css'
import { UniverseGeometryMap } from './UniverseGeometryMap'
import { UniverseQueryPanel } from './UniverseQueryPanel'
import type { UniverseMap } from '../gateway/universe.client'
import { SectionTopThree } from './SectionTopThree'
import { SectionCompetitiveness } from './SectionCompetitiveness'
import { SectionInsightTabs } from './SectionInsightTabs'
import { FloatingInsightPanel } from './FloatingInsightPanel'
import type {
  ElectoralResultsView,
} from '../gateway/electoral.response'
import type {
  TerritorialGeometryView,
} from '../gateway/territorial.geometry'
import type {
  TerritorialTruthView,
} from '../gateway/territorial.response'
import { getHeytiModule } from '../platform/module.catalog'
import { useWorkspace } from '../platform/useWorkspace'
import { ElectoralHistoricalComparison } from './SectionElectoralSummary'
import { SectionGeometryMap } from './SectionGeometryMap'

interface WorkspaceCanvasProps {
  socioQueryRequest?: number
  scenarioKind?: 'scenario' | 'goals' | 'win' | 'comparison' | 'participation-table' | 'sensitivity' | 'distribution' | 'multi-scenario'
  stability?: ElectoralStability | null
  stabilityOpen?: boolean
  onCloseStability?: () => void
  onStabilityPending?: () => void
  onStabilityResult?: (result: ElectoralStability) => void
  participationScenario?: ParticipationScenario | null
  participationScenarioOpen?: boolean
  onCloseParticipationScenario?: () => void
  onParticipationScenarioPending?: () => void
  onParticipationScenarioResult?: (result: ParticipationScenario) => void
  mapResults2024?: boolean
  mapDataAlerts?: boolean
  mapHistoricalMargin?: boolean
  mapParticipation?: boolean
  activeQuery?: string
  universeMapKind?: 'leaders' | 'abstention' | 'concentration' | 'participation' | 'margin' | 'data-alerts' | 'results2024' | 'reference' | 'geographic' | 'area-comparison' | 'area-competitiveness' | 'area-top3'
  universeMapOpen?: boolean
  universeMap?: UniverseMap | null
  onCloseUniverseMap?: () => void
  onUniverseMapResult?: (result: UniverseMap) => void
  onUniverseMapPending?: () => void
  topThreeOpen?: boolean
  onCloseTopThree?: () => void
  competitivenessOpen?: boolean
  onCloseCompetitiveness?: () => void
  historicalComparisonOpen?: boolean
  onCloseHistoricalComparison?: () => void
  insightPanelRequest?: number
  activeInsightTab?: number
  onSelectInsightTab?: (index: number) => void
  onOpenCrossQuery: () => void
  onConfigureComparison: () => void
  territorialTruth: TerritorialTruthView | null
  territorialGeometry: TerritorialGeometryView | null
  electoralResults: ElectoralResultsView | null
  territorialLoading: boolean
  territorialError: string | null
}

function classificationLabel(
  classification: string,
): string {
  switch (classification) {
    case 'CURRENT_TERRITORIAL_SECTION':
      return 'Sección territorial vigente'

    case 'SYNTHETIC_CANDIDATE':
      return 'Candidata sintética'

    default:
      return classification
  }
}

function publicationLabel(
  publicationStatus: string,
): string {
  switch (publicationStatus) {
    case 'ALLOWED':
      return 'Publicación permitida'

    case 'BLOCKED':
      return 'Publicación bloqueada'

    default:
      return publicationStatus
  }
}

function WorkspaceCanvasContent({
  socioQueryRequest = 0,
  scenarioKind = 'scenario',
  stability,
  stabilityOpen,
  onCloseStability,
  onStabilityPending,
  onStabilityResult,
  participationScenario,
  participationScenarioOpen,
  onCloseParticipationScenario,
  onParticipationScenarioPending,
  onParticipationScenarioResult,
  activeQuery = 'summary',
  mapResults2024 = false,
  mapDataAlerts = false,
  mapHistoricalMargin = false,
  mapParticipation = false,
  universeMapKind,
  universeMapOpen,
  universeMap,
  onCloseUniverseMap,
  onUniverseMapResult,
  onUniverseMapPending,
  topThreeOpen,
  onCloseTopThree,
  competitivenessOpen,
  onCloseCompetitiveness,
  historicalComparisonOpen,
  onCloseHistoricalComparison,
  insightPanelRequest,
  activeInsightTab,
  onSelectInsightTab,
  onOpenCrossQuery,
  onConfigureComparison,
  territorialTruth,
  territorialGeometry,
  electoralResults,
  territorialLoading,
  territorialError,
}: WorkspaceCanvasProps) {
  const { state, setMapView } = useWorkspace()
  const socioActive = state.activeModuleId === 'socioeconomic' && state.mode !== 'comparison'
  const fieldActive = state.activeModuleId === 'field' && state.mode !== 'comparison'
  const universeScope = state.universe ? `${state.universe.level}:${state.universe.id}` : 'none'
  const [socioVisited, setSocioVisited] = useState(socioActive)
  const [socioMemory, setSocioMemory] = useState({scope: universeScope, revision: 0})
  useEffect(() => {
    if (socioActive) setSocioVisited(true)
    setSocioMemory(previous => advanceSocioScope(previous, universeScope, socioActive))
  }, [universeScope, socioActive])

  const sourceMap = stability?.base ?? participationScenario?.base ?? universeMap
  const { selection: areaSelection } = useAreaSectionSelection()
  const { selectedSection: selectedAreaSection, selectSection } = useAreaSectionSource(sourceMap)
  const resultsSelected = selectedAreaSection
  const winSelected = selectedAreaSection
  const focusResultSection = (id: string) => {
    if (!universeMap) return
    const view = fitUniverseSection(universeMap, id)
    if (view) { selectSection(id); setMapView(view) }
  }
  const focusWinSection = (id: string) => {
    if (!participationScenario) return
    const view = fitUniverseSection(participationScenario.base, id)
    if (view) { selectSection(id); setMapView(view) }
  }

  const activeModule = getHeytiModule(
    state.activeModuleId,
  )

  const queryDescription = ['territorial-analysis', 'win-all'].includes(state.activeModuleId) ? queryDescriptions[activeQuery] ?? queryDescriptions.summary : activeModule.description

  const truthStatus = universeMap && areaReading(universeMap) ? `${AREA_TITLES[areaReading(universeMap)!.kind]} · ${universeMap.year} · cobertura parcial` : stability ? 'Estabilidad 2018–2024 · cobertura parcial · fuentes en auditoría' : participationScenario ? `${participationScenario.participationComparison ? 'Comparación de escenarios 2027' : participationScenario.distributionOnly ? 'Distribución estimada 2027' : participationScenario.sensitivity ? 'Sensibilidad a participación 2027' : participationScenario.comparison ? 'Comparación descriptiva 2027' : participationScenario.win ? 'Escenario parcial 2027' : participationScenario.goals ? 'Metas 2027' : 'Escenario 2027'} · estimación · fuentes en auditoría` : universeMap ? `${geographicGroupsOf(universeMap) ? 'Agrupación geográfica · datos 2024' : referenceSettings(universeMap) ? 'Comparación histórica 2024' : mapResults2024 ? 'Resultados 2024' : mapDataAlerts ? 'Alertas de datos 2024' : mapHistoricalMargin ? 'Diferencia histórica 2024' : mapParticipation ? 'Participación histórica' : universeMap.metric === 'concentration' ? 'Concentración parcial' : universeMap.metric === 'abstention' ? 'Abstención' : 'Mayor votación rastreada'} · cobertura parcial` : territorialLoading
    ? 'Consultando HEYTI-CORE'
    : territorialTruth
      ? publicationLabel(
          territorialTruth.publicationStatus,
        )
      : 'Sin datos representados'

  return (<>
    {state.mode === 'comparison' ? <ComparisonWorkspace onConfigure={onConfigureComparison} onUniverseChange={onUniverseMapPending} /> : null}
    {fieldActive ? <FieldWorkspace /> : null}
    <div style={{display: socioActive && state.mode !== 'comparison' ? 'contents' : 'none'}} aria-hidden={!socioActive || state.mode === 'comparison'}>
      {(socioVisited || socioActive) ? <SocioWorkspaceHost key={socioMemory.revision} query={activeQuery} requestId={socioQueryRequest} /> : null}
    </div>
    <div key={universeScope} style={{display: socioActive || fieldActive || state.mode === 'comparison' ? 'none' : 'contents'}} aria-hidden={socioActive || fieldActive || state.mode === 'comparison'}>
    <main className="workspace-canvas" data-map-expanded={['territorial-analysis', 'win-all'].includes(state.activeModuleId) ? 'true' : undefined}>
      {!['territorial-analysis', 'win-all'].includes(state.activeModuleId) ? (
      <section className="workspace-introduction">
        <div>
          <p className="workspace-eyebrow">
            MÓDULO {activeModule.code}
          </p>
          <h1>{activeModule.label}</h1>
          <p>{activeModule.description}</p>
        </div>

        <button
          type="button"
          className="workspace-action"
          onClick={onOpenCrossQuery}
        >
          Consulta cruzada
        </button>
      </section>
      ) : null}

      <div className="workspace-visual-grid">
        <section
          className="workspace-visual-panel"
          aria-labelledby="visual-panel-title"
        >
          <header>
            <div>
              <p>UNIVERSO SELECCIONADO</p>
              <h2 id="visual-panel-title">
                {state.universe
                  ? state.universe.label
                  : 'Universo no seleccionado'}
              </h2>
            </div>

            <span className="workspace-truth-status">
              {truthStatus}
            </span>
          </header>

          <div
            className={
              (territorialGeometry || universeMap || participationScenario || stability)
                ? 'workspace-visual-map'
                : 'workspace-visual-placeholder'
            }
          >
            {stability ? (
              <UniverseGeometryMap key={`stability:${stability.base.universe.level}:${stability.base.universe.id}:${stability.base.contest}`} result={stability.base} stability={stability} selectedSection={selectedAreaSection} onSelectSection={selectSection} queryDescription={queryDescription} />
            ) : participationScenario ? (
              <UniverseGeometryMap key={`scenario:${participationScenario.base.universe.level}:${participationScenario.base.universe.id}:${participationScenario.base.contest}`} result={participationScenario.base} scenario={participationScenario} selectedSection={selectedAreaSection} onSelectSection={selectSection} queryDescription={queryDescription} />
            ) : universeMap ? (
              <UniverseGeometryMap key={`${universeMap.universe.level}:${universeMap.universe.id}`} result={universeMap} results2024Mode={mapResults2024} selectedSection={selectedAreaSection} onSelectSection={selectSection} participation={mapParticipation} historicalMarginMode={mapHistoricalMargin} dataAlertsMode={mapDataAlerts} queryDescription={queryDescription} />
            ) : territorialGeometry ? (
              <SectionGeometryMap
                queryDescription={queryDescription}
                territorialGeometry={
                  territorialGeometry
                }
              />
            ) : (
              <>
                <span aria-hidden="true">◎</span>

                {territorialTruth ? (
                  territorialTruth.truthStatus ===
                  'unavailable' ? (
                    <>
                      <strong>
                        Identidad territorial no publicable
                      </strong>
                      <small>
                        HEYTI-CORE bloqueó su representación.
                        No se mostrará mapa, geometría ni
                        información territorial como si
                        estuviera certificada.
                      </small>
                    </>
                  ) : (
                    <>
                      <strong>
                        Geometría territorial no disponible
                      </strong>
                      <small>
                        La identidad fue consultada, pero no
                        existe una geometría autorizada para
                        representarla.
                      </small>
                    </>
                  )
                ) : (
                  <>
                    <strong>Área de visualización</strong>
                    <small>
                      Selecciona una sección para consultar su
                      identidad territorial certificada.
                    </small>
                  </>
                )}
              </>
            )}
          </div>
        </section>

        {!areaSelection ? <FloatingInsightPanel title="Resumen de sección" minimizable expandRequest={insightPanelRequest}>

          {territorialLoading ? (
            <div className="workspace-insight-empty">
              <strong>Consultando Data Truth</strong>
              <p>
                HEYTI-CORE está validando la identidad
                territorial solicitada.
              </p>
            </div>
          ) : null}

          {!territorialLoading && territorialError ? (
            <div
              className="workspace-insight-error"
              role="alert"
            >
              <strong>Consulta no disponible</strong>
              <p>{territorialError}</p>
            </div>
          ) : null}

          {!territorialLoading &&
          !territorialError &&
          territorialTruth ? (
            <div className="workspace-insight-result">
              <SectionDemoProvider key={territorialTruth.sectionId} sectionId={territorialTruth.sectionId}>
              <SectionInsightTabs
                selectedIndex={activeInsightTab}
                onSelectedIndexChange={onSelectInsightTab}
                electionYear={2024}
                summary={<>
              <div className="workspace-truth-summary">
                <span
                  data-status={
                    territorialTruth.truthStatus
                  }
                >
                  {publicationLabel(
                    territorialTruth.publicationStatus,
                  )}
                </span>
                <strong>
                  Sección {territorialTruth.sectionId}
                </strong>
                <p>
                  {classificationLabel(
                    territorialTruth.classification,
                  )}
                </p>
              </div>

                  <p className="heyti-overview-note">
                    Consulta las pestañas para revisar datos de demostración y su evolución.
                    La autorización territorial no acredita la validación de todas las cifras electorales.
                  </p>
                  <SectionDemoPanel view="summary" />
                </>}
                current={<SectionDemoPanel view="current" />}
                history={<SectionDemoPanel view="history" />}
                trace={<>
                  <SectionDemoPanel view="trace" />
                  <details><summary>Estado del lector auditado · independiente de la demostración</summary><VersionedElectoralPanel sectionId={territorialTruth.sectionId} /></details>
              <details className="heyti-trace-disclosure" open>
                <summary>Trazabilidad de la consulta territorial</summary>
                <dl className="workspace-truth-details">
                <div>
                  <dt>Clasificación</dt>
                  <dd>
                    {territorialTruth.classification}
                  </dd>
                </div>
                <div>
                  <dt>Estado de respuesta</dt>
                  <dd>
                    {territorialTruth.responseStatus}
                  </dd>
                </div>
                <div>
                  <dt>Versión de conocimiento</dt>
                  <dd>
                    {territorialTruth.knowledgeVersion ??
                      'No informada'}
                  </dd>
                </div>
                <div>
                  <dt>Solicitud</dt>
                  <dd>
                    {territorialTruth.requestId ??
                      'No informada'}
                  </dd>
                </div>
              </dl>
              </details>

              {territorialTruth.warnings.length > 0 ? (
                <section className="workspace-warning-list">
                  <h3>Advertencias</h3>
                  <ul>
                    {territorialTruth.warnings.map(
                      (warning) => (
                        <li key={warning.code}>
                          <strong>{warning.code}</strong>
                          <span>{warning.message}</span>
                        </li>
                      ),
                    )}
                  </ul>
                </section>
              ) : (
                <p className="workspace-no-warnings">
                  Sin advertencias de Data Truth.
                </p>
              )}                </>}
              />
              </SectionDemoProvider>
            </div>
          ) : null}

          {!territorialLoading &&
          !territorialError &&
          !territorialTruth ? (
            <div className="workspace-insight-empty">
              <strong>Sin lectura disponible</strong>
              <p>
                Selecciona una sección para obtener una
                respuesta autorizada de HEYTI.
              </p>
            </div>
          ) : null}
        </FloatingInsightPanel> : null}
        {stabilityOpen && onStabilityPending && onStabilityResult ? (
          <FloatingInsightPanel title="Estabilidad 2018–2024 · lectura parcial" comparative onClose={onCloseStability}>
            <ElectoralStabilityPanel result={stability ?? null} onPending={onStabilityPending} onResult={onStabilityResult} />
          </FloatingInsightPanel>
        ) : null}
        {participationScenarioOpen && onParticipationScenarioPending && onParticipationScenarioResult ? (
          <FloatingInsightPanel title={scenarioKind === 'multi-scenario' ? 'Comparador de escenarios de participación' : scenarioKind === 'distribution' ? 'Distribución de votación por sección · escenario 2027' : scenarioKind === 'sensitivity' ? 'Sensibilidad a participación · escenario 2027' : scenarioKind === 'participation-table' ? 'Tabla de participación estimada 2027' : (scenarioKind === 'comparison' || scenarioKind === 'win') ? 'Escenario descriptivo 2027 · votos y participación' : scenarioKind === 'goals' ? 'Metas de participación 2027 · escenario' : 'Escenario de participación 2027 · estimación'} comparative onClose={onCloseParticipationScenario}>
            {scenarioKind === 'multi-scenario' ? <ParticipationComparisonPanel result={participationScenario?.participationComparison ? participationScenario : null} onResult={onParticipationScenarioResult} onPending={onParticipationScenarioPending} selectedSection={winSelected} onSelectSection={focusWinSection} /> : scenarioKind === 'sensitivity' ? <ParticipationSensitivityPanel result={participationScenario?.sensitivity && !participationScenario.participationComparison ? participationScenario : null} onResult={onParticipationScenarioResult} onPending={onParticipationScenarioPending} selectedSection={winSelected} onSelectSection={focusWinSection} /> : <ParticipationScenarioPanel distributionMode={scenarioKind === 'distribution'} key={scenarioKind} tableMode={scenarioKind === 'participation-table'} comparisonMode={scenarioKind === 'comparison' || scenarioKind === 'win'} selectedSection={winSelected} onSelectSection={focusWinSection} goalsMode={scenarioKind === 'goals'} result={participationScenario && (participationScenario.participationComparison ? 'multi-scenario' : participationScenario.distributionOnly ? 'distribution' : participationScenario.sensitivity ? 'sensitivity' : participationScenario.tableOnly ? 'participation-table' : participationScenario.comparison ? 'comparison' : participationScenario.win ? 'win' : participationScenario.goals ? 'goals' : 'scenario') === (scenarioKind === 'win' ? 'comparison' : scenarioKind) ? participationScenario : null} onPending={onParticipationScenarioPending} onResult={onParticipationScenarioResult} />}
          </FloatingInsightPanel>
        ) : null}
        {universeMapOpen && onUniverseMapResult && onUniverseMapPending ? (
          <FloatingInsightPanel title={isAreaKind(universeMapKind) ? AREA_TITLES[universeMapKind] : universeMapKind === 'geographic' ? 'Colindancias y agrupaciones de secciones' : universeMapKind === 'reference' ? 'Eficiencia del voto · histórica por sección' : universeMapKind === 'results2024' ? 'Resultados 2024 por universo' : universeMapKind === 'data-alerts' ? 'Alertas de datos · 2024' : universeMapKind === 'margin' ? 'Diferencia entre partidos · 2024' : universeMapKind === 'participation' ? 'Participación histórica · Ganar Todo' : universeMapKind === 'concentration' ? 'Concentración 2024 · índice parcial' : universeMapKind === 'abstention' ? 'Abstención por universo · lectura parcial' : 'Ganadores por año · lectura parcial'} comparative onClose={onCloseUniverseMap}>
            {isAreaKind(universeMapKind) ? <TerritorialAreaPanel key={universeMapKind} kind={universeMapKind} result={universeMap && areaReading(universeMap)?.kind === universeMapKind ? universeMap : null} onResult={onUniverseMapResult} onPending={onUniverseMapPending} selectedSection={resultsSelected} onSelectSection={focusResultSection} /> : universeMapKind === 'geographic' ? <GeographicGroupsPanel result={universeMap && geographicGroupsOf(universeMap) ? universeMap : null} onResult={onUniverseMapResult} onPending={onUniverseMapPending} selectedSection={resultsSelected} onSelectSection={focusResultSection} /> : universeMapKind === 'reference' ? <HistoricalReferencePanel result={universeMap && referenceSettings(universeMap) ? universeMap : null} onResult={onUniverseMapResult} onPending={onUniverseMapPending} selectedSection={resultsSelected} onSelectSection={focusResultSection} /> : <UniverseQueryPanel key={universeMapKind} results2024Mode={universeMapKind === 'results2024'} selectedSection={resultsSelected} onSelectSection={focusResultSection} dataAlertsMode={universeMapKind === 'data-alerts'} historicalMarginMode={universeMapKind === 'margin'} participation={universeMapKind === 'participation'} metric={(universeMapKind === 'concentration' || universeMapKind === 'margin' || universeMapKind === 'data-alerts' || universeMapKind === 'results2024') ? 'concentration' : (universeMapKind === 'participation' || universeMapKind === 'abstention') ? 'abstention' : 'leaders'} result={universeMap && !areaReading(universeMap) && (universeMap.metric ?? 'leaders') === ((universeMapKind === 'margin' || universeMapKind === 'data-alerts' || universeMapKind === 'results2024') ? 'concentration' : universeMapKind === 'participation' ? 'abstention' : universeMapKind) && mapParticipation === (universeMapKind === 'participation') && mapHistoricalMargin === (universeMapKind === 'margin') && mapDataAlerts === (universeMapKind === 'data-alerts') && mapResults2024 === (universeMapKind === 'results2024') ? universeMap : null} onResult={onUniverseMapResult} onPending={onUniverseMapPending} />}
          </FloatingInsightPanel>
        ) : null}
        {topThreeOpen ? (
          <FloatingInsightPanel title="Top 3 por puesto" comparative onClose={onCloseTopThree}>
            <div style={{ padding: '20px 16px' }}>
              {territorialLoading ? <p role="status">Consultando la sección en HEYTI-CORE…</p>
                : territorialError ? <p role="alert">{territorialError}</p>
                : territorialTruth?.truthStatus === 'certified' && territorialTruth.publicationStatus === 'ALLOWED'
                  && electoralResults && electoralResults.sectionId === territorialTruth.sectionId
                  ? <SectionTopThree key={electoralResults.sectionId} electoralResults={electoralResults} />
                  : <p>Selecciona y consulta una sección para revisar sus partidos rastreados.</p>}
            </div>
          </FloatingInsightPanel>
        ) : null}
        {competitivenessOpen ? (
          <FloatingInsightPanel title="Competitividad por puesto" comparative onClose={onCloseCompetitiveness}>
            <div style={{ padding: '20px 16px' }}>
              {territorialLoading ? <p role="status">Consultando la sección en HEYTI-CORE…</p>
                : territorialError ? <p role="alert">{territorialError}</p>
                : territorialTruth?.truthStatus === 'certified' && territorialTruth.publicationStatus === 'ALLOWED'
                  && electoralResults && electoralResults.sectionId === territorialTruth.sectionId
                  ? <SectionCompetitiveness key={electoralResults.sectionId} electoralResults={electoralResults} />
                  : <p>Selecciona y consulta una sección para revisar su competitividad.</p>}
            </div>
          </FloatingInsightPanel>
        ) : null}
        {historicalComparisonOpen ? (
          <FloatingInsightPanel title="Comparativa histórica por puesto" comparative onClose={onCloseHistoricalComparison}>
            <div className="heyti-independent-comparison">
              {territorialLoading ? <p role="status">Consultando la sección en HEYTI-CORE…</p>
                : territorialError ? <p role="alert">{territorialError}</p>
                : territorialTruth?.truthStatus === 'certified' && territorialTruth.publicationStatus === 'ALLOWED'
                  && electoralResults && electoralResults.sectionId === territorialTruth.sectionId ? <>
                    <h3>Sección {territorialTruth.sectionId}</h3>
                    <p className="heyti-overview-note">PAN, PRI, PVEM y MORENA: cobertura parcial. Los datos faltantes no equivalen a cero. La autorización territorial no acredita la validación de todas las cifras electorales.</p>
                    <ElectoralHistoricalComparison key={electoralResults.sectionId} electoralResults={electoralResults} independent />
                  </> : <p>Selecciona y consulta una sección para comparar sus resultados históricos disponibles.</p>}
            </div>
          </FloatingInsightPanel>
        ) : null}
      </div>
    </main>
    </div>
  </>)
}

export function WorkspaceCanvas(props: WorkspaceCanvasProps) {
  const { state } = useWorkspace()
  const universe = state.universe ? `${state.universe.level}:${state.universe.id}` : 'none'
  const scope = `${state.mode}:${state.activeModuleId}:${universe}:${props.activeQuery ?? 'summary'}`
  return <AreaSectionSelectionProvider scope={scope} visible={state.mode !== 'comparison'}>
    <WorkspaceCanvasContent {...props} />
  </AreaSectionSelectionProvider>
}
