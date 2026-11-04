# HEYTI — Cobertura del ZIP federal de cómputos 2024 en Guanajuato

Corte de análisis: 29/09/2026. Fuente original: `20240608_2030_COMPUTOS(1).zip`, corte declarado 08/06/2024 20:30 UTC-6, SHA-256 `f0b0f90483720374eaac50cfb356b43425697fabfa3f963d22a5b8f2d849312f`. Filtrado exacto de entidad 11; lectura de PRES, SEN y DIP_FED. Sólo lectura; no base viva.

| Tipo de fila | PRES | SEN | DIP_FED |
|---|---:|---:|---:|
| B/C/E ordinaria | 8,103 | 8,103 | 8,103 |
| S especial | 41 | 82 (41 MR + 41 RP) | 82 (41 MR + 41 RP) |
| A voto anticipado | 15 | 15 | 15 |
| M | 5 | 5 | 0 |
| V | 2 | 2 | 0 |
| P | 2 | 0 | 0 |
| **Total filas Guanajuato** | **8,168** | **8,207** | **8,200** |

En las 8,103 B/C/E por cargo, la suma LN es **4,831,142**; las claves y cifras por casilla coinciden entre los tres archivos según el cotejo previo de A2024. Los 41 especiales de PRES tienen LN cero; SEN/DIP_FED desdoblan MR/RP por `TIPO_ACTA`, no representan 82 casillas físicas distintas. Las filas A/M/V/P requieren interpretación documental de tipo y cargo antes de integrarse o emparejarse con `MEC` local. No sumar cargos ni modalidades como una única elección.

Este archivo federal respalda LN de las casillas locales ordinarias, pero **aún no constituye cotejo de votos federales contra una descarga SICEE PEF 2024 equivalente**. Mantener pendiente esa comparación fuente contra fuente, y no trasladar cifras de Gubernatura/Ayuntamientos a cargos federales.
