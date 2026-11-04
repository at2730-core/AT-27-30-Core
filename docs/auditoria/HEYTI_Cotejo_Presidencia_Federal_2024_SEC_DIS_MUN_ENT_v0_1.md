# HEYTI — Presidencia federal 2024, SEC→DIS/MUN→ENT Guanajuato

Revisión del 29 de septiembre de 2026. Fuente SICEE original `INE_SICEE_PRES_2024_original.zip`, CSV `2024_SEE_PRE_NAL_{SEC,DIS,MUN,ENT}.csv`, `ID_ESTADO=11`. Se cotejaron exactamente `NUM_VOTOS_VALIDOS`, `NUM_VOTOS_CAN_NREG`, `NUM_VOTOS_NULOS`, `TOTAL_VOTOS`, `LISTA_NOMINAL`.

| Nivel | Filas GTO | Resultado de cotejo |
|---|---:|---|
| SEC | 3,234 | Base del agrupamiento; incluye una fila SEC=0 de voto en el extranjero |
| DIS | 16 | 16/16 coinciden con suma SEC por `ID_DISTRITO_FEDERAL`, incluido distrito 0 |
| MUN | 47 | 47/47 coinciden con suma SEC por `ID_MUNICIPIO`, incluido municipio 0 |
| ENT | 1 | Coincide con la suma SEC, DIS y MUN en los cinco campos |

No hay claves SEC sin DIS o MUN, diferencias numéricas ni valores vacíos en los campos cotejados. Los totales ENT son `TOTAL_VOTOS=2,759,092` y `LISTA_NOMINAL=4,843,711`; este último incluye la unidad de voto en el extranjero y por eso no equivale a la suma de lista nominal de casillas ordinarias únicamente. El cotejo CAS→SEC está en `HEYTI_Cotejo_Presidencia_Federal_2024_CAS_SEC_v0_1.md`. La consistencia aritmética interna no reemplaza el cotejo con la publicación de cómputos ni determina firmeza jurídica. Base viva intacta.
