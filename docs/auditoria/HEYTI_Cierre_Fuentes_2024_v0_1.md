# HEYTI — Cierre de revisión de fuentes 2024, Guanajuato

Fecha de consolidación: 26 de octubre de 2026. Versión 0.1.

## Dictamen de alcance

Se consolida el cierre documental de la revisión de fuentes 2024 con reservas. Comprende nueve series: Ayuntamientos, Diputaciones locales MR/RP, Gubernatura, Presidencia, Senado MR/RP y Diputaciones federales MR/RP, exclusivamente Guanajuato. El expediente permite terminar la ronda general de inspección de fuentes y pasar a decisiones de integración por alcance y métrica. No declara que todos los resultados sean definitivos, que todas las actas hayan sido cotejadas individualmente ni que exista una fuente seleccionada en producción.

Este documento sintetiza reportes existentes y salidas PostgreSQL compartidas por el usuario. No ejecuta nuevas pruebas de base de datos ni una búsqueda judicial actualizada. Las reservas permanecen abiertas y trazables; su cierre requiere evidencia específica, no repetir el recorrido general de casillas. La aprobación técnica de una carga y su consistencia interna no sustituyen la adjudicación de una fuente.

## Matriz de las nueve series

Estados de revisión: CERRADA CON RESERVAS. Uso propuesto: análisis del corte publicado identificado, limitado a campos comprobados. No es una autorización de publicación o selección automática. En todos los casos se conservan originales, hashes y modalidad.

| Serie | Evidencia disponible | Uso analítico propuesto y reserva principal |
|---|---|---|
| Presidencia | 8,168 CAS → 3,234 SEC; SEC → 16 DIS, 47 MUN y ENT: cinco campos coinciden. Comparación externa de TOTAL_VOTOS y LN: 8,103 ordinarias y 65 no ordinarias coinciden con cómputos federales. | Corte publicado identificable; ENT total 2,759,092. Distinguir extranjero, MEC, A y P. Los cinco campos agregados no acreditan cotejo externo exhaustivo de cada opción partidista. |
| Senado MR | 8,166 CAS → 3,234 SEC; DIS/MUN/ENT concilian cinco campos. Comparación externa de total y LN en 8,103 ordinarias y 63 no ordinarias. | Analizar MR por separado. Conservar siete identidades MEC dentro de SEC0; no sumar MR y RP. No se certifica firmeza jurídica universal. |
| Senado RP | 8,207 CAS → 3,234 SEC; MUN concilia; 16 DISPP y ENTPP concilian cinco campos. Siete columnas de partido ENTPP = suma DISPP. Comparación externa total/LN: 8,103 + 104 filas. | Distribución por partido DISPP/ENTPP separada de opciones crudas SEC. RP incluye MR más 41 SRP; no duplicar. |
| Diputaciones federales MR | 8,159 CAS → 3,233 SEC. Once anuladas explican 3,778 votos en diez secciones; LN se conserva. SEC → 15 DIS, 46 MUN y ENT concilia. Cuatro distritos afectados tienen 72 cotejos documentales concordantes. | Usar SEC del corte con exclusiones ya incorporadas; no restar nuevamente 3,778. Conservar alcance judicial de D10/12/14/15; no presentarlo como certificación universal de firmeza. |
| Diputaciones federales RP | 8,200 CAS → 3,233 SEC y MUN concilian. 15 DISPP y ENTPP concilian cinco campos y siete columnas partidistas agregadas. | Mantener los votos y metadatos RP tal como se publicaron. No trasladar anulaciones MR automáticamente. CIR nacional queda fuera del cierre Guanajuato por estado. |
| Diputaciones locales MR | 8,169 CAS → 3,258 SEC y agregados DIS/MUN concilian cinco campos. 8,103 ordinarias coinciden en total con IEEG; 21 agrupamientos distritales A coinciden en total y LN. | Corte SICEE con reserva de LN e identidad especial. La igualdad de totales no acredita toda la distribución partidista externa. |
| Diputaciones locales RP | 8,210 CAS → 3,258 SEC concilian cinco campos. Incluye cobertura MR y 41 SRP; 8,103 ordinarias coinciden en total con IEEG. | Separar modalidad y especiales SMR/SRP. No sumar ambas coberturas. No declarar comprobados agregados RP que no constan en los cotejos citados. |
| Gubernatura | 8,176 CAS → 3,259 SEC y agregados DIS/MUN concilian cinco campos. 8,103 ordinarias coinciden en total con IEEG; canales especiales identificados. | Analizar el corte publicado señalando la diferencia estatal de dos votos nulos: SICEE 2,721,628 frente a IEEG 2,721,630. Bloqueada la etiqueta de total estatal único definitivo hasta adjudicar corte/canal VA D22. |
| Ayuntamientos | Recorrido de 46 municipios; 3,257 SEC, 58,626 cotejos de campos de votos y 3,257 de LN sin discordancia interna tras tratamiento de anuladas. Evidencia documental de profundidad desigual por municipio. | Análisis por corte y municipio con reservas del registro de 46. Bloqueada la presentación de un resultado estatal homogéneo definitivo. No confundir concordancia interna con actas individuales completamente verificadas. |

