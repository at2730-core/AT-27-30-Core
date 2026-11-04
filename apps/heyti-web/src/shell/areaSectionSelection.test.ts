import { describe, expect, it } from 'vitest'
import type { UniverseMap } from '../gateway/universe.client'
import { clearAreaSource, selectAreaSection, selectionForScope } from './areaSectionSelectionState'

const map = (): UniverseMap => ({
  universe:{id:'6',label:'Distrito local 6',level:'local-district',sections:2},
  year:2024,contest:'DL',counts:{NO_DATA:2},coverage:{geographic:2,represented:2,blocked:0},provenance:{},
  sections:['1466','1467'].map(sectionId=>({sectionId,status:'NO_DATA',leader:null,total:null,geometry:{type:'Polygon',coordinates:[[[-101.7,21.1],[-101.6,21.1],[-101.6,21.2],[-101.7,21.1]]]}})),
})
describe('Detalle de sección dentro de un universo',()=>{
  it('selecciona una sección representada sin modificar universo, geometrías ni datos',()=>{
    const source=map(),before=JSON.stringify(source)
    const selected=selectAreaSection(null,source,'1466','AT:DL06')!
    expect(selected.sectionId).toBe('1466');expect(selected.map).toBe(source)
    expect(JSON.stringify(source)).toBe(before)
  })
  it('permite consultar la ficha aunque la métrica del mapa sea N/D',()=>{
    expect(selectAreaSection(null,map(),'1466','AT')?.sectionId).toBe('1466')
  })
  it('rechaza claves ajenas, bloqueadas o de otra unidad territorial',()=>{
    const source=map(),previous=selectAreaSection(null,source,'1466','AT')!
    for(const id of ['9999','11020','1102000010010','0','01466','1466x',''])
      expect(selectAreaSection(previous,source,id,'AT')).toBe(previous)
  })
  it('actualiza sección y solicitud al seleccionar desde cualquier origen',()=>{
    const source=map(),first=selectAreaSection(null,source,'1466','AT')!
    const second=selectAreaSection(first,source,'1467','AT')!
    expect(second.sectionId).toBe('1467');expect(second.request).toBe(first.request+1)
    expect(first.sectionId).toBe('1466')
  })
  it('otra pulsación sobre la misma sección permite volver a expandir el panel',()=>{
    const source=map(),first=selectAreaSection(null,source,'1466','AT')!
    expect(selectAreaSection(first,source,'1466','AT')!.request).toBe(first.request+1)
  })
  it('oculta el detalle al cambiar módulo, consulta, modo o universo',()=>{
    const selected=selectAreaSection(null,map(),'1466','individual:AT:DL06:results')!
    expect(selectionForScope(selected,selected.scope)).toBe(selected)
    for(const scope of ['individual:GT:DL06:results','individual:AT:DL06:history','individual:AT:DF01:results','comparison:AT:DL06:results'])
      expect(selectionForScope(selected,scope)).toBeNull()
  })
  it('limpia la ficha al reemplazar o retirar el mapa de origen',()=>{
    const source=map(),selected=selectAreaSection(null,source,'1466','AT')!
    expect(clearAreaSource(selected,source)).toBeNull()
  })
  it('una limpieza tardía de otro mapa no borra una selección nueva',()=>{
    const old=map(),next=map(),selected=selectAreaSection(null,next,'1467','AT')!
    expect(clearAreaSource(selected,old)).toBe(selected)
    expect(selectionForScope(null,'AT')).toBeNull()
  })
})
