# HEYTI — Cotejo de 28 municipios A2024 pendientes

**27 de septiembre de 2026.** Comparación aritmética de archivos originales, sin cambios en la base viva. El estado judicial de estas 28 filas sigue pendiente.

- IEEG: `IEEG_Computos_2024_original.zip`, SHA-256 `d1a2760a600206358f4e376ea2f3ab67c6e33548db7bb4abc4aaede0c7a865b5`; subarchivo `09062024_1200_COMPUTOS_AYUN_GTO.zip`, `GTO_AYUN_2024.csv`, corte declarado 09/06/2024 12:00 UTC−6.
- SICEE: `INE_SICEE_GTO_PEL_2024_original.zip`, SHA-256 `13fe6a2ddb432922bddc9090f08eb0e558aeb3094ef1ba763b78d789b3d55e69`; `2024_SEE_AYUN_GTO_MUN.csv`.
- Método: agrupar por `ID_UBICACION` las casillas IEEG con `CONTABILIZADA=1`, tratar celdas numéricas vacías como cero solo para la suma, y comparar contra `ID_MUNICIPIO` SICEE. Las 28 claves se toman de las filas `JUDICIAL_NO_REVISADO` del registro municipal.
- Una casilla IEEG de Salvatierra (`9036 VA01`) tiene `CONTABILIZADA=0`, 0 votos y LN=1; queda excluida de la suma conforme al indicador de la fuente.

## Resultado

Los 28 municipios coinciden exactamente en **16 campos de votos**: `PAN`, `PRI`, `PRD`, `PVEM`, `PT`, `MC`, `MORENA`, `PAN_PRI_PRD`, `PAN_PRI`, `PAN_PRD`, `PRI_PRD`, `CAND_IND_1`, `NUM_VOTOS_VALIDOS`, `NUM_VOTOS_CAN_NREG`, `NUM_VOTOS_NULOS`, `TOTAL_VOTOS`. Las columnas `CAND_IND_2` y `CAND_IND_3` de SICEE MUN están vacías o en cero para estas 28 filas y no tienen par explícito en el CSV IEEG.

**La lista nominal difiere en 27 de 28 municipios.** El signo de la tabla es IEEG − SICEE; no se ha determinado la causa y no debe interpretarse automáticamente como error de una fuente.

| ID | Municipio | Votos en ambas fuentes | LN IEEG agregada | LN SICEE MUN | Δ LN |
|---:|---|---:|---:|---:|---:|
| 6 | ATARJEA | 3,561 | 4,535 | 4,535 | +0 |
| 8 | MANUEL DOBLADO | 19,337 | 33,965 | 33,899 | +66 |
| 9 | COMONFORT | 32,192 | 65,693 | 64,628 | +1,065 |
| 10 | CORONEO | 6,056 | 9,901 | 9,889 | +12 |
| 11 | CORTAZAR | 48,698 | 79,502 | 79,948 | -446 |
| 12 | CUERAMARO | 13,721 | 25,273 | 25,233 | +40 |
| 13 | DOCTOR MORA | 13,057 | 20,468 | 20,443 | +25 |
| 18 | JARAL DEL PROGRESO | 19,067 | 30,446 | 30,881 | -435 |
| 19 | JERECUARO | 22,365 | 42,337 | 42,256 | +81 |
| 20 | LEON | 711,277 | 1,278,414 | 1,272,183 | +6,231 |
| 21 | MOROLEON | 25,422 | 48,741 | 47,629 | +1,112 |
| 22 | OCAMPO | 11,110 | 19,602 | 19,567 | +35 |
| 24 | PUEBLO NUEVO | 7,855 | 11,638 | 11,618 | +20 |
| 25 | PURISIMA DEL RINCON | 34,446 | 63,551 | 62,492 | +1,059 |
| 26 | ROMITA | 30,035 | 51,636 | 50,586 | +1,050 |
| 27 | SALAMANCA | 125,852 | 229,330 | 227,017 | +2,313 |
| 28 | SALVATIERRA | 44,717 | 87,513 | 86,884 | +629 |
| 30 | SAN FELIPE | 45,422 | 90,887 | 89,275 | +1,612 |
| 31 | SAN FRANCISCO DEL RINCON | 56,943 | 102,793 | 101,717 | +1,076 |
| 32 | SAN JOSE ITURBIDE | 38,858 | 69,787 | 68,729 | +1,058 |
| 33 | SAN LUIS DE LA PAZ | 53,271 | 99,899 | 98,821 | +1,078 |
| 34 | SANTA CATARINA | 3,399 | 4,962 | 4,983 | -21 |
| 39 | TARIMORO | 18,214 | 32,419 | 32,362 | +57 |
| 41 | URIANGATO | 29,731 | 54,907 | 54,305 | +602 |
| 42 | VALLE DE SANTIAGO | 59,881 | 122,775 | 122,822 | -47 |
| 43 | VICTORIA | 10,712 | 15,422 | 16,528 | -1,106 |
| 45 | XICHU | 5,945 | 9,020 | 9,015 | +5 |
| 46 | YURIRIA | 32,287 | 66,967 | 66,806 | +161 |

