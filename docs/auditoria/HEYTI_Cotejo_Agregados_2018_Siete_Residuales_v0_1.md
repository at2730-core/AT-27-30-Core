# HEYTI — Siete agregados SICEE 2018 con residuo adicional

Fecha de revisión: 29/09/2026. Fuente: `INE_SICEE_GTO_PEL_2018_original.zip`, archivos CSV CAS/SEC/MUN/DIS de Ayuntamientos, Diputaciones locales MR y Gubernatura. Complemento del registro `HEYTI_Incidencias_Totales_Agregados_SICEE_2018.json`. Lectura solamente; base viva intacta.

Se seleccionaron las **siete filas** cuyo `TOTAL_VOTOS` no iguala `NUM_VOTOS_VALIDOS + NUM_VOTOS_CAN_NREG + NUM_VOTOS_NULOS` y cuya diferencia no se explica únicamente por los nulos. Para cada municipio A o distrito DL/G se sumaron directamente las secciones de la misma elección, territorio y corte. El total seccional proviene también de sus casillas en el caso G distrito 21 examinado por detalle. La LN agregada coincide con la suma seccional en los siete casos.

| Elección / territorio | Total agregado | Suma total SEC | Diferencia agregado − SEC | Otros componentes agregados vs SEC |
|---|---:|---:|---:|---|
| A / Cuerámaro, MUN 12 | 11,734 | 12,267 | −533 | Válidos, no registrados y nulos iguales |
| A / Jaral del Progreso, MUN 18 | 18,032 | 18,538 | −506 | Los tres iguales |
| A / San Luis de la Paz, MUN 33 | 41,587 | 43,678 | −2,091 | Los tres iguales |
| DL MR / San Francisco del Rincón, DIS 10 | 102,162 | 106,238 | −4,076 | Los tres iguales |
| G / Guanajuato, DIS 8 | 97,147 | 97,066 | +81 | Los tres iguales |
| G / San Francisco del Rincón, DIS 10 | 103,284 | 106,287 | −3,003 | Los tres iguales |
| G / León, DIS 21 | 101,635 | 99,751 | +1,884 | Válidos 99,909 vs 97,637 (+2,272); no registrados 111 vs 111; nulos 2,047 vs 2,003 (+44) |

En **seis** territorios el problema queda acotado al campo `TOTAL_VOTOS` del agregado: los otros tres componentes y LN coinciden exactamente con SEC. En **G distrito 21**, SEC y CAS coinciden entre sí en 89 secciones y 280 casillas: 97,637 válidos, 111 no registrados, 2,003 nulos, 99,751 total y 178,486 LN. La fila DIS publica 99,909 válidos, 111 no registrados, 2,047 nulos, 101,635 total y la misma LN 178,486. Además, el total DIS difiere de la suma de sus propios componentes (102,067) en −432. Se documentan **dos niveles de discordancia** sin atribuir causa ni sustituir una cifra por otra.

Estas siete filas pertenecen al conjunto previo de **42 incidencias aritméticas** de agregados 2018 (35 con nulos omitidos exactamente y estas siete con residuo adicional). Mantener MUN/DIS, SEC y CAS como registros de su respectivo nivel, con valor literal y procedencia. Para uso operativo, no inferir un total definitivo del agregado discordante; mostrar la incidencia y consultar acta, cómputo rectificado o publicación oficial si existe. Si la documentación pública no resuelve el caso, conservar la nota de discrepancia para el reporte final y eventual consulta personal que Alex decida realizar.
