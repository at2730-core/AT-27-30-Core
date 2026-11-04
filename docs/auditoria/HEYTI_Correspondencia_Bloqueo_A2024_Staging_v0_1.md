# HEYTI — Correspondencia del bloqueo A2024 con staging

Fecha: 2026-10-03. Estado: propuesta documental; sin SQL ejecutado ni modificación de producción.

## Evidencia y procedencia

Fuente inmediata: copia adjunta `HEYTI_Registro_Municipal_A2024_46_v0_1(1).md`.
SHA-256 de esta copia: `b98968050574fb6af9d849d57bfee8aeadb87fcd9e5eb545d0625edcc9705c88`.
ZIP SICEE A2024 identificado por el registro: `13fe6a2ddb432922bddc9090f08eb0e558aeb3094ef1ba763b78d789b3d55e69`.

Las conclusiones judiciales de este documento proceden del expediente ya documentado en el registro. No se realizó una nueva búsqueda de resoluciones posteriores ni se volvieron a descargar sentencias en este bloque.

El registro consigna San Miguel de Allende: total municipal SICEE 75,386 frente a cómputo judicial localizado 76,757. Diferencia aritmética 1,371. Cuatro casillas restituidas conservan en SICEE la marca TRIBUNAL=ANULADA. Referencias del registro: SM-JDC-517/2024 y SUP-REC-22097/2024 con acumulados; el desechamiento del recurso no constituye una nueva revisión de fondo.

El registro conserva 27 municipios como JUDICIAL_NO_REVISADO; las concordancias focales de los restantes no certifican exhaustivamente sus vectores CAS/SEC.

## Correspondencia propuesta

| Capa | Estado observado o registrado | Tratamiento propuesto |
|---|---|---|
| Fuente original | Archivo SICEE con su hash y datos publicados | Inmutable; preservar votos y marcas judiciales crudas |
| Registro de lectura A2024 UNICA | BLOCKED_JUDICIAL_CUT_CONFLICT; selección UNDECIDED | Mantener bloqueo actual de presentación |
| source_release en base aislada | UNREVIEWED, fecha publicada ausente | No cambiar toda la fuente por un conflicto de alcance específico sin revisar qué series comparte |
| election_series A2024 UNICA | UNREVIEWED; SOURCE_AS_PUBLISHED | Asociar incidencia abierta a la serie exacta resuelta por hashes y miembros; no declarar SELECTED ni CERTIFIED |
| Municipio San Miguel de Allende | Conflicto municipal documentado | Incidencia raíz del expediente; conservar 75,386 y 76,757 como valores de procedencias distintas |
| Unidades SEC/CAS afectadas | Requieren identificación exacta contra filas staging | Incidencias vinculadas solo después de cotejar claves, pertenencia municipal, miembros y marcas; no distribuir 1,371 por estimación |
| Presentación RESULT | NO_RELEASE_SELECTED en pruebas | Mantener indisponibilidad; no sumar casillas restituidas automáticamente |
| Presentación NOMINAL_LIST | Evidencia favorable diferenciada | No habilitada por este documento; necesita política y soporte de bloqueo por métrica |

La incidencia propuesta debe expresar `JUDICIAL_CUT_CONFLICT`, estado abierto, referencia al expediente y a esta evidencia, identidad de la serie, valores comparados y alcance municipal. Los nombres concretos de columnas y estados permitidos deberán verificarse en el DDL realmente instalado antes de generar SQL. Este documento no inventa identificadores PostgreSQL.

## Límite actual del lector

Se inspeccionó la implementación local de:
`D:/GitHub/AT-27-30-core/src/heyti/capabilities/describe_section/versioned_electoral_source.py` y
`D:/GitHub/AT-27-30-core/src/heyti/capabilities/describe_section/staging_electoral_repository.py`
mediante sus copias de trabajo en este entorno. Los cambios posteriores en la computadora del usuario requieren cotejo antes de aplicar una propuesta.

El registro bloquea la serie por certificación BLOCKED antes de presentar. Además, el adaptador adjunta incidencias abiertas y el lector bloquea presentación si hay incidencias, sin distinguir su métrica. El adaptador consulta incidencias por fuente/serie/unidad; el contrato actual no ofrece alcance municipal independiente.

Por ello, una incidencia a nivel de serie bloquearía conservadoramente toda A2024, incluida NOMINAL_LIST. Las diferencias de verdad entre votos y LN deben documentarse ahora, pero permitir LN de forma independiente exige una modificación explícita del contrato y pruebas de que jamás autoriza RESULT. No usar un cambio de etiqueta para eludir el bloqueo.

## Evidencia nominal separada

El registro documenta 8,103 claves ordinarias B/C/E con LN SICEE igual a PRES/SEN/DIP_FED; las series federales pueden compartir catálogo. Esto respalda consistencia por clave, no tres mediciones independientes ni certificación de votos locales. Se excluyen 41 especiales y 24 anticipadas. Persisten 18 excepciones CCPC por residencia; no se convierten automáticamente en ubicación de casilla.

## Próximo bloque: inventario de solo lectura

Antes de producir una escritura se requiere obtener, desde la base aislada conservada:

1. DDL instalado de source_release, source_member, election_series, audit_run y reconciliation_issue, incluyendo claves, restricciones y estados admitidos.
2. Resolución única de fuente y serie A2024 por ZIP y hashes SEC/CAS de la matriz; comprobar otras series que compartan release_id.
3. Incidencias existentes de esa fuente/serie para evitar duplicarlas y conservar el historial de auditoría.
4. Filas crudas y proyectadas de las cuatro casillas restituidas, con claves exactas, unidad SEC vinculada y municipio; cotejar sus 1,371 votos con el expediente.

Con ese inventario se podrá preparar un ensayo transaccional en staging aislado, con verificaciones y ROLLBACK. El bloqueo vigente permanece durante todo el proceso. La fase siguiente no consiste en certificar A2024 ni sustituir el total municipal original.