**Control:** 28 municipios; 16 × 28 = 448 comparaciones de campos de voto sin diferencias; 27 diferencias de LN; Δ LN agregado +17,332.

## Límite y siguiente cotejo

Este resultado compara el agregado de casillas IEEG con la fila municipal SICEE, sin afirmar equivalencia de identidad de cada casilla ni cierre judicial. Para explicar LN se necesita comparar CAS por clave completa y reglas de lista nominal, incluidas casillas especiales, voto anticipado y registros no contabilizados. La sentencia federal de San Miguel de Allende que modifica cuatro casillas mantiene bloqueada la selección de A2024 como serie definitiva.

## Localización de las diferencias de LN en CAS

La clave comparable ordinaria es `(municipio, sección numérica, tipo, id de casilla, extensión)`. Dentro de los 28 municipios hay **4,663 casillas con esa clave presente en ambos archivos**; 3,058 tienen LN distinta. Sus diferencias IEEG − SICEE se agrupan así:

| Tipo | Casillas emparejadas | LN distinta | Δ LN |
|---|---:|---:|---:|
| Básica (B) | 1,881 | 1,285 | −1,380 |
| Contigua (C) | 2,663 | 1,701 | −1,958 |
| Extraordinaria (E) | 98 | 51 | −329 |
| Especial (S) | 21 | 21 | +21,000 |
| **Total** | **4,663** | **3,058** | **+17,333** |

En las **21 especiales** IEEG consigna `LISTA_NOMINAL=1000` y SICEE `LISTA_NOMINAL=0`, con votos iguales en los ejemplos comprobados; es una diferencia de convención de registro observada, cuya norma y alcance aún deben verificarse. Ejemplo: Comonfort, sección 613, `SMR01` IEEG / `S01` SICEE, 13 votos en ambos.

Las 3,037 diferencias restantes de B/C/E suman −3,667. De ellas, 2,979 tienen magnitud de uno a cinco registros; **58** son mayores. Ejemplos: Valle de Santiago, sección 2869 E01, LN IEEG 376 / SICEE 750, 376 votos en ambos; León, sección 3094 B, LN IEEG 375 / SICEE 748, 0 votos en ambos. Esas diferencias requieren cotejo de fuente nominal y de acta antes de clasificar error o corrección.

Hay otras **16 casillas de voto anticipado** identificadas en IEEG como secciones 9022–9046 y `VA01`, y en SICEE como sección 0 y distintos identificadores `VA`. Se emparejan de manera unívoca por municipio, tipo A y total de votos/LN, pero **no por la clave literal**. Una de ellas, Salvatierra `9036 VA01` (0 votos, LN=1), está marcada `CONTABILIZADA=0` en IEEG; ello explica que Δ LN municipal sea +17,332, una unidad menor que la suma de las casillas emparejadas. No se debe unir por sección literal ni territorializar sección 0.

