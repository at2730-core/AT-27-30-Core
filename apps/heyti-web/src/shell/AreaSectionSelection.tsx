import { createContext, useCallback, useContext, useLayoutEffect, useMemo, useState } from 'react'
import type { ReactNode } from 'react'
import type { UniverseMap } from '../gateway/universe.client'
import type { AreaSectionSelection } from './areaSectionSelectionState'
import { clearAreaSource, selectAreaSection, selectionForScope } from './areaSectionSelectionState'
import { FloatingInsightPanel } from './FloatingInsightPanel'
import { SectionDemoPanel, SectionDemoProvider } from './SectionDemoPanel'
import { SectionInsightTabs } from './SectionInsightTabs'

interface AreaSelectionContext {
  selection: AreaSectionSelection | null
  select: (map: UniverseMap, id: string) => void
  clearSource: (map: UniverseMap) => void
}
const Context = createContext<AreaSelectionContext>({selection:null, select:()=>{}, clearSource:()=>{}})
export const useAreaSectionSelection = () => useContext(Context)

// One owner per visible map. Replacing or clearing a result invalidates its
// detail; another map's late cleanup cannot clear a newer selection.
export function useAreaSectionSource(map: UniverseMap | null | undefined) {
  const {selection, select, clearSource} = useAreaSectionSelection()
  useLayoutEffect(() => {
    if (map) return () => clearSource(map)
  }, [map, clearSource])
  return {
    selectedSection: map && selection?.map === map ? selection.sectionId : null,
    selectSection: (id: string) => { if (map) select(map, id) },
  }
}

function AreaSectionSummary({selection}: {selection: AreaSectionSelection}) {
  const [tab, setTab] = useState(0)
  return <FloatingInsightPanel title="Resumen de sección" minimizable initiallyExpanded expandRequest={selection.request}>
    <div className="workspace-insight-result" style={{gridTemplateColumns: 'minmax(0, 1fr)'}} >
    <p className="heyti-overview-note">Sección <strong>{selection.sectionId}</strong> seleccionada dentro de {selection.map.universe.label}. La consulta del universo se conserva. Esta ficha muestra datos electorales históricos; los escenarios 2027 permanecen en su consulta.</p>
    <SectionDemoProvider key={selection.sectionId} sectionId={selection.sectionId}>
      <SectionInsightTabs electionYear={2024} selectedIndex={tab} onSelectedIndexChange={setTab}
        summary={<SectionDemoPanel view="summary" />}
        current={<SectionDemoPanel key={`current:${selection.map.contest}`} view="current" initialContest={selection.map.contest} />}
        history={<SectionDemoPanel key={`history:${selection.map.contest}`} view="history" initialContest={selection.map.contest} />}
        trace={<SectionDemoPanel view="trace" />} />
    </SectionDemoProvider>
    </div>
  </FloatingInsightPanel>
}

export function AreaSectionSelectionProvider({scope, visible, children}: {scope:string; visible:boolean; children:ReactNode}) {
  const [stored, setStored] = useState<AreaSectionSelection | null>(null)
  const selection = selectionForScope(stored, scope)
  // Discard old scope state, so returning to a previous query cannot resurrect
  // its selection without a new click.
  useLayoutEffect(() => { setStored(previous => selectionForScope(previous, scope)) }, [scope])
  const select = useCallback((map:UniverseMap, id:string) => {
    setStored(previous => selectAreaSection(previous, map, id, scope))
  }, [scope])
  const clearSource = useCallback((map:UniverseMap) => {
    setStored(previous => clearAreaSource(previous, map))
  }, [])
  const value = useMemo(() => ({selection, select, clearSource}), [selection, select, clearSource])
  return <Context.Provider value={value}>{children}{visible && selection ? <AreaSectionSummary selection={selection} /> : null}</Context.Provider>
}
