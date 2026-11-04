# HEYTI — Cotejo CAS→SEC, Senadurías federales 2024, Guanajuato

Fecha: 29 de septiembre de 2026. Fuentes: paquetes SICEE federales originales `INE_SICEE_SEN_MR_2024_original.zip` y `INE_SICEE_SEN_RP_2024_original.zip`, archivos CSV `2024_SEE_SEN_FED_{MR,RP}_NAL_{CAS,SEC}.csv` filtrados por `ID_ESTADO=11`.

| Modalidad | CAS GTO | SEC GTO | Filas SEC=0 | SEC sin CAS | Diferencias en cinco campos |
|---|---:|---:|---:|---:|---:|
| MR | 8,166 | 3,234 | 1 | 0 | 0 |
| RP | 8,207 | 3,234 | 1 | 0 | 0 |

Cada SEC coincide con la suma de CAS en `NUM_VOTOS_VALIDOS`, `NUM_VOTOS_CAN_NREG`, `NUM_VOTOS_NULOS`, `TOTAL_VOTOS` y `LISTA_NOMINAL`. No hubo vacíos en esos cinco campos ni estatus CAS que contenga `ANULAD`. Se agrupó CAS por `(ID_DISTRITO_FEDERAL, ID_MUNICIPIO, SECCION)` para distinguir la fila `SEC=0` del voto en el extranjero. RP incluye las 8,166 filas MR y 41 SRP adicionales; no se deben sumar ambas modalidades entre sí. Las siete actas MEC dentro de la única fila SEC=0 requieren conservar su identidad individual en CAS.

Este resultado mide consistencia interna CAS→SEC y complementa `HEYTI_Cotejo_Federal_2024_GTO_5_Series_v0_1.md`, que ya cotejó SICEE con el cómputo federal publicado. No había paquete federal de Senado 2018 en los archivos locales examinados; no se declara hecho un cotejo de ese año. Sin cambios a la base viva.
