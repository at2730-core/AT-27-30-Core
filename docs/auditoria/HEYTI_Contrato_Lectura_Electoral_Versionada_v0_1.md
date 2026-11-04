# HEYTI — Contrato de lectura electoral versionada v0.1

**27 de septiembre de 2026. Estado: diseño para revisión, sin despliegue.** El ensayo aislado PostgreSQL de 23 series SEC/CAS pasó; la matriz `HEYTI_Matriz_Seleccion_Cortes_23_Series_v0_1.csv` deja la selección para presentación en `UNDECIDED` y la fecha de corte SICEE en `UNVERIFIED`. No se consulta `at2730_core` ni se publica información nueva.

## Identidad de consulta

La petición debe especificar `year`, `type` (`A/DF/DL/G/P/S`), `modality` (`MR/RP/UNICA`), `unit_kind`, identidad histórica de la unidad y **política de selección de release**. Una consulta sin modalidad para DF/DL/S o sin release seleccionado no elige automáticamente una fila por año o sección. `SECCION=0` requiere identidad adicional de distrito/municipio/tipo de acta; no entra en el mapa de secciones ordinarias.

El resultado incluye dos niveles inconfundibles:

| Nivel | Campos obligatorios |
|---|---|
| Procedencia | `release_id`, autoridad, nombre de ZIP, SHA-256, miembro SEC, hash CSV, `cut_label`, fecha de corte o `null` con estado `UNVERIFIED`, miembro CAS cuando aplique. |
| Identidad | Año, elección, modalidad, `unit_key`, `unit_kind`, sección literal, distrito/municipio originales, `territorial_status`, posible FK territorial vigente nullable. |
| Resultado SEC | `total_votes` nullable, `total_raw`, `nominal_list` nullable, `nominal_raw`, estados y causas separadas; `options[]` con columna literal, ordinal, tipo, votos nullable y literal original. |
| Evidencia CAS | Casillas vinculadas por `member_id + source_line`, identidad de acta literal, `ESTATUS_ACTA`, `TRIBUNAL`, `JUICIO`, `OBSERVACIONES`, `RUTA_ACTA` y votos crudos por opción. Ruta de acta ≠ archivo PDF verificado. |
| Selección y confianza | `selection_status`, `certification_status`, incidencias abiertas, cobertura y motivo de indisponibilidad para UI. Estos campos son distintos de `tribunal` y del estado de una celda. |

**Ausencia y cero:** `NULL`/literal vacío se mantienen distintos de `0`; una anulación conserva el acta CAS cruda y el SEC publicado, sin sumarlos de nuevo. `NUM_VOTOS_VALIDOS` es agregado auxiliar, no una opción adicional para volver a sumar al total. Los votos de combinación permanecen en su columna literal hasta que una regla de candidatura acreditada permita atribuirlos.

## Selección de corte y visualización

1. El registro íntegro de cada release es consultable para auditoría con su estado. `PASSED_ISOLATED` demuestra carga reproducible, **no** certificación oficial de corte ni permiso de publicación.
2. Una política versionada seleccionará, por `(year,type,modality,unit_kind)`, una fuente y un corte después de documentar fecha, jurisdicción, resoluciones y alcance. Puede excluir unidades con incidencia sin borrar el release. Si falta política o hay empate de versiones, devolver `NO_RELEASE_SELECTED` y no inferir la versión más reciente.
3. La proyección de candidatura requiere mapeo completo de partidos, combinaciones e independientes por elección y reglas oficiales. Si es insuficiente, `winner` y `margin` son `null` con causa; no se calcula sobre cuatro siglas ni se desempata por orden de columnas.
4. La compatibilidad V1 puede entregar los cuatro partidos como **subconjunto explícito** y con metadatos fuera del objeto plano que esperan los módulos. Ningún consumidor debe convertir `NULL` en `0`. Mantener bloqueada la maestra `24G_*` copiada y sus indicadores dependientes.
5. La entrega a HEYTI-CORE debe atravesar DB→Capability→Runtime→Materialización→UI con pruebas doradas de identidad y cifras. Casos mínimos: DF21 MR/RP sección 218, A21 163/2541, DL21 MR/RP 1080, G24 1, P24 1150, sección histórica, SEC0, cero legítimo y empate.

## Pendientes para seleccionar release

- Obtener fecha, versión y alcance documentado del corte de los ZIP SICEE. Para A/DL/G locales 2024, preservar el corte IEEG del 9 de junio y resolver formalmente su relación con el estado posterior SICEE; en A/DL 2021 conservar el antecedente IEEG cuando exista.
- Completar expedientes de 1,160 comparaciones con una casilla vacía; 79 rutas de acta y 94 sin ruta figuran entre 173 casillas de serie. La coincidencia de la suma de números conocidos con SEC no transforma el vacío en cero.
- Resolver correspondencia de candidaturas/combinaciones y cuatro columnas independientes locales 2018 ambiguas; no inventar titular ni ganador.
- Contrastar imágenes de actas y sentencias disponibles; mantener siete residuos de agregados 2018 y diferencias de lista nominal entre cortes como incidencias.

**Puerta de aplicación:** inspeccionar el checkout actual y las reglas de gobernanza; implementar una vista/API con política versionada y pruebas de rechazo de versiones no seleccionadas. Ensayar contra una copia aislada antes de proponer migración aditiva a `at2730_core`. Ningún cambio de UI ni dato vivo está autorizado por este documento.
