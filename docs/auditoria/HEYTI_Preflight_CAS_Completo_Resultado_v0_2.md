# HEYTI — Preflight de carga CAS completa v0.2

**27 de septiembre de 2026.** Análisis local y de sólo lectura de los 15 ZIP originales, 23 CSV SEC y sus 23 CSV CAS. Los SHA-256 de ZIP y CSV CAS se verificaron contra los manifiestos. Se restauró desde el original conservado una copia local incompleta de `INE_SICEE_S_2018_original.zip` y se confirmó que su SHA-256 volvió a coincidir con el manifiesto (`fc83f3e8aaba95357cd49b4bd91ee0171cfe00a66d5bb4cd9b35906cfbe32ee1`). Esa copia de trabajo no altera el archivo original ni cambia conteos anteriores.

| Año | Filas CAS GTO | Celdas de opción | Literales vacíos | CAS `SECCION=0` |
|---|---:|---:|---:|---:|
| 2018 | 67,339 | 1,936,753 | 658,360 | 64 |
| 2021 | 38,817 | 791,751 | 144,959 | 30 |
| 2024 | 73,623 | 1,333,364 | 16,318 | 127 |
| **Total** | **179,779** | **4,061,868** | **819,637** | **221** |

Las 179,779 filas CAS encuentran exactamente una unidad SEC de su serie; hay cero CAS sin unidad y cero identidades SEC ambiguas. Las columnas comunes de opciones suman las 524 del catálogo versionado. Se observaron 17 pares de filas de A 2018 con la misma etiqueta de casilla dentro de la misma sección, pero diferente renglón y votos: la clave técnica completa usa `member_id + source_line`, conservando las dos. En DF 2021 MR y RP, quince filas CAS `SECCION=0` se llaman `P1`, una por distrito: la clave de la unidad especial incluye distrito y evita fundirlas.

El SQL generado carga primero 23 miembros CAS y 179,779 filas `raw_row`; luego crea `casilla_tally` y `casilla_option_vote` en transacciones separadas para cada año. Un control posterior exige 221 CAS especiales, 119 unidades SEC con diferencia de total explicada exactamente por casillas marcadas `ANULADA`, dos filas A 2018 sección 336 C10 preservadas y 15 unidades especiales DF 2021 MR P1 independientes.

**Estado:** preflight local aprobado; SQL generado y hashes cotejados, **sin ejecución PostgreSQL de la carga completa**. El piloto de cinco casillas v0.2 sí pasó en la base temporal de Alex el 26/09. La carga completa puede requerir espacio y tiempo considerables: el SQL CAS descomprimido ocupa ~190 MiB, además de ~68 MiB del SQL SEC y las tablas/índices temporales que albergarán más de cuatro millones de celdas. El ejecutor verifica hashes y elimina su base temporal incluso si un lote falla; si `dropdb` falla lo advierte.
