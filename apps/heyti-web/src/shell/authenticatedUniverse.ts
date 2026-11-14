import type {
  TerritorialAccess,
} from '../gateway/auth.client'
import type {
  UniverseOption,
} from '../gateway/universe.client'
import type {
  UniverseSelection,
} from '../platform/platform.types'

export function authenticatedDefaultUniverse(
  access: TerritorialAccess,
  catalog: UniverseOption[],
): UniverseSelection | null {
  if (
    access.globalAccess
    || catalog.length !== 1
  ) {
    return null
  }

  const universe = catalog[0]

  return {
    id: universe.id,
    label: universe.label,
    level: universe.level,
    parentId: (
      universe.level === 'state'
        ? null
        : '11'
    ),
    truthStatus: 'pending',
  }
}
