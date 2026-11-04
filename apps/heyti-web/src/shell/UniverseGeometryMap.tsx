import { areaReading, AREA_TITLES } from './territorialAreaAnalysis'
import { geographicGroupsOf, geographicLabel } from './geographicGroups'
import { sensitivityLabel } from './participationSensitivity'
import { historicalReference, referenceLabel, referenceSettings } from './historicalReference'
import { dataAlertDetail } from './dataAlerts'
import { marginLabel } from './historicalMargin'
import { comparisonRowLabel } from './partyComparison'
import { winRowLabel } from './winScenario'
import { goalRowLabel } from './participationGoals'
import { stabilityRowLabel } from './electoralStability'
import type { ElectoralStability } from './electoralStability'
import { scenarioRowLabel } from './participationScenario'
import type { ParticipationScenario } from './participationScenario'
import { participationValue } from './participation'
import { useState } from 'react'
import type { UniverseMap } from '../gateway/universe.client'
import { BaseMap } from './BaseMap'
export const outcomeColors: Record<string, string> = { GOAL_PASS: '#22c55e', GOAL_NEAR: '#facc15', GOAL_FAIL: '#ef4444', STAB_HIGH: '#22c55e', STAB_MID: '#facc15', STAB_LOW: '#ef4444', PART_LOW: '#ef4444', PART_MID: '#facc15', PART_HIGH: '#22c55e', HHI_LOW: '#2a9d8f', HHI_MID: '#e9c46a', HHI_HIGH: '#9b59b6', ABS_LOW: '#2a9d8f', ABS_MID: '#e9c46a', ABS_HIGH: '#f4a261', ABS_VERY_HIGH: '#c94040', PAN: '#1765b3', PRI: '#c83e48', PVEM: '#278348', MORENA: '#853641', TIE: '#805ad5', ZERO_TOTAL: '#f2c85b', NO_DATA: '#94a3b8', NOT_CONTESTED: '#e2e8f0', INCONSISTENT: '#f08a42', NO_TRACKED_VOTES: '#cbd5e1' }
export const outcomeLabels: Record<string, string> = { PART_LOW: 'Menos de 30%', PART_MID: '30% a menos de 50%', PART_HIGH: '50% a 100%', HHI_LOW: 'Índice parcial menor de 0.30', HHI_MID: 'Índice parcial de 0.30 a menos de 0.45', HHI_HIGH: 'Índice parcial de 0.45 o mayor', ABS_LOW: 'Menos de 25%', ABS_MID: '25% a menos de 50%', ABS_HIGH: '50% a menos de 75%', ABS_VERY_HIGH: '75% a 100%', PAN: 'PAN', PRI: 'PRI', PVEM: 'PVEM', MORENA: 'MORENA', TIE: 'Empate rastreado', ZERO_TOTAL: 'Total en cero', NO_DATA: 'Datos faltantes', NOT_CONTESTED: 'No celebrada', INCONSISTENT: 'Cifras inconsistentes', NO_TRACKED_VOTES: 'Sin votos rastreados' }
export function sectionOutcomeLabel(metric: UniverseMap['metric'], status: string, reason?: string | null): string {
  if (status === 'NO_DATA') {
    if (metric === 'abstention') return 'Votos totales o lista nominal faltantes'
    if (reason === 'TRACKED_BREAKDOWN_MISSING') return 'Desglose por partido faltante'
    if (reason === 'TOTAL_MISSING') return 'Votos totales faltantes'
    return 'Desglose por partido o total faltante'
  }
  return outcomeLabels[status]
}
export function UniverseGeometryMap({ result, queryDescription, participation = false, scenario, stability, selectedSection, onSelectSection, historicalMarginMode = false, dataAlertsMode = false, results2024Mode = false }: { results2024Mode?: boolean; dataAlertsMode?: boolean; historicalMarginMode?: boolean; selectedSection?: string | null; onSelectSection?: (id: string) => void; result: UniverseMap; queryDescription?: string; participation?: boolean; scenario?: ParticipationScenario; stability?: ElectoralStability }) {
  const [localSelected, setLocalSelected] = useState<string | null>(null)
  const selected = selectedSection === undefined ? localSelected : selectedSection
  const setSelected = (id: string) => { setLocalSelected(id); onSelectSection?.(id) }
  const chosen = result.sections.find(s => s.sectionId === selected)
  const sensitivity = scenario?.sensitivity
  const area = areaReading(result)
  const geographic = geographicGroupsOf(result)
  const reference = referenceSettings(result)
  const mapLabel = area ? AREA_TITLES[area.kind] + ' · límites de referencia, métricas en tabla' : geographic ? 'Colindancias y agrupaciones geográficas' : scenario?.participationComparison ? 'Comparación de escenarios · mapa '+(scenario.participationComparison.activeDelta>0?'+':'')+scenario.participationComparison.activeDelta+' pp frente a base' : sensitivity ? 'Sensibilidad de participación · variación de volumen' : reference ? 'Comparación histórica por sección · ' + reference.party : results2024Mode ? 'Resultados 2024 por sección' : dataAlertsMode ? 'Alertas de datos · 2024' : historicalMarginMode ? 'Diferencia entre partidos rastreados · histórica 2024' : stability ? 'Estabilidad 2018–2024 · partidos rastreados' : scenario?.distributionOnly ? 'Distribución estimada por sección · proporciones 2024 constantes' : scenario?.comparison ? 'Comparación descriptiva de votos 2027' : scenario?.win ? `Escenario parcial 2027 · ${scenario.win.party} · proporciones 2024 constantes` : scenario?.goals ? `Metas 2027 · meta ${scenario.goals.target}% · tolerancia ${scenario.goals.tolerance} pp · estimación` : scenario ? 'Escenario de participación 2027 · estimación' : participation ? 'Participación histórica' : result.metric === 'concentration' ? 'Concentración parcial' : result.metric === 'abstention' ? 'Abstención' : 'Mayor votación rastreada'
  const rowLabel = (s: UniverseMap['sections'][number]) => area ? 'Consulta las cifras y métricas en la tabla del universo' : geographic ? geographicLabel(geographic.rows[s.sectionId]) : sensitivity ? sensitivityLabel(sensitivity.rows[s.sectionId]) : reference ? referenceLabel(historicalReference(s, reference.party), reference) : results2024Mode ? 'Consulta los datos en la tabla' : dataAlertsMode ? dataAlertDetail(s) : historicalMarginMode ? marginLabel(s) : stability ? stabilityRowLabel(stability.rows[s.sectionId]) : scenario ? (scenario.comparison ? comparisonRowLabel(scenario.comparison.rows[s.sectionId]) : scenario.win ? winRowLabel(scenario.win.rows[s.sectionId], scenario.win.party) : scenario.goals ? `${goalRowLabel(scenario.rows[s.sectionId], scenario.goals)} · ${scenarioRowLabel(scenario.rows[s.sectionId])}` : scenarioRowLabel(scenario.rows[s.sectionId])) : s.concentration != null ? `Índice parcial ${s.concentration.toFixed(3)}` : s.abstention != null ? `${(participation ? participationValue(s.abstention)! : s.abstention).toFixed(1)}% de ${participation ? 'participación' : 'abstención'}` : sectionOutcomeLabel(result.metric, s.leader ?? s.status, s.missingReason)

  return <figure className="section-geometry-map">
    <BaseMap sensitivity={sensitivity} result={result} selectedSection={selected ?? null} onSelectSection={setSelected} neutral={results2024Mode || !!area} />
    <figcaption style={{ flexDirection: 'column', alignItems: 'flex-start', gap: 4 }}>
      <strong>{queryDescription ?? 'Mapa del universo: resultados disponibles por sección.'}</strong>
      <span>Mapa: {mapLabel} · {stability ? '2018–2024' : scenario ? 2027 : result.year} · {result.contest} · Cobertura parcial · Capa base OpenStreetMap</span>
      {chosen ? <span>Sección {chosen.sectionId}: {rowLabel(chosen)}</span> : null}
    </figcaption>
  </figure>
}
