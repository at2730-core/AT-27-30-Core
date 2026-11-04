# HEYTI — Matriz de cierre e integración electoral

Fecha: 30/09/2026. Alcance: procesos 2018, 2021 y 2024. Documento de trabajo para revisión; no certifica las 23 series ni autoriza cambios en la base viva.

## Resultado verificado en esta sesión

DL2018 MR, distrito local 13, Silao de la Victoria: el archivo IEEG `Computo_x_casillas_Diputaciones_2017_2018_1.xlsx`, hoja `Diputaciones`, contiene 307 casillas y 128 secciones. Comparación IEEG contra SICEE CAS: 307 claves emparejadas y cero diferencias en 18 campos (14 categorías de voto, no registrados, nulos, total y lista nominal). Se homologaron únicamente etiquetas C01/C1, E01/E1, E01C01/E1C1 y SMR01/S1, sin modificar votos. No hay claves duplicadas. Los totales por casilla IEEG coinciden con la suma de sus categorías numéricas.

| Campo | SICEE DIS | Suma SICEE SEC | Suma SICEE CAS | IEEG por casilla |
|---|---:|---:|---:|---:|
| MORENA crudo | 9,439 | 19,439 | 19,439 | 19,439 |
| Votos válidos | 74,623 | 84,623 | 84,623 | 84,623 (calculado) |
| Total | 77,976 | 87,976 | 87,976 | 87,976 |

Conclusión: corroboración externa del detalle y discrepancia de agregación DIS de −10,000 en estos tres campos. La causa y el corte jurídico definitivo no están probados. Propuesta para el producto derivado: utilizar el detalle corroborado, identificando fuente, modalidad y corte, con aviso de discrepancia DIS. Conservar DIS íntegro. No sustituir el original ni declarar rectificación oficial.

## Nueva evidencia G2024 VA distrito 22

Se descargó el acta IEEG Acta/012/2024 completa (48 páginas). Se revisaron visualmente las páginas 32, 34, 47 y 48: p.32 identifica el inicio del cómputo de Gubernatura el 6 de junio de 2024; p.34 aporta los encabezados de la tabla; p.47 contiene la fila sección 9021, tipo **A01**, con PAN=1, PVEM_PT_MORENA=1, NOREG=0, NULOS=2 y TOTAL=4. Los restantes campos de voto de esa fila son cero. Los válidos calculados son 2. P.48 consigna aprobación del acta el 6 de junio de 2024. El OCR es auxiliar; la lectura de la fila y sus encabezados se hizo sobre las imágenes orientadas correctamente.

Esta evidencia corrobora las cifras IEEG reportadas (4 totales / 2 nulos), pero el acta muestra A01, mientras el reporte de CSV usa VA01 y SICEE VA31. No demuestra equivalencia formal de las tres etiquetas, causa de los dos nulos, ausencia de ajustes posteriores ni el corte definitivo de SICEE. El reporte de rastreo anterior queda superado en su afirmación de que no se había inspeccionado un renglón correspondiente a sección 9021. No se afirma haber comprobado cada casilla del PDF ni disponer del acta individual de escrutinio.

## Matriz por asunto

Los estados siguientes provienen del Registro Único de Pendientes de 30/09/2026, excepto la corroboración DL13 realizada aquí. Se revisaron también los dos reportes de agregados locales 2018. Sus conteos se consolidan documentalmente en esta versión; no se presenta esa lectura como una nueva ejecución de los 91 cotejos. Los demás reportes detallados no disponibles no se dan por revisados ni certificados.

