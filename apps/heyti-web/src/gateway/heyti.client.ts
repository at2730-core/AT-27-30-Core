export interface HeytiResponseBlock {
  type: string
  role: string
  content: unknown
}

export interface HeytiResponseWarning {
  code: string
  message: string
}

export interface HeytiResponseError {
  code: string
  message: string
}

export interface HeytiResponseTrace {
  request_id: string | null
  session_id: string | null
  execution_id: string | null
  knowledge_version: string | null
}

export interface HeytiResponse {
  response_id: string
  contract: 'HEYTI_RESPONSE'
  version: string
  capability_id: string
  status: string
  blocks: HeytiResponseBlock[]
  warnings: HeytiResponseWarning[]
  errors: HeytiResponseError[]
  trace: HeytiResponseTrace
}

export class HeytiGatewayError extends Error {
  readonly code: string
  readonly status: number | null

  constructor(
    code: string,
    message: string,
    status: number | null = null,
  ) {
    super(message)
    this.name = 'HeytiGatewayError'
    this.code = code
    this.status = status
  }
}

function isRecord(
  value: unknown,
): value is Record<string, unknown> {
  return (
    typeof value === 'object' &&
    value !== null &&
    !Array.isArray(value)
  )
}

function requireString(
  value: unknown,
  field: string,
): string {
  if (typeof value !== 'string' || !value) {
    throw new HeytiGatewayError(
      'INVALID_RESPONSE',
      `HEYTI respondió sin ${field} válido.`,
    )
  }

  return value
}

function parseMessages(
  value: unknown,
  field: string,
): HeytiResponseWarning[] {
  if (!Array.isArray(value)) {
    throw new HeytiGatewayError(
      'INVALID_RESPONSE',
      `HEYTI respondió sin ${field} válido.`,
    )
  }

  return value.map((entry) => {
    if (!isRecord(entry)) {
      throw new HeytiGatewayError(
        'INVALID_RESPONSE',
        `HEYTI respondió con ${field} inválido.`,
      )
    }

    return {
      code: requireString(
        entry.code,
        `${field}.code`,
      ),
      message: requireString(
        entry.message,
        `${field}.message`,
      ),
    }
  })
}

function parseBlocks(
  value: unknown,
): HeytiResponseBlock[] {
  if (!Array.isArray(value)) {
    throw new HeytiGatewayError(
      'INVALID_RESPONSE',
      'HEYTI respondió sin blocks válidos.',
    )
  }

  return value.map((entry) => {
    if (!isRecord(entry)) {
      throw new HeytiGatewayError(
        'INVALID_RESPONSE',
        'HEYTI respondió con un block inválido.',
      )
    }

    return {
      type: requireString(
        entry.type,
        'ResponseBlock.type',
      ),
      role: requireString(
        entry.role,
        'ResponseBlock.role',
      ),
      content: entry.content,
    }
  })
}

function parseTrace(
  value: unknown,
): HeytiResponseTrace {
  if (!isRecord(value)) {
    throw new HeytiGatewayError(
      'INVALID_RESPONSE',
      'HEYTI respondió sin trace válido.',
    )
  }

  const nullableString = (
    entry: unknown,
    field: string,
  ): string | null => {
    if (entry === null) {
      return null
    }

    return requireString(entry, field)
  }

  return {
    request_id: nullableString(
      value.request_id,
      'trace.request_id',
    ),
    session_id: nullableString(
      value.session_id,
      'trace.session_id',
    ),
    execution_id: nullableString(
      value.execution_id,
      'trace.execution_id',
    ),
    knowledge_version: nullableString(
      value.knowledge_version,
      'trace.knowledge_version',
    ),
  }
}

