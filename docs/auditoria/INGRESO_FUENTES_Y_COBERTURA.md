# HEYTI V2 — Ingreso municipal estimado ICMM 2024

## Fuente y unidad
INEGI, Ingreso Corriente para los Municipios de México (ICMM), año de ingreso2024. Publicación28septiembre2026. Se descargó el ZIP desde el enlace DataDownload del portal oficial; se conservó íntegro en referencias-oficiales/INEGI_ICMM. No se cambió la carpeta de fuentes de Alex.
Portal: https://www.inegi.org.mx/investigacion/icmm/
Datos: https://www.inegi.org.mx/contenidos/investigacion/icmm/datosabiertos/conjunto_de_datos_icmm_2024_csv.zip
Reporte: https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/icmm/ICMM2024_RR.pdf

La unidad es ingreso corriente promedio trimestral por hogar, en pesos de la fuente. No es ingreso per cápita ni salario personal. Los datos no se actualizan a2026 y no se comparan con2020/2022 en esta consulta. El reporte denomina las cifras precios constantes; se mantienen importes originales sin nueva deflactación.

## Cobertura y precisión
46municipios de Guanajuato y1referencia estatal. Cinco estadísticas por unidad: valor estimado, error estándar, límite inferior, límite superior y coeficiente de variación. Se preservan235filas CSV originales. Intervalos al90%, según página3del reporte. Precisión porCV: alta entre0y15%, moderada de15a menosde30%, baja desde30%. CV0se identifica por separado; no se confunde con faltante. No se recalculan intervalos.
Los colores aplican los rangos del cuadro2del reporte2024: menosde35000,35000a45000,45000a60000,60000a80000,80000o más (límites inferiores inclusivos). Son estratos sobre estimaciones puntuales; un cambio de color no acredita diferencia estadísticamente significativa.

## Geografía
Se reutiliza cartografía INEGI municipal del Censo2020 aportada por Alex, capa11mun,46polígonos y codificaciónISO88591. Se transforma aWGS84 sin simplificar, manteniendo vértices y geometrías completas. Correspondencia de límites2020con ingreso2024 pendiente de conciliar, expresamente indicada.
Para filtros se usa cruce de superficie positiva con secciones representadas porCORE en la cartografía de referencia; no se supone equivalencia de códigos municipales entre instituciones. Los municipios se muestran completos, pueden repetirse entre universos y los cruces de borde pueden ser pequeños. No se generan ingresos por sección ni distrito ni se prorratean valores. Las secciones bloqueadas no intervienen.
La referencia estatal11000se mantiene aparte de la tabla municipal y se toma directamente de la fuente. No se promedian ni suman los valores municipales para reproducirla.

## Integración
Nueva consulta Ingreso estimado · municipios2024, mapa base, límites seccionales opcionales, tabla de46municipios según filtro, intervalos/errores/CV/precisión/estrato y selección con acercamiento y ficha. Fuente separada heyti-ingreso-municipal-2024.json con estadísticas CSV originales, cartografía y hashes. Conservadas las cinco consultas previas y fuentes.
Respaldo previo en auditoria-socioeconomico/respaldo_pre_ingreso. Preparación reproducible en auditoria-socioeconomico/preparar_ingreso.py. Auditoría como usuario final de los tres módulos al terminar Socioeconómico.

## Validación final
169 pruebas aprobadas en35archivos. Compilación correcta con aviso de tamañoJSno bloqueante. Cotejo independiente235/235estadísticas conCSVoriginal exacto. JSON socioeconómico anterior sin cambio. No hubo comprobación interactiva ni móvil.
