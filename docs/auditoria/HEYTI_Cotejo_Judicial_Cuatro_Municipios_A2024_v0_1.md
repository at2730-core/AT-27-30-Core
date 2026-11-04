# HEYTI — Cotejo judicial focalizado de cuatro municipios A2024

**27 de septiembre de 2026.** Se contrastaron las marcas CAS y `TOTAL_VOTOS` MUN del ZIP preservado `INE_SICEE_GTO_PEL_2024_original.zip` con los efectos de resoluciones oficiales posteriores al cómputo inicial IEEG. Sin cambios a la base viva.

| Municipio | SICEE MUN | CAS `ANULADA` en SICEE | Comprobación jurisdiccional localizada | Estado del corte para este municipio |
|---|---:|---:|---|---|
| Celaya | **231,939** | 5 | Sala Monterrey confirmó la nulidad de cinco casillas determinada por el tribunal local, SM-JRC-314/2024. El cotejo inicial IEEG − SICEE fue 1,670 votos, igual al total de las cinco CAS anuladas. | Marcas y delta concordantes; revisar vector/cómputo judicial completo |
| Irapuato | **237,278** | 34 | Tribunal local anuló 32; Sala Monterrey añadió **1037 C2 (321 votos)** y **1063 B (439)**: 238,038 − 760 = **237,278**, SM-JRC-308/2024. Ambas aparecen `ANULADA` en el ZIP. | Total y dos adiciones concordantes con sentencia federal |
| Silao de la Victoria | **75,031** | 11 | El tribunal local anuló **2662 C1**; Sala Monterrey anuló otras diez (**2656 B, 2688 B, 2695 C2, 2699 B, 2700 B, 2702 C3, 2709 C4, 2710 C9, 2712 C1, 2725 B**), SM-JRC-262/2024. Las once aparecen `ANULADA` en el ZIP; 78,492 − 3,461 = **75,031**. | Total y marcas concordantes con secuencia local y federal revisada |
| San Miguel de Allende | **75,386** | 8 | Sala Monterrey restituyó **156 C1, 172 B, 191 B, 200 E1**, aún `ANULADA` en el ZIP; 75,386 + 1,371 = **76,757**, SM-JDC-517/2024. | **Conflicto judicial confirmado** |

## Fuentes oficiales

- Celaya: https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JRC-0314-2024-
- Irapuato: https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JRC-0308-2024-
- Silao: https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JRC-0262-2024.pdf ; documentación oficial del IEEG reproducida en https://oficialiapartes.congresogto.gob.mx/Files/299929/Exp299929-LXVI-32520241002150924.pdf
- San Miguel de Allende: https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JDC-0517-2024.pdf

## Interpretación y pendientes

Las discrepancias frente al cómputo inicial IEEG se localizan en cuatro municipios. Para tres, las marcas revisadas son compatibles con resoluciones judiciales; por tanto, **no corresponde descartar globalmente SICEE**. Para San Miguel existe contradicción directa con la recomposición federal. Esta revisión de cuatro expedientes no certifica la situación judicial de los otros 42 municipios ni el release completo. Mantener A2024 en `BLOCKED_JUDICIAL_CUT_CONFLICT` y `presentation_selection=UNDECIDED` hasta terminar verificación municipal, firmeza procesal y procedencia del archivo. No mezclar cifras de cortes distintos en una misma serie presentada como definitiva.

### Reconciliación exacta de San Miguel de Allende

La sentencia federal SM-JDC-517/2024 y acumulados, de 03/09/2024, especifica las cuatro casillas restituidas y el cómputo municipal modificado. En `2024_SEE_AYUN_GTO_CAS.csv` del ZIP SICEE citado, las cuatro claves `(ID_MUNICIPIO=3, SECCION, TIPO_CASILLA, ID_CASILLA, EXT_CONTIGUA=0)` aparecen con los siguientes votos crudos, pero todas conservan `TRIBUNAL=ANULADA` con referencia a la resolución **local** TEEG-REV-45/2024 y acumulados:

| Casilla | PAN | PRI | PRD | PVEM | PT | MC | MORENA | CAND_IND_2 | No reg. | Nulos | Total |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 156 C1 | 70 | 124 | 6 | 4 | 3 | 11 | 116 | 10 | 0 | 17 | 361 |
| 172 B | 87 | 179 | 3 | 2 | 0 | 6 | 156 | 11 | 1 | 8 | 453 |
| 191 B | 70 | 104 | 2 | 5 | 8 | 3 | 67 | 2 | 0 | 23 | 284 |
| 200 E1 (`EXT_CONTIGUA=0`) | 73 | 86 | 4 | 6 | 1 | 5 | 83 | 4 | 0 | 11 | 273 |
| **Suma restituida** | **300** | **493** | **15** | **17** | **12** | **25** | **422** | **27** | **1** | **59** | **1,371** |

