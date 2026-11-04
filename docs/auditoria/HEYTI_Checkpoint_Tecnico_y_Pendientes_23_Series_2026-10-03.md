# HEYTI — Checkpoint técnico y pendientes de 23 series

Fecha: 2026-10-03. Alcance: 2018, 2021 y 2024; 2015 excluido.

## Dictamen de alcance

La carga aislada SEC/CAS, el lector PostgreSQL y la integración con runtime tienen evidencia técnica satisfactoria. Ninguna de las 23 series queda autorizada por este checkpoint para presentar resultados electorales. No se modifica la base viva ni se selecciona un corte.

Este documento consolida salidas de consola proporcionadas por el usuario. La consulta de estados de PostgreSQL fue de solo lectura y terminó con ROLLBACK. No supone acceso directo desde este entorno a la computadora del usuario.

## Evidencia técnica

Base aislada conservada: `heyti_cas_full_probe_d12d6718adb8`.

| Comprobación | Evidencia reportada | Límite |
|---|---|---|
| Suite posterior al Bloque 3 | 461 pruebas y 53 subtests aprobados | No certifica fuentes ni cortes judiciales |
| SEC, 23 series | 73,262 filas de Guanajuato; 137 SEC0 | Carga y proyección técnicas |
| CAS, 23 series | 179,779 filas; 4,061,868 celdas; 221 SEC0; 119 exclusiones explicadas | No adjudica diferencias electorales |
| Lector PostgreSQL | Nueve identidades inspeccionadas | No constituye cobertura funcional de todas las unidades |
| Runtime y entrega | Tres escenarios aprobados; cero llamadas DB en los escenarios de presentación | Entrega de estados de indisponibilidad; permisos de prueba sintéticos |

Casos reales del lector: DL2021 MR/RP 1080; A2021 163 y 2541; DF2021 MR/RP 218; P2024 1150, 343 y agregado especial SEC0. Se preservaron cero frente a NULL, literal original, modalidad e identidad especial. La genealogía de 343 no quedó certificada. DF2021 RP 218 fue cotejado con fila cruda, sin adjudicación externa.

## Estado observado en PostgreSQL

Las 15 fuentes comparten `SOURCE_AS_PUBLISHED_UNVERIFIED_DATE`, están `UNREVIEWED` y carecen de `published_at`. Las 23 series están `SOURCE_AS_PUBLISHED` y `UNREVIEWED`. Esta etiqueta identifica el archivo cargado; no acredita que sea el resultado judicial definitivo.

El registro de auditoría contiene estados más específicos que estos valores iniciales de staging. Se reproducen abajo desde la copia local de la matriz de selección. No son nuevos dictámenes ni se escribieron en PostgreSQL.

