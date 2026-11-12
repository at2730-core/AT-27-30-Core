import {
  afterEach,
  describe,
  expect,
  it,
} from 'vitest'
import {
  authenticatedHeaders,
  clearAuthenticatedSessionToken,
  setAuthenticatedSessionToken,
} from './auth.transport'

describe('transporte autenticado en memoria', () => {
  afterEach(() => {
    clearAuthenticatedSessionToken()
  })

  it('no inventa una cabecera sin sesion', () => {
    expect(authenticatedHeaders()).toEqual({})
  })

  it('produce Bearer para la sesion activa', () => {
    setAuthenticatedSessionToken(
      'SESSION_TOKEN_CERTIFIED',
    )

    expect(authenticatedHeaders()).toEqual({
      Authorization: (
        'Bearer SESSION_TOKEN_CERTIFIED'
      ),
    })
  })

  it('elimina el token al cerrar la sesion', () => {
    setAuthenticatedSessionToken(
      'SESSION_TOKEN_CERTIFIED',
    )
    clearAuthenticatedSessionToken()

    expect(authenticatedHeaders()).toEqual({})
  })

  it.each([
    '',
    '   ',
    'token con espacios',
  ])('rechaza tokens incompatibles: %j', (token) => {
    expect(() => {
      setAuthenticatedSessionToken(token)
    }).toThrow('sessionToken no es valido.')
  })
})
