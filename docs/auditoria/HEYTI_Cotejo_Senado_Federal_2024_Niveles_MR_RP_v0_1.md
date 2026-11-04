# HEYTI — Senadurías federales 2024, niveles SICEE MR y RP, Guanajuato

Fecha: 29 de septiembre de 2026. Fuentes originales: `INE_SICEE_SEN_MR_2024_original.zip` y `INE_SICEE_SEN_RP_2024_original.zip`, CSV `2024_SEE_SEN_FED_{MR,RP}_NAL_*.csv` filtrados a `ID_ESTADO=11`. Campos: `NUM_VOTOS_VALIDOS`, `NUM_VOTOS_CAN_NREG`, `NUM_VOTOS_NULOS`, `TOTAL_VOTOS`, `LISTA_NOMINAL`.

| Modalidad | Nivel publicado | Filas GTO | Resultado |
|---|---|---:|---|
| MR | SEC | 3,234 | Base, incluye distrito/municipio/sección 0 del voto en el extranjero |
| MR | DIS | 16 | 16/16 iguales a la suma SEC por distrito federal |
| MR | MUN | 47 | 47/47 iguales a la suma SEC por municipio |
| MR | ENT | 1 | Igual a las sumas SEC, DIS y MUN en cinco campos |
| RP | SEC | 3,234 | Base, incluye unidad 0 |
| RP | MUN | 47 | 47/47 iguales a la suma SEC por municipio |

No hubo claves SEC sin agregación, diferencias ni vacíos en los cinco campos cotejados. El ZIP RP no contiene tablas generales `NAL_DIS.csv` ni `NAL_ENT.csv`: publica `NAL_DISPP.csv` y `NAL_ENTPP.csv`, desgloses de partidos que requieren un cotejo específico de su estructura; no se declara validación directa de DIS o ENT generales para RP. El cotejo CAS→SEC de ambas modalidades se documentó en `HEYTI_Cotejo_Senado_2024_CAS_SEC_MR_RP_v0_1.md`. No sumar MR y RP entre sí ni alterar la base viva.
