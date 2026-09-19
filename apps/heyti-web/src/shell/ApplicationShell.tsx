import {
  useState,
} from 'react'
import type {
  FormEvent,
} from 'react'
import './ApplicationShell.css'
import {
  describeSection,
} from '../gateway/heyti.client'
import {
  readTerritorialGeometry,
} from '../gateway/territorial.geometry'
import type {
  TerritorialGeometryView,
} from '../gateway/territorial.geometry'
import {
  readTerritorialTruth,
} from '../gateway/territorial.response'
import type {
  TerritorialTruthView,
} from '../gateway/territorial.response'
import { useWorkspace } from '../platform/useWorkspace'
import { WorkspaceProvider } from '../platform/WorkspaceProvider'
import { ModuleNavigation } from './ModuleNavigation'
import { WorkspaceCanvas } from './WorkspaceCanvas'
import { WorkspaceHeader } from './WorkspaceHeader'

type OpenPanel =
  | 'universe'
  | 'cross-query'
  | 'comparison'
  | null

const panelContent = {
  'cross-query': {
    eyebrow: 'CONSULTA CRUZADA',
    title: 'Pregúntale a HEYTI',
    message:
      'La consulta cruzada se habilitará al integrar las siguientes capacidades certificadas.',
  },
  comparison: {
    eyebrow: 'COMPARACIÓN',
    title: 'Configurar módulos',
    message:
      'Aquí se seleccionarán hasta tres módulos sobre el mismo universo.',
  },
} as const

function ApplicationShellContent() {
  const {
    selectUniverse,
  } = useWorkspace()

  const [openPanel, setOpenPanel] =
    useState<OpenPanel>(null)
  const [sectionInput, setSectionInput] =
    useState('')
  const [territorialTruth, setTerritorialTruth] =
    useState<TerritorialTruthView | null>(null)
  const [
    territorialGeometry,
    setTerritorialGeometry,
  ] = useState<TerritorialGeometryView | null>(null)
  const [territorialLoading, setTerritorialLoading] =
    useState(false)
  const [territorialError, setTerritorialError] =
    useState<string | null>(null)

  const content =
    openPanel === 'cross-query' ||
    openPanel === 'comparison'
      ? panelContent[openPanel]
      : null

  const closePanel = () => {
    if (!territorialLoading) {
      setOpenPanel(null)
    }
  }

  const handleUniverseSubmit = async (
    event: FormEvent<HTMLFormElement>,
  ) => {
    event.preventDefault()

    const requestedSectionId = sectionInput.trim()

    setTerritorialLoading(true)
    setTerritorialError(null)

    try {
      const response = await describeSection(
        requestedSectionId,
      )
      const truth = readTerritorialTruth(
        response,
        requestedSectionId,
      )
      const geometry = readTerritorialGeometry(
        response,
        requestedSectionId,
      )

      if (
        truth.truthStatus !== 'certified' &&
        geometry !== null
      ) {
        throw new Error(
          'HEYTI rechazó una geometría sin autorización.',
        )
      }

      setTerritorialTruth(truth)
      setTerritorialGeometry(geometry)
      selectUniverse({
        id: truth.sectionId,
        label: `Sección ${truth.sectionId}`,
        level: 'section',
        parentId: null,
        truthStatus: truth.truthStatus,
      })
      setSectionInput(truth.sectionId)
      setOpenPanel(null)
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : 'No fue posible consultar la sección.'

      setTerritorialError(message)
    } finally {
      setTerritorialLoading(false)
    }
  }

  return (
    <div className="application-shell">
      <ModuleNavigation />

      <div className="application-workspace">
        <WorkspaceHeader
          onOpenUniverseSelector={() => {
            setTerritorialError(null)
            setOpenPanel('universe')
          }}
        />

        <WorkspaceCanvas
          onOpenCrossQuery={() =>
            setOpenPanel('cross-query')
          }
          onConfigureComparison={() =>
            setOpenPanel('comparison')
          }
          territorialTruth={territorialTruth}
          territorialGeometry={territorialGeometry}
          territorialLoading={territorialLoading}
          territorialError={territorialError}
        />
      </div>

      {openPanel === 'universe' ? (
        <div className="shell-dialog-layer">
          <section
            className="shell-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="universe-dialog-title"
          >
            <button
              type="button"
              className="shell-dialog-close"
              aria-label="Cerrar"
              disabled={territorialLoading}
              onClick={closePanel}
            >
              ×
            </button>

            <p>CONTEXTO TERRITORIAL</p>
            <h2 id="universe-dialog-title">
              Seleccionar sección
            </h2>
            <p>
              Consulta una identidad territorial contra la
              fuente certificada de Guanajuato 2023.
            </p>

            <form
              className="universe-section-form"
              onSubmit={handleUniverseSubmit}
            >
              <label htmlFor="universe-section-id">
                Número de sección
              </label>

              <input
                id="universe-section-id"
                name="section_id"
                type="text"
                inputMode="numeric"
                autoComplete="off"
                placeholder="Ejemplo: 1524"
                value={sectionInput}
                disabled={territorialLoading}
                onChange={(event) =>
                  setSectionInput(event.target.value)
                }
              />

              <button
                type="submit"
                disabled={territorialLoading}
              >
                {territorialLoading
                  ? 'Consultando...'
                  : 'Consultar en HEYTI'}
              </button>
            </form>

            {territorialError ? (
              <div
                className="shell-dialog-error"
                role="alert"
              >
                {territorialError}
              </div>
            ) : null}

            <div className="shell-dialog-notice">
              La interfaz mostrará únicamente la clasificación
              y publicación autorizadas por Data Truth.
            </div>
          </section>
        </div>
      ) : null}

      {content ? (
        <div className="shell-dialog-layer">
          <section
            className="shell-dialog"
            role="dialog"
            aria-modal="true"
            aria-labelledby="shell-dialog-title"
          >
            <button
              type="button"
              className="shell-dialog-close"
              aria-label="Cerrar"
              onClick={() => setOpenPanel(null)}
            >
              ×
            </button>

            <p>{content.eyebrow}</p>
            <h2 id="shell-dialog-title">
              {content.title}
            </h2>
            <p>{content.message}</p>

            <div className="shell-dialog-notice">
              Sin datos simulados.
            </div>
          </section>
        </div>
      ) : null}
    </div>
  )
}

export function ApplicationShell() {
  return (
    <WorkspaceProvider>
      <ApplicationShellContent />
    </WorkspaceProvider>
  )
}
