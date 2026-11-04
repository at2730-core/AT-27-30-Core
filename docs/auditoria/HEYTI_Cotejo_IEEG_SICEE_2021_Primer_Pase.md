# HEYTI — Cotejo IEEG/SICEE 2021, primer pase

**27 de septiembre de 2026.** Lectura local de ZIP preservados; sin escritura a la base viva. Comparación exploratoria de PAN, PRI, PVEM, MORENA y total de votos por sección ordinaria. Las cifras siguientes no son certificación del corte.

## Método y límites

- IEEG: `IEEG_Computos_2021_original.zip`, `GTO_AYUN_2021.csv` y `GTO_DIP_LOC_2021.csv`; ocho líneas de metadatos preceden las filas CAS. Total IEEG se llama `TOTAL_VOTOS_CALCULADO`.
- SICEE: `INE_SICEE_GTO_PEL_2021_original.zip`, `2021_SEE_AYUN_GTO_SEC.csv` y `2021_SEE_DIP_LOC_MR_GTO_SEC.csv`.
- Se agruparon filas IEEG por sección y se compararon con SEC SICEE. Cualquier celda con vacío o `-` en alguna fila IEEG, o sin número en SEC, quedó **indeterminada** en vez de tratarse como cero.
- El CSV IEEG de diputaciones contiene 62 filas de casilla especial tipo `S` en 31 secciones, con dos filas por identidad textual de casilla en ejemplos examinados. No se puede separar de forma segura MR y RP con la llave textual disponible; se excluyeron esas **31 secciones completas** de este primer cotejo MR. No se evaluó lista nominal ni secciones especiales 9000+.

| Elección | Pares de sección examinados | Secciones con alguna diferencia numérica determinada | Celdas numéricas distintas PAN/PRI/PVEM/MORENA/total | Comparaciones indeterminadas PAN/PRI/PVEM/MORENA/total |
|---|---:|---:|---|---|
| Ayuntamientos | 3,159 | 33 | 28 / 29 / 28 / 29 / 32 | 11 / 11 / 45 / 26 / 11 |
| Diputaciones locales MR, sin 31 secciones con S | 3,128 | 13 | 11 / 12 / 12 / 11 / 13 | 9 / 9 / 9 / 9 / 9 |

Una sección con diferencia numérica puede tener otras opciones indeterminadas. Los conteos no deben sumarse como si fueran secciones únicas. El primer registro IEEG 2021 muestra `10/06/2021 10:00 (UTC-5)` dentro del CSV, mientras el ZIP interno está rotulado `20210610_1200`; conservamos ambos literales sin inferir equivalencia horaria o judicial.

## Próxima comprobación

En una segunda revisión de las 31 filas SICEE MR de casilla especial `S`, la comparación de PAN, PRI, PRD, PVEM, PT, MC, MORENA, PES, RSP, FXM, PRI_PRD y TOTAL identificó **23 filas IEEG de forma única**, dejó **2 con empate** (248 y 2547: las dos filas IEEG igualan los campos comparados) y **6 sin coincidencia exacta**. En 1282, 1518, 1866, 2270 y 2794 SICEE MR tiene total `0` con opción PAN vacía, mientras una de las dos filas IEEG contiene `-`; no se presume igualdad entre vacío, guion y cero. En 2193 MR tiene PAN 148 y total 322, frente a una fila IEEG PAN 138 y total 322 y otra con `-`. Esto es una pista de identidad, no una asignación segura de todas las filas; se mantienen excluidas las 31 secciones del resultado MR agregado.

De las **32 diferencias numéricas determinadas de total** en ayuntamientos, **18** coinciden exactamente con la suma de casillas SICEE `TRIBUNAL=ANULADA`. Las otras **14** se desglosan así:

| Patrón observado en IEEG | Secciones | Alcance |
|---|---|---|
| Clave `CLAVE_ACTA` repetida, con una fila adicional por sección | 164, 835, 1037, 1940, 2017, 2018, 2466, 2613, 2797, 2959 | Siete pares repiten los votos examinados; en 2017, 2466 y 2613 los dos renglones de la misma clave contienen valores distintos. No deduplicar sin adjudicar la fila. |
| Mismo número de filas CAS en ambos archivos, valor de casilla distinto | 709, 1944, 2001, 2876 | Comparar identidad y acta de origen para explicar las diferencias de total (-9, +1, +1, +1 respectivamente, IEEG menos SEC SICEE). |

En las cuatro casillas con igual número de filas, la identidad textual y los cambios literales son:

| Sección/casilla | IEEG → SICEE | Campo que explica el total |
|---|---|---|
| 709 E01 | 122 → 131 | RSP 1 → 10 |
| 1944 B | 158 → 157 | NULOS 2 → 1 |
| 2001 C01 | 159 → 158 | NULOS 2 → 1 |
| 2876 C01 | 129 → 128 | MORENA 37 → 36 |

En las tres claves repetidas con votos diferentes, SICEE CAS coincide con **una** de las filas IEEG: sección 2017 B (151 frente a la otra fila 173), 2466 C01 (356 frente a 276) y 2613 B (330 frente a 325). Esta coincidencia ayuda a identificar la fila representada en SICEE, pero no autoriza eliminar la otra sin expediente de origen. Los CAS SICEE examinados de estas siete secciones no aportan `RUTA_ACTA` ni marca `TRIBUNAL` para resolver el cambio documental.

La sección restante de las 33 afectadas difiere en otra opción, sin diferencia determinada de total. La coincidencia aritmética en las 18 anulaciones no sustituye la consulta de sentencia ni acta. Las diez claves repetidas no autorizan borrar registros de la fuente preservada.

Construir identidad CAS explícita para las casillas especiales de 2021 y cotejar los campos de estado/tribunal de SICEE contra cada diferencia determinada. Examinar las 11/9 secciones con totales indeterminados y los casos A21 163/2541 y DL21 1080 sin imputar cero. Solicitar o localizar la documentación de versión y resoluciones correspondiente antes de seleccionar release para presentación.

## Diputaciones locales MR: 13 secciones con total distinto

El cotejo CAS acota los patrones: **10 secciones** (341, 356, 560, 1078, 1177, 1320, 1342, 1483, 1492, 1612) tienen una `CLAVE_ACTA` repetida y una fila IEEG adicional. En 1320, 1177 y 1492, las dos filas de la misma clave presentan totales distintos; no procede deduplicar sin expediente. La sección **2251** difiere por 235 votos, exactamente el total de una casilla SICEE marcada `ANULADA`. Las otras dos tienen el mismo número de casillas pero valores distintos: **2595 C02** total IEEG 132 frente a SICEE 231 y **2699 E01** 136 frente a 150. Estos dos CAS SICEE no muestran marca `TRIBUNAL`. Las 31 secciones con casillas especiales MR/RP siguen excluidas de este conteo.

## Lista nominal 2021

En SICEE, la suma de LN CAS reproduce LN SEC en las 3,159 secciones ordinarias de **A, DL MR y DL RP**, sin vacíos. En IEEG ayuntamientos hay 31 casillas especiales con LN 1,000; sus 31 homólogas SICEE tienen LN 0. Excluyendo las diez secciones IEEG con clave de acta repetida, entre 3,149 secciones comparables la LN coincide en 3,118 y difiere en esas 31, exactamente +1,000 IEEG menos SICEE cada una. En diputaciones IEEG, al excluir secciones con claves repetidas y casillas especiales MR/RP no adjudicadas, las **3,117 secciones restantes** coinciden en LN con SICEE MR. Esto contrasta con las 2,654 diferencias residuales de LN 2024; no extrapolar el patrón 2021 al corte posterior.
