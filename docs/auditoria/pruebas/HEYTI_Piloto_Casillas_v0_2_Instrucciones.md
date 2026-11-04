# HEYTI — Ensayo aislado CAS v0.2

**26 de septiembre de 2026.** La extensión v0.2 aún no ha sido ejecutada en PostgreSQL. Este paquete prepara una primera prueba de cinco casillas de dos series; **no lo ejecutes sobre `at2730_core`**. El ejecutor crea una base aleatoria `heyti_cas_probe_*` y la elimina al terminar, con independencia del resultado. Si `dropdb` falla, muestra una advertencia y el nombre de la base temporal.

## Archivos

En `D:\GitHub\AT-27-30-core\docs\auditoria\pruebas` conserva los archivos del ensayo previo de proyección 23 series v0.1: `HEYTI_Staging_Electoral_v0_1_PROPUESTA_NO_EJECUTAR.sql`, `HEYTI_Prueba_Staging_Aislada_v0_1.sql`, `HEYTI_Verificacion_Carga_Cruda_23_Series_v0_1.sql`, `HEYTI_Proyeccion_23_Series_v0_1.sql` y `HEYTI_Carga_Cruda_23_Series_PRUEBA.sql.gz`. Agrega en esa misma carpeta:

- `HEYTI_Ensayo_Casillas_Piloto_v0_2.ps1` — ejecutor temporal.
- `HEYTI_Staging_Casillas_v0_2_PROPUESTA_NO_EJECUTAR.sql` — DDL adicional.
- `HEYTI_Piloto_Casillas_DF18_21_v0_2.sql` — carga y controles de cinco casillas.

Los archivos `HEYTI_Generar_Piloto_Casillas_v0_2.py` y `HEYTI_Manifiesto_CAS_23_Series_2018_2024_v0_1.json` documentan cómo se produjo el SQL, pero no son necesarios para ejecutar el `.ps1`. El ejecutor verifica los hashes del `.sql.gz` v0.1 y los dos SQL v0.2. También requiere los DDL originales del repositorio en `database\ddl` y PostgreSQL 18 en la ruta habitual.

Desde PowerShell, en esa carpeta:

```powershell
.\HEYTI_Ensayo_Casillas_Piloto_v0_2.ps1
```

Si aparece el aviso de seguridad de Windows y reconoces los archivos descargados, puedes elegir `Z` para ejecutar esta vez. El script volverá a pedir la contraseña de `postgres` para sus llamadas a PostgreSQL.

## Controles esperados

1. Los mismos controles v0.1: 15 ZIP, 23 series, 73,262 filas SEC, 524 columnas, 1,664,253 celdas.
2. Registro de dos CSV CAS asociados a su respectivo release SEC, con cinco filas CAS y sus opciones literales.
3. DF 2021 MR sección 218: tres CAS suman 918 votos; CAS anulada de 304; SEC publicado de 614.
4. DF 2018 MR sección 553: la opción PAN de una casilla permanece `NULL`, con literal vacío y causa `LITERAL_BLANK`.
5. Aviso `Piloto CAS v0.2 OK: 5 casillas...`, seguido de eliminación de la base temporal.

Si surge un error, copia la salida completa desde `ERROR:` y el nombre de la base temporal; no ejecutes manualmente ninguno de los SQL sobre la base viva. Este piloto todavía no carga las 179,779 CAS ni prueba `SECCION=0`: esas puertas siguen pendientes tras verificar el DDL y las llaves en PostgreSQL real.
