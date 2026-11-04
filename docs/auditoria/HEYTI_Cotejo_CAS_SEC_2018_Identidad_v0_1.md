# HEYTI — CAS contra SEC SICEE 2018 e identidad territorial

Fecha: 29/09/2026. Fuente original `INE_SICEE_GTO_PEL_2018_original.zip`, CSV CAS y SEC de Ayuntamientos (A), Diputaciones locales MR (DL MR) y Gubernatura (G). Lectura solamente; base viva intacta.

La llave `(distrito, municipio, sección)` **no es segura** entre CAS y SEC en este paquete: varios renglones de una misma sección difieren en los metadatos de distrito o municipio. Antes de cotejar votos se verificó que las claves de `SECCION` en SEC son únicas en cada serie y que las CAS se pueden agrupar por ella dentro de cada elección. El cotejo de los cinco campos (válidos, no registrados, nulos, total y LN) se rehízo con `SECCION` en el contexto de la serie; un valor vacío siguió siendo indeterminado, no cero.

| Serie | SEC | CAS | SEC sin diferencia de votos determinada | SEC cuya resta de votos se explica por CAS `Anulada` | Otras diferencias no explicadas |
|---|---:|---:|---:|---:|---:|
| A | 3,137 | 7,463 | 3,100 | 37 | 0 |
| DL MR | 3,137 | 7,463 | 3,137 | 0 | 0 |
| G | 3,138 | 7,479 | 3,138 | 0 | 0 |

En A hay **41 CAS marcadas `Anulada`**, con **11,858 votos crudos**. Para las 37 secciones afectadas, en cada campo de votos computable la diferencia `SUM(CAS)−SEC` coincide exactamente con las CAS anuladas; LN se mantiene igual. En cuatro secciones algunas celdas SEC de válidos/no registrados están vacías, por lo que se conserva el estado indeterminado de esas celdas mientras el resto de campos respeta la misma regla. No reincorporar los 11,858 votos al SEC ni convertir vacíos en cero.

## Metadatos que impiden unir por distrito y municipio a la vez

| Serie | Filas CAS con metadato diferente de su SEC | Secciones afectadas | Campo diferente |
|---|---:|---:|---|
| A | 2,070 | 801 | `ID_DISTRITO_LOCAL`; municipio igual |
| DL MR | 306 | 133 | `ID_MUNICIPIO`; distrito igual |
| G | 306 | 133 | `ID_MUNICIPIO`; distrito igual |

Un cruce inicial por los tres campos produjo miles de falsas diferencias en votos y LN al dejar CAS fuera de su grupo. El emparejamiento por sección única de la serie las elimina. **La identidad territorial discordante sigue siendo una incidencia propia:** no se reescribió el municipio/distrito de CAS ni se infirió qué campo histórico es correcto. Validar catálogo y vigencia de geografía antes de proyectar estas filas a `territorial.section_history` o a capas de mapa. Conservar ambas claves de origen y registrar el vínculo de sección junto con versión/corte.

Este cotejo CAS→SEC es independiente de las diferencias de agregados MUN/DIS 2018 documentadas en `HEYTI_Cobertura_Agregados_2018_MUN_DIS_vs_SEC_v0_1.md`; que CAS→SEC cuadre por sección no corrige un agregado superior discordante.
