# HEYTI — Verificación del manifiesto seccional v0.1

**26 de septiembre de 2026.** Generado con `HEYTI_Generar_Manifiesto_23_Series_v0_1.py` a partir de los 15 ZIP originales presentes en la copia de trabajo. Cada ZIP pasó prueba CRC; el manifiesto contiene SHA-256 del ZIP y CSV, ruta exacta, codificación, cabecera, tipo de elección y modalidad. No hubo escritura en PostgreSQL.

| Medida | Conteo |
|---|---:|
| ZIP originales | 15 |
| CSV a nivel sección | 23 |
| Filas físicas en esos 23 CSV (incluye otros estados en fuentes federales) | 863,286 |
| Filas cuyo `ID_ESTADO` es Guanajuato (11) | 73,262 |
| Filas GTO con sección numérica 1–8999 | 73,125 |
| Filas GTO con `SECCION=0` | 137 |
| Filas GTO con sección numérica ≥9000 o clave no numérica | 0 |

El conteo 73,125 **suma 23 series**, por lo que una misma sección aparece más de una vez entre elecciones y modalidades. Por ejemplo, DF 2021 MR y RP contienen 3,159 secciones ordinarias cada uno y 15 filas `SECCION=0` cada uno; A 2024 tiene 3,233 ordinarias y 24 filas `SECCION=0`. Las 137 filas de sección 0 requieren identidad propia por elección, municipio, distrito y acta; este conteo no prueba su significado individual. Las actas VA/MEC con claves 9000+ pueden existir en archivos de casilla aunque no figuren como `SECCION>=9000` en estos CSV agregados.

El manifiesto fija modalidad por ruta explícita: 2018/2021/2024 DF MR/RP; 2018/2021/2024 DL MR/RP cuando existen; 2018/2024 S MR/RP; A/G/P se registran `UNICA` en estos CSV. Esa etiqueta describe el archivo, no resuelve todas las reglas jurídicas de candidatura. Fechas de publicación, URL oficial y corte certificado siguen pendientes; se registran como desconocidos.

**Validación pendiente:** cotejar las 23 rutas con el inventario auditado del repositorio, verificar versiones publicadas de cada fuente, definir identidad de sección 0, revisar reglas de cómputo antes de cargar y probar el DDL en PostgreSQL aislado. Este inventario no autoriza publicar resultados ni sustituir los JSON actuales.
