# HEYTI — Revisión técnica del core y política de lectura propuesta v0.1

Fecha: 2026-09-30. Alcance: revisión documental y estática del ZIP AT-27-30-core(2), contrastada con la matriz de cierre v0.4. No se ejecutó SQL, no se modificó el repositorio ni la base viva. Este documento no certifica resultados electorales.

## Resultado

El ensayo aislado SEC+CAS ya está documentado como aprobado el 27 de septiembre. La tarea siguiente es implementar selección explícita de fuentes y lectura versionada; no repetir por rutina la carga ni importar resultados a las tablas legadas.

La matriz del repositorio contiene 23 identidades distintas año/tipo/modalidad, 15 nombres de ZIP fuente, 73,262 filas SEC y 179,779 filas CAS. Incluye 137 filas SEC con sección cero y 221 CAS con sección cero. Las 23 series tienen presentación UNDECIDED y fecha de corte UNVERIFIED. A2024 tiene certificación BLOCKED_JUDICIAL_CUT_CONFLICT; las restantes PENDING_SOURCE_ADJUDICATION. Estos estados deben conservarse al conectar la lectura.

La evidencia del ensayo es un reporte histórico del repositorio; no constituye una nueva ejecución ni acredita que esas tablas existan hoy en la base viva. El ZIP del core no demuestra por sí solo disponibilidad material de los 15 paquetes originales. Antes de reproducir la carga deberán localizarse y comprobarse contra sus hashes.

## Hallazgos y consecuencia para la implementación

| Componente | Hallazgo | Acción concreta |
|---|---|---|
| DDL legado 004_create_electoral_base.sql | election es única por año/tipo; section_result exige sección vigente y voto no nulo. No representa modalidades, fuentes ni cortes. | Mantenerlo como legado; usar staging versionado para la nueva lectura. |
| Contratos de importación, staging y lectura | Ya requieren identidad histórica, modalidades, opciones originales, procedencia y selección explícita. | Implementar sobre esos contratos; no inventar un modelo paralelo. |
| Staging CAS v0.2 | Vincula SEC y CAS del mismo release; conserva identidad original y votos nulos con causa. | Tomarlo como base técnica y conservar texto crudo/estado del campo. |
| Clave CAS de la proyección | CASROW identifica miembro y fila; protege las filas originales, pero no acredita equivalencia entre actas de distintas fuentes. | Mantener clave cruda y añadir equivalencias documentadas por separado. |
| Proyección de carga | INSERT de ensayo sobre base limpia; no demuestra política de reejecución productiva. | Definir transacción, rechazo de duplicados y comparación de hashes antes de desplegar. |
| Lector electoral actual | Consume maestra JSON, cuatro partidos y contiendas; no selecciona release/modalidad ni expone todas las opciones literales. | Añadir adaptador versionado con contrato separado de compatibilidad. |
| Nombre CertifiedElectoralSectionSource | El nombre y la docstring no prueban certificación de los datos cargados. | Mostrar certificación explícita proveniente de auditoría, nunca inferida del nombre de clase. |
| Liderazgo en el lector | Calcula liderazgo entre partidos rastreados. | Mantener esa etiqueta; ganador oficial exige universo y reglas completos. |

Archivo de lector revisado: `D:\GitHub\AT-27-30-core\src\heyti\capabilities\describe_section\electoral_result_source.py`.

## Política propuesta, lista para implementar

La solicitud debe identificar año, tipo, modalidad, unidad histórica y política/release. La respuesta debe incluir release y hashes, autoridad, miembro fuente, corte y estado de su fecha, opciones literales, métricas con nulos preservados, selección, certificación e incidencias aplicables.

