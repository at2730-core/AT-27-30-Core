# HEYTI — Cotejo de lista nominal Gubernatura 2024 por casilla

Corte de análisis: 29/09/2026. Sólo lectura de los ZIP originales; ninguna escritura en la base viva.

## Archivos y llaves

- IEEG: `09062024_1200_COMPUTOS_GTO(1).zip`, `GTO_GUB_2024.csv`, corte 09/06/2024 12:00 UTC-6; SHA-256 del ZIP `d1a2760a600206358f4e376ea2f3ab67c6e33548db7bb4abc4aaede0c7a865b5`.
- INE SICEE: `INE_SICEE_GTO_PEL_2024_original.zip`, `2024_SEE_GOB_GTO_CAS.csv`. Los campos ordinarios se emparejaron por entidad Guanajuato, sección, tipo B/C/E, ID de casilla y extensión contigua. No usar esta llave a ciegas para sección cero.
- Control federal: `20240608_2030_COMPUTOS(1).zip`, `PRES_2024.csv`, corte 08/06/2024 20:30 UTC-6; SHA-256 `f0b0f90483720374eaac50cfb356b43425697fabfa3f963d22a5b8f2d849312f`.

## Resultados ordinarios

| Estado LN IEEG vs SICEE | Casillas B/C/E | LN en cómputo federal PRES |
|---|---:|---|
| Igual | 2,830 | Coincide con ambas |
| Distinta | 5,273 | Coincide con SICEE en todas |
| **Total** | **8,103** | **8,103/8,103 SICEE** |

Los 8,103 registros ordinarios emparejados tienen `TOTAL_VOTOS` idéntico entre IEEG y SICEE **dentro de Gubernatura**. La distribución de diferencias de LN es idéntica a la observada en A2024: 5,199 diferencias absolutas de 1–5 y 74 >5. Esta coincidencia entre elecciones locales y el control federal sugiere reutilización de un catálogo de LN por casilla; no prueba independencia de los sistemas del INE ni explica técnicamente el dato IEEG. Preferencia propuesta de LN ordinaria: SICEE con valor crudo IEEG preservado y procedencia explícita.

## Fuera del conjunto ordinario

- **41 especiales S** tienen votos idénticos IEEG/SICEE y LN IEEG=1,000 frente a SICEE=0. En cómputos federales las mismas 41 claves figuran con LN=0; el manual federal indica que especiales no tienen lista nominal propia. Estado `LN_NO_APLICA_CASILLA_ESPECIAL`; el significado exacto de `1000` en el CSV IEEG sigue sin diccionario.
- IEEG GUB contiene 8,166 filas: 8,103 B/C/E, 41 S, 21 A y 1 MEC. SICEE GUB contiene 8,176: 8,103 B/C/E, 41 S, 25 A y 7 MEC. Las filas A/MEC no tienen correspondencia por sección/tipo/ID/extensión: IEEG utiliza secciones sintéticas 9001–9021 y 9042, mientras SICEE usa sección cero. Se debe reconstruir su identidad con campos adicionales, sin crear un mapeo por intuición.
- SICEE contiene dos pares MEC con el mismo `SECCION=0, TIPO=MEC, ID_CASILLA=1/2` pero `ACTA_CASILLA-MEC` distingue `VeMRE01/02` de `VMRE01/02`. **No son duplicados de fila**: la llave abreviada colisiona y perdería votos/LN si se impone unicidad. Para MEC, preservar `ACTA_CASILLA-MEC` y tipo/canal de voto antes de diseñar llave histórica.

Pendiente: comparar GUB A/MEC por modalidad, lugar y acta usando documentación pública; decidir el tratamiento por canal sólo tras cotejo. Sin cambio a producción.

## Reconstrucción A/MEC con documento de claves

