import type { HeytiModuleId } from '../platform/platform.types'

export function ModuleIcon({ moduleId }: { moduleId: HeytiModuleId }) {
  const paths: Record<HeytiModuleId, string> = {
    'territorial-analysis': 'M3 5l6-2 6 2 6-2v16l-6 2-6-2-6 2V5zm6-2v16m6-14v16',
    'win-all': 'M3 20h18M5 16l5-5 4 3 6-9m-5 0h5v5',
    socioeconomic: 'M9 11a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm8 0a2.5 2.5 0 1 0 0-5M3 20v-2a6 6 0 0 1 12 0v2m2-6a5 5 0 0 1 4 4v2',
    field: 'M4 21V3m0 1h15l-3 4 3 4H4',
    'et-27': 'M9 3h6v5H9V3zM3 16h6v5H3v-5zm12 0h6v5h-6v-5zM12 8v4m-6 4v-4h12v4',
    'election-day': 'M7 13l-4 4v4h18v-4l-4-4M6 17h12M9 3h6v10H9V3zm1 5 1 1 3-3',
  }
  return <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor"
    strokeWidth="1.7" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" focusable="false">
    <path d={paths[moduleId]} />
  </svg>
}
