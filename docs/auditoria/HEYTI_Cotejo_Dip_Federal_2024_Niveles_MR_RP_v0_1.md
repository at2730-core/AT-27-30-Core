# HEYTI — Diputaciones federales 2024, niveles SICEE MR y RP, Guanajuato

Fecha: 29 de septiembre de 2026. Paquetes originales `INE_SICEE_DIP_MR_2024_original.zip` y descarga pública RP íntegra SHA-256 `57702d9440ee5b7543366bd16b680ff503c96a19c2e969675b2c4522e05605a4`; CSV `2024_SEE_DIP_FED_{MR,RP}_NAL_*.csv` filtrados a `ID_ESTADO=11`. Comparación de `NUM_VOTOS_VALIDOS`, `NUM_VOTOS_CAN_NREG`, `NUM_VOTOS_NULOS`, `TOTAL_VOTOS` y `LISTA_NOMINAL`.

| Modalidad | Nivel publicado | Filas GTO | Resultado |
|---|---|---:|---|
| MR | SEC | 3,233 | Base del cotejo |
| MR | DIS | 15 | 15/15 iguales a suma SEC por distrito federal |
| MR | MUN | 46 | 46/46 iguales a suma SEC por municipio |
| MR | ENT | 1 | Igual a sumas SEC, DIS y MUN en cinco campos |
| RP | SEC | 3,233 | Base del cotejo |
| RP | MUN | 46 | 46/46 iguales a suma SEC por municipio |

No hubo grupos sin nivel agregado, diferencias ni vacíos en los campos cotejados. MR SEC ya refleja la exclusión numérica de 11 casillas con `TRIBUNAL=ANULADA` repartidas en diez secciones; ese ajuste no genera nueva discrepancia SEC→DIS/MUN/ENT. RP conserva los votos crudos de esas casillas y tiene consistencia CAS→SEC→MUN, pero esto no determina su efecto jurídico RP.

RP no incluye CSV generales `NAL_DIS.csv` ni `NAL_ENT.csv`; ofrece `NAL_DISPP.csv`, `NAL_ENTPP.csv` y `NAL_CIR.csv`, que requieren cotejo según su propio desglose. No se declaran verificados como agregados generales. Mantener MR y RP separados, conservar metadatos judiciales y no modificar la base viva. Ver `HEYTI_Cotejo_Dip_Federal_MR2024_CAS_SEC_11_Anuladas_v0_1.md`.
