export type HeytiModuleId =
  | 'territorial-analysis'
  | 'win-all'
  | 'field'
  | 'election-day'
  | 'et-27'
  | 'socioeconomic'

export type WorkspaceMode =
  | 'individual'
  | 'comparison'

export type UniverseLevel =
  | 'country'
  | 'state'
  | 'municipality'
  | 'federal-district'
  | 'local-district'
  | 'section'

export type DataTruthStatus =
  | 'certified'
  | 'pending'
  | 'unavailable'

export interface HeytiModuleDefinition {
  id: HeytiModuleId
  code: string
  label: string
  shortLabel: string
  description: string
  accentKey: string
}

export interface UniverseSelection {
  id: string
  label: string
  level: UniverseLevel
  parentId: string | null
  truthStatus: DataTruthStatus
}

export interface WorkspaceState {
  activeModuleId: HeytiModuleId
  mode: WorkspaceMode
  universe: UniverseSelection | null
  comparisonModuleIds: HeytiModuleId[]
}
