# HEYTI — Cotejo del octavo grupo municipal A2024 — v0.1

Fecha de consolidación: 26 de octubre de 2026.
Alcance: ayuntamientos de Guanajuato 2024; municipios 3, 7, 11, 20, 25, 27 y 34.
Base de ensayo del usuario: heyti_cas_full_probe_d12d6718adb8.
Fuentes crudas: release_id = 10; serie de proyección seccional revisada: series_id = 16.

## Estado de este reporte

Consolidación de las salidas de PowerShell/psql compartidas por el usuario y de los documentos oficiales consultados durante la sesión. Las consultas se ejecutaron en transacciones READ ONLY y terminaron en ROLLBACK. Este reporte no certifica la elección, no selecciona un release para consumo, no modifica fuentes ni autoriza integración en producción.

El cotejo interno CAS–SEC está comprobado para los siete municipios. El alcance documental es distinto por municipio; se detalla abajo. Una suma municipal coincidente no sustituye un cotejo individual exhaustivo.

## Inventario y conciliación interna

| Municipio | CAS | SEC | Votos CAS crudos | Votos SEC | Lista nominal CAS y SEC | CAS anuladas en CSV |
|---|---:|---:|---:|---:|---:|---:|
| 3 San Miguel de Allende | 255 | 106 | 77,964 | 75,386 | 144,253 | 8 |
| 7 Celaya | 669 | 254 | 233,609 | 231,939 | 405,800 | 5 |
| 11 Cortazar | 135 | 56 | 48,698 | 48,698 | 79,948 | 0 |
| 20 León | 2,086 | 778 | 711,277 | 711,277 | 1,272,183 | 0 |
| 25 Purísima del Rincón | 98 | 26 | 34,446 | 34,446 | 62,492 | 0 |
| 27 Salamanca | 385 | 159 | 125,852 | 125,852 | 227,017 | 0 |
| 34 Santa Catarina | 11 | 6 | 3,399 | 3,399 | 4,983 | 0 |
| Total de filas | 3,639 | 1,385 | — | — | — | 13 |

Todos los campos de votos y lista nominal revisados en el inventario fueron numéricos.
Se comprobaron 24,930 cotejos de votos (18 campos × 1,385 secciones) y 1,385 de lista nominal: cobertura inválida 0, campos no numéricos 0, discordancias de votos 0 y discordancias de lista nominal 0.

Para votos, la conciliación excluye CAS marcadas ANULADA. Para lista nominal se conservan todas las CAS. Esto reproduce el corte de los CSV; no acredita que dicho corte incorpore todas las resoluciones posteriores.

San Miguel de Allende: 8 CAS anuladas suman 2,578 votos; 77,964 − 2,578 = 75,386.
Celaya: 5 CAS anuladas suman 1,670 votos; 233,609 − 1,670 = 231,939.
Ambas conciliaciones se comprobaron por sección, sin discordancias de lista nominal.

## Filas SEC0

Los siete municipios tienen una fila SEC0. Se verificó su representación como SPECIAL_SECTION_ROW, section_code = 0 y territorial_section_id vacío/NULL. Se conserva original_identity; no se adjudica una sección territorial ordinaria.

| Municipio | Línea CAS | Línea SEC | Rótulo CAS | Distrito local | LN | Votos |
|---|---:|---:|---|---:|---:|---:|
| 3 | 305 | 497 | VA13 | 9 | 11 | 10 |
| 7 | 793 | 1357 | VA32 | 15 | 17 | 13 |
| 11 | 1662 | 1018 | VA17 | 13 | 2 | 1 |
| 20 | 3260 | 2481 | VA36 | 3 | 33 | 29 |
| 25 | 5722 | 1891 | VA24 | 18 | 2 | 2 |
| 27 | 5915 | 1198 | VA19 | 14 | 10 | 9 |
| 34 | 7116 | 268 | VA39 | 2 | 1 | 1 |

No confundir consistencia CAS–SEC de SEC0 con equivalencia documental de los rótulos 90xx A01.

## Santa Catarina: cotejo documental

Acta 13/2024: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmsc-acta-13.pdf

11 filas × 9 campos = 99 controles numéricos coincidentes: PAN, PRI, PRD, PVEM, PT, MORENA, no registrados, nulos y total. La tabla no proporciona un control separado de MC ni de combinaciones de coalición.

