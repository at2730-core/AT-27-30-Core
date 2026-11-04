# HEYTI — Segundo grupo de seis municipios A2024

Consolidación: 15 de octubre de 2026 (America/Mexico_City). Evidencia: salidas PostgreSQL ejecutadas por Alex los días 4 y 15 de octubre. Base aislada: heyti_cas_full_probe_d12d6718adb8. Fuente release 10, serie A2024 UNICA 16. Consultas con transacción y ROLLBACK; sin selección ni certificación ni escritura de resultados.

## Cotejo interno comprobado

| ID | Municipio | CAS | SEC | Total CAS=SEC | Cotejos votos | Cotejos LN |
|---|---|---:|---:|---:|---:|---:|
|16|Huanímaro|31|13|10994|234|13|
|23|Pénjamo|235|113|63110|2034|113|
|29|San Diego de la Unión|55|28|18629|504|28|
|35|Santa Cruz de Juventino Rosas|108|36|40092|648|36|
|36|Santiago Maravatío|13|10|4535|180|10|
|38|Tarandacuao|20|12|6303|216|12|

Total 462 CAS, 212 SEC, 3816 comparaciones de votos (18 campos por sección) y 212 de LN. Cero cobertura inválida, cero valores no numéricos y cero diferencias en los filtros ejecutados. Sin SEC0 en estas seis series municipales. Sin marcas TRIBUNAL en las filas inspeccionadas; su ausencia no demuestra inexistencia de impugnaciones. La LN sumada conserva la codificación de la fuente, sin asignar significado de padrón ordinario a casillas especiales.

## Controles documentales externos comprobados

- Huanímaro: PAN 2839, PRI 31, PRD 2673, PVEM 3364, MC 250, MORENA 1537, no registrados 0, nulos 300 y total 10994. Nueve controles coincidentes; tabla PDF página 3, impresa 2, TEEG-REV-41/2024.
- Pénjamo: PAN 23634, PRI 4576, PVEM 1629, PT 831, MC 2588, MORENA 26660. Seis controles coincidentes sobre 113 filas SEC; tabla PDF página 4, impresa 3, TEEG-REV-48/2024. No inferir nulos ni no registrados por diferencia con total municipal 63110.
- San Diego: PAN 1671, PRI 7657, PRD 49, PVEM 2183, PT 314, MC 461, MORENA 5599, no registrados 0, nulos 695, total 18629. Diez controles coincidentes; SM-JRC-254/2024 y SM-JRC-328/2024 acumulado.
- Juventino Rosas: PAN 7100, PRI 528, PRD 8559, PVEM 2135, PT 660, MORENA 5375, no registrados 4, nulos 1556 y total 40092. Nueve controles coincidentes; SM-JDC-482/2024 y acumulado. CAND_IND_3 suma 14175 y CAND_IND_1/2 cero: coincidencia numérica con Fidel Armando Ruiz Ramírez, pendiente identificación formal de columna; no contar como décimo control de identidad aprobado.
- Tarandacuao: PAN 2322, PRI 2102, PVEM 320, PT 119, MC 61, MORENA 1145, no registrados 1, nulos 233. Ocho rubros coincidentes; TEEG-REV-39/2024, PDF página 4, impresa 3. Suma 6303, igual al total interno; no contar total como noveno rubro independiente de la tabla.
- Santiago Maravatío: acta IEEG/014/2024, página 4, enumera 13 casillas. Sumas PAN 2316, PRI 38, MC 15, MORENA 2055, no registrados 0, nulos 111, total 4535. Siete controles coincidentes con 10 filas SEC. Las 13 filas transcritas cuadran individualmente en sus componentes. El cotejo ejecutado es municipal agregado, no cotejo DB por cada una de las 13 claves de casilla.

Balance: 42 controles de tablas reproducidas en sentencias y siete controles agregados de acta IEEG. No son 49 campos distintos por sección ni certificación electoral.

## Corrección y controles descartados

El bloque inicial de Santiago Maravatío y Tarandacuao contenía errores del asistente en cifras, etiquetas y atribución documental. No es evidencia de error en staging. Queda invalidado como control externo. Para Tarandacuao se releyó la tabla original y se aprovechó únicamente la salida observada contra los valores corregidos, más consulta separada PRI=2102. Para Santiago se sustituyó el control por lectura de acta oficial y consulta nueva de siete rubros. No se modificó la base para hacerla coincidir.

## Recurso posterior localizado el 15 de octubre

SUP-REC-13760/2024 y SUP-REC-13769/2024 acumulado, fallo definitivo de 11/09/2024: desecha las demandas contra SM-JDC-482/2024 y SM-JDC-513/2024 (Juventino Rosas). Trata asignación de regidurías; la cadena distingue confirmación del cómputo de modificaciones a integración. No se localizó una orden de modificación de cifras en esta resolución. El desechamiento no equivale a nuevo estudio de fondo del vector. Se descartó el proyecto con fecha asteriscada y se leyó la versión definitiva.

Búsquedas por TEEG-REV-48/2024, TEEG-REV-41/2024, TEEG-REV-39/2024, SM-JRC-254/2024, SM-JRC-303/2024 y SUP-REC no localizaron otros fallos posteriores pertinentes en los resultados consultados. Esto no acredita su inexistencia ni cierra el inventario judicial de los cinco municipios restantes.

## Fuentes oficiales

- Huanímaro: https://oficialiapartes.congresogto.gob.mx/Files/294999/Exp294999-LXV-8162020240709105036.pdf
- Pénjamo: https://oficialiapartes.congresogto.gob.mx/Files/294998/Exp294998-LXV-8161920240709104405.pdf
- San Diego: https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JRC-0254-2024.pdf
- Juventino Rosas regional: https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JDC-0482-2024-
- Juventino Rosas superior definitivo: https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SUP-REC-13760-2024
- Tarandacuao: https://oficialiapartes.congresogto.gob.mx/Files/294518/Exp294518-LXV-8113920240628155154.pdf
- Santiago local: https://oficialiapartes.congresogto.gob.mx/Files/295825/Exp295825-LXV-8243920240729125626.pdf
- Santiago federal: https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JRC-0303-2024-
- Santiago acta: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmsm-acta-14.pdf

## Pendientes y punto de retorno

Conservar los bloqueos de selección/presentación. Completar inventario de recursos posteriores; verificar fechas/cortes y vincular evidencia con hashes antes de cualquier propuesta de selección. Identificar formalmente CAND_IND_3 de Juventino Rosas. El acta de Santiago permite como siguiente control cotejar las 13 claves CAS y sus siete campos, sin repetir el agregado ya aprobado. Consolidar estas referencias en el registro maestro mediante edición controlada; este reporte no afirma que dicho registro ya haya sido actualizado.

Primer y segundo grupo juntos: 11124 cotejos internos de votos y 618 de LN concordantes. Estos conteos describen únicamente los doce municipios ensayados en ambos grupos y no cierran la auditoría de los 46 municipios ni de las 23 series.