Este análisis localiza las diferencias y no acredita que la LN de una de las dos fuentes sea la definitiva. La equivalencia de votos por casilla completa y los 58 casos ordinarios de LN más grandes son el siguiente control.

## Control adicional de votos por casilla

En las **4,663 casillas con clave ordinaria emparejada** se compararon individualmente los mismos 16 campos de votos y no hubo diferencias (74,608 comparaciones). Las **16 casillas de voto anticipado** se asociaron exclusivamente dentro del mismo municipio por tipo A, al haber una por municipio en cada fuente; sus 16 campos de votos también coinciden (256 comparaciones), pese a que las secciones e identificadores literales difieren. En total son **4,679 casillas y 74,864 comparaciones de campos de votos sin discrepancia** entre estos dos archivos para los 28 municipios. La VA de Salvatierra no contabilizada aporta cero votos en ambos; su LN no se agregó al cómputo IEEG. Esta equivalencia es estadística de los archivos comparados, no una declaración de firmeza judicial ni un aval de LN.

## Anexo: 58 casillas B/C/E con |Δ LN| > 5

El signo es IEEG − SICEE. Los votos de cada par coinciden, incluso cuando la LN no coincide. Esta lista identifica prioridades de cotejo documental, no una corrección automática.

| Municipio | Sección | Casilla IEEG | LN IEEG | LN SICEE | Δ LN | Votos ambas |
|---|---:|---|---:|---:|---:|---:|
| CORTAZAR | 697 | B | 562 | 748 | -186 | 386 |
| CORTAZAR | 697 | C01 | 561 | 748 | -187 | 394 |
| CORTAZAR | 697 | C02 | 561 | 747 | -186 | 393 |
| CORTAZAR | 715 | B | 721 | 727 | -6 | 260 |
| JARAL DEL PROGRESO | 1195 | B | 501 | 750 | -249 | 387 |
| JARAL DEL PROGRESO | 1195 | C01 | 500 | 749 | -249 | 395 |
| LEON | 1349 | B | 643 | 750 | -107 | 508 |
| LEON | 1349 | C01 | 643 | 749 | -106 | 549 |
| LEON | 1349 | C02 | 643 | 749 | -106 | 514 |
| LEON | 1349 | C03 | 642 | 749 | -107 | 519 |
| LEON | 1349 | C04 | 642 | 749 | -107 | 515 |
| LEON | 1349 | C05 | 642 | 749 | -107 | 494 |
| LEON | 1514 | B | 473 | 467 | +6 | 350 |
| LEON | 1515 | B | 606 | 597 | +9 | 446 |
| LEON | 1527 | B | 557 | 550 | +7 | 431 |
| LEON | 1591 | B | 563 | 750 | -187 | 458 |
| LEON | 1591 | C01 | 563 | 750 | -187 | 420 |
| LEON | 1591 | C02 | 563 | 749 | -186 | 380 |
| LEON | 1677 | B | 643 | 749 | -106 | 384 |
| LEON | 1677 | C01 | 643 | 749 | -106 | 439 |
| LEON | 1677 | C02 | 643 | 749 | -106 | 389 |
| LEON | 1677 | C03 | 643 | 749 | -106 | 387 |
| LEON | 1677 | C04 | 643 | 749 | -106 | 401 |
| LEON | 1677 | C05 | 643 | 749 | -106 | 0 |
| LEON | 1702 | B | 728 | 722 | +6 | 541 |
| LEON | 1702 | C01 | 728 | 722 | +6 | 584 |
| LEON | 1705 | B | 440 | 434 | +6 | 346 |
| LEON | 1705 | C01 | 439 | 433 | +6 | 360 |
| LEON | 1805 | B | 680 | 672 | +8 | 506 |
| LEON | 3043 | B | 648 | 640 | +8 | 521 |
| LEON | 3094 | B | 375 | 748 | -373 | 0 |
| LEON | 3139 | B | 498 | 749 | -251 | 394 |
| LEON | 3139 | C01 | 498 | 748 | -250 | 412 |
| LEON | 3188 | B | 653 | 646 | +7 | 540 |
| LEON | 3188 | C01 | 653 | 646 | +7 | 527 |
| LEON | 3188 | C02 | 653 | 646 | +7 | 536 |
| LEON | 3188 | C03 | 653 | 646 | +7 | 527 |
| SALVATIERRA | 2297 | C01 | 719 | 725 | -6 | 377 |
| SALVATIERRA | 2303 | B | 717 | 724 | -7 | 306 |
| SALVATIERRA | 2338 | B | 501 | 750 | -249 | 371 |
| SALVATIERRA | 2338 | C01 | 500 | 749 | -249 | 374 |
| SAN FELIPE | 2409 | B | 750 | 563 | +187 | 272 |
| SAN FELIPE | 2409 | C01 | 750 | 563 | +187 | 260 |
| SAN FELIPE | 2409 | C02 | 750 | 563 | +187 | 292 |
| URIANGATO | 2797 | B | 500 | 750 | -250 | 400 |
| URIANGATO | 2797 | C01 | 500 | 750 | -250 | 413 |
| VALLE DE SANTIAGO | 2839 | B | 500 | 750 | -250 | 393 |
| VALLE DE SANTIAGO | 2839 | C01 | 500 | 750 | -250 | 372 |
| VALLE DE SANTIAGO | 2869 | E01 | 376 | 750 | -374 | 376 |
| VALLE DE SANTIAGO | 2887 | B | 374 | 748 | -374 | 308 |
| VICTORIA | 2892 | B | 561 | 749 | -188 | 544 |
| VICTORIA | 2892 | C01 | 561 | 748 | -187 | 526 |
| VICTORIA | 2892 | C02 | 561 | 748 | -187 | 523 |
| VICTORIA | 2903 | B | 562 | 749 | -187 | 471 |
| VICTORIA | 2903 | C01 | 562 | 749 | -187 | 467 |
| VICTORIA | 2903 | C02 | 562 | 748 | -186 | 461 |
| YURIRIA | 2970 | B | 732 | 724 | +8 | 312 |
| YURIRIA | 2978 | B | 584 | 578 | +6 | 286 |

