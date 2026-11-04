# HEYTI V2 — Marginación urbana 2020

## Archivos y procedencia
Fuentes entregadas por Alex en D:/GitHub/Fuentes Socioeconomico: IMU_2020.zip y 11_guanajuato.zip. Copias intactas conservadas en referencias-oficiales/CONAPO_IMU_2020. Se extrajeron valores de la hoja IMU_2020 y se mantuvieron las 23 columnas originales. El diccionario usa POB_TOT/OSCEL para campos que la hoja de datos denomina POB_TOTAL/OVSCEL; la presentación identifica su significado explícitamente.
CONAPO: https://www.gob.mx/conapo/documentos/indices-de-marginacion-2020-284372
INEGI: https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=889463807469

## Resultado
- 2,214 registros de índice de Guanajuato, claves únicas.
- 3,714 geometrías de AGEB urbanas; 2,214 enlazadas por clave completa.
- 1,500 geometrías sin registro en esta base. Se conservan como N/D sin inferir causa.
- Ningún registro de índice sin geometría; ninguna AGEB sin cruce con secciones de la cartografía de referencia.
- Grados conservados: Muy bajo405, Bajo598, Medio694, Alto359, Muy alto158.

## Cartografía y cruce
La capa 11a usa MEXICO_ITRF_2008_LCC. Se transforma a coordenadas geográficas WGS84 para Leaflet, conservando todos los vértices, sin simplificación. Una geometría inválida se reparó exclusivamente para el cálculo de intersecciones; la geometría publicada de visualización se conserva transformada sin alteración topológica. Cruce por superficie de intersección estrictamente positiva en el sistema proyectado original, con secciones.geojson de la versión de referencia. No se unen por coincidencia de códigos de municipio entre instituciones.
El estado muestra todas las AGEB. Municipios y distritos se filtran por cruce con secciones representadas por el CORE; las bloqueadas no intervienen. La AGEB se conserva completa y puede aparecer en varios universos. No se prorratean población, porcentajes o índices. No constituye equivalencia certificada de límites ni índice de sección/distrito. Se identifican las secciones sin cruce, sin asumir que son rurales. La cobertura rural requiere fuente y escala distintas.

## Presentación
Mapa base OpenStreetMap, grados oficiales CONAPO (no cuantiles locales), N/D gris, overlay opcional de secciones discontinuas y selección tabla/mapa. Tabla completa: clave, municipio, localidad, población, grado, índices, estado y once porcentajes originales. Ficha muestra todos los campos originales. Los porcentajes tienen diferentes poblaciones de referencia y no se agregan. Índices se muestran sin recalcular.

## Verificación
162 pruebas aprobadas en34archivos, cinco pruebas nuevas. Se verifica fuente real y preservación de valores, N/D, clasificación, selección territorial y rechazo de entradas inválidas. Muestra independiente de ida/vuelta de coordenadas: error máximo inferior a0.000001metros; intersecciones muestreadas con superficie positiva. JSON socioeconómico previo intacto. Comprobación interactiva y móvil pendiente; auditoría de usuario final de los tres módulos al terminar Socioeconómico.
