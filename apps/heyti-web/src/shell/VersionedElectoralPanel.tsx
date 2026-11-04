import { useEffect, useState } from 'react'
import type { ElectoralQuery } from '../gateway/heyti.client'
import { describeSection } from '../gateway/heyti.client'
import { readVersionedElectoral } from '../gateway/electoral.versioned'
import type { VersionedElectoralView } from '../gateway/electoral.versioned'

const series: {label: string; query: ElectoralQuery}[] = [
  {label: 'Ayuntamientos', query: {year: 2024, type: 'A', modality: 'UNICA'}},
  {label: 'Diputaciones locales MR', query: {year: 2024, type: 'DL', modality: 'MR'}},
  {label: 'Diputaciones locales RP', query: {year: 2024, type: 'DL', modality: 'RP'}},
  {label: 'Gubernatura', query: {year: 2024, type: 'G', modality: 'UNICA'}},
  {label: 'Presidencia', query: {year: 2024, type: 'P', modality: 'UNICA'}},
  {label: 'Senado MR', query: {year: 2024, type: 'S', modality: 'MR'}},
  {label: 'Senado RP', query: {year: 2024, type: 'S', modality: 'RP'}},
  {label: 'Diputaciones federales MR', query: {year: 2024, type: 'DF', modality: 'MR'}},
  {label: 'Diputaciones federales RP', query: {year: 2024, type: 'DF', modality: 'RP'}},
]

export function VersionedElectoralPanel({sectionId}: {sectionId: string}) {
  const [selected, setSelected] = useState(0)
  const [result, setResult] = useState<VersionedElectoralView | null>(null)
  const [error, setError] = useState<string | null>(null)
  useEffect(() => {
    const controller = new AbortController()
    setResult(null)
    setError(null)
    describeSection(sectionId, controller.signal, series[selected].query)
      .then(response => {
        if (!controller.signal.aborted) setResult(readVersionedElectoral(response))
      })
      .catch((cause: unknown) => {
        if (!controller.signal.aborted) setError(cause instanceof Error ? cause.message : 'No fue posible consultar la fuente.')
      })
    return () => controller.abort()
  }, [sectionId, selected])
  return <section aria-label="Estado de fuente electoral 2024">
    <h3>Elección 2024 · Sección {sectionId}</h3>
    <label>Elección y modalidad <select value={selected} onChange={event => {
      setResult(null); setError(null); setSelected(Number(event.target.value))
    }}>{series.map((item, index) => <option key={item.label} value={index}>{item.label}</option>)}</select></label>
    <div role="status">
      {error ? <p>{error}</p> : !result ? <p>Consultando estado de la fuente…</p> : <>
        <p>{result.status === 'NO_RELEASE_SELECTED' ? 'Fuente pendiente de selección. Los resultados electorales aún no están habilitados.'
          : result.status === 'SELECTED_RESULT' ? 'Fuente seleccionada. Su visualización detallada requiere una integración posterior.'
          : 'Los resultados electorales no están disponibles para esta consulta.'}</p>
        <details><summary>Estado de la fuente</summary><p>{result.status}</p>
          <p>Selección: {result.selectionStatus ?? 'No informada'}</p>
          <p>Validación: {result.certificationStatus ?? 'No informada'}</p></details>
      </>}
    </div>
  </section>
}