Fuente metodológica contextual: el manual oficial del PREP 2024 del INE, https://ayuda.ine.mx/2024/assets/docs/prep/manual-base-datos-prep.pdf, define LN=0 para casillas especiales porque carecen de lista nominal, y distingue boletas disponibles de LN. Esa definición es de PREP, no prueba por sí sola el contrato de cada campo SICEE o del cómputo IEEG aquí comparado.

## Priorización de los 58 casos ordinarios

Los 58 renglones se concentran en **9 municipios y 28 secciones**: León 31, Victoria 6, Cortazar 4, Salvatierra 4, Valle de Santiago 4, San Felipe 3, Jaral del Progreso 2, Uriangato 2 y Yuriria 2. En **36 renglones**, la LN SICEE es 748, 749 o 750 y excede la LN IEEG; los votos siguen idénticos. Otros tres renglones de San Felipe sección 2409 muestran la dirección inversa (IEEG 750, SICEE 563; Δ +187 en B, C1 y C2). La repetición dentro de una misma sección favorece examinar la asignación de LN por sección/casilla y la versión del padrón antes de tratar cada fila como transcripción independiente; esta es una hipótesis de trabajo, no una causa probada.

El anexo técnico de coordinación INE–IEEG para Guanajuato 2024, https://repositoriodocumental.ine.mx/xmlui/bitstream/handle/123456789/153485/2023-UTVOPL-AT-PEC-GUANAJUATO-F.pdf, describe cuadernillos de LN con un máximo de 750 electores; **no** establece que toda casilla deba tener LN=750 ni determina cuál valor de estos CSV es correcto. Para resolver los 28 grupos de sección se requieren los listados definitivos por sección/casilla o una aclaración documentada de los productores de ambos archivos.

