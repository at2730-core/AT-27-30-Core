# HEYTI — auditoría electoral preliminar 2018–2024

Fecha: 2026-09-24. Alcance: cotejo interno y primera conciliación contra el archivo oficial INE 2021; sin modificación de datos.

ZIP SHA-256: `2d5727a14766fd0c3e565bf23ad5fd7d63ce7ddee52eb3e58d65846237af5c59`. Maestra: 3310 registros, 3310 secciones únicas.

| Elección | Año | Secciones derivadas con año | Secciones con alguna diferencia respecto a maestra |
|---|---:|---:|---:|
| A | 2018 | 3137 | 37 |
| A | 2021 | 3159 | 75 |
| A | 2024 | 3257 | 0 |
| DF | 2018 | 3137 | 0 |
| DF | 2021 | 3160 | 0 |
| DF | 2024 | 3233 | 2574 |
| DL | 2018 | 3137 | 29 |
| DL | 2021 | 3159 | 375 |
| DL | 2024 | 3254 | 0 |
| G | 2018 | 3137 | 0 |
| G | 2024 | 3255 | 3254 |
| S | 2018 | 3137 | 0 |
| S | 2024 | 3234 | 2684 |
| P | 2018 | 3137 | 0 |
| P | 2024 | 3234 | 2454 |

## Hallazgos que requieren resolución

- DF 2021: maestra contiene `21DF_TOTAL` y `21DF_LN`, pero no columnas `21DF_PAN/PRI/PVEM/MORENA`; derivado DF sí tiene esos votos para 2021. Conservarlos, revisar procedencia y cotejar con cómputos INE.
- La mera presencia de un campo en 3,310 registros no significa cobertura histórica: hay secciones sin elección en los derivados, ceros y secciones históricas.
- Secciones presentes solo en derivados: DF `0`; G `9042`; S y P `4074`. Verificar identidad territorial y vigencia antes de asignar o descartar.
- Ejemplos de discrepancia: sección 332, DF 2024, PAN: maestra 129, derivado 301; sección 754, DL 2021, PAN: maestra 644, derivado 470.
- Las discrepancias pueden deberse a homologación territorial, transformación o versiones de fuente. Esta auditoría no determina qué cifra es oficial.
- Un bloque de Análisis Territorial espera arreglos por puesto, pero estos derivados son objetos `{meta,secciones}`. Verificar ejecución antes de migrar UI.

## Fuentes oficiales para el cotejo

- INE Cómputos Distritales 2021: https://computos2021.ine.mx/base-de-datos (declara `Diputaciones.csv` por acta y `LEEME.txt`). ZIP oficial recibido del usuario y verificado en esta sesión.
- INE SICEE: https://sicee.ine.mx/
- IEEG resultados: https://ieeg.mx/resultados-de-elecciones/

## Puerta de integración

Obtener descargas originales de cómputos 2018/2021/2024; registrar URL, fecha, hash y diccionario; reconciliar por elección, año, sección histórica y tratamiento de coaliciones; contrastar con maestra y derivados; solo después proponer cambios a HEYTI-CORE. 2015 fuera del alcance operativo.

## Conciliación inicial con cómputos INE DF 2021

Archivo aportado: `DF_2021_BD.zip`; SHA-256 `6b7a4ad69795de301b9ace72e41e668834e0f2000341840aa10d5db1d576c456`. ZIP exterior e interior pasan prueba de integridad. Corte del CSV: 11/06/2021 10:00 (UTC−5), 163,666/163,666 actas nacionales. Contiene `diputaciones.csv`, archivo de candidaturas y `LEEME.txt`. `diputaciones.csv` está codificado en Latin-1, separado por `|` y tiene seis filas preliminares antes del encabezado tabular.

