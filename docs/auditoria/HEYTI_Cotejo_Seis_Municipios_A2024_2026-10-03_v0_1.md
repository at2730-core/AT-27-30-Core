# HEYTI — Cotejo agrupado de seis municipios A2024

Fecha local: 3 de octubre de 2026. Base de ensayo: `heyti_cas_full_probe_d12d6718adb8`. Evidencia PostgreSQL: salidas de consultas de solo lectura ejecutadas por Alex. No se realizaron escrituras, selección de cortes ni certificación.

## Resultados comprobados

| ID | Municipio | Total SEC = CAS | Filas SEC | Filas CAS | Secciones ordinarias | Controles judiciales coincidentes |
|---|---|---:|---:|---:|---:|---|
| 1 | Abasolo | 42081 | 50 | 121 | 50 | 7/7 partidos publicados |
| 2 | Acámbaro | 49490 | 91 | 182 | 90 | 5/5 candidaturas publicadas |
| 4 | Apaseo el Alto | 26930 | 44 | 94 | 44 | 7/7 controles por candidatura y total |
| 5 | Apaseo el Grande | 38680 | 46 | 128 | 45 | 8/8 controles por candidatura y total |
| 14 | Dolores Hidalgo | 67475 | 72 | 207 | 71 | 8/8 controles por candidatura y total |
| 15 | Guanajuato | 92458 | 103 | 258 | 102 | 11/11 controles publicados |

990 filas CAS y 406 SEC: totales numéricos, sin marcas TRIBUNAL. Las marcas vacías no prueban inexistencia de impugnaciones. En las 402 secciones ordinarias: 7236 comparaciones de campos, cero cobertura inválida, cero valores no numéricos y cero diferencias CAS→SEC. SEC=0 quedó fuera de este cotejo seccional. Hay 46 controles numéricos judiciales ensayados, todos coincidentes. No equivale a cotejo exhaustivo de todos los rubros de todas las sentencias.

## Tratamiento de coaliciones

En Apaseos, Dolores Hidalgo y Acámbaro se suma PAN + PRI + PRD + PAN_PRI_PRD + PAN_PRI + PAN_PRD + PRI_PRD para comparar la candidatura de coalición. No se redistribuyen votos a partidos. En Guanajuato se comparó separadamente la suma de las cuatro combinaciones (1562) además de cada partido.

## Acámbaro: etiquetas recuperadas y cotejo comprobado

El fallo local TEEG-REV-31/2024, página PDF 4 (impresa 3), publica cinco candidaturas: Paulet Fernández Martínez 1165; Mayra Alcantar León 2036; Tonathiu Albarrán Martínez 2209; Olga Lidia Tirado Zúñiga 19354; Claudia Silva Campos 22413. Los tres últimos controles inequívocos previamente ensayados fueron PT 2036, MORENA 19354 y coalición 22413. El registro oficial IEEG identifica a Paulet como PVEM y Tonathiu como MC. Alex ejecutó el cotejo final: PVEM 1165 y MC 2209 coinciden en 91 filas SEC por campo, cero no numéricos y diferencia cero. Con ello las cinco candidaturas publicadas coinciden con staging. La suma de las cinco candidaturas es 47277; no se infieren de ella los valores individuales de nulos o candidaturas no registradas.

Cadena localizada: TEEG-REV-31/2024 confirmó el cómputo; SM-JRC-229/2024 desechó por falta de legitimación procesal; SUP-REC-816/2024, 31/07/2024, desechó porque la resolución recurrida no era de fondo. La sentencia definitiva de Sala Superior se distingue del proyecto preliminar publicado en otra ruta. Ninguno de los desechamientos acredita por sí mismo un cotejo de fondo del vector.

## Fuentes oficiales consultadas

- Abasolo: https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JRC-0307-2024.pdf (tabla de siete partidos en PDF p. 2; desechamiento por extemporaneidad).
- Acámbaro local: https://oficialiapartes.congresogto.gob.mx/Files/294499/Exp294499-LXV-8112020240628150214.pdf (escaneo inspeccionado).
- Acámbaro federal: https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JRC-0229-2024-
- Acámbaro Sala Superior, fallo definitivo: https://www.te.gob.mx/media/SentenciasN/pdf/Superior/SUP-REC-0816-2024.pdf
- Etiquetas Acámbaro: https://ieeg.mx/registro-de-candidaturas/ (tabla de presidencias municipales, registro PEL 2023–2024).
- Apaseo el Alto: https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JDC-0545-2024-
- Apaseo el Grande: https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JDC-0450-2024.pdf
- Dolores Hidalgo: https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JRC-0302-2024-
- Guanajuato: https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JDC-0451-2024.pdf

