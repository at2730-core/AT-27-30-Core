import type {
  AuthenticatedUser,
} from '../gateway/auth.client'
import type { AreaKind } from './territorialAreaAnalysis'
import { ContextQueryDialog } from './ContextQueryDialog'
import { availableCrossQueries, scopeKey } from './contextQueries'
import type { CrossQueryId } from './contextQueries'
import { readVersionedElectoral } from '../gateway/electoral.versioned'
import type { ElectoralStability } from './electoralStability'
import type { ParticipationScenario } from './participationScenario'
import {
  useState,
} from 'react'
import type {
  FormEvent,
} from 'react'
import './ApplicationShell.css'
import type { UniverseMap } from '../gateway/universe.client'
import {
  readElectoralResults,
} from '../gateway/electoral.response'
import type {
  ElectoralResultsView,
} from '../gateway/electoral.response'
import {
  describeSection,
} from '../gateway/heyti.client'
import {
  readTerritorialGeometry,
} from '../gateway/territorial.geometry'
import type {
  TerritorialGeometryView,
} from '../gateway/territorial.geometry'
import {
  readTerritorialTruth,
} from '../gateway/territorial.response'
import type {
  TerritorialTruthView,
} from '../gateway/territorial.response'
import { useWorkspace } from '../platform/useWorkspace'
import { WorkspaceProvider } from '../platform/WorkspaceProvider'
import { ModuleNavigation } from './ModuleNavigation'
import { WorkspaceCanvas } from './WorkspaceCanvas'
import { WorkspaceHeader } from './WorkspaceHeader'

type OpenPanel =
  | 'universe'
  | 'cross-query'
  | 'comparison'
  | null

interface ApplicationShellProps {
  user: AuthenticatedUser
  logoutPending: boolean
  logoutError: string | null
  onLogout: () => Promise<void>
}

