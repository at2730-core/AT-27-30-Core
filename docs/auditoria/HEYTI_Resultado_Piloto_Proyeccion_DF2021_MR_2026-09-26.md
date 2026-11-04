# HEYTI — Resultado del piloto de proyección DF 2021 MR

**26 de septiembre de 2026.** Evidencia: salida de PowerShell compartida por Alex al ejecutar `D:\GitHub\AT-27-30-core\docs\auditoria\pruebas\HEYTI_Ensayo_Proyeccion_Piloto_DF2021_MR_v0_1.ps1`. Base de prueba `heyti_raw_probe_ed839934fe12`. No se utilizó `at2730_core`.

| Control | Evidencia | Estado |
|---|---|---|
| DDL de staging y prueba de restricciones | 11 tablas, `NOTICE ... OK`, `ROLLBACK` de fixtures | Pasó |
| Carga cruda repetida | `COPY 73262`, `INSERT 0 73262`, 23 series, 137 `SEC=0` | Pasó |
| Catálogo de opciones | `INSERT 0 524` | Pasó |
| Identidades DF 2021 MR | `INSERT 0 3174` | Pasó |
| Totales y lista nominal del piloto | `INSERT 0 3174` | Pasó |
| Celdas de opción del piloto | `INSERT 0 73002` | Pasó |
| Conciliación numérica | `opciones=total en 3174 unidades` | Pasó |
| Vacíos literales | `9522 vacíos preservados` | Pasó |
| Caso judicial MR, sección 218 | `sección 218=614` | Pasó |
| Transacción de proyección | `COMMIT`, `PILOTO DF 2021 MR OK` | Pasó |
| Limpieza de la base temporal | `Eliminando únicamente ...`, contraseña y regreso al prompt sin advertencia del script | Sin error reportado; no hay consulta `pg_database` independiente |

El piloto distingue 3,159 secciones ordinarias y 15 registros `SECCION=0` dentro de las 3,174 unidades DF 2021 MR. La carga de 524 columnas cataloga las 23 series, pero `section_tally` y `option_vote` solo se poblaron para DF 2021 MR. No se equiparan columnas independientes a personas ni se reparten combinaciones de coalición. La igualdad opciones→total es interna al CSV de este piloto; no certifica que otras modalidades o la maestra legado sean correctas.

**Estado:** puerta de proyección piloto superada en PostgreSQL 18, sin integración en la base viva. La continuación de la auditoría queda pausada a solicitud de Alex hasta que indique retomar.
