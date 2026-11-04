# HEYTI — 42 agregados SICEE 2018 contra secciones y casillas

Fecha de revisión: 29/09/2026. Fuente original `INE_SICEE_GTO_PEL_2018_original.zip`; selección de incidencias `HEYTI_Incidencias_Totales_Agregados_SICEE_2018.json`. Elecciones A, DL MR y G en Guanajuato. Sólo lectura, sin cambio de base viva.

El control anterior encontró **42 agregados MUN/DIS** en los que `TOTAL_VOTOS` no iguala válidos + no registrados + nulos: 35 diferencias iguales exactamente al número de nulos y siete con otro residuo. Eso es un **control interno de la fila**, no una comparación entre niveles. Esta revisión compara cada una de las 42 filas con la suma de sus SEC por elección y territorio. Para los cinco casos con diferencias de componentes se contrastó también la suma CAS. Se conservaron los literales originales y las claves MUN/DIS.

| Resultado entre agregado y suma SEC | A | DL MR | G | Total |
|---|---:|---:|---:|---:|
| Sólo difiere `TOTAL_VOTOS`; válidos, no registrados, nulos y LN iguales | 18 | 8 | 11 | **37** |
| Difieren además uno o varios componentes de votos; LN igual | 2 | 2 | 1 | **5** |
| **Total** | **20** | **10** | **12** | **42** |

Los **cinco** casos de segunda fila, con diferencia **agregado menos suma SEC**, son:

| Elección / territorio | Δ válidos | Δ no registrados | Δ nulos | Δ total | Δ LN |
|---|---:|---:|---:|---:|---:|
| A / San José Iturbide, MUN 32 | +397 | 0 | −397 | −1,658 | 0 |
| A / Tierra Blanca, MUN 40 | −387 | 0 | −11 | −759 | 0 |
| DL MR / Celaya, DIS 16 | −2,004 | −1 | −92 | −5,949 | 0 |
| DL MR / Valle de Santiago, DIS 19 | −2,314 | 0 | −130 | −7,683 | 0 |
| G / León, DIS 21 | +2,272 | 0 | +44 | +1,884 | 0 |

En esas cinco claves, **SEC y CAS coinciden exactamente** en los cinco campos examinados (válidos, no registrados, nulos, total y LN). A 32: 38 SEC/99 CAS; A 40: 10/23; DL 16: 110/320; DL 19: 156/388; G 21: 89/280. No se atribuye causa a la discrepancia del agregado ni se declara que un nivel sustituya legalmente a otro. El caso G 21 también está en los siete residuos aritméticos adicionales; los otros cuatro tenían en la fila agregada la omisión exacta de nulos, **pero esa clasificación interna no explica sus diferencias frente a SEC/CAS**.

Conservar la dimensión de nivel (`CAS`, `SEC`, `MUN`, `DIS`), modalidad, corte y procedencia. Bloquear el uso del `TOTAL_VOTOS` agregado discordante como dato certificado sin nota. En los cinco casos, no fusionar componentes de agregado y seccional para fabricar una fila corregida. Consultar publicaciones de cómputo/rectificación y actas públicas si se encuentran; si no, mantener la discrepancia en el reporte final y en la lista de aclaraciones que Alex eventualmente decidirá plantear a su contacto, sin enviar comunicaciones desde esta auditoría.
