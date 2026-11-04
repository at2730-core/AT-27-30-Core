# HEYTI — Distrito local 13 de 2018: ruta de cotejo externo

**Consulta:** 30/09/2026. **Estado:** diferencia comprobada dentro del paquete SICEE; pendiente cotejo de la fila con cómputo IEEG independiente. No se alteró el dato original ni la base viva.

## Clave y discrepancia

Elección de diputaciones locales 2018, **mayoría relativa, distrito 13 (Silao de la Victoria, Guanajuato)**, archivo `2018_SEE_DIP_LOC_MR_GTO_DIS.csv`. La fila DIS registra `MORENA=9,439`, `NUM_VOTOS_VALIDOS=74,623` y `TOTAL_VOTOS=77,976`. La suma de **128 SEC** registra respectivamente `19,439`, `84,623` y `87,976`; CAS suma también **87,976**. Los demás campos de opción comunes DIS/SEC coinciden. Los archivos agregados distintos `DISPP` y `DISCAND` registran **87,976** como total del mismo distrito; sus columnas repartidas por partido/candidatura no se sustituyen por la columna cruda MORENA de DIS. Evidencia y método detallados: `HEYTI_Cobertura_Agregados_2018_MUN_DIS_vs_SEC_v0_1.md`.

| Nivel / publicación SICEE | MORENA crudo directamente comparable | Votos válidos | Total |
|---|---:|---:|---:|
| DIS MR | 9,439 | 74,623 | 77,976 |
| Suma SEC MR | 19,439 | 84,623 | 87,976 |
| Suma CAS MR | Ver cotejo por opción SEC/CAS | Ver reporte de origen | 87,976 |
| DISPP / DISCAND | Definiciones distintas, sin equivalencia directa | No equiparar | 87,976 |

## Publicación externa identificada

El [portal oficial IEEG de resultados de cómputo distrital y municipal 2018](https://sistemas.ieeg.mx/computos-finales-2018/) enlaza “Cómputo Diputaciones” a [**Computo x casillas Diputaciones.xlsx**](https://sistemas.ieeg.mx/computos-finales-2018/assets/files/Computo%20x%20casillas%20Diputaciones.xlsx). El buscador indexa el enlace, pero no pudo abrir el contenido XLSX para leer el distrito 13. **No se ha cotejado ninguna celda de esa planilla** ni establecido su fecha de corte, hash, cobertura o tratamiento judicial; el mero enlace no adjudica el total.

### Próxima verificación reproducible

1. Obtener públicamente el XLSX del enlace IEEG y registrar URL, fecha de descarga, SHA-256, hojas y metadatos/corte. Si el portal permite seleccionar distrito 13, capturar sus cifras con fecha y modalidad.
2. Identificar distrito **local** XIII, elección de **diputaciones MR**, y la llave por casilla/sección. Comparar el mismo universo, evitando duplicar RP o mezclar coalición, candidatura y partido.
3. Sumar casillas del XLSX y comparar `MORENA`, válidos y total con DIS, SEC y CAS SICEE. Investigar ausencias, recuentos, anulaciones y publicaciones modificadas antes de declarar un valor para HEYTI.
4. Si no hay desglose público accesible o la documentación no explica la diferencia, dejar **DIS 77,976 / SEC-CAS 87,976** y **MORENA DIS 9,439 / SEC 19,439** como conflicto no adjudicado para el informe final de Alex. No enviar solicitudes durante la auditoría.

El patrón exacto de −10,000 en un campo es compatible con un error de transcripción o transformación, pero **no demuestra su causa ni autoriza corregir el CSV original**.
