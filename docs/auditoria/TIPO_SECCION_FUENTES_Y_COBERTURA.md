# HEYTI V2 — Tipo urbano-rural de sección

## Decisión y alcance
Se sustituye la entrada pendiente «Índice urbano-rural» por «Tipo urbano-rural · secciones». La fuente oficial clasifica las secciones como urbanas (2), mixtas (3) y rurales (4). Los códigos identifican categorías, sin escala de 0 a 100 ni orden de bienestar.
V1 admitía un campo URB aportado manualmente y un fallback de demostración aleatorio; no se encontró una fórmula acreditada para un índice continuo en los archivos revisados. La nueva consulta conserva la clasificación respaldada por los datos disponibles.

## Fuentes conservadas
1. Estadísticas Censales a Escalas Geoelectorales 2020, INEGI/INE, archivo INE_SECCION_2020.csv y catálogo cat_secciones_2020.csv de Guanajuato. El descriptor confirma TIPO: 2 Urbana, 3 Mixta, 4 Rural. Datos censales 2020, cartografía electoral de enero de 2021. El tipo, población y claves se cotejan con la referencia oficial existente.
2. Campo TIPO de secciones.geojson del archivo territorial de V2 aportado por Alex. Se conserva su procedencia y SHA-256. La fecha oficial de esta cartografía no está acreditada; no se denomina clasificación vigente ni se usa una fecha de archivo como corte oficial.

https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/geoelectorales/eceg_2020_csv.zip
https://gaia.inegi.org.mx/mdm6/docs/geoelectorales/Metodolog%C3%ADa_de_Estad%C3%ADsticas_Censales_a_escalas_Geoelectorales.pdf

## Cotejo completo
- Censo: 3,161 registros, 1,873 urbanos, 224 mixtos y 1,064 rurales.
- Archivo V2: 3,266 secciones, 1,969 urbanas, 235 mixtas y 1,062 rurales.
- 3,131 claves comunes; 13 clasificaciones distintas. No se interpreta como urbanización o evolución temporal demostrada.
- 135 claves del archivo sin registro censal propio: N/D censal, sin heredar clasificación del origen.
- 30 registros censales sin polígono en el archivo de referencia: se conservan en la tabla estatal fuera del mapa, sin asignar distrito actual.

## Presentación y denominadores
Selector de universo y fuente para colorear. Mapa base, números de sección, tres colores categóricos y gris para N/D. Tabla completa con ambas clasificaciones, cotejo, población censal, municipio y DF de la fuente 2020 y correspondencia territorial. Selección con detalle y acercamiento cuando existe geometría.
Los porcentajes cuentan secciones representadas con tipo utilizable de la fuente seleccionada. Los N/D se enumeran aparte; no se calculan porcentajes de habitantes urbanos/rurales ni se reparte población de secciones mixtas. La población se conserva como contexto individual por sección, sin total territorial certificado.
La tabla estatal de referencia tiene 3,296 filas: 3,266 representadas y 30 censales sin polígono. La vista censal tiene 3,131 tipos utilizables sobre los polígonos y 135 N/D. En la del archivo V2 hay 3,266 tipos utilizables si el CORE entrega la misma geometría.
Se coteja una huella geométrica calculada sobre tipo, estructura de coordenadas y valores IEEE-754 (FNV-1a de 32 bits) para evitar asociar automáticamente un tipo del archivo a otro polígono con la misma clave. No es autenticación oficial. Si la huella no coincide, el tipo original sigue en la tabla, pero no se aplica al mapa ni se incluye en el cotejo de tipos. La clasificación censal sigue siendo enlace por clave con equivalencia de límites pendiente.

## Verificación
184 pruebas aprobadas en 37 archivos, ocho nuevas. Compilación correcta, con aviso no bloqueante de tamaño JavaScript. Cotejados directamente con el CSV los 3,161 tipos, poblaciones y claves. Comprobadas las 3,266 huellas entre la preparación Python y el código de aplicación y la cobertura estatal completa con las funciones de la aplicación. El JSON socioeconómico original conserva su SHA-256.
No se ejecutó comprobación interactiva ni móvil. La auditoría de usuario final de los tres módulos se realizará al terminar Socioeconómico. Queda pendiente Proyección 2027.

## Continuidad y archivos
Fuentes originales intactas. Archivo nuevo public/data/heyti-tipo-seccion-2020.json; SocioRuralWorkspace.tsx, socioRural.ts y socioRural.test.ts. Integración en ApplicationShell, WorkspaceCanvas y ModuleNavigation. Respaldos en auditoria-socioeconomico/respaldo_pre_tipo_seccion. Preparación y comprobación reproducibles en preparar_tipo_seccion.py y verificar_tipo_seccion.mjs.
