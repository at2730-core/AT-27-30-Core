# HEYTI — Preflight del piloto DF 2021 MR

**26 de septiembre de 2026.** Próxima puerta en una base temporal; este piloto todavía no se ejecutó en PostgreSQL de Alex. Usa la carga cruda de 15 ZIP/23 series ya probada, proyecta solo DF 2021 MR y cataloga columnas de las 23 series. No modifica `at2730_core` ni los JSON de V1.

## Cotejos fuera de PostgreSQL

- El catálogo existente cubre todas las columnas electorales de los 23 encabezados. Clasifica 197 columnas de partido, 169 combinaciones, 96 columnas independientes literales, 23 de no registrados, 23 de nulos y 16 agregados de votos válidos: **524 columnas**. Un campo de agregado `NUM_VOTOS_VALIDOS` no se suma como candidatura adicional.
- Las 3,174 filas DF 2021 MR de Guanajuato tienen 3,174 llaves únicas: 3,159 secciones ordinarias y 15 `SECCION=0` diferenciadas por distrito federal. Ninguna se enlaza forzosamente al catálogo territorial vigente.
- Hay 23 columnas de votos/opciones en DF 2021 MR: **73,002 celdas** en 3,174 filas. **9,522 celdas vacías** se preservan como `NULL` con causa, sin convertirlas en cero.
- En las 3,174 filas, la suma de columnas de opción numéricas publicadas coincide con `TOTAL_VOTOS`; la sección 218 MR tiene total 614. Esto no selecciona RP ni resuelve candidaturas independientes ambiguas.

## Ensayo en Windows

En `D:\GitHub\AT-27-30-core\docs\auditoria\pruebas`, conservar los cinco archivos del ensayo de carga cruda que ya pasaron. Agregar solo:

1. `HEYTI_Ensayo_Proyeccion_Piloto_DF2021_MR_v0_1.ps1`
2. `HEYTI_Proyeccion_Piloto_DF2021_MR_v0_1.sql`

Desde esa carpeta:

```powershell
.\HEYTI_Ensayo_Proyeccion_Piloto_DF2021_MR_v0_1.ps1
```

El ejecutor verifica el ZIP SQL por SHA-256, crea una nueva base `heyti_raw_probe_*`, aplica el DDL y la carga cruda ya conocidos, incorpora las 524 columnas clasificadas, proyecta únicamente DF 2021 MR y compara 73,002 celdas con 3,174 totales y los 9,522 vacíos. Elimina la base de prueba al final. Si falla una restricción, la transacción de proyección se revierte y se conserva la salida del error para diagnóstico.

**Límite:** aún faltarán las otras 22 series en `computation_unit`, `section_tally` y `option_vote`, actas a nivel casilla, política de corte y la cadena completa a interfaz. El piloto no acredita resultados electorales para publicación.
