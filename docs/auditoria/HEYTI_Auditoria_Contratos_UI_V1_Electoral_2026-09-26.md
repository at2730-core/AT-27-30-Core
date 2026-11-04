# HEYTI — Revisión de contratos electorales de la interfaz V1

**26 de septiembre de 2026.** Inspección estática de ocho archivos entregados por Alex; sin ejecutar navegador, modificar código ni escribir PostgreSQL. Los archivos HTML aislados no incluyen sus seis JSON electorales, catálogo ni geometría, de modo que esta revisión no certifica la salida visual.

## Archivos recibidos y función

| Archivo | Evidencia de dependencia |
|---|---|
| `index.html` | Redirige a `estrategico/portal.html`; no lee datos electorales. |
| `portal.html` | Define `AT_PATHS`: geometría, catálogo, `P/G/A/DF/DL/S.json` y maestra; persiste rutas y universo en `localStorage`. |
| `analisis_territorial.html` | Consume JSON por elección y año; mapa, históricos y cálculos por sección. |
| `ganar_todo.html` | Consume JSON por elección y año; calcula márgenes, participación y escenarios 2027. |
| `campo.html` | Consume geometría, catálogo y JSON; obtiene LN 2024 de DL con fallback a P. |
| `estructura.html`, `dia_D.html` | Consumen geometría/catálogo/JSON y sus propias fuentes operativas. |
| `puntos_campo.geojson` | FeatureCollection válida con 10 puntos; es evidencia de Campo, no geometría de las 3,266 secciones. |

## Brechas verificadas en el código

1. El contrato de presentación actual es `secciones[sección][año]`, con campos de partido, `VOTOS` y `LN`. No transporta identificador de release, modalidad MR/RP, estado de verdad ni identidad histórica. Por ejemplo, `portal.html` líneas 968–991, `analisis_territorial.html` 1640–1661 y `ganar_todo.html` 1974–2002. Una sustitución directa de JSON por filas del nuevo staging no sería compatible.
2. El panel histórico de Análisis Territorial, líneas 1650–1719, calcula ganador entre PAN/PRI/PVEM/MORENA y convierte `NULL`/ausencia a cero (`+row.VOTOS||0`, `+row.LN||0`). El aviso “OTROS” reconoce diferencia entre la suma de esos cuatro y el total; aun así, el ganador mostrado por otras vistas puede excluir candidaturas o combinaciones.
3. Ganar Todo, líneas 1974–2002, convierte `LN` y `VOTOS` vacíos a cero y construye *shares* a partir de todas las claves distintas de `LN`/`VOTOS`. Al agregar metadatos al mismo objeto plano, esos metadatos podrían entrar en el cálculo; se requiere un adaptador explícito y datos electorales con esquema separado.
4. Campo, líneas 913–925, toma LN 2024 de DL y usa P si falta. Esa precedencia debe corresponder a una versión oficial certificada; P 2024 tiene discrepancias constatadas en la auditoría y no debe convertirse en fuente de respaldo implícita de verdad.
5. `puntos_campo.geojson` tiene 10 puntos y no suple `data/geo/secciones.geojson`. No es posible certificar cruces de mapa por sección con solo estos ocho archivos.

## Ajuste al contrato de staging y puerta de integración

- Conservar staging completo por release, modalidad, opción y estado de celda; definir una **proyección de lectura versionada** con `source_release_id`, `election_series_id`, `modality`, `truth_status`, `territorial_status` y cobertura, separando `totals` y `options` de los metadatos.
- Construir un adaptador V1 controlado para las vistas que todavía esperan `secciones[sección][año]`. Elegir explícitamente modalidad y corte por elección; ante ausencia, anulación o fuente sin certificar, indicar “sin dato certificado” y evitar cálculos de ganador/participación.
- Certificar resultados de competencia con el catálogo completo de opciones y reglas oficiales de candidatura/coalición por elección. La proyección de cuatro partidos podrá mostrarse únicamente como subconjunto identificado; no usarla como ganador oficial.
- Añadir pruebas de contrato y casos dorados antes de conectar datos reales a UI: DF21 sección 218 MR/RP; DL21 sección 1080; A21 secciones 163/2541; P24 sección 1150; G24 sección 1; una sección histórica y una unidad especial. Comparar fuente→staging→adaptador→UI sin transformar `NULL` en cero.

**Estado:** hallazgos de revisión estática para el diseño; no hay cambio de comportamiento ni aprobación de publicación. La migración de módulos queda condicionada a fuentes y proyección certificadas.
