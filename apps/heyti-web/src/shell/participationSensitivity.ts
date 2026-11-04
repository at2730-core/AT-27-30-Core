import type { UniverseMap } from '../gateway/universe.client'
import { buildParticipationScenario } from './participationScenario'
import type { ParticipationScenario } from './participationScenario'
import { comparePartyVotes } from './partyComparison'
import type { ComparisonRow } from './partyComparison'
export interface SensitivityRow {
  sectionId: string; nominal: number | null; years: number[]; basePercent: number | null;
  rawModified: number | null; modifiedPercent: number | null; appliedPP: number | null;
  limited: boolean; baseTotal: number | null; modifiedTotal: number | null; difference: number | null;
  before: ComparisonRow; after: ComparisonRow; status: string;
}
export interface ParticipationSensitivity { delta: number; rows: Record<string,SensitivityRow>; valid: number; limited: number; nominal: number; baseTotal: number; modifiedTotal: number }
export function buildParticipationSensitivity(maps: UniverseMap[], delta: number): ParticipationScenario {
  if (maps.length !== 4 || !Number.isFinite(delta) || delta < -8 || delta > 8 || !Number.isInteger(delta * 2)) throw new Error('La variación debe ir de −8 a +8 pp, en pasos de 0.5; se requieren históricos y desglose 2024.')
  const scenario = buildParticipationScenario(maps.slice(0,3))
  const modifiedRows = Object.fromEntries(Object.entries(scenario.rows).map(([id,row])=>[id,{...row,percent: row.percent === null ? null : Math.max(0,Math.min(100,row.percent+delta))}]))
  const before = comparePartyVotes(scenario,maps[3]), after = comparePartyVotes({...scenario,rows:modifiedRows},maps[3])
  const rows: Record<string,SensitivityRow> = {}
  let valid=0,limited=0,nominal=0,baseTotal=0,modifiedTotal=0
  for (const section of scenario.base.sections) {
    const base = scenario.rows[section.sectionId]
    const calculable = base.percent !== null && base.nominal !== null && Number.isSafeInteger(base.nominal) && base.nominal > 0
    const raw = calculable ? base.percent! + delta : null
    const percent = raw === null ? null : Math.max(0,Math.min(100,raw))
    const totalBefore = calculable ? Math.round(base.nominal! * base.percent! / 100) : null
    const totalAfter = calculable ? Math.round(base.nominal! * percent! / 100) : null
    const row: SensitivityRow = {
      sectionId:section.sectionId,nominal:base.nominal,years:[...base.years],basePercent:base.percent,
      rawModified:raw,modifiedPercent:percent,appliedPP:calculable?percent!-base.percent!:null,
      limited:raw!==null&&(raw<0||raw>100),baseTotal:totalBefore,modifiedTotal:totalAfter,
      difference:calculable?totalAfter!-totalBefore!:null,before:before.rows[section.sectionId],after:after.rows[section.sectionId],status:calculable?'AVAILABLE':base.reason??'NO_DATA',
    }
    rows[section.sectionId]=row
    if(calculable){valid++;nominal+=base.nominal!;baseTotal+=totalBefore!;modifiedTotal+=totalAfter!;if(row.limited)limited++}
  }
  return {...scenario,sensitivity:{delta,rows,valid,limited,nominal,baseTotal,modifiedTotal}}
}
export function sensitivityLabel(row: SensitivityRow) {
  return row.difference === null ? 'Participación no calculable: históricos insuficientes o inconsistentes' : `Participación: ${row.basePercent!.toFixed(3)}% → ${row.modifiedPercent!.toFixed(3)}%; total estimado: ${row.baseTotal} → ${row.modifiedTotal}; variación ${row.difference > 0 ? '+' : ''}${row.difference} votos${row.limited ? '; limitada a 0–100%' : ''}`
}
export function sensitivityStyle(row: SensitivityRow) {
  const value=row.difference
  return {fillColor:value===null||value===0?'#94a3b8':value>0?'#2563eb':'#c56a26',fillOpacity:value===null||value===0?0.2:0.4}
}