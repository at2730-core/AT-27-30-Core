import { getHeytiModule } from '../platform/module.catalog'
import { useWorkspace } from '../platform/useWorkspace'

interface WorkspaceHeaderProps {
  onOpenUniverseSelector: () => void
  onOpenCrossQuery: () => void
}

export function WorkspaceHeader({
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
    <header className="workspace-header" style={{ flexWrap: 'wrap' }}>
      <div className="workspace-breadcrumb" style={{ flexWrap: 'wrap', minWidth: 0 }}>
        <span>HEYTI-CORE</span>
        <span aria-hidden="true">/</span>
        <strong>{activeModule.label}</strong>
        {state.activeModuleId === 'territorial-analysis' ? <>
          <span aria-hidden="true">·</span>
          <span>{activeModule.description}</span>
        </> : null}
      </div>

      <div className="workspace-header-actions" style={{ flexWrap: 'wrap' }}>
        {state.activeModuleId === 'territorial-analysis' ? (
          <button type="button" className="workspace-action" onClick={onOpenCrossQuery}>Consulta cruzada</button>
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
            ◎
          </span>

          <span className="universe-trigger-copy">
            <small>UNIVERSO ACTIVO</small>
            <strong>{universeLabel}</strong>
          </span>

          <span aria-hidden="true">⌄</span>
        </button>

        <div
          className="workspace-mode-selector"
          role="group"
          aria-label="Modo de visualización"
        >
          <button
            type="button"
            aria-pressed={state.mode === 'individual'}
            data-active={state.mode === 'individual'}
            onClick={() => setMode('individual')}
          >
            Individual
          </button>

          <button
            type="button"
            aria-pressed={state.mode === 'comparison'}
            data-active={state.mode === 'comparison'}
            onClick={() => setMode('comparison')}
          >
            Comparar
          </button>
        </div>
      </div>
    </header>
  )
}
