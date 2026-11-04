import {
  DEFAULT_MODULE_ID,
} from './module.catalog'
import type {
  HeytiModuleId,
  UniverseSelection,
  WorkspaceMode,
  WorkspaceState,
} from './platform.types'

export const MAX_COMPARISON_MODULES = 3

export const INITIAL_WORKSPACE_STATE: WorkspaceState = {
  activeModuleId: DEFAULT_MODULE_ID,
  mode: 'individual',
  universe: null,
  mapView: { zoom: 1, x: 0, y: 0 },
  comparisonModuleIds: [],
}

export type WorkspaceAction =
  | { type: 'set-map-view'; view: { zoom: number; x: number; y: number } }
  | {
      type: 'select-module'
      moduleId: HeytiModuleId
    }
  | {
      type: 'select-universe'
      universe: UniverseSelection | null
    }
  | {
      type: 'set-mode'
      mode: WorkspaceMode
    }
  | {
      type: 'set-comparison-modules'
      moduleIds: HeytiModuleId[]
    }

export function workspaceReducer(
  state: WorkspaceState,
  action: WorkspaceAction,
): WorkspaceState {
  switch (action.type) {
    case 'set-map-view':
      return { ...state, mapView: action.view }

    case 'select-module':
      return {
        ...state,
        activeModuleId: action.moduleId,
      }

    case 'select-universe':
      return {
        ...state,
        universe: action.universe,
        mapView: state.universe?.id === action.universe?.id && state.universe?.level === action.universe?.level
          ? state.mapView : { zoom: 1, x: 0, y: 0 },
      }

    case 'set-mode':
      return {
        ...state,
        mode: action.mode,
      }

    case 'set-comparison-modules':
      return {
        ...state,
        comparisonModuleIds: [
          ...new Set(action.moduleIds),
        ].slice(0, MAX_COMPARISON_MODULES),
      }

    default:
      return state
  }
}
