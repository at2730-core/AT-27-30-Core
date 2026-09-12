export type StartupStepStatus =
  | 'pending'
  | 'running'
  | 'passed'
  | 'warning'
  | 'failed'

export type PlatformStatus =
  | 'initializing'
  | 'ready'
  | 'degraded'
  | 'error'

export interface StartupStep {
  id: string
  label: string
  status: StartupStepStatus
  detail: string
}

export interface StartupState {
  platformStatus: PlatformStatus
  progress: number
  steps: StartupStep[]
  coreConnected: boolean
}