| Serie | Certificación en matriz | Pendiente registrado |
|---|---|---|
| 2018 A UNICA | PENDING_SOURCE_ADJUDICATION | Corte municipal/distrital agregado 2018 con incidencias ajenas a SEC ; Totales CAS crudos difieren de SEC por actas anuladas |
| 2018 DF MR | PENDING_SOURCE_ADJUDICATION | Vacíos SEC/CAS requieren expediente; no imputar cero |
| 2018 DF RP | PENDING_SOURCE_ADJUDICATION | Vacíos SEC/CAS requieren expediente; no imputar cero |
| 2018 DL MR | PENDING_SOURCE_ADJUDICATION | Corte municipal/distrital agregado 2018 con incidencias ajenas a SEC ; Vacíos SEC/CAS requieren expediente; no imputar cero |
| 2018 DL RP | PENDING_SOURCE_ADJUDICATION | Corte municipal/distrital agregado 2018 con incidencias ajenas a SEC ; Vacíos SEC/CAS requieren expediente; no imputar cero |
| 2018 G UNICA | PENDING_SOURCE_ADJUDICATION | Corte municipal/distrital agregado 2018 con incidencias ajenas a SEC |
| 2018 P UNICA | PENDING_SOURCE_ADJUDICATION | Vacíos SEC/CAS requieren expediente; no imputar cero |
| 2018 S MR | PENDING_SOURCE_ADJUDICATION | Vacíos SEC/CAS requieren expediente; no imputar cero |
| 2018 S RP | PENDING_SOURCE_ADJUDICATION | Vacíos SEC/CAS requieren expediente; no imputar cero |
| 2021 A UNICA | PENDING_SOURCE_ADJUDICATION | SEC 163/2541: total NULL tras anulación; antecedente IEEG separado ; Vacíos SEC/CAS requieren expediente; no imputar cero ; Totales CAS crudos difieren de SEC por actas anuladas |
| 2021 DF MR | PENDING_SOURCE_ADJUDICATION | SEC 218: 614 tras anular CAS 304; RP separado ; Totales CAS crudos difieren de SEC por actas anuladas |
| 2021 DF RP | PENDING_SOURCE_ADJUDICATION |  |
| 2021 DL MR | PENDING_SOURCE_ADJUDICATION | Vacíos SEC/CAS requieren expediente; no imputar cero ; Totales CAS crudos difieren de SEC por actas anuladas |
| 2021 DL RP | PENDING_SOURCE_ADJUDICATION | SEC 1080: total NULL, paquete no entregado; MR registra 0 ; Vacíos SEC/CAS requieren expediente; no imputar cero ; Totales CAS crudos difieren de SEC por actas anuladas |
| 2024 A UNICA | BLOCKED_JUDICIAL_CUT_CONFLICT | Alternativa IEEG 09-06-2024 preservada; comparación de cortes pendiente ; JUDICIAL_CUT_CONFLICT: SICEE marca anuladas 156 C1, 172 B, 191 B y 200 E1; Sala Monterrey revocó su nulidad; ver alerta judicial ; Totales CAS crudos difieren de SEC por actas anuladas |
| 2024 DF MR | PENDING_SOURCE_ADJUDICATION | Maestra/DB legado discrepan de SICEE; no consumir legado ; Totales CAS crudos difieren de SEC por actas anuladas |
| 2024 DF RP | PENDING_SOURCE_ADJUDICATION | Maestra/DB legado discrepan de SICEE; no consumir legado |
| 2024 DL MR | PENDING_SOURCE_ADJUDICATION | Alternativa IEEG 09-06-2024 preservada; comparación de cortes pendiente |
| 2024 DL RP | PENDING_SOURCE_ADJUDICATION | Alternativa IEEG 09-06-2024 preservada; comparación de cortes pendiente |
| 2024 G UNICA | PENDING_SOURCE_ADJUDICATION | Alternativa IEEG 09-06-2024 preservada; comparación de cortes pendiente ; Maestra legado 24G copia 18G; no consumir legado |
| 2024 P UNICA | PENDING_SOURCE_ADJUDICATION | Maestra/DB legado discrepan de SICEE; no consumir legado |
| 2024 S MR | PENDING_SOURCE_ADJUDICATION | Maestra/DB legado discrepan de SICEE; no consumir legado |
| 2024 S RP | PENDING_SOURCE_ADJUDICATION | Maestra/DB legado discrepan de SICEE; no consumir legado |

En todas las filas, la fecha de corte permanece `UNVERIFIED` y la selección de presentación `UNDECIDED`. La presentación debe conservar `NO_RELEASE_SELECTED` mientras falte selección explícita válida. Un permiso para lista nominal no autoriza votos.

## Trabajo pendiente, en orden

1. Documentar por fuente el origen oficial, ZIP y miembros SEC/CAS con hashes, fecha de publicación acreditada y significado del corte. Una fecha de descarga no sustituye una fecha de publicación o un corte judicial.
2. Preparar una correspondencia revisable entre incidencias del registro y estados de staging, especialmente el bloqueo judicial A2024. Definir alcance por serie/unidad/métrica antes de proponer una escritura; no rebajar el bloqueo por el estado inicial UNREVIEWED.
3. Adjudicar con evidencia externa los expedientes abiertos. Prioridades: conflicto judicial municipal A2024, distrito local 13 de 2018, diferencias P2024 con legado y corte G2024. Conservar todas las cifras originales y sus procedencias.
4. Solo para el alcance acreditado, formular una decisión explícita de selección con evidencia, fecha y tratamiento judicial. Después probar una lectura de presentación autorizada; hasta entonces los ensayos de entrega prueban el bloqueo y no la entrega de votos certificados.

## Criterio de cierre

La fase técnica puede registrarse como validada dentro del alcance anterior. La auditoría electoral y la habilitación de presentación siguen abiertas. Este checkpoint no integra correcciones numéricas, no habilita series, no altera hashes ni convierte vacíos en cero.
