let activeSessionToken: string | null = null

function normalizeToken(sessionToken: string): string {
  if (typeof sessionToken !== 'string') {
    throw new TypeError(
      'sessionToken debe ser una cadena.',
    )
  }

  const normalized = sessionToken.trim()

  if (!normalized || /\s/.test(normalized)) {
    throw new TypeError(
      'sessionToken no es valido.',
    )
  }

  return normalized
}

export function setAuthenticatedSessionToken(
  sessionToken: string,
): void {
  activeSessionToken = normalizeToken(sessionToken)
}

export function clearAuthenticatedSessionToken(): void {
  activeSessionToken = null
}

export function authenticatedHeaders(): Record<string, string> {
  if (!activeSessionToken) {
    return {}
  }

  return {
    Authorization: `Bearer ${activeSessionToken}`,
  }
}
