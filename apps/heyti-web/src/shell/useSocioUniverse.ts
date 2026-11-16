import { useLayoutEffect, useRef } from 'react'
import type { UniverseOption } from '../gateway/universe.client'
import { useWorkspace } from '../platform/useWorkspace'
import { reconcileSocioUniverse, universeKey } from './socioUniverseSelection'

export function useSocioUniverse(catalog: UniverseOption[], invalidate: () => void) {
  const { state, selectUniverse } = useWorkspace()
  const remembered = useRef('')
  const active = state.universe
  // Section focus is not a new area selection.
  const preferred = active?.level === 'section'
    ? remembered.current : active ? universeKey(active) : ''
  const choice = reconcileSocioUniverse(catalog, preferred)
  const previous = useRef(choice)
  useLayoutEffect(() => {
    remembered.current = choice
    if (previous.current !== choice) {
      previous.current = choice
      invalidate()
    }
  }, [choice, invalidate])
  function setChoice(key: string) {
    const option = catalog.find(u => universeKey(u) === key)
    if (!option) return
    selectUniverse({ id: option.id, label: option.label, level: option.level,
      parentId: option.level === 'state' ? null : '11', truthStatus: 'pending' })
  }
  return { choice, setChoice }
}
