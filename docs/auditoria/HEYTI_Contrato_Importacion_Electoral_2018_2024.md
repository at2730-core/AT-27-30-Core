# HEYTI — Contrato de importación electoral 2018–2024

**Estado:** propuesta auditada contra las fuentes aportadas; pendiente de contraste con el esquema y los contratos vigentes de HEYTI-CORE. **Alcance:** Guanajuato, elecciones 2018, 2021 y 2024. Los datos de 2015 se conservan sin incorporarlos a esta migración.

## Identidad y procedencia

Cada resultado conserva una clave lógica formada por `año + elección + modalidad + unidad territorial histórica/tipo de acta + fuente/corte`. `MR`, `RP` y elección sin modalidad aplicable no comparten identidad. Las actas especiales usan identificador y tipo de acta; una clave `9001–9046` del IEEG no se interpreta automáticamente como sección geográfica del INE. Municipio/distrito y geometría se relacionan con su versión territorial; no se reescriben retrospectivamente.

Por carga registrar ZIP original, ruta CSV interna, SHA-256, organismo, fecha del corte, fecha de ingesta y transformación. Los cortes IEEG 9 junio 2024 y SICEE posterior se preservan en registros versionados. La vista de resultado vigente elige un corte mediante una regla documentada y no borra el anterior.

## Datos por resultado

| Campo lógico | Regla |
| --- | --- |
| `option_id`, `option_kind`, `raw_column`, `votes` | Una fila por **columna original**: partido, combinación de coalición, candidatura independiente y otras opciones oficiales. Conservar nombre de columna, cifra cruda y vacío. No repartir votos de combinación entre partidos durante ingesta. |
| `total_votes`, `registered_non_votes`, `null_votes`, `nominal_list` | Conservar las magnitudes originales y su procedencia; `total_votes` puede ser `NULL`. Cero numérico no sustituye vacío. |
| `result_status` y `reason` | Distinguir publicado, anulado, paquete no entregado, sin dato, en revisión y demás estados documentados por acta. No derivar causa solo de una desigualdad aritmética. |
| `candidate_id` y atribución | Vínculo posterior y versionado a candidatura/coalición según elección y regla oficial. Permitir nombre no resuelto: cuatro columnas independientes locales de 2018 permanecen sin atribución personal por columna. |
| `source_version` | Identifica MR/RP, corte judicial y fuente. Un mismo valor numérico en dos versiones no autoriza fusionar sus registros. |

La identidad aritmética se valida donde el total es numérico: suma de opciones originales + no registrados + nulos = total. Se registran las discrepancias de agregados SICEE 2018 como incidencias de ese nivel; no se corrigen por imputación. Validar unicidad de clave, cobertura por elección/año/modalidad, secciones históricas, estados de ausencia y original intacto.

## Proyecciones de consumo

1. **Fuente fiel:** filas originales por opción y versión, consultables sin pérdida de columnas.
2. **Vista de candidatura:** agrega combinaciones con regla electoral verificable y versionada; ganador/margen solo cuando el resultado y la atribución sean suficientes. Cero o empate conserva su estado, sin desempate por orden de columnas.
3. **Compatibilidad V1:** `{meta,secciones}` con claves de sección numéricas sin ceros, años como cadena y filas planas de votos más `VOTOS/LN`; se genera explícitamente desde la fuente fiel. Metadatos de estado/procedencia van fuera de la fila plana hasta actualizar todos los consumidores. Su desglose de cuatro siglas debe indicarse como parcial.
4. **Entrega HEYTI:** DB → Capability → Runtime → Materialización → UI conserva identidad, corte, modalidad, estado y cobertura. Bloquear G 2024 de la maestra copiada y sus indicadores dependientes hasta reconstrucción y prueba completa.

## Casos semilla obligatorios

| Caso | Resultado esperado |
| --- | --- |
| G 2024 frente a G 2018 | Rechazo de copia `24G_*`; cuarentena previa activa hasta fuente reconstruida; ganador y proyección dependientes también controlados. |
| DL 2021, 328 secciones vacías de maestra | Recuperación MR desde SICEE/derivado; RP se carga aparte. |
| A 2021, secciones 163 y 2541 | Total `NULL` con causal de anulación; antecedente previo separado; sin ganador. |
| DL 2021, sección 1080 | MR total 0, RP total `NULL` con paquete no entregado. |
| Secciones 1, 51, 999 y 1000 | Identidad y lectura estable con y sin ceros iniciales en todos los módulos. |
| A 2018, sección 51; A 2024, sección 2399 | Opción ajena a cuatro siglas preservada; no declarar ganador de candidatura sin regla de coalición. |
| A 2018, sección 28 | Empate entre columnas actuales no se resuelve por orden de campos. |
| P 2024, sección 754; A 2024, sección 354 | Alerta `VOTOS>LN` con cifras y cortes originales visibles; sin inferir causa. |
| Actas especiales IEEG 9001–9046 | Tipo de acta separado de sección geográfica; correspondencia con SICEE `SECCION=0` documentada. |

## Secuencia de aplicación

Inspeccionar el checkout de HEYTI-CORE y sus contratos actuales; crear staging reproducible e inmutable; cargar fuente fiel; validar los 23 conjuntos y casos semilla; construir vistas de candidatura y compatibilidad; ejecutar reconciliación fuente→DB→Capability→Runtime→Materialización y Golden Cases de interfaz; registrar cambios por módulo. No sustituir manualmente el maestro ni retirar la cuarentena G 2024 antes de superar sus pruebas.

**Pendientes abiertos:** evidencia nominal de cuatro columnas independientes locales 2018, causas de siete residuos adicionales en agregados 2018, causal precisa de cambios de LN, alcance de actas especiales y origen del vaciado de `21DL_*`. Se conservan cifra y estado original aunque el pendiente permanezca abierto.