La fila `200 E1` con `EXT_CONTIGUA=1` es otra casilla (303 votos, `Paquete no entregado`) y **no** forma parte de este ajuste. El campo `CAND_IND_2`, no `CAND_IND_1`, corresponde a la candidatura independiente de esta elección municipal. La suma y los diez incrementos reproducen exactamente el cuadro de efectos de la sentencia. El SICEE MUN conserva 75,386; la sentencia establece **75,386 + 1,371 = 76,757** y los nuevos totales por opción. La evidencia permite definir una **reconciliación judicial derivada y trazable**, pero no sobrescribir el ZIP original ni declarar que todo el paquete A2024 está actualizado; tampoco se ha encontrado en esta revisión un CSV oficial posterior del INE/IEEG que ya publique esa corrección.

**Control de agregación del propio ZIP:** en San Miguel hay 255 CAS, de las cuales 8 están `TRIBUNAL=ANULADA` y 2 `TRIBUNAL=MODIFICADA`. La suma de `TOTAL_VOTOS` crudo de las 255 es **77,964**; las ocho anuladas suman **2,578** y las otras 247 suman **75,386**, exactamente el MUN SICEE. Las cuatro restituidas suman 1,371; las otras cuatro anuladas suman **1,207** y continúan fuera del resultado judicial. Por ello, la operación reproducible para este caso es **75,386 + 1,371 = 76,757**. Sumar indiscriminadamente todas las CAS daría 77,964 e introduciría 1,207 votos de casillas que permanecen anuladas. Este control usa el `TOTAL_VOTOS` ya publicado de las dos filas `MODIFICADA`; no reconstruye su acta previa.

**Puente con el cómputo inicial IEEG:** en `09062024_1200_COMPUTOS_AYUN_GTO.zip/GTO_AYUN_2024.csv` las cuatro casillas restituidas constan como `CONTABILIZADA=1`, con exactamente 361, 453, 284 y 273 votos. El archivo inicial suma **77,790** en las 255 filas municipales. Frente a sus homólogas SICEE, las casillas modificadas 176 C1 y 216 C1 pasan de **253 a 353** y de **258 a 332**, respectivamente: incremento neto **174**. Así se reproduce el resultado federal también desde el corte inicial: **77,790 − 1,207 (las cuatro anulaciones que subsisten) + 174 (dos modificaciones) = 76,757**. La diferencia entre el IEEG inicial y el agregado SICEE local es **2,404 = 2,578 − 174**. La diferencia entre IEEG inicial y resultado federal es **1,033 = 1,207 − 174**. Esta igualdad de totales no implica que el corte inicial IEEG sea definitivo; las versiones difieren precisamente por efectos judiciales. Para las cuatro secciones restituidas, el total SICEE SEC previo y el total derivado al reintegrar la casilla son, respectivamente, **156: 1,515→1,876; 172: 1,964→2,417; 191: 296→580; 200: 1,301→1,574**. Estos últimos valores son una derivación aritmética, no filas publicadas por SICEE.

**Identidad de casilla especial:** al emparejar las 255 filas mediante la clave literal `(sección, tipo, número, extensión)`, quedan una fila exclusiva en cada CSV: IEEG `9023 A1` y SICEE `SEC=0 A13`. Ambas tienen el mismo vector de votos (PRI 2, MORENA 6, nulos 2, total 10) y lista nominal 11. Por tanto, el desfase de claves **no añade una diferencia de votos** al puente municipal; es compatible con la distinta codificación de una casilla especial. No se debe convertir automáticamente `9023` en `0` ni `A1` en `A13` para otras filas sin un catálogo de correspondencia oficial.

**Recurso posterior localizado:** la Sala Superior resolvió el 03/10/2024 los expedientes SUP-REC-22097/2024 y acumulados SUP-REC-22098/2024 y SUP-REC-22312/2024 (https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-22097-2024). Desechó las tres demandas por incumplir el requisito especial de procedencia, **sin estudio de fondo**; por ello no alteró la recomposición del 03/09/2024 de la Sala Monterrey. La cadena judicial localizada respalda mantener 76,757 como último cómputo judicial identificado para San Miguel; no convierte en correcto el agregado 75,386 del ZIP SICEE ni certifica por sí sola los otros 45 municipios.

Los cinco CSV de `AYUNTAMIENTOS_csv` conservan dentro del ZIP la marca `2024-11-19 19:07:00`. Esa marca de entrada ZIP es posterior a los fallos revisados, pero **no acredita fecha de publicación, actualización de contenido ni ejecución uniforme de sentencias**. El contenido de San Miguel contradice directamente su sentencia. La página pública del INE describe descargas SICEE por proceso, pero no aporta en ese texto un historial de versiones/hashes del ZIP específico: https://ine.mx/voto-y-elecciones/resultados-electorales/. La búsqueda realizada no identificó una versión corregida verificable; esto no prueba que no exista.
