import {
  useEffect,
  useMemo,
  useState,
} from 'react'
import {
  CircleMarker,
  GeoJSON,
  MapContainer,
  Popup,
  TileLayer,
  useMap,
} from 'react-leaflet'
import { geoJSON } from 'leaflet'
import type { GeoJsonObject } from 'geojson'
import type {
  FieldMapResponse,
  FieldPoint,
  FieldSummaryResponse,
} from '../gateway/field.client'
import {
  fetchFieldMap,
  fetchFieldSummary,
} from '../gateway/field.client'
import {
  fetchUniverseMap,
} from '../gateway/universe.client'
import type {
  UniverseMap,
} from '../gateway/universe.client'
import { useWorkspace } from '../platform/useWorkspace'
import {
  toGeoJsonFeatureCollection,
} from './mapGeoJson'
import {
  fieldRoleLabel,
  filterFieldPoints,
} from './fieldWorkspace.logic'
import './FieldWorkspace.css'

const LEON_CENTER: [number, number] = [
  21.122,
  -101.68,
]

const ROLE_COLORS: Record<string, string> = {
  ADVERSARIO: '#dc2626',
  LIDER: '#2563eb',
  OBSERVADOR: '#7c3aed',
  REP_CASILLA: '#ea580c',
  REP_GENERAL: '#0891b2',
  SIMPATIZANTE: '#16a34a',
}

function FieldMapFocus({
  data,
  sectionCode,
}: {
  data: ReturnType<
    typeof toGeoJsonFeatureCollection
  > | null
  sectionCode: string
}) {
  const map = useMap()

  useEffect(() => {
    if (!data || data.features.length === 0) {
      return
    }

    const normalizedSection = sectionCode.trim()
    const selectedFeature = normalizedSection
      ? data.features.find(
          (feature) => (
            String(feature.properties.sectionId) ===
            normalizedSection
          ),
        )
      : null

    const focusData = selectedFeature ?? data
    const bounds = geoJSON(
      focusData as GeoJsonObject,
    ).getBounds()

    if (!bounds.isValid()) {
      return
    }

    map.fitBounds(bounds, {
      padding: normalizedSection
        ? [42, 42]
        : [24, 24],
      maxZoom: normalizedSection ? 16 : 12,
    })
  }, [data, map, sectionCode])

  return null
}

function FieldPointPopup({
  point,
}: {
  point: FieldPoint
}) {
  return (
    <div className="field-popup">
      <strong>{fieldRoleLabel(point.roleCode)}</strong>
      <span>Sección {point.sectionCode}</span>
      <small>Referencia protegida: {point.actorRef}</small>
    </div>
  )
}

