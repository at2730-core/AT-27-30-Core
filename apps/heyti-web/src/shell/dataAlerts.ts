import type { UniverseMap } from '../gateway/universe.client'
export const dataAlertLabels:Record<string,string>={AVAILABLE:'Total y desglose rastreado disponibles',TRACKED_ZERO:'Desglose rastreado en cero con total positivo',NO_DATA:'Datos faltantes',ZERO_TOTAL:'Total de la contienda en cero',INCONSISTENT:'Cifras inconsistentes',NOT_CONTESTED:'Contienda no celebrada'}
export function dataAlertStatus(row:UniverseMap['sections'][number]):string {
 if (!row.status.startsWith('HHI_')) return row.status
 return row.votes && Object.values(row.votes).every(v=>v===0)?'TRACKED_ZERO':'AVAILABLE'
}
export function dataAlertDetail(row:UniverseMap['sections'][number]):string {
 if(row.status==='NO_DATA')return row.missingReason==='TOTAL_MISSING'?'Votos totales faltantes':row.missingReason==='TRACKED_BREAKDOWN_MISSING'?'Desglose por partido faltante':'Total o desglose faltante'
 return dataAlertLabels[dataAlertStatus(row)]??'Estado no disponible'
}
export function dataAlertCounts(result:UniverseMap):Record<string,number>{const counts:Record<string,number>={};for(const row of result.sections){const key=dataAlertStatus(row);counts[key]=(counts[key]??0)+1}return counts}
