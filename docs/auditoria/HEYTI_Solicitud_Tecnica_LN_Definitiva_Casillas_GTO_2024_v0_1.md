# HEYTI — Especificación para obtener LN definitiva por casilla, Guanajuato 2024

**Objeto.** Obtener un catálogo estadístico oficial de la Lista Nominal de Electores Definitiva con Fotografía utilizada el 2 de junio de 2024 en Guanajuato, por casilla, sin nombres, claves de elector ni otros datos personales. Incluir, si corresponde, el efecto de adendas y resoluciones administrativas o judiciales. Precisar fecha de corte, versión, autoridad responsable y método de distribución de electores entre casillas de una sección.

**Campos mínimos solicitados.** Entidad (11), municipio, sección, distrito federal/local, tipo de casilla, número de casilla, extensión contigua, LN definitiva asignada a esa casilla, fecha y versión del catálogo. Para casillas extraordinarias, especiales y voto anticipado, indicar la regla de LN y una clave comparable. Entregar CSV/XLSX y ficha metodológica; si los datos por casilla no son públicos, indicar el agregado disponible y la ruta formal para solicitar únicamente cantidades estadísticas.

**Razón y alcance.** En 28 municipios, 4,642 casillas ordinarias B/C/E se emparejan por municipio, sección, tipo, número y extensión. Los tres CSV de cómputos IEEG 2024 comparten los mismos valores de LN entre sí; las tres series SICEE 2024 también coinciden entre sí. Ambos paquetes discrepan en 3,037 casillas y coinciden en 1,605. Los 16 campos de votos de Ayuntamientos IEEG/SICEE coinciden en las 4,679 casillas cotejadas (incluidas S y VA); la LN es un problema separado de los votos. Véase `HEYTI_Cotejo_28_Municipios_A2024_IEEG_SICEE_v0_1.md`.

**Priorización.** Las 58 casillas ordinarias con |IEEG − SICEE| > 5 se concentran en estas 28 secciones:

| Municipio | Sección |
|---|---:|
| CORTAZAR | 697 |
| CORTAZAR | 715 |
| JARAL DEL PROGRESO | 1195 |
| LEON | 1349 |
| LEON | 1514 |
| LEON | 1515 |
| LEON | 1527 |
| LEON | 1591 |
| LEON | 1677 |
| LEON | 1702 |
| LEON | 1705 |
| LEON | 1805 |
| LEON | 3043 |
| LEON | 3094 |
| LEON | 3139 |
| LEON | 3188 |
| SALVATIERRA | 2297 |
| SALVATIERRA | 2303 |
| SALVATIERRA | 2338 |
| SAN FELIPE | 2409 |
| URIANGATO | 2797 |
| VALLE DE SANTIAGO | 2839 |
| VALLE DE SANTIAGO | 2869 |
| VALLE DE SANTIAGO | 2887 |
| VICTORIA | 2892 |
| VICTORIA | 2903 |
| YURIRIA | 2970 |
| YURIRIA | 2978 |

**Caso testigo.** San Felipe, sección 2409, casillas B/C1/C2/C3: IEEG 750/750/750/563 (suma 2,813); SICEE 563/563/563/563 (suma 2,252). Se solicita el valor definitivo por cada casilla y, si hubo rectificación, la fecha y el acto que la sustenta. No inferir el valor definitivo por la repetición entre series de un mismo paquete.

**Criterio de cierre.** Registrar procedencia y hash del catálogo recibido; emparejar claves sin confundir sección 0, especiales y VA; comparar 3,037 discrepancias y documentar excepciones. Mantener ambas cifras y `LN_NO_ADJUDICADA` mientras falte evidencia independiente. Este documento es una especificación de datos; no constituye una solicitud enviada ni autoriza cambios en la base viva.

## Ampliación de alcance — 28 de septiembre de 2026

La cifra de 3,037 discrepancias corresponde al subconjunto inicial de **28 municipios**. Para la solicitud definitiva, el alcance es **todo Guanajuato (46 municipios)**. La matriz `HEYTI_Matriz_Cotejo_CAS_LN_A2024_46_v0_1.csv` (SHA-256 `70a14f21e8fcd33b905ccca4334d3934fb6e64532fd17bdd239860e4b1e9d164`) identifica por municipio el número de casillas y claves emparejadas, las diferencias de LN ordinaria y especial, y la magnitud absoluta de las diferencias ordinarias. Solicitar todas las claves de los 46 municipios, no sólo las 28 secciones prioritarias arriba listadas.

Priorizar para una primera respuesta los municipios **León, Irapuato, Celaya, Valle de Santiago y Victoria (Guanajuato)**, según suma de diferencias absolutas de LN ordinaria por clave. En Victoria, las secciones **2892** y **2903** concentran seis casillas con una diferencia IEEG − SICEE de **−1,122** (−188/−187/−187 y −187/−187/−186). Como caso testigo adicional, León **3094 B1** registra **375** IEEG y **748** SICEE, con cero votos en la elección de ayuntamiento en ambos paquetes. Estos casos requieren cantidad estadística por casilla, fecha exacta del corte y aclaración sobre eventuales adendas y actualizaciones.

Pedir también una **tabla oficial de correspondencia** para las claves de voto anticipado: por ejemplo, San Felipe `9037 A1` IEEG frente a `SEC=0 A2` SICEE. No equiparar claves distintas por compartir votos y LN. Para casillas especiales, solicitar confirmación expresa de que no existe LN ordinaria asignada y la semántica de `1,000` en el archivo IEEG frente a `0` en SICEE. La entrega de listas nominales definitivas a los 15 consejos distritales fue informada por INE Guanajuato (https://centralelectoral.ine.mx/2024/04/21/entrega-ine-guanajuato-listas-nominales-de-electores-definitivas-a-15-consejos-distritales/); esa nota acredita la entrega institucional, pero **no** proporciona el extracto estadístico por casilla solicitado aquí.
