import type { HeytiResponse } from './heyti.client'

export interface VersionedElectoralView {
  status: string
  selectionStatus: string | null
  certificationStatus: string | null
}

export function readVersionedElectoral(response: HeytiResponse): VersionedElectoralView {
  const blocks = response.blocks.filter(block => block.role === 'electoral_versioned')
  if (blocks.length !== 1 || response.blocks.some(block => block.role === 'electoral')) {
    throw new Error('La respuesta electoral versionada falta o contiene fuentes incompatibles.')
  }
  const value = blocks[0].content
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Contrato electoral inválido.')
  const row = value as Record<string, unknown>
  if (row.purpose !== 'PRESENTATION' || row.metric_scope !== 'RESULT' || typeof row.status !== 'string' || !('data' in row)) {
    throw new Error('La respuesta no corresponde a presentación electoral.')
  }
  if (row.data !== null && (row.status !== 'SELECTED_RESULT' || row.selection_status !== 'SELECTED' || row.certification_status !== 'CERTIFIED')) {
    throw new Error('HEYTI rechazó cifras sin selección acreditada.')
  }
  if (row.status === 'SELECTED_RESULT' && row.data === null) throw new Error('Resultado seleccionado sin datos.')
  return {
    status: row.status,
    selectionStatus: typeof row.selection_status === 'string' ? row.selection_status : null,
    certificationStatus: typeof row.certification_status === 'string' ? row.certification_status : null,
  }
}
