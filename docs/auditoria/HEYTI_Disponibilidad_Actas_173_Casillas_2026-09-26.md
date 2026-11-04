# HEYTI — Disponibilidad de actas para 173 casillas con vacíos

**26 de septiembre de 2026.** Inventario local de 15 ZIP INE/SICEE y dos ZIP IEEG de cómputos 2021/2024, incluidos sus ZIP anidados. Se cotejó con `HEYTI_Casillas_Con_Vacios_SEC_Numerico_23_Series_2026-09-26.csv`. No se consultó ni modificó PostgreSQL.

| Estado | Casillas de serie |
|---|---:|
| Total con alguna columna vacía y SEC numérico | 173 |
| Con `RUTA_ACTA` consignada en CAS | 79 |
| Sin `RUTA_ACTA` consignada | 94 |
| Imagen/PDF de acta contenida en los ZIP aportados | 0 |

Los 15 ZIP SICEE contienen CSV y XLSX, sin imágenes/PDF de acta. Los cinco ZIP internos del IEEG contienen CSV únicamente. `RUTA_ACTA` es una referencia de nombre; no indica por sí sola que el archivo esté disponible en el paquete. Se identifican 18 registros con estatus `Paquete no entregado`/`PAQUETE NO ENTREGADO`, sin inferir que todas las columnas vacías tengan la misma causa.

**Ruta de revisión externa:** el manual oficial de SICEE explica que las consultas federales incluyen detalle por acta de casilla y que la imagen PDF puede descargarse desde la información contextual **cuando está disponible**. Referencia: https://sicee.ine.mx/assets/media/Manual_de%20_Usuario_SICEE25.pdf (pp. 5 y 18 del PDF, según numeración del documento). La consulta caso por caso debe anotar URL/identificador, fecha, hash del PDF, columna revisada, valor literal y resolución del caso. Para las series locales, localizar el repositorio institucional de actas IEEG pertinente; estos ZIP no lo incluyen.

**Estado:** no se cierran las 1,160 comparaciones sólo porque SEC coincida con la suma de los números CAS disponibles. Sin imagen o explicación oficial del vacío, permanecerán como `no_determinado`. Los 27 campos de A 2021 anulados y dos celdas `CAND_IND1` con SEC vacío constan en el expediente separado.
