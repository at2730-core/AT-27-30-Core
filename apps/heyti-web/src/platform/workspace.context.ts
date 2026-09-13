import { createContext } from 'react'
import type {
  HeytiModuleId,
  UniverseSelection,
  WorkspaceMode,
  WorkspaceState,
} from './platform.types'

export interface WorkspaceContextValue {
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
