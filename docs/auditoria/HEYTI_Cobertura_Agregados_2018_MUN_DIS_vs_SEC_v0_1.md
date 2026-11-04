# HEYTI — Cobertura de agregados SICEE 2018 contra SEC

Fecha: 29/09/2026. Fuente: `INE_SICEE_GTO_PEL_2018_original.zip`. Se cotejaron todas las filas A MUN (46), DL MR DIS (22) y G DIS (23), con cinco campos: válidos, no registrados, nulos, total y lista nominal. Sólo lectura; no modificación de base viva.

| Control | A MUN | DL MR DIS | G DIS | Total |
|---|---:|---:|---:|---:|
| Ya en 42 incidencias aritméticas internas | 20 | 10 | 12 | 42 |
| **Nueva discordancia agregado vs suma SEC**, sin falla aritmética interna previa | **4** | **7** | **0** | **11** |
| Cinco campos iguales a SEC | 21 | 5 | 11 | 37 |
| Total y LN iguales a SEC, válidos indeterminados por SEC vacío | 1 | 0 | 0 | 1 |
| **Filas examinadas** | **46** | **22** | **23** | **91** |

Las 11 diferencias nuevas, como **agregado menos suma de SEC**, son:

| Elección / territorio | Δ válidos | Δ no registrados | Δ nulos | Δ total | Δ LN |
|---|---:|---:|---:|---:|---:|
| A / San Miguel de Allende, MUN 3 | indeterminado: tres SEC vacíos | 0 | 0 | −1 | 0 |
| A / Irapuato, MUN 17 | −2,733 | −46 | −88 | −2,867 | 0 |
| A / León, MUN 20 | +7 | +1 | −402 | −394 | 0 |
| A / Silao de la Victoria, MUN 37 | 0 | 0 | −10 | −10 | 0 |
| DL MR / León, DIS 5 | −512 | 0 | −20 | −532 | 0 |
| DL MR / León, DIS 6 | −1,746 | −1 | −66 | −1,813 | 0 |
| DL MR / Guanajuato, DIS 8 | −381 | 0 | −17 | −398 | 0 |
| DL MR / Irapuato, DIS 12 | −1,273 | −2 | −42 | −1,317 | 0 |
| DL MR / Silao de la Victoria, DIS 13 | −10,000 | 0 | 0 | −10,000 | 0 |
| DL MR / Salamanca, DIS 14 | −626 | −1 | −18 | −645 | 0 |
| DL MR / León, DIS 21 | −371 | −1 | −5 | −377 | 0 |

**CAS vs SEC en las 11:** en A Irapuato y los siete distritos DL MR, las sumas CAS y SEC coinciden en los cinco campos. En A San Miguel de Allende, León y Silao, CAS supera SEC en **6,214**, **2,695** y **1,906** votos totales, respectivamente; esas cantidades son exactamente la suma de CAS con `TRIBUNAL=Anulada` (21, 9 y 7 casillas). La coincidencia aritmética describe el tratamiento seccional del archivo; no identifica por sí sola la publicación o sentencia de cada nulidad ni explica los residuales MUN vs SEC de −1, −394 y −10. A San Miguel tiene además tres SEC con votos válidos vacíos; no se imputaron como cero.

### Desglose del distrito 13 DL MR

La diferencia exacta de **10,000** se localiza en un solo campo de opción del archivo `2018_SEE_DIP_LOC_MR_GTO_DIS.csv`: `MORENA=9,439` frente a la suma de las 128 SEC, `MORENA=19,439`. Los demás campos de opción compartidos por DIS y SEC coinciden; `NUM_VOTOS_VALIDOS` publica 74,623 frente a 84,623 y `TOTAL_VOTOS` 77,976 frente a 87,976. CAS y SEC también suman 87,976. Los agregados separados `DISPP` y `DISCAND` publican `TOTAL_VOTOS=87,976` para el mismo distrito, pero su desglose de candidaturas/partidos usa reglas distintas y **no debe equipararse directamente** con la columna cruda `MORENA` de DIS. El patrón es compatible con una pérdida de 10,000 en la fila DIS, pero la causa documental y un eventual archivo corregido permanecen sin confirmar; conservar 9,439 y 19,439 con su procedencia.

La fila A San Felipe, MUN 30, no muestra diferencia determinada en total, no registrados, nulos ni LN, pero una SEC deja `NUM_VOTOS_VALIDOS` vacío; por eso se clasificó como **indeterminada**, no como igualdad completa de los cinco campos. La LN agregada coincide con SEC en las 91 filas, aun cuando los votos discrepan.

### Alcance de las otras diferencias nuevas

En A MUN 17 (Irapuato) y en DL MR DIS 5, 6, 8, 12, 14 y 21, la diferencia de total se distribuye entre **varias columnas de partidos/opciones**, además de nulos y en algunos casos no registrados. No se reduce a una sola cifra mal transcrita. A MUN 20 (León) presenta PRI +10, MC −3, no registrados +1 y nulos −402; A MUN 37 (Silao) sólo nulos −10; A MUN 3 (San Miguel) registra `PT_ES` −1, con tres SEC de válidos vacíos. En DL MR DIS 8 hay dos filas CAS de 398 votos (878 C01 y 887 C01) con el mismo vector de opciones que el residuo agregado, **sin marca `TRIBUNAL`**; esa igualdad no identifica cuál, si alguna, explica el agregado.

El contraste de `TOTAL_VOTOS` de los archivos agregados `MUN/DIS`, `MUNCAND/DISCAND` y `MUNPP/DISPP` muestra que en la mayoría de estas claves los tres agregados publican el mismo total, inferior a SEC. Hay excepciones: A Irapuato publica 204,910 en MUN y MUNCAND, 202,964 en MUNPP, frente a 207,777 SEC; DL MR Salamanca DIS 14 publica 117,034 en DIS, 115,806 en DISCAND y 116,563 en DISPP, frente a 117,679 SEC. Esas diferencias entre agregados del mismo paquete requieren examen de versión y regla de distribución; no se declara un total único a partir de ellas.

**Alcance:** el conjunto inicial de 42 detectaba sólo fallas aritméticas **dentro** de MUN/DIS. Las 11 nuevas tienen identidad aritmética interna, pero fallan el cotejo **entre niveles**. La cifra `−10,000` de DL distrito 13 se conserva literalmente y requiere cotejo documental prioritario; no se corrige como supuesta errata. La investigación judicial/corte y la selección de cifras para HEYTI siguen abiertas. Preservar CAS, SEC, MUN y DIS por separado; registrar 11 nuevas incidencias en el reporte final. No se ha enviado ninguna solicitud externa.
