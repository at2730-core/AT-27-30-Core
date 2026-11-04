import { describe, expect, it } from 'vitest'
import type { UniverseSection, UniverseMap } from '../gateway/universe.client'
import { historicalReference, referenceStyle, attachHistoricalReference } from './historicalReference'
const row = (votes: Record<string, number | null>, total: number | null = 200): UniverseSection => ({ sectionId:'0001', status:'HHI_MID', leader:null, total, votes, geometry:{type:'Polygon',coordinates:[[[0,0],[1,0],[0,1],[0,0]]]}})
const settings = {party:'PAN',unit:'votes',cap:100,emphasis:0} as const

describe('comparación histórica por referencia',()=>{
  it('calcula diferencias históricas sin sumar el voto de un umbral',()=>{
    const result = historicalReference(row({PAN:80,PRI:60,PVEM:20,MORENA:10}),'PAN')
    expect(result.difference).toBe(20); expect(result.pp).toBe(10); expect(result.contrastParties).toEqual(['PRI'])
    expect('additional' in result).toBe(false); expect('transfer' in result).toBe(false)
  })
  it('usa el mismo referente máximo de las otras opciones para cualquier selección',()=>{
    const source = row({PAN:80,PRI:60,PVEM:20,MORENA:10})
    expect(historicalReference(source,'PRI').difference).toBe(-20)
    expect(historicalReference(source,'MORENA').difference).toBe(-70)
  })
  it('conserva empates tanto de máximo como de contraste',()=>{
    const result=historicalReference(row({PAN:70,PRI:70,PVEM:70,MORENA:0},220),'PAN')
    expect(result.difference).toBe(0);expect(result.leaders).toEqual(['PAN','PRI','PVEM']);expect(result.contrastParties).toEqual(['PRI','PVEM'])
  })
  it('mantiene cero observado, faltantes y total cero como estados diferentes',()=>{
    expect(historicalReference(row({PAN:0,PRI:20,PVEM:10,MORENA:0}),'PAN').difference).toBe(-20)
    const missing=historicalReference(row({PAN:0,PRI:null,PVEM:10,MORENA:0}),'PAN')
    expect(missing.selected).toBe(0);expect(missing.difference).toBeNull();expect(missing.status).toBe('NO_DATA')
    expect(historicalReference(row({PAN:0,PRI:0,PVEM:0,MORENA:0},0),'PAN').status).toBe('ZERO_TOTAL')
    expect(historicalReference(row({PAN:0,PRI:0,PVEM:0,MORENA:0},10),'PAN').leaders).toEqual([])
  })
  it('no calcula sobre inconsistencias, no celebradas o desgloses imposibles',()=>{
    const source=row({PAN:80,PRI:60,PVEM:20,MORENA:10},100)
    expect(historicalReference(source,'PAN').status).toBe('INCONSISTENT')
    expect(historicalReference({...source,status:'NOT_CONTESTED'},'PAN').difference).toBeNull()
    expect(historicalReference(row({PAN:NaN,PRI:0,PVEM:0,MORENA:0}),'PAN').status).toBe('INCONSISTENT')
  })
  it('aplica la misma intensidad a diferencias de igual magnitud y no cambia cifras',()=>{
    const positive=historicalReference(row({PAN:80,PRI:60,PVEM:20,MORENA:10}),'PAN')
    const negative=historicalReference(row({PAN:80,PRI:60,PVEM:20,MORENA:10}),'PRI')
    expect(referenceStyle(positive,settings).fillOpacity).toBe(referenceStyle(negative,{...settings,party:'PRI'}).fillOpacity)
    expect(referenceStyle(positive,{...settings,emphasis:30}).fillOpacity).toBeLessThan(referenceStyle(positive,settings).fillOpacity)
    expect(positive.difference).toBe(20)
  })
  it('conserva filas y datos originales al adjuntar controles, rechaza escalas inválidas',()=>{
    const source={year:2024,metric:'concentration',sections:[row({PAN:0,PRI:null,PVEM:0,MORENA:0})]} as UniverseMap
    const result=attachHistoricalReference(source,settings)
    expect(result.sections).toBe(source.sections);expect(result.sections).toHaveLength(1)
    expect('historicalReference' in source).toBe(false)
    expect(()=>attachHistoricalReference(source,{...settings,cap:0})).toThrow()
    expect(()=>attachHistoricalReference({...source,year:2021},settings)).toThrow()
  })
})