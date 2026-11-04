# Idea pendiente — App de auditoría de resultados electorales

**Proponente:** Alex. **Registrada:** 25 de septiembre de 2026. **Retomar:** cuando terminemos HEYTI-CORE; no desplazar la auditoría y migración electoral actual.

## Propósito

Crear una herramienta independiente que reciba fuentes oficiales de resultados de una elección y entregue a candidaturas/equipos expedientes revisables de discrepancias y patrones atípicos a nivel de acta, casilla, sección y agregado. Ayuda a decidir qué casos investigar con especialistas. La herramienta no declara fraude automáticamente.

## Revisiones iniciales

- Integridad aritmética: opciones + no registrados + nulos frente a total; actas repetidas, campos faltantes y ceros frente a valores vacíos.
- Plausibilidad: votos frente a lista nominal de la misma elección y modalidad; contemplar casillas especiales, voto anticipado, actas MEC y reglas específicas antes de alertar. Detectar concentraciones extremas, incluida votación unánime, como señales de revisión y no como imposibilidades demostradas.
- Comparación de cortes: IEEG/INE/SICEE, acta por casilla, sección y agregado; identificar cambios por partido, coalición, candidatura independiente y nulos; recuentos, anulaciones y modificación judicial.
- Procedencia y reproducibilidad: URL/fuente, hash, fecha de corte, versión, clave original, modalidad MR/RP, regla aplicada, cálculo exacto, evidencia de acta, severidad y estado de revisión.
- Entrega: tablero para filtrar y priorizar hallazgos, expediente exportable por caso y registro de revisión humana. No imputar intenciones ni causas sin pruebas.

## Casos semilla de HEYTI

- Gubernatura Guanajuato 2024, voto anticipado distrito 22: IEEG 4 votos (2 nulos), SICEE 2 (0 nulos), ambos con 2 votos válidos y LN 2. Preservar versiones.
- 2018: cuatro discrepancias entre casilla/sección y agregado municipal/distrital de candidaturas independientes; necesitan resolución documental.
- 2021: totales seccionales vacíos por anulaciones o paquetes no entregados; NULL y 0 tienen significados distintos.
- 2024: actas especiales con claves 9001–9046 en IEEG, SECCION=0 en SICEE; evitar tratarlas como secciones geográficas.

## Punto de reanudación

Después de cerrar HEYTI-CORE, definir alcance mínimo, fuentes admitidas, criterios auditables, reglas de excepción y prototipo con casos reales documentados. Mantener el proyecto separado de la ingesta vigente de HEYTI-CORE hasta acordar arquitectura.
