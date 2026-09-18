import type { DataTruthStatus } from '../platform/platform.types'
import {
  HeytiGatewayError,
  findResponseBlock,
} from './heyti.client'
import type {
  HeytiResponse,
  HeytiResponseWarning,
} from './heyti.client'

export interface TerritorialTruthView {
  sectionId: string
  classification: string
  publicationStatus: string
  truthStatus: DataTruthStatus
  responseStatus: string
  warnings: HeytiResponseWarning[]
  requestId: string | null
  sessionId: string | null
  knowledgeVersion: string | null
}

function isRecord(
  value: unknown,
): value is Record<string, unknown> {
  return (
    typeof value === 'object' &&
    value !== null &&
    !Array.isArray(value)
  )
}

function requireString(
  value: unknown,
  fieldName: string,
): string {
  if (typeof value !== 'string' || !value.trim()) {
    throw new HeytiGatewayError(
      'INVALID_DATA_TRUTH',
      `Data Truth no contiene un valor válido para ${fieldName}.`,
    )
  }

  return value.trim()
}

function resolveTruthStatus(
  publicationStatus: string,
): DataTruthStatus {
  switch (publicationStatus) {
    case 'ALLOWED':
      return 'certified'

    case 'BLOCKED':
      return 'unavailable'

    default:
      return 'pending'
  }
}

export function readTerritorialTruth(
  response: HeytiResponse,
  requestedSectionId: string,
): TerritorialTruthView {
  const normalizedSectionId = requestedSectionId.trim()

  if (!/^[1-9]\d*$/.test(normalizedSectionId)) {
    throw new HeytiGatewayError(
      'INVALID_SECTION_ID',
      'La sección debe ser un entero positivo.',
    )
  }

  const block = findResponseBlock(
    response,
    'data_truth',
  )

  if (!block) {
    throw new HeytiGatewayError(
      'MISSING_DATA_TRUTH',
      'La respuesta de HEYTI no contiene el bloque Data Truth.',
    )
  }

  if (!isRecord(block.content)) {
    throw new HeytiGatewayError(
      'INVALID_DATA_TRUTH',
      'El bloque Data Truth no contiene un objeto válido.',
    )
  }

  const classification = requireString(
    block.content.classification,
    'classification',
  )
  const publicationStatus = requireString(
    block.content.publication_status,
    'publication_status',
  )

  return {
    sectionId: normalizedSectionId,
    classification,
    publicationStatus,
    truthStatus: resolveTruthStatus(
      publicationStatus,
    ),
    responseStatus: response.status,
    warnings: [...response.warnings],
    requestId: response.trace.request_id,
    sessionId: response.trace.session_id,
    knowledgeVersion:
      response.trace.knowledge_version,
  }
}
