# HEYTI V2 — Punto de retorno y revisión inicial

Fecha: 5 de octubre de 2026. Estado: PREPARACIÓN; demo no implementada ni publicada.

## Punto de retorno de Auditoría Migración Electoral II

La auditoría permanece abierta y se retomará en su hilo original. La evidencia documental más reciente consultada es HEYTI_Revision_A2024_Lote_04_Seis_Municipios_v0_1.md, del 3 de octubre. Este lote no tuvo acceso ni escritura DB, selección ni certificación. Conserva 27 pendientes judiciales; cuatro lotes cubren barrido documental de 24 municipios, además del reporte León/Salamanca/Cortazar. Cobertura de revisión no equivale a cortes certificados.

Siguiente paso documentado: consolidar matriz municipio/serie con documento localizado, total cotejado, vector pendiente, expediente pertinente, recursos posteriores, fecha de corte y condición de cierre. Priorizar DF2024 MR distrito 10 y documentos administrativos de transcripción incompleta. Comprobar si el corte ya incorpora la anulación de 2797 C1 antes de aplicar cualquier ajuste; no trasladar efectos a A2024 ni RP.

La salida SQL adjunta del 3 de octubre 15:37:57 registra 19 filas de San Miguel de Allende, con identidades originales y hashes; termina en ROLLBACK. Esto acredita ese cotejo, no una liberación electoral completa.

El contexto recuperado menciona NO_RELEASE_SELECTED, 471 pruebas y 65 subtests, y evidencia en D:\GitHub\AT-27-30-core\docs\auditoria\HEYTI_Resultado_Runtime_Entrega_Electoral_v0_1.json. El archivo y esas pruebas NO fueron inspeccionados ni ejecutados en esta sesión. No se certifica HEAD, rama o estado de trabajo actual.

## Fuentes y bloqueos conservados

Registro consultado: HEYTI_Registro_Unico_Pendientes_Auditoria_Electoral_v0_1.md, corte 30/09/2026. Se mantienen LN24, CCPC24, ESPEC24, VA24, AG18, DF18RP, EXT18, ESP21, JUD y DB; este documento no los cierra ni sustituye el registro. Conservar originales, cortes, modalidades, niveles, vacíos y discrepancias; NULL no equivale a cero. La integración abarca 2018, 2021 y 2024; no incorporar 2015 por defecto.

## Revisión de la entrega actual

Sólo están disponibles ocho archivos adjuntos. D:\GitHub\AT-27-30-core es una ruta del equipo del usuario y no es accesible desde esta sesión. Estos HTML no acreditan el estado del repositorio actual.

Análisis Territorial, Ganar Todo y Campo leen AT_UNIVERSE y AT_PATHS de localStorage. El portal escribe un universo con scope, key, label y ts. Las rutas electorales son archivos JSON locales; no se ha acreditado conexión a HEYTI-CORE. No se ha comprobado persistencia de centro/zoom entre módulos.

Faltan data/geo/secciones.geojson, data/catalogo_territorial.json, data/electoral/{P,G,A,DF,DL,S}.json, data/Datos_Electoral.json y recursos assets. El portal también referencia assets/css/base.css, assets/logo-at.svg y src/portal.js. index.html remite a estrategico/portal.html. Los nombres numerados adjuntos no reproducen esa estructura. Los módulos dependen de CDN externos; no se ha verificado funcionamiento offline.

puntos_campo.geojson contiene 10 features y campos de nombre, teléfono, domicilio y PIN. Su clasificación como demo no está acreditada; no cargarlo en una presentación como datos ficticios. Conservar original y preparar una copia explícita de demostración cuando se defina su tratamiento. No se copian valores de contacto a este informe.

## Puerta de validación de la demo

| Tramo | Estado actual | Evidencia necesaria |
|---|---|---|
| Fuente | Entrega parcial, sin certificación electoral inspeccionada | Manifestación de procedencia, hash, corte y alcance por serie |
| Fuente→DB | Pendiente | Cotejo con llaves y definición comunes; conservar discrepancias |
| DB→capability→runtime | Pendiente | Repositorio actual, contratos, lector y salida trazable |
| Runtime→pantalla | Pendiente | Golden Cases y valores esperados en mapas, tablas y gráficas |
| Navegación/universo/zoom | Base localStorage identificada; interacción no probada | Mismo universo y vista tras AT→Ganar Todo→Campo→AT y recarga |

La demo identificará cada conjunto como DEMO, CERTIFICADO para un alcance concreto o PENDIENTE. No inventar resultados electorales ni presentar simulaciones como predicción oficial. Las cifras de auditoría no se convierten automáticamente en datos liberados para pantalla.

## Insumo requerido para continuar

ZIP del estado actual de D:\GitHub\AT-27-30-core, incluyendo cambios sin commit, src, tests, docs/architecture, docs/auditoria, contratos y lectores vigentes. Incluir dependencias locales de los módulos V1 cuando vivan en otro repositorio. Excluir credenciales, .env, entornos virtuales y node_modules. Acompañar salida git status --short --branch y git log -1 --format=fuller. Un archivo git archive por sí solo no conserva cambios sin commit.

No se modificó ningún adjunto, fuente, DB o repositorio. No hubo despliegue ni cambio de visibilidad.

## Inventario de originales recibidos

| Archivo | Bytes | SHA-256 |
|---|---:|---|
| 01-index.html | 670 | 72446e69f8c2d11977d0d89bb11b82f21721dc9c237c85b5f03f2782e94e3e64 |
| 02-ganar_todo.html | 281259 | 5583d0d6255bfd3719fd7fe6b0198b2722bd3e04614d63d5d5ee1e0861ebade5 |
| 03-analisis_territorial.html | 162923 | 23db2f46f9fbd346667994298a4df8121dc707679b29119427a1825c2e11d775 |
| 04-puntos_campo.geojson | 7851 | bfab666ae7c597127850f9cb16813e9562b9c5060b6ce29fffefdfa1d6844825 |
| 05-estructura.html | 152270 | 8b36f298c63ecc94b6447ddfe89a6ad3aafed47ba06117817568a9aa52130ed6 |
| 06-dia_D.html | 71951 | 3d3cee0c051e56829a3668fb3c6495a01696f83e628478b50f606e4d1eaaed40 |
| 07-portal.html | 43429 | 2d2d2c88ec10b05eefe0b45f5f31b6d3d4fdccc1d47fc354d9147ad9295f78b1 |
| 08-campo.html | 100797 | 872cedbee5245db238ba19d7b7902a84fd321e75d867e8a885010c761913ea06 |
