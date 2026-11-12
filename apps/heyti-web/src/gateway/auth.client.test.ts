import {
  afterEach,
  describe,
  expect,
  it,
  vi,
} from 'vitest'
import {
  AuthClientError,
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