| ID | Estado de evidencia | Condición para integración | Cierre de investigación |
|---|---|---|---|
| LN24 | Cotejo por casilla concluido según registro; causa/corte pendientes | SICEE como propuesta de LN ordinaria, con procedencia; conservar IEEG y confirmar semántica | Propuesto como causa no adjudicada, pendiente consolidación del reporte |
| CCPC24 | 18 excepciones censales/ordinarias; explicación territorial pendiente | Separar residencia y ubicación; no reasignar 97/115 por inferencia | Propuesto como correspondencia no adjudicada |
| ESPEC24 | LN IEEG 1,000 / SICEE 0 en 41 especiales | Preservar literales; no usar esta LN como denominador de participación ordinaria; semántica específica pendiente | Propuesto como definición pendiente |
| VA24 | A: identidad formal de claves pendiente. G D22: 4/2 votos, diferencia de 2 nulos | Mantener modalidades e identidades por fuente; no elegir total G definitivo ni transferir conflicto a A | G D22: IEEG corroborado en acta de sesión p.47; diferencia SICEE y mapeo de claves no adjudicados |
| AG18 | 91 filas examinadas según reportes: 53 discordantes (42 internas + 11 adicionales), 37 iguales y 1 indeterminada | No reemplazar todos los agregados por SEC. DL13: detalle corroborado como propuesta derivada con trazabilidad | DL13 corroborado externamente; otras 52 discordancias sin adjudicación documental. Reportes de cobertura revisados; cierre de investigación propuesto con reservas |
| DF18RP | Diferencia aritmética de 18,442 ligada a independientes MR, según registro | Conservar MR/RP y totales por fuente; no sumar ni equiparar modalidades | Explicación aritmética disponible; definición específica pendiente |
| EXT18 | LN extranjera SICEE 11,532 / cómputos 11,536 | Conservar ambas LN y no distribuir +4 entre MEC | Causa no adjudicada propuesta |
| ESP21 | Especiales DL2021 sin etiqueta MR/RP; 14 secciones con indeterminación | Preservar filas e identidad incierta; excluir asignación automática por orden | Identidad no adjudicada propuesta |
| JUD | Aritmética CAS→SEC cotejada según registro; 3 totales SEC2021 NULL | Registrar anulaciones y corte judicial por fuente; preservar NULL y distinguir cero/vacío | Documentación de integración pendiente |
| DB | 2,449/3,228 secciones P2024 discordantes en auditoría previa | Recuperar SQL y repetir fuente→DB con claves y definiciones equivalentes; incluir partidos/coaliciones/totales/LN | Verificación técnica pendiente; no se cierra como falta de evidencia pública |

## Condiciones de cierre e integración

1. Cerrar cada investigación como corroborada, explicada aritméticamente o no adjudicada, con evidencia y límites. No adjudicado no significa dato corregido ni certificado.
2. Para cada serie registrar fuente, archivo, hash, modalidad, nivel territorial, corte y tratamiento judicial. Conservar opciones partidistas/coaliciones/candidaturas con sus definiciones.
3. Consolidar los reportes detallados restantes antes de declarar cierre general. El índice de pendientes no reemplaza su evidencia.
4. Preparar staging o base de prueba, plan de reversión y comparación fuente→DB. Sin acceso al repositorio/base local no se declara ejecutada esta validación.
5. Verificar cobertura de las 23 series, claves, vacíos, NULL, cero, anulaciones, identidades ambiguas y conflictos. No usar sumas de universos distintos como prueba de cobertura.
6. Entregar preguntas a Alex; no contactar autoridades. Después de validar la integración, continuar con DB→Capability→Runtime→Materialización y Golden Cases antes de migrar módulos.

## Preguntas documentadas para Alex

- VA24 G D22: El acta de sesión p.47 respalda 2 nulos y total 4 para 9021 A01. ¿Qué corte u operación explica SICEE total 2 / nulos 0 y qué catálogo vincula A01/VA01/VA31?
- AG18: ¿qué documentos explican los agregados discrepantes y el DIS de DL13 frente al detalle corroborado?
- LN24/CCPC24/ESPEC24: ¿cuál es la definición y corte de LN, su correspondencia territorial y el significado del literal 1,000 en especiales?
- VA24 A: ¿qué catálogo vincula formalmente las claves de ambas publicaciones?
- DF18RP: ¿TOTAL_VOTOS RP excluye las candidaturas independientes MR por definición?
- EXT18: ¿qué corte o ajuste explica la diferencia de cuatro en LN extranjera?
- ESP21: ¿qué catálogo o actas identifican MR/RP de las filas especiales ambiguas?

## Huellas de los archivos consultados

- `IEEG_2018.zip`: SHA-256 `2fa32b5a6a717d221da52ccb1ad08cd32eb807784274167c1d94a3a5cb1aeb08`.
- `GTO_PEL_2018.zip`: SHA-256 `c5683d3bdadb4025880ddecb7c0de32b63cf9f2909bd2cfed760452669bc3b04`.
- `HEYTI_Registro_Unico_Pendientes_Auditoria_Electoral_v0_1(1).md`: SHA-256 `1d4949f63c107abad2a5ab53c79a578fb4cec04a6cbc2bc24f232d6372a73668`.
- `HEYTI_Rastreo_Publico_G2024_VA_D22_v0_1(1).md`: SHA-256 `64d6afa76aa3cd2611b0df1c38b5f64e86460cacfbd355a158a552d9c23b8345`.
- Acta IEEG CD22, 48 páginas: SHA-256 `cca1fff4e23d881a0d421b415ec865f1e1469d521851377c57774bcc5bdc24ff`. URL: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cd22-acta-12.pdf.

