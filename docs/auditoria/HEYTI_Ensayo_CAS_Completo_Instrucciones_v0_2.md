# HEYTI — Ensayo completo de 23 series CAS v0.2

**27 de septiembre de 2026.** Preparación para ejecutar en una base PostgreSQL temporal. No se modifica `at2730_core`; no ejecutar manualmente los SQL en la base viva.

En `D:\GitHub\AT-27-30-core\docs\auditoria\pruebas` deben permanecer los archivos que ya usaste en la proyección SEC y en el piloto CAS: `HEYTI_Staging_Electoral_v0_1_PROPUESTA_NO_EJECUTAR.sql`, `HEYTI_Prueba_Staging_Aislada_v0_1.sql`, `HEYTI_Carga_Cruda_23_Series_PRUEBA.sql.gz`, `HEYTI_Verificacion_Carga_Cruda_23_Series_v0_1.sql`, `HEYTI_Proyeccion_23_Series_v0_1.sql` y `HEYTI_Staging_Casillas_v0_2_PROPUESTA_NO_EJECUTAR.sql`.

Agrega en esa misma carpeta estos **cuatro archivos nuevos**:

1. `HEYTI_Ensayo_Carga_CAS_23_Series_v0_2.ps1` — ejecutor.
2. `HEYTI_Carga_Cruda_CAS_23_Series_PRUEBA.sql.gz` — carga cruda CAS comprimida, verificada por SHA-256.
3. `HEYTI_Proyeccion_CAS_23_Series_v0_2.sql` — proyección anual CAS.
4. `HEYTI_Verificacion_CAS_23_Series_v0_2.sql` — comprobaciones finales.

El manifiesto, el generador `.py` y el resultado del preflight son documentación de reproducibilidad; no son requisitos de ejecución del PowerShell. El ejecutor usa los DDL del repositorio en `database\ddl` y PostgreSQL 18 en `C:\Program Files\PostgreSQL\18\bin`. Descomprime dos SQL en la carpeta temporal de Windows y los borra al finalizar; por su tamaño, asegúrate de disponer de varios GB libres para esos archivos y las tablas de PostgreSQL. El tiempo de ejecución será mayor que el del piloto de cinco casillas.

Desde PowerShell:

```powershell
Set-Location 'D:\GitHub\AT-27-30-core\docs\auditoria\pruebas'
.\HEYTI_Ensayo_Carga_CAS_23_Series_v0_2.ps1
```

La salida esperada incluye `CAS crudo OK: 23 archivos, 179779 filas GTO`, luego tres avisos `CAS 2018/2021/2024 OK`, y al final `CAS 23 series OK: 179779 filas, 4061868 celdas, 221 SEC0, 119 exclusiones explicadas`. El script imprime el nombre de su base aleatoria `heyti_cas_full_probe_*` y la elimina al terminar. Si falla, comparte el primer `ERROR` completo y las últimas líneas de limpieza; no repitas a ciegas ni cargues datos a `at2730_core`.

**Límite de la prueba:** demostrar carga y reconciliación interna de los CSV originales no certifica imágenes de actas faltantes, texto de sentencias, candidaturas ni toda la cadena de HEYTI hasta UI. Los literales vacíos permanecen `NULL`.
