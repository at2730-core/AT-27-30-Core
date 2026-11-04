# HEYTI — Cotejo federal 2024 Guanajuato, cinco series SICEE

Fecha: 29/09/2026. Archivos públicos del INE/SICEE obtenidos de `https://sicee.ine.mx/downloadzip`, selección Federal/2024, y cómputos federales `20240608_2030_COMPUTOS(1).zip` aportados por Alex. Lectura de originales; no modificación de base viva.

## Procedencia reproducible

| Serie | URL ZIP pública SICEE | SHA-256 ZIP | Filas entidad 11 |
|---|---|---|---:|
| Presidencia | https://sicee.ine.mx/ACTASSICEEN2024/download/FEDERALES_2024/PRESIDENCIA_2024.zip | `3122304d4dec2a24168708af9836f5df2860ac4347163dc311473bd037737bbf` | 8,168 |
| Senado MR | https://sicee.ine.mx/ACTASSICEEN2024/download/FEDERALES_2024/SENADUR%C3%8DAS_MR_2024.zip | `bafa39ae21279f229a3892422d8b9fb339160bc92a17c9a3583c92c1154c19cf` | 8,166 |
| Senado RP | https://sicee.ine.mx/ACTASSICEEN2024/download/FEDERALES_2024/SENADUR%C3%8DAS_RP_2024.zip | `2c5d1aee26b9dfd1d188c9c9949d2b8d366c055d5e2a37b1da2a8b0dcc9fafbe` | 8,207 |
| Diputaciones federales MR | https://sicee.ine.mx/ACTASSICEEN2024/download/FEDERALES_2024/DIPUTACIONES_FED_MR_2024.zip | `9da21ef4e7ed7f490d3351c4834c4cea0bff050699d9d4ebf45f902e333cc61c` | 8,159 |
| Diputaciones federales RP | https://sicee.ine.mx/ACTASSICEEN2024/download/FEDERALES_2024/DIPUTACIONES_FED_RP_2024.zip | `57702d9440ee5b7543366bd16b680ff503c96a19c2e969675b2c4522e05605a4` | 8,200 |

## Cotejo por casilla ordinaria

Para cada serie, filtro `ID_ESTADO=11`, tipo B/C/E y llave `SECCION`, `TIPO_CASILLA`, `ID_CASILLA`, `EXT_CONTIGUA`; cómputo federal equivalente por cargo. Las **8,103** claves por serie están presentes una sola vez en cada paquete y coinciden `TOTAL_VOTOS` y `LISTA_NOMINAL` **8,103/8,103**. Los cargos se compararon dentro de su elección; no se compararon votos de Presidencia contra Senado o Diputaciones. La suma LN ordinaria por cargo es **4,831,142**.

## Relación de modalidades

Senado MR (8,166 filas GTO) es subconjunto de Senado RP (8,207): **8,166 filas comunes idénticas en todos los campos**, RP agrega 41 `SRP`. Diputaciones MR (8,159) es subconjunto de RP (8,200), RP agrega 41 `SRP`; los valores numéricos en las 8,159 claves comunes son iguales. Hay **11 diferencias de metadatos** en `TRIBUNAL` y `OBSERVACIONES`: sólo MR marca `ANULADA` en 11 casillas ordinarias, y RP deja esos campos vacíos. No sumar íntegramente MR y RP ni deduplicar borrando esas marcas.

Estas **11 casillas MR** conservan **3,778 votos crudos** en sus filas SICEE y RP, pero la etiqueta MR `ANULADA` remite a cuatro expedientes. Matriz por clave `HEYTI_DL_Federal_2024_11_CAS_Anuladas_MR_v0_1.csv`, SHA-256 `32f6f48957a0cf8bb9550a65bae215c60fde64b29f572abd6ae9caed47133316`.