| Situación | Comportamiento requerido |
|---|---|
| No existe selección explícita aprobada | NO_RELEASE_SELECTED; ninguna sustitución automática por el archivo más reciente. |
| Consulta de auditoría a un release identificado | Permitir inspección de lo publicado con procedencia y pendientes visibles; no convertirla en presentación certificada. |
| Conflicto judicial aplicable a la unidad | Bloquear presentación como resultado definitivo; conservar fuentes y evidencia del conflicto. |
| Casilla anulada | Conservar dato crudo y efecto en una derivación identificada; no borrar ni sumar indiscriminadamente. |
| Campo vacío | Mantener NULL, texto crudo y causa; no imputar cero. |
| Sección cero, especiales, VA o MEC | Conservar identidad especial; no forzar FK a sección ordinaria vigente. |
| MR y RP | Consultar series separadas. Toda equivalencia de actas requiere evidencia; no fusionar por parecido de clave. |
| Lista nominal especial o con discrepancia | Mostrar definición/procedencia y advertir incidencia en el dato; no calcular participación con denominador no adjudicado. |
| Opciones incompletas o coaliciones sin regla documentada | No calcular ganador oficial ni repartir combinaciones. |
| Legado G2024 copiado de G2018 | Mantener cuarentena; no usar como respaldo automático. |

La selección debe poder acotarse por unidad y métrica: corroborar lista nominal no certifica votos, y resolver un municipio no cierra toda A2024. Toda derivación debe registrar sus entradas, regla y evidencia, sin cambiar originales.

## Casos de aceptación antes de conectar producción

1. DL2018 MR, distrito 13: mostrar DIS MORENA 9,439/total 77,976 y detalle corroborado MORENA 19,439/total 87,976 como fuentes distintas. No rectificar el DIS ni declarar causa probada.
2. P2024: conservar el cotejo original de 2,449 discordantes entre 3,228 secciones presentes en DB. El acuerdo DB–maestra legado no valida la maestra frente a SICEE.
3. A2024 San Miguel de Allende: impedir presentación definitiva del corte SICEE 75,386 frente al antecedente judicial 76,757 mientras siga sin resolverse la selección. Mantener los 27 municipios con revisión judicial pendiente.
4. G2024 VA D22: conservar total/nulos IEEG 4/2 frente a SICEE 2/0; el acta A01 respalda el primer par, pero no prueba por sí sola equivalencia A01/VA01/VA31 ni corte posterior.
5. A2021 SEC 163/2541 y DL2021 RP SEC 1080: preservar vacíos y modalidad; distinguirlos de cero.
6. Especiales DL2021: conservar 31 SMR y 31 SRP con deduplicación exclusivamente en derivaciones respaldadas por identidad de acta/modalidad.
7. MEC: conservar ACTA_CASILLA-MEC y procedencia; no fusionar modalidades postal/internet ni trasladar lista nominal entre cortes.
8. Solicitud sin selección: devolver NO_RELEASE_SELECTED aunque exista una carga técnica aprobada.

## Orden de trabajo siguiente

Primero implementar el registro de selección y estados de incidencia, conservando las 23 selecciones UNDECIDED. Después añadir lectura explícita para auditoría de releases identificados y una lectura de presentación que aplique bloqueos por unidad/métrica. Verificar los casos anteriores en un entorno aislado con fuentes comprobadas. La conexión a la base viva queda supeditada a conocer su esquema y carga actuales y a disponer de la selección respaldada por evidencia.

## Evidencia revisada del repositorio

- docs/auditoria/HEYTI_Matriz_Seleccion_Cortes_23_Series_v0_1.csv
- docs/auditoria/HEYTI_Resultado_Ensayo_CAS_Completo_PostgreSQL_2026-09-27.md
- docs/auditoria/HEYTI_Resultado_Proyeccion_23_Series_PostgreSQL_2026-09-26.md
- docs/auditoria/HEYTI_Resultado_Cotejo_SEC_CAS_23_Series_2026-09-26.md
- Contratos de importación, staging y lectura electoral versionada 2018–2024.
- Propuesta staging CAS v0.2, proyección CAS v0.2 y DDL electoral legado.
- SQL y resultados originales del cotejo P2024 contra SICEE y contra la maestra legado.

Las cifras del ensayo, los estados de selección y los resultados históricos son evidencia documental. Los hallazgos sobre restricciones del DDL y del lector provienen de lectura estática. Las acciones y la política de este documento son propuestas, no cambios ya desplegados.
