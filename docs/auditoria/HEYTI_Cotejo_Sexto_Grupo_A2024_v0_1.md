# HEYTI — Balance del sexto grupo municipal A2024
Fecha de corte de esta nota: 2026-10-23.
Estado: cotejos parciales documentados; SIN CERTIFICACIÓN ni selección de corte.

## Alcance y entorno
Serie 16, release 10. Base aislada usada por Alex: heyti_cas_full_probe_d12d6718adb8.
Fuentes crudas: GTO_PEL_2024/AYUNTAMIENTOS_csv/2024_SEE_AYUN_GTO_CAS.csv y 2024_SEE_AYUN_GTO_SEC.csv.
Evidencia de ejecución: salidas psql compartidas en esta conversación. Consultas de lectura cerradas con ROLLBACK. Esta nota no constituye una nueva ejecución independiente ni escritura en PostgreSQL.

## Conciliación interna previamente ejecutada
|Municipio|ID|CAS|SEC|Votos CAS|Votos SEC|Lista nominal CAS = SEC|
|---|---:|---:|---:|---:|---:|---:|
|Romita|26|95|50|30035|30035|50586|
|Salvatierra|28|160|85|44717|44717|86884|
|San Felipe|30|157|72|45422|45422|89275|
|San José Iturbide|32|114|39|38858|38858|68729|
|San Luis de la Paz|33|162|58|53271|53271|98821|
|Silao de la Victoria|37|248|79|78492|75031|153531|

383 unidades seccionales, incluidas cuatro SEC0; 6894 cotejos de votos (18 campos por unidad) y 383 de lista nominal, con cobertura válida, sin valores no numéricos ni discordancias en los controles ejecutados.
En Silao se excluyó la votación de las casillas marcadas ANULADA para conciliar votos; su lista nominal se conservó. Once casillas marcadas suman 3461 votos: 78492 − 3461 = 75031.

## Cotejo documental externo
|Municipio|Resultado observado|Pendientes|
|---|---|---|
|Romita|63 casillas × 8 campos = 504 controles: 484 coinciden y 20 difieren. Una casilla adicional, 2085 B, tiene siete coincidencias parciales.|28 casillas sin cotejo documental registrado; tres rótulos pendientes; PVEM de 2085 B; aclarar 20 diferencias en siete casillas; revisión jurisdiccional sin cierre.|
|Salvatierra|Ocho controles municipales coinciden con la tabla documental consultada: PAN 11024, PRI 1633, PVEM 2083, PT 863, MC 1814, MORENA 24969, no registrados 71 y nulos 2260.|La tabla no acredita las columnas omitidas ni un total expresamente declarado; revisión de cadena posterior pendiente.|
|San Felipe|156 casillas × 14 campos = 2184 coincidencias. Fila especial: 14 coincidencias numéricas adicionales.|Acreditar equivalencia 9037 A01 del acta con SEC0 / VA02 del CSV; columnas omitidas y cierre jurisdiccional pendientes.|
|San José Iturbide|114 casillas × 9 campos = 1026 coincidencias.|Columnas omitidas por la tabla y cierre de revisión jurisdiccional.|
|San Luis de la Paz|160 casillas × 11 = 1760 coincidencias, diez más en 2587 C03 y once en la fila especial: 1781 coincidencias numéricas.|MC de 2587 C03 con marca documental; equivalencia 9039 A01 con SEC0 / VA38; columnas omitidas y cierre jurisdiccional.|
|Silao de la Victoria|14 controles del vector rectificado coinciden. Once identidades de casillas anuladas coinciden con los controles: una local y diez regionales.|Comprobar cadena posterior y gobernanza del corte; no hay selección ni certificación autorizada por estos cotejos.|

Las casillas especiales S incluidas en las tablas se conservaron con su tipo. Los conteos de casillas cotejadas no significan cotejo de todas las columnas existentes en el CSV.

