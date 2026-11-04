import type { WorkspaceState } from './platform.types'
import { HEYTI_MODULES } from './module.catalog'
const KEY = 'HEYTI_V2_WORKSPACE_V1'
export function restoreWorkspace(fallback: WorkspaceState): WorkspaceState {
  try {
    const saved = JSON.parse(localStorage.getItem(KEY) ?? 'null')
    const ids = new Set<string>(HEYTI_MODULES.map(m => m.id))
    if (!saved || !ids.has(saved.activeModuleId)) return fallback
    const u = saved.universe
    const levels = ['country', 'state', 'municipality', 'federal-district', 'local-district', 'section']
    if (u !== null && (!u || typeof u.id !== 'string' || typeof u.label !== 'string' || !levels.includes(u.level))) return fallback
    const v = saved.mapView
    const validView = v && [v.zoom, v.x, v.y].every(Number.isFinite) && v.zoom >= 1 && v.zoom <= 8 && Math.abs(v.x) <= 3200 && Math.abs(v.y) <= 2000
    return {
      activeModuleId: saved.activeModuleId,
      mode: saved.mode === 'comparison' ? 'comparison' : 'individual',
      // Stored identity is a preference, never an authorization or cached result.
      universe: u ? { id: u.id, label: u.label, level: u.level, parentId: typeof u.parentId === 'string' ? u.parentId : null, truthStatus: 'pending' } : null,
      mapView: validView ? { zoom: v.zoom, x: v.x, y: v.y } : { zoom: 1, x: 0, y: 0 },
      comparisonModuleIds: Array.isArray(saved.comparisonModuleIds) ? [...new Set<string>(saved.comparisonModuleIds.filter((id: unknown) => typeof id === 'string' && ids.has(id)))].slice(0, 3) as WorkspaceState['comparisonModuleIds'] : [],
    }
  } catch { return fallback }
}
export function persistWorkspace(state: WorkspaceState): void {
  try { localStorage.setItem(KEY, JSON.stringify(state)) } catch { /* Session remains usable without storage. */ }
}
