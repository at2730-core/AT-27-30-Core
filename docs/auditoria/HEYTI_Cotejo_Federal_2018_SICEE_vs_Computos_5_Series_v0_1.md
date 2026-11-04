# HEYTI — Cotejo federal 2018: SICEE contra cómputos, Guanajuato

Fecha de revisión: 30 de septiembre de 2026. Fuente de cómputos: [Cómputos 2018, INE](https://computos2018.ine.mx/), archivo de corte `20180708_2130_CW.zip` publicado por el propio sitio, **8 de julio de 2018, 21:30 (UTC-5)**, SHA-256 `eac4a411017c4c338d407f2ac34cc089b89878225f189456c2b7a93cd098e4e9`. Prueba ZIP satisfactoria; contiene tres ZIP internos de Presidencia, Senadurías y Diputaciones, cada uno con CSV de actas y candidaturas. Fuentes SICEE: cinco paquetes federales 2018 originales. Sus hashes figuran en `HEYTI_Inventario_Federal_2018_2021_Fuentes_Pendientes_v0_1.md`; Presidencia se recuperó nuevamente con el **mismo hash previo** `f04fbad28bb13f960f3136efc7e3e4cbc61a613794429c8433699cb9d86e84c0` al detectar una copia de trabajo incompleta.

Se filtró `ID_ESTADO=11`. Llave de casilla: distrito federal, sección, tipo, identificador, extensión, todos normalizados; las especiales usan además el identificador de modalidad: cómputo `NUM_ACTA_IMPRESO` **2 Presidencia, 4/5 Senado MR/RP, 7/8 Diputaciones MR/RP**, frente a `CASILLA=SMR/SRP` SICEE. No se suman MR y RP. Las unidades extranjeras del cómputo M (Presidencia) y V (Senado) se cotejan por agregado con las 16 MEC SICEE, no por llave individual.

| Serie | Claves emparejadas | Diferencias `TOTAL_VOTOS` por casilla | LN ordinaria comparable | Excepciones de campos vacíos |
|---|---:|---:|---|---|
| Presidencia | 7,463/7,463 | 0 | 0 diferencias | 1 CAS, sección 553 C01 distrito 12 |
| Senado MR | 7,463/7,463 | 0 | 0 diferencias | 2 CAS, secciones 371 C02 y 471 C06 distrito 12 |
| Senado RP | 7,499/7,499 | 0 | 0 diferencias | Las mismas 2 CAS |
| Diputaciones MR | 7,463/7,463 | 0 | 0 diferencias | 1 CAS, sección 553 C01 distrito 12 |
| Diputaciones RP | 7,499/7,499 | **532**, suma SICEE−cómputo **−18,442** | 0 diferencias | La misma CAS 553 C01 |

En las excepciones, el cómputo presenta LN en blanco y votos partidistas con `-`; SICEE conserva LN (500 para 553 C01; 504/686 para las dos casillas de Senado), nulos y no registrados vacíos, y total de votos 0. LN, nulos y no registrados se califican **no determinables** en esas claves; los totales de votos sí coinciden como 0. En todas las otras claves coinciden LN, no registrados y nulos.

**Diputaciones RP:** las 532 diferencias son exclusivamente del distrito 12. En cada una, el total del cómputo excede el SICEE RP exactamente por los votos de candidatura independiente presentes en SICEE MR; la suma es **18,442**. Las 36 SRP están emparejadas. SICEE RP, internamente, satisface en cada sección `RP.SEC.TOTAL_VOTOS = MR.SEC.TOTAL_VOTOS − votos candidatura independiente MR + votos SRP`. El CSV del cómputo usa el total de acta ordinaria que incluye esos votos; por tanto no son diferencias inexplicadas de captura. La [LGIPE en versión con última reforma de 27/01/2017, art. 15.2](https://www.ine.mx/wp-content/uploads/2020/07/Despen-LEGIPE-NormaINE.pdf) excluye los votos de candidaturas independientes al calcular la votación nacional emitida para asignación de diputaciones RP. Esto es compatible con la diferencia observada, pero **no demuestra por sí solo** que la columna `TOTAL_VOTOS` SICEE RP de cada casilla implemente exactamente esa definición; la documentación específica de SICEE sigue pendiente. No reemplazar ninguno de los totales ni adjudicar que uno es erróneo.

**Voto extranjero:** las 16 MEC SICEE suman los mismos votos totales que el único registro M/V de cómputo: Presidencia **4,824** y Senado MR/RP **4,519**. SICEE registra LN **11,532** y el cómputo **11,536**, diferencia **+4** en este último para ambos cargos. Conservar ambas cifras y buscar la causa documental; no ajustar la base viva.

Este cotejo identifica la versión y las transformaciones necesarias antes de proyectar resultados. No valida resoluciones posteriores, ni convierte `NULL`, blanco o `-` en cero, ni modifica fuentes maestras o base viva. No se enviaron solicitudes ni comunicaciones al INE.