La fila documental 9040 A01 coincide numéricamente con SEC0 VA39 (PAN = 1; total = 1), pero su equivalencia de identidad sigue pendiente. No se certificó documentalmente la LN por casilla mediante este acta.

## Purísima del Rincón: cotejo documental

Acta CMPR 17/2024: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmpr-acta-17.pdf

98 filas × 14 campos = 1,372 controles coincidentes. Incluyen siete partidos, cuatro combinaciones PAN/PRI/PRD, no registrados, nulos y total.
Primer bloque: 31 filas/434 controles. Segundo bloque: 67 filas/938 controles. Cobertura inválida, no numéricos y discordancias: 0.

En 2043 C02 se preservó la lectura no registrados = 9 y nulos = 0, sin invertir columnas.
La fila 9034 A01 / SEC0 VA24 conserva equivalencia de identidad pendiente; su vector numérico coincide (PAN = 1, PVEM = 1, total = 2).
Las columnas de candidaturas independientes y la LN no quedaron documentalmente verificadas por estos 14 controles.

## Cortazar: cotejo documental

Acta CMCT 18/2024: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmct-acta-18.pdf

135 filas × 10 campos = 1,350 controles coincidentes. Campos: siete partidos, coalición agrupada, nulos y total.
COALICION se cotejó contra la suma de las cuatro combinaciones PAN/PRI/PRD del CSV. Esta coincidencia agrupada no valida cada combinación por separado.
El acta no ofrece no registrados como columna separada para este cotejo; no se asumió cero.
La fila 9027 A01 / SEC0 VA17 coincide numéricamente (PVEM = 1, total = 1), con identidad pendiente.
No se extiende esta comprobación a LN ni candidaturas independientes.

## Celaya: vectores documentales y nulidades

Fuentes:
- Acta judicial local TEEG-REV-47/2024, copia oficial: https://oficialiapartes.congresogto.gob.mx/Files/296020/Exp296020-LXV-82634-OF20240809112148.pdf
- SM-JRC-314/2024: https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JRC-0314-2024.pdf

Se cotejaron 8 controles municipales iniciales agrupados contra las 669 CAS, todos coincidentes. Posteriormente se comprobaron 42 controles documentales: 14 campos × 3 cortes (CAS crudo, CAS anulado y SEC rectificado), todos coincidentes.

| Campo | CAS crudo | Anulado | SEC rectificado |
|---|---:|---:|---:|
| PAN | 67,484 | 412 | 67,072 |
| PRI | 8,339 | 83 | 8,256 |
| PRD | 1,373 | 6 | 1,367 |
| PVEM | 11,888 | 87 | 11,801 |
| PT | 4,399 | 35 | 4,364 |
| MC | 20,905 | 133 | 20,772 |
| MORENA | 107,723 | 836 | 106,887 |
| PAN_PRI_PRD | 1,870 | 10 | 1,860 |
| PAN_PRI | 631 | 1 | 630 |
| PAN_PRD | 68 | 0 | 68 |
| PRI_PRD | 40 | 0 | 40 |
| No registrados | 170 | 3 | 167 |
| Nulos | 8,719 | 64 | 8,655 |
| Total | 233,609 | 1,670 | 231,939 |

Las cinco casillas anuladas se cotejaron individualmente: 5 × 14 = 70 valores, cobertura 1 por casilla, no numéricos 0, discordancias 0, las cinco marcas ANULADA correctas y exactamente cinco filas anuladas en CSV.

| Casilla | Línea CAS | Total |
|---|---:|---:|
| 364 B01 | 896 | 293 |
| 398 C01 | 965 | 299 |
| 451 C01 | 1069 | 306 |
| 519 B01 | 1259 | 410 |
| 530 C02 | 1322 | 362 |

No se realizó cotejo documental individual exhaustivo de las 669 CAS. Los conteos anteriores corresponden a pruebas de distinto alcance y no deben sumarse como celdas únicas.

## Salamanca: cobertura documental de las 385 filas

Fuente: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmsa-acta-17.pdf

Resumen municipal: 14 campos × 2 niveles (385 CAS y 159 SEC) = 28 comparaciones documentales coincidentes. Total de ambos niveles: 125,852.

Cotejo individual consolidado, sin duplicar casillas focales ya incluidas en los bloques:
| Bloque | Filas | Controles | Diferencias |
|---|---:|---:|---:|
| Página 9 | 27 | 378 | 1 |
| Página 10, controles corregidos por relectura | 49 | 686 | 0 |
| Página 11 | 49 | 685 | 0 |
| Página 12 | 49 | 686 | 0 |
| Página 13 | 49 | 686 | 0 |
| Página 14 | 49 | 686 | 0 |
| Páginas 15–17 agrupadas | 113 | 1,582 | 0 |
| Total | 385 | 5,389 | 1 |

