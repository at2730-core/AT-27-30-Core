# HEYTI — Corrección del contrato de casillas en staging v0.2

**26 de septiembre de 2026.** Propuesta de diseño, sin ejecutar SQL ni modificar `at2730_core`.

## Evidencia

El staging v0.1 ya guarda 23 CSV SEC, 73,262 filas GTO, con 524 columnas catalogadas y 1,664,253 celdas proyectadas. El manifiesto CAS v0.1 agrega sus 23 archivos compañeros, fijados por SHA-256 del ZIP y del CSV: **179,779 filas GTO**, incluidas **221 filas de casilla con `SECCION=0`**. No deben confundirse con las 137 filas SEC de sección cero: la relación es muchos-a-uno según identidad especial.

El esquema `HEYTI_Staging_Electoral_v0_1_PROPUESTA_NO_EJECUTAR.sql` contiene `acta_evidence`, pero su clave foránea `(member_id, series_id) → election_series(member_id, series_id)` exige que `member_id` sea el CSV **SEC** de la serie. Su otra clave `(member_id, raw_row_id) → raw_row(member_id, raw_row_id)` no puede señalar simultáneamente el CSV **CAS**. Por ello, **la v0.1 probada no admite todavía la carga íntegra de actas de casilla**, aunque sí la de secciones. Tampoco tiene tabla de votos literales por opción en cada casilla.

## Contrato requerido para v0.2

1. Registrar cada CSV CAS como `source_member`, con sus SHA-256, cabecera, codificación y conteos del manifiesto. Registrar sus filas como `raw_row` sin modificar el texto literal.
2. Crear una asociación `series_cas_member` que vincule el `series_id` seccional con el `member_id` CAS, exigiendo que ambos `source_member` pertenezcan al **mismo `source_release`**. En SQL, se puede imponer con claves únicas `(release_id, member_id)` en `source_member`, dos FKs compuestas al mismo `release_id`, y FK `(section_member_id,series_id)` a `election_series`.
3. Crear `casilla_tally` con FK a `series_cas_member`, `raw_row` CAS y `computation_unit` SEC. La clave de acta debe incorporar entidad, sección, distrito/municipio aplicables, tipo de casilla, número, `EXT_CONTIGUA` y, cuando proceda, identidad especial `SECCION=0`/MEC. No usar solo el número de sección ni mezclar MR y RP.
4. Crear `casilla_option_vote` con FK compuesta a `casilla_tally` y a `option_column` de la misma serie. Guardar `raw_value`, valor numérico o `NULL`, motivo de ausencia, y ordinal de columna. Guardar aparte `TOTAL_VOTOS`, `LISTA_NOMINAL` y sus literales.
5. Conservar `ESTATUS_ACTA`, `TRIBUNAL`, `JUICIO`, `OBSERVACIONES` y `RUTA_ACTA` como campos literales/procedencia, además de `raw_cells`. La referencia `RUTA_ACTA` no equivale a un PDF disponible. Añadir referencia y hash de imagen sólo cuando se obtenga físicamente el archivo.
6. Materializar por separado el total CAS crudo y el total SEC publicado. La reconciliación debe clasificar: igualdad numérica, diferencia exactamente explicada por CAS marcadas anuladas, ambos vacíos, SEC numérico con CAS vacía, SEC vacía con CAS numérica y diferencia residual. Nunca corregir SEC sumando CAS por defecto.

## Puerta de ensayo aislado

En una base temporal, probar al menos DF 2021 MR sección 218 (CAS 918, una anulada de 304, SEC 614); A 2021 secciones 163/2541 (SEC `NULL` tras anulación); DL RP 2021 sección 1080 (`NULL` distinto de MR 0); una de las 173 casillas con vacío literal; y una unidad especial `SECCION=0`. Verificar que la vista SEC existente sigue reproduciendo las 73,262 unidades y que CAS queda trazable por SHA, fila y columna. Sólo después ensayar carga completa y verificar 179,779 filas CAS.

**Estado:** contrato propuesto. La v0.1 se mantiene como evidencia del ensayo exitoso de resultados SEC; no se reescribe ni se declara certificada la cadena CAS hasta probar la extensión.
