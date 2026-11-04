# HEYTI — Control agrupado DF2024 MR: distritos 10, 12, 14 y 15

Fecha: 2026-10-03. Evidencia staging: salidas compartidas por Alex, consultas READ ONLY con ROLLBACK en heyti_cas_full_probe_d12d6718adb8, series_id 5. No conexión directa del asistente a esa DB; sin escritura, selección ni certificación. Complementa HEYTI_Control_DF2024_MR_D10_Staging_y_Seguimiento_Judicial_v0_1.md.

## Resultado comprobado en staging

| Distrito | Filas SEC | Total concordante | Campos concordantes | CAS anuladas | Votos excluidos |
|---:|---:|---:|---:|---:|---:|
| 10 | 293 | 204116 | 18/18 | 1 | 410 |
| 12 | 222 | 199413 | 18/18 | 5 | 1600 |
| 14 | 291 | 167044 | 18/18 | 2 | 613 |
| 15 | 184 | 159546 | 18/18 | 3 | 1155 |

72/72 comparaciones de campo concordantes, todas con cero valores no numéricos. El conteo de filas es por distrito, no por columna ni total estatal. El cotejo agrupado CAS→SEC cubrió diez secciones: una fila SEC por sección, 11 CAS ANULADA, exclusión observada 3778 igual a la esperada y LN CAS = LN SEC en las diez. Conservar votos crudos y marcas; no restar nuevamente 3778.

## Vector esperado y observado (sin distribución de coaliciones)

| Campo | D10 | D12 | D14 | D15 |
|---|---:|---:|---:|---:|
| PAN | 52037 | 64687 | 52722 | 55385 |
| PRI | 8568 | 9593 | 13077 | 5713 |
| PRD | 1603 | 1482 | 1503 | 1261 |
| PVEM | 21754 | 7540 | 10306 | 5109 |
| PT | 4583 | 3273 | 3586 | 3250 |
| MC | 24575 | 19963 | 10529 | 12704 |
| MORENA | 78928 | 80197 | 63882 | 65918 |
| PAN_PRI_PRD | 1137 | 2025 | 1228 | 1372 |
| PAN_PRI | 441 | 699 | 588 | 531 |
| PAN_PRD | 69 | 89 | 79 | 59 |
| PRI_PRD | 35 | 47 | 32 | 30 |
| PVEM_PT_MORENA | 2491 | 4227 | 2180 | 2959 |
| PVEM_PT | 334 | 238 | 326 | 250 |
| PVEM_MORENA | 1239 | 1002 | 730 | 760 |
| PT_MORENA | 470 | 605 | 420 | 698 |
| NUM_VOTOS_CAN_NREG | 125 | 144 | 109 | 101 |
| NUM_VOTOS_NULOS | 5727 | 3602 | 5747 | 3446 |
| TOTAL_VOTOS | 204116 | 199413 | 167044 | 159546 |

## Control CAS→SEC por sección

| Distrito | Sección | CAS crudo | SEC | Exclusión | CAS anuladas | LN CAS y SEC |
|---:|---:|---:|---:|---:|---:|---:|
| 10 | 2797 | 810 | 400 | 410 | 1 | 1500 |
| 12 | 364 | 599 | 308 | 291 | 1 | 918 |
| 12 | 398 | 585 | 285 | 300 | 1 | 937 |
| 12 | 451 | 626 | 309 | 317 | 1 | 923 |
| 12 | 530 | 1151 | 789 | 362 | 1 | 2137 |
| 12 | 536 | 1668 | 1338 | 330 | 1 | 3621 |
| 14 | 71 | 613 | 307 | 306 | 1 | 1258 |
| 14 | 3276 | 606 | 299 | 307 | 1 | 1162 |
| 15 | 1058 | 808 | 403 | 405 | 1 | 1311 |
| 15 | 3258 | 1530 | 780 | 750 | 2 | 2836 |

El control agrupado verificó cantidad y total de CAS marcadas por sección, no volvió a cotejar todas sus claves individuales ni el vector CAS completo; sus claves proceden de la matriz previa de las 11 casillas. Los vectores de esta prueba son sumas SEC distritales.

## Documentación judicial y corroboración oficial

Cuadros de efectos consultados: SM-JIN-80/2024 (D10), SM-JIN-41/2024 (D12), SM-JIN-94/2024 (D14) y SM-JIN-56/2024 (D15). Los controles no usan los votos distribuidos después entre partidos coaligados. En SM-JIN-94, el encabezado de un cuadro menciona también 56 C1, pero sus renglones y resolutivos anulan 71 C1 y 3276 C1; no se añade una tercera CAS por ese encabezado.

- https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JIN-0080-2024.pdf
- https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JIN-0041-2024.pdf
- https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JIN-0094-2024-
- https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JIN-0056-2024.pdf

El informe INE “Avance en el desarrollo e integración de resultados federales del Sistema de Consulta de la Estadística de las Elecciones Federales 2023-2024”, Anexo 1, página impresa 43, filas 43–46, identifica las cuatro sentencias y las once claves, con efecto de anulación y modificación sin cambio de ganador. Las identifica en su concentrado de sentencias definitorias JIN/REC. Es corroboración administrativa posterior del tratamiento; no prueba individualmente inexistencia de reconsideraciones ni reemplaza la cadena exigida para certificación.
https://repositoriodocumental.ine.mx/xmlui/bitstream/handle/123456789/178354/coe-3se-09-12-2024-p05.pdf

Búsquedas específicas en fuentes del TEPJF de SM-JIN-41/94/56 de 2024 con SUP-REC no proporcionaron una correspondencia expresa con recursos posteriores. SUP-REC-893/2018 aparece como precedente citado en SM-JIN-94, no como revisión de esta sentencia de 2024. Las páginas de sesiones y listas generales no demuestran ausencia de recursos. D10 conserva la misma limitación documentada en su informe individual.

## Alcance de cierre

CONTROL_NUMERICO_STAGING_CONCORDANTE en los cuatro distritos; CORROBORACION_INE_CONCENTRADO_DEFINITORIO. Son etiquetas documentales propuestas, no estados escritos a la base.

Pendientes antes de selección/certificación: evidencia individual suficiente de cadena judicial, fecha/corte y vínculo por hashes del release, política aprobada. No se altera RP, A2024 ni LN; no se disminuyen los 27 pendientes judiciales municipales. No se afirma carga DIS: para D10 no se encontró el miembro de ruta esperada y para D12/14/15 este bloque suma SEC.

Siguiente trabajo: retomar controles administrativos A2024 incompletos de Purísima del Rincón y Santa Catarina; los cuatro controles federales numéricos no requieren repetirse salvo cambio de fuente o nueva evidencia.