Resultado: 5,388 valores coincidentes; una discrepancia documental; una celda adicional excluida por lectura dudosa. En todos los bloques: cobertura inválida 0 y no numéricos CSV 0.

### Pendientes documentales

1. 2110 C02, PRI_PRD: tabla final = 0, CSV = 1. El reporte anexo de recuento también muestra 1. La tabla final suma 464 en componentes aunque declara 465; el CSV suma 465 y declara 465. El anexo y la tabla final presentan además distinto valor de MORENA. No se adjudica el voto por consistencia aritmética. Línea CAS 5926; SHA256 4557b59079e67ccf628a7137b20cff6adaf04075b11933880cd3811c8b7c6c3d. La sección concilia CAS–SEC para MORENA (1,043), PRI_PRD (1) y TOTAL_VOTOS (3,147).
2. 2163 C02, PRI_PRD: lectura dudosa de la tabla final. Celda excluida mediante NULL en el control, no en la fuente. No se interpreta como cero ni se incorpora a los 5,389 cotejos.
3. 9035 A01 / SEC0 VA19: equivalencia de identidad pendiente. Sus 14 valores coinciden: PAN 2, PRI 1, MC 1, MORENA 5 y total 9.

### Caso 2252 B / C01

El acta, página 8, explica que los votos de B quedaron contabilizados en C01. Totales documentales cotejados: B = 0, C01 = 450. Ambos coinciden.
Se conservan identidades y listas nominales separadas: B LN = 514; C01 LN = 513.
En CSV ambas filas tienen TRIBUNAL y OBSERVACIONES vacíos. No se marca anulación por inferencia.
Líneas 6256 y 6257; hashes:
- B: e4324aacc9cce5fb7df54ee57aa600a531a8adcd0fec3b41e9c19f15e14588ba
- C01: 01af40c1d6b1013a00f9d37d29f4ac3650b7a283dad726f3f345c900359ee740

Cinco discrepancias iniciales del bloque de página 10 se resolvieron por relectura ampliada como errores de transcripción del control, no como correcciones de CSV: 2122 B (PRI_PRD 0 y nulos 6), 2130 B (PAN_PRI 7), 2141 B (PAN_PRI 1 y nulos 15). El bloque completo de 686 controles se volvió a ejecutar y pasó.

## León: fuente documental incompleta

Fuente examinada: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmle-acta-19.pdf

El PDF tiene 24 páginas y presenta las páginas impresas impares de un acta de 47 páginas; faltan los reversos. Se observaron saltos 9→11→13 y la última página impresa 47. El cierre declara 24 fojas, 23 útiles por ambos lados y una solo por su anverso.

No se dispone de una copia documental completa en la fuente examinada. La búsqueda alternativa de esta sesión no produjo un resumen oficial completo utilizable como control independiente. Los resultados de prensa o agregadores no se utilizaron como controles documentales oficiales.

Se observaron componentes con literales NP y Sin Dato, incluso en filas con total declarado 0. No se sustituyen esos literales por cero.

Estado: conciliación interna CAS–SEC comprobada; cotejo documental exhaustivo pendiente de fuente completa o alternativa oficial. No se certifican documentalmente las 2,086 CAS mediante este archivo parcial. La omisión documental no demuestra por sí misma un error en el CSV.

## San Miguel de Allende: desfase de corte judicial confirmado

Fuentes:
- SM-JDC-517/2024 y acumulados, 3 de septiembre de 2024: https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JDC-0517-2024-
- PDF: https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JDC-0517-2024.pdf
- SUP-REC-22097/2024 y acumulados, 3 de octubre de 2024: https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-22097-2024

La Sala Monterrey restituyó las casillas 156 C01, 172 B01, 191 B01 y 200 E01. El CSV conserva sus cuatro marcas ANULADA y SEC conserva 75,386, correspondiente al corte local.
Se comprobaron 33 controles agrupados (11 campos × 3 cortes) y 44 controles individuales de las cuatro restituidas, todos coincidentes, sin problemas de cobertura ni campos no numéricos.

