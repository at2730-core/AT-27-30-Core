import { getHeytiModule } from '../platform/module.catalog'
import { useWorkspace } from '../platform/useWorkspace'

interface WorkspaceCanvasProps {
  onOpenCrossQuery: () => void
  onConfigureComparison: () => void
}

export function WorkspaceCanvas({
  onOpenCrossQuery,
  onConfigureComparison,
}: WorkspaceCanvasProps) {
  const { state } = useWorkspace()

  const activeModule = getHeytiModule(
    state.activeModuleId,
  )

  if (state.mode === 'comparison') {
    return (
      <main className="workspace-canvas">
        <section className="workspace-introduction">
          <div>
            <p className="workspace-eyebrow">
              CONTEXTO COMPARTIDO
            </p>
            <h1>Comparar perspectivas</h1>
            <p>
              Hasta tres módulos sobre el mismo universo.
            </p>
          </div>

          <button
            type="button"
            className="workspace-action"
            onClick={onConfigureComparison}
          >
            Configurar módulos
          </button>
        </section>

        <section className="workspace-empty-state">
          <span aria-hidden="true">◇</span>
          <h2>Comparación sin configurar</h2>
          <p>
            Selecciona un universo y los módulos que deseas
            contrastar.
          </p>
        </section>
      </main>
    )
  }

  return (
    <main className="workspace-canvas">
      <section className="workspace-introduction">
        <div>
          <p className="workspace-eyebrow">
            MÓDULO {activeModule.code}
          </p>
          <h1>{activeModule.label}</h1>
          <p>{activeModule.description}</p>
        </div>

        <button
          type="button"
          className="workspace-action"
          onClick={onOpenCrossQuery}
        >
          Consulta cruzada
        </button>
      </section>

      <div className="workspace-visual-grid">
        <section
          className="workspace-visual-panel"
          aria-labelledby="visual-panel-title"
        >
          <header>
            <div>
              <p>OBJETO PRINCIPAL</p>
              <h2 id="visual-panel-title">
                {state.universe
                  ? state.universe.label
                  : 'Universo no seleccionado'}
              </h2>
            </div>

            <span className="workspace-truth-status">
              Sin datos representados
            </span>
          </header>

          <div className="workspace-visual-placeholder">
            <span aria-hidden="true">◎</span>
            <strong>Área de visualización</strong>
            <small>
              Aquí se presentará el mapa, gráfica o recurso
              certificado correspondiente.
            </small>
          </div>
        </section>

        <aside
          className="workspace-insight-panel"
          aria-labelledby="insight-panel-title"
        >
          <header>
            <p>RESPUESTA HEYTI</p>
            <h2 id="insight-panel-title">
              Lectura del módulo
            </h2>
          </header>

          <div className="workspace-insight-empty">
            <strong>Sin lectura disponible</strong>
            <p>
              HEYTI responderá cuando exista un universo y
              una fuente autorizada.
            </p>
          </div>
        </aside>
      </div>
    </main>
  )
}
