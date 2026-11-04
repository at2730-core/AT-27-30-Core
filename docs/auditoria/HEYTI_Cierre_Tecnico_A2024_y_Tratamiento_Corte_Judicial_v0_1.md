# HEYTI — Cierre técnico A2024 y tratamiento del corte judicial

Fecha: 2026-10-03. Alcance: mecanismo de incidencias y lectura en staging aislado. Estado electoral: abierto, sin selección de presentación.

## Evidencia ejecutada por el usuario

Base original del ensayo: `heyti_cas_full_probe_d12d6718adb8`. A2024 corresponde a `release_id=10`, `series_id=16`; el mismo release contiene DL MR 17, DL RP 18 y G 19. Estos identificadores son locales a esa base y no deben trasladarse a otra sin resolución por hashes.

El ensayo SQL validó cuatro filas y hashes, creó temporalmente una auditoría y una incidencia OPEN de JUDICIAL_CUT_CONFLICT vinculada sólo a la serie 16 y terminó con ROLLBACK. Conteos finales de ambos registros del ensayo: 0. No cambió votos ni certificaciones.

| Casilla | ID local | Línea CAS | Votos crudos | Marca SICEE |
|---|---:|---:|---:|---|
| 156 C01 | 122857 | 343 | 361 | ANULADA |
| 172 B | 122901 | 387 | 453 | ANULADA |
| 191 B | 122956 | 442 | 284 | ANULADA |
| 200 E01 | 122973 | 459 | 273 | ANULADA |
| Total | | | 1,371 | |

156 C04, ID local 122860, línea 346, 343 votos, también aparece ANULADA y queda fuera del conjunto restituido documentado. No inferir que toda marca ANULADA de estas secciones deba revertirse.

La prueba Python creó `heyti_a2024_reader_probe_03e26d4d6d74` como copia temporal, registró allí la incidencia y obtuvo:

| Serie | Conflictos DB JUDICIAL_CUT_CONFLICT | Auditoría | Presentación sin política |
|---|---:|---|---|
| A UNICA | 1 | OK | NO_RELEASE_SELECTED |
| DL MR | 0 | OK | NO_RELEASE_SELECTED |
| DL RP | 0 | OK | NO_RELEASE_SELECTED |
| G UNICA | 0 | OK | NO_RELEASE_SELECTED |

La copia fue eliminada y los conteos de auditorías/incidencias de la base original permanecieron iguales. Esto acredita visibilidad de la incidencia en el adaptador, acceso de auditoría y separación de ese conflicto por serie. No es una comparación integral de todas las tablas ni una prueba de presentación con política aprobada. La prueba de selección ausente bloquea antes de consultar datos; no debe atribuirse ese resultado a un filtro judicial por métrica.

## Tratamiento del corte propuesto

Conservar como versión original `SOURCE_AS_PUBLISHED`: archivo, hashes, votos, marcas, NULL, opciones y claves históricas inmutables. El total municipal original documentado es 75,386; el total judicial localizado en el expediente previo es 76,757, diferencia 1,371. Ambos totales proceden del registro municipal de auditoría; no son una nueva fila municipal importada en este ensayo.

El candidato para uso electoral es una versión derivada judicial separada, con procedencia explícita. No sobrescribir el ZIP ni declarar que éste fue rectificado por la autoridad. El nombre de corte, identidad derivada, hashes de entrada y del producto, reglas de cómputo y fecha deberán constar en un manifiesto propio. Esta propuesta no crea ni certifica esa versión.

Para construirla falta completar el expediente de transformación:

1. Conservar y cotejar los textos judiciales y tablas aplicables de SM-JDC-517/2024 y la cadena SUP-REC-22097/2024 y acumulados; registrar sus efectos, fechas y alcance, sin equiparar desechamiento con nueva confirmación de fondo.
2. Cotejar por cada una de las cuatro casillas el vector completo de opciones, no sólo TOTAL_VOTOS. Mantener identificaciones de candidatura/coalición separadas de columnas de partidos para evitar doble conteo.
3. Definir el tratamiento de anulaciones restantes, incluida 156 C04, a partir del expediente. No restituir por pertenecer a la misma sección.
4. Derivar los vectores SEC y municipal con controles de cobertura y suma. El total 76,757 debe resultar del vector acreditado; no basta sumarle 1,371 a un total ni ajustar un residuo.
5. Validar el contrato de cortes derivados: el adaptador actual resuelve judicial_cut=SOURCE_AS_PUBLISHED y no admite automáticamente una nueva vista judicial. Diseñar resolución explícita y pruebas antes de integrar esa versión.
6. Completar el alcance judicial de los otros municipios de A2024: el registro conserva 27 pendientes. Un expediente municipal no certifica la serie estatal entera.

## Lista nominal y bloqueo

La LN ordinaria dispone de corroboración previa por 8,103 claves con cómputos federales, sujeta a corte y procedencia. Ese resultado no autoriza votos municipales. Especiales y anticipadas conservan tratamiento separado.

El lector vigente aplica bloqueo de serie e incidencias abiertas sin discriminación de métrica. Por tanto, habilitar NOMINAL_LIST de forma independiente exige evolución explícita del contrato y pruebas que mantengan RESULT bloqueado. No levantar el bloqueo A2024 para aprovechar evidencia nominal.

## Decisión de este bloque

Mecanismo técnico validado; conflicto electoral pendiente; fuente original conservada. No quedó una incidencia persistente en la base original porque los ensayos fueron revertidos o eliminados. El registro de lectura mantiene el bloqueo ya existente. No hubo escritura en la base viva, selección, certificación ni presentación de votos autorizada.

Siguiente trabajo sustantivo: expediente del vector judicial de San Miguel, antes de producir código de derivación. No repetir las cargas ni la suite general por este cierre documental.

## Artefactos reproducibles

- `HEYTI_Ensayo_Incidencia_A2024_ROLLBACK_v0_1.sql` — SHA-256 `cf5948579740b676f069fe22e0727d1dc028a69b300129677f2c905193720395`.
- `HEYTI_Prueba_Adaptador_Incidencia_A2024_v0_1.py` — SHA-256 `73200525a53cade5a830d5e6b7d3f4153c465ed5cc79971f9a9c9dab3b5cf48d`.

Guardar este documento en `D:/GitHub/AT-27-30-core/docs/auditoria/`. Las salidas fueron proporcionadas por el usuario; este entorno no ejecutó los ensayos contra su PostgreSQL.
