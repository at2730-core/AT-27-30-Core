import type {
  StartupState,
  StartupStep,
  StartupStepStatus,
} from './startup.types'

type StateListener = (state: StartupState) => void

interface CheckResult {
  status: Extract<StartupStepStatus, 'passed' | 'warning'>
  detail: string
}

const initialSteps: StartupStep[] = [
  {
    id: 'web-runtime',
    label: 'Interfaz local',
    status: 'pending',
    detail: 'Esperando validación.',
  },
  {
    id: 'local-storage',
    label: 'Almacenamiento operativo',
    status: 'pending',
    detail: 'Esperando validación.',
  },
  {
    id: 'core-gateway',
    label: 'Conexión con HEYTI-CORE',
    status: 'pending',
    detail: 'Esperando validación.',
  },
]

function updateStep(
  state: StartupState,
  index: number,
  status: StartupStepStatus,
  detail: string,
): StartupState {
  const steps = state.steps.map((step, stepIndex) =>
    stepIndex === index ? { ...step, status, detail } : step,
  )

  return {
    ...state,
    steps,
    progress: Math.round(((index + 1) / steps.length) * 100),
  }
}

function validateWebRuntime(): CheckResult {
  const available =
    typeof window !== 'undefined' &&
    typeof document !== 'undefined'

  if (!available) {
    throw new Error('El entorno web no está disponible.')
  }

  return {
    status: 'passed',
    detail: 'Interfaz web disponible.',
  }
}

function validateLocalStorage(): CheckResult {
  const key = 'heyti.startup.check'

  try {
    window.localStorage.setItem(key, 'ok')
    window.localStorage.removeItem(key)

    return {
      status: 'passed',
      detail: 'Almacenamiento local disponible.',
    }
  } catch {
    return {
      status: 'warning',
      detail: 'Almacenamiento local no disponible.',
    }
  }
}

async function validateCoreGateway(): Promise<CheckResult> {
  const gatewayUrl =
    import.meta.env.VITE_HEYTI_GATEWAY_URL?.trim()

  if (!gatewayUrl) {
    return {
      status: 'warning',
      detail: 'Transporte CORE pendiente de configuración.',
    }
  }

  const controller = new AbortController()
  const timeout = window.setTimeout(
    () => controller.abort(),
    3000,
  )

  try {
    const baseUrl = gatewayUrl.replace(/\/+$/, '')
    const response = await fetch(`${baseUrl}/health`, {
      headers: {
        Accept: 'application/json',
      },
      signal: controller.signal,
    })

    if (!response.ok) {
      return {
        status: 'warning',
        detail: `CORE respondió con estado ${response.status}.`,
      }
    }

    const payload: unknown = await response.json()
    const healthy =
      typeof payload === 'object' &&
      payload !== null &&
      'status' in payload &&
      payload.status === 'OK'

    return healthy
      ? {
          status: 'passed',
          detail: 'HEYTI-CORE disponible.',
        }
      : {
          status: 'warning',
          detail: 'CORE respondió sin contrato de salud válido.',
        }
  } catch {
    return {
      status: 'warning',
      detail: 'HEYTI-CORE no está disponible.',
    }
  } finally {
    window.clearTimeout(timeout)
  }
}

export async function runStartupChecks(
  notify: StateListener,
): Promise<StartupState> {
  let state: StartupState = {
    platformStatus: 'initializing',
    progress: 0,
    steps: initialSteps.map((step) => ({ ...step })),
    coreConnected: false,
  }

  notify(state)

  const checks = [
    () => Promise.resolve(validateWebRuntime()),
    () => Promise.resolve(validateLocalStorage()),
    validateCoreGateway,
  ]

  try {
    for (let index = 0; index < checks.length; index += 1) {
      state = updateStep(
        state,
        index,
        'running',
        'Verificando...',
      )
      notify(state)

      const result = await checks[index]()
      state = updateStep(
        state,
        index,
        result.status,
        result.detail,
      )
      notify(state)
    }
  } catch (error) {
    const detail =
      error instanceof Error
        ? error.message
        : 'Error de inicialización no identificado.'

    state = {
      ...state,
      platformStatus: 'error',
      steps: state.steps.map((step) =>
        step.status === 'running'
          ? { ...step, status: 'failed', detail }
          : step,
      ),
    }

    notify(state)
    return state
  }

  const coreConnected =
    state.steps.find((step) => step.id === 'core-gateway')
      ?.status === 'passed'

  const degraded = state.steps.some(
    (step) => step.status === 'warning',
  )

  state = {
    ...state,
    platformStatus: degraded ? 'degraded' : 'ready',
    coreConnected,
  }

  notify(state)
  return state
}
