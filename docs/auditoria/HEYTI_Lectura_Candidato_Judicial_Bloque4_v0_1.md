# HEYTI — Bloque 4: candidato judicial de auditoría

Fecha: 2026-10-03. Estado: implementación de auditoría separada; sin selección ni certificación. Sólo 2024 A UNICA, municipio 3 San Miguel de Allende.

Se agrega un módulo de candidato derivado, manifiesto de transformación, diez pruebas unitarias y una prueba PostgreSQL de lectura. No se modifica el lector original, provider, runtime, materializador, matriz de selección ni DB. El instalador sólo agrega archivos; rechaza cualquier archivo existente distinto, verificando hashes antes de copiar.

El candidato se construye con 106 respuestas AUDIT completas, fuente exacta por hashes, cuatro filas CAS explícitas y el control de exclusión 156 C04. Valida 17 opciones por unidad, base municipal, deltas por CAS, vector derivado y aritmética en cada unidad. Conserva snapshot original, NULL nominal, marcas ANULADA, incidencias, identidad especial y genealogía; expone el derivado por separado. El hash de contenido liga manifiesto, originales y producto. La fecha de generación no sustituye la fecha de publicación de la fuente.

La identidad derivada requiere coincidencia explícita para consultar. Otra serie, unidad fuera del municipio o identidad equivocada no devuelve datos. PRESENTATION devuelve NO_RELEASE_SELECTED tanto para RESULT como NOMINAL_LIST, incluso si se pasa policy_id. No tiene mecanismo para certificar o seleccionar y no está conectado al flujo DescribeSection. La lectura del candidato admite sólo AUDIT RESULT; la LN queda en el snapshot original, no como nueva derivación o permiso de presentación.

## Archivos y rutas Windows

- `D:/GitHub/AT-27-30-core/src/heyti/capabilities/describe_section/judicial_derived_audit_source.py`
- `D:/GitHub/AT-27-30-core/tests/core/test_judicial_derived_audit_source.py`
- `D:/GitHub/AT-27-30-core/docs/auditoria/HEYTI_Manifiesto_Candidato_SanMiguel_A2024_v0_1.json`
- `D:/GitHub/AT-27-30-core/docs/auditoria/pruebas/HEYTI_Prueba_Candidato_Judicial_SanMiguel_A2024_v0_1.py`
- Este informe en `docs/auditoria/`.

## Validación

Diez pruebas unittest nuevas aprobadas localmente, con fixtures SEC sintéticas y el delta documentado. Los fixtures no representan el vector oficial de cada sección. Se probaron hashes, ambigüedad, falta de celdas/unidades, NULL de votos, valores inconsistentes, exclusión, conservación de originales y no selección. Las 50 pruebas unittest específicas de bloques anteriores también se ejecutan como regresión. La suite pytest completa no se ejecutó en este entorno, que no tiene pytest instalado; se indica ejecución local en Windows.

La prueba PostgreSQL pendiente usa psycopg2 ya disponible, solicita contraseña sin almacenarla y lee únicamente `heyti_cas_full_probe_d12d6718adb8`. Exporta una instantánea REPEATABLE READ READ ONLY e importa esa misma instantánea en todas las conexiones del adaptador, evitando mezclar 106 momentos de lectura. No crea otra base ni hace escrituras. Cierra cada conexión y la exportadora en finally. No genera archivos de datos electorales ni JSON con contraseña.

## Alcance electoral

La cadena localizada SM-JDC-517/2024 (03/09/2024) y SUP-REC-22097/2024 y acumulados (03/10/2024, desechamiento sin fondo) respalda el expediente documentado. El candidato reproduce numéricamente 75,386 + 1,371 = 76,757. No declara rectificación del ZIP ni certificación judicial estatal. Persisten revisión de otros municipios, identidad personal de CAND_IND_2 y selección aprobada para presentación.

El manifiesto fija transformación e inputs; su hash es control de integridad, no firma de una autoridad. Las respuestas recibidas por el constructor se consideran provenientes del lector auditado; esto no es un canal de admisión de datos externos sin revisión.

## Pasos locales

1. Extraer ZIP y ejecutar Aplicar_Bloque4.ps1 apuntando al repositorio correcto.
2. Ejecutar pytest sobre el nuevo archivo de pruebas; después la suite completa como cierre de integración.
3. Con PYTHONPATH apuntando al src del repositorio, ejecutar el archivo Python de prueba PostgreSQL con su ruta completa.
4. Revisar los cuatro deltas y total municipal, bloqueos RESULT/NOMINAL_LIST y cierre del snapshot. No seleccionar ni certificar a partir del OK técnico.

## Corrección v0.2 — identidad especial observada

La primera ejecución real pasó 471 pruebas y 65 subtests, pero el candidato rechazó UNIT_KIND. La unidad especial observada es SPECIAL_SECTION_ROW con clave SEC0:["", "9", "3", "SAN MIGUEL DE ALLENDE"], sección literal 0 y municipio 3. Se incorpora esa identidad exacta al manifiesto y a la validación, sin convertirla en SPECIAL_AGGREGATE ni SECTION ordinaria. Se actualiza el hash fijado por la prueba PostgreSQL. Se agrega una prueba de conservación de clave, tipo, identidad original y FK ordinaria ausente; identidades distintas son rechazadas. La prueba PostgreSQL completa sigue pendiente de repetición.
