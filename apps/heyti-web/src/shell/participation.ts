import type { UniverseMap } from '../gateway/universe.client'
export function participationValue(abstention: number | null | undefined): number | null {
  return abstention == null ? null : 100 - abstention
}
export function participationBand(abstention: number | null | undefined, status: string): string {
  const percent = participationValue(abstention)
  return percent === null ? status : percent < 30 ? 'PART_LOW' : percent < 50 ? 'PART_MID' : 'PART_HIGH'
}
export function participationCounts(result: UniverseMap): Record<string, number> {
  const counts: Record<string, number> = {}
  for (const row of result.sections) {
    const key = participationBand(row.abstention, row.status)
    counts[key] = (counts[key] ?? 0) + 1
  }
  return counts
}
