export const SOCIO_VIEWS = ['socio-indicators', 'socio-education', 'socio-services', 'socio-margination', 'socio-income', 'socio-poverty', 'socio-rural', 'socio-projection'] as const
export type SocioView = typeof SOCIO_VIEWS[number]
export function rememberSocioView(previous: SocioView, incoming: string): SocioView {
  return SOCIO_VIEWS.includes(incoming as SocioView) ? incoming as SocioView : previous
}
export interface SocioMemoryScope { scope: string; revision: number }
export function advanceSocioScope(previous: SocioMemoryScope, scope: string, active: boolean): SocioMemoryScope {
  if (previous.scope === scope) return previous
  // A query made inside Socio updates its own result. A universe change outside
  // Socio invalidates the hidden result so it cannot reappear under a new scope.
  return { scope, revision: previous.revision + (active ? 0 : 1) }
}
