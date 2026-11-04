# HEYTI — Preflight de proyección de 23 series

**26 de septiembre de 2026, hora de México.** Diseño para ensayo temporal; no se ha ejecutado esta proyección completa en PostgreSQL. Reutiliza los cinco archivos del ensayo de carga cruda ya probado. No altera `at2730_core` ni publica resultados.

| Año | Unidades | Celdas de opción y agregados | Vacíos que permanecen `NULL` | Totales publicados vacíos |
|---|---:|---:|---:|---:|
| 2018 | 28,237 | 812,581 | 276,022 | 0 |
| 2021 | 15,825 | 322,863 | 59,088 | 3 |
| 2024 | 29,200 | 528,809 | 6,466 | 0 |
| **Total** | **73,262** | **1,664,253** | **341,576** | **3** |

Se revisaron los 23 CSV originales: no hay llaves de unidad duplicadas dentro de una serie ni discordancias entre suma de opciones electorales y `TOTAL_VOTOS` donde el total es numérico. Los tres totales vacíos corresponden a A 2021 secciones 163 y 2541, y DL RP 2021 sección 1080. Se conservan con causa genérica `SOURCE_BLANK_UNCLASSIFIED` hasta incorporar la evidencia judicial/documental; no se convierten en cero.

El SQL cataloga 524 columnas con etiqueta literal. Distingue 197 partidos, 169 combinaciones, 96 columnas independientes, 23 no registrados, 23 nulos y 16 agregados `NUM_VOTOS_VALIDOS`. Los agregados válidos se guardan pero **no** se vuelven a sumar al total de candidaturas. La etiqueta independiente no resuelve por sí sola la identidad de la candidatura. Cada año se inserta y verifica en su propia transacción; una discrepancia detiene el ensayo y la base temporal se elimina mediante el ejecutor.

## Archivos para agregar a PRUEBAS

1. `HEYTI_Ensayo_Proyeccion_23_Series_v0_1.ps1`
2. `HEYTI_Proyeccion_23_Series_v0_1.sql`

Los cinco archivos anteriores del ensayo crudo permanecen en `D:\GitHub\AT-27-30-core\docs\auditoria\pruebas`. Ejecutar desde esa carpeta:

```powershell
.\HEYTI_Ensayo_Proyeccion_23_Series_v0_1.ps1
```

La carga de 1.66 millones de celdas puede tardar varios minutos en el equipo de Alex. El ejecutor crea `heyti_full_probe_*`, comprueba hashes, carga los originales GTO en staging, proyecta por año, verifica sumas y elimina esa base temporal al concluir. Un `COMMIT` se refiere únicamente a la base de ensayo.

**Límite:** proyección seccional no equivale a certificación completa de actas, corte judicial, alianzas/candidaturas o ganador. Quedan por conciliar actas de casilla, fuentes→staging→consulta y la cadena Capability→Runtime→Materialización→UI antes de integración o visibilidad.
