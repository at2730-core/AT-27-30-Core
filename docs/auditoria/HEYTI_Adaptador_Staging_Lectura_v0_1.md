# HEYTI — Adaptador de lectura de staging SEC/CAS v0.1

Fecha: 2026-09-30. Estado: código preparado y probado con dobles DB-API; SQL pendiente de ensayo PostgreSQL real. No desplegado.

## Resultado

Se implementó StagingElectoralRepository como adaptador del lector versionado. Consume el DDL SEC v0.1 y CAS v0.2 del ZIP del core. Recibe una fábrica de conexiones dedicada; no incluye credenciales, no conecta por su cuenta, no modifica pyproject.toml y no instala controladores.

El componente abre una transacción REPEATABLE READ READ ONLY, consulta únicamente electoral_stage y finaliza con rollback/cierre incluso ante errores. Todos los valores de consulta se pasan como parámetros DB-API, nunca mediante interpolación en SQL. El factory debe devolver una conexión nueva e inactiva con filas de tipo tupla; el adaptador es dueño de su cierre. Un controlador compatible como psycopg deberá configurarse fuera de este bloque; no se probó ningún controlador real aquí.

## Correspondencia de identidad y cortes

El release del lector utiliza una clave de auditoría; el staging usa IDs numéricos. La consulta resuelve exactamente un release/serie mediante hash ZIP, rutas y hashes SEC/CAS, año, elección, modalidad, geografía GTO, nivel SECTION y judicial_cut SOURCE_AS_PUBLISHED. Cero o varias correspondencias fallan explícitamente.

No se supone que cut_label de la matriz y de la base tengan el mismo literal. StagingCutBinding exige clave de auditoría, literal exacto del corte en la base y referencia de evidencia de correspondencia. Esta referencia la suministra un proceso de confianza: el adaptador no verifica por sí mismo su autenticidad. No se generaron correspondencias reales ni se inventó fecha del corte. Un binding técnico no aprueba selección electoral para presentación.

La respuesta conserva la procedencia de la matriz y, por separado, los IDs, corte y estados existentes en staging. No se sustituyen certificación o selección del staging por éxito de carga.

## Contenido consultado

- Unidad histórica y claves opacas exactas del staging; ORDINARY_SECTION/SEC:n y unidades especiales se consultan sin normalización territorial automática.
- Totales, lista nominal, valores crudos, estados y causas de ausencia.
- Todas las columnas originales de opciones, en orden, incluyendo combinaciones, independientes y agregados auxiliares. No se suman ni atribuyen a candidaturas.
- Fila SEC original, miembro, línea y hash de fila.
- CAS asociadas a la unidad, con filas crudas, identidad original, valores, opciones, ESTATUS_ACTA, TRIBUNAL, JUICIO, OBSERVACIONES y RUTA_ACTA. La ruta no acredita que el PDF haya sido verificado.
- Incidencias no RESOLVED de todos los audit_run del release cuyo alcance incluya la unidad/serie. No se elige automáticamente la corrida más reciente. Estados de resolución distintos se tratan conservadoramente como pendientes.
- Conteos de opciones esperadas/celdas cargadas y CAS. La ausencia de celdas SEC añade incidencia; estos conteos no certifican completitud CAS ni resolución judicial.

Un bloqueo o rechazo de release registrado en staging se conserva como incidencia y bloquea PRESENTATION en el lector. La consulta AUDIT mantiene visibles los datos y pendientes. El lector continúa sin ganador/margen y conserva las 23 selecciones pendientes de la matriz.

## Verificación

36 pruebas aprobadas: 23 del primer bloque y 13 nuevas del adaptador. Estas últimas comprueban parámetros, transacción solicitada de solo lectura, ausencia/ambigüedad de releases y unidades, cierre ante fallos, NULL, actas anuladas, bloqueo de staging y rechazo de cobertura incompleta. Los resultados DB-API son sintéticos y están identificados como tales.

Se intentó descubrir pruebas electorales existentes; dos módulos no pudieron importarse porque pytest no está instalado. La ejecución final se limitó explícitamente a los dos módulos nuevos y pasó. No se afirma que la suite completa del core pasó.

No hay psql, servidor PostgreSQL ni controlador psycopg disponibles en este entorno. El SQL se revisó estáticamente contra el DDL aportado; no se probó su sintaxis/ejecución en PostgreSQL, restricciones reales de permisos, planes de consulta ni una conexión real. No se ejecutó SQL contra la base viva o una copia. El resultado todavía no es validación fuente→DB ni end-to-end.

## Archivos Python y rutas completas

- `D:\GitHub\AT-27-30-core\src\heyti\capabilities\describe_section\staging_electoral_repository.py`
- `D:\GitHub\AT-27-30-core\src\heyti\capabilities\describe_section\versioned_electoral_source.py`
- `D:\GitHub\AT-27-30-core\tests\core\test_staging_electoral_repository.py`
- `D:\GitHub\AT-27-30-core\tests\core\test_versioned_electoral_source.py`

El ZIP Bloque2 incluye ambos componentes y sus pruebas, las notas de ambos bloques, la matriz original sin cambios y un manifiesto con SHA-256. Es un paquete acumulativo de archivos nuevos; no sustituye el repositorio completo. Se comprobó que ningún archivo extraído del ZIP original fue modificado.

Para repetir las pruebas de contrato en una copia de trabajo Windows:

```powershell
Set-Location 'D:\GitHub\AT-27-30-core'
$heytiPreviousPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = 'src;tests/core'
    python -m unittest test_versioned_electoral_source test_staging_electoral_repository -v
    if ($LASTEXITCODE -ne 0) { throw 'Fallaron las pruebas de contrato electoral' }
} finally {
    $env:PYTHONPATH = $heytiPreviousPythonPath
}
```

## Ensayo PostgreSQL que sigue pendiente

1. Identificar o reconstruir una copia aislada con el staging SEC+CAS probado; el ensayo histórico documentado fue temporal y no acredita una base actualmente disponible.
2. Verificar tablas/columnas contra DDL v0.1+v0.2 y hashes/miembros de las fuentes. Registrar correspondencias de cut_label, sin dar por verificada una fecha desconocida.
3. Configurar una conexión dedicada de solo lectura y comprobar las dos consultas con las claves exactas existentes. Debe fallar ante corte/hash/modalidad incorrectos y mantener errores de DB visibles.
4. Cotejar resultados reales, por lo menos A21 163/2541, DL21 MR/RP 1080, DF21 MR/RP 218, P24 1150, una unidad histórica y una SEC0. Los nuevos ejemplos sintéticos no sustituyen esos casos dorados.
5. Ejecutar la suite completa y después integrar contrato de petición con DescribeSection, Runtime, Materialización y UI. No activar presentación sin selección acreditada ni retirar la cuarentena del legado G2024.

Las cifras del distrito 13 de 2018 y el conflicto judicial municipal de A2024 pertenecen a niveles agregados DIS/MUN que este adaptador SEC/CAS no representa: deberán conservarse como fuentes/incidencias de su nivel, sin atribuir al adaptador una rectificación que no ejecuta.
