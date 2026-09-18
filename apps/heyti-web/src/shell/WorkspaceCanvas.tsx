import type {
  TerritorialTruthView,
} from '../gateway/territorial.response'
import { getHeytiModule } from '../platform/module.catalog'
import { useWorkspace } from '../platform/useWorkspace'

interface WorkspaceCanvasProps {
  onOpenCrossQuery: () => void
  onConfigureComparison: () => void
  territorialTruth: TerritorialTruthView | null
  territorialLoading: boolean
  territorialError: string | null
}

function classificationLabel(
  classification: string,
): string {
  switch (classification) {
    case 'CURRENT_TERRITORIAL_SECTION':
      return 'Sección territorial vigente'

    case 'SYNTHETIC_CANDIDATE':
      return 'Candidata sintética'

    default:
      return classification
  }
}

function publicationLabel(
  publicationStatus: string,
): string {
  switch (publicationStatus) {
    case 'ALLOWED':
      return 'Publicación permitida'

    case 'BLOCKED':
      return 'Publicación bloqueada'

    default:
      return publicationStatus
  }
}

export function WorkspaceCanvas({
  onOpenCrossQuery,
  onConfigureComparison,
  territorialTruth,
  territorialLoading,
  territorialError,
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

  const truthStatus = territorialLoading
    ? 'Consultando HEYTI-CORE'
    : territorialTruth
      ? publicationLabel(
          territorialTruth.publicationStatus,
        )
      : 'Sin datos representados'

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
              {truthStatus}
            </span>
          </header>

          <div className="workspace-visual-placeholder">
            <span aria-hidden="true">◎</span>

            {territorialTruth ? (
              territorialTruth.truthStatus ===
              'certified' ? (
                <>
                  <strong>
                    Verdad territorial certificada
                  </strong>
                  <small>
                    Identidad validada por HEYTI-CORE. La
                    geometría y el mapa se integrarán en el
                    siguiente bloque de migración.
                  </small>
                </>
              ) : territorialTruth.truthStatus ===
                'unavailable' ? (
                <>
                  <strong>
                    Identidad territorial no publicable
                  </strong>
                  <small>
                    HEYTI-CORE bloqueó su representación. No
                    se mostrará mapa, geometría ni información
                    territorial como si estuviera certificada.
                  </small>
                </>
              ) : (
                <>
                  <strong>
                    Identidad territorial pendiente
                  </strong>
                  <small>
                    La fuente requiere validación antes de
                    permitir su representación territorial.
                  </small>
                </>
              )
            ) : (
              <>
                <strong>Área de visualización</strong>
                <small>
                  Selecciona una sección para consultar su
                  identidad territorial certificada.
                </small>
              </>
            )}
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

          {territorialLoading ? (
            <div className="workspace-insight-empty">
              <strong>Consultando Data Truth</strong>
              <p>
                HEYTI-CORE está validando la identidad
                territorial solicitada.
              </p>
            </div>
          ) : null}

          {!territorialLoading && territorialError ? (
            <div
              className="workspace-insight-error"
              role="alert"
            >
              <strong>Consulta no disponible</strong>
              <p>{territorialError}</p>
            </div>
          ) : null}

          {!territorialLoading &&
          !territorialError &&
          territorialTruth ? (
            <div className="workspace-insight-result">
              <div className="workspace-truth-summary">
                <span
                  data-status={
                    territorialTruth.truthStatus
                  }
                >
                  {publicationLabel(
                    territorialTruth.publicationStatus,
                  )}
                </span>
                <strong>
                  Sección {territorialTruth.sectionId}
                </strong>
                <p>
                  {classificationLabel(
                    territorialTruth.classification,
                  )}
                </p>
              </div>

              <dl className="workspace-truth-details">
                <div>
                  <dt>Clasificación</dt>
                  <dd>
                    {territorialTruth.classification}
                  </dd>
                </div>
                <div>
                  <dt>Estado de respuesta</dt>
                  <dd>
                    {territorialTruth.responseStatus}
                  </dd>
                </div>
                <div>
                  <dt>Versión de conocimiento</dt>
                  <dd>
                    {territorialTruth.knowledgeVersion ??
                      'No informada'}
                  </dd>
                </div>
                <div>
                  <dt>Solicitud</dt>
                  <dd>
                    {territorialTruth.requestId ??
                      'No informada'}
                  </dd>
                </div>
              </dl>

              {territorialTruth.warnings.length > 0 ? (
                <section className="workspace-warning-list">
                  <h3>Advertencias</h3>
                  <ul>
                    {territorialTruth.warnings.map(
                      (warning) => (
                        <li key={warning.code}>
                          <strong>{warning.code}</strong>
                          <span>{warning.message}</span>
                        </li>
                      ),
                    )}
                  </ul>
                </section>
              ) : (
                <p className="workspace-no-warnings">
                  Sin advertencias de Data Truth.
                </p>
              )}
            </div>
          ) : null}

          {!territorialLoading &&
          !territorialError &&
          !territorialTruth ? (
            <div className="workspace-insight-empty">
              <strong>Sin lectura disponible</strong>
              <p>
                Selecciona una sección para obtener una
                respuesta autorizada de HEYTI.
              </p>
            </div>
          ) : null}
        </aside>
      </div>
    </main>
  )
}
