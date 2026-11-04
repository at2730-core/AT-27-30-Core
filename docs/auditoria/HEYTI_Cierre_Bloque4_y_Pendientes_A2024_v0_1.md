# HEYTI — Cierre técnico del Bloque 4 y pendientes A2024

Fecha: 2026-10-03. Evidencia de ejecución: salidas aportadas por el usuario en su repositorio Windows. Este documento no certifica un corte electoral ni modifica la matriz de selección.

## Resultado del Bloque 4 corregido

La prueba real PostgreSQL del candidato judicial de San Miguel de Allende terminó satisfactoriamente en `heyti_cas_full_probe_d12d6718adb8`.

Candidato ejecutado: `A2024_SMA_SM_JDC_517_2024_DERIVED_v0_1:9877e067498a1a332589951308012820051042f63fe9bb5bbc12300a388a0716`.

Se verificaron 106 unidades y 1,802 celdas: 102 unidades sin delta y cuatro con restitución. El total derivado es 76,757, obtenido de 75,386 + 1,371.

| Unidad | Base | Delta | Derivado |
|---|---:|---:|---:|
| SEC:156 | 1,515 | 361 | 1,876 |
| SEC:172 | 1,964 | 453 | 2,417 |
| SEC:191 | 296 | 284 | 580 |
| SEC:200 | 1,301 | 273 | 1,574 |

La corrección conserva `SPECIAL_SECTION_ROW` para `SEC0:["", "9", "3", "SAN MIGUEL DE ALLENDE"]`; no la transforma en sección ordinaria ni en `SPECIAL_AGGREGATE`. El snapshot base conserva originales, marcas ANULADA, lista nominal e identidad especial. La ejecución informó ausencia de escritura DB, selección, certificación y conexión del candidato al runtime. El snapshot de lectura quedó cerrado.

Presentación RESULT y NOMINAL_LIST: `NO_RELEASE_SELECTED`.

## Validación y alcance

- Suite completa anterior a la corrección: 471 pruebas y 65 subtests aprobados.
- Después de la corrección: 11 pruebas y 17 subtests del candidato aprobados.
- Después de la corrección: prueba PostgreSQL del candidato aprobada.

No se atribuye a la suite completa anterior una validación de la versión corregida. El ensayo permite cerrar la implementación del candidato para auditoría; la presentación electoral sigue pendiente de selección y evidencia de corte.

## Revisión adicional de pendientes municipales

Se consultaron fuentes oficiales TEEG y TEPJF. La búsqueda adicional no produjo una sentencia pertinente de cómputo municipal que permita reclasificar León, Salamanca o Cortazar. El índice TEEG presentó acceso intermitente y errores 403; por ello no se declara revisado exhaustivamente. Ausencia de hallazgo no equivale a ausencia de impugnación.

| Municipio | Control de votos del registro previo | Estado conservado | Trabajo pendiente |
|---|---:|---|---|
| León | 711,277 | JUDICIAL_NO_REVISADO | Identificar resolución de cómputo municipal y su cadena de revisión; separar asuntos de registro y regidurías. |
| Salamanca | 125,852 | JUDICIAL_NO_REVISADO | Localizar resolución municipal pertinente; no usar procedimientos sancionadores ni diputación local XX para cerrar ayuntamiento. |
| Cortazar | 48,698 | JUDICIAL_NO_REVISADO | Completar inventario postelectoral y cotejar efectos sobre el cómputo municipal. |

Los controles numéricos anteriores proceden del registro municipal adjuntado, no de una nueva certificación externa. Los 27 municipios pendientes de ese registro conservan su estado. Las diferencias de lista nominal mantienen su tratamiento separado del resultado electoral.

## Referencias oficiales y trazabilidad

- SM-JDC-517/2024 y acumulados: https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JDC-0517-2024-
- SUP-REC-22097/2024 y acumulados: https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-22097-2024
- Índice de boletines TEEG 2024: https://www.teegto.org.mx/boletines2024.html
- Boletín 22/2024: https://teegto.org.mx/22-2024boletin.html — asunto de registro de planilla en León; no constituye cotejo del cómputo municipal.

Archivo de referencia local: `HEYTI_Registro_Municipal_A2024_46_v0_1(1).md` adjuntado por el usuario. No se sobrescribe ese registro ni la base original.

## Siguiente entrega necesaria

Completar el inventario de expedientes postelectorales pertinentes, registrar fecha, municipio, elección, efectos y cadena de revisión, y sólo entonces proponer cambios de estado con evidencia. No es necesario repetir la carga ni el ensayo PostgreSQL ya aprobado para continuar esta investigación documental.