function ApplicationShellContent({
  user,
  logoutPending,
  logoutError,
  onLogout,
}: ApplicationShellProps) {
  const {
    selectUniverse, state, selectModule, setMode,
  } = useWorkspace()

  const [stability, setStability] = useState<ElectoralStability | null>(null)
  const [stabilityOpen, setStabilityOpen] = useState(false)
  const [scenarioKind, setScenarioKind] = useState<'scenario' | 'goals' | 'win' | 'comparison' | 'participation-table' | 'sensitivity' | 'distribution' | 'multi-scenario'>('scenario')
  const [participationScenario, setParticipationScenario] = useState<ParticipationScenario | null>(null)
  const [participationScenarioOpen, setParticipationScenarioOpen] = useState(false)
  const [activeQuery, setActiveQuery] = useState('summary')
  const [socioQueryRequest,setSocioQueryRequest] = useState(0)
  const [universeMapKind, setUniverseMapKind] = useState<'leaders' | 'abstention' | 'concentration' | 'participation' | 'margin' | 'data-alerts' | 'results2024' | 'reference' | 'geographic' | 'area-comparison' | 'area-competitiveness' | 'area-top3'>('leaders')
  const [mapResults2024, setMapResults2024] = useState(false)
  const [mapDataAlerts, setMapDataAlerts] = useState(false)
  const [mapHistoricalMargin, setMapHistoricalMargin] = useState(false)
  const [mapParticipation, setMapParticipation] = useState(false)
  const [universeMapOpen, setUniverseMapOpen] = useState(false)
  const [universeMap, setUniverseMap] = useState<UniverseMap | null>(null)
  const [topThreeOpen, setTopThreeOpen] = useState(false)
  const [competitivenessOpen, setCompetitivenessOpen] = useState(false)
  const [historicalComparisonOpen, setHistoricalComparisonOpen] = useState(false)

  const [insightPanelRequest, setInsightPanelRequest] = useState(0)
  const [activeInsightTab, setActiveInsightTab] = useState(0)

  const [openPanel, setOpenPanel] =
    useState<OpenPanel>(null)
  const [sectionInput, setSectionInput] =
    useState('')
  const [territorialTruth, setTerritorialTruth] =
    useState<TerritorialTruthView | null>(null)
  const [
    territorialGeometry,
    setTerritorialGeometry,
  ] = useState<TerritorialGeometryView | null>(null)
  const [electoralResults, setElectoralResults] =
    useState<ElectoralResultsView | null>(null)
  const [territorialLoading, setTerritorialLoading] =
    useState(false)
  const [territorialError, setTerritorialError] =
    useState<string | null>(null)

  const closePanel = () => {
    if (!territorialLoading) {
      setOpenPanel(null)
    }
  }

  const handleUniverseSubmit = async (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault()

    const requestedSectionId = sectionInput.trim()

    setStabilityOpen(false)
    setStability(null)
    setParticipationScenarioOpen(false)
    setParticipationScenario(null)
    setUniverseMapOpen(false)
    setUniverseMap(null)
    setTerritorialTruth(null)
    setTerritorialGeometry(null)
    setElectoralResults(null)
    setTerritorialLoading(true)
    setTerritorialError(null)

    try {
      const response = await describeSection(
        requestedSectionId,
      )
      const truth = readTerritorialTruth(
        response,
        requestedSectionId,
      )
      const geometry = readTerritorialGeometry(
        response,
        requestedSectionId,
      )
      readVersionedElectoral(response)
      const electoral = readElectoralResults(
        response,
      )
      if (electoral !== null) throw new Error("La consulta versionada no admite resultados del maestro anterior.")

      if (
        truth.truthStatus !== 'certified' &&
        (
          geometry !== null ||
          electoral !== null
        )
      ) {
        throw new Error(
          'HEYTI rechazó contenido de dominio sin autorización.',
        )
      }

      setTerritorialTruth(truth)
      setTerritorialGeometry(geometry)
      setElectoralResults(electoral)
      selectUniverse({
        id: truth.sectionId,
        label: `Sección ${truth.sectionId}`,
        level: 'section',
        parentId: null,
        truthStatus: truth.truthStatus,
      })
      setSectionInput(truth.sectionId)
      setOpenPanel(null)
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : 'No fue posible consultar la sección.'

      setTerritorialTruth(null)
      setTerritorialGeometry(null)
      setElectoralResults(null)
      setTerritorialError(message)
    } finally {
      setTerritorialLoading(false)
    }
  }

  const openTerritorialArea = (kind: AreaKind, query: string) => {
    setStabilityOpen(false); setParticipationScenarioOpen(false)
    setTopThreeOpen(false); setCompetitivenessOpen(false); setHistoricalComparisonOpen(false)
    setUniverseMap(null); setMapResults2024(false); setMapDataAlerts(false); setMapHistoricalMargin(false); setMapParticipation(false)
    setActiveQuery(query); setUniverseMapKind(kind); setUniverseMapOpen(true)
  }

  const launchCrossQuery = (id: CrossQueryId) => {
    const entry = availableCrossQueries(state.universe).find(query => query.id === id)
    if (!entry || entry.scope !== 'area') return
    setMode('individual')
    selectModule(entry.module)
    setStabilityOpen(false)
    setParticipationScenarioOpen(false)
    setTopThreeOpen(false)
    setCompetitivenessOpen(false)
    setHistoricalComparisonOpen(false)
    if (entry.module === 'socioeconomic') {
      setUniverseMapOpen(false)
      setActiveQuery(entry.id)
      setSocioQueryRequest(n => n + 1)
    } else if (entry.id === 'results2024' || entry.id === 'leaders' || entry.id === 'participation') {
      setUniverseMap(null)
      setActiveQuery(entry.id)
      setUniverseMapKind(entry.id)
      setUniverseMapOpen(true)
    }
    setOpenPanel(null)
  }

  return (
    <div className="application-shell">
      <ModuleNavigation
        onOpenParticipationTable={() => { setStabilityOpen(false); setActiveQuery('participation-table'); setUniverseMapOpen(false); setScenarioKind('participation-table'); setParticipationScenarioOpen(true) }}
        onOpenResults2024={() => { setParticipationScenarioOpen(false); setStabilityOpen(false); setTopThreeOpen(false); setCompetitivenessOpen(false); setHistoricalComparisonOpen(false); setUniverseMap(null); setActiveQuery('results2024'); setUniverseMapKind('results2024'); setUniverseMapOpen(true) }}
        onOpenDataAlerts={() => { setParticipationScenarioOpen(false); setStabilityOpen(false); setActiveQuery('data-alerts'); setUniverseMapKind('data-alerts'); setUniverseMapOpen(true) }}
        socioProjectionOpen={activeQuery === 'socio-projection'}
        socioRuralOpen={activeQuery === 'socio-rural'}
        socioPovertyOpen={activeQuery === 'socio-poverty'}
        socioIncomeOpen={activeQuery === 'socio-income'}
        socioMarginationOpen={activeQuery === 'socio-margination'}
        socioServicesOpen={activeQuery === 'socio-services'}
        socioEducationOpen={activeQuery === 'socio-education'}
        onOpenSocioQuery={view => { setActiveQuery(view === 'projection' ? 'socio-projection' : view === 'rural' ? 'socio-rural' : view === 'poverty' ? 'socio-poverty' : view === 'income' ? 'socio-income' : view === 'margination' ? 'socio-margination' : view === 'education' ? 'socio-education' : view === 'services' ? 'socio-services' : 'socio-indicators'); setSocioQueryRequest(n => n + 1) }}
        onOpenDistribution={() => { setStabilityOpen(false); setActiveQuery('distribution-scenario'); setUniverseMapOpen(false); setScenarioKind('distribution'); setParticipationScenarioOpen(true) }}
        onOpenSensitivity={() => { setStabilityOpen(false); setActiveQuery('participation-sensitivity'); setUniverseMapOpen(false); setScenarioKind('sensitivity'); setParticipationScenarioOpen(true) }}
        onOpenMultiScenario={() => { setStabilityOpen(false); setActiveQuery('participation-comparison'); setUniverseMapOpen(false); setScenarioKind('multi-scenario'); setParticipationScenarioOpen(true) }}
        onOpenReference={() => { setParticipationScenarioOpen(false); setStabilityOpen(false); setActiveQuery('historical-reference'); setUniverseMapKind('reference'); setUniverseMapOpen(true) }}
        onOpenGeographic={() => { setParticipationScenarioOpen(false); setStabilityOpen(false); setActiveQuery('geographic-groups'); setUniverseMapKind('geographic'); setUniverseMapOpen(true) }}
        onOpenHistoricalMargin={() => { setParticipationScenarioOpen(false); setStabilityOpen(false); setActiveQuery('historical-margin'); setUniverseMapKind('margin'); setUniverseMapOpen(true) }}
        distributionOpen={participationScenarioOpen && scenarioKind === 'distribution'}
        multiScenarioOpen={participationScenarioOpen && scenarioKind === 'multi-scenario'}
        sensitivityOpen={participationScenarioOpen && scenarioKind === 'sensitivity'}
        partyComparisonOpen={participationScenarioOpen && scenarioKind === 'comparison'}
        onOpenPartyComparison={() => { setStabilityOpen(false); setActiveQuery('party-comparison'); setUniverseMapOpen(false); setScenarioKind('comparison'); setParticipationScenarioOpen(true) }}
        participationGoalsOpen={participationScenarioOpen && scenarioKind === 'goals'}
        onOpenParticipationGoals={() => { setStabilityOpen(false); setActiveQuery('participation-goals'); setUniverseMapOpen(false); setScenarioKind('goals'); setParticipationScenarioOpen(true) }}
        stabilityOpen={stabilityOpen}
        onOpenStability={() => { setActiveQuery('stability'); setUniverseMapOpen(false); setParticipationScenarioOpen(false); setStabilityOpen(true) }}
        participationScenarioOpen={participationScenarioOpen && scenarioKind === 'scenario'}
        onOpenParticipationScenario={() => { setStabilityOpen(false); setScenarioKind('scenario'); setActiveQuery('participation-scenario'); setUniverseMapOpen(false); setParticipationScenarioOpen(true) }}
        universeMapOpen={universeMapOpen}
        universeMapKind={universeMapKind}
        onOpenParticipation={() => { setParticipationScenarioOpen(false); setStabilityOpen(false); setActiveQuery('participation'); setUniverseMapKind('participation'); setUniverseMapOpen(true) }}
        onOpenConcentration={() => { setParticipationScenarioOpen(false); setStabilityOpen(false); setUniverseMap(null); setActiveQuery('concentration'); setUniverseMapKind('concentration'); setUniverseMapOpen(true) }}
        onOpenAbstention={() => { setParticipationScenarioOpen(false); setStabilityOpen(false); setUniverseMap(null); setActiveQuery('abstention'); setUniverseMapKind('abstention'); setUniverseMapOpen(true) }}
        onOpenUniverseMap={() => { setParticipationScenarioOpen(false); setStabilityOpen(false); setUniverseMap(null); setActiveQuery('leaders'); setUniverseMapKind('leaders'); setUniverseMapOpen(true) }}
        topThreeOpen={topThreeOpen || (universeMapOpen && universeMapKind === 'area-top3')}
        onOpenTopThree={() => openTerritorialArea('area-top3', 'top3')}
        competitivenessOpen={competitivenessOpen || (universeMapOpen && universeMapKind === 'area-competitiveness')}
        onOpenCompetitiveness={() => openTerritorialArea('area-competitiveness', 'competitiveness')}
        historicalComparisonOpen={historicalComparisonOpen || (universeMapOpen && universeMapKind === 'area-comparison')}
        onOpenHistoricalComparison={() => openTerritorialArea('area-comparison', 'comparison')}
        activeInsightTab={activeInsightTab}
        onSelectInsightTab={index => { setActiveQuery(['summary', 'current', 'history', 'trace'][index] ?? 'summary'); setActiveInsightTab(index); setInsightPanelRequest(current => current + 1) }}
        onOpenUniverse={() => {
          setTerritorialError(null)
          setOpenPanel('universe')
        }}
      />

      <div className="application-workspace">
        <WorkspaceHeader
          user={user}
          logoutPending={logoutPending}
          logoutError={logoutError}
          onLogout={onLogout}
          onOpenCrossQuery={() => setOpenPanel('cross-query')}
          onOpenUniverseSelector={() => {
            setTerritorialError(null)
            setOpenPanel('universe')
          }}
        />

        <WorkspaceCanvas
          stability={stability}
          stabilityOpen={stabilityOpen}
          onCloseStability={() => setStabilityOpen(false)}
          onStabilityPending={() => { setStability(null); setParticipationScenario(null); setUniverseMap(null); setTerritorialTruth(null); setTerritorialGeometry(null); setElectoralResults(null); setTerritorialError(null) }}
          onStabilityResult={result => {
            setStability(result)
            selectUniverse({ id: result.base.universe.id, label: result.base.universe.label, level: result.base.universe.level, parentId: result.base.universe.level === 'state' ? null : '11', truthStatus: 'pending' })
          }}
          scenarioKind={scenarioKind}
          participationScenario={participationScenario}
          participationScenarioOpen={participationScenarioOpen}
          onCloseParticipationScenario={() => setParticipationScenarioOpen(false)}
          onParticipationScenarioPending={() => { setStability(null); setParticipationScenario(null); setUniverseMap(null); setTerritorialTruth(null); setTerritorialGeometry(null); setElectoralResults(null); setTerritorialError(null) }}
          onParticipationScenarioResult={result => {
            setParticipationScenario(result)
            selectUniverse({ id: result.base.universe.id, label: result.base.universe.label, level: result.base.universe.level, parentId: result.base.universe.level === 'state' ? null : '11', truthStatus: 'pending' })
          }}
          socioQueryRequest={socioQueryRequest}
          activeQuery={activeQuery}
          universeMapOpen={universeMapOpen}
          universeMapKind={universeMapKind}
          universeMap={universeMap}
          mapParticipation={mapParticipation}
          mapHistoricalMargin={mapHistoricalMargin}
          mapResults2024={mapResults2024}
          mapDataAlerts={mapDataAlerts}
          onCloseUniverseMap={() => setUniverseMapOpen(false)}
          onUniverseMapPending={() => {
            setStability(null)
            setParticipationScenario(null)
            setUniverseMap(null)
            setTerritorialTruth(null)
            setTerritorialGeometry(null)
            setElectoralResults(null)
            setTerritorialError(null)
          }}
          onUniverseMapResult={result => {
            setMapResults2024(universeMapKind === 'results2024')
            setMapDataAlerts(universeMapKind === 'data-alerts')
            setMapHistoricalMargin(universeMapKind === 'margin')
            setMapParticipation(universeMapKind === 'participation')
            setUniverseMap(result)
            selectUniverse({ id: result.universe.id, label: result.universe.label, level: result.universe.level, parentId: result.universe.level === 'state' ? null : '11', truthStatus: 'pending' })
          }}
          topThreeOpen={topThreeOpen}
          onCloseTopThree={() => setTopThreeOpen(false)}
          competitivenessOpen={competitivenessOpen}
          onCloseCompetitiveness={() => setCompetitivenessOpen(false)}
          historicalComparisonOpen={historicalComparisonOpen}
          onCloseHistoricalComparison={() => setHistoricalComparisonOpen(false)}
          insightPanelRequest={insightPanelRequest}
          activeInsightTab={activeInsightTab}
          onSelectInsightTab={index => { setActiveQuery(['summary', 'current', 'history', 'trace'][index] ?? 'summary'); setActiveInsightTab(index); setInsightPanelRequest(current => current + 1) }}
          onOpenCrossQuery={() =>
            setOpenPanel('cross-query')
          }
          onConfigureComparison={() =>
            setOpenPanel('comparison')
          }
          territorialTruth={territorialTruth}
          territorialGeometry={territorialGeometry}
          electoralResults={electoralResults}
          territorialLoading={territorialLoading}
          territorialError={territorialError}
        />
      </div>

      {openPanel === 'universe' ? (
        <div className="shell-dialog-layer">
          <section
            className="shell-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="universe-dialog-title"
          >
            <button
              type="button"
              className="shell-dialog-close"
              aria-label="Cerrar"
              disabled={territorialLoading}
              onClick={closePanel}
            >
              ×
            </button>

            <p>CONTEXTO TERRITORIAL</p>
            <h2 id="universe-dialog-title">
              Seleccionar sección
            </h2>
            <p>
              Consulta una identidad territorial contra la
              fuente certificada de Guanajuato 2023.
            </p>

            <form
              className="universe-section-form"
              onSubmit={handleUniverseSubmit}
            >
              <label htmlFor="universe-section-id">
                Número de sección
              </label>

              <input
                id="universe-section-id"
                name="section_id"
                type="text"
                inputMode="numeric"
                autoComplete="off"
                placeholder="Ejemplo: 1524"
                value={sectionInput}
                disabled={territorialLoading}
                onChange={(event) =>
                  setSectionInput(event.target.value)
                }
              />

              <button
                type="submit"
                disabled={territorialLoading}
              >
                {territorialLoading
                  ? 'Consultando...'
                  : 'Consultar en HEYTI'}
              </button>
            </form>

            {territorialError ? (
              <div
                className="shell-dialog-error"
                role="alert"
              >
                {territorialError}
              </div>
            ) : null}

            <div className="shell-dialog-notice">
              La interfaz mostrará únicamente la clasificación
              y publicación autorizadas por Data Truth.
            </div>
          </section>
        </div>
      ) : null}

      {openPanel === 'cross-query' || openPanel === 'comparison' ? (
        <ContextQueryDialog key={`${openPanel}:${scopeKey(state.universe)}`} kind={openPanel}
          onClose={() => setOpenPanel(null)} onLaunch={launchCrossQuery} />
      ) : null}
    </div>
  )
}

export function ApplicationShell(
  props: ApplicationShellProps,
) {
  return (
    <WorkspaceProvider>
      <ApplicationShellContent {...props} />
    </WorkspaceProvider>
  )
}
