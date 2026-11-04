import { describe, expect, it } from 'vitest'
import { advanceSocioScope, rememberSocioView } from './socioWorkspaceMemory'
describe('Socio workspace navigation memory', () => {
  it('preserves education when an electoral query becomes active', () => {
    expect(rememberSocioView('socio-education', 'participation')).toBe('socio-education')
    expect(rememberSocioView('socio-education', 'leaders')).toBe('socio-education')
  })
  it('honours an explicit Socio subview change', () => {
    expect(rememberSocioView('socio-education', 'socio-services')).toBe('socio-services')
  })
  it('does not reset a result when switching modules in DF01', () => {
    const state={scope:'federal-district:1',revision:0}
    expect(advanceSocioScope(state,state.scope,false)).toBe(state)
    expect(advanceSocioScope(state,state.scope,true)).toBe(state)
  })
  it('invalidates hidden results when the universe changes elsewhere', () => {
    expect(advanceSocioScope({scope:'federal-district:1',revision:0},'federal-district:2',false)).toEqual({scope:'federal-district:2',revision:1})
  })
  it('keeps a newly queried Socio result when it updates the shared universe', () => {
    expect(advanceSocioScope({scope:'federal-district:1',revision:0},'municipality:1',true)).toEqual({scope:'municipality:1',revision:0})
  })
  it('invalidates after a universe reset outside Socio', () => {
    expect(advanceSocioScope({scope:'federal-district:1',revision:2},'none',false).revision).toBe(3)
  })
})