## Caso testigo: San Felipe, sección 2409

| Fuente | B | C1 | C2 | C3 | LN seccional |
|---|---:|---:|---:|---:|---:|
| IEEG CAS 09/06/2024 | 750 | 750 | 750 | 563 | 2,813 |
| SICEE CAS / SEC | 563 | 563 | 563 | 563 | 2,252 |

Los votos por casilla son **272, 260, 292 y 263**, idénticos en IEEG y SICEE; suman 1,087. El SEC SICEE publica LN=2,252 y votos=1,087, que reproducen su CAS. Como referencia temporal, el acuerdo IEEG CGIEEG/082/2023 (https://api.ieeg.mx/repoinfo/Uploads/231115-extra-acuerdo-082.pdf) reportaba LN seccional 2,188 en noviembre de 2023 para fines de porcentajes de candidaturas independientes. Esa cifra anterior no es la LN definitiva de junio de 2024, pero hace prioritaria la comprobación de los tres valores 750 del archivo IEEG y del reparto SICEE 563 × 4 contra el listado final. No se sobrescribe ninguno.

## Cotejo por sección de los 28 grupos prioritarios

Todas las 28 secciones conservan una diferencia de LN al sumar **todas** sus casillas; ninguna se cancela solo por redistribución interna. Se incluyen también las casillas de esa sección cuya diferencia individual era de cinco o menos. El Δ agregado de estos grupos es −6,492; la cifra no equivale al Δ municipal total, que incluye las demás secciones y las especiales.

| Municipio | Sección | Casillas | LN IEEG CAS | LN SICEE CAS | Δ LN |
|---|---:|---:|---:|---:|---:|
| CORTAZAR | 697 | 3 | 1,684 | 2,243 | -559 |
| CORTAZAR | 715 | 1 | 721 | 727 | -6 |
| JARAL DEL PROGRESO | 1195 | 2 | 1,001 | 1,499 | -498 |
| LEON | 1349 | 6 | 3,855 | 4,495 | -640 |
| LEON | 1514 | 1 | 473 | 467 | +6 |
| LEON | 1515 | 1 | 606 | 597 | +9 |
| LEON | 1527 | 1 | 557 | 550 | +7 |
| LEON | 1591 | 3 | 1,689 | 2,249 | -560 |
| LEON | 1677 | 6 | 3,858 | 4,494 | -636 |
| LEON | 1702 | 2 | 1,456 | 1,444 | +12 |
| LEON | 1705 | 2 | 879 | 867 | +12 |
| LEON | 1805 | 1 | 680 | 672 | +8 |
| LEON | 3043 | 1 | 648 | 640 | +8 |
| LEON | 3094 | 1 | 375 | 748 | -373 |
| LEON | 3139 | 2 | 996 | 1,497 | -501 |
| LEON | 3188 | 4 | 2,612 | 2,584 | +28 |
| SALVATIERRA | 2297 | 2 | 1,439 | 1,450 | -11 |
| SALVATIERRA | 2303 | 1 | 717 | 724 | -7 |
| SALVATIERRA | 2338 | 2 | 1,001 | 1,499 | -498 |
| SAN FELIPE | 2409 | 4 | 2,813 | 2,252 | +561 |
| URIANGATO | 2797 | 2 | 1,000 | 1,500 | -500 |
| VALLE DE SANTIAGO | 2839 | 2 | 1,000 | 1,500 | -500 |
| VALLE DE SANTIAGO | 2869 | 3 | 1,305 | 1,679 | -374 |
| VALLE DE SANTIAGO | 2887 | 2 | 878 | 1,250 | -372 |
| VICTORIA | 2892 | 3 | 1,683 | 2,245 | -562 |
| VICTORIA | 2903 | 3 | 1,686 | 2,246 | -560 |
| YURIRIA | 2970 | 1 | 732 | 724 | +8 |
| YURIRIA | 2978 | 1 | 584 | 578 | +6 |

## Control cruzado con otras elecciones del 2 de junio de 2024

Se cotejaron las **58 casillas B/C/E** del anexo, identificadas por municipio, sección, tipo, número y extensión, contra los CSV de casilla de **Gubernatura GTO 2024** (`2024_SEE_GOB_GTO_CAS.csv`, ZIP SICEE GTO citado arriba) y **Presidencia 2024** (`2024_SEE_PRE_NAL_CAS.csv`, ZIP `INE_SICEE_P_2024_original.zip`, SHA-256 `3122304d4dec2a24168708af9836f5df2860ac4347163dc311473bd037737bbf`). Las 58 claves aparecen una sola vez en cada serie y cubren 28 secciones de nueve municipios.

| Control de LN en las 58 casillas | Casillas |
|---|---:|
| SICEE Ayuntamientos = SICEE Gubernatura = SICEE Presidencia | 58 |
| IEEG Ayuntamientos = SICEE Gubernatura | 0 |
| IEEG Ayuntamientos = SICEE Presidencia | 0 |

En San Felipe 2409, las cuatro casillas B/C1/C2/C3 registran LN 563 también en Gubernatura y Presidencia SICEE; Ayuntamientos IEEG registra 750/750/750/563. **Control ampliado:** los CSV IEEG de Gubernatura y Diputaciones locales del mismo paquete de cómputos del 09/06/2024 repiten exactamente la LN de Ayuntamientos IEEG en las 58 casillas; ninguno de esos valores coincide con SICEE en ellas. En San Felipe 2409 las tres series IEEG registran 750/750/750/563. La divergencia es, por tanto, **entre los paquetes IEEG y SICEE**, no exclusiva del archivo IEEG Ayuntamientos. Las series de una misma institución pueden compartir el origen o procesamiento de LN; esta concordancia interna no adjudica cuál valor es el definitivo. Antes de corregir la fuente maestra se necesita el listado final por casilla o documentación oficial equivalente, y el análisis judicial municipal pendiente continúa abierto.

Se amplió el cruce a **todas las 4,642 casillas ordinarias B/C/E** de los 28 municipios presentes en SICEE Ayuntamientos. Las mismas 4,642 claves aparecen en Gubernatura y Presidencia SICEE 2024; en **4,642/4,642** la LN coincide exactamente entre las tres series. Este universo comprende las 3,037 casillas B/C/E cuya LN difiere entre IEEG y SICEE Ayuntamientos y otras 1,605 sin esa diferencia. Quedan fuera las 21 casillas especiales S y 16 de voto anticipado VA por sus reglas de identificación y LN distintas. La coincidencia intrafuente no resuelve por sí sola la divergencia con IEEG.

En las **mismas 4,642 casillas**, los CSV IEEG de Ayuntamientos, Gubernatura y Diputaciones locales (paquetes internos `09062024_1200_COMPUTOS_AYUN_GTO.zip`, `09062024_1200_COMPUTOS_GUB_GTO.zip` y `09062024_1200_COMPUTOS_DIP_LOC_GTO.zip` del ZIP IEEG citado al inicio) registran **4,642/4,642 LN iguales entre sí**. Las dos familias coinciden en 1,605 casillas y difieren en **3,037**, siempre con consistencia interna en cada familia. Este control corrige cualquier interpretación anterior de que la diferencia fuese exclusiva de Ayuntamientos IEEG. Tampoco permite elegir la LN definitiva sin una fuente nominal independiente de ambos paquetes.

La publicación del INE sobre la entrega de la LN definitiva en Guanajuato confirma el total estatal de **4,831,142** personas y la entrega a los consejos distritales en abril de 2024 (https://centralelectoral.ine.mx/2024/04/21/entrega-ine-guanajuato-listas-nominales-de-electores-definitivas-a-15-consejos-distritales/). Esa numeralia estatal no identifica el valor por casilla de los casos anteriores, por lo que no se utiliza para adjudicar las diferencias.
