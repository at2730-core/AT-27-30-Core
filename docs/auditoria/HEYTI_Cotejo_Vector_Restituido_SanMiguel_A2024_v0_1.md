# HEYTI — Vector restituido San Miguel de Allende A2024

Fecha de cotejo: 2026-10-03. Estado: cotejo focal aprobado; sin selección ni escritura en base viva.

Fuente staging: salida del usuario, serie 16, CAS 122857/122901/122956/122973; cuatro casillas y 68 celdas. Fuente judicial: sentencia SM-JDC-517/2024 y acumulados, 03/09/2024, apartado III Efectos, tabla de votación agregada y cómputo modificado:
https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JDC-0517-2024-

La lectura oficial confirma las cuatro restituciones 156 C1, 172 B, 191 B y 200 E1. La tabla por casilla coincide numéricamente con los vectores staging. En la extracción HTML los encabezados gráficos de la primera tabla no son texto; el cuadro siguiente de cómputo modificado sí identifica los partidos y la candidatura independiente. Se corroboró con ese cuadro el agregado por rubro; no se adjudicó aquí el nombre personal asociado a CAND_IND_2.

| Rubro staging | 156 C01 | 172 B | 191 B | 200 E01 | Agregado | Agregado judicial |
|---|---:|---:|---:|---:|---:|---:|
| PAN | 70 | 87 | 70 | 73 | 300 | 300 |
| PRI | 124 | 179 | 104 | 86 | 493 | 493 |
| PRD | 6 | 3 | 2 | 4 | 15 | 15 |
| PVEM | 4 | 2 | 5 | 6 | 17 | 17 |
| PT | 3 | 0 | 8 | 1 | 12 | 12 |
| MC | 11 | 6 | 3 | 5 | 25 | 25 |
| MORENA | 116 | 156 | 67 | 83 | 422 | 422 |
| CAND_IND_2 | 10 | 11 | 2 | 4 | 27 | 27 |
| No registrados | 0 | 1 | 0 | 0 | 1 | 1 |
| Nulos | 17 | 8 | 23 | 11 | 59 | 59 |
| TOTAL | 361 | 453 | 284 | 273 | 1,371 | 1,371 |

Las cuatro columnas de combinaciones PAN_PRI_PRD/PAN_PRI/PAN_PRD/PRI_PRD y CAND_IND_1/CAND_IND_3 son cero en las cuatro filas staging. La sentencia publica un vector condensado; no se presenta la omisión de una columna como acreditación explícita de su cero judicial.

Controles: válidos por casilla 344/444/261/262; suman 1,311. No registrados 1; nulos 59; total 1,371. NUM_VOTOS_VALIDOS es control auxiliar y no se suma nuevamente a los partidos, independientes y combinaciones. CAND_IND_2 aporta 27, igual al rubro judicial CANDIDATURA INDEPENDIENTE; la relación de identidad personal sigue pendiente de catálogo.

## Cómputo municipal identificado en la sentencia

| Rubro judicial | Base local | Agregado restituido | Modificado |
|---|---:|---:|---:|
| PAN | 15,196 | 300 | 15,496 |
| PRI | 25,520 | 493 | 26,013 |
| PRD | 663 | 15 | 678 |
| PVEM | 1,130 | 17 | 1,147 |
| PT | 1,052 | 12 | 1,064 |
| MC | 1,725 | 25 | 1,750 |
| MORENA | 25,031 | 422 | 25,453 |
| Independiente | 1,884 | 27 | 1,911 |
| No registrados | 20 | 1 | 21 |
| Nulos | 3,165 | 59 | 3,224 |
| TOTAL | 75,386 | 1,371 | 76,757 |

El cotejo resuelve la incertidumbre focal sobre la composición numérica de los 1,371 votos. No acredita todavía que el vector municipal completo de SEC staging sea el mismo que la base local anterior de la sentencia; ese contraste se completó en el ensayo posterior documentado abajo.

156 C04 permanece fuera del grupo restituido. No se modifica su marca por asociación territorial. La fecha 03/09/2024 es la de esta sentencia; no sustituye published_at del ZIP SICEE ni acredita por sí sola la ausencia de resoluciones posteriores.

Pendientes antes de habilitar: revisar cadena judicial y alcance vigente, cotejar vector municipal base contra staging y fuente MUN, verificar proyección SEC de las restituciones, definir manifiesto de corte derivado y adaptar resolución del lector. Mantener bloqueo de A2024 y selección UNDECIDED. No se certifican los otros 45 municipios.


