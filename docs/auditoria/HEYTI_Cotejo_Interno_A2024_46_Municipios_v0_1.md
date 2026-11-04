# HEYTI — Cotejo interno A2024 en 46 municipios

**27 de septiembre de 2026.** Fuente preservada: `INE_SICEE_GTO_PEL_2024_original.zip`; SHA-256 `13fe6a2ddb432922bddc9090f08eb0e558aeb3094ef1ba763b78d789b3d55e69`. Sin modificación a base viva.

## Método reproducible

Leer `AYUNTAMIENTOS_csv/2024_SEE_AYUN_GTO_{MUN,SEC,CAS}.csv` del ZIP y agrupar por `ID_MUNICIPIO` (46 identidades). Comparar las 19 columnas numéricas `PAN`, `PRI`, `PRD`, `PVEM`, `PT`, `MC`, `MORENA`, `PAN_PRI_PRD`, `PAN_PRI`, `PAN_PRD`, `PRI_PRD`, `CAND_IND_1`, `CAND_IND_2`, `CAND_IND_3`, `NUM_VOTOS_VALIDOS`, `NUM_VOTOS_CAN_NREG`, `NUM_VOTOS_NULOS`, `TOTAL_VOTOS`, `LISTA_NOMINAL`. Los vacíos se tratan como cero **solo para la suma de comprobación**, sin modificar ni reinterpretar el dato original. Para votos CAS, excluir `TRIBUNAL=ANULADA`; para `LISTA_NOMINAL`, incluir todas las CAS, incluso anuladas.

| Nivel | Filas | Cotejo municipal | Diferencias |
|---|---:|---|---:|
| MUN | 46 | Base de comparación | — |
| SEC | 3,257 | 46 municipios × 19 columnas | 0 |
| CAS | 8,168 | 46 municipios × 18 columnas de votos, excluyendo 58 CAS anuladas | 0 |
| CAS | 8,168 | 46 municipios × `LISTA_NOMINAL`, incluyendo todas las CAS | 0 |

En CAS aparecen además dos marcas `MODIFICADA` y 8,108 marcas vacías; las dos filas modificadas se incluyen en la suma tal como constan en el archivo.

Si se excluyen las 58 CAS anuladas **también** al sumar lista nominal, se producen cuatro diferencias artificiales: municipio 3 San Miguel de Allende 144,253 frente a 139,016 (5,237); 7 Celaya 405,800 frente a 403,008 (2,792); 17 Irapuato 463,972 frente a 443,144 (20,828); 37 Silao de la Victoria 153,531 frente a 146,276 (7,255). La lista nominal del municipio sí coincide con la suma CAS completa. La anulación de votos no elimina a los electores de la lista nominal.

## Alcance y límite

Este cotejo demuestra **coherencia aritmética interna** del ZIP bajo esas reglas. No certifica que el corte sea definitivo ni que coincida con sentencias posteriores. En San Miguel de Allende, los tres niveles se alinean en 75,386 votos, mientras la sentencia federal SM-JDC-517/2024 y acumulados recompuso el municipio a 76,757 después de restituir cuatro casillas. Por ello A2024 continúa `BLOCKED_JUDICIAL_CUT_CONFLICT` y `presentation_selection=UNDECIDED`. Véase `HEYTI_Alerta_Corte_Judicial_A2024_SICEE_v0_1.md`.

Fuente jurisdiccional: https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JDC-0517-2024.pdf (apartado III, efectos y cómputo modificado).
