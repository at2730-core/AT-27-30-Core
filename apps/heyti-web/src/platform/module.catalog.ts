import type {
  HeytiModuleDefinition,
  HeytiModuleId,
} from './platform.types'

export const HEYTI_MODULES = [
  {
    id: 'territorial-analysis',
    code: '01',
    label: 'Análisis Territorial',
    shortLabel: 'Territorial',
    description:
      'Lectura espacial y electoral del universo activo.',
    accentKey: 'territorial',
  },
  {
    id: 'win-all',
    code: '02',
    label: 'Ganar Todo',
    shortLabel: 'Ganar Todo',
    description:
      'Análisis de escenarios y oportunidades estratégicas.',
    accentKey: 'strategy',
  },
  {
    id: 'socioeconomic',
    code: '03',
    label: 'Socioeconómico',
    shortLabel: 'Socioeconómico',
    description:
      'Lectura de indicadores del contexto social.',
    accentKey: 'socioeconomic',
  },
  {
    id: 'field',
    code: '04',
    label: 'Promoción',
    shortLabel: 'Promoción',
    description:
      'Planeación, seguimiento y control territorial.',
    accentKey: 'field',
  },
  {
    id: 'et-27',
    code: '05',
    label: 'ET-27',
    shortLabel: 'ET-27',
    description:
      'Capacidad estratégica ET-27.',
    accentKey: 'et-27',
  },
  {
    id: 'election-day',
    code: '06',
    label: 'Día D',
    shortLabel: 'Día D',
    description:
      'Seguimiento de la operación durante la jornada.',
    accentKey: 'election-day',
  },
] as const satisfies readonly HeytiModuleDefinition[]

export const DEFAULT_MODULE_ID: HeytiModuleId =
  'territorial-analysis'

export function getHeytiModule(
  moduleId: HeytiModuleId,
): HeytiModuleDefinition {
  const moduleDefinition = HEYTI_MODULES.find(
    ({ id }) => id === moduleId,
  )

  if (!moduleDefinition) {
    throw new Error(
      `Módulo HEYTI no registrado: ${moduleId}`,
    )
  }

  return moduleDefinition
}
