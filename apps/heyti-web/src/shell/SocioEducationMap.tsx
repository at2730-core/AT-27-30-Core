import { useMemo } from 'react'
import type { UniverseMap } from '../gateway/universe.client'
import { GeographicMap } from './GeographicMap'
import { toGeoJsonFeatureCollection } from './mapGeoJson'
import { SOCIO_COLORS, socioBand } from './socioeconomic'
import { socioLinkLabel } from './socioTraceability'
import type { SocioReference } from './socioTraceability'
export function SocioEducationMap({map,values,label,unit,cuts,groups,reference,selected,onSelect}:{map:UniverseMap;values:Record<string,number|null>;label:string;unit:string;cuts:number[];groups:number;reference:SocioReference;selected:string|null;onSelect:(id:string)=>void}){
 const data=useMemo(()=>{
  const collection=toGeoJsonFeatureCollection(map.sections)
  for(const feature of collection.features){
   const id=feature.properties.sectionId,value=values[id]??null
   feature.properties.referenceLabel=label+' · '+(value===null?'N/D':value.toLocaleString('es-MX',{maximumFractionDigits:3})+' '+unit)+' · Censo 2020 · '+socioLinkLabel(id,reference)
  }
  return collection
 },[map,values,label,unit,reference])
 return <figure className="section-geometry-map"><GeographicMap data={data} selectedSection={selected} onSelectSection={onSelect} showSectionLabels style={feature=>{
  const id=String(feature?.properties?.sectionId??''),band=socioBand(values[id]??null,cuts)
  return {fillColor:band===null?'#94a3b8':SOCIO_COLORS[Math.round(band*4/(groups-1))],fillOpacity:band===null?.22:.48,color:selected===id?'#059669':'#64748b',weight:selected===id?3:1}
 }}/><figcaption><strong>{label} · INEGI 2020. Oscuro = mayor valor del indicador; gris = N/D. Colores descriptivos, sin índice combinado. Equivalencia de límites pendiente.</strong></figcaption></figure>
}
