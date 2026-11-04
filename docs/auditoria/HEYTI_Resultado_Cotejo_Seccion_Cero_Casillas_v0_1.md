# HEYTI — Resultado del cotejo CAS→SEC para `SECCION=0`

**26 de septiembre de 2026.** Comparación de los miembros `*_CAS.csv` y `*_SEC.csv` contenidos en los 15 ZIP originales, con `ID_ESTADO=11`. Se verificó SHA-256 de cada ZIP y de cada CSV seccional frente al manifiesto; no hubo escritura en PostgreSQL ni transformación de datos de fuente.

| Control | Resultado |
|---|---:|
| Series con `SECCION=0` | 13 |
| Filas SEC=0 examinadas | 137 |
| Filas SEC=0 sin casillas enlazadas | 0 |
| Registros CAS=0 vinculados, sumados por serie | 221 |
| Campos numéricos comparables: suma CAS vs valor SEC | 2,790 |
| Diferencias numéricas | **0** |
| Columnas vacías tanto en SEC como en todas las CAS correspondientes | 60 |
| Campos numéricos indeterminados adicionales | 0 |

La unión usa estado, distrito federal, distrito local, municipio y etiqueta de municipio **dentro de la misma serie**. Compara las columnas electorales literales compartidas, incluidos partidos, combinaciones, votos válidos, nulos, no registrados, `TOTAL_VOTOS` y `LISTA_NOMINAL` cuando están presentes y son enteros. Los 60 vacíos coincidentes se conservan como vacíos; no se contabilizan como ceros ni como una igualdad numérica. Los 221 registros CAS son ocurrencias por serie y modalidad, no actas únicas entre elecciones.

El lector detectó CSV con BOM UTF-8 inicial y bytes internos que requieren CP1252. La primera ejecución produjo tres falsas diferencias al tratar `ï»¿CIRCUNSCRIPCION` como campo numérico. Se corrigió para retirar el BOM antes de CP1252, regeneró el manifiesto y repitió la comparación: cero diferencias. El resultado reproducible detallado está en `HEYTI_Cotejo_Seccion_Cero_Casillas_v0_1.json` y el procedimiento en `HEYTI_Cotejar_Seccion_Cero_Casillas_v0_1.py`.

**Alcance de la conclusión:** las sumas de casillas coinciden con sus filas agregadas `SEC=0` para los campos comparables de estos archivos. No demuestra que sean la versión jurídicamente final de cada acta, ni define por sí mismo las categorías `P`, `VA`, `MEC`, `VM` o `Ve`. Tampoco analiza aún las secciones ordinarias o unidades especiales solo presentes en CAS. Es una puerta de consistencia de fuente; la prueba de DDL en PostgreSQL aislado sigue pendiente.
