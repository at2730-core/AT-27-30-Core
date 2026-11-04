# HEYTI — Primer bloque de lectura electoral versionada v0.1

Fecha: 2026-09-30. Estado: implementación aislada, sin despliegue.

## Entrega

Se añade un componente separado del proveedor existente: catálogo de releases construido desde la matriz de 23 series, decisiones de selección con alcance exacto por política/serie/unidad/métrica y lectura con propósitos AUDIT y PRESENTATION. No se conecta al proveedor DescribeSection ni a PostgreSQL, Runtime, Materialización o UI en este bloque.

La carga del catálogo no verifica físicamente los archivos fuente: valida el formato de hashes y conserva los hashes declarados. Los IDs generados son claves de auditoría deterministas año/tipo/modalidad/hash ZIP/hash SEC; no son IDs de PostgreSQL. El adaptador futuro deberá resolver esa correspondencia explícitamente.

El repositorio de snapshots es una interfaz. En las pruebas se utiliza un doble en memoria con cifras sintéticas identificadas; no se carga ni certifica un resultado electoral nuevo. Las decisiones de selección son entradas de confianza del componente: sus referencias documentales se exigen, pero la autenticidad de la certificación debe verificarse fuera del lector antes de suministrarlas. No hay decisiones reales aprobadas ni un almacén persistente de políticas en este bloque.

## Comportamiento verificado

- Sin política o selección única respaldada: NO_RELEASE_SELECTED, sin consulta al repositorio.
- Una fuente explícita en AUDIT es inspeccionable aun con bloqueo, manteniendo estado y procedencia.
- PRESENTATION rechaza conflicto judicial, fecha de corte no verificada e incidencias de unidad abiertas.
- MR/RP, identidad histórica y hashes deben coincidir con el snapshot. No se selecciona automáticamente el release más reciente.
- Se conservan valores literales, NULL con causa, cero, opciones originales y actas CAS crudas anuladas. No se calculan ganador, margen, participación ni reparto de coaliciones.
- Una selección NOMINAL_LIST no permite presentar votos ni evidencia CAS de votos.
- La matriz real conserva las 23 selecciones UNDECIDED y los cortes UNVERIFIED.

El bloqueo judicial de una serie se aplica conservadoramente a toda ella. No se implementan excepciones por municipio ni filtrado fino de incidencias por métrica; una excepción futura deberá tener contrato y evidencia específicos. Una consulta RESULT puede preservar magnitudes incompletas con sus estados y NULL, pero nunca produce ganador.

## Archivos nuevos y rutas en Windows

- `D:\GitHub\AT-27-30-core\src\heyti\capabilities\describe_section\versioned_electoral_source.py`
- `D:\GitHub\AT-27-30-core\tests\core\test_versioned_electoral_source.py`
- `D:\GitHub\AT-27-30-core\docs\auditoria\HEYTI_Implementacion_Lectura_Versionada_v0_1.md`

El ZIP de entrega contiene estos archivos, un manifiesto de hashes y una copia sin cambios de `docs/auditoria/HEYTI_Matriz_Seleccion_Cortes_23_Series_v0_1.csv`, necesaria para la prueba del catálogo. No es un repositorio completo ni reemplaza el ZIP original. Revisar en una copia de trabajo antes de incorporarlo al checkout actual.

## Verificación ejecutada

23 pruebas unittest aprobadas en la copia aislada del core, incluyendo la matriz real y casos sintéticos de rechazo/preservación. No se ejecutó la suite completa del core: pytest no está instalado en este entorno. Tampoco se ejecutaron pruebas de PostgreSQL ni los casos dorados electorales con todas sus fuentes reales. Este resultado es validación del componente, no certificación end-to-end.

Repetición en PowerShell, desde una copia que contenga los archivos:

```powershell
Set-Location 'D:\GitHub\AT-27-30-core'
$heytiPreviousPythonPath = $env:PYTHONPATH
try {
    $env:PYTHONPATH = 'src'
    python -m unittest discover -s tests/core -p test_versioned_electoral_source.py -v
    if ($LASTEXITCODE -ne 0) { throw 'Fallaron las pruebas de lectura versionada' }
} finally {
    $env:PYTHONPATH = $heytiPreviousPythonPath
}
```

## Continuación concreta

Implementar un adaptador de solo lectura al staging SEC/CAS que entregue el contrato literal de snapshot y resuelva los IDs de auditoría contra los IDs de staging; ejecutarlo sobre una copia aislada comprobada. Después integrar un contrato explícito de petición electoral al proveedor/capacidad, ejecutar la suite del core y comprobar la cadena DB→Capability→Runtime→Materialización→UI. La selección real de cortes y los pendientes de auditoría siguen abiertos.

Los HTML de módulos y el GeoJSON adjuntos quedan disponibles para la etapa posterior de migración; no se modifican en este bloque.