El anexo oficial INE de modificación al Anexo 15 del Reglamento de Elecciones, pp. 11 y 38 (https://repositoriodocumental.ine.mx/xmlui/bitstream/handle/123456789/163803/INE-CCOE-001-2024-a1.pdf) define `VMRE01/02` como mesas de voto postal en el extranjero, `VeMRE01/02` como mesas de voto electrónico por internet y `VA01/02` como mesas de voto anticipado. Por ello la llave para MEC SICEE debe incluir **`ACTA_CASILLA-MEC` completa**. Las 7 filas SICEE GUB son 2 electrónicas (`VeMRE01/02`, 6,750 votos, LN 8,346) y 5 postales (`VMRE01…05`, 2,467 votos, LN 3,718): **9,217 votos, LN 12,064** en total. La única fila MEC IEEG GUB, sección sintética 9042, registra **9,217 votos y LN 0**. El total de votos coincide agregado, pero no hay correspondencia uno a uno ni equivalencia de LN; conservar desglose SICEE y fila IEEG cruda, sin proyectar `LN=0` como padrón de los residentes en el extranjero.

El voto anticipado GUB A aparece en IEEG en 21 filas por distrito local, sección sintética 9001–9021 y `ACTA_CASILLA-MEC=VA01` repetida; SICEE tiene 25 filas por municipio con sección cero y actas `VA01…VA31`. Al **agrupar por distrito local**, LN coincide en **21/21** (162 en total) y votos coinciden en **20/21** distritos. En el **distrito 22**, IEEG tiene 4 votos y LN 2 frente a SICEE 2 votos y LN 2 (una fila `VA31` en Acámbaro). Total A IEEG **132 votos, LN 162**; SICEE **130 votos, LN 162**. Esta es una discrepancia de votos por distrito que no se explica por desagregación de identidades; estado `VA_GUB_D22_VOTOS_IEEG_SICEE_DIF_2`. Conservar ambos, cotejar acta pública distrital antes de adjudicar, y no extender la diferencia a elección A2024, cuyo voto anticipado tiene otro universo y totales.

### Detalle de la discrepancia VA del distrito local 22

La fila IEEG GUB `ID_DISTRITO_LOCAL=22, SECCION=9021, TIPO_CASILLA=A, ID_CASILLA=01, ACTA_CASILLA-MEC=VA01` tiene `PAN=1`, `NUM_VOTOS_VALIDOS=2`, `Nulos=2`, `TOTAL_VOTOS=4`, `LISTA_NOMINAL=2`, participación calculada **200.0000%**, estatus **Grupo de Recuento**, `RECONTADA=1`, `TRIBUNAL=-`, `RUTA_ACTA=-`. La fila SICEE `ID_DISTRITO_LOCAL=22, MUNICIPIO=ACAMBARO, SECCION=0, TIPO_CASILLA=A, ID_CASILLA=31, ACTA_CASILLA-MEC=VA31` tiene `PAN=1`, `MORENA_PT_PVEM=1`, `NUM_VOTOS_VALIDOS=2`, `NUM_VOTOS_NULOS=0`, `TOTAL_VOTOS=2`, `LISTA_NOMINAL=2`, estatus **GRUPO DE RECUENTO**, ruta de acta vacía. La diferencia está en los **dos nulos adicionales consignados por IEEG**; los dos votos válidos coinciden agregados. Por la falta de imagen de acta/cotejo público directamente recuperable, esto sigue siendo **conflicto de fuente**, no imputación de causa ni prueba de alteración. El valor IEEG de 4 supera su LN 2 y requiere nota de calidad especial; la elección de registro para materialización de VA GUB queda pendiente del acta o resolución, con ambos valores preservados.

### Efecto en el total estatal GUB

La suma de **todos los registros por tipo**, preservando las siete filas MEC SICEE, muestra IEEG **2,721,630 votos / 55,916 nulos** en 8,166 filas frente a SICEE **2,721,628 votos / 55,914 nulos** en 8,176 filas. B/C/E aportan los mismos votos y nulos en ambas fuentes; lo mismo S y MEC. Sólo A difiere: IEEG **132 votos / 6 nulos** frente a SICEE **130 votos / 4 nulos**. Por tanto, la diferencia estatal exacta de **2 votos** procede del conflicto VA del distrito local 22, sin otras diferencias agregadas en votos. El total IEEG de 55,916 nulos coincide con su publicación oficial de resultados de Gubernatura (https://ieeg.mx/realiza-ieeg-computo-estatal-y-entrega-constancia-a-gobernadora-electa/); eso confirma procedencia de IEEG, **no resuelve la divergencia con SICEE**. Los resultados por opción válidos están pendientes de un cotejo equivalente antes de concluir identidad total. Mantener `GUB2024_TOTAL_VOTOS_CONFLICTO_VA_D22_2_NULOS`; no sustituir resultados de la base viva por criterio de LN ordinaria.