## Romita: diferencias abiertas
|Casilla|Control acta → CSV|
|---|---|
|2065 C01|PRI 82 → 83; PVEM 22 → 24; MORENA 77 → 78; nulos 13 → 9|
|2069 C01|PAN 191 → 188; MORENA 98 → 96; nulos 6 → 9; total 398 → 396|
|2070 B|PAN 225 → 230; PVEM 23 → 22; total 447 → 451|
|2070 C01|PAN 210 → 209; nulos 15 → 16|
|2074 C02|nulos 8 → 9; total 290 → 291|
|2079 B|PAN 179 → 176; PRI 103 → 102; total 351 → 347|
|2092 C01|MORENA 31 → 32; total 179 → 180|

Rótulos pendientes: acta 2057 C01 frente a posible CSV 2067 C01; acta 2058 B01 y C01 frente a posibles CSV 2068 B y C01. No se aprobó equivalencia por similitud de vectores.
2085 B: PVEM tiene una marca delante de 19; CSV registra 19. Otros siete campos coinciden.
Las 28 referencias pendientes tienen una fila fuente cada una, hash identificado, ESTATUS_ACTA Grupo de Recuento y campos RUTA_ACTA, OBSERVACIONES y TRIBUNAL vacíos. Eso no explica por sí solo las diferencias ni demuestra inexistencia de constancias.

## Identidades especiales
San Felipe: CAS línea 6515, SEC0 / VA02, ID_CASILLA 2, total 1, MORENA 1, LN 1.
Hash: f1ee1a56ca1f63052bbf34c56405bdc580b575bca998d380194f147c6d7e4390.
Unidad SPECIAL_SECTION_ROW, sección 0, distrito local 1, sin territorial_section_id.

San Luis de la Paz: CAS línea 6954, SEC0 / VA38, ID_CASILLA 38, PVEM 1, MORENA 3, total 4, LN 6.
Hash: a57479229f404951cff63f76482a738c81687db8128efb307384dedf9775f902.
Unidad SPECIAL_SECTION_ROW, sección 0, distrito local 2, sin territorial_section_id.

San Luis de la Paz 2587 C03: línea 7068, CSV MC 27, total 354, estatus Acta Casilla, sin ruta ni observaciones.
Hash: 5b113c92c70ed470c64bf96691251809230fbc0207897b1475b051ee1cfa721d.
El literal marcado de MC no se convirtió en un control numérico aprobado.

## Correcciones de transcripción del cotejo
San Felipe: 2377 C02 total se corrigió de 358 a 336; 2378 B PVEM de 68 a 58; 2400 B PVEM de 125 a 129; 2401 C01 PVEM de 172 a 177.
Se ampliaron imágenes y se repitieron las consultas, con cero discordancias. No son incidencias de las fuentes. El archivo local del primer bloque de distribución fue inspeccionado por Alex y contiene PVEM 58.

## Fuentes documentales consultadas
- Romita acta 16/2024: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmro-acta-16.pdf
- Salvatierra TEEG-REV-52/2024, resolución de desechamiento por extemporaneidad, sin resolución de fondo: https://oficialiapartes.congresogto.gob.mx/Files/294025/Exp294025-LXV-8064620240620162802.pdf
- San Felipe CMSF/018/2024: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmsf-acta-18.pdf
- San José Iturbide acta 16/2024: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmsj-acta-16.pdf
- San Luis de la Paz acta 15/2024: https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cmsl-acta-15.pdf
- Silao CGIEEG/186/2024: https://oficialiapartes.congresogto.gob.mx/Files/299929/Exp299929-LXVI-32520241002150924.pdf
- Cadena identificada en Silao: TEEG-REV-34/2024 y acumulado 49/2024; SM-JRC-262/2024.

Las búsquedas efectuadas para Romita, San Felipe, San José Iturbide y San Luis de la Paz no localizaron en esta sesión sentencias que modifiquen esos cómputos municipales. Es un resultado limitado de búsqueda, no prueba de inexistencia ni firmeza. Los asuntos de candidaturas y de diputaciones distritales no se usaron para cerrar ayuntamientos.

## Punto de continuación
Sexto grupo con conciliación interna ejecutada y cotejo externo parcial documentado. Permanecen los pendientes descritos; no declarar municipios certificados.
Continuar con inventario global de pendientes y siguientes municipios, sin repetir los bloques aprobados salvo nueva evidencia o cambios. Conservar originales, marcas ANULADA, NULL/cero e identidades especiales.