Filtro `ID_ESTADO=11`: 7,791 filas de actas, 15 distritos, 3,160 claves de sección (incluye sección `0000` con actas P). Las 3,160 claves coinciden exactamente con las claves de DF 2021 del derivado. La suma directa de votos por sección coincide con `DF.json` en 3,130 secciones y difiere en 30. La lista nominal coincide en 3,159; la diferencia es sección `0`, que agrupa actas P de 15 distritos y no representa una sección territorial ordinaria.

En 29 de las 30 secciones discordantes existen varias actas con la misma `CLAVE_CASILLA`; 28 de esos casos involucran actas S y uno corresponde a sección 0 con actas P de distintos distritos. La sección 218 difiere incluso sin clave de casilla repetida: la maestra/derivado excluye una acta C de 304 votos, mientras su LN sí se suma. Por ejemplo, sección 754 tiene dos actas S con idéntica clave de casilla y votos distintos; el derivado conserva solo una para votos. En secciones 967 y 2381 el derivado conserva la otra acta S. Por ello no hay una regla de deduplicación universal comprobada y no corresponde reemplazar automáticamente los valores.

**Estado al primer corte:** archivo oficial preservado y diferencias caracterizadas. La regla para MR de actas especiales se resolvió en la actualización siguiente. Persisten sección 218, prisión preventiva, coaliciones y cotejo con el modelo HEYTI-CORE. No se integraron cifras.

## Desglose de las 30 diferencias DF 2021

| Patrón observado al comparar votos `DF.json` con actas INE | Secciones |
|---|---:|
| Actas S: derivado suma la primera de dos actas con idéntica clave de casilla | 25 |
| Actas S: derivado suma la segunda de dos actas con idéntica clave de casilla | 3 |
| Sección 0: actas P de 15 distritos con una misma clave de casilla; derivado retiene únicamente los 14 votos de un distrito | 1 |
| Sección 218: derivado omite votos de un acta C (304), pero su lista nominal sí está incluida | 1 |

Las 28 secciones con dos actas S son: 81, 157, 172, 175, 291, 444, 613, 754, 967, 972, 982, 1282, 1518, 1570, 1729, 1927, 2062, 2193, 2270, 2381, 2450, 2507, 2547, 2620, 2657, 2833, 2919 y 3171. En 967, 1282 y 2381 el derivado incorpora la segunda; en las demás, la primera. La clave de casilla por sí sola no identifica inequívocamente el acta.

La clasificación anterior es descriptiva; la regla por principio electoral se resuelve en la actualización siguiente. Conservar `CLAVE_ACTA`, distrito, sección, tipo y votos. La sección 218 requiere revisión independiente de su acta C.

## Regla confirmada: DF 2021 por mayoría relativa

