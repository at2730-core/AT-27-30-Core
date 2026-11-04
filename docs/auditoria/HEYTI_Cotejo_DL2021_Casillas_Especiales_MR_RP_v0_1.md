# HEYTI — Identidad de casillas especiales, Diputaciones locales 2021

**Corrección del 29/09/2026.** La primera versión de este reporte descartaba por error una de las dos filas S por sección del archivo SICEE RP al construir una llave sólo por sección. Los conteos anteriores (15/16) **quedan sustituidos** por los siguientes. La identidad correcta de modalidad está en `CASILLA=SMR01` o `SRP01`. Originales preservados: `IEEG_Computos_2021_original.zip` (`20210610_1200_DIP_LOC_GTO.zip` → `GTO_DIP_LOC_2021.csv`) e `INE_SICEE_GTO_PEL_2021_original.zip` (CSV CAS de Diputaciones locales MR y RP). Lectura solamente; sin cambio de base viva.

## Método

IEEG contiene **62 filas S en 31 secciones**, dos por `CLAVE_ACTA`, sin etiqueta MR/RP en esos renglones. SICEE MR contiene 31 `SMR01`; el archivo SICEE RP contiene **esas mismas 31 SMR01 más 31 SRP01**. Cada par IEEG se cotejó una sola vez contra una MR y una RP por sección (la fila SMR repetida en el archivo RP no se cuenta de nuevo). Se compararon literalmente 16 campos: PAN, PRI, PRD, PVEM, PT, MC, MORENA, NA_Gto, PES, RSP, FXM, PRI_PRD, candidatura independiente, no registrados, nulos y total. LN se excluye de identidad numérica: IEEG muestra 1,000 en especiales y SICEE 0. Vacío, guion y cero siguen siendo distintos.

| Coincidencia exacta de los 16 campos | Secciones | Cantidad |
|---|---|---:|
| Filas IEEG distintas emparejan por separado MR y RP | 157, 172, 175, 291, 613, 754, 967, 972, 982, 1927, 2381, 2450, 2507, 2620, 2833, 2919, 3171 | **17** |
| Ambas filas IEEG y ambas modalidades SICEE son numéricamente idénticas; orden no adjudicable | 248, 2547 | **2** |
| Una fila IEEG sólo coincide con MR; ninguna coincide con RP | 81, 444, 1570, 1729, 2062 | **5** |
| Una fila IEEG sólo coincide con RP; ninguna coincide con MR | 1282, 1518, 1866, 2193, 2270, 2794 | **6** |
| Una fila IEEG coincide con MR y RP; la otra tiene guiones | 2657 | **1** |
| **Total** | | **31** |

En **754** el orden IEEG se invierte: primera fila 428 corresponde a RP y segunda 423 a MR; por ello el orden no constituye una regla de modalidad. En **81**, IEEG 127/126 y SICEE MR 127/RP 132, por lo que sólo MR coincide. En **2193**, IEEG PAN 138 y total 322 coincide con SICEE RP; MR tiene PAN 148 y total 322, una discrepancia de opción que un cotejo sólo de totales ocultaría. En **1282, 1518, 1866, 2270 y 2794**, la fila IEEG con votos coincide con SICEE RP; SICEE MR registra total 0 y opciones vacías, mientras la segunda IEEG contiene guiones. No imputar cero a esos guiones.

Las 31 filas `SMR01` comunes a los dos archivos SICEE deben deduplicarse **por identidad de acta y modalidad entre archivos**, sin borrar los originales. Los campos `ESTATUS_ACTA`, `TRIBUNAL` y `OBSERVACIONES` de las 16 secciones sin emparejamiento único no aportan por sí solos una marca judicial explicativa: se observan principalmente `ACTA CASILLA`, algunos `GRUPO DE RECUENTO`, y campos judiciales vacíos. Su ausencia no demuestra que no exista una rectificación externa.

## Decisión

Las **17** secciones con correspondencia distinta admiten vínculo numérico provisional IEEG→SICEE MR/RP; las otras **14** permanecen indeterminadas para al menos una modalidad o para la identidad de sus dos filas. Conservar ambas filas IEEG y ambos registros SICEE separados, sus cortes y literales. No sumar 62 IEEG como 62 casillas físicas ni usar la posición de una fila como modalidad. El primer pase de agregados de 2021 excluía las 31 secciones completas: esta revisión permite acotar 17 correspondencias, pero no rehace ni certifica aún aquel agregado. Priorizar documentación pública de 81, 2193 y las cinco parejas cero/vacío frente a guion. Sin prueba suficiente, HEYTI conserva la cifra original y una nota de adjudicación indeterminada. No se envió solicitud ni comunicación externa.
