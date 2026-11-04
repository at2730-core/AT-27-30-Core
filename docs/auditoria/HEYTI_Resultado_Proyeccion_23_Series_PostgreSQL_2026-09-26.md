# HEYTI — Resultado de la proyección de 23 series en PostgreSQL 18

**26 de septiembre de 2026.** Evidencia: salida de PowerShell compartida por Alex al ejecutar `D:\GitHub\AT-27-30-core\docs\auditoria\pruebas\HEYTI_Ensayo_Proyeccion_23_Series_v0_1.ps1`. Base desechable `heyti_full_probe_3c782dfc29b7`; `at2730_core` no participó.

| Año | Unidades insertadas | Celdas insertadas | Vacíos preservados | Totales `NULL` | Estado |
|---|---:|---:|---:|---:|---|
| 2018 | 28,237 | 812,581 | 276,022 | 0 | `NOTICE ... OK`, `COMMIT` |
| 2021 | 15,825 | 322,863 | 59,088 | 3 | `NOTICE ... OK`, `COMMIT` |
| 2024 | 29,200 | 528,809 | 6,466 | 0 | `NOTICE ... OK`, `COMMIT` |
| **Total** | **73,262** | **1,664,253** | **341,576** | **3** | **23 series listadas** |

El proceso cargó primero 73,262 filas crudas, catalogó 524 columnas, proyectó `computation_unit`, `section_tally` y `option_vote`, y cotejó las sumas de opciones con `TOTAL_VOTOS` en cada año cuando el total era numérico. El control adicional confirmó que los tres totales vacíos se conservaron en A 2021 secciones 163 y 2541 y DL RP 2021 sección 1080. Se mostraron las 23 series con conteos por modalidad, sin errores de SQL. La salida termina en regreso al prompt después de `dropdb`, sin advertencia de limpieza; no se aportó consulta independiente a `pg_database`.

**Qué acredita:** reproducibilidad y consistencia interna de los CSV seccionales de Guanajuato al cargarse en staging versionado, separación MR/RP y preservación de vacíos y `SECCION=0`. Es una prueba en una base temporal, no una migración a HEYTI-CORE.

**Qué falta:** cotejar y preservar actas de casilla y resoluciones/cortes; acreditar candidaturas y distribución de combinaciones para cualquier cálculo de ganador; resolver procedencia y discrepancias de la maestra legado P/DF/S 2024 y G 2024 copiado de 2018; elegir versiones certificadas por elección/modalidad; verificar fuente→DB→Capability→Runtime→Materialización→UI y Golden Cases. Ninguna cifra de la base viva o pantalla queda certificada por esta prueba.
