# HEYTI — Política propuesta de precedencia electoral v0.1

**27 de septiembre de 2026. Estado: preferencia de auditoría; liberación para presentación pendiente.**

## Decisión

Usar los ZIP **INE/SICEE preservados** como referencia principal de consulta estadística para las 23 series 2018/2021/2024, con elección y modalidad explícitas. Conservamos los cómputos IEEG como evidencia oficial del corte local y las sentencias/actas como evidencia para adjudicar cambios. Esta precedencia es una **regla interna de HEYTI**; no afirma que el INE invalide al IEEG en elecciones locales.

| Situación | Regla de HEYTI |
|---|---|
| Valor SICEE y valor IEEG distintos, ambos numéricos | Registrar ambos valores, origen, corte y delta. La vista estadística preferirá SICEE **solo después** de certificar ZIP, modalidad, identidad y alcance del release. |
| SICEE vacío/guion/NULL; IEEG numérico | Conservar estado faltante SICEE. No rellenar silenciosamente desde IEEG ni convertirlo en cero; expediente explícito si se aprueba excepción. |
| SICEE `0`; IEEG numérico | Conservar el cero literal y marcar divergencia. Verificar semántica, especialmente LN de casilla especial, antes de participación. |
| Casilla `ANULADA`/`MODIFICADA` o sentencia | Preservar CAS crudo y SEC publicado; asociar resolución. No reconstruir SEC sumando todas las CAS ni reemplazarlo por el corte IEEG anterior. |
| MR/RP, `SECCION=0`, 9000+, identidad histórica | Nunca colapsar modalidades ni unidades especiales por número de sección. |
| Resultado de candidatura o ganador | Requiere catálogo completo y atribución oficial de coaliciones, candidaturas e independientes; cuatro partidos no bastan. |

La matriz `HEYTI_Matriz_Seleccion_Cortes_23_Series_v0_1.csv` mantiene `presentation_selection=UNDECIDED`, `cut_date_status=UNVERIFIED` y `certification_status=PENDING_SOURCE_ADJUDICATION`. La preferencia no activa un release, no modifica `at2730_core` y no autoriza publicación. La política deberá fijar el hash de cada ZIP/CSV y versión de corte al certificarlo; una sentencia verificada o una nueva publicación oficial abre revisión versionada, nunca una sustitución silenciosa.

## Fundamento y límite

El [INE presenta SICEE](https://www.ine.mx/voto-y-elecciones/resultados-electorales/) como consulta detallada de resultados federales y locales por casilla, sección y otros niveles. Su [manual](https://sicee.ine.mx/assets/media/Manual_de%20_Usuario_SICEE25.pdf) explica la descarga ZIP/CSV y señala que los organismos electorales locales comparten resultados locales. El [IEEG publica resultados y validez](https://ieeg.mx/resultados-y-validez-2023-2024/) y enlaza sus cómputos distritales y municipales. Estas publicaciones sustentan mantener las dos procedencias; no proporcionan en lo revisado metadatos suficientes para certificar fecha judicial exacta de cada ZIP SICEE.

En la [presentación institucional del SICEE del 26 de noviembre de 2025](https://centralelectoral.ine.mx/2025/11/26/version-estenografica-de-la-presentacion-de-la-estadistica-de-las-elecciones-2024-y-del-proceso-electoral-del-poder-judicial-2025-a-traves-del-sistema-de-consulta-de-la-estadistica-de-las-elecciones/), el INE describe el sistema como integración de cómputos, actas y determinaciones jurisdiccionales, con tablas locales proporcionadas por los OPLE. Esto refuerza usar SICEE como referencia estadística posterior, pero **la declaración general del sistema no identifica por hash ni fecha de extracción nuestros ZIP específicos**. Se conserva la puerta de certificación por archivo.

La búsqueda de documentación pública de LN no localizó una definición de por qué IEEG registra 1,000 y SICEE 0 en 41 casillas especiales 2024, ni la versión de LN que explica las 2,654 diferencias residuales. Son observaciones de los CSV, no una regla oficial inferida. El expediente por sección `HEYTI_Desglose_LN_IEEG_SICEE_2024_por_Seccion.csv` permanece abierto.

## Control previo a aplicación

1. Completar expedientes abiertos 2021/2024 y cotejo de cortes; comprobar sentencias donde figuren cambios.
2. Documentar por serie autoridad, modalidad, hash, fecha/alcance, unidad territorial y tratamiento de LN especial.
3. Ensayar un adaptador versionado con casos dorados y rechazo `NO_RELEASE_SELECTED` cuando falte certificación.
4. Proponer migración aditiva a la base viva y visualización solo tras revisión de la evidencia y pruebas fuente→DB→Capability→Runtime→Materialización→UI.