| Campo | SEC local | Restitución | Federal derivado/documental |
|---|---:|---:|---:|
| PAN | 15,196 | 300 | 15,496 |
| PRI | 25,520 | 493 | 26,013 |
| PRD | 663 | 15 | 678 |
| PVEM | 1,130 | 17 | 1,147 |
| PT | 1,052 | 12 | 1,064 |
| MC | 1,725 | 25 | 1,750 |
| MORENA | 25,031 | 422 | 25,453 |
| CI agrupadas | 1,884 | 27 | 1,911 |
| No registrados | 20 | 1 | 21 |
| Nulos | 3,165 | 59 | 3,224 |
| Total | 75,386 | 1,371 | 76,757 |

CI agrupa CAND_IND_1, CAND_IND_2 y CAND_IND_3; su coincidencia no adjudica separadamente cada columna.
FEDERAL_DERIVADO suma 106 SEC locales y cuatro CAS restituidas: las 110 filas fuente son operandos de cálculo, no 110 secciones.

| Casilla restituida | Línea CAS | Total | Marca CSV |
|---|---:|---:|---|
| 156 C01 | 343 | 361 | ANULADA |
| 172 B01 | 387 | 453 | ANULADA |
| 191 B01 | 442 | 284 | ANULADA |
| 200 E01 | 459 | 273 | ANULADA |

Las otras cuatro casillas anuladas del corte local son 156 C04, 175 C03, 202 B01 y 3213 C02. La restitución de las cuatro anteriores no autoriza borrar todas las anulaciones.

### Dos casillas MODIFICADA

Se cotejó documentalmente PRI en ambas:
- 176 C01: PRI = 111; línea 409; suma de componentes CSV = total CSV = 353.
- 216 C01: PRI = 101; línea 496; suma de componentes CSV = total CSV = 332.

Ambas con cobertura 1, marca MODIFICADA, no numéricos 0 y diferencias 0.
Hashes:
- 176 C01: cb9b595f15d95d29907540edb9dfa3af98fe411ee34b352578ae6a88bf8c2c24
- 216 C01: 6eca1322e0d5892ee2bdbda84eae5f2292dcbb41496f6433e88843aac3c77d4e

El control documental de ese bloque comprende únicamente los dos valores PRI. Los totales y la suma de 16 componentes fueron comprobaciones internas del CSV.
La sentencia refiere tanto 35 como 36 como valor anterior del PRI en 216 C01. Se preserva la inconsistencia narrativa; no se usa ninguno como control definitivo ni se deriva un incremento único desde ese texto.

### Cierre de la cadena consultada

Sala Superior acumuló SUP-REC-22098/2024 y SUP-REC-22312/2024 a SUP-REC-22097/2024 y desechó las demandas por no actualizar el requisito especial de procedencia. Fue un desechamiento sin estudio de fondo; no debe describirse como validación numérica de Sala Superior ni como nueva rectificación. La decisión consultada no revocó la restitución regional.

Estado: BLOQUEADO_POR_DESFASE_DE_CORTE_JUDICIAL. Se conservan 75,386 como valor del release crudo y 76,757 como referencia judicial federal documentada. No se alteró ni promovió una nueva fuente o proyección. Falta preparar una incorporación versionada y controlada que preserve trazabilidad, una vez revisados los demás requisitos de auditoría.
No se realizó cotejo individual exhaustivo de las 255 CAS mediante los controles judiciales focales.

## Continuidad de trabajo

1. Conservar todos los pendientes de grupos anteriores; este reporte no los sustituye ni los cierra.
2. Obtener fuente completa/alternativa oficial de León.
3. Resolver lectura de Salamanca 2163 C02 y discrepancia documental 2110 C02, sin completar valores por inferencia.
4. Resolver equivalencias documentales de SEC0; preservar identidad especial y territorial_section_id NULL.
5. Mantener diferenciados el corte local de SMA y la referencia federal; diseñar después su incorporación versionada, sin editar raw_row.
6. Mantener como parciales los cotejos individuales de Celaya y SMA, aunque los vectores municipales coincidan.
7. Actualizar el registro municipal general y el registro único de pendientes mediante comparación con su versión vigente; no se actualizaron en esta consolidación.

## Método operativo acordado

Agrupar el máximo de filas compatible con lectura documental confiable. Preferir una ejecución por municipio o por conjunto completo de páginas restantes, con resumen y JSON de diferencias. No repetir pruebas aprobadas salvo cambios, errores o incertidumbre nueva. Nunca transcribir controles desde el propio CSV y presentarlos como evidencia independiente.