export function FieldWorkspace() {
  const { state } = useWorkspace()
  const activeUniverse = state.universe
  const [summary, setSummary] =
    useState<FieldSummaryResponse | null>(null)
  const [mapResponse, setMapResponse] =
    useState<FieldMapResponse | null>(null)
  const [territorialMap, setTerritorialMap] =
    useState<UniverseMap | null>(null)
  const [selectedRole, setSelectedRole] =
    useState('ALL')
  const [sectionFilter, setSectionFilter] =
    useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] =
    useState<string | null>(null)

  useEffect(() => {
    const controller = new AbortController()

    Promise.all([
      fetchFieldSummary(controller.signal),
      fetchFieldMap(undefined, controller.signal),
      activeUniverse
        ? fetchUniverseMap(
            {
              level:
                activeUniverse.level === "country"
                || activeUniverse.level === "section"
                  ? "state"
                  : activeUniverse.level,
              id: activeUniverse.id,
              label: activeUniverse.label,
              sections: 0,
            },
            2024,
            'A',
            controller.signal,
          )
        : Promise.resolve(null),
    ])
      .then(([
        summaryResult,
        mapResult,
        territorialResult,
      ]) => {
        setSummary(summaryResult)
        setMapResponse(mapResult)
        setTerritorialMap(territorialResult)
        setError(null)
      })
      .catch((reason: unknown) => {
        if (
          reason instanceof DOMException &&
          reason.name === 'AbortError'
        ) {
          return
        }

        setError(
          reason instanceof Error
            ? reason.message
            : 'Campo no est? disponible.',
        )
      })
      .finally(() => {
        if (!controller.signal.aborted) {
          setLoading(false)
        }
      })

    return () => controller.abort()
  }, [activeUniverse])

  const territorialGeometry = useMemo(
    () => territorialMap
      ? toGeoJsonFeatureCollection(
          territorialMap.sections.map((section) => ({
            sectionId: section.sectionId,
            status: section.status,
            geometry: section.geometry,
          })),
        )
      : null,
    [territorialMap],
  )

  const points = useMemo(
    () => filterFieldPoints(
      mapResponse?.points ?? [],
      selectedRole,
      sectionFilter,
    ).filter(
      (point) => (
        point.geometryStatus === 'AVAILABLE' &&
        point.latitude !== null &&
        point.longitude !== null
      ),
    ),
    [mapResponse, selectedRole, sectionFilter],
  )

  const roleEntries = Object.entries(
    summary?.summary.byRole ?? {},
  ).sort(([left], [right]) =>
    fieldRoleLabel(left).localeCompare(
      fieldRoleLabel(right),
      'es',
    ),
  )

  return (
    <main className="field-workspace">
      <header className="field-heading">
        <div>
          <h1>Lectura territorial protegida</h1>
          <span>
            Datos operativos sin información personal.
          </span>
        </div>

        <span className="field-privacy-badge">
          Datos personales protegidos
        </span>
      </header>

      {loading ? (
        <section
          className="field-message"
          role="status"
        >
          Consultando Campo en HEYTI-CORE?
        </section>
      ) : null}

      {!loading && error ? (
        <section
          className="field-message field-message-error"
          role="alert"
        >
          <strong>Campo no est? disponible</strong>
          <span>{error}</span>
        </section>
      ) : null}

      {!loading && !error && summary && mapResponse ? (
        <>
          <section
            className="field-metrics"
            aria-label="Resumen operativo de Campo"
          >
            <article>
              <span>Registros</span>
              <strong>
                {summary.summary.totalRecords}
              </strong>
            </article>

            <article>
              <span>Geolocalizados</span>
              <strong>
                {summary.summary.geolocatedRecords}
              </strong>
            </article>

            <article>
              <span>Sin geometría</span>
              <strong>
                {summary.summary.recordsWithoutGeometry}
              </strong>
            </article>

            <article>
              <span>Sin asignación</span>
              <strong>
                {summary.summary.unassignedRecords}
              </strong>
            </article>
          </section>

          <section className="field-content">
            <aside className="field-sidebar">
              <div className="field-filter">
                <label htmlFor="field-role">
                  Rol operativo
                </label>
                <select
                  id="field-role"
                  value={selectedRole}
                  onChange={(event) =>
                    setSelectedRole(event.target.value)
                  }
                >
                  <option value="ALL">
                    Todos los roles
                  </option>
                  {roleEntries.map(([role]) => (
                    <option key={role} value={role}>
                      {fieldRoleLabel(role)}
                    </option>
                  ))}
                </select>
              </div>

              <div className="field-filter">
                <label htmlFor="field-section">
                  Sección
                </label>
                <input
                  id="field-section"
                  type="search"
                  inputMode="numeric"
                  pattern="[0-9]*"
                  placeholder="Ej. 1464"
                  value={sectionFilter}
                  onChange={(event) =>
                    setSectionFilter(
                      event.target.value.replace(
                        /\D/g,
                        '',
                      ),
                    )
                  }
                />
              </div>

              <button
                type="button"
                className="field-reset"
                onClick={() => {
                  setSelectedRole('ALL')
                  setSectionFilter('')
                }}
              >
                Restablecer filtros
              </button>

              <div className="field-role-list">
                <h2>Distribución por rol</h2>

                {roleEntries.map(([role, count]) => (
                  <button
                    type="button"
                    key={role}
                    data-active={selectedRole === role}
                    onClick={() => setSelectedRole(role)}
                  >
                    <span
                      className="field-role-color"
                      style={{
                        backgroundColor:
                          ROLE_COLORS[role] ?? '#475569',
                      }}
                      aria-hidden="true"
                    />
                    <span>{fieldRoleLabel(role)}</span>
                    <strong>{count}</strong>
                  </button>
                ))}
              </div>
            </aside>

            <section
              className="field-map-panel"
              aria-label="Mapa operativo de Campo"
            >
              <header>
                <div>
                  <p>PUNTOS REPRESENTADOS</p>
                  <h2>{points.length}</h2>
                </div>

                <span>
                  Cobertura certificada: {
                    mapResponse.coverage.geolocatedRecords
                  } de {mapResponse.coverage.records}
                </span>
              </header>

              <div className="field-map">
                <MapContainer
                  center={LEON_CENTER}
                  zoom={11}
                  scrollWheelZoom
                  className="field-leaflet-map"
                >
                  <TileLayer
                    attribution={
                      '&copy; OpenStreetMap contributors'
                    }
                    url={
                      'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'
                    }
                  />

                  <FieldMapFocus
                    data={territorialGeometry}
                    sectionCode={sectionFilter}
                  />

                  {territorialGeometry ? (
                    <GeoJSON
                      key={
                        territorialMap
                          ? `${territorialMap.universe.level}:${territorialMap.universe.id}`
                          : 'field-territory'
                      }
                      data={territorialGeometry}
                      interactive={false}
                      style={(feature) => {
                        const sectionId = String(
                          feature?.properties?.sectionId ?? '',
                        )
                        const selected =
                          sectionFilter.trim() !== '' &&
                          sectionId === sectionFilter.trim()

                        return {
                          color: selected
                            ? '#047857'
                            : '#334155',
                          weight: selected ? 3 : 1.1,
                          opacity: selected ? 1 : 0.8,
                          fillColor: selected
                            ? '#34d399'
                            : '#dbe7e5',
                          fillOpacity: selected
                            ? 0.2
                            : 0.08,
                        }
                      }}
                    />
                  ) : null}

                  {points.map((point) => (
                    <CircleMarker
                      key={point.actorRef}
                      center={[
                        point.latitude as number,
                        point.longitude as number,
                      ]}
                      radius={7}
                      pathOptions={{
                        color: '#ffffff',
                        weight: 2,
                        fillColor:
                          ROLE_COLORS[point.roleCode] ??
                          '#475569',
                        fillOpacity: 0.9,
                      }}
                    >
                      <Popup>
                        <FieldPointPopup point={point} />
                      </Popup>
                    </CircleMarker>
                  ))}
                </MapContainer>
              </div>

              {points.length === 0 ? (
                <p className="field-empty">
                  No existen puntos para los filtros
                  seleccionados.
                </p>
              ) : null}
            </section>
          </section>

          <footer className="field-trace">
            <strong>Privacidad:</strong>
            <span>{summary.privacyMode}</span>
            <span>
              La interfaz no recibe nombres, teléfonos,
              domicilios, observaciones ni PIN.
            </span>
          </footer>
        </>
      ) : null}
    </main>
  )
}
