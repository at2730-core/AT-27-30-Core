import type {
  AuthenticatedUser,
  AuthRole,
} from '../gateway/auth.client'
import { getHeytiModule } from '../platform/module.catalog'
import { useWorkspace } from '../platform/useWorkspace'

interface WorkspaceHeaderProps {
  user: AuthenticatedUser
  logoutPending: boolean
  logoutError: string | null
  onLogout: () => Promise<void>
  onOpenUniverseSelector: () => void
  onOpenCrossQuery: () => void
}

const roleLabels: Record<AuthRole, string> = {
  ADMINISTRATOR: 'Administrador',
  COORDINATOR: 'Coordinador',
  PROMOTER: 'Promotor',
}

export function WorkspaceHeader({
  user,
  logoutPending,
  logoutError,
  onLogout,
  onOpenUniverseSelector,
  onOpenCrossQuery,
}: WorkspaceHeaderProps) {
  const {
    state,
    setMode,
  } = useWorkspace()

  const activeModule = getHeytiModule(
    state.activeModuleId,
  )

  const universeLabel =
    state.universe?.label ?? 'Seleccionar universo'

  return (
    <header
      className="workspace-header"
      style={{ flexWrap: 'wrap' }}
    >
      <div
        className="workspace-breadcrumb"
        style={{
          flexWrap: 'wrap',
          minWidth: 0,
        }}
      >
        <span>HEYTI-CORE</span>
        <span aria-hidden="true">/</span>
        <strong>{activeModule.label}</strong>

        {state.activeModuleId ===
        'territorial-analysis' ? (
          <>
            <span aria-hidden="true">&middot;</span>
            <span>{activeModule.description}</span>
          </>
        ) : null}
      </div>

      <div
        className="workspace-header-actions"
        style={{ flexWrap: 'wrap' }}
      >
        {state.activeModuleId ===
        'territorial-analysis' ? (
          <button
            type="button"
            className="workspace-action"
            onClick={onOpenCrossQuery}
          >
            Consulta cruzada
          </button>
        ) : null}

        <button
          type="button"
          className="universe-trigger"
          aria-haspopup="dialog"
          onClick={onOpenUniverseSelector}
        >
          <span
            className="universe-trigger-symbol"
            aria-hidden="true"
          >
            &#9678;
          </span>

          <span className="universe-trigger-copy">
            <small>UNIVERSO ACTIVO</small>
            <strong>{universeLabel}</strong>
          </span>

          <span aria-hidden="true">&#8964;</span>
        </button>

        <div
          className="workspace-mode-selector"
          role="group"
          aria-label="Modo de visualizacion"
        >
          <button
            type="button"
            aria-pressed={
              state.mode === 'individual'
            }
            data-active={
              state.mode === 'individual'
            }
            onClick={() => setMode('individual')}
          >
            Individual
          </button>

          <button
            type="button"
            aria-pressed={
              state.mode === 'comparison'
            }
            data-active={
              state.mode === 'comparison'
            }
            onClick={() => setMode('comparison')}
          >
            Comparar
          </button>
        </div>

        <div className="workspace-identity">
          <div className="workspace-identity-copy">
            <small>SESI&Oacute;N ACTIVA</small>
            <strong>{user.displayName}</strong>
            <span>{roleLabels[user.role]}</span>
          </div>

          <button
            type="button"
            className="workspace-logout"
            disabled={logoutPending}
            onClick={() => {
              void onLogout()
            }}
          >
            {logoutPending
              ? 'Cerrando...'
              : 'Cerrar sesi\u00f3n'}
          </button>
        </div>

        {logoutError ? (
          <div
            className="workspace-logout-error"
            role="alert"
          >
            {logoutError}
          </div>
        ) : null}
      </div>
    </header>
  )
}
