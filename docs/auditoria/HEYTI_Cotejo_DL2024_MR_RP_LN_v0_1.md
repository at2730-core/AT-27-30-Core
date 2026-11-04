# HEYTI — Cotejo Diputaciones Locales 2024, MR/RP y lista nominal

Corte de análisis: 29/09/2026. Lectura de ZIP originales; sin modificar base viva.

Fuentes: IEEG `09062024_1200_COMPUTOS_GTO(1).zip/GTO_DIP_LOC_2024.csv` (8,206 filas); INE SICEE `INE_SICEE_GTO_PEL_2024_original.zip`, `2024_SEE_DIP_LOC_MR_GTO_CAS.csv` (8,169 filas) y `2024_SEE_DIP_LOC_RP_GTO_CAS.csv` (8,210 filas). Claves ordinarias: entidad 11, sección, tipo B/C/E, ID y extensión. Claves especiales: sección y `ACTA_CASILLA-MEC` completa (SMR/SRP); distrito/modalidad para VA antes de cualquier mapeo.

## Casillas ordinarias

Cada paquete contiene las mismas **8,103** claves B/C/E. En cada modalidad MR y RP, `TOTAL_VOTOS` coincide IEEG/SICEE en **8,103/8,103**; la LN coincide en **2,830** y difiere en **5,273**. La distribución de LN es idéntica a A2024 y G2024. El control federal por clave ya comprobado para estas 8,103 claves A2024 favorece SICEE, pero su catálogo puede ser compartido entre elecciones; conservar valores crudos por serie.

## Casillas especiales y denominador

IEEG contiene **82** filas S, identificadas por `ACTA_CASILLA-MEC` como 41 SMR y 41 SRP, con 14,614 votos en total. La descarga SICEE MR contiene **41 SMR** (6,629 votos) y la descarga RP contiene **82**: las mismas **41 SMR** y 41 SRP (14,614 votos). Al emparejar por sección + acta, los votos coinciden **41/41** MR y **82/82** RP; LN IEEG es 1,000 en cada una, SICEE 0. **MR está incluida en el archivo RP**: sumar ambos ZIP SICEE duplicaría 41 actas y 6,629 votos. Para materializar, usar el archivo RP como conjunto SMR+SRP o la unión deduplicada por acta, preservando modalidad; nunca sumar archivos completos sin llave.

Las especiales no tienen lista nominal propia según el manual oficial de cómputos federales 2024 (https://ayuda.ine.mx/2024/assets/docs/computos/mas-temas/manual-base-datos-computos.pdf, p. 21). No interpretar el `1000` IEEG como electores nominales sin diccionario local.

## Voto anticipado

IEEG tiene **21** filas A (una por distrito con datos), y cada una de las descargas SICEE MR/RP tiene **25** filas A desglosadas por municipio. Agrupadas por **ID_DISTRITO_LOCAL numérico**, las 21 sumas de votos y LN son idénticas IEEG/SICEE: **121 votos, LN 162** en ambas modalidades. No inferir identidad fila a fila ni sumar MR y RP como si fueran distintas votaciones anticipadas; son dos publicaciones de la elección con coincidencia de valor en este subconjunto. No confundir con el caso de 2 votos nulos del voto anticipado GUB.

Estado de decisión: LN ordinaria `SICEE_RESPALDADA_CASILLA`; especiales `LN_NO_APLICA`; VA `AGREGADO_DISTRITAL_COINCIDE / CLAVE_FILA_SIN_MAPEO`; cobertura MR/RP `RP_INCLUYE_SMR`. Verificar criterio de modalidades y actas antes de integrar a HEYTI.

### Comprobación de inclusión MR→RP

Se construyó llave completa SICEE con distrito local, municipio, sección, tipo, ID, extensión y `ACTA_CASILLA-MEC`. Las **8,169/8,169 filas del archivo MR** están también en RP con los mismos `TOTAL_VOTOS` y `LISTA_NOMINAL`: 8,103 B/C/E, 41 SMR y 25 A. El archivo RP agrega **exactamente 41 SRP**. La comparación de todos los campos compartidos encuentra una sola variación textual de mayúsculas/minúsculas en `ESTATUS_ACTA` de una VA (`Acta Casilla`/`ACTA CASILLA`); no hay diferencia numérica en el subconjunto. Por tanto, MR es subconjunto de RP **en estas descargas específicas**. Preservar la procedencia de cada ZIP y la distinción SMR/SRP, sin asumir que todos los procesos históricos tendrán la misma relación.
