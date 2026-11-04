# HEYTI — Senado y Diputaciones federales RP 2024: DISPP y ENTPP, Guanajuato

Fecha: 29 de septiembre de 2026. Paquetes SICEE `INE_SICEE_SEN_RP_2024_original.zip` y `DIPUTACIONES_FED_RP_2024.zip` (SHA-256 `57702d9440ee5b7543366bd16b680ff503c96a19c2e969675b2c4522e05605a4`). Archivos `2024_SEE_{SEN,DIP}_FED_RP_NAL_{SEC,DISPP,ENTPP}.csv`, `ID_ESTADO=11`. Se cotejan cinco campos: votos válidos, no registrados, nulos, total de votos y lista nominal.

| Cargo RP | SEC | DISPP | ENTPP | Cotejo de cinco campos |
|---|---:|---:|---:|---|
| Senado | 3,234 | 16 | 1 | 16/16 DISPP = suma SEC por distrito; ENTPP = suma DISPP y suma SEC |
| Diputaciones | 3,233 | 15 | 1 | 15/15 DISPP = suma SEC por distrito; ENTPP = suma DISPP y suma SEC |

No hay distrito SEC sin fila DISPP ni diferencias en esos cinco campos. Incluye distrito 0 para Senado, correspondiente al voto en el extranjero. Las siete columnas de partido en ENTPP coinciden exactamente con la suma de esas mismas columnas en DISPP. En cada fila DISPP, la suma de las siete columnas de partido coincide con `NUM_VOTOS_VALIDOS`.

**Regla de interpretación:** DISPP/ENTPP distribuyen votos entre partidos; las columnas partidistas SEC contienen el desglose crudo de opciones, incluidas combinaciones de coalición. Por eso hay diferencias si se compara directamente `PAN`, `PRI`, `PVEM`, etc. SEC con las columnas homónimas DISPP: 48 pares distrito/partido en Senado y 81 en Diputaciones. Estas diferencias de representación **no son** diferencias de total de votos ni, por sí solas, errores. No se suman MR y RP. El archivo RP Diputaciones además publica `NAL_CIR.csv`, cuya unidad es circunscripción y queda fuera de este cotejo Guanajuato por estado. Conservar todas las opciones originales y la versión de fuente, sin cambios a la base viva.
