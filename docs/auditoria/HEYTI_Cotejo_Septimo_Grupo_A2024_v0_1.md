# HEYTI — Cotejo del séptimo grupo municipal A2024

Fecha: 24 de octubre de 2026. Versión 0.1. Estado: cotejo numérico documental completado en los campos indicados; auditoría y certificación final pendientes.

## Alcance y evidencia

Ayuntamientos de Guanajuato 2024: Tarimoro (39), Uriangato (41), Valle de Santiago (42), Victoria (43), Xichú (45) y Yuriria (46). Las ejecuciones fueron realizadas por Alex mediante psql en la base aislada `heyti_cas_full_probe_d12d6718adb8`; sus salidas se compartieron en la conversación. Todas terminaron en ROLLBACK, con consultas de solo lectura. No se modificó la base, no se seleccionó una release para producción ni se certificaron resultados.

Fuente CSV: release_id 10, miembros `GTO_PEL_2024/AYUNTAMIENTOS_csv/2024_SEE_AYUN_GTO_CAS.csv` y `GTO_PEL_2024/AYUNTAMIENTOS_csv/2024_SEE_AYUN_GTO_SEC.csv`. Las unidades SEC0 se revisaron en series_id 16.

## Inventario e integridad interna

| Municipio | CAS | SEC | Votos CAS=SEC | Lista nominal CAS=SEC | SEC0 |
|---|---:|---:|---:|---:|---:|
| Tarimoro | 62 | 34 | 18,214 | 32,362 | 0 |
| Uriangato | 87 | 27 | 29,731 | 54,305 | 1 |
| Valle de Santiago | 217 | 78 | 59,881 | 122,822 | 1 |
| Victoria | 30 | 15 | 10,712 | 16,528 | 0 |
| Xichú | 24 | 15 | 5,945 | 9,015 | 1 |
| Yuriria | 122 | 58 | 32,287 | 66,806 | 1 |
| Total de filas | 542 | 227 | | | 4 |

Inventario sin valores no numéricos en votos o lista nominal, sin filas marcadas ANULADA ni otras marcas. Cotejo interno por sección: 18 campos de votos y lista nominal. Se completaron 4,086 cotejos de votos y 227 de lista nominal, con cero coberturas inválidas, campos no numéricos y discordancias.

## Cotejo documental por casilla

| Municipio | Acta | Filas cotejadas | Campos por fila | Controles coincidentes |
|---|---|---:|---:|---:|
| Tarimoro | 013/2024, pp. 5–6 | 62 | 14 | 868 |
| Uriangato | 14/2024, pp. 5–9 | 87 | 13 | 1,131 |
| Valle de Santiago | 17/2024, pp. 5–9 | 217 | 14 | 3,038 |
| Victoria | 013/2024, p. 4 | 30 | 13 | 390 |
| Xichú | 015/2024, p. 3 | 24 | 9 | 216 |
| Yuriria | 16/6/2024, pp. 12–14 | 122 | 14 | 1,708 |
| Total | | 542 | | 7,351 |

Todas las salidas reportaron cero discordancias, cobertura inválida y valores no numéricos. De los 7,351 controles, 50 son coincidencias numéricas de cuatro filas especiales cuya equivalencia de identidad entre acta y CSV no está acreditada. Los otros 7,301 corresponden a las 538 casillas con sección distinta de cero.

Campos de los cotejos de 14 columnas: PAN, PRI, PRD, PVEM, PT, MC, MORENA, PAN_PRI_PRD, PAN_PRD, PAN_PRI, PRI_PRD, NUM_VOTOS_CAN_NREG, NUM_VOTOS_NULOS y TOTAL_VOTOS.

Uriangato: mismos campos excepto PT. Victoria: mismos campos excepto MC. Xichú: PAN, PRI, PRD, PVEM, PT, MORENA, NUM_VOTOS_CAN_NREG, NUM_VOTOS_NULOS y TOTAL_VOTOS. Las columnas ausentes no se convirtieron en cero ni se declararon documentalmente verificadas. Lista nominal, votos válidos y candidaturas independientes no están incluidos en estos controles documentales por casilla.

Identidades con extensión se cotejaron mediante SECCION, TIPO_CASILLA, ID_CASILLA y EXT_CONTIGUA, incluidas Victoria 2899 E01C01 y las extraordinarias con extensiones de Valle de Santiago.

