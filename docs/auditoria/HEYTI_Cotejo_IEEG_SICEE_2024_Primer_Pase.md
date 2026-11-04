# HEYTI — Cotejo IEEG/SICEE 2024, primer pase

**27 de septiembre de 2026.** Lectura local de ZIP preservados; sin escritura a PostgreSQL. Comparación exploratoria por sección ordinaria y columnas literales PAN, PRI, PVEM, MORENA y TOTAL_VOTOS. No es certificación de corte ni dictamen de causa.

## Método

- IEEG: `IEEG_Computos_2024_original.zip`, CSV internos `GTO_AYUN_2024.csv`, `GTO_DIP_LOC_2024.csv` y `GTO_GUB_2024.csv`; encabezado de actas en línea 9 (después de ocho líneas de metadatos). Se sumaron los valores de filas `CONTABILIZADA=1` por `SECCION`. En diputaciones MR se excluyeron las actas especiales `SRP` del mismo CSV IEEG.
- SICEE: `INE_SICEE_GTO_PEL_2024_original.zip`, CSV `2024_SEE_AYUN_GTO_SEC.csv`, `2024_SEE_DIP_LOC_MR_GTO_SEC.csv` y `2024_SEE_GOB_GTO_SEC.csv`. Se tomó el valor SEC publicado para la misma sección.
- Se excluyó `SECCION=0` de la comparación y se identificaron aparte las claves 9000+. Las columnas de combinaciones y candidaturas se preservan sin atribución a los cuatro partidos.
- La lista nominal se revisó en un pase adicional: la suma de `LISTA_NOMINAL` en CAS SICEE coincide con SEC en las 3,233 secciones ordinarias de cada serie. Se aplicó igual suma a IEEG, excluyendo `SRP` para DL MR.

## Resultado preliminar

| Serie | Secciones con al menos una fila IEEG contabilizada y par SEC | PAN | PRI | PVEM | MORENA | TOTAL_VOTOS | Secciones con alguna diferencia en esos cinco campos |
|---|---:|---:|---:|---:|---:|---:|---:|
| Ayuntamientos 2024 | 3,233 | 52 | 53 | 51 | 52 | 53 | 53 |
| Diputaciones locales 2024, MR | 3,233 | 0 | 0 | 0 | 0 | 0 | 0 |
| Gubernatura 2024 | 3,232 | 0 | 0 | 0 | 0 | 0 | 0 |

**Corrección del primer cálculo:** el CSV IEEG de diputaciones incluye actas `SRP` junto a `SMR`; comparar ambas con SICEE MR produjo 34 falsas discrepancias. Tras excluir `SRP`, no quedan diferencias en los cinco campos revisados. SICEE tiene 3,233 claves de sección ordinaria únicas en cada serie. En IEEG gubernatura la sección 2445 solo tiene una fila B con `CONTABILIZADA=0` y `TOTAL_VOTOS=0`; se dejó fuera del par contabilizado. Por tanto, la coincidencia de gubernatura cubre 3,232 pares, no toda la serie.

En los archivos IEEG hay claves 9000+ (`24` en ayuntamientos, `21` en diputaciones y `22` en gubernatura) sin par por número en SEC SICEE. Se registran como unidades especiales pendientes de identidad, no como secciones ordinarias faltantes. El conteo de secciones con al menos una fila contabilizada puede ser menor que el de claves presentes en IEEG.

En ayuntamientos, **51 de 53 secciones** tienen diferencias en los cinco campos que coinciden exactamente con la suma de las casillas SICEE marcadas `TRIBUNAL=ANULADA` (58 filas CAS). Las otras dos, secciones **176 y 216**, contienen casillas `TRIBUNAL=MODIFICADA`; sus residuos respecto al IEEG son respectivamente `PRI=-100, TOTAL_VOTOS=-100` y `PAN=+19, PRI=-66, PVEM=+1, MORENA=-15, TOTAL_VOTOS=-74` (IEEG menos SICEE). Esta igualdad aritmética describe la transformación observada, no verifica todavía la sentencia ni el acta original.

Los encabezados internos IEEG 2024 señalan `09/06/2024 12:00 (UTC-6)`. Es una etiqueta del corte IEEG preservado; no demuestra que el ZIP SICEE sea contemporáneo ni final.

## Lista nominal, cotejo adicional

En **2,657 de 3,233 secciones** la LN sumada de casillas IEEG difiere de la LN SEC SICEE. El patrón es **idéntico** para A, DL MR y G: 2,159 diferencias positivas y 498 negativas (IEEG menos SICEE), con saldo aritmético +36,372, mínimo -640 y máximo +2,001. En otras 576 secciones coincide. Se validó antes que la suma de LN CAS SICEE reproduce SEC exactamente en las tres series. El mismo patrón transversal apunta a un insumo territorial/LN compartido entre elecciones, pero **esa causa es una inferencia**, no una explicación documental probada. No se debe usar indistintamente LN IEEG y LN SICEE ni calcular participación cruzando votos de una versión con LN de la otra.

**Casillas especiales:** en gubernatura IEEG hay 41 filas `TIPO_CASILLA=S` distribuidas en 38 secciones ordinarias, con LN 1,000 por fila. Las 41 CAS especiales SICEE correspondientes registran LN `0`. Esta diferencia de criterio explica un componente de 41,000 unidades de LN en la suma de esas secciones, aunque coexisten otros cambios. Al retirar solo la contribución de las especiales IEEG, **2,654 secciones aún difieren** (rango residual -640 a +561); por tanto, no explica la discrepancia general. El saldo de diferencias puede ser menor que 41,000 porque hay diferencias negativas en otras casillas.

El detalle reproducible por sección está en `HEYTI_Desglose_LN_IEEG_SICEE_2024_por_Seccion.csv` (3,233 filas, campos de ambos cortes, contribución especial y residual). Se comprobaron además igualdad de LN por sección entre A/DL MR/G dentro de cada fuente. Por ejemplo, la sección 1349 conserva seis casillas B/C01–C05 en ambos archivos: LN IEEG 643/643/643/642/642/642 frente a SICEE 750/749/749/749/749/749. El residual -640 corresponde a valores distintos de **las mismas seis casillas**, no a una casilla faltante. No se atribuye aún el cambio a una actualización específica del padrón o de la lista nominal.

## Pendientes antes de adjudicar diferencias

1. Revisar las resoluciones y actas de las 51 secciones con anulación, especialmente las secciones 176 y 216 con modificación. En la sección 156, dos casillas `ANULADA` de 361 y 343 votos suman la diferencia de 704.
2. Obtener metadatos de la versión de LN y cotejar las casillas con mayores diferencias. La diferencia de 2,657 secciones ya está verificada por suma CAS→SEC SICEE; la causa y el corte siguen pendientes.
3. Repetir el cotejo para 2021 A/DL, donde los archivos IEEG contienen corte interno `10/06/2021 10:00 (UTC-5)`, distinto de la etiqueta `20210610_1200` del ZIP interno.
4. Mantener `UNDECIDED` en las 23 selecciones para presentación hasta documentar versiones, sentencias y cobertura.
