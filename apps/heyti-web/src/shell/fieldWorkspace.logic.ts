import type { FieldPoint } from '../gateway/field.client'

const FIELD_ROLE_LABELS: Record<string, string> = {
  ADVERSARIO: 'Adversario',
  LIDER: 'Líder',
  OBSERVADOR: 'Observador',
  REP_CASILLA: 'Representante de casilla',
  REP_GENERAL: 'Representante general',
  SIMPATIZANTE: 'Simpatizante',
}

export function fieldRoleLabel(role: string): string {
  return FIELD_ROLE_LABELS[role] ?? role
}

export function filterFieldPoints(
  points: FieldPoint[],
  role: string,
  section: string,
): FieldPoint[] {
  const normalizedSection = section.trim()

  return points.filter((point) => (
    (role === 'ALL' || point.roleCode === role) &&
    (
      normalizedSection === '' ||
      point.sectionCode === normalizedSection
    )
  ))
}