## Límites y pendientes

Conservación de las cuatro identidades SEC0 comprobada; verificar otros posibles medios posteriores, corte, fechas, hashes y política de selección. Abasolo mantiene cotejo parcial de siete partidos; los seis totales municipales se contrastaron con controles del registro previo. Los resultados internos y documentales no seleccionan releases ni autorizan presentación. La base original y las fuentes crudas permanecen conservadas.

## Actualización del 4 de octubre: identidades SEC0

Salida PostgreSQL proporcionada por Alex al cierre del 3 de octubre: cuatro pares crudos CAS/SEC coinciden en votos y LN.

| Municipio | Clave CAS original | Votos CAS = SEC | LN CAS = SEC | Distrito local conservado |
|---|---|---:|---:|---|
| Acámbaro | VA31 | 2 | 2 | 22 |
| Apaseo el Grande | VA22 | 2 | 2 | 17 |
| Dolores Hidalgo | VA01 | 3 | 3 | 1 |
| Guanajuato | VA34 | 13 | 21 | 8 |

Las cuatro computation_unit conservan unit_kind SPECIAL_SECTION_ROW, section_code 0, original_identity con municipio y distrito originales, y territorial_section_id NULL. Abasolo y Apaseo el Alto no devolvieron filas especiales bajo los filtros ejecutados. Este control comprueba conservación interna de las identidades e igualdad numérica; no acredita mapeo oficial de claves de voto anticipado entre IEEG e INE ni sustituye el cotejo de cada columna del vector SEC0. No se hicieron escrituras a PostgreSQL.


## Actualización del 4 de octubre: vectores SEC0 y lista nominal

Alex ejecutó dos consultas adicionales de solo lectura, ambas concluidas con ROLLBACK.

- SEC0: 18 campos en cada uno de los municipios 2, 5, 14 y 15; 72 comparaciones CAS→SEC. Cero cobertura inválida, cero campos no numéricos y cero campos discordantes.
- LN por sección: 406 secciones (402 ordinarias y cuatro especiales); cero cobertura inválida, cero secciones con LN no numérica y cero discordancias CAS→SEC.
- Acumulado de votos: 7308 comparaciones (7236 ordinarias + 72 especiales), sin diferencias. Cada campo se compara independientemente; NUM_VOTOS_VALIDOS y TOTAL_VOTOS no se suman nuevamente a sus componentes.

| ID | Municipio | Secciones cotejadas | SEC0 | LN SEC = CAS |
|---|---|---:|---:|---:|
| 1 | Abasolo | 50 | 0 | 71493 |
| 2 | Acámbaro | 91 | 1 | 99549 |
| 4 | Apaseo el Alto | 44 | 0 | 51751 |
| 5 | Apaseo el Grande | 46 | 1 | 75745 |
| 14 | Dolores Hidalgo | 72 | 1 | 124993 |
| 15 | Guanajuato | 103 | 1 | 153389 |

Estos valores son sumas de la LN publicada; no acreditan por sí solos equivalencia con un padrón municipal certificado ni el significado normativo de LN para casillas especiales. La identidad SPECIAL_SECTION_ROW permanece conservada.

### Búsqueda adicional de recursos posteriores

El 4 de octubre se consultaron búsquedas públicas por números de expedientes SM-JDC-545/2024, SM-JDC-450/2024, SM-JRC-302/2024, SM-JDC-451/2024, SM-JDC-452/2024 y SM-JRC-307/2024, combinados con SUP-REC o reconsideración y nombres municipales. No se obtuvo un nuevo fallo posterior directamente vinculado al cómputo de estas elecciones. Las referencias a precedentes antiguos, registro de candidaturas y fiscalización no se incorporan como modificaciones del cómputo.

La búsqueda no acredita inexistencia de recursos posteriores. Se conserva pendiente la trazabilidad judicial de los cinco municipios distintos de Acámbaro; para este último ya está localizado SUP-REC-816/2024. No se modifican selection_status ni certification_status. El cotejo interno de votos y LN del grupo queda comprobado dentro de los filtros ejecutados, sin selección de corte ni autorización de presentación.
