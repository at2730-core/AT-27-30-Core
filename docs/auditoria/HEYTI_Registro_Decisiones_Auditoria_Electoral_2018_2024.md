# HEYTI — Registro de decisiones de auditoría electoral

Fecha: 25 de septiembre de 2026. Alcance: Guanajuato, 2018 → 2021 → 2024. Los datos de 2015 se conservan fuera de esta integración.

**Estado operativo:** auditoría de fuentes en curso. HEYTI-CORE local no está montado en este entorno; ninguna fuente, tabla o capacidad del repositorio del usuario se modificó aquí. Los artefactos de auditoría se guardan por separado. No afirmar que un dato se corrigió en la maestra cuando solo existe evidencia o contención en runtime.

| ID | Situación | Estado comprobado | Decisión para la integración |
|---|---|---|---|
| G24-COPY | `24G_*` replica exactamente `18G_*` en 3,137 filas de la maestra aportada | **Ya conocido** en trabajo previo. La cuarentena existe en el proveedor y su prueba unitaria, pero el ZIP CORE del 25/09/2026 muestra que la composición de runtime no la activa; la contención efectiva end-to-end queda **no acreditada en esta copia**. La copia de maestra permanece intacta. | Activar/verificar protección en la composición real mientras se reconstruye G 2024; probar fuente→DB→Capability→Runtime→Materialización y retirar guardia solo después de validación. |
| G24-DERIVED | `GANADOR_24G` copia `GANADOR_18G`; `PROY_2027_G_TOTAL/LN` copian `18G_TOTAL/LN` en 3,137 filas | **Consecuencia recién verificada de la fuente conocida**. No se validó protección de todas las proyecciones; el proveedor DescribeSection del ZIP solo publica su contrato de cuatro partidos. | Bloquear indicadores de ganador y proyección G dependientes de la maestra copiada; revisar consumidores y Golden Cases antes de habilitar. |
| DL21-GAP | `21DL_*` vacío en 328 secciones de la maestra (325 León, 3 Dolores Hidalgo) | Las 328 filas existen. Los seis campos del derivado `DL.json` coinciden con SICEE **MR**; total 178,751 votos MR. | Recuperar las seis opciones legado y todas las opciones originales MR; incorporar RP desde su CSV independiente. Investigar por qué la maestra perdió el bloque. |
| DF21-DETAIL | `21DF_*` en maestra solo tiene TOTAL y LN | SICEE DF MR/RP contiene partidos y opciones completas; el derivado reproduce MR para seis campos en las 3,159 secciones ordinarias. | Integrar todas las opciones de MR y RP con claves de modalidad; no deducir votos de partido desde TOTAL. |
| MODALITY | `DL/DF/S` de los derivados tienen modalidad distinta según año | 2018 y 2021 corresponden MR; 2024 DL/DF/S reproducen RP donde aplican. | Clave de resultado `(año, elección, modalidad, sección histórica, corte/fuente)`; no mezclar ni sumar MR y RP. |
| OPTION-SCOPE | Cuatro partidos directos omiten desglose oficial | 23 conjuntos inventariados; etiquetas locales y federales enlazadas a `PARTICIPANTES`. | Guardar partido, combinación, independiente, no registrados y nulos como opciones originales; no redistribuir coaliciones por defecto. |
| LOCAL24-CUT | Derivados locales 2024 proceden del corte IEEG de 9 junio | Coinciden en seis campos con suma de actas de ese ZIP; SICEE refleja estado posterior y LN distinta. | Preservar ambos cortes y estado judicial. Para presentación vigente, aplicar regla documentada por elección/corte; no sobrescribir historia. |
| LN24 | LN local derivada difiere de SICEE en 2,657 secciones | Descompuesta en cambios de LN ordinaria y tratamiento de casillas especiales. | No sustituir por un ajuste global de 1,000; conservar LN de cada fuente y casilla. |
| A21-NULL | A secciones 163 y 2541 sin total SICEE | Casillas anuladas; IEEG previo registra 371 y 436 votos. | Total NULL con causal y votos anteriores versionados; no reincorporar votos anulados. |
| DL21-RP-NULL | DL RP sección 1080 sin total | Paquetes no entregados; MR publica 0. | Conservar RP NULL y MR 0 por separado. |
| SPECIAL24 | Actas voto anticipado y MEC 2024 | IEEG usa claves 9001–9046; SICEE `SECCION=0`. Diferencia G anticipado distrito 22: dos nulos entre cortes. | Tipo de acta separado de sección geográfica; no colocar actas especiales en capa territorial. |
| AGG18 | 42 totales MUN/DIS de SICEE 2018 fallan identidad aritmética | 35 excluyen nulos exactamente; siete tienen otro residuo. Los agregados por candidatura comprobados cumplen su propia identidad. | Conservar campos crudos y expediente por fila; no corregir a ciegas ni imputar causa. |
| CI18 | Independientes locales 2018 | Mapeo nominal corregido por acuerdo IEEG. Cuatro columnas de dos municipios siguen ambiguas por persona; otras 23 opciones tienen vínculo territorial. | Mantener cuatro nombres sin adjudicación por columna hasta evidencia de acta nominal. |
| ONE-OFF | Maestra sin `21A_TOTAL` sección 1404 y `24P_TOTAL` sección 1150 | Derivados coinciden con los respectivos seccionales oficiales en esos totales. | Recuperar mediante ETL versionado; no parchear la maestra a mano. |