La columna `NUM_ACTA_IMPRESO` del CSV marca 31 actas especiales como `2EMR` y otras 31 como `2ERP`; el orden de estas dos actas cambia entre secciones. Una sentencia del TEPJF (SX-JIN-37/2021 y acumulado, párrafos 132–140, https://www.te.gob.mx/media/SentenciasN/pdf/xalapa/SX-JIN-0037-2021.pdf) explica que la base contiene ambas modalidades y que el cómputo de mayoría relativa excluye las actas `2ERP`. La regla reproducible es filtrar `ID_ESTADO=11`, agregar las actas normales `2` y especiales `2EMR` por sección, preservar las `2ERP` como evidencia de otra modalidad, y tratar `SECCION=0000` por distrito y tipo P, fuera de la agregación territorial ordinaria.

Aplicada esa regla a las 3,159 secciones ordinarias de Guanajuato, `DF.json` coincide exactamente en PAN, PRI, PVEM, MORENA y VOTOS en **3,158** secciones; la lista nominal coincide en **3,159**. Única excepción: sección **218** (distrito federal 2), con tres actas `2`: B 301 votos, C 304 y E 313. El archivo INE suma 918 votos; el derivado contiene 614 = B+E, pero LN 1,872 = B+C+E. Por partido INE vs derivado: PAN 196 vs 138; PRI 279 vs 189; PVEM 35 vs 24; MORENA 245 vs 156. Diferencia exacta del acta C. Requiere revisión de identidad y validación en cómputo oficial antes de corregir maestra o derivado.

No se ha verificado todavía la regla de asignación de votos de coalición a partidos ni la reconciliación con las tablas de HEYTI-CORE. La regla MR aquí documentada no autoriza mezclar `2ERP` ni alterar la fuente sin expediente de corrección.

## Expediente puntual de corrección candidata: DF 2021, sección 218

El CSV del INE, distrito federal 2, contiene las actas B `110218B010050262` (301 votos, LN 572), C `110218C010046679` (304 votos, LN 571) y E `110218E010053100` (313 votos, LN 729). Las tres tienen `NUM_ACTA_IMPRESO=2` y no son `2ERP`. Los votos de C por columna directa son PAN 58, PRI 90, PVEM 11 y MORENA 89. La maestra y `DF.json` contienen exactamente B+E para votos, pero B+C+E para LN.

| Campo | Maestra y derivado | Suma INE de actas MR | Incremento candidato |
|---|---:|---:|---:|
| PAN | 138 | 196 | 58 |
| PRI | 189 | 279 | 90 |
| PVEM | 24 | 35 | 11 |
| MORENA | 156 | 245 | 89 |
| VOTOS | 614 | 918 | 304 |
| LN | 1,872 | 1,872 | 0 |

Las columnas por partido del CSV son votos directos asentados en acta; el CSV conserva en columnas distintas las combinaciones de coalición (`PAN-PRI`, `PVEM-PT-MORENA`, etc.). La concordancia de 3,158 secciones se refiere exclusivamente a esas cuatro columnas directas, al total y a LN; no acredita una regla de redistribución de votos de coalición. La sección 218 es **corrección candidata documentada**, no cambio aplicado.

**Siguiente puerta:** contrastar el acta C y el total en la consulta oficial de la sección o el acta de cómputo del distrito 2, luego proponer ajuste versionado de `21DF_TOTAL` y de DF 2021 por partido. Antes de ejecutar cambios en la base de HEYTI, auditar el repositorio y reconciliar fuente → DB → Capability → Runtime → Materialización con casos dorados.

## Nuevo bloque oficial IEEG 2021: Ayuntamiento y Diputación Local

Descarga original: https://computosgto2021.ieeg.mx/assets/basedatos/20210610_1200_COM_GTO.zip; conservada como `IEEG_Computos_2021_original.zip`; SHA-256 `d0bd3003629cd2a51bdb5e439ef19e7bd6e0668ff3eada3e0b08680087b77f67`. ZIP exterior y dos ZIP internos verificados sin errores. Contiene `GTO_AYUN_2021.csv` y `GTO_DIP_LOC_2021.csv` y catálogos de candidaturas. Nombre de paquete y portal: corte 12:00; ambos CSV declaran 10/06/2021 10:00 (UTC−5); no resolver esa diferencia de metadatos sin evidencia. Archivos CSV en Latin-1, delimitados por coma, con filas de encabezado previas.

| Elección | Filas CSV | Claves de sección CSV/derivado | Filas especiales S | Secciones que difieren en VOTOS tras suma simple |
|---|---:|---:|---:|---:|
| A 2021 | 7,755 | 3,159 / 3,159 | 31 | 43 |
| DL 2021 | 7,787 | 3,159 / 3,159 | 62 | 45 |

Estas cifras son una **comparación exploratoria**, no un conteo de errores: hay celdas con guion `-` y valores vacíos que la suma exploratoria omitió. Para A aparecen 9 guiones en TOTAL; para DL, 21. DL tiene dos filas S por varias claves de casilla, sin un campo explícito `2EMR/2ERP` en este CSV. La regla federal no se traslada automáticamente al formato local. Se requiere clasificación de actas y contraste con el portal IEEG antes de proponer ajustes.

En la maestra, la presencia de columnas de 2021 para A y DL en 3,310 filas no equivale a 3,310 secciones electorales con resultados: los derivados y CSV oficiales solo exponen 3,159 claves en cada elección. No crear votos para secciones sin acta. No hay elección G, S ni P en 2021 dentro del material entregado; ausencia esperada por calendario, no falta de datos.

## Alcance de la comparación local 2021 y contrato de cobertura partidaria

Los CSV declaran 10:00 y el portal muestra 12:00; no está comprobado que los registros fila a fila correspondan al mismo corte. `GTO_AYUN_2021.csv` declara 2,021,103 votos y `GTO_DIP_LOC_2021.csv` declara 2,025,062; el portal de Diputaciones Locales visible a las 12:00 muestra 2,021,663 votos de mayoría relativa y 2,025,062 al sumar también casillas especiales RP. La coincidencia del 2,025,062 muestra que una diferencia de encabezado o de modalidad puede explicar discrepancias; no demuestra por sí sola que el contenido por acta sea idéntico. La caracterización 43/45 es exploratoria y no equivale a 43/45 errores. Es imprescindible comparar conceptos electorales equivalentes, horas de corte y campo de modalidad; celdas `-` conservan estado de dato no numérico, no se convierten automáticamente en cero.

Los CSV oficiales locales 2021 incluyen como columnas separadas PAN, PRI, PRD, PVEM, PT, MC, MORENA, NA_Gto, PES, RSP, FXM, candidaturas independientes cuando corresponden, la combinación `PRI_PRD`, no registrados, nulos, total y LN. La maestra actual solo conserva cuatro partidos (PAN, PRI, PVEM, MORENA) y total/LN; por ello **no es una representación completa de las actas** aun donde esos cuatro partidos concuerdan.

**Contrato objetivo propuesto para la migración:** preservar cada acta original y su procedencia (autoridad, URL, hash, corte, elección, año, distrito, sección histórica, casilla, identificador de acta y modalidad). Guardar un resultado por opción tal como figura en el acta: partido individual, combinación de coalición, candidatura independiente, no registrados, nulos y total, sin distribuir votos combinados de forma implícita. La vista agregada por sección tendrá semántica de MR/RP explícita y no mezclará esos principios. Una vista de compatibilidad podrá exponer las cuatro columnas antiguas, señalando que son un subconjunto. Definir reglas de distribución de coaliciones solo si las exige un indicador y tras documentarlas por elección. No incorporar 2015 en esta migración.

## Hallazgo local 2021: claves de acta repetidas y valores en conflicto

Se agruparon las filas por `(SECCION, CLAVE_CASILLA)` dentro de cada elección, sin colapsar registros. En A 2021 hay 10 grupos repetidos, 7 de filas idénticas y 3 con valores distintos; los 10 son casillas ordinarias. En DL 2021 hay 42 grupos repetidos: 7 idénticos y 35 con diferencias en al menos alguna columna; 11 grupos corresponden exclusivamente a casillas no especiales. Treinta y dos grupos DL tienen totales de votos distintos. Entre los grupos DL se incluyen parejas especiales que podrían representar modalidades distintas, pero el CSV local no contiene la marca `2EMR/2ERP` que sí trae el archivo federal.

Ejemplos verificables en el archivo local descargado: A sección 2466, acta `112466C0100`, mismo municipio 31 y LN 639, totales 276 y 356; PRI 8 y 88. A sección 2017, acta `112017B0100`, mismo municipio 23 y LN 750, totales 151 y 173. DL sección 1492, acta `111492C0400`, mismo distrito local 51 y LN 709, totales 204 y 202. Ninguna de estas tres parejas se resuelve separando MR/RP de casillas especiales.

**Puerta de decisión:** mantener todas las filas como evidencia y consultar acta de cómputo, recuento o versión oficial corregida antes de elegir el resultado canónico. Identificadores y corte del archivo son parte obligatoria de la trazabilidad. En 2021 las diferencias 43 (A) y 45 (DL) siguen sin certificarse como correcciones; el formato tiene guiones y duplicados.

## Resolución con SICEE INE: fuentes locales 2021 por sección

Fuente independiente oficial INE: https://sicee.ine.mx/downloadzip, ámbito Local, elección 2021, Guanajuato `GTO_PEL_2021.zip`; copia conservada como `INE_SICEE_GTO_PEL_2021_original.zip`; SHA-256 `b1104c62ba32602e0ec6b0b54778fd456fcf25004552368a21ccfad7ccf70c9b1`. ZIP íntegro. Contiene CSV y XLSX por casilla, sección, municipio/distrito, para Ayuntamientos y Diputaciones Locales MR/RP. Los CSV de sección tienen 3,159 filas y claves únicas en cada elección/modalidad.

| Campo | A 2021: diferencias derivado/INE | A 2021: diferencias maestra/INE | DL 2021 MR: diferencias derivado/INE | DL 2021 MR: diferencias maestra/INE |
|---|---:|---:|---:|---:|
| PAN | 0 | 37 | 0 | 370 |
| PRI | 0 | 38 | 0 | 371 |
| PVEM | 0 | 37 | 0 | 369 |
| MORENA | 0 | 38 | 0 | 369 |
| TOTAL | 0 | 42 | 0 | 371 |
| LN | 0 | 42 | 0 | 367 |

El cotejo se hizo por sección y valor entero, no por orden de filas. `A.json` reproduce exactamente los seis campos del archivo SICEE de Ayuntamientos; `DL.json` reproduce exactamente los seis campos del archivo SICEE de Diputaciones Locales **MR**. En 29 secciones, el archivo SICEE de DL **RP** difiere de MR en los votos, por lo que la elección de modalidad tiene efecto concreto. LN coincide entre MR y RP. La maestra tiene valores divergentes, particularmente DL 2021; no sobrescribir el derivado verificado con valores de la maestra.

La clasificación previa de 43/45 diferencias a partir del ZIP de cómputos locales y suma simple queda **superada como criterio de corrección**: los CSV de ese paquete contienen actas repetidas/conflictivas, `-` y modalidades no identificadas. Se conservan como evidencia del corte pero se toma el SICEE seccional MR como referencia para este cotejo, pendiente de validación de equivalencia de procedencia y de casos puntuales. Para recuperar todos los partidos y combinaciones en el maestro futuro, usar los archivos SICEE por casilla y sección con sus columnas completas; no inferir votos faltantes de los cuatro partidos de la maestra.

## Cotejo SICEE Guanajuato 2018 y 2024: elecciones locales

Descargas oficiales en https://sicee.ine.mx/downloadzip, ámbito Local, Guanajuato: `GTO_PEL_2018.zip` (`INE_SICEE_GTO_PEL_2018_original.zip`, SHA-256 `c5683d3bdadb4025880ddecb7c0de32b63cf9f2909bd2cfed760452669bc3b04`) y `GTO_PEL_2024.zip` (`INE_SICEE_GTO_PEL_2024_original.zip`, SHA-256 `13fe6a2ddb432922bddc9090f08eb0e558aeb3094ef1ba763b78d789b3d55e69`). Cada paquete incluye CSV por casilla y sección de Ayuntamiento, Diputación Local MR y RP, y Gubernatura; preserva columnas de partidos y combinaciones de coalición. El cotejo siguiente usa únicamente secciones positivas y **MR** para DL; compara cuatro votos directos, TOTAL_VOTOS y LISTA_NOMINAL. Filas de sección cero se conservan para análisis de votos especiales/extranjero por separado.

| Año y elección | Secciones ordinarias SICEE | Diferencias maestra: PAN / PRI / PVEM / MORENA / TOTAL / LN | Diferencias derivado: PAN / PRI / PVEM / MORENA / TOTAL / LN |
|---|---:|---|---|
| 2018 A | 3,137 | 37 / 37 / 36 / 36 / 37 / 0 | 0 / 0 / 0 / 0 / 0 / 0 |
| 2018 DL MR | 3,137 | 29 / 29 / 29 / 29 / 29 / 0 | 0 / 0 / 0 / 0 / 0 / 0 |
| 2018 G | 3,137 | 0 / 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 / 0 |
| 2024 A | 3,233 | 52 / 53 / 51 / 52 / 53 / 2,657 | 52 / 53 / 51 / 52 / 53 / 2,657 |
| 2024 DL MR | 3,233 | 34 / 33 / 33 / 34 / 34 / 2,657 | 34 / 33 / 33 / 34 / 34 / 2,657 |
| 2024 G | 3,233 | 3,218 / 3,226 / 3,171 / 3,230 / 3,220 / 3,222 | 0 / 0 / 0 / 0 / 0 / 2,657 |

Para PVEM de A 2018 hay además **cinco celdas vacías en SICEE**, frente a cero en los archivos HEYTI; no se contabilizaron como coincidencias ni diferencias numéricas. Las 3,310 secciones de la maestra incluyen 173 claves sin resultado ordinario en SICEE 2018 y 77 sin resultado ordinario en SICEE 2024: son diferencias de cobertura temporal, no imputaciones automáticas. En 2024 existen múltiples registros de sección cero en ciertos municipios/distritos; no usarlos como clave única ni agregarlos indiscriminadamente a secciones ordinarias.

**Prioridad de saneamiento:** la maestra 2024 G diverge masivamente en votos, mientras el derivado G coincide en los cinco campos de votos; el campo LN del derivado difiere de la fuente oficial en 2,657 secciones, al igual que A y DL 2024. También hay votos 2024 A/DL divergentes en ambos archivos. Estas cifras identifican expedientes de corrección, no autorizan reemplazos ciegos: antes de integrar, fijar regla de LN según elección y revisar secciones puntuales y procedencia. HEYTI-CORE no se ha modificado.

## Cotejo SICEE federal 2018 y 2024: Guanajuato

Desde https://sicee.ine.mx/downloadzip, ámbito Federal, se descargaron los originales de Diputaciones Federales MR, Presidencia y Senadurías MR para 2018 y 2024. ZIP intactos, con archivos nacionales CSV por casilla y sección; se filtró `ID_ESTADO=11` y `SECCION>0`, sin combinar MR con RP. En cada elección/año hay 3,137 secciones ordinarias en 2018 y 3,233 en 2024, todas con clave única; los 173/77 identificadores adicionales de la maestra no son resultados ordinarios de esos años. Presidencia y Senado incluyen además un registro de sección cero estatal. Las columnas de partidos son votos directos; coaliciones se conservan por separado.

| Archivo original | SHA-256 |
|---|---|
| `INE_SICEE_DF_MR_2018_original.zip` | `0c6c40bb408cbbcc06e2fd61413d85f2dd1d8d49a2c2bb362cea8f27b3c94be4` |
| `INE_SICEE_P_2018_original.zip` | `f04fbad28bb13f960f3136efc7e3e4cbc61a613794429c8433699cb9d86e84c0` |
| `INE_SICEE_S_2018_original.zip` | `fc83f3e8aaba95357cd49b4bd91ee0171cfe00a66d5bb4cd9b35906cfbe32ee1` |
| `INE_SICEE_DF_MR_2024_original.zip` | `9da21ef4e7ed7f490d3351c4834c4cea0bff050699d9d4ebf45f902e333cc61c` |
| `INE_SICEE_P_2024_original.zip` | `3122304d4dec2a24168708af9836f5df2860ac4347163dc311473bd037737bbf` |
| `INE_SICEE_S_2024_original.zip` | `bafa39ae21279f229a3892422d8b9fb339160bc92a17c9a3583c92c1154c19cf` |

| Año y elección | Diferencias maestra: PAN / PRI / PVEM / MORENA / TOTAL / LN | Diferencias derivado: PAN / PRI / PVEM / MORENA / TOTAL / LN |
|---|---|---|
| 2018 DF MR | 0 / 0 / 0 / 0 / 0 / LN ausente | 0 / 0 / 0 / 0 / 0 / 0 |
| 2018 P | 0 / 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 / 0 |
| 2018 S MR | 0 / 0 / 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 / 0 / 0 |
| 2024 DF MR | 1,994 / 1,241 / 1,450 / 1,993 / 2,278 / 15 | 47 / 47 / 47 / 47 / 47 / 0 |
| 2024 P | 1,726 / 1,074 / 1,240 / 1,848 / 2,167 / 16 | 0 / 0 / 0 / 0 / 0 / 0 |
| 2024 S MR | 2,125 / 1,300 / 1,466 / 2,136 / 2,409 / 15 | 38 / 38 / 36 / 38 / 38 / 0 |

`18DF_LN` no existe en la maestra; sí existe LN 2018 DF en el derivado, con concordancia total. En 2024 P el derivado seccional coincide por completo en los seis campos. La maestra muestra diferencias extensas en votos federales 2024; el derivado DF tiene 47 secciones con diferencias de todos los campos de votos, y S 38 en el total. Estas últimas exigen revisión de casillas especiales, recuentos y origen de agregación antes de cambiar valores. Los conteos de diferencias comparan igualdad de campo, no suman votos faltantes ni prueban una causa. El siguiente trabajo debe certificar los casos discordantes por casilla y elaborar el paquete de migración completo de opciones políticas; no modificar la fuente HEYTI-CORE sin acceso al repositorio y validación de la cadena de datos.

### Revisión de las 85 discrepancias federales 2024 por casilla

El archivo complementario `HEYTI_Discrepancias_Federales_2024_DF_S.csv` enumera una fila por cada una de las 47 secciones DF MR y 38 secciones S MR discrepantes, con total del derivado, total oficial seccional, suma de registros oficiales por casilla, número y votos de casillas especiales MR, casillas anuladas, y los cuatro partidos directos. No se agregan filas `SECCION=0` a ninguna sección ordinaria.

En **10 secciones DF MR**, la suma sin filtro de casillas excede exactamente al total seccional por los votos de una o dos casillas marcadas `TRIBUNAL=ANULADA`; los cinco campos de votos del derivado coinciden con la suma sin filtro por casilla, mientras el seccional oficial excluye esas casillas. Son secciones 71, 364, 398, 451, 530, 536, 1058, 2797, 3258 y 3276. Ejemplo: sección 71, casilla B=307 y C1=306 `ANULADA`; el seccional oficial tiene 307 votos y el derivado 613. En la sección 3258 constan dos casillas anuladas por un total de 750 votos. Esta es una causa demostrada de la diferencia y debe preservarse la sentencia y su registro como evidencia de resolución judicial.

Las **otras 37 secciones DF MR** tienen al menos una casilla especial `SMR`; sus sumas por casilla coinciden con los totales seccionales oficiales, pero el derivado tiene más votos. Las **38 secciones S MR** discrepantes también tienen al menos una `SMR`; suma por casilla y total oficial coinciden, y el derivado excede el oficial. Esa asociación no identifica todavía el mecanismo de duplicación o la versión de origen del derivado. Por ejemplo, sección 81: DF oficial 2,681 / derivado 2,920 / casilla SMR 315; Senado oficial 2,623 / derivado 3,304 / casilla SMR 276. Las diferencias (239 y 681) no son simplemente los votos de esas casillas especiales. Verificar el origen del derivado y la identificación de casillas, así como la modalidad RP, antes de atribuir causas o automatizar ajustes.