function parseHeytiResponse(
  payload: unknown,
): HeytiResponse {
  if (!isRecord(payload)) {
    throw new HeytiGatewayError(
      'INVALID_RESPONSE',
      'HEYTI respondió con un contrato inválido.',
    )
  }

  if (payload.contract !== 'HEYTI_RESPONSE') {
    throw new HeytiGatewayError(
      'INVALID_RESPONSE',
      'HEYTI respondió con un contrato no soportado.',
    )
  }

  return {
    response_id: requireString(
      payload.response_id,
      'response_id',
    ),
    contract: 'HEYTI_RESPONSE',
    version: requireString(
      payload.version,
      'version',
    ),
    capability_id: requireString(
      payload.capability_id,
      'capability_id',
    ),
    status: requireString(
      payload.status,
      'status',
    ),
    blocks: parseBlocks(payload.blocks),
    warnings: parseMessages(
      payload.warnings,
      'warnings',
    ),
    errors: parseMessages(
      payload.errors,
      'errors',
    ),
    trace: parseTrace(payload.trace),
  }
}

export function gatewayBaseUrl(): string {
  const configuredUrl =
    import.meta.env.VITE_HEYTI_GATEWAY_URL?.trim()

  if (!configuredUrl) {
    throw new HeytiGatewayError(
      'GATEWAY_NOT_CONFIGURED',
      'La URL de HEYTI-CORE no está configurada.',
    )
  }

  return configuredUrl.replace(/\/+$/, '')
}

async function readPayload(
  response: Response,
): Promise<unknown> {
  try {
    return await response.json()
  } catch {
    throw new HeytiGatewayError(
      'INVALID_JSON_RESPONSE',
      'HEYTI-CORE respondió sin JSON válido.',
      response.status,
    )
  }
}

function readErrorMessage(
  payload: unknown,
): {
  code: string
  message: string
} {
  if (
    isRecord(payload) &&
    isRecord(payload.error) &&
    typeof payload.error.code === 'string' &&
    typeof payload.error.message === 'string'
  ) {
    return {
      code: payload.error.code,
      message: payload.error.message,
    }
  }

  return {
    code: 'GATEWAY_REQUEST_FAILED',
    message: 'HEYTI-CORE no pudo completar la solicitud.',
  }
}

export interface ElectoralQuery {
  year: 2024
  type: 'A' | 'DL' | 'DF' | 'G' | 'S' | 'P'
  modality: 'UNICA' | 'MR' | 'RP'
}

export async function describeSection(
  sectionId: string,
  signal?: AbortSignal,
  electoralQuery: ElectoralQuery = { year: 2024, type: 'A', modality: 'UNICA' },
): Promise<HeytiResponse> {
  const normalizedSectionId = sectionId.trim()

  if (!/^[1-9]\d*$/.test(normalizedSectionId)) {
    throw new HeytiGatewayError(
      'INVALID_SECTION_ID',
      'La sección debe ser un entero positivo.',
    )
  }

  let response: Response

  try {
    response = await fetch(
      `${gatewayBaseUrl()}/v1/sections/describe`,
      {
        method: 'POST',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          section_id: normalizedSectionId,
          electoral_query: electoralQuery,
        }),
        signal,
      },
    )
  } catch (error) {
    if (
      error instanceof DOMException &&
      error.name === 'AbortError'
    ) {
      throw error
    }

    throw new HeytiGatewayError(
      'GATEWAY_UNAVAILABLE',
      'No fue posible conectar con HEYTI-CORE.',
    )
  }

  const payload = await readPayload(response)

  if (!response.ok) {
    const gatewayError = readErrorMessage(payload)

    throw new HeytiGatewayError(
      gatewayError.code,
      gatewayError.message,
      response.status,
    )
  }

  const parsed = parseHeytiResponse(payload)

  if (parsed.capability_id !== 'describe_section') {
    throw new HeytiGatewayError(
      'INVALID_RESPONSE',
      'HEYTI respondió desde una capability inesperada.',
    )
  }

  return parsed
}

export function findResponseBlock(
  response: HeytiResponse,
  role: string,
): HeytiResponseBlock | undefined {
  return response.blocks.find(
    (block) => block.role === role,
  )
}
