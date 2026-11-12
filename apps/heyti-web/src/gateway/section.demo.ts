import { authenticatedHeaders } from './auth.transport'
import { gatewayBaseUrl } from './heyti.client'

export const DEMO_CONTESTS = ['A','DL','DF','G','S','P'] as const
export const DEMO_PARTIES = ['PAN','PRI','PVEM','MORENA'] as const
export type DemoContestId = typeof DEMO_CONTESTS[number]
export interface DemoContest { status: string; total: number | null; nominal: number | null; votes: Record<string, number | null> }
export interface SectionDemo { sectionId: string; status: string; provenance: Record<string,string>; years: { year: number; contests: Record<DemoContestId,DemoContest> }[] }
function obj(v: unknown): Record<string,unknown> {
  if (!v || typeof v !== 'object' || Array.isArray(v)) throw new Error('Respuesta de demostración inválida.')
  return v as Record<string,unknown>
}
function str(v: unknown): string { if (typeof v !== 'string' || !v) throw new Error('Metadatos de demostración incompletos.'); return v }
function num(v: unknown): number | null {
  if (v === null) return null
  if (typeof v !== 'number' || !Number.isSafeInteger(v) || v < 0) throw new Error('Cifra de demostración inválida.')
  return v
}
export function parseSectionDemo(raw: unknown, sectionId: string): SectionDemo {
  const r=obj(raw)
  if (!/^[1-9]\d*$/.test(sectionId) || r.contract!=='HEYTI_UNIVERSE_RESPONSE' || r.version!=='1.0' || r.capability_id!=='describe_universe' || r.section_id!==sectionId || r.view!=='SECTION_DEMO' || r.source_mode!=='DEMO_MASTER' || r.modality!=='UNSPECIFIED_IN_MASTER') throw new Error('La respuesta no corresponde a la sección o fuente de demostración solicitada.')
  const provenance=Object.fromEntries(Object.entries(obj(r.provenance)).map(([k,v])=>[k,str(v)]))
  if (provenance.electoral_validation!=='AUDIT_PENDING' || provenance.electoral_scope!=='TRACKED_PARTIES_ONLY' || provenance.grouping_basis!=='PROPERTIES_OF_CURRENT_GEOJSON' || !/^[a-f0-9]{64}$/i.test(provenance.master_sha256??'') || !/^[a-f0-9]{64}$/i.test(provenance.geometry_sha256??'')) throw new Error('Procedencia de demostración no soportada.')
  const status=str(r.status)
  if (!['DEMO_AVAILABLE','TERRITORIAL_BLOCKED','GEOMETRY_UNAVAILABLE','NO_DATA'].includes(status) || !Array.isArray(r.years)) throw new Error('Estado de demostración inválido.')
  if (status!=='DEMO_AVAILABLE') {
    if(r.years.length) throw new Error('Una sección no disponible contiene cifras.')
    return {sectionId,status,provenance,years:[]}
  }
  if(r.years.length!==3) throw new Error('Cobertura histórica incompleta.')
  const years=r.years.map((value,index)=>{
    const y=obj(value), contests=obj(y.contests)
    if(y.year!==[2018,2021,2024][index] || Object.keys(contests).sort().join()!==[...DEMO_CONTESTS].sort().join()) throw new Error('Años o contiendas de demostración inválidos.')
    const parsed=Object.fromEntries(DEMO_CONTESTS.map(cid=>{
      const c=obj(contests[cid]), votes=obj(c.votes), status=str(c.status)
      if(!['AVAILABLE','AVAILABLE_WITHOUT_NOMINAL_LIST','SUMMARY_ONLY','NOT_CONTESTED','ZERO_TOTAL','INCOMPLETE','INCONSISTENT','TIED_TRACKED_LEAD'].includes(status) || Object.keys(votes).sort().join()!==[...DEMO_PARTIES].sort().join()) throw new Error('Desglose de demostración inválido.')
      return [cid,{status,total:num(c.total),nominal:num(c.nominal),votes:Object.fromEntries(DEMO_PARTIES.map(p=>[p,num(votes[p])]))}]
    })) as Record<DemoContestId,DemoContest>
    return {year:y.year as number,contests:parsed}
  })
  return {sectionId,status,provenance,years}
}
export function demoParticipation(c: DemoContest): number | null {
  return c.status==='NOT_CONTESTED'||c.status==='INCONSISTENT'||c.total===null||c.nominal===null||c.nominal<=0||c.total>c.nominal ? null : c.total*100/c.nominal
}
export async function fetchSectionDemo(sectionId: string, signal?: AbortSignal): Promise<SectionDemo> {
  const response=await fetch(`${gatewayBaseUrl()}/v1/universes/describe`,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json',...authenticatedHeaders()},body:JSON.stringify({operation:'section-demo',section_id:sectionId}),signal})
  if(!response.ok) throw new Error(`No fue posible consultar los datos de demostración (HTTP ${response.status}). Reinicia HEYTI-CORE tras aplicar el bloque.`)
  return parseSectionDemo(await response.json(),sectionId)
}
