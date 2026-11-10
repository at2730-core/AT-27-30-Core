import {
  afterEach,
  describe,
  expect,
  it,
  vi,
} from 'vitest'

import {
  fetchFieldMap,
  fetchFieldSummary,
  parseFieldMap,
} from './field.client'

const summaryResponse = {
  contract: 'HEYTI_FIELD_RESPONSE',
  version: '1.0',
  capability_id: 'describe_field',
  operation: 'summary',
  privacy: {
    mode: 'PERSONAL_DATA_REDACTED',
  },
  summary: {
    total_records: 45,
    geolocated_records: 45,
    records_without_geometry: 0,
    unassigned_records: 0,
    by_role: {
      LIDER: 4,
      SIMPATIZANTE: 41,
    },
  },
}

const mapResponse = {
  contract: 'HEYTI_FIELD_RESPONSE',
  version: '1.0',
  capability_id: 'describe_field',
  operation: 'map',
  privacy: {
    mode: 'PERSONAL_DATA_REDACTED',
  },
  filter: {
    section_code: null,
  },
  points: [
    {
      actor_ref: 'FIELD-0123456789ABCDEF',
      section_code: '1001',
      role_code: 'LIDER',
      geometry_status: 'AVAILABLE',
      longitude: -101.68,
      latitude: 21.12,
    },
  ],
  coverage: {
    records: 1,
    geolocated_records: 1,
    records_without_geometry: 0,
  },
}

function mockFetch(payload: unknown) {
  vi.stubEnv(
    'VITE_HEYTI_GATEWAY_URL',
    'http://127.0.0.1:8765',
  )
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => payload,
    }),
  )
}

afterEach(() => {
  vi.unstubAllGlobals()
  vi.unstubAllEnvs()
})

describe('field client privacy contract', () => {
  it('reads the certified summary', async () => {
    mockFetch(summaryResponse)

    const response = await fetchFieldSummary()

    expect(response.summary.totalRecords).toBe(45)
    expect(response.privacyMode).toBe(
      'PERSONAL_DATA_REDACTED',
    )
  })

  it('reads only public map fields', async () => {
    mockFetch(mapResponse)

    const response = await fetchFieldMap()

    expect(response.points[0]).toEqual({
      actorRef: 'FIELD-0123456789ABCDEF',
      sectionCode: '1001',
      roleCode: 'LIDER',
      geometryStatus: 'AVAILABLE',
      longitude: -101.68,
      latitude: 21.12,
    })
  })

  it('rejects personal fields in a point', () => {
    const unsafe = {
      ...mapResponse,
      points: [
        {
          ...mapResponse.points[0],
          phone: 'not-authorized',
        },
      ],
    }

    expect(() => parseFieldMap(unsafe)).toThrow(
      'campos no autorizados',
    )
  })

  it('rejects inconsistent coverage', () => {
    expect(() =>
      parseFieldMap({
        ...mapResponse,
        coverage: {
          records: 2,
          geolocated_records: 1,
          records_without_geometry: 0,
        },
      }),
    ).toThrow('cobertura')
  })
})
