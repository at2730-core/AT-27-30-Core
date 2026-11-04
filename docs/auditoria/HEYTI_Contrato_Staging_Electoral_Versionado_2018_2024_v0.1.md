# HEYTI — Contrato propuesto de staging electoral versionado v0.1

**Fecha:** 26 de septiembre de 2026. **Estado:** diseño para revisión; no es migración ejecutada. **Alcance:** Guanajuato, procesos 2018, 2021 y 2024; los datos 2015 se conservan fuera de esta integración. No modifica fuentes, repositorio Windows ni PostgreSQL. No publica resultados.

## 1. Evidencia y problema que resuelve

- Hay 23 conjuntos seccionales oficiales inventariados en 15 ZIP; originales, hashes, miembros ZIP y rutas CSV ya se comprobaron. Se deben conservar como entradas inmutables junto con su corte, modalidad y eventuales resoluciones judiciales.
- `D:\GitHub\AT-27-30-core\database\ddl\004_create_electoral_base.sql` declara `electoral.section_result` con llave `(section_id,election_id,party_id)` y solo cuatro partidos operativos. No puede almacenar simultáneamente MR/RP, versiones de corte, coaliciones, independientes, nulos o un resultado de una sección histórica ausente de `territorial.section`.
- `D:\GitHub\AT-27-30-core\database\etl\008_load_electoral_full.py` lee la maestra permisivamente, omite votos `NaN`, busca `section_id` vigente y salta las claves no encontradas; el `UPSERT` puede sustituir filas antiguas. Este ETL queda fuera de la ruta de carga candidata.
- DF 2021: cero filas en DB; `electoral/DF.json` coincide en seis campos con SICEE MR en 3,159 secciones, mientras RP difiere en 29 secciones de votos. Las 29 identidades históricas fuera del catálogo actual deben conservarse.
- 2018: 31 secciones oficiales ausentes de DB en seis elecciones. 2024: cinco ausentes en A/DF/DL/P/S; G 2024 tiene además 124 secciones nuevas sin filas, dos claves antiguas cargadas fuera del universo y valores copiados de 2018. P/DF/S 2024 reproducen exactamente la maestra en DB, aunque la maestra discrepa ampliamente de SICEE.
- El documento normativo `D:\GitHub\AT-27-30-core\docs\architecture\data\HEYTI_Data_Truth_Governance_v1.0.md` exige procedencia, estado de verdad y conservación histórica. En su fase de auditoría prohíbe poblar `territorial.section_history` por simple inferencia y no autoriza crear todavía `section_lineage`.

## 2. Frontera de operación

1. **Original inmutable:** ZIP exterior/interior y CSV/acta en almacenamiento de fuentes con SHA-256 y metadatos. No sobrescribir ni renombrar durante auditoría.
2. **Staging aditivo y aislado:** propuesta de esquema `electoral_stage`, sin FK obligatoria a `territorial.section` vigente y sin `UPDATE` a `electoral.section_result`.
3. **Proyección candidata:** reconstrucción de series por `(fuente, corte, año, elección, modalidad, sección o unidad especial)` con todas las opciones electorales. Estado `CANDIDATE` hasta conciliar.
4. **Publicación de consulta:** solo una selección explícita de versión y modalidad, con certificación y Golden Cases. La cuarentena G 2024 permanece mientras la cadena completa no esté validada.

## 3. Contrato físico propuesto, sujeto a revisión del checkout real

| Entidad propuesta | Llave e información mínima | Invariante |
|---|---|---|
| `source_release` | `release_id`; fuente lógica; nombre/ruta física; hash SHA-256; autoridad; fecha de publicación/corte y zona horaria; fecha de obtención; estado de certificación | Una versión no cambia de bytes; un corte IEEG y otro SICEE son releases diferentes. |
| `source_member` | `release_id`, ruta de ZIP interno/CSV, hash, codificación, delimitador, número de filas | Cada miembro leído es reproducible desde el ZIP preservado. |
| `election_series` | `release_id`, año, tipo A/DF/DL/G/P/S, ámbito, modalidad `MR`/`RP`/`UNICA` cuando la fuente así lo define, nivel acta/sección, regla judicial vigente | MR y RP nunca comparten llave ni se suman entre sí. `UNICA` no se infiere cuando hay modalidades. |
| `source_territorial_identity` | `series_id`, `section_code` canónico, periodo aplicable, municipio/distrito originales, `territorial_status`, FK vigente nullable, `genealogy_status` | Una clave histórica existe aunque la FK actual sea `NULL`; la relación con sucesoras queda `UNRESOLVED` sin evidencia. |
| `source_special_identity` | `series_id`, clase `VA`/`MEC`/`P`/municipal u otra etiqueta literal, distrito, municipio, identificador de acta original y ámbito | `SECCION=0` y claves 9000+ no se fuerzan a sección ordinaria ni se colapsan entre municipios/distritos. |
| `acta_evidence` | `series_id`, identidad original, distrito, casilla, `CLAVE_ACTA` u otra clave fuente, estado de cómputo/tribunal, localización de fila original, hash de archivo | La misma `CLAVE_CASILLA` no basta para deduplicar actas; preservar decisiones MR/RP y anulaciones. |
| `option_catalog` | `release_id`, columna literal, tipo `PARTY`/`COALITION_COMBINATION`/`INDEPENDENT`/`WRITE_IN`/`NULL_VOTE`/otra, candidatura solo si está acreditada | Los votos de combinación no se reparten por defecto entre partidos. Un nombre independiente ambiguo permanece sin asignación. |
| `section_tally` | `series_id`, identidad territorial o especial, total y LN nullable, estado/causal de cada dato, referencia a filas y actas | `NULL`, cero oficial, anulación, paquete no entregado y `NaN` legado no son equivalentes. Unicidad por release, serie y unidad de cómputo. |
| `option_vote` | `section_tally_id`, `option_id`, votos nullable, estado de verdad, evidencia de celda | Cada opción publicada se conserva, incluidas las no modeladas por los cuatro partidos. |
| `audit_run` y `reconciliation_issue` | hashes de entrada, versión de importador/reglas, inicio/fin, conteos, llave/valor discrepante, severidad, evidencia y estado | Repetir una carga idéntica no duplica observaciones; incidencias no se resuelven rellenando ceros. |

