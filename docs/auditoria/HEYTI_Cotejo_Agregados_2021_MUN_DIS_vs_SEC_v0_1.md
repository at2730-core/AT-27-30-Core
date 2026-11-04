# HEYTI — Agregados SICEE 2021 contra secciones

Fecha: 29/09/2026. Original `INE_SICEE_GTO_PEL_2021_original.zip`; CSV CAS/SEC/MUN de Ayuntamientos y SEC/DIS de Diputaciones locales MR. Sólo lectura, sin cambios a la base viva.

Se compararon `NUM_VOTOS_VALIDOS`, `NUM_VOTOS_CAN_NREG`, `NUM_VOTOS_NULOS`, `TOTAL_VOTOS` y `LISTA_NOMINAL` de cada agregado contra sus secciones del mismo territorio y elección. Vacío no se interpreta como cero.

| Serie | Agregados | Cinco campos iguales a suma SEC | SEC con votos vacíos y agregado igual a suma de SEC con voto publicado |
|---|---:|---:|---:|
| A MUN | 46 | 44 | 2 |
| DL MR DIS | 22 | 22 | 0 |
| **Total** | **68** | **66** | **2** |

Las dos excepciones de Ayuntamientos son **San Miguel de Allende MUN 3**, sección **163**, y **San José Iturbide MUN 32**, sección **2541**. En SEC, ambos conservan LN (678 y 1,202), pero votos válidos, no registrados, nulos y total vacíos. Las otras SEC del municipio suman exactamente las cuatro cifras de votos del MUN y toda la LN SEC suma exactamente la LN MUN. En CAS, sección 163 B conserva **371 votos crudos** y marca `TRIBUNAL=ANULADA`; sección 2541 B/C01 conserva **214 y 222** votos crudos, ambos `ANULADA`. Esos 371/436 votos no se imputan al total municipal SICEE ni se transforman en cero en SEC.

El cotejo confirma consistencia entre niveles en este conjunto salvo los dos vacíos judiciales; no certifica que el corte IEEG de 2021 tenga las mismas cifras o modalidades. Se conservan los dos cortes, las actas crudas y el estado judicial. Los casos de CAS especiales MR/RP, claves repetidas IEEG y diferencias entre paquetes se documentan por separado.
