# HEYTI — Diputaciones federales 2021, CAS→SEC y niveles MR/RP, Guanajuato

Fecha: 29 de septiembre de 2026. ZIP públicos SICEE `DIPUTACIONES_FED_MR_2021.zip` (SHA-256 `90e325eed451985506750e7b03444c64b79382fdd31ab9ef4cdfb274e6a6798e`) y `DIPUTACIONES_FED_RP_2021.zip` (SHA-256 `65f86f16baa871dfba4d7bba841f4c5502bffe99d1dcf03b6150978b63bd588e`). Filtrado `ID_ESTADO=11`. Campos comparables en todos los niveles: `NUM_VOTOS_CAN_NREG`, `NUM_VOTOS_NULOS`, `TOTAL_VOTOS`, `LISTA_NOMINAL`. Agregación CAS por `(ID_DISTRITO_FEDERAL, ID_MUNICIPIO, SECCION)`.

| Modalidad | CAS | SEC | CAS→SEC | Niveles superiores publicados |
|---|---:|---:|---|---|
| MR | 7,760 | 3,174 | 3,173 SEC exactas; 1 SEC con CAS C01 anulada | DIS 15, DISPP 15, MUN 47, ENT 1, ENTPP 1: todos coinciden con sumas SEC en cuatro campos |
| RP | 7,791 | 3,174 | 3,174 SEC exactas | DISPP 15, MUN 47, ENTPP 1: todos coinciden con sumas SEC en cuatro campos |

En **MR distrito federal 2, municipio ID 3, sección 218**, CAS B=301, C01=304, E01=313: suma cruda 918, SEC=614; diferencia **−304**. La C01 está marcada `TRIBUNAL=Anulada`, `JUICIO=SM-JIN-29-2021 Y ACUMULADOS`. SEC resta también 1 voto no registrado y 8 nulos de la C01; conserva `LISTA_NOMINAL=1,872`, igual a la suma CAS. En **RP** la SEC 218 registra **918**, con la misma lista nominal. Es una diferencia por modalidad y metadatos judiciales, no una licencia para restar RP. Las fuentes de cómputo del corte 11/06/2021 y SICEE coinciden en 22 campos por CAS para MR 7,760 y RP 7,791, como se documenta en `HEYTI_Inventario_Federal_2018_2021_Fuentes_Pendientes_v0_1.md`.

En RP no hay `NAL_DIS.csv` ni `NAL_ENT.csv` generales; se validaron los desgloses DISPP y ENTPP para esos cuatro campos. Ninguna clave quedó sin agrupación; cero vacíos en los campos cotejados. No se modifica la base viva.
