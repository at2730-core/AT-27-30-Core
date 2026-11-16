import { describe, expect, it } from 'vitest'
import { reconcileSocioUniverse } from './socioUniverseSelection'
const leon = { level: 'municipality', id: '787' }
const state = { level: 'state', id: '11' }
describe('socio universe reconciliation', () => {
  it('keeps authorized preference', () => expect(reconcileSocioUniverse([state, leon], 'municipality:787')).toBe('municipality:787'))
  it('selects sole authorized option', () => expect(reconcileSocioUniverse([leon], 'state:11')).toBe('municipality:787'))
  it('requires explicit choice for multiple options', () => expect(reconcileSocioUniverse([state, leon], '')).toBe(''))
  it('rejects unavailable preference with multiple options', () => expect(reconcileSocioUniverse([state, leon], 'municipality:999')).toBe(''))
  it('blocks empty catalog', () => expect(reconcileSocioUniverse([], 'municipality:787')).toBe(''))
})
