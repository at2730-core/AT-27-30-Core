# HEYTI — Cotejo seccional contra casillas, 23 series

**26 de septiembre de 2026.** Análisis local de los 15 ZIP originales INE/SICEE para Guanajuato, mediante `HEYTI_Cotejar_Secciones_Casillas_23_Series_v0_1.py`. Los SHA-256 de cada ZIP y CSV seccional se verificaron contra el manifiesto. No se modificó PostgreSQL ni la maestra.

## Resultado

| Medida | Conteo |
|---|---:|
| Series SEC/CAS cotejadas | 23 |
| Filas seccionales GTO | 73,262 |
| Filas de casilla GTO | 179,779 |
| Secciones sin casillas asociadas / grupos de casilla huérfanos | 0 / 0 |
| Celdas numéricas SEC = suma CAS | 1,415,400 |
| Celdas numéricas SEC ≠ suma CAS sin filtrar actas anuladas | 1,418 |
| Diferencias de `TOTAL_VOTOS` incluidas arriba | 119 |
| Celdas literalmente vacías a ambos niveles | 341,544 |
| Comparaciones indeterminadas por valor vacío en algún nivel | 1,189 |

Las **1,418 diferencias numéricas** corresponden a **119 unidades seccionales** distribuidas en siete series. En **cada diferencia**, el valor seccional coincide exactamente con la suma de casillas **después de excluir las casillas cuyo campo `TRIBUNAL` dice `ANULADA`/`Anulada`**. Es evidencia de la transformación aplicada a las cifras publicadas; no se infiere aquí el contenido de la sentencia a partir de su nombre.

| Serie | Secciones afectadas (`TOTAL_VOTOS`) | Celdas numéricas afectadas |
|---|---:|---:|
| 2018 A | 37 | 471 |
| 2021 A | 18 | 233 |
| 2021 DF MR | 1 | 13 |
| 2021 DL MR | 1 | 13 |
| 2021 DL RP | 1 | 13 |
| 2024 A | 51 | 542 |
| 2024 DF MR | 10 | 133 |
| **Total** | **119** | **1,418** |

Ejemplo: DF 2021 MR, sección 218: el CSV de casillas suma 918 votos; una casilla de 304 votos está marcada `Anulada` en `TRIBUNAL` (`SM-JIN-29-2021 Y ACUMULADOS`); el CSV seccional publica 614. Esto explica la diferencia 918 − 304 = 614. También se comprobaron las otras columnas numéricas de esa unidad.

## Alcance y siguiente puerta

La proyección en staging conserva el **resultado seccional publicado**, que incorpora estas exclusiones. Sumar indiscriminadamente los votos crudos de casilla produciría 119 totales distintos. El expediente de cada casilla anulada debe preservarse por separado, con estatus, referencia judicial y valores crudos, para permitir reproducir ambos estados.

Las 1,189 comparaciones indeterminadas contienen algún vacío literal a un nivel; no se convierten a cero ni se consideran aprobadas. La prueba comprueba identidad aritmética de CSV SEC/CAS, no verifica físicamente la imagen de cada acta, el texto de cada resolución, la vigencia de todos los cortes ni la atribución de votos de coalición a candidaturas. El JSON adjunto contiene cada diferencia con su sección, columna, casillas, `TRIBUNAL` y referencia disponible; los vacíos indeterminados se contabilizan por serie y se dan ejemplos, pero requieren expediente propio si se pretende cerrar el cien por ciento de las celdas.
