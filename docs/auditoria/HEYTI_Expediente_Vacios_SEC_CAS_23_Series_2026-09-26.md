# HEYTI — Vacíos no equiparables a cero en el cotejo SEC/CAS

**26 de septiembre de 2026.** Complemento del cotejo reproducible de los 23 CSV seccionales y sus CSV de casilla en 15 ZIP originales de Guanajuato. Se revisaron las 1,189 celdas numéricamente indeterminadas conservando los valores literales en `HEYTI_Cotejo_Secciones_Casillas_23_Series_v0_1.json`.

| Configuración | Celdas | Unidades seccionales de serie | Lectura |
|---|---:|---:|---|
| SEC numérico, alguna CAS vacía | 1,160 | 137 | La suma CAS no se puede certificar tratando el vacío como cero. |
| SEC vacío, alguna CAS numérica | 29 | 4 | 27 celdas de A 2021 en secciones 163 y 2541; dos valores cero de `CAND_IND1` en DL 2021 MR, secciones 1410 y 336. |
| **Total** | **1,189** | **141** | Ninguna celda imputada. |

Los 27 campos de **A 2021, secciones 163 y 2541**, incluyen los dos `TOTAL_VOTOS` vacíos. Todas las casillas de esas dos secciones están marcadas `ANULADA` en `TRIBUNAL`, aunque conservan sus votos anteriores en CAS. La cifra seccional vacía representa ausencia de resultado publicado tras la anulación; no es un total de cero ni debe reconstruirse sumando esas actas.

En **DL 2021 MR, secciones 1410 y 336**, `CAND_IND1` está vacío en SEC mientras una casilla trae el literal `0` y otras casillas de la misma sección están vacías. Un cero aislado no convierte toda la opción seccional en cero. Los 1,160 casos restantes tienen al menos una casilla vacía y una cifra seccional numérica. Son principalmente opciones de combinaciones, pero incluyen otras columnas; la captura cruda queda disponible para inspección por columna y casilla.

## Priorización por casilla

Las 1,160 celdas pendientes se concentran en **173 casillas de serie**, repartidas entre 137 unidades seccionales de serie. En **las 1,160 celdas**, la suma de los valores CAS conocidos coincide con la cifra SEC; esto muestra que la aritmética es compatible con omitir el vacío, pero **no demuestra** que el literal vacío sea un cero. De las 173 casillas, 79 traen `RUTA_ACTA` en el CSV; una ruta es una referencia y no prueba que la imagen del acta esté incluida en el ZIP.

El inventario `HEYTI_Casillas_Con_Vacios_SEC_Numerico_23_Series_2026-09-26.csv` agrupa cada casilla de serie, sus columnas vacías, modalidad, estatus, referencia judicial y ruta de acta cuando existen. La identidad MR/RP permanece separada; una misma casilla física puede figurar en más de una serie.

**Regla de integración:** conservar el literal de cada CAS, el literal SEC y el estatus judicial; distinguir `NULL` de `0`. Para cerrar las 1,160 comparaciones restantes, cotejar el expediente de la casilla vacía y la metodología del corte. La coincidencia eventual entre SEC y la suma de valores CAS conocidos no sería prueba suficiente de que el vacío signifique cero. Ningún dato de `at2730_core` fue cambiado.
