# HEYTI — Ensayo de carga cruda de 23 series en PostgreSQL 18

**26 de septiembre de 2026.** Evidencia: salida de PowerShell aportada por Alex al ejecutar `D:\GitHub\AT-27-30-core\docs\auditoria\pruebas\HEYTI_Ensayo_Carga_Cruda_23_Series_v0_1.ps1`. Base desechable: `heyti_raw_probe_0c38f0cb84b0`. No se usó `at2730_core`.

| Verificación | Evidencia observada | Resultado |
|---|---|---|
| DDL de territorial, electoral y staging | `CREATE SCHEMA`, 11 tablas de staging, índices, `COMMIT` | Pasó |
| Fixtures de restricciones | Aviso `11 tablas, identidad histórica, SEC0, MR/RP, NULL y cero: OK` seguido de `ROLLBACK` | Pasó |
| Lectura del SQL generado | `COPY 73262` | Pasó |
| Persistencia de filas crudas en base temporal | `INSERT 0 73262`, `DO`, `COMMIT` | Pasó |
| Control de cobertura | Aviso `Carga cruda OK: 15 ZIP, 23 series, 73262 filas GTO, 137 SEC=0` | Pasó |
| Conteos por serie | Salida de 23 filas; 2018 nueve series, 2021 cinco, 2024 nueve; valores concordantes con manifiesto | Pasó |
| Limpieza | Mensaje de eliminación de `heyti_raw_probe_0c38f0cb84b0`, solicitud de contraseña y regreso al prompt sin advertencia de `dropdb` | El script no reportó error; consulta explícita adicional no aportada |

**Alcance:** queda verificada la carga en un entorno aislado de releases, miembros, modalidades y 73,262 registros seccionales de Guanajuato con celdas literales y hashes de línea. Los conteos de DF 2021 (3,174 por modalidad) y A 2024 (3,257) incluyen filas `SECCION=0`; no equivalen al número de secciones ordinarias. Las 23 series no son 23 elecciones independientes: MR/RP son modalidades distintas.

**Aún no certificado:** `computation_unit`, `option_column`, `section_tally`, `option_vote`, actas, conciliación completa por opción, selección de corte, ni datos de Capability→Runtime→Materialización→UI. El ensayo no corrige la maestra legado ni los valores 2024 discordantes. La siguiente puerta es proyectar identidades y opciones en otra base desechable, manteniendo `NULL` y etiquetas literales, antes de estudiar integración en HEYTI-CORE.
