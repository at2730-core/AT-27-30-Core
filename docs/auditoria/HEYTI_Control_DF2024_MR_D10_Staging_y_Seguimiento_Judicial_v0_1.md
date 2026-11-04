# HEYTI — DF2024 MR distrito 10: staging y seguimiento judicial

Fecha: 2026-10-03. Base reportada por Alex: heyti_cas_full_probe_d12d6718adb8. Serie staging 5. Evidencia DB: salidas de consultas ejecutadas por Alex en transacciones READ ONLY terminadas con ROLLBACK; no ejecución directa de DB por el asistente. Sin escritura, selección ni certificación.

## Controles comprobados

- CAS 2797 B1: total 400, válidos 384, no registrados 2, nulos 14, LN 750; TRIBUNAL vacío.
- CAS 2797 C1: total crudo 410, válidos 402, no registrados 0, nulos 8, LN 750; TRIBUNAL ANULADA; OBSERVACIONES SM-JIN-80-2024-SENT-NUL-MOD.pdf.
- SEC 2797: total 400, vector coincidente con B1; LN 1500, CASILLAS 2 y ACTAS_CASILLA-MEC 2 preservados. La anulación no elimina el registro crudo ni reduce automáticamente LN.
- Distrito federal 10: 293 filas SEC; cero totales no numéricos; suma 204116.
- Consulta de miembro DIS mediante sustitución del sufijo _SEC.csv por _DIS.csv: cero filas. Esto identifica ausencia de esa ruta esperada en el catálogo consultado, no demuestra ausencia universal de datos distritales bajo otros nombres.

## Vector distrital cotejado

Cada campo siguiente cuenta 293 filas, cero valores no numéricos y diferencia cero frente al control del cómputo modificado de SM-JIN-80/2024. Son columnas originales de voto por partido/combinación; no distribución final de votos de coalición.

| Campo | Esperado y observado |
|---|---:|
| PAN | 52037 |
| PRI | 8568 |
| PRD | 1603 |
| PVEM | 21754 |
| PT | 4583 |
| MC | 24575 |
| MORENA | 78928 |
| PAN_PRI_PRD | 1137 |
| PAN_PRI | 441 |
| PAN_PRD | 69 |
| PRI_PRD | 35 |
| PVEM_PT_MORENA | 2491 |
| PVEM_PT | 334 |
| PVEM_MORENA | 1239 |
| PT_MORENA | 470 |
| NUM_VOTOS_CAN_NREG | 125 |
| NUM_VOTOS_NULOS | 5727 |
| TOTAL_VOTOS | 204116 |

18/18 campos concordantes. El control numérico CAS→SEC y suma distrital SEC queda comprobado en el alcance consultado. No volver a restar 410: el efecto ya está incorporado en SEC. No trasladarlo al ayuntamiento A2024 ni a DF RP.

## Seguimiento oficial nuevo

El informe INE “Avance en el desarrollo e integración de resultados federales del Sistema de Consulta de la Estadística de las Elecciones Federales 2023-2024”, PDF de 56 páginas, incluye en su Anexo 1, página impresa 43 (índice PDF 43), fila 43: Guanajuato, distrito 10, Uriangato, Diputación MR, casilla 2797 C1, Anula, SM-JIN-80/2024. Describe modificación del cómputo sin cambio de ganador y la ubica en un concentrado de sentencias definitorias JIN/REC. Esta corroboración oficial posterior apoya el tratamiento aplicado por SICEE; no se interpreta como constancia individual de ausencia de reconsideraciones.

Fuente leída en el apartado pertinente:
https://repositoriodocumental.ine.mx/xmlui/bitstream/handle/123456789/178354/coe-3se-09-12-2024-p05.pdf

Sentencia de origen y vector de efectos:
https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JIN-0080-2024.pdf

Las búsquedas específicas SM-JIN-80/2024 + SUP-REC/reconsideración no localizaron un recurso vinculado de forma expresa. Esa falta de resultados no acredita inexistencia de recurso ni firmeza. La lista general del acuerdo INE/CG2129/2024 ya registrada en la auditoría federal tampoco establece, por sí sola, una correspondencia individual.

## Procedencia previa recuperada

Se leyeron dentro de AT-27-30-core(2).zip los informes HEYTI_Cotejo_Federal_2024_GTO_5_Series_v0_1.md, HEYTI_Cotejo_Dip_Federal_MR2024_CAS_SEC_11_Anuladas_v0_1.md y HEYTI_Cotejo_Dip_Federal_2024_Niveles_MR_RP_v0_1.md. Ya documentaban la exclusión de C1 en SEC y concordancia SEC→DIS. El cotejo local actual confirma el efecto numérico en staging, sin afirmar que DIS se haya cargado allí.

Hash ZIP MR documentado previamente: 9da21ef4e7ed7f490d3351c4834c4cea0bff050699d9d4ebf45f902e333cc61c. Las consultas actuales no recalcularon ese hash ni verificaron la unión por hash del snapshot; conservar esta limitación.

## Estado y pendientes

Estado documental propuesto: CONTROL_NUMERICO_STAGING_D10_CONCORDANTE; CORROBORACION_INE_CONCENTRADO_DEFINITORIO. No se persiste en DB ni se cambia la matriz original.

Pendientes: completar evidencia individual de cadena judicial/firmeza según contrato, verificar fecha de corte y procedencia del release por hashes, y aprobar política de selección antes de presentación. Los 27 pendientes judiciales municipales A2024 no disminuyen: esta revisión pertenece a otra serie.
