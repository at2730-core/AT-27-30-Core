export type UniverseIdentity = { level: string; id: string }
export const universeKey = (u: UniverseIdentity) => `${u.level}:${u.id}`

export function reconcileSocioUniverse(
  catalog: readonly UniverseIdentity[], preferred: string,
): string {
  if (catalog.some(u => universeKey(u) === preferred)) return preferred
  return catalog.length === 1 ? universeKey(catalog[0]) : ''
}
