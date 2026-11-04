import { createContext } from 'react'
import type {
  HeytiModuleId,
  UniverseSelection,
  WorkspaceMode,
  WorkspaceState,
} from './platform.types'

export interface WorkspaceContextValue {
  setMapView: (view: { zoom: number; x: number; y: number }) => void
  state: WorkspaceState
  selectModule: (moduleId: HeytiModuleId) => void
  selectUniverse: (
    universe: UniverseSelection | null,
  ) => void
  setMode: (mode: WorkspaceMode) => void
  setComparisonModules: (
    moduleIds: HeytiModuleId[],
  ) => void
}

export const WorkspaceContext =
  createContext<WorkspaceContextValue | null>(null)