## Fuentes documentales oficiales inspeccionadas

- Tarimoro: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmtr-acta-013.pdf
- Uriangato: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmur-acta-14.pdf
- Valle de Santiago: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmvs-acta-17.pdf
- Victoria: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmvt-acta-13.pdf
- Xichú: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmxi-acta-15.pdf
- Yuriria: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmyu-acta-16.pdf

Los controles se transcribieron visualmente de las tablas de resultados de los documentos. La coincidencia acta–CSV no sustituye la revisión de resoluciones posteriores ni garantiza independencia entre ambas fuentes.

## Cuatro identidades especiales pendientes

| Municipio | Rótulo del acta | Identidad CSV | Línea CAS | DL | LN | Total | Vector no cero |
|---|---|---|---:|---:|---:|---:|---|
| Uriangato | 9043 A01 | SEC0 / VA41, A, id 41, ext 0 | 7605 | 20 | 1 | 1 | PVEM 1 |
| Valle de Santiago | 9044 A01 | SEC0 / VA42, A, id 42, ext 0 | 7692 | 20 | 5 | 5 | PAN 1, PRI 1, MORENA 3 |
| Xichú | 9045 A01 | SEC0 / VA43, A, id 43, ext 0 | 8024 | 2 | 2 | 2 | PVEM 1, MORENA 1 |
| Yuriria | 9046 A01 | SEC0 / VA44, A, id 44, ext 0 | 8048 | 20 | 3 | 3 | PVEM 1, MORENA 1, nulos 1 |

Se preservan como SPECIAL_SECTION_ROW, section_code 0, territorial_section_id NULL. No se vinculan automáticamente con secciones territoriales 9043–9046. Sus pares SEC tienen las mismas LN y votos: líneas 2071, 2098, 300 y 2176 respectivamente. ID_DISTRITO_FEDERAL es NULL en la identidad original de las unidades.

Huellas SHA-256 de las líneas crudas CAS especiales:

- Uriangato: `1649aa9a0b0f750d4b96945a0aa1bb26986dbcf588135e5667334c93dbe1a525`.
- Valle de Santiago: `e48ca48c15a06f2f88217206017185c81389735b0a7e7e0013d598789656474f`.
- Xichú: `eca736cd9fe99ab4da7fbab566a0983c990d7f138b12840c9e436132096d1481`.
- Yuriria: `7bc68f9a8b3ed0981d04b59f9373db8880c3f77b39955aa7dbe217d9ed7f1637`.

RUTA_ACTA, OBSERVACIONES y TRIBUNAL vacíos en estas cuatro filas. ESTATUS_ACTA: Uriangato y Xichú, Acta Levantada en Consejo; Yuriria, Grupo de Recuento; Valle de Santiago, literal `Acta de  Casilla`.

## Observaciones preservadas

Tarimoro: el acta contiene notas sobre 2745 C02 y 2777 C02, relativas a boletas y documentación de recuento. No se infirieron ajustes ni anulaciones de esas notas. Los 868 controles coinciden; queda pendiente evaluar el alcance documental de las notas en el expediente de cierre.

Valle de Santiago: los renglones 2855 C02 y 2856 B01 presentan el mismo vector en el acta y en el CSV. Se cotejaron con identidades distintas y ambos coincidieron. Esa coincidencia no acredita por sí misma un duplicado indebido ni justifica eliminar una fila.

## Pendientes para el cierre de auditoría

1. Acreditar mediante documento oficial la correspondencia de las cuatro identidades especiales; conservar rótulos originales y ausencia de vínculo territorial mientras tanto.
2. Completar el rastreo y evaluación de resoluciones, rectificaciones y acuerdos posteriores aplicables al cómputo municipal de cada municipio. Este reporte no acredita que no existan.
3. Cubrir o documentar explícitamente las columnas no incluidas en cada tabla y los campos fuera del cotejo documental realizado.
4. Incorporar esta evidencia al registro municipal y al registro único de pendientes, sin marcar como certificados los municipios por el solo resultado de estos controles.
5. Conservar evidencia reproducible de las consultas y salidas locales. Este reporte resume las ejecuciones compartidas; no constituye una ejecución independiente de la base del usuario.

## Resultado

Cotejo numérico documental del séptimo grupo completado en el alcance descrito, sin diferencias observadas. Persisten las limitaciones e identidades pendientes anteriores. No autoriza migración productiva, selección de release ni certificación final.