Los cinco campos de los cotejos de agregación son NUM_VOTOS_VALIDOS, NUM_VOTOS_CAN_NREG, NUM_VOTOS_NULOS, TOTAL_VOTOS y LISTA_NOMINAL. No deben sumarse votos válidos otra vez a los componentes partidistas.

## Reservas que sobreviven al cierre

| Reserva | Evidencia y consecuencia concreta |
|---|---|
| Fecha de publicación y selección | Los registros técnicos conservan fecha de publicación no verificada y selección pendiente. Fechas de sentencia, descarga o generación no sustituyen published_at. Identificar siempre paquete/corte; no anunciar “último resultado oficial” por inferencia. |
| Lista nominal local | En las 8,103 ordinarias, 2,830 LN IEEG/SICEE coinciden y 5,273 difieren; el cotejo federal respalda numéricamente la LN SICEE. No mezclar denominadores IEEG con numeradores SICEE ni convertir especiales LN=0/1000 en padrón ordinario. |
| SEC0 e identidades | Preservar SPECIAL_SECTION_ROW sin territorial_section_id. Igualdad de votos no prueba equivalencia formal entre rótulos 90xx A01 y VAxx. No georreferenciar ni crear genealogía por esos empates. |
| Gubernatura VA D22 | Acta IEEG revisada: PAN 1, combinación PVEM_PT_MORENA 1, nulos 2, total 4; SICEE total 2 y nulos 0. El acta corrobora el vector IEEG; no explica por sí sola la transformación posterior o equivalencia formal. No corregir raw ni escoger silenciosamente un total. |
| San Miguel de Allende | SEC local 75,386; restituciones 156 C1, 172 B, 191 B y 200 E1 suman 1,371; derivado 76,757. Ensayo temporal de 106 unidades y 1,802 celdas pasó y terminó ROLLBACK. Candidato reproducido, no instalado ni seleccionado. Mantener excluidas las otras cuatro anuladas; no aplicar regla a los otros municipios. |
| Salamanca | 2110 C2: PRI_PRD documental final 0 frente a CSV 1; tabla final suma 464 pero declara 465, CSV suma y declara 465. No adjudicar el voto. 2163 C2: una celda PRI_PRD de lectura pendiente excluida del cotejo, no convertida en cero. |
| León | Consistencia interna de 2,086 CAS y 778 SEC; acta disponible incompleta, sin reversos. No afirmar cotejo documental integral ni transformar NP/Sin Dato en cero. |
| Otros municipios | Conservar reservas de Romita, Doctor Mora, Pueblo Nuevo, Villagrán y las restantes del registro municipal. En San Luis de la Paz 2587 C3, lectura MC pendiente; diez campos concordantes no cierran el undécimo. Celdas omitidas o parciales no equivalen a ceros. |
| Legado y aplicación | Copias antiguas o divergentes no se vuelven válidas por este cierre. La migración, lector, selección del corte y pantalla requieren validación independiente. Mantener NO_RELEASE_SELECTED donde no exista política explícita aprobada. |

## Qué termina y qué sigue

Termina la revisión general de fuentes 2024 con el alcance comprobado arriba y sus excepciones registradas. No se requiere otra ronda general casilla por casilla para producir este cierre. Las investigaciones pendientes se acotan a las reservas y a las decisiones de uso que realmente necesiten resolverlas.

La siguiente fase es integración controlada: implementar una política de fuente por serie, territorio y métrica; excluir o advertir los alcances reservados; verificar de fuente a staging, lector y pantalla; y, sólo con autorización separada, seleccionar/publicar. No se ha cambiado la base viva ni certificado resultados. 2018 y 2021 no quedan cerrados por este documento.

## Índice de evidencia

Reportes consultados; sus fechas de prueba se mantienen y no se presentan como ejecuciones del 26 de octubre:

- Cotejo Federal 2024 GTO 5 Series; Presidencia CAS–SEC y SEC–DIS–MUN–ENT; Senado CAS–SEC MR/RP y niveles MR/RP; Diputaciones federales MR CAS–SEC 11 anuladas y niveles MR/RP; RP federal DISPP/ENTPP (29/09/2026).
- Cotejo agrupado de cuatro distritos DF MR 2024: 72 controles documentales y 11 identidades anuladas. El ámbito no equivale a cotejo individual de todas las actas federales.
- Cotejo de niveles locales 2024; cotejo DL RP CAS–SEC 2018/2024; cotejo DL MR/RP y LN 2024; Gubernatura 2024 LN y canales; Matriz de cierre v0.4 con corroboración documental VA D22.
- Vector restituido San Miguel A2024 v0.1, actualización del 03/10/2026: derivación temporal y cadena judicial identificada. Las búsquedas descritas en ese reporte no prueban inexistencia absoluta de otro acto.
- Registro Municipal A2024 46 v0.1, consolidación 26/10/2026; Cotejo Octavo Grupo A2024 v0.1; Registro Único de Pendientes, actualizado 26/10/2026. Se conserva la historia de cotejos y correcciones de transcripción.
- Checkpoint técnico de 23 series: 461 pruebas y 53 subpruebas reportadas. Es evidencia técnica previa; este cierre no las reejecuta ni las convierte en certificación electoral.

Conclusión de alcance: revisión de fuentes 2024 consolidada y cerrada con reservas; habilitación de resultados definitivos y despliegue pendientes de decisiones e integración explícitas.
