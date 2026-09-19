import {
  useId,
} from 'react'
import type {
  GeoLinearRing,
  GeoMultiPolygonCoordinates,
  GeoPosition,
  TerritorialGeometryView,
} from '../gateway/territorial.geometry'

interface SectionGeometryMapProps {
  territorialGeometry: TerritorialGeometryView
}

interface GeometryBounds {
  minX: number
  minY: number
  maxX: number
  maxY: number
}

const VIEW_WIDTH = 800
const VIEW_HEIGHT = 500
const VIEW_PADDING = 42

function asMultiPolygon(
  territorialGeometry: TerritorialGeometryView,
): GeoMultiPolygonCoordinates {
  const { geometry } = territorialGeometry

  return geometry.type === 'Polygon'
    ? [
        geometry.coordinates,
      ]
    : geometry.coordinates
}

function collectPositions(
  polygons: GeoMultiPolygonCoordinates,
): GeoPosition[] {
  const positions: GeoPosition[] = []

  for (const polygon of polygons) {
    for (const ring of polygon) {
      positions.push(...ring)
    }
  }

  return positions
}

function geometryBounds(
  positions: GeoPosition[],
): GeometryBounds {
  const first = positions[0]

  let minX = first[0]
  let minY = first[1]
  let maxX = first[0]
  let maxY = first[1]

  for (const [x, y] of positions.slice(1)) {
    minX = Math.min(minX, x)
    minY = Math.min(minY, y)
    maxX = Math.max(maxX, x)
    maxY = Math.max(maxY, y)
  }

  return {
    minX,
    minY,
    maxX,
    maxY,
  }
}

function projection(
  bounds: GeometryBounds,
): (position: GeoPosition) => GeoPosition {
  const dataWidth = Math.max(
    bounds.maxX - bounds.minX,
    Number.EPSILON,
  )
  const dataHeight = Math.max(
    bounds.maxY - bounds.minY,
    Number.EPSILON,
  )
  const availableWidth =
    VIEW_WIDTH - VIEW_PADDING * 2
  const availableHeight =
    VIEW_HEIGHT - VIEW_PADDING * 2
  const scale = Math.min(
    availableWidth / dataWidth,
    availableHeight / dataHeight,
  )
  const renderedWidth = dataWidth * scale
  const renderedHeight = dataHeight * scale
  const offsetX =
    (VIEW_WIDTH - renderedWidth) / 2
  const offsetY =
    (VIEW_HEIGHT - renderedHeight) / 2

  return ([longitude, latitude]) => [
    offsetX +
      (longitude - bounds.minX) * scale,
    VIEW_HEIGHT -
      (
        offsetY +
        (latitude - bounds.minY) * scale
      ),
  ]
}

function ringPath(
  ring: GeoLinearRing,
  project: (
    position: GeoPosition,
  ) => GeoPosition,
): string {
  return ring
    .map((position, index) => {
      const [x, y] = project(position)
      const command = index === 0 ? 'M' : 'L'

      return `${command}${x.toFixed(2)},${y.toFixed(2)}`
    })
    .concat('Z')
    .join(' ')
}

function geometryPath(
  polygons: GeoMultiPolygonCoordinates,
): string {
  const positions = collectPositions(polygons)
  const project = projection(
    geometryBounds(positions),
  )

  return polygons
    .flatMap((polygon) =>
      polygon.map((ring) =>
        ringPath(ring, project),
      ),
    )
    .join(' ')
}

export function SectionGeometryMap({
  territorialGeometry,
}: SectionGeometryMapProps) {
  const titleId = useId()
  const descriptionId = useId()
  const polygons = asMultiPolygon(
    territorialGeometry,
  )
  const path = geometryPath(polygons)

  return (
    <figure className="section-geometry-map">
      <svg
        viewBox={`0 0 ${VIEW_WIDTH} ${VIEW_HEIGHT}`}
        role="img"
        aria-labelledby={`${titleId} ${descriptionId}`}
        preserveAspectRatio="xMidYMid meet"
      >
        <title id={titleId}>
          Geometría de la sección{' '}
          {territorialGeometry.sectionId}
        </title>
        <desc id={descriptionId}>
          Polígono territorial certificado y ajustado al
          área de visualización.
        </desc>

        <path
          className="section-geometry-shape"
          d={path}
          fillRule="evenodd"
          vectorEffect="non-scaling-stroke"
        />
      </svg>

      <figcaption>
        <strong>
          Sección {territorialGeometry.sectionId}
        </strong>
        <span>
          Geometría certificada ·{' '}
          {territorialGeometry.crs}
        </span>
      </figcaption>
    </figure>
  )
}
