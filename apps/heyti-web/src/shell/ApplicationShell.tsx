import { useState } from 'react'
import './ApplicationShell.css'
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
  universe: {
    eyebrow: 'CONTEXTO TERRITORIAL',
    title: 'Seleccionar universo',
    message:
      'El selector se habilitará al conectar el catálogo territorial autorizado.',
  },
  'cross-query': {
    eyebrow: 'CONSULTA CRUZADA',
    title: 'Pregúntale a HEYTI',
    message:
      'La consulta se habilitará cuando existan capacidades conectadas al Gateway.',
  },
  comparison: {
    eyebrow: 'COMPARACIÓN',
    title: 'Configurar módulos',
    message:
      'Aquí se seleccionarán hasta tres módulos sobre el mismo universo.',
  },
} as const

function ApplicationShellContent() {
  const [openPanel, setOpenPanel] =
    useState<OpenPanel>(null)

  const content = openPanel
    ? panelContent[openPanel]
    : null

  return (
    <div className="application-shell">
      <ModuleNavigation />

      <div className="application-workspace">
        <WorkspaceHeader
          onOpenUniverseSelector={() =>
            setOpenPanel('universe')
          }
        />

        <WorkspaceCanvas
          onOpenCrossQuery={() =>
            setOpenPanel('cross-query')
          }
          onConfigureComparison={() =>
            setOpenPanel('comparison')
          }
        />
      </div>

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
