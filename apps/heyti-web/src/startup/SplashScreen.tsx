import { useEffect, useState } from 'react'
import { runStartupChecks } from './runStartupChecks'
import type {
  StartupState,
  StartupStepStatus,
} from './startup.types'
import './SplashScreen.css'

interface SplashScreenProps {
  onEnter: () => void
}

const statusLabels: Record<StartupStepStatus, string> = {
  pending: 'Pendiente',
  running: 'Verificando',
  passed: 'Correcto',
  warning: 'Atención',
  failed: 'Error',
}

const minimumDisplayTime = 1800

export function SplashScreen({
  onEnter,
}: SplashScreenProps) {
  const [state, setState] = useState<StartupState | null>(
    null,
  )
  const [canContinue, setCanContinue] = useState(false)
  const [attempt, setAttempt] = useState(0)

  useEffect(() => {
    let active = true
    let continueTimer: number | undefined
    const startedAt = window.performance.now()

    void runStartupChecks((nextState) => {
      if (active) {
        setState(nextState)
      }
    }).then((result) => {
      if (!active) {
        return
      }

      const elapsed = window.performance.now() - startedAt
      const remaining = Math.max(
        0,
        minimumDisplayTime - elapsed,
      )

      continueTimer = window.setTimeout(() => {
        if (active && result.platformStatus !== 'error') {
          setCanContinue(true)
        }
      }, remaining)
    })

    return () => {
      active = false

      if (continueTimer !== undefined) {
        window.clearTimeout(continueTimer)
      }
    }
  }, [attempt])

  const progress = state?.progress ?? 0
  const platformStatus =
    state?.platformStatus ?? 'initializing'

  const statusMessage = {
    initializing: 'Inicializando plataforma...',
    ready: 'Plataforma lista.',
    degraded:
      'Plataforma disponible con capacidades limitadas.',
    error: 'No fue posible inicializar la plataforma.',
  }[platformStatus]

  return (
    <main className="splash" aria-labelledby="splash-title">
      <section className="splash-card">
        <header className="splash-header">
          <div className="splash-mark" aria-hidden="true">
            H
          </div>

          <div>
            <p className="splash-eyebrow">HEYTI-CORE</p>
            <h1 id="splash-title">HEYTI V2.0</h1>
            <p className="splash-subtitle">
              Inteligencia territorial
            </p>
          </div>
        </header>

        <div className="splash-version">
          <span>Versión 2.0.0-alpha.1</span>
          <span>Entorno local</span>
        </div>

        <div
          className="splash-progress"
          role="progressbar"
          aria-label="Progreso de inicialización"
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={progress}
        >
          <div
            className="splash-progress-value"
            style={{ width: `${progress}%` }}
          />
        </div>

        <div className="splash-progress-copy">
          <span>{statusMessage}</span>
          <strong>{progress}%</strong>
        </div>

        <ol className="splash-steps">
          {(state?.steps ?? []).map((step) => (
            <li
              key={step.id}
              className="splash-step"
              data-status={step.status}
            >
              <span
                className="splash-step-indicator"
                aria-hidden="true"
              />

              <span className="splash-step-copy">
                <strong>{step.label}</strong>
                <small>{step.detail}</small>
              </span>

              <span className="splash-step-status">
                {statusLabels[step.status]}
              </span>
            </li>
          ))}
        </ol>

        {platformStatus === 'error' ? (
          <button
            className="splash-button splash-button-secondary"
            type="button"
            onClick={() => {
              setState(null)
              setCanContinue(false)
              setAttempt((value) => value + 1)
            }}
          >
            Reintentar
          </button>
        ) : (
          <button
            className="splash-button"
            type="button"
            disabled={!canContinue}
            onClick={onEnter}
          >
            {canContinue
              ? 'Entrar a HEYTI'
              : 'Verificando plataforma'}
          </button>
        )}

        <p className="splash-footnote">
          El estado de CORE se presenta sin simulaciones.
        </p>
      </section>
    </main>
  )
}
