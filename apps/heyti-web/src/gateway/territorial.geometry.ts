import {
  HeytiGatewayError,
} from './heyti.client'
import type {
  HeytiResponse,
} from './heyti.client'

export type GeoPosition = [
  number,
  number,
]

export type GeoLinearRing = GeoPosition[]

export type GeoPolygonCoordinates = GeoLinearRing[]

export type GeoMultiPolygonCoordinates =
  GeoPolygonCoordinates[]

export interface TerritorialPolygonGeometry {
  type: 'Polygon'
  coordinates: GeoPolygonCoordinates
}

export interface TerritorialMultiPolygonGeometry {
  type: 'MultiPolygon'
  coordinates: GeoMultiPolygonCoordinates
}

export type TerritorialGeometry =
  | TerritorialPolygonGeometry
  | TerritorialMultiPolygonGeometry

export interface TerritorialGeometryView {
  sectionId: string
  crs: 'OGC:CRS84'
  geometry: TerritorialGeometry
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

function invalidGeometry(
  message: string,
): never {
  throw new HeytiGatewayError(
    'INVALID_TERRITORIAL_GEOMETRY',
    message,
  )
}

function parsePosition(
  value: unknown,
): GeoPosition {
  if (
    !Array.isArray(value) ||
    value.length < 2 ||
    typeof value[0] !== 'number' ||
    !Number.isFinite(value[0]) ||
    typeof value[1] !== 'number' ||
    !Number.isFinite(value[1])
  ) {
    return invalidGeometry(
      'La geometría contiene una posición inválida.',
    )
  }

  return [
    value[0],
    value[1],
  ]
}

function positionsAreEqual(
  first: GeoPosition,
  second: GeoPosition,
): boolean {
  return (
    first[0] === second[0] &&
    first[1] === second[1]
  )
}

function parseLinearRing(
  value: unknown,
): GeoLinearRing {
  if (!Array.isArray(value) || value.length < 4) {
    return invalidGeometry(
      'La geometría contiene un anillo inválido.',
    )
  }

  const ring = value.map(parsePosition)

  if (
    !positionsAreEqual(
      ring[0],
      ring[ring.length - 1],
    )
  ) {
    return invalidGeometry(
      'La geometría contiene un anillo abierto.',
    )
  }

  return ring
}

function parsePolygonCoordinates(
  value: unknown,
): GeoPolygonCoordinates {
  if (!Array.isArray(value) || value.length === 0) {
    return invalidGeometry(
      'La geometría no contiene polígonos válidos.',
    )
  }

  return value.map(parseLinearRing)
}

function parseMultiPolygonCoordinates(
  value: unknown,
): GeoMultiPolygonCoordinates {
  if (!Array.isArray(value) || value.length === 0) {
    return invalidGeometry(
      'La geometría no contiene multipolígonos válidos.',
    )
  }

  return value.map(parsePolygonCoordinates)
}

function parseGeometry(
  value: unknown,
): TerritorialGeometry {
  if (!isRecord(value)) {
    return invalidGeometry(
      'El bloque territorial no contiene geometría.',
    )
  }

  if (value.type === 'Polygon') {
    return {
      type: 'Polygon',
      coordinates: parsePolygonCoordinates(
        value.coordinates,
      ),
    }
  }

  if (value.type === 'MultiPolygon') {
    return {
      type: 'MultiPolygon',
      coordinates: parseMultiPolygonCoordinates(
        value.coordinates,
      ),
    }
  }

  return invalidGeometry(
    'El tipo de geometría territorial no está soportado.',
  )
}

export function readTerritorialGeometry(
  response: HeytiResponse,
  requestedSectionId: string,
): TerritorialGeometryView | null {
  const territorialBlocks = response.blocks.filter(
    (block) => block.role === 'territorial',
  )

  if (territorialBlocks.length === 0) {
    return null
  }

  if (territorialBlocks.length !== 1) {
    return invalidGeometry(
      'La respuesta contiene múltiples bloques territoriales.',
    )
  }

  const content = territorialBlocks[0].content

  if (!isRecord(content)) {
    return invalidGeometry(
      'El bloque territorial no contiene un objeto válido.',
    )
  }

  const normalizedSectionId =
    requestedSectionId.trim()

  if (
    typeof content.section_id !== 'string' ||
    content.section_id !== normalizedSectionId
  ) {
    return invalidGeometry(
      'La geometría no corresponde a la sección solicitada.',
    )
  }

  if (content.crs !== 'OGC:CRS84') {
    return invalidGeometry(
      'La geometría territorial no utiliza OGC:CRS84.',
    )
  }

  return {
    sectionId: content.section_id,
    crs: content.crs,
    geometry: parseGeometry(content.geometry),
  }
}
