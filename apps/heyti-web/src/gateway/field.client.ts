import {
  gatewayBaseUrl,
  HeytiGatewayError,
} from './heyti.client'

export type FieldGeometryStatus =
  | 'AVAILABLE'
  | 'NO_GEOMETRY'

export interface FieldPoint {
  actorRef: string
  sectionCode: string
  roleCode: string
  geometryStatus: FieldGeometryStatus
  longitude: number | null
  latitude: number | null
}

export interface FieldSummary {
  totalRecords: number
  geolocatedRecords: number
  recordsWithoutGeometry: number
  unassignedRecords: number
  byRole: Record<string, number>
}

export interface FieldSummaryResponse {
  contract: 'HEYTI_FIELD_RESPONSE'
  version: '1.0'
  capabilityId: 'describe_field'
  operation: 'summary'
  privacyMode: 'PERSONAL_DATA_REDACTED'
  summary: FieldSummary
}

export interface FieldMapResponse {
  contract: 'HEYTI_FIELD_RESPONSE'
  version: '1.0'
  capabilityId: 'describe_field'
  operation: 'map'
  privacyMode: 'PERSONAL_DATA_REDACTED'
  sectionCode: string | null
  points: FieldPoint[]
  coverage: {
    records: number
    geolocatedRecords: number
    recordsWithoutGeometry: number
  }
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

function invalid(message: string): never {
  throw new HeytiGatewayError(
    'INVALID_FIELD_RESPONSE',
    message,
  )
}

function requiredString(
  value: unknown,
  field: string,
): string {
  if (typeof value !== 'string' || !value) {
    return invalid(
      `HEYTI respondió sin ${field} válido.`,
    )
  }

  return value
}

function nonNegativeInteger(
  value: unknown,
  field: string,
): number {
  if (
    typeof value !== 'number' ||
    !Number.isInteger(value) ||
    value < 0
  ) {
    return invalid(
      `HEYTI respondió con ${field} inválido.`,
    )
  }

  return value
}

function parseBase(
  payload: unknown,
  operation: 'summary' | 'map',
): Record<string, unknown> {
  if (!isRecord(payload)) {
    return invalid(
      'HEYTI respondió con un contrato de Campo inválido.',
    )
  }

  if (
    payload.contract !== 'HEYTI_FIELD_RESPONSE' ||
    payload.version !== '1.0' ||
    payload.capability_id !== 'describe_field' ||
    payload.operation !== operation
  ) {
    return invalid(
      'HEYTI respondió con un contrato de Campo no soportado.',
    )
  }

  if (
    !isRecord(payload.privacy) ||
    payload.privacy.mode !== 'PERSONAL_DATA_REDACTED'
  ) {
    return invalid(
      'HEYTI respondió sin protección de datos personales.',
    )
  }

  return payload
}

function parseRoles(
  value: unknown,
): Record<string, number> {
  if (!isRecord(value)) {
    return invalid(
      'HEYTI respondió sin distribución por rol.',
    )
  }

  return Object.fromEntries(
    Object.entries(value).map(([role, count]) => [
      requiredString(role, 'role_code'),
      nonNegativeInteger(count, `by_role.${role}`),
    ]),
  )
}

export function parseFieldSummary(
  payload: unknown,
): FieldSummaryResponse {
  const base = parseBase(payload, 'summary')

  if (!isRecord(base.summary)) {
    return invalid(
      'HEYTI respondió sin resumen de Campo.',
    )
  }

  const totalRecords = nonNegativeInteger(
    base.summary.total_records,
    'total_records',
  )
  const geolocatedRecords = nonNegativeInteger(
    base.summary.geolocated_records,
    'geolocated_records',
  )
  const recordsWithoutGeometry = nonNegativeInteger(
    base.summary.records_without_geometry,
    'records_without_geometry',
  )
  const unassignedRecords = nonNegativeInteger(
    base.summary.unassigned_records,
    'unassigned_records',
  )
  const byRole = parseRoles(base.summary.by_role)

  if (
    geolocatedRecords + recordsWithoutGeometry
      !== totalRecords ||
    Object.values(byRole).reduce(
      (total, count) => total + count,
      unassignedRecords,
    ) !== totalRecords
  ) {
    return invalid(
      'El resumen de Campo es inconsistente.',
    )
  }

  return {
    contract: 'HEYTI_FIELD_RESPONSE',
    version: '1.0',
    capabilityId: 'describe_field',
    operation: 'summary',
    privacyMode: 'PERSONAL_DATA_REDACTED',
    summary: {
      totalRecords,
      geolocatedRecords,
      recordsWithoutGeometry,
      unassignedRecords,
      byRole,
    },
  }
}

const PUBLIC_POINT_FIELDS = new Set([
  'actor_ref',
  'section_code',
  'role_code',
  'geometry_status',
  'longitude',
  'latitude',
])

function parsePoint(value: unknown): FieldPoint {
  if (!isRecord(value)) {
    return invalid('Punto de Campo inválido.')
  }

  if (
    Object.keys(value).some(
      (field) => !PUBLIC_POINT_FIELDS.has(field),
    )
  ) {
    return invalid(
      'El punto de Campo contiene campos no autorizados.',
    )
  }

  const actorRef = requiredString(
    value.actor_ref,
    'actor_ref',
  )
  const sectionCode = requiredString(
    value.section_code,
    'section_code',
  )
  const roleCode = requiredString(
    value.role_code,
    'role_code',
  )

  if (
    value.geometry_status !== 'AVAILABLE' &&
    value.geometry_status !== 'NO_GEOMETRY'
  ) {
    return invalid('geometry_status inválido.')
  }

  if (value.geometry_status === 'NO_GEOMETRY') {
    if (
      value.longitude !== null ||
      value.latitude !== null
    ) {
      return invalid(
        'Un punto sin geometría contiene coordenadas.',
      )
    }

    return {
      actorRef,
      sectionCode,
      roleCode,
      geometryStatus: 'NO_GEOMETRY',
      longitude: null,
      latitude: null,
    }
  }

  if (
    typeof value.longitude !== 'number' ||
    typeof value.latitude !== 'number' ||
    !Number.isFinite(value.longitude) ||
    !Number.isFinite(value.latitude)
  ) {
    return invalid('Coordenadas de Campo inválidas.')
  }

  return {
    actorRef,
    sectionCode,
    roleCode,
    geometryStatus: 'AVAILABLE',
    longitude: value.longitude,
    latitude: value.latitude,
  }
}

export function parseFieldMap(
  payload: unknown,
): FieldMapResponse {
  const base = parseBase(payload, 'map')

  if (
    !Array.isArray(base.points) ||
    !isRecord(base.coverage) ||
    !isRecord(base.filter)
  ) {
    return invalid(
      'HEYTI respondió sin mapa de Campo válido.',
    )
  }

  const points = base.points.map(parsePoint)
  const records = nonNegativeInteger(
    base.coverage.records,
    'coverage.records',
  )
  const geolocatedRecords = nonNegativeInteger(
    base.coverage.geolocated_records,
    'coverage.geolocated_records',
  )
  const recordsWithoutGeometry = nonNegativeInteger(
    base.coverage.records_without_geometry,
    'coverage.records_without_geometry',
  )

  if (
    records !== points.length ||
    geolocatedRecords + recordsWithoutGeometry
      !== records
  ) {
    return invalid(
      'La cobertura del mapa de Campo es inconsistente.',
    )
  }

  const sectionCode =
    base.filter.section_code === null
      ? null
      : requiredString(
          base.filter.section_code,
          'filter.section_code',
        )

  return {
    contract: 'HEYTI_FIELD_RESPONSE',
    version: '1.0',
    capabilityId: 'describe_field',
    operation: 'map',
    privacyMode: 'PERSONAL_DATA_REDACTED',
    sectionCode,
    points,
    coverage: {
      records,
      geolocatedRecords,
      recordsWithoutGeometry,
    },
  }
}

async function requestField(
  body: Record<string, unknown>,
  signal?: AbortSignal,
): Promise<unknown> {
  let response: Response

  try {
    response = await fetch(
      `${gatewayBaseUrl()}/v1/field/describe`,
      {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
        signal,
      },
    )
  } catch (error) {
    if (
      error instanceof DOMException &&
      error.name === 'AbortError'
    ) {
      throw error
    }

    throw new HeytiGatewayError(
      'GATEWAY_UNAVAILABLE',
      'No fue posible conectar con HEYTI-CORE.',
    )
  }

  let payload: unknown

  try {
    payload = await response.json()
  } catch {
    throw new HeytiGatewayError(
      'INVALID_JSON_RESPONSE',
      'HEYTI-CORE respondió sin JSON válido.',
      response.status,
    )
  }

  if (!response.ok) {
    throw new HeytiGatewayError(
      'FIELD_REQUEST_FAILED',
      'HEYTI-CORE no pudo consultar Campo.',
      response.status,
    )
  }

  return payload
}

export async function fetchFieldSummary(
  signal?: AbortSignal,
): Promise<FieldSummaryResponse> {
  return parseFieldSummary(
    await requestField(
      { operation: 'summary' },
      signal,
    ),
  )
}

export async function fetchFieldMap(
  sectionCode?: string,
  signal?: AbortSignal,
): Promise<FieldMapResponse> {
  const normalized = sectionCode?.trim()

  if (
    normalized !== undefined &&
    !/^[1-9]\d*$/.test(normalized)
  ) {
    throw new HeytiGatewayError(
      'INVALID_SECTION_ID',
      'La sección debe ser un entero positivo.',
    )
  }

  return parseFieldMap(
    await requestField(
      {
        operation: 'map',
        ...(normalized
          ? { section_code: normalized }
          : {}),
      },
      signal,
    ),
  )
}
