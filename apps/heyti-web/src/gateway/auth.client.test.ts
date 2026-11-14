import {
  afterEach,
  describe,
  expect,
  it,
  vi,
} from 'vitest'
import {
  AuthClientError,
  changePassword,
  currentSession,
  login,
  logout,
} from './auth.client'

const sessionPayload = {
  status: 'AUTHENTICATED',
  session_token: 'A'.repeat(43),
  expires_at: '2026-11-12T18:00:00+00:00',
  user: {
    user_id: 3,
    username: 'alex',
    display_name: 'Alex',
    role: 'ADMINISTRATOR',
  },
  territorial_access: {
    global_access: true,
    scopes: [
      {
        scope_id: 1,
        name: 'Acceso global',
        type: 'GLOBAL',
        municipality: null,
        section_count: 0,
      },
    ],
  },
}

function mockResponse(
  payload: unknown,
  status = 200,
) {
  vi.stubEnv(
    'VITE_HEYTI_GATEWAY_URL',
    'http://127.0.0.1:8765',
  )
  vi.stubGlobal(
    'fetch',
    vi.fn().mockResolvedValue({
      ok: status >= 200 && status < 300,
      status,
      json: async () => payload,
    }),
  )
}

afterEach(() => {
  vi.unstubAllGlobals()
  vi.unstubAllEnvs()
})

describe('cliente de autenticacion', () => {
  it('inicia sesion sin conservar la contrasena', async () => {
    mockResponse(sessionPayload)

    const session = await login(
      'alex',
      'secret-password',
    )

    expect(session).toEqual({
      sessionToken: 'A'.repeat(43),
      expiresAt: '2026-11-12T18:00:00+00:00',
      territorialAccess: {
        globalAccess: true,
        scopes: [
          {
            scopeId: 1,
            name: 'Acceso global',
            type: 'GLOBAL',
            municipality: null,
            sectionCount: 0,
          },
        ],
      },
      user: {
        userId: 3,
        username: 'alex',
        displayName: 'Alex',
        role: 'ADMINISTRATOR',
      },
    })

    const fetchMock = vi.mocked(fetch)
    const request = fetchMock.mock.calls[0]

    expect(request[0]).toBe(
      'http://127.0.0.1:8765/v1/auth/login',
    )
    expect(request[1]?.body).toContain(
      'secret-password',
    )
    expect(session).not.toHaveProperty(
      'password',
    )
  })

  it('traduce el rechazo uniforme del CORE', async () => {
    mockResponse(
      {
        error: {
          code: 'INVALID_CREDENTIALS',
          message: 'Credenciales invalidas.',
        },
      },
      401,
    )

    await expect(
      login('alex', 'wrong-password'),
    ).rejects.toMatchObject({
      name: 'AuthClientError',
      code: 'INVALID_CREDENTIALS',
      status: 401,
    })
  })

  it('rechaza una identidad incompatible', async () => {
    mockResponse({
      ...sessionPayload,
      user: {
        ...sessionPayload.user,
        role: 'UNKNOWN',
      },
    })

    await expect(
      login('alex', 'secret-password'),
    ).rejects.toThrow(
      'rol autenticado',
    )
  })

  it('consulta la sesion con Bearer', async () => {
    mockResponse(sessionPayload)

    await currentSession('session-token')

    const headers = vi.mocked(fetch)
      .mock.calls[0][1]?.headers as (
        Record<string, string>
      )

    expect(headers.Authorization).toBe(
      'Bearer session-token',
    )
  })

  it('cierra la sesion con Bearer', async () => {
    mockResponse({
      status: 'SIGNED_OUT',
    })

    await logout('session-token')

    const request = vi.mocked(fetch)
      .mock.calls[0]

    expect(request[0]).toBe(
      'http://127.0.0.1:8765/v1/auth/logout',
    )
    expect(request[1]?.method).toBe('POST')
  })

  it('reporta una falla de red sin filtrar datos', async () => {
    vi.stubEnv(
      'VITE_HEYTI_GATEWAY_URL',
      'http://127.0.0.1:8765',
    )
    vi.stubGlobal(
      'fetch',
      vi.fn().mockRejectedValue(
        new Error('network detail'),
      ),
    )

    await expect(
      login('alex', 'secret-password'),
    ).rejects.toEqual(
      new AuthClientError(
        'NETWORK_ERROR',
        'No fue posible conectar con HEYTI-CORE.',
        0,
      ),
    )
  })
})

