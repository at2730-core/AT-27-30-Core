import { afterEach, describe, expect, it, vi } from 'vitest'
import { fetchUniverseMap } from './universe.client'
const universe = { level: 'municipality' as const, id: '20', label: 'Municipio 20', sections: 1 }
const geometry = { type: 'Polygon', coordinates: [[[0,0],[1,0],[1,1],[0,0]]] }
const source = () => ({ contract: 'HEYTI_UNIVERSE_RESPONSE', version: '1.0', capability_id: 'describe_universe', universe, year: 2024, contest: 'A', sections: [{ section_id: '1524', crs: 'OGC:CRS84', geometry, status: 'ZERO_TOTAL', leader: null as string | null, total: 0 }], counts: { ZERO_TOTAL: 1 }, coverage: { geographic_sections: 1, represented_sections: 1, blocked_sections: 0 }, provenance: { electoral_scope: 'TRACKED_PARTIES_ONLY', grouping_basis: 'PROPERTIES_OF_CURRENT_GEOJSON', electoral_validation: 'AUDIT_PENDING' } })
function mock(data: unknown) { vi.stubEnv('VITE_HEYTI_GATEWAY_URL','http://127.0.0.1:8765'); vi.stubGlobal('fetch',vi.fn().mockResolvedValue({ ok: true, json: async () => data })) }
afterEach(() => { vi.unstubAllGlobals(); vi.unstubAllEnvs() })
describe('universe map contract', () => {
  it('preserves zero without assigning party',async () => { mock(source()); const map = await fetchUniverseMap(universe,2024,'A'); expect(map.sections[0].total).toBe(0); expect(map.sections[0].leader).toBeNull() })
  it('rejects another universe',async () => { mock({ ...source(), universe: { ...universe, id:'21' } }); await expect(fetchUniverseMap(universe,2024,'A')).rejects.toThrow('no corresponde') })
  it('rejects counts that disagree with map',async () => { mock({ ...source(), counts: { PAN: 1 } }); await expect(fetchUniverseMap(universe,2024,'A')).rejects.toThrow('Leyenda') })
  it('rejects a leader assigned to zero',async () => { const data = source(); data.sections[0] = { ...data.sections[0], leader:'PAN' }; mock(data); await expect(fetchUniverseMap(universe,2024,'A')).rejects.toThrow('Clasificación') })
  it('rejects inconsistent coverage',async () => { mock({ ...source(), coverage: { geographic_sections:1, represented_sections:1, blocked_sections:1 } }); await expect(fetchUniverseMap(universe,2024,'A')).rejects.toThrow('Cobertura') })
  it('rejects malformed geometry',async () => { const data = source(); data.sections[0].geometry.coordinates = []; mock(data); await expect(fetchUniverseMap(universe,2024,'A')).rejects.toThrow() })
})
