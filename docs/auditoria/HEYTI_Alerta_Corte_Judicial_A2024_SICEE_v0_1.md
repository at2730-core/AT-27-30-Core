# HEYTI — Alerta de corte judicial en Ayuntamientos 2024

**27 de septiembre de 2026. Estado: bloqueo de certificación de A2024 para presentación.** No se modificó fuente original, staging ni base viva.

## Contradicción verificable

La [sentencia de Sala Superior SUP-REC-22097/2024 y acumulados](https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-22097-2024) describe que la Sala Regional Monterrey, el 3 de septiembre de 2024, **revocó la nulidad local** de 156 C1, 172 B, 191 B y 200 E1 en la elección del Ayuntamiento de San Miguel de Allende. La Sala Superior desechó los recursos de reconsideración; ello no es un nuevo recuento de los cuatro valores por Sala Superior. El mismo fallo refiere correcciones en 176 C1 y 216 C1.

| Sección / casilla | `TOTAL_VOTOS` CAS SICEE preservado | `TRIBUNAL` CAS SICEE | Referencia del fallo federal |
|---|---:|---|---|
| 156 C01 | 361 | `ANULADA` | Nulidad local revocada por Sala Monterrey |
| 172 B | 453 | `ANULADA` | Nulidad local revocada por Sala Monterrey |
| 191 B | 284 | `ANULADA` | Nulidad local revocada por Sala Monterrey |
| 200 E01 | 273 | `ANULADA` | Nulidad local revocada por Sala Monterrey |

Las cuatro CAS suman 1,371 votos crudos. La [sentencia SM-JDC-517/2024 y acumulados, pp. 63–64](https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JDC-0517-2024.pdf) declara válida esa votación y contiene el cuadro de recomposición. El renglón `ID_MUNICIPIO=3`, San Miguel de Allende, de `AYUNTAMIENTOS_csv/2024_SEE_AYUN_GTO_MUN.csv` dentro de `INE_SICEE_GTO_PEL_2024_original.zip` reproduce **exactamente el cómputo modificado por el Tribunal Local antes de restituir las cuatro casillas**:

| Concepto | SICEE municipal / Tribunal Local | Adición ordenada por Sala Monterrey | Cómputo federal recompuesto |
|---|---:|---:|---:|
| PAN | 15,196 | 300 | 15,496 |
| PRI | 25,520 | 493 | 26,013 |
| PRD | 663 | 15 | 678 |
| PVEM | 1,130 | 17 | 1,147 |
| PT | 1,052 | 12 | 1,064 |
| MC | 1,725 | 25 | 1,750 |
| MORENA | 25,031 | 422 | 25,453 |
| Candidatura independiente | 1,884 | 27 | 1,911 |
| No registrados | 20 | 1 | 21 |
| Nulos | 3,165 | 59 | 3,224 |
| **Total** | **75,386** | **1,371** | **76,757** |

La coincidencia de las diez categorías y el total, junto con la marca `ANULADA` de las cuatro CAS, confirma que **este ZIP SICEE conserva el corte local previo a la recomposición federal para ese municipio**. No se infiere de ello la fecha exacta de publicación del ZIP ni que todos los municipios compartan ese corte. Para este caso sí existe un cómputo posterior expresamente fijado en sentencia; aún corresponde verificar publicaciones oficiales posteriores y documentar la firmeza procesal antes de certificar la serie completa.

### Consistencia entre niveles dentro del ZIP

El mismo `TOTAL_VOTOS=75,386` aparece en el registro MUN y en la suma de las 106 filas SEC del municipio (incluida la identidad especial, si corresponde). Las 255 filas CAS suman 77,964 en valores crudos; al excluir las CAS marcadas `TRIBUNAL=ANULADA`, suman exactamente 75,386. La diferencia de 2,578 corresponde al conjunto de anulaciones que este ZIP aplica, **no únicamente** a las cuatro casillas restituidas. En la sección 156, además de 156 C1 (361), figura 156 C4 (343) como anulada; la sentencia examinada restituye C1, no C4. Por ello no procede reactivar por analogía todas las casillas anuladas ni reemplazar indiscriminadamente las filas SEC.

La prueba anterior se reproduce leyendo las tres tablas originales `MUN.csv`, `SEC.csv` y `CAS.csv` del mismo ZIP, filtrando `ID_MUNICIPIO=3`, sumando `TOTAL_VOTOS` y, para el segundo total CAS, omitiendo únicamente `TRIBUNAL=ANULADA`. Es un cotejo del municipio, no una validación de las otras 45 municipalidades.

## Consecuencia para HEYTI

La preferencia estadística por SICEE queda **subordinada a la validación jurisdiccional por elección y release**. A2024 no debe declararse `CERTIFIED_FINAL`, usarse para ganador/participación o sustituir el cómputo judicial en San Miguel de Allende con este ZIP. Preservar el ZIP por hash, marcar incidencia `JUDICIAL_CUT_CONFLICT`, mantener `presentation_selection=UNDECIDED` y cotejar las publicaciones posteriores oficiales. Comprobar si SICEE ofreció otra versión corregida y documentar fecha/hash antes de considerar sustitución. La sentencia sirve para contrastar el municipio; todavía no se ha generado ni validado una corrección de todas las unidades SEC/CAS del ZIP.

Este hallazgo **no demuestra** que todas las 23 series SICEE tengan el mismo problema. Sí invalida la inferencia general de que la presentación institucional del SICEE certifica por sí sola cada ZIP descargado.
