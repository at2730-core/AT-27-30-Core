import {
  useMemo,
  useReducer,
} from 'react'
import type { ReactNode } from 'react'
import { WorkspaceContext } from './workspace.context'
import {
  INITIAL_WORKSPACE_STATE,
  workspaceReducer,
} from './workspace.state'
import type {
  HeytiModuleId,
  UniverseSelection,
  WorkspaceMode,
} from './platform.types'

interface WorkspaceProviderProps {
  children: ReactNode
}

export function WorkspaceProvider({
  children,
}: WorkspaceProviderProps) {
  const [state, dispatch] = useReducer(
    workspaceReducer,
    INITIAL_WORKSPACE_STATE,
  )

  const value = useMemo(
    () => ({
      state,

      selectModule: (moduleId: HeytiModuleId) => {
        dispatch({
          type: 'select-module',
          moduleId,
        })
      },

      selectUniverse: (
        universe: UniverseSelection | null,
      ) => {
        dispatch({
          type: 'select-universe',
          universe,
        })
      },

      setMode: (mode: WorkspaceMode) => {
        dispatch({
          type: 'set-mode',
          mode,
        })
      },

      setComparisonModules: (
        moduleIds: HeytiModuleId[],
      ) => {
        dispatch({
          type: 'set-comparison-modules',
          moduleIds,
        })
      },
    }),
    [state],
  )

  return (
    <WorkspaceContext.Provider value={value}>
      {children}
    </WorkspaceContext.Provider>
  )
}
