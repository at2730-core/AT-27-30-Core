import { HEYTI_MODULES } from '../platform/module.catalog'
import { useWorkspace } from '../platform/useWorkspace'

export function ModuleNavigation() {
  const {
    state,
    selectModule,
  } = useWorkspace()

  return (
    <aside className="module-navigation">
      <div className="module-navigation-brand">
        <span
          className="module-navigation-mark"
          aria-hidden="true"
        >
          H
        </span>

        <span>
          <strong>HEYTI</strong>
          <small>V2.0 · CORE</small>
        </span>
      </div>

      <p className="module-navigation-status">
        Plataforma operativa
      </p>

      <nav aria-label="Módulos HEYTI">
        <ul className="module-navigation-list">
          {HEYTI_MODULES.map((moduleDefinition) => {
            const isActive =
              state.activeModuleId === moduleDefinition.id

            return (
              <li key={moduleDefinition.id}>
                <button
                  type="button"
                  className="module-navigation-button"
                  data-accent={moduleDefinition.accentKey}
                  data-active={isActive}
                  aria-current={isActive ? 'page' : undefined}
                  onClick={() =>
                    selectModule(moduleDefinition.id)
                  }
                >
                  <span
                    className="module-navigation-code"
                    aria-hidden="true"
                  >
                    {moduleDefinition.code}
                  </span>

                  <span className="module-navigation-label">
                    {moduleDefinition.label}
                  </span>
                </button>
              </li>
            )
          })}
        </ul>
      </nav>

      <div className="module-navigation-footer">
        <span aria-hidden="true" />
        <span>
          <strong>Runtime</strong>
          <small>Estado disponible en diagnóstico</small>
        </span>
      </div>
    </aside>
  )
}