No hay una llave única general basada solo en `(año, elección, sección)`: perdería modalidad, corte y unidades especiales. En etapa de diseño se debe comprobar la unicidad real de cada serie oficial y formalizar restricciones e índices en un DDL revisado, sin deducir genealogía geográfica de un código repetido.

## 4. Reglas de transformación y selección

- Ingestar **todas** las columnas electorales originales y conservar la etiqueta exacta; una vista de cuatro partidos es una proyección limitada, no el registro de verdad.
- Usar enteros exactos para votos, total y LN; guardar el texto original y el estado de celda para vacíos. `NaN` de la maestra legado no se carga como número ni se transforma en cero. Un `0` explícito de fuente se distingue como `OFFICIAL_ZERO`.
- Registrar por separado `truth_status`, `territorial_status` y `certification_status` de acuerdo con la gobernanza. Un resultado anulable puede tener antecedente de acta y total vigente `NULL` con causal; preservar ambos cortes.
- `A 2021` secciones 163/2541: total oficial vacío por actas anuladas, LN y antecedente preservados. `DL RP 2021` sección 1080: total `NULL` por paquete no entregado; `DL MR` sección 1080: cero publicado. `DF MR/RP 2021` sección 218: 614/918 votos por estado judicial de C1; nunca sobrescribir una modalidad con la otra.
- Las 24 filas A 2024 `SECCION=0` se identifican por municipio y procedencia; las actas G 2024 VA 9001–9021 y MEC 9042 se guardan en unidad especial, no en `territorial.section`.
- La política de *versión elegida para presentación* se documenta por elección y modalidad y se prueba. Un corte posterior no invalida ni borra uno anterior. No escoger MR/RP por menor número de discrepancias con la maestra.
- La maestra legado permanece evidencia `LEGACY_SOURCE` con procedencia pendiente en `24DF_*`, `24S_*` y `24P_*`. El candidato oficial se construye desde originales; no se crea mediante `UPSERT` del legado.

## 5. Secuencia de implementación y puertas

| Fase | Trabajo | Salida comprobable y puerta |
|---|---|---|
| A. Congelar | Inventario 15 ZIP/23 conjuntos, hashes, corte, codificación, filas, claves y modalidad | 15/15 integridad ZIP y 23/23 rutas; manifiesto firmado por versión. |
| B. Diseño | Revisar checkout/DDL reales, contrato de identidad histórica, llave de opción y estados de celda; preparar DDL migratorio reversible | DDL y migración **revisados**, sin escribir aún en DB; no poblar `section_history` ni inventar `section_lineage`. |
| C. Ensayo aislado | Importador determinista a staging de prueba, sin tocar tablas legado | 23 series seccionales presentes; conteos, unicidad, integridad aritmética y tres totales oficialmente vacíos con causal. |
| D. Conciliación | Cotejar por sección/acta/opción, fuente→staging y staging→proyección; registrar diferencias | DF 2021 MR 3,159/3,159 en seis campos; RP separado; 31/29/5 identidades históricas preservadas; G 2024 3,233 ordinarias, actas especiales aparte. |
| E. Integración | Respaldo, transacción y migración aditiva controlada en HEYTI-CORE | DB legado intacta, FK histórica nullable, rollback probado; 23/23 cargas reproducibles con hashes y run_id. |
| F. Entrega | Capability→Runtime→Materialización→UI y casos dorados | `NULL`/0, empate, alianzas, sección histórica, DF21-218, DL21-1080, A21-163/2541, P24-1150 y G24-1; cuarentena G hasta pasar toda la cadena. |

**Criterio de bloqueo:** no publicar ni ampliar visibilidad; no habilitar cifras G 2024 copiadas ni proyecciones 2027 dependientes. La DB actual y el ZIP del repositorio son evidencia de auditoría, no el destino de una corrección inmediata. Las cuatro columnas independientes ambiguas de 2018 y otras causas no acreditadas se conservan literalmente con incidencia abierta; no se inventa adjudicación.

## 6. Decisiones abiertas para la revisión técnica

1. Identificador estable de unidad histórica y vigencia territorial: comprobar catálogos oficiales de geografía; no asignar secciones predecesoras a sucesoras por suposición.
2. Semántica exacta de actas especiales, `SECCION=0` por elección y distrito/municipio, y metadatos judiciales de cada corte.
3. Catálogo de partidos, combinaciones y candidaturas por elección: mantener columna literal y relación acreditada, sin cálculo de ganador sobre solo cuatro partidos.
4. Linaje de `24DF_*`, `24S_*`, `24P_*` de la maestra: localizar generador, bitácora o archivo de entrada si existe. La igualdad DB↔maestra no identifica su origen.
5. Disponibilidad de `D:\GitHub\AT-27-30-core\datasets\spatial\secciones.geojson` (3,266 geometrías) para probar la ruta HTTP/UI real; no sustituir geometría de demostración para certificarla.

**Rutas del código revisado:** `D:\GitHub\AT-27-30-core\database\etl\008_load_electoral_full.py` y `D:\GitHub\AT-27-30-core\src\heyti\audit\data_truth\section_truth.py`. Esta propuesta se basa en el ZIP aportado; verificar el checkout local de Alex antes de transformar el contrato en DDL o ETL.
