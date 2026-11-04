# HEYTI — Alcance municipal de diferencias A2024 IEEG frente a SICEE

**27 de septiembre de 2026.** Cotejo estadístico de fuentes originales, sin modificar base viva. Fuente IEEG: `IEEG_Computos_2024_original.zip` (subarchivo de ayuntamientos, casillas `CONTABILIZADA=1`); fuente SICEE: `INE_SICEE_GTO_PEL_2024_original.zip` (AYUN SEC y CAS). Se comparan secciones ordinarias compartidas y `TOTAL_VOTOS`, junto con las cuatro columnas de partido de la auditoría previa. Los detalles por sección/campo están en `HEYTI_Diferencias_IEEG_SICEE_2024_v0_1.csv`.

| Municipio | Secciones con diferencia de total | IEEG − SICEE en votos | CAS SICEE `ANULADA` | Votos de CAS anuladas | CAS `MODIFICADA` |
|---|---:|---:|---:|---:|---:|
| Celaya | 5 | +1,670 | 5 | 1,670 | 0 |
| Irapuato | 28 | +10,609 | 34 | 10,609 | 0 |
| San Miguel de Allende | 9 | +2,404 | 8 | 2,578 | 2 |
| Silao de la Victoria | 11 | +3,461 | 11 | 3,461 | 0 |
| **Total** | **53** | **+18,144** | **58** | **18,318** | **2** |

En San Miguel, las secciones 176 y 216 tienen diferencia IEEG − SICEE de −100 y −74 respectivamente, que explica la resta de 174 al total de 2,578 anulado: 2,578 − 174 = 2,404. Las casillas SICEE 176 C1 y 216 C1 están marcadas `MODIFICADA`. Esta igualdad aritmética ubica el efecto; requiere conservar ambas versiones de voto y el expediente para atribuir jurídicamente cada ajuste.

De las 53 secciones, 51 contienen casillas anuladas y dos muestran la modificación anterior. La correspondencia de cantidades demuestra por qué difiere el corte IEEG frente al SICEE en estos campos; **no prueba** que las 58 anulaciones ni las dos modificaciones sigan vigentes como estado final. En particular, Sala Monterrey restituyó cuatro CAS de San Miguel (1,371 votos) después del corte que refleja este ZIP SICEE, y fijó 76,757 para ese municipio. Véase `HEYTI_Alerta_Corte_Judicial_A2024_SICEE_v0_1.md` y la sentencia https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JDC-0517-2024.pdf.

No hay diferencias del total en los demás municipios dentro de los pares ordinarios comparados. El universo de esta comprobación es de 3,233 secciones emparejadas y 46 municipios, con exclusiones de identidades no comparables que constan en la auditoría previa; no equivale a una certificación judicial de toda la serie.
