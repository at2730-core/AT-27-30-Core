import { gatewayBaseUrl } from './heyti.client'

export type AuthRole =
  | 'ADMINISTRATOR'
  | 'COORDINATOR'
  | 'PROMOTER'

export interface AuthenticatedUser {
  userId: number
  username: string
  displayName: string
  role: AuthRole
}

export interface AuthSession {
  sessionToken: string
  expiresAt: string
  user: AuthenticatedUser
}

export class AuthClientError extends Error {
  readonly code: string
  readonly status: number

  constructor(
    code: string,
    message: string,
    status: number,
  ) {
    super(message)
    this.name = 'AuthClientError'
    this.code = code
    this.status = status
  }
}

function record(value: unknown): Record<string, unknown> {
  if (
    typeof value !== 'object'
    || value === null
    || Array.isArray(value)
  ) {
    throw new Error(
      'La respuesta de autenticacion no es un objeto.',
    )
  }

  return value as Record<string, unknown>
}

function text(
  value: unknown,
  fieldName: string,
): string {
  if (
    typeof value !== 'string'
    || !value.trim()
  ) {
    throw new Error(
      `El campo ${fieldName} no es valido.`,
    )
  }

  return value
}

function parseRole(value: unknown): AuthRole {
  if (
    value !== 'ADMINISTRATOR'
    && value !== 'COORDINATOR'
    && value !== 'PROMOTER'
  ) {
    throw new Error(
      'El rol autenticado no es compatible.',
    )
  }

  return value
}

function parseSession(value: unknown): AuthSession {
  const payload = record(value)

  if (payload.status !== 'AUTHENTICATED') {
    throw new Error(
      'La respuesta no confirma autenticacion.',
    )
  }

  const rawUser = record(payload.user)
  const userId = rawUser.user_id

  if (
    typeof userId !== 'number'
    || !Number.isSafeInteger(userId)
    || userId <= 0
  ) {
    throw new Error(
      'El identificador del usuario no es valido.',
    )
  }

  return {
    sessionToken: text(
      payload.session_token,
      'session_token',
    ),
    expiresAt: text(
      payload.expires_at,
      'expires_at',
    ),
    user: {
      userId,
      username: text(
        rawUser.username,
        'user.username',
      ),
      displayName: text(
        rawUser.display_name,
        'user.display_name',
      ),
      role: parseRole(rawUser.role),
    },
  }
}

function parseError(
  value: unknown,
  status: number,
): AuthClientError {
  try {
    const payload = record(value)
    const error = record(payload.error)

    return new AuthClientError(
      text(error.code, 'error.code'),
      text(error.message, 'error.message'),
      status,
    )
  } catch {
    return new AuthClientError(
      'AUTHENTICATION_ERROR',
      'No fue posible completar la autenticacion.',
      status,
    )
  }
}

async function requestJson(
  path: string,
  init: RequestInit,
): Promise<unknown> {
  let response: Response

  try {
    response = await fetch(
      `${gatewayBaseUrl()}${path}`,
      init,
    )
  } catch {
    throw new AuthClientError(
      'NETWORK_ERROR',
      'No fue posible conectar con HEYTI-CORE.',
      0,
    )
  }

  let payload: unknown = null

  try {
    payload = await response.json()
  } catch {
    payload = null
  }

  if (!response.ok) {
    throw parseError(
      payload,
      response.status,
    )
  }

  return payload
}

export async function login(
  username: string,
  password: string,
  signal?: AbortSignal,
): Promise<AuthSession> {
  const payload = await requestJson(
    '/v1/auth/login',
    {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username,
        password,
      }),
      signal,
    },
  )

  return parseSession(payload)
}

export async function currentSession(
  sessionToken: string,
  signal?: AbortSignal,
): Promise<AuthSession> {
  const payload = await requestJson(
    '/v1/auth/session',
    {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        Authorization: `Bearer ${sessionToken}`,
      },
      signal,
    },
  )

  return parseSession(payload)
}

export async function logout(
  sessionToken: string,
  signal?: AbortSignal,
): Promise<void> {
  const payload = record(
    await requestJson(
      '/v1/auth/logout',
      {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          Authorization: (
            `Bearer ${sessionToken}`
          ),
        },
        signal,
      },
    ),
  )

  if (payload.status !== 'SIGNED_OUT') {
    throw new Error(
      'HEYTI-CORE no confirmo el cierre de sesion.',
    )
  }
}
