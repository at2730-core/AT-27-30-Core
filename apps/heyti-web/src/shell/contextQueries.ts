import type { HeytiModuleId, UniverseSelection } from '../platform/platform.types'
export const COMPARISON_MODULES = [
  {id:'territorial-analysis',label:'Análisis Territorial · resultados 2024'},
  {id:'win-all',label:'Ganar Todo · participación histórica'},
  {id:'socioeconomic',label:'Socioeconómico · indicadores 2020'},
] as const
export const CROSS_QUERIES = [
  {id:'results2024',module:'territorial-analysis',label:'Análisis Territorial · resultados 2024',scope:'area'},
  {id:'leaders',module:'territorial-analysis',label:'Análisis Territorial · mayor votación rastreada por año',scope:'area'},
  {id:'participation',module:'win-all',label:'Ganar Todo · participación histórica',scope:'area'},
  {id:'socio-indicators',module:'socioeconomic',label:'Socioeconómico · indicadores generales',scope:'area'},
  {id:'socio-education',module:'socioeconomic',label:'Socioeconómico · perfil educativo 2020',scope:'area'},
  {id:'section-summary',module:'territorial-analysis',label:'Sección · resumen electoral 2024',scope:'section'},
  {id:'section-current',module:'territorial-analysis',label:'Sección · elección 2024',scope:'section'},
  {id:'section-history',module:'territorial-analysis',label:'Sección · historial 2018–2024',scope:'section'},
  {id:'section-trace',module:'territorial-analysis',label:'Sección · fuente de demostración',scope:'section'},
] as const
export type CrossQueryId = typeof CROSS_QUERIES[number]['id']
export function scopeKey(universe:UniverseSelection|null):string {
  return universe?`${universe.level}:${universe.id}`:'none'
}
export function supportedUniverse(universe:UniverseSelection|null):boolean {
  return !!universe&&/^[1-9]\d*$/.test(universe.id)&&['state','municipality','federal-district','local-district','section'].includes(universe.level)
}
export function availableCrossQueries(universe:UniverseSelection|null) {
  if(!supportedUniverse(universe))return []
  return CROSS_QUERIES.filter(q=>q.scope===(universe!.level==='section'?'section':'area'))
}
export function comparisonModules(ids:readonly HeytiModuleId[]):HeytiModuleId[] {
  if(ids.length<2||ids.length>3||new Set(ids).size!==ids.length||ids.some(id=>!COMPARISON_MODULES.some(m=>m.id===id))) throw new Error('Selecciona dos o tres módulos descriptivos distintos.')
  return [...ids]
}
