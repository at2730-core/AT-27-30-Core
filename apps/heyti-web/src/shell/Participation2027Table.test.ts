import {describe,it,expect} from 'vitest'
import type {ScenarioRow} from './participationScenario'
import {estimatedParticipationThreePercent,estimatedParticipationTotal,sortParticipationRows} from './Participation2027Table'
const row=(sectionId:string, nominal:number|null, percent:number|null, reason:string|null=null):ScenarioRow=>({sectionId, nominal, percent, reason, raw: percent, clamped:false, years:[2018,2021,2024]})
describe('Total estimado con LN base2024',()=>{
 it('redondea total con base y porcentaje sin redondear porcentaje primero',()=>{expect(estimatedParticipationTotal(row('331',806,78.758))).toBe(635);expect(estimatedParticipationTotal(row('331',810,80.483))).toBe(652)})
 it('calcula el 3% del total estimado 2027',()=>{expect(estimatedParticipationThreePercent(row('331',806,78.758))).toBe(19);expect(estimatedParticipationThreePercent(row('331',810,80.483))).toBe(20)})
 it('ordena columnas numéricas y conserva el desempate por sección',()=>{const rows=[row('12', 500, 51), row('2', 800, 40), row('100', 200, 60)]; expect(sortParticipationRows(rows,'nominal').map(r=>r.sectionId)).toEqual(['100','12','2']); expect(sortParticipationRows(rows,'total',true).map(r=>r.sectionId)).toEqual(['2','12','100'])})
 it('conserva cero y no rellena insuficiencias o inconsistencias',()=>{expect(estimatedParticipationTotal(row('331',100,0))).toBe(0);expect(estimatedParticipationTotal(row('331',null,50))).toBeNull();expect(estimatedParticipationTotal(row('331',100,null))).toBeNull();expect(estimatedParticipationTotal(row('331',100,50,'INCONSISTENT'))).toBeNull();expect(estimatedParticipationTotal(row('331',0,50))).toBeNull();expect(estimatedParticipationThreePercent(row('331',100,null))).toBeNull();expect(estimatedParticipationThreePercent(row('331',100,50,'INCONSISTENT'))).toBeNull()})
})
