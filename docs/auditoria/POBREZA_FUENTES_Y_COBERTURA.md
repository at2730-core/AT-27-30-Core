# HEYTI V2 — Pobreza: municipios e historial, localidades urbanas

## Fuentes
Se descargaron directamente del portal de CONEVAL y se preservaron íntegros en referencias-oficiales/CONEVAL_Pobreza_2020:
- Concentrado_indicadores_de_pobreza_2020.zip, con hoja Concentrado municipal y Concentrado estatal.
- Indicador_pobreza_localidad_2020.zip, hoja Guanajuato.

https://www.coneval.org.mx/Medicion/Paginas/Pobreza-municipio-2010-2020.aspx
https://www.coneval.org.mx/Medicion/Paginas/pobreza_localidad_urbana.aspx

Son datos históricos producidos por CONEVAL. No se presentan como medición nueva de2026. Se reemplaza la entrada pendiente Pobreza(proxy) por una consulta de indicadores oficiales publicados, sin construir un proxy con variables parciales.

## Cobertura municipal
46municipios, referencia estatal separada,16indicadores en2010/2015/2020. Se conservan porcentaje, personas y, en14indicadores donde se publica, carencias promedio. Los dos indicadores que no publican carencias promedio son vulnerables por ingreso y no pobre/no vulnerable. No se llenan esos campos con cero.
La población de referencia es la calibrada para la medición de pobreza, con propósito estadístico; puede diferir deCenso/CONAPO. Se conservan porcentajes publicados sin recalcularlos a partir de conteos redondeados. Categorías/carencias superpuestas: no sumar columnas. No se obtienen tasas distritales ni se reparten cantidades entre secciones.

## Cobertura por localidad
180localidades de Guanajuato. Rangos originales:2en[0,20),24en[20,40),80en[40,60),65en[60,80),9en[80,100]. Se conservan textos originales con extremos abiertos/cerrados, sin sustituir por puntos medios ni calcular cantidad de personas en pobreza multiplicando rangos por población.
La población totalITER2020 es contexto de la localidad; no es un conteo de pobreza ni la población calibrada de la estimación municipal. Áreas rurales fuera de esta estimación por localidad; la vista municipal incluye contexto municipal completo.

## Geometría y discrepancias
Cartografía INEGI Censo2020 aportada por Alex, capas11mun y11l, reproyectada aWGS84sin simplificar. Los46municipios y180localidades se enlazan por clave completa. No se imputaron polígonos.
En la primera revisión de ámbito Urbano se localizaron176polígonos. Los4restantes existen en11lcon ámbito Rural:110150034Capulín de Bustos,110201294La Barranca,110270133San José de Mendoza y110460044Parangarico. CONEVAL los incluye como localidades urbanas. Se conservaron los4polígonos originales, el rango publicado y la diferencia de clasificación, que queda visible en pantalla y pendiente de conciliar. Ninguna geometría de estas180localidades resultó inválida.
Cruce con secciones de referencia mediante superficie positiva. Se conservan unidades completas y puede haber repetición entre universos/cruces pequeños por bordes. Cartografía2020 no reconstruye límites históricos2010/2015. El enlace orienta consulta sin certificar equivalencia territorial. Secciones bloqueadas no participan.

## Presentación
Dos vistas: Localidades urbanas2020por rangos; Municipios con año/indicador seleccionables. Mapa base, overlay opcional de secciones, tabla íntegra, selección y detalle. Vista municipal con tabla de16indicadores, referencia estatal y ficha histórica de3años para el indicador seleccionado. La urbana conserva180filas y su rango/poblaciónITER, sin porcentaje puntual inventado. Colores municipales: bandas descriptivas fijas de20puntos porcentuales; no se presentan como clasificación oficial municipal. Fuente/códigosN-D/n.a. y límites visibles.

## Continuidad
Alex confirmó lista la consulta deIngresos y autorizó seguir. Auditoría como usuario final de los tres módulos reservada hasta terminar Socioeconómico. Después dePobreza quedan pendientes Índice urbano-rural yProyección2027. Respaldo de integración en auditoria-socioeconomico/respaldo_pre_pobreza. Preparación y verificación reproducibles en preparar_pobreza.py y verificar_pobreza.py.

## Verificación final
Cotejados exactamente6627valores municipales/estatales y180registros de localidades contraExceloriginal. Compilación correcta. Primera corrida:175pruebas aprobadas y1timeout5000ms en prueba previa deEducación. Repetición íntegra contestTimeout30000:176pruebas aprobadas en36archivos. No se modificaron aserciones ni configuración persistente. JSONsocioeconómico previo sin cambios. Sin comprobación visual interactiva/móvil en esta entrega.
