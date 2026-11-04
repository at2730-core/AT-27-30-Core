import type { UniverseMap } from '../gateway/universe.client'
import { SOCIO_INDICATORS } from './socioeconomic'
import type { SocioKey } from './socioeconomic'
import { SOCIO_FIELD_MAPPING, SOCIO_METHOD_URL, SOCIO_OFFICIAL_URL, socioUniverseCoverage } from './socioTraceability'
import type { SocioReference, SocioVerification } from './socioTraceability'

export function SocioTraceabilitySummary({map,reference,verification,indicator}:{map:UniverseMap;reference:SocioReference;verification:SocioVerification;indicator:SocioKey}){
 const coverage=socioUniverseCoverage(map,reference)
 return <section className="heyti-data-panel-detail" aria-label="Fuente y correspondencia territorial socioeconómica">
  <h3>Fuente: INEGI e INE · Censo 2020</h3>
  <p>Estadísticas Censales a Escalas Geoelectorales 2020. Datos censales de 2020, publicación 18 de agosto de 2021. La fecha de consulta no actualiza el año de las cifras.</p>
  <p role="status"><strong>Archivo completo de Guanajuato · cotejo de los 14 indicadores:</strong> {verification.allMatch?`Cotejo de cifras correcto: ${verification.matched.toLocaleString('es-MX')} valores del archivo coinciden con la referencia oficial descargada.`:`Cotejo con diferencias o faltantes: ${verification.matched.toLocaleString('es-MX')} coincidencias, ${verification.different} diferencias, ${verification.missing} valores faltantes, ${verification.withoutReference} registros sin referencia y ${verification.referenceWithoutRecord} registros oficiales ausentes del archivo. Revisa el estado de cada valor; no todos pueden identificarse como cifras de 2020.`}</p>
  <p>Universo actual ({map.universe.label}): {coverage.matched} secciones enlazadas por clave y {coverage.withoutRecord} sin registro censal propio para esa clave; {map.coverage.blocked} geometrías bloqueadas no representadas. Estos conteos corresponden a las secciones representadas del universo consultado, no a todo Guanajuato.</p>
  <p><strong>La coincidencia de clave no certifica la equivalencia de límites.</strong> La base censal utiliza cartografía de enero de 2021; el mapa y las agrupaciones provienen del CORE. Los límites y su correspondencia con el corte censal siguen pendientes de conciliar.</p>
  {coverage.districtDifferences!==null?<p>{coverage.districtDifferences} secciones enlazadas tienen un distrito federal distinto en la fuente de 2020 frente al distrito seleccionado. Las sumas de registros enlazados no son el total distrital oficial publicado en 2020 ni un total actual certificado.</p>:null}
  <p>{coverage.documentedOrigins} secciones representadas tienen una sección de origen documentada. Esa relación no permite repartir su población ni copiar sus cifras a cada nueva sección. N/D se conserva como dato no disponible, nunca como cero.</p>
  <p>Campo oficial del indicador seleccionado: <strong>{SOCIO_FIELD_MAPPING[indicator]}</strong>. {indicator==='VIV_CON_AGUA'?'Agua entubada dentro de vivienda o patio/terreno; no acredita potabilidad, continuidad o conexión a red pública.':indicator==='VIV_CON_DRENAJE'?'Incluye drenaje hacia red pública y otras modalidades; no equivale exclusivamente a alcantarillado municipal.':indicator==='ESCOLARIDAD_PROM'?'Grado promedio de escolaridad de población de 15 años y más, con exclusión de grados no especificados. La media no ponderada de valores seccionales asigna el mismo peso a cada sección con dato; no es el promedio ponderado de la población ni un promedio oficial del territorio actual.':indicator==='POB_18MAS'?'Población de 18 años y más no equivale a lista nominal ni padrón electoral.':''}</p>
  <details><summary>Fuentes, campos y límites del cotejo</summary>
   <p><a href={SOCIO_OFFICIAL_URL} target="_blank" rel="noreferrer">Paquete oficial INEGI</a> · <a href={SOCIO_METHOD_URL} target="_blank" rel="noreferrer">Metodología geoelectoral</a></p>
   <p>Referencia descargada y cotejada el {reference.audited}. El cotejo compara los 14 indicadores del archivo completo con una copia separada de valores oficiales; no valida todas las demás fuentes de HEYTI. Fuente completa: {Object.keys(reference.sections).length.toLocaleString('es-MX')} registros históricos. Se conservan aparte los que no se representan en este universo, incluidos otros territorios y posibles geometrías bloqueadas.</p>
   <dl>{SOCIO_INDICATORS.map(i=><div key={i.key}><dt>{i.label}</dt><dd>{SOCIO_FIELD_MAPPING[i.key]}</dd></div>)}</dl>
   <p>Huella SHA256 del CSV oficial de Guanajuato: <span style={{overflowWrap:'anywhere'}}>{reference.officialCsvSha256}</span>. Referencia de cifras; no es una certificación de equivalencia territorial.</p>
   <p>Las relaciones de origen se documentaron parcialmente en INE/CG590/2022 y CGIEEG/039/2024; la creación de 3179 en INE/CG1461/2021. No se han resuelto todos los cambios de límites, reseccionamientos o cortes. No se calculan marginación, ingresos, pobreza ni proyecciones en este bloque.</p>
  </details>
 </section>
}
