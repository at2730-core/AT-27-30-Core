import { gatewayBaseUrl } from './heyti.client'

export type AuthRole =
  | 'ADMINISTRATOR'
  | 'COORDINATOR'
  | 'PROMOTER'

export type TerritorialScopeType =
  | 'GLOBAL'
  | 'MUNICIPALITY'
  | 'SECTION_SET'

export interface TerritorialMunicipality {
  municipalityId: number
  code: string
  name: string
}

export interface TerritorialScope {
  scopeId: number
  name: string
  type: TerritorialScopeType
  municipality: TerritorialMunicipality | null
  sectionCount: number
}

export interface TerritorialAccess {
  globalAccess: boolean
  scopes: TerritorialScope[]
}

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
  territorialAccess: TerritorialAccess
}

export interface PasswordChangedUser {
  userId: number
  username: string
  displayName: string
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

function positiveInteger(
  value: unknown,
  field: string,
): number {
  if (
    typeof value !== 'number'
    || !Number.isSafeInteger(value)
    || value <= 0
  ) {
    throw new Error(
      `El campo ${field} no es un entero positivo.`,
    )
  }

  return value
}

function nonNegativeInteger(
  value: unknown,
  field: string,
): number {
  if (
    typeof value !== 'number'
    || !Number.isSafeInteger(value)
    || value < 0
  ) {
    throw new Error(
      `El campo ${field} no es un entero no negativo.`,
    )
  }

  return value
}

function parseScopeType(
  value: unknown,
): TerritorialScopeType {
  if (
    value !== 'GLOBAL'
    && value !== 'MUNICIPALITY'
    && value !== 'SECTION_SET'
  ) {
    throw new Error(
      'El tipo de alcance territorial no es compatible.',
    )
  }

  return value
}

function parseMunicipality(
  value: unknown,
): TerritorialMunicipality | null {
  if (value === null) {
    return null
  }

  const municipality = record(value)

  return {
    municipalityId: positiveInteger(
      municipality.municipality_id,
      'municipality.municipality_id',
    ),
    code: text(
      municipality.code,
      'municipality.code',
    ),
    name: text(
      municipality.name,
      'municipality.name',
    ),
  }
}

function parseTerritorialScope(
  value: unknown,
): TerritorialScope {
  const scope = record(value)
  const type = parseScopeType(scope.type)
  const municipality = parseMunicipality(
    scope.municipality,
  )
  const sectionCount = nonNegativeInteger(
    scope.section_count,
    'scope.section_count',
  )

  if (
    type === 'MUNICIPALITY'
    && municipality === null
  ) {
    throw new Error(
      'El alcance municipal no identifica municipio.',
    )
  }

  if (
    type === 'GLOBAL'
    && (
      municipality !== null
      || sectionCount !== 0
    )
  ) {
    throw new Error(
      'El alcance global contiene recursos incompatibles.',
    )
  }

  return {
    scopeId: positiveInteger(
      scope.scope_id,
      'scope.scope_id',
    ),
    name: text(
      scope.name,
      'scope.name',
    ),
    type,
    municipality,
    sectionCount,
  }
}

function parseTerritorialAccess(
  value: unknown,
): TerritorialAccess {
  const access = record(value)

  if (typeof access.global_access !== 'boolean') {
    throw new Error(
      'global_access debe ser booleano.',
    )
  }

  if (!Array.isArray(access.scopes)) {
    throw new Error(
      'scopes debe ser una lista.',
    )
  }

  const scopes = access.scopes.map(
    parseTerritorialScope,
  )
  const scopeIds = scopes.map(
    scope => scope.scopeId,
  )

  if (new Set(scopeIds).size !== scopeIds.length) {
    throw new Error(
      'La sesion contiene alcances duplicados.',
    )
  }

  const derivedGlobalAccess = scopes.some(
    scope => scope.type === 'GLOBAL',
  )

  if (
    access.global_access
    !== derivedGlobalAccess
  ) {
    throw new Error(
      'global_access no coincide con los alcances.',
    )
  }

  return {
    globalAccess: access.global_access,
    scopes,
  }
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
    territorialAccess: parseTerritorialAccess(
      payload.territorial_access,
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

function parsePasswordChanged(
  value: unknown,
): PasswordChangedUser {
  const payload = record(value)

  if (payload.status !== 'PASSWORD_CHANGED') {
    throw new Error(
      'La respuesta no confirma el cambio.',
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
    userId,
    username: text(
      rawUser.username,
      'user.username',
    ),
    displayName: text(
      rawUser.display_name,
      'user.display_name',
    ),
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

export async function changePassword(
  username: string,
  currentPassword: string,
  newPassword: string,
  confirmation: string,
  signal?: AbortSignal,
): Promise<PasswordChangedUser> {
  const payload = await requestJson(
    '/v1/auth/password',
    {
      method: 'POST',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username,
        current_password: currentPassword,
        new_password: newPassword,
        confirmation,
      }),
      signal,
    },
  )

  return parsePasswordChanged(payload)
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