## Puertas de aceptación para la interfaz y materialización

Esta revisión usa los HTML aportados de V1; el estado actual de HEYTI-CORE requiere inspección al momento de integración. Las puertas siguientes se comprueban **después** de migrar fuentes y antes de habilitar indicadores nuevos:

| Prioridad | ID | Riesgo cuantificado | Evidencia mínima para cerrar |
|---|---|---|---|
| Bloqueante | UI-IDENTITY | Varios módulos consultan `"0051"` aunque los seis JSON aportados almacenan `"51"`; 994 claves de 1–999 por archivo. | Una búsqueda canónica reutilizada por los módulos; casos `1/51/999/1000` y secciones históricas con valor esperado de seis puestos. |
| Bloqueante | UI-RESULT | El cálculo limitado a cuatro siglas omite una columna de partido/independiente superior en 135/3,233 secciones A 2024, por ejemplo; coaliciones aún requieren atribución. | Ganador/margen por candidatura y modalidad cotejado con acta/agregado oficial para casos semilla; cero y empate explícitos. |
| Bloqueante | UI-NULL | A 2021 secciones 163/2541 pasan de total SICEE vacío a cero derivado; 48 filas sin votos y 179 empates positivos entre columnas actuales. | `NULL` con causal, cero legítimo, empate y ganador ausente diferenciados en fuente, API, materialización y vista. |
| Alta | UI-OPTIONS | Siete selectores de Ganar Todo y un gráfico de Análisis Territorial usan cuatro siglas fijas. | Catálogo versionado por elección/año/tipo de opción; controles y leyendas muestran todas las categorías elegibles, sin contar nulos como candidatura. |
| Alta | UI-LN | 87 pares sección–elección de 2024 con `VOTOS>LN` en al menos un corte; hay recortes a 100% en interfaz. | Valor bruto, fuente/corte y alerta visibles; expediente cotejado individualmente sin imputar causa. |
| Bloqueante | G24-CHAIN | La maestra aún copia `18G_*` en `24G_*` y campos relacionados de ganador/proyección; cuarentena previa conocida. | Reconstrucción G 2024 oficial y validación fuente→DB→Capability→Runtime→Materialización, incluida proyección; cuarentena activa hasta entonces. |

Los pendientes de nombre para cuatro columnas independientes de 2018 y de causas para discrepancias de agregados o LN se mantienen abiertos con cifra cruda preservada; **no obligan a inventar una adjudicación** para cargar el dato original con estado de revisión. El repositorio local de Alex no está disponible aquí; las puertas no se marcan como superadas por esta auditoría estática.

## Secuencia de cierre

1. Congelar originales, hashes y rutas del manifiesto de 23 conjuntos; fijar claves históricas, modalidad, corte, estado judicial y tipo de acta.
2. Construir importador reproducible para todas las columnas originales y una proyección seccional con controles de unicidad, completitud, suma y NULL/0. Rechazar copias literales de votos entre años como `24G_*` salvo justificación explícita.
3. Cargar en staging aislado; cotejar los casos semilla anteriores y conteos contra fuentes originales. Conservar discrepancias abiertas como incidencias con evidencia.
4. Integrar a HEYTI-CORE solo después de inspeccionar su checkout actual, esquema y ETL; ejecutar auditoría fuente→DB→Capability→Runtime→Materialización y Golden Cases en UI. Registrar cada cambio de fuente, transformación y módulo.
5. Retirar la cuarentena G 2024 únicamente cuando la reconstrucción y toda la cadena de entrega reproduzcan resultados certificados. No publicar ni ampliar visibilidad.

**Pendientes documentales:** evidencia nominal de cuatro columnas independientes 2018; causa de divergencias entre agregados 2018; causal precisa de ajustes de LN entre cortes; identidad/alcance de actas MEC; origen del vaciado de `21DL_*`. Estos pendientes no autorizan inventar datos ni impiden conservar la opción y su cifra original con estado de revisión.
