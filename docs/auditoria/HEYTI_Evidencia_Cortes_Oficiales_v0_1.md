# HEYTI — Evidencia para selección de cortes oficiales v0.1

**27 de septiembre de 2026.** Alcance: 23 series SEC/CAS de Guanajuato 2018, 2021 y 2024. Esta nota no selecciona release ni modifica `at2730_core`.

## Evidencia localizada

| Fuente | Lo que acredita | Lo que no acredita |
|---|---|---|
| [IEEG, proceso 2023–2024](https://ieeg.mx/proceso-electoral-2023-2024) y [Resultados y Validez](https://ieeg.mx/resultados-y-validez-2023-2024/) | El instituto publica separadamente resultados de cómputos distritales y municipales y documentos de resultados/validez. | Que los ZIP INE/SICEE de 2024 coincidan con un corte concreto del IEEG o incorporen todas las sentencias posteriores. |
| [IEEG, proceso 2020–2021](https://ieeg.mx/proceso-electoral-2020-2021) | Enlace institucional a cómputos de 2021. | Fecha o versión exacta de los ZIP INE/SICEE de 2021. |
| ZIP IEEG preservados localmente (`IEEG_Computos_2024_original.zip`, `IEEG_Computos_2021_original.zip`) | Sus nombres internos incluyen etiquetas `09062024_1200` y `20210610_1200`, respectivamente; identifican los archivos preservados. | Fecha de firmeza judicial o equivalencia entre los campos de IEEG y SICEE. Una etiqueta de archivo no constituye constancia de corte definitivo. |
| Matriz local `HEYTI_Matriz_Seleccion_Cortes_23_Series_v0_1.csv` | Identifica ZIP/CSV/hashes y conteos de SEC y CAS. El ensayo aislado pasó para 73,262 SEC y 179,779 CAS. | Certificación institucional o aptitud automática para presentación. |

## Decisión provisional

Las 23 filas permanecen `cut_date_status=UNVERIFIED`, `presentation_selection=UNDECIDED` y `certification_status=PENDING_SOURCE_ADJUDICATION`. El éxito técnico de carga no resuelve qué versión debe mostrarse. En especial, el corte local IEEG 2024 y las publicaciones INE/SICEE se conservan como fuentes y jurisdicciones diferenciadas; ninguna sustituye silenciosamente a otra.

## Evidencia necesaria para resolverlo

1. Localizar metadatos institucionales de generación/publicación y alcance de cada paquete INE/SICEE, incluyendo si hubo actualizaciones por sentencias y cómo se versionaron.
2. Confrontar por elección y modalidad los cortes IEEG disponibles con SEC/CAS SICEE usando llaves y conceptos homólogos; registrar diferencias de votos, total y lista nominal sin inferir causas.
3. Asociar resoluciones y actas documentales a las unidades afectadas. Un `RUTA_ACTA` textual sin PDF verificado no basta.
4. Aprobar una política versionada por `(año, elección, modalidad, tipo de unidad)` con fuente, corte, jurisdicción, excepciones y evidencia. Hasta entonces, la lectura de presentación devuelve `NO_RELEASE_SELECTED`.
