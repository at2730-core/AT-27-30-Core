# HEYTI — Resultado del ensayo aislado de staging en PostgreSQL 18

**26 de septiembre de 2026.** Evidencia: salida de PowerShell compartida por Alex al ejecutar `D:\GitHub\AT-27-30-core\docs\auditoria\pruebas\HEYTI_Ensayo_Staging_Aislado_v0_1.ps1`. Base temporal generada: `heyti_stage_probe_c68f795c7f73`. El script apunta a esa base temporal, no a `at2730_core`.

| Puerta | Evidencia observada | Estado |
|---|---|---|
| Esquema territorial y electoral del checkout | `CREATE SCHEMA`, tablas e índices sin errores | Pasó |
| DDL `electoral_stage` v0.1 | `BEGIN`, 11 `CREATE TABLE`, cuatro `CREATE INDEX`, `COMMIT` | Pasó |
| Restricciones de ensayo | `DO` y aviso `11 tablas, identidad histórica, SEC0, MR/RP, NULL y cero: OK` | Pasó |
| Persistencia de fixtures | `ROLLBACK` | No quedaron los datos de prueba |
| Estado final del proceso | `ENSAYO OK: esquema y restricciones probados en base temporal.` | Pasó |
| Eliminación de base temporal | Consulta posterior `SELECT EXISTS ... datname = 'heyti_stage_probe_c68f795c7f73'` devolvió `f` | **Confirmada** |

Este resultado demuestra que el DDL propuesto se ejecuta junto con los DDL básicos del checkout de Alex y que los casos de restricciones codificados pasan en PostgreSQL 18. No demuestra carga de las 23 series, sumas electorales en staging, permisos/índices bajo volumen real, ni certificación de la cadena UI. La consulta posterior confirmó la eliminación de la base temporal.

**Verificación de limpieza, solo lectura:**

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -X -U postgres -d postgres -tAc "SELECT EXISTS (SELECT 1 FROM pg_database WHERE datname = 'heyti_stage_probe_c68f795c7f73');"
```

Alex ejecutó la consulta y obtuvo `f`: la base temporal ya no existe. El siguiente trabajo técnico es un importador de ensayo que use el manifiesto por hash, preserve todos los campos y coteje las 23 series sin tocar `electoral.section_result`.