describe('cambio obligatorio de contrasena', () => {
  it('envia el cambio sin devolver secretos', async () => {
    mockResponse({
      status: 'PASSWORD_CHANGED',
      user: {
        user_id: 8,
        username: 'jose.de.jesus',
        display_name: 'Jose de Jesus',
      },
    })

    const result = await changePassword(
      'jose.de.jesus',
      'Temporal-2026',
      'Definitiva-2026',
      'Definitiva-2026',
    )

    expect(result).toEqual({
      userId: 8,
      username: 'jose.de.jesus',
      displayName: 'Jose de Jesus',
    })

    const request = vi.mocked(fetch).mock.calls[0]
    const body = String(request[1]?.body)

    expect(request[0]).toBe(
      'http://127.0.0.1:8765/v1/auth/password',
    )
    expect(request[1]?.method).toBe('POST')
    expect(body).toContain('"current_password"')
    expect(body).toContain('"new_password"')
    expect(result).not.toHaveProperty('password')
    expect(result).not.toHaveProperty('sessionToken')
  })

  it('traduce una credencial temporal invalida', async () => {
    mockResponse(
      {
        error: {
          code: 'INVALID_CREDENTIALS',
          message: 'Credenciales invalidas.',
        },
      },
      401,
    )

    await expect(
      changePassword(
        'jose.de.jesus',
        'incorrecta',
        'Definitiva-2026',
        'Definitiva-2026',
      ),
    ).rejects.toMatchObject({
      name: 'AuthClientError',
      code: 'INVALID_CREDENTIALS',
      status: 401,
    })
  })

  it('rechaza una confirmacion HTTP incompatible', async () => {
    mockResponse({
      status: 'UNKNOWN',
      user: {
        user_id: 8,
        username: 'jose.de.jesus',
        display_name: 'Jose de Jesus',
      },
    })

    await expect(
      changePassword(
        'jose.de.jesus',
        'Temporal-2026',
        'Definitiva-2026',
        'Definitiva-2026',
      ),
    ).rejects.toThrow(
      'no confirma el cambio',
    )
  })
})

describe('alcance territorial autenticado', () => {
  it('traduce un alcance municipal', async () => {
    mockResponse({
      ...sessionPayload,
      user: {
        user_id: 4,
        username: 'jose.de.jesus',
        display_name: 'Jose de Jesus',
        role: 'COORDINATOR',
      },
      territorial_access: {
        global_access: false,
        scopes: [
          {
            scope_id: 2,
            name: 'Municipio 20 - Leon',
            type: 'MUNICIPALITY',
            municipality: {
              municipality_id: 20,
              code: '20',
              name: 'Leon de los Aldama',
            },
            section_count: 787,
          },
        ],
      },
    })

    const session = await login(
      'jose.de.jesus',
      'definitive-password',
    )

    expect(session.territorialAccess).toEqual({
      globalAccess: false,
      scopes: [
        {
          scopeId: 2,
          name: 'Municipio 20 - Leon',
          type: 'MUNICIPALITY',
          municipality: {
            municipalityId: 20,
            code: '20',
            name: 'Leon de los Aldama',
          },
          sectionCount: 787,
        },
      ],
    })
  })

  it('rechaza una sesion sin alcance', async () => {
    const {
      territorial_access: _territorialAccess,
      ...incompleteSession
    } = sessionPayload

    mockResponse(incompleteSession)

    await expect(
      login('alex', 'secret-password'),
    ).rejects.toThrow(
      'La respuesta de autenticacion no es un objeto.',
    )
  })

  it('rechaza una marca global inconsistente', async () => {
    mockResponse({
      ...sessionPayload,
      territorial_access: {
        global_access: false,
        scopes: [
          {
            scope_id: 1,
            name: 'Acceso global',
            type: 'GLOBAL',
            municipality: null,
            section_count: 0,
          },
        ],
      },
    })

    await expect(
      login('alex', 'secret-password'),
    ).rejects.toThrow(
      'global_access no coincide con los alcances.',
    )
  })
})
