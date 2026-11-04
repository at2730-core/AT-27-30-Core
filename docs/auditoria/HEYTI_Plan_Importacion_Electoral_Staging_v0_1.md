# HEYTI — Plan de importación electoral a staging v0.1

**Estado:** propuesta de implementación para revisión; no se ejecutó el DDL ni se cargó PostgreSQL. **Ámbito:** Guanajuato, 2018/2021/2024; 2015 excluido. Acompaña `HEYTI_Staging_Electoral_v0_1_PROPUESTA_NO_EJECUTAR.sql` y el contrato de staging v0.1.

## Evidencia de estructura

El ZIP de HEYTI-CORE contiene `D:\GitHub\AT-27-30-core\database\ddl\004_create_electoral_base.sql`, que define `electoral.section_result` único por sección, elección y partido, y `D:\GitHub\AT-27-30-core\database\ddl\001_create_territorial_base.sql`, con `territorial.section` único por clave actual. El staging propuesto es aditivo y solo usa una FK territorial nullable. La inspección de cuatro cabeceras oficiales muestra que DF MR/RP 2021, P 2024 y A 2024 incluyen columnas de partidos, combinaciones, nulos, no registrados, total y LN; no son cuatro columnas de partido.

## Orden de trabajo

1. **Revisar el checkout real.** Comparar los dos DDL anteriores y `D:\GitHub\AT-27-30-core\database\etl\008_load_electoral_full.py` con el ZIP auditado; revisar permisos de esquema, políticas de migración y respaldo. La ruta ETL legado no se reutiliza para carga oficial.
2. **Manifiesto inmutable.** Una entrada por cada uno de los 15 ZIP; incluir hash SHA-256, autoridad, corte, nombre físico y ruta; una entrada por miembro CSV seccional con hash, codificación, delimitador, cabecera y conteo. Declarar las 23 series con año, elección, modalidad y corte mediante mapeo explícito. Rechazar rutas no inventariadas, cabeceras nuevas y discrepancia de bytes; preservar el ZIP original. Los CSV federales contienen otros estados: filtrar explícitamente `ID_ESTADO` numérico 11 para la proyección Guanajuato, conservar el archivo nacional y registrar ambos conteos.
3. **Ensayo de DDL en base desechable.** Revisar el SQL línea por línea y aplicarlo únicamente a una copia de prueba del esquema vigente. Verificar creación/rollback, restricciones, claves compuestas y que `electoral.section_result` y `territorial.section` no cambien. `CREATE TABLE IF NOT EXISTS` no certifica estructura previa: en cada entorno comparar definición resultante contra el contrato.
4. **Importador determinista.** Leer miembros sin editar los originales; insertar `source_release`→`source_member`→`election_series`→`raw_row` para filas de Guanajuato, con texto y hash de cada registro y ordinal original del CSV nacional; después clasificar unidad territorial/especial, catálogo literal de opciones, total/LN y votos. Una repetición con el mismo manifiesto debe ser idempotente y producir los mismos hashes y conteos, sin `UPSERT` de resultados electorales.
5. **Validación semántica.** Separar sección ordinaria de `SECCION=0`, VA y MEC según tipo/ámbito. El cotejo preliminar detecta 137 filas SEC=0 en 13 series: DF21 contiene 15 `P` por distrito en cada modalidad; G/P/S 2018 y 2024 contienen agregados extranjeros, y locales 2024 contienen registros `VA` por municipio/distrito. Conservar etiquetas fuente hasta corroborar su definición; no suponer equivalencias entre secciones históricas. Conservar MR/RP y decisiones judiciales de actas por separado. `NULL`, cero oficial, `NaN` legado, anulación y paquete no entregado llevan causa y estado distintos. Las combinaciones de coalición e independientes quedan como columnas literales mientras no haya mapeo acreditado.
6. **Conciliación.** Comprobar conteos de miembros y series (15 ZIP/23 conjuntos); duplicados, rangos enteros, totales publicados vs opciones cuando la regla del archivo lo permite, LN y causal de vacíos. Comparar fuente→staging por registro/opción y staging→proyección por sección, con incidentes persistentes y sin rellenar ceros. Casos: DF21 3,159 MR, sección 218 MR/RP; DL21 1080; A21 163/2541; P24 1150; G24 1 y 3,233 ordinarias; ausencias históricas 31/29/5. Los 23 conjuntos no se deben tratar como una sola modalidad.
7. **Integración posterior.** Solo tras conciliar y certificar una política de corte/modalidad por elección, preparar adaptador de lectura; comprobar fuente→DB→Capability→Runtime→Materialización→UI con casos dorados. Mantener G 2024 y escenarios derivados en cuarentena hasta superar esa cadena.

## Condiciones para aceptar el importador

- Los 15 originales y los 23 conjuntos están identificados por hash; ninguna serie se carga en modalidad implícita cuando existen MR/RP.
- Cada fila/celda proyectada tiene procedencia de archivo y registro; sus opciones incluyen nulos y combinaciones, sin reparto inferido.
- Los vacíos oficiales y claves históricas se preservan; la FK a catálogo vigente puede ser `NULL`; no se inventa genealogía.
- Una segunda ejecución idéntica no duplica datos ni modifica tablas legado; incidentes abiertos se reportan y bloquean publicación.
- El adaptador V1 evita convertir `NULL` en cero o etiquetar ganador con solo cuatro partidos.

## Revisiones pendientes antes de ejecutar el SQL

El DDL v0.1 es un **borrador técnico**, no una migración aprobada. Aún hay que fijar las claves de unidad especial por archivo, validar tipos de estado contra gobernanza y fechas/cortes oficiales, revisar el manifiesto generado y ensayar una base desechable. Las FK compuestas de `section_tally` y `acta_evidence` impiden cruzar miembro y serie en esos registros, pero falta diseñar la cardinalidad de múltiples actas por sección. La cláusula de unicidad `source_release(outer_zip_sha256, cut_label)` presupone que cada corte se registra una sola vez; revisar esa política antes de aplicar.
