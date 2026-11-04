# HEYTI — Diputaciones federales MR 2024, CAS→SEC Guanajuato

Cotejo del 29 de septiembre de 2026 sobre el ZIP original SICEE `INE_SICEE_DIP_MR_2024_original.zip`, CSV `2024_SEE_DIP_FED_MR_NAL_CAS.csv` y `..._SEC.csv`, filtrados por `ID_ESTADO=11`. Se agrupa CAS por `(ID_DISTRITO_FEDERAL, ID_MUNICIPIO, SECCION)`.

8,159 filas CAS corresponden a 3,233 filas SEC, sin claves sin pareja ni valores vacíos en los cinco campos cotejados. En 3,223 SEC coinciden los cinco campos (`NUM_VOTOS_VALIDOS`, `NUM_VOTOS_CAN_NREG`, `NUM_VOTOS_NULOS`, `TOTAL_VOTOS`, `LISTA_NOMINAL`). En otras 10 SEC hay 30 diferencias de campo: la diferencia de `TOTAL_VOTOS` corresponde exactamente a las 11 CAS cuyo campo `TRIBUNAL` dice `ANULADA`; son 3,778 votos crudos. En las diez SEC, `LISTA_NOMINAL` coincide con la suma de todas las CAS, incluidas las anuladas. Las diferencias en componentes de votos se explican al excluir esas mismas CAS. La columna `ESTATUS_ACTA` no contiene por sí misma la marca `ANULADA`: debe leerse `TRIBUNAL` y conservar `OBSERVACIONES`.

| Distrito federal | Municipio ID | Sección | CAS anuladas | CAS votos crudos excluidos del total SEC |
|---:|---:|---:|---:|---:|
| 10 | 41 | 2797 | C1 | 410 |
| 12 | 7 | 364 | B1 | 291 |
| 12 | 7 | 398 | C1 | 300 |
| 12 | 7 | 451 | C1 | 317 |
| 12 | 7 | 530 | C2 | 362 |
| 12 | 7 | 536 | C3 | 330 |
| 14 | 2 | 71 | C1 | 306 |
| 14 | 5 | 3276 | C1 | 307 |
| 15 | 17 | 1058 | C1 | 405 |
| 15 | 17 | 3258 | B1 y C2 | 750 |
| **Total** | | **10 secciones** | **11 CAS** | **3,778** |

Esto concuerda con la matriz judicial previamente documentada en `HEYTI_Cotejo_Federal_2024_GTO_5_Series_v0_1.md`. No implica inferir la firmeza de sentencias ni trasladar el tratamiento MR a RP. La copia RP inicial era incompleta. Se recuperó de la descarga pública SICEE un ZIP íntegro con SHA-256 `57702d9440ee5b7543366bd16b680ff503c96a19c2e969675b2c4522e05605a4`, coincidente con el hash del cotejo federal previo, y prueba ZIP sin errores. Véase la actualización RP siguiente. No se alteró la base viva.

## Actualización: RP CAS→SEC

Fuente: https://sicee.ine.mx/ACTASSICEEN2024/download/FEDERALES_2024/DIPUTACIONES_FED_RP_2024.zip; CSV `2024_SEE_DIP_FED_RP_NAL_CAS.csv` y `..._SEC.csv`, `ID_ESTADO=11`. Las **8,200 CAS RP** se agrupan en **3,233 SEC** con la misma clave federal/municipal/sección. Las 3,233 SEC tienen CAS y coinciden en los cinco campos cotejados; cero diferencias y cero vacíos. RP incorpora 41 SRP a las 8,159 CAS MR; ninguna CAS RP presenta marca `ANULADA` en `TRIBUNAL`. Las once CAS con marca judicial MR siguen presentes como votos crudos en RP: este cotejo aritmético no determina su efecto jurídico RP. Mantener ambas modalidades y la nota judicial separadas.
