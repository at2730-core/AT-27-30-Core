# HEYTI — Resultado del ensayo CAS completo v0.2 en PostgreSQL 18

**27 de septiembre de 2026.** Evidencia: salida de PowerShell compartida por Alex al ejecutar `D:\GitHub\AT-27-30-core\docs\auditoria\pruebas\HEYTI_Ensayo_Carga_CAS_23_Series_v0_2.ps1`. Base temporal `heyti_cas_full_probe_6f5febc7166f`; el ejecutor no selecciona `at2730_core`.

## Controles observados

| Bloque | Resultado |
|---|---|
| Staging SEC v0.1 | 11 tablas y prueba de identidad histórica, SEC0, MR/RP, `NULL` y cero: OK; prueba revertida con `ROLLBACK`. |
| Carga SEC | 15 ZIP, 23 series, 73,262 filas GTO, 137 SEC0: OK. |
| Proyección SEC | 73,262 unidades, 524 columnas, 1,664,253 celdas; tres totales `NULL` de 2021 preservados. |
| DDL CAS v0.2 | `ALTER TABLE`, tres tablas e índice: `COMMIT` sin error. |
| Carga cruda CAS | `COPY 179779`, `INSERT 0 179779`, `CAS crudo OK: 23 archivos, 179779 filas GTO`, `COMMIT`. |
| Proyección CAS 2018 | 67,339 filas, 1,936,753 celdas, 658,360 vacíos: `NOTICE ... OK`, `COMMIT`. |
| Proyección CAS 2021 | 38,817 filas, 791,751 celdas, 144,959 vacíos: `NOTICE ... OK`, `COMMIT`. |
| Proyección CAS 2024 | 73,623 filas, 1,333,364 celdas, 16,318 vacíos: `NOTICE ... OK`, `COMMIT`. |
| Verificación final | 23 series listadas; 179,779 filas, 4,061,868 celdas, 221 CAS `SECCION=0`, 119 diferencias de total explicadas exactamente por casillas marcadas anuladas: OK. |

El ejecutor imprimió `ENSAYO CAS COMPLETO OK`, después `Eliminando únicamente la base temporal: heyti_cas_full_probe_6f5febc7166f`, solicitó contraseña y regresó al prompt sin advertencia. Por el control de salida de `dropdb` en el PowerShell, ello es evidencia de eliminación exitosa; no se aportó una consulta independiente a `pg_database`.

## Interpretación y límite

La carga reproducible SEC+CAS funciona en una base aislada, conserva filas crudas con su fuente y columna literal, separa MR/RP, preserva 819,637 vacíos CAS y permite reproducir 119 exclusiones judiciales de total. El hecho de que el control SEC/CAS pase no convierte los vacíos en cero ni resuelve los 1,160 cotejos con alguna casilla vacía. Tampoco acredita imagen individual de acta, texto de sentencia, correspondencia candidatura/coalición, selección del corte vigente, ni el flujo fuente→base viva→Capability→Runtime→Materialización→UI.

**Estado:** ensayo técnico completo aprobado en PostgreSQL temporal; ninguna migración a la base viva ni certificación electoral integral. La siguiente puerta es documentar por serie el corte seleccionable y las incidencias pendientes, y definir el contrato de lectura que entregue `NULL`, anulaciones y modalidad sin pérdida a HEYTI-CORE antes de escribir en producción.