## Actualización: validación SEC y cadena judicial (2026-10-03)

El usuario ejecutó el agregado SEC de municipio 3: 106 unidades (105 ordinarias, una especial), 106 totales cargados, cero totales NULL; 17 columnas con 106 celdas cargadas y cero NULL cada una. Los partidos y rubros auxiliares coinciden con la base local de la sentencia; CAND_IND_2 suma 1,884 y las demás columnas independientes y combinaciones suman cero. Queda acreditada la coincidencia numérica del vector completo, conservando pendiente el vínculo personal de la candidatura.

El ensayo de derivación temporal pasó en PostgreSQL: 106 unidades, 1,802 celdas y cuatro secciones con delta. SEC156 1,515+361=1,876; SEC172 1,964+453=2,417; SEC191 296+284=580; SEC200 1,301+273=1,574. El agregado municipal es 76,757 y cumple controles aritméticos por sección. Válidos 73,512, no registrados 21, nulos 3,224. Terminó con ROLLBACK y temporales_eliminadas=t. No se creó un corte persistente.

Corrección técnica del SQL: se sustituyó BEGIN TRANSACTION READ ONLY por BEGIN porque PostgreSQL rechazó CREATE TEMP TABLE en la primera ejecución. La versión corregida fue ejecutada satisfactoriamente por el usuario. Conserva ausencia de escrituras en tablas persistentes y ROLLBACK final; no debe describirse como transacción de solo lectura.

La revisión oficial posterior leyó íntegramente SUP-REC-22097/2024, sentencia de 03/10/2024:
https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-22097-2024

Sus resolutivos acumulan SUP-REC-22098/2024 y SUP-REC-22312/2024 y desechan las demandas por no cumplir el requisito especial de procedencia. No dictan una sustitución del vector municipal de SM-JDC-517/2024. Conclusión de auditoría: en la cadena judicial identificada no se localiza modificación posterior del vector regional. Este alcance no equivale a demostrar, sólo por ausencia en búsqueda, que nunca existió otro expediente o acto de cumplimiento.

## Contrato propuesto del candidato derivado

Identificador descriptivo propuesto: A2024_SMA_SM_JDC_517_2024_DERIVED_v0_1. Estado: candidato judicial reproducido, sin certificación ni selección. El identificador no es un nombre de corte ya instalado.

- Serie: 2024/A/UNICA; alcance municipal ID3 y sus 106 unidades, incluida su identidad especial original. No extender al resto de municipios.
- Insumos: ZIP y miembros SEC/CAS originales con hashes; referencias judiciales, fechas y capturas/tablas de efectos; cuatro filas CAS con hash e identidad literal.
- Regla: vector SEC original más vector de restituciones exactamente enumeradas. Delta cero para las otras 102 unidades. No modificar marcas judiciales originales; registrar el efecto como metadato de derivación separado.
- Exclusiones: 156 C04; totales auxiliares excluidos de suma de votos para evitar duplicación; ninguna transformación de LN, genealogía o identidad especial.
- Producto: vector por unidad y opción, valores base/delta/derivado, manifiesto de transformación y hash propio. El derivado no se presenta como ZIP rectificado por IEEG/INE.
- Tiempo: distinguir fecha de sentencia regional 03/09/2024, resolución superior 03/10/2024 y fecha de generación del producto. No llenar published_at de la fuente original con estas fechas.
- Selección: decisión explícita por alcance y métrica, separada de identidad física y éxito técnico. La evidencia de este expediente no selecciona automáticamente A2024 estatal.
- Lector: requiere soporte explícito para resolver corte derivado y relacionarlo con sus insumos. El adaptador vigente sólo resuelve SOURCE_AS_PUBLISHED; no cambiar la etiqueta ni flexibilizar validaciones para admitirlo por accidente.

Pruebas requeridas para integrar el contrato: identidad/hash del producto; exclusión de 156 C04; invariancia de las 102 unidades sin delta; equivalencia del vector municipal; historial base/derivado visible en auditoría; rechazo de otra serie/corte/alcance; presentación bloqueada sin política; separación RESULT/NOMINAL_LIST; no selección automática de otros municipios. No se implementó todavía este contrato ni se habilitó publicación.
