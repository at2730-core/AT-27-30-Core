# HEYTI — Identidad preliminar de `SECCION=0` en 23 series

**26 de septiembre de 2026.** Cotejo estático de los CSV `*_SEC.csv` y `*_CAS.csv` en los 15 ZIP; únicamente `ID_ESTADO=11`. No se modificó ninguna fuente ni PostgreSQL. `TIPO_CASILLA` y `ACTA_CASILLA-MEC` se reportan literalmente; la denominación jurídica definitiva requiere corroboración documental.

| Año | Elección/modalidad | Filas SEC=0 | Filas CAS=0 | Patrón literal CAS | Identidad mínima observada en SEC |
|---|---|---:|---:|---|---|
| 2021 | DF MR | 15 | 15 | `TIPO_CASILLA=P` | Distrito federal: 15 valores distintos; municipio 0. |
| 2021 | DF RP | 15 | 15 | `TIPO_CASILLA=P` | Distrito federal: 15 valores distintos; municipio 0. |
| 2018 | G | 1 | 16 | `TIPO_CASILLA=MEC` | Municipio 0, `VOTO EN EL EXTRANJERO`; agregación de casillas. |
| 2024 | A | 24 | 24 | `TIPO_CASILLA=A`, actas `VA*` | Municipio distinto por fila; 14 distritos locales representados. |
| 2024 | DL MR | 25 | 25 | `TIPO_CASILLA=A`, actas `VA*` | Par distrito local/municipio; 21 distritos, 18 municipios. |
| 2024 | DL RP | 25 | 25 | `TIPO_CASILLA=A`, actas `VA*` | Par distrito local/municipio; 21 distritos, 18 municipios. |
| 2024 | G | 26 | 32 | 25 `A`/`VA*` y 7 `MEC` | 25 pares distrito/municipio más un agregado extranjero de municipio 0. |
| 2018 | P | 1 | 16 | `MEC` | Municipio 0, extranjero. |
| 2024 | P | 1 | 7 | `MEC`, prefijos `VM`/`Ve` | Distrito y municipio 0, extranjero. |
| 2018 | S MR | 1 | 16 | `MEC` | Municipio 0, extranjero. |
| 2024 | S MR | 1 | 7 | `MEC`, prefijos `VM`/`Ve` | Distrito y municipio 0, extranjero. |
| 2018 | S RP | 1 | 16 | `MEC` | Municipio 0, extranjero. |
| 2024 | S RP | 1 | 7 | `MEC`, prefijos `VM`/`Ve` | Distrito y municipio 0, extranjero. |

**Total:** 137 filas `SEC=0` en 13 series. Las otras 10 series no tienen filas `SEC=0`. Dentro de cada serie, la clave candidata `(distrito federal, distrito local, municipio, etiqueta de municipio)` no tiene duplicados entre esas filas; esto es una comprobación de unicidad, no prueba que sea llave suficiente para nuevas fuentes/cortes. La llave física debe incluir además `release_id`, serie, modalidad y la identidad de origen. En casilla debe incluir acta/casilla literal y ordinal de registro; una fila agregada puede corresponder a varias casillas y no se debe sustituir por una de ellas.

**Regla propuesta:** `SECCION=0` nunca se carga como sección ordinaria ni se enlaza por FK a `territorial.section`. Representar las filas extranjeras como `SPECIAL_AGGREGATE`, las filas VA/P como `SPECIAL_SECTION_ROW` hasta establecer su definición oficial y las casillas de origen en `acta_evidence`. Mantener `TOTAL_VOTOS` y `LISTA_NOMINAL` publicados en la fila agregada; no sumar CAS por defecto, ya que puede haber reglas judiciales o de cómputo distintas. Validar por opción y acta antes de certificar.

**Límite:** este cruce solo usó los miembros seccional y de casilla emparejados por nombre; aún no acredita descripción oficial de `P`, `VA`, `VM`, `Ve` ni la conciliación numérica acta→sección. Tampoco cubre otras unidades especiales existentes solo en archivos de casilla.
