export const SOCIO_INDICATORS = [{"key": "POB_TOTAL", "label": "Población total", "unit": "personas"}, {"key": "POB_15_17", "label": "Población de 15 a 17 años", "unit": "personas"}, {"key": "POB_18MAS", "label": "Población de 18 años y más", "unit": "personas"}, {"key": "ESCOLARIDAD_PROM", "label": "Escolaridad promedio", "unit": "años"}, {"key": "ANALFABETAS_15MAS", "label": "Personas analfabetas de 15 años y más", "unit": "personas"}, {"key": "PEA_12MAS", "label": "Población económicamente activa de 12 años y más", "unit": "personas"}, {"key": "OCUPADOS_12MAS", "label": "Personas ocupadas de 12 años y más", "unit": "personas"}, {"key": "DESOCUPADOS_12MAS", "label": "Personas desocupadas de 12 años y más", "unit": "personas"}, {"key": "VIV_CON_ELECTRICIDAD", "label": "Viviendas con electricidad", "unit": "viviendas"}, {"key": "VIV_CON_AGUA", "label": "Viviendas con agua entubada", "unit": "viviendas"}, {"key": "VIV_CON_DRENAJE", "label": "Viviendas con drenaje", "unit": "viviendas"}, {"key": "VIV_CON_INTERNET", "label": "Viviendas con internet", "unit": "viviendas"}, {"key": "VIV_CON_CEL", "label": "Viviendas con celular", "unit": "viviendas"}, {"key": "VIV_CON_PC", "label": "Viviendas con computadora", "unit": "viviendas"}] as const
export type SocioKey = typeof SOCIO_INDICATORS[number]['key']
export type SocioData = Record<string, Record<SocioKey, number | null>>
export function parseSocio(value: unknown): SocioData {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('Archivo socioeconómico inválido.')
  const result: SocioData = {}
  for (const [id, raw] of Object.entries(value)) {
    if (!/^[1-9]\d*$/.test(id) || !raw || typeof raw !== 'object' || Array.isArray(raw)) throw new Error('Identidad o registro socioeconómico inválido.')
    const row = raw as Record<string, unknown>
    result[id] = Object.fromEntries(SOCIO_INDICATORS.map(({key}) => {
      const v = row[key]
      if (v === null || v === undefined || (typeof v === 'string' && !v.trim())) return [key, null]
      if (typeof v !== 'number' && (typeof v !== 'string' || !/^\d+(?:\.\d+)?$/.test(v.trim()))) throw new Error(`Valor inválido: sección ${id}, ${key}.`)
      const n = Number(v)
      if (!Number.isFinite(n) || n < 0 || (key !== 'ESCOLARIDAD_PROM' && !Number.isSafeInteger(n))) throw new Error(`Cifra inválida: sección ${id}, ${key}.`)
      return [key, n]
    })) as Record<SocioKey, number | null>
  }
  if (!Object.keys(result).length) throw new Error('Archivo sin registros.')
  return result
}
// Cuantil empírico de rango más próximo; los valores iguales permanecen juntos.
export function socioCuts(values: (number | null)[], groups: number): number[] {
  if (![3,4,5].includes(groups)) throw new Error('Clasificación inválida.')
  const sorted = values.filter((v): v is number => v !== null).sort((a,b)=>a-b)
  if (!sorted.length) return []
  return Array.from({length: groups-1}, (_,i)=>sorted[Math.ceil(sorted.length*(i+1)/groups)-1])
}
export function socioBand(value: number | null, cuts: number[]): number | null {
  if (value === null) return null
  const index = cuts.findIndex(c=>value<=c)
  return index < 0 ? cuts.length : index
}
export const SOCIO_COLORS = ['#d9f0ed','#a7d9d1','#6bbcb0','#33958b','#17636a']