## Consolidación documental AG18

Reportes revisados: `HEYTI_Cotejo_Agregados_2018_42_vs_SEC_CAS_v0_1(1).md` y `HEYTI_Cobertura_Agregados_2018_MUN_DIS_vs_SEC_v0_1(1).md`, ambos con corte 29/09/2026.

| Clasificación | A MUN | DL MR DIS | G DIS | Total |
|---|---:|---:|---:|---:|
| Falla aritmética interna y discordancia frente a SEC | 20 | 10 | 12 | 42 |
| Discordancia frente a SEC sin falla interna | 4 | 7 | 0 | 11 |
| Cinco campos iguales a SEC | 21 | 5 | 11 | 37 |
| Total y LN coinciden, válidos indeterminados | 1 | 0 | 0 | 1 |
| Filas examinadas | 46 | 22 | 23 | 91 |

Los 42 y los 11 son grupos distintos: 53 discordancias. Los cinco casos con componentes diferentes están dentro de los 42; no se suman aparte. DL13 está dentro de los 11; tras el cotejo independiente quedan 52 discordancias sin adjudicación documental, más la fila indeterminada A San Felipe MUN30. G contiene 23 filas DIS según el reporte: esto no se interpreta como 23 distritos ordinarios sin revisar la identidad de esa fila adicional.

- En 37 de los 42, sólo difiere TOTAL_VOTOS frente a SEC; en cinco también difieren componentes: A San José Iturbide MUN32, A Tierra Blanca MUN40, DL Celaya DIS16, DL Valle de Santiago DIS19 y G León DIS21. SEC/CAS coinciden en los cinco campos para esas cinco claves según reporte; no se fabrica una corrección mezclando niveles.
- En A San Miguel de Allende, León y Silao, CAS supera SEC en 6,214 / 2,695 / 1,906 votos, coincidiendo con las CAS marcadas Anulada (21 / 9 / 7). Esos conteos de casillas no se suman con los 53 agregados. La explicación CAS→SEC no explica automáticamente los residuos MUN→SEC de −1 / −394 / −10.
- A San Miguel contiene tres SEC con válidos vacíos y A San Felipe una SEC con válidos vacío. Son vacíos de 2018 y no se confunden con los tres NULL de 2021. No imputar cero.
- A Irapuato: MUN/MUNCAND 204,910; MUNPP 202,964; SEC 207,777. DL Salamanca DIS14: DIS 117,034; DISCAND 115,806; DISPP 116,563; SEC 117,679. Mantener los totales y sus definiciones separados.
- DL Guanajuato DIS8: dos CAS de 398 votos comparten el vector del residuo, sin marca TRIBUNAL. No deducir anulación ni seleccionar una por esa igualdad.
- LN coincide agregado→SEC en las 91 filas, según el reporte; eso no certifica los votos ni establece por sí solo la definición de LN.

### Tratamiento propuesto para AG18

Cerrar el bloque de cotejo documental como **consolidado con reservas**. Conservar las 53 incidencias entre niveles, diferenciando DL13 corroborado externamente y las otras 52 no adjudicadas. Mantener A San Felipe como indeterminado. No declarar todas las fuentes certificadas ni corregir MUN/DIS masivamente.

En la integración separar datos originales de agregados derivados. Un agregado calculado desde SEC debe identificarse como derivado de esa fuente/corte y modalidad; no presentarlo como el cómputo oficial MUN/DIS rectificado. Mantener detalle CAS crudo y SEC con sus tratamientos judiciales, sin sumarlos ni mezclarlos. La elección de un valor de presentación sigue condicionada a la matriz por serie y a validación fuente→DB.

SHA-256 `HEYTI_Cotejo_Agregados_2018_42_vs_SEC_CAS_v0_1(1).md`: `ba64426208622be56bc545a0829e6aadf1f37daf93638bb8e2040ee784f0dea9`.

SHA-256 `HEYTI_Cobertura_Agregados_2018_MUN_DIS_vs_SEC_v0_1(1).md`: `dce4b2049d733efb41be6fd8536cbafa742a19f52483f07da275294c742257e4`.