| Sentencia oficial | Distrito | Casillas cuya votación MR se anuló | Votos crudos SICEE en esas casillas |
|---|---:|---|---:|
| [SM-JIN-80/2024](https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JIN-0080-2024.pdf) | 10 | 2797 C1 | 410 |
| [SM-JIN-41/2024](https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JIN-0041-2024.pdf) | 12 | 364 B1, 398 C1, 451 C1, 530 C2, 536 C3 | 1,600 |
| [SM-JIN-94/2024](https://www.te.gob.mx/sentenciasHTML/convertir/expediente/SM-JIN-0094-2024-) | 14 | 71 C1, 3276 C1 | 613 |
| [SM-JIN-56/2024](https://www.te.gob.mx/media/SentenciasN/pdf/monterrey/SM-JIN-0056-2024.pdf) | 15 | 1058 C1, 3258 B, 3258 C2 | 1,155 |
| **Total** | | **11 casillas** | **3,778** |

Las cuatro sentencias declaran nulidad en esas claves y modifican los cómputos distritales MR correspondientes. La columna de votos suma el archivo crudo SICEE; **no equivale a votos válidos finales de MR ni por sí sola a la resta jurídica final**. Verificar la recomposición distrital y eventuales recursos posteriores antes de fijar un total definitivo. El [acuerdo INE/CG2129/2024 publicado en DOF](https://dof.gob.mx/nota_detalle_popup.php?codigo=5737808) enumera recursos de reconsideración de diputaciones en general, pero no enlaza en ese apartado cada recurso con los cuatro juicios aquí revisados: no se infiere firmeza ni modificación de estas cuatro sentencias a partir de esa lista. El mismo número de votos en RP, cuyos metadatos judiciales están vacíos, no prueba que RP deba recibir igual efecto jurídico. Se preservan ambos registros sin alterar la base viva.

## Tipos no ordinarios

Presidencia SICEE contiene 41 especiales S, 15 A, 7 MEC y 2 P; el cómputo federal PRES registra las mismas 65 filas no ordinarias, pero desglosa MEC en 5 M y 2 V. **Cotejo PRES no ordinario cerrado: 65/65 claves emparejadas sin duplicados; `TOTAL_VOTOS` y `LISTA_NOMINAL` iguales en 65/65.** Clave B/C/E excluida aquí: para S/A/P se usan sección, tipo, número y extensión; para los siete MEC se usa el prefijo de `ACTA_CASILLA-MEC` (`VMRE` postal → M, `VeMRE` electrónico → V) y el número MEC. Los cinco M y dos V tienen sección `0` en SICEE y `4074` en el cómputo; equipararlos sólo por número, sin la identidad de modalidad, produciría colisiones.

Senado SICEE MR contiene 41 SMR, 15 A y 7 MEC (**63**); RP añade 41 SRP (**104**). El cómputo federal SEN muestra 82 S (MR y RP), 15 A, 5 M y 2 V (**104**); `TIPO_ACTA=3EMR` y `3ERP` distingue los dos votos de la misma especial. **SEN MR: 63/63; SEN RP: 104/104 claves emparejadas, cero diferencias en votos totales y LN.** En MR, las 41 SRP adicionales del cómputo corresponden a la serie SICEE RP, y no son faltantes.

Diputaciones SICEE MR contiene 41 SMR y 15 A (**56**); RP añade 41 SRP (**97**). El cómputo federal DIP muestra 82 S y 15 A (**97**); `TIPO_ACTA=4EMR` y `4ERP` distingue las especiales. **DIP MR: 56/56; DIP RP: 97/97 claves emparejadas, cero diferencias en votos totales y LN.** Como en Senado, las 41 SRP del cómputo no pertenecen a la serie MR. Conservar `ACTA_CASILLA-MEC` y `TIPO_ACTA` para evitar colisiones. Este cotejo verifica igualdad con el archivo de cómputos publicado; no convierte automáticamente los votos crudos de las 11 casillas anuladas en votos válidos finales MR.

Estado: `FED2024_ORDINARIAS_COTEJADAS_5_SERIES`, `NO_ORDINARIAS_COTEJADAS_65_63_104_56_97`, `RP_INCLUYE_MR`, `DIP_MR_11_ANULADAS_METADATOS`, `CADENA_JUDICIAL_PENDIENTE`. No proyectar al maestro electoral ni base viva hasta el cierre judicial.
