# HEYTI — Integración DescribeSection electoral versionada, Bloque 3 v0.1

Fecha: 2026-10-03. Estado: implementado en copia aislada; pendiente de aplicar y verificar en el checkout Windows.

## Resultado y alcance

Se incorpora un payload opcional electoral_query a DescribeSection. Exige año entero, tipo y modalidad explícitos; admite release_id, policy_id y metric_scope RESULT/NOMINAL_LIST. DescribeSection solo admite PRESENTATION para una sección ordinaria positiva. AUDIT, SEC0 y actas especiales siguen en el lector de auditoría separado. No se configura automáticamente una conexión ni una política.

Ejemplo sin selección (debe devolver NO_RELEASE_SELECTED si Data Truth permite publicación y el lector está inyectado):

```json
{"section_id":"1080","electoral_query":{"year":2021,"type":"DL","modality":"RP"}}
```

El proveedor recibe versioned_electoral_source como dependencia explícita. Primero comprueba identidad y permiso Data Truth. Si no existe permiso, no consulta la fuente. Si falta el lector, entrega VERSIONED_SOURCE_NOT_CONFIGURED. No reemplaza una consulta versionada fallida con resultados legados. Las solicitudes sin electoral_query conservan el flujo electoral legado existente: este paquete no constituye una migración completa de ese flujo ni elimina su configuración de cuarentena.

Se añade SectionDescription.electoral_versioned, separado del objeto electoral legado. El materializador conserva el sobre entero en role electoral_versioned: bloque metadata sin datos cuando está bloqueado, bloque domain si el lector devuelve selección y certificación explícitas. La autorización de NOMINAL_LIST preserva su alcance y no incluye votos. El estado de los campos y la procedencia no se convierten en certificación por éxito técnico.

No se cambia la versión HEYTI_RESPONSE 1.0; el rol añadido es una extensión opcional que todavía debe probarse con los validadores de entrega y consumidores reales. No se conecta el runtime de producción ni se modifica UI/DB. El bloque no sustituye la reconciliación end-to-end acordada.

## Archivos y rutas completas

Modificados:
- D:\GitHub\AT-27-30-core\src\heyti\capabilities\describe_section\models.py
- D:\GitHub\AT-27-30-core\src\heyti\capabilities\describe_section\provider.py
- D:\GitHub\AT-27-30-core\src\heyti\capabilities\describe_section\implementation.py
- D:\GitHub\AT-27-30-core\src\heyti\materialization\describe_section\materializer.py

Nuevos:
- D:\GitHub\AT-27-30-core\src\heyti\capabilities\describe_section\electoral_query.py
- D:\GitHub\AT-27-30-core\tests\core\test_describe_section_versioned_electoral.py

## Verificación

50 pruebas unittest aprobadas aquí: 36 de Bloques 1/2 y 14 nuevas. Las nuevas cubren preservación del flujo legado, ausencia de fallback, identidad ordinaria, rechazo de AUDIT/SEC0, Data Truth, falta de fuente, selección sintética, alcance de LN, copia defensiva y materialización de estados bloqueados/seleccionados.

Los ejemplos seleccionados son sintéticos. Ninguna selección electoral real fue certificada. No hay pytest disponible aquí; la suite completa posterior a Bloque 3 debe ejecutarse en Windows. Antes de este bloque, Alex reportó 447 passed, 41 subtests passed y nueve casos distintos reales del adaptador PostgreSQL, en heyti_cas_full_probe_d12d6718adb8. Es evidencia reportada por el usuario, no una ejecución remota del asistente. El bloqueo inicial por contraseña se resolvió y la verificación CAS completa reportó éxito.

## Aplicación controlada

Extraer el ZIP a una carpeta temporal fuera del repositorio. Ejecutar Aplicar_Bloque3.ps1 desde esa carpeta. El instalador primero valida todos los archivos de entrada, dependencias y bases esperadas, tolerando solo conversión CRLF/LF; si algún archivo difiere, aborta antes de escribir. Hace respaldo local de los destinos existentes, aplica cuatro modificaciones/dos adiciones y copia esta nota a docs/auditoria. No ejecuta SQL ni hace commit. Si la suite falla después de aplicar, conservar el error y el respaldo para revisión; no conectar producción.

Después ejecutar en el entorno habitual del core:

```powershell
Set-Location 'D:\GitHub\AT-27-30-core'
python -m pytest -q
if ($LASTEXITCODE -ne 0) { throw 'Falló la suite posterior al Bloque 3' }
```

El alcance de verificación siguiente es validar entrega/runtime con este rol opcional y hacer una prueba real DB→Capability→Materialización sobre la base aislada, manteniendo NO_RELEASE_SELECTED. Se requieren cortes seleccionados y casos UI acreditados antes de consumir resultados como definitivos.
