# HEYTI — CAS contra SEC SICEE local 2021

Fecha: 29/09/2026. Original `INE_SICEE_GTO_PEL_2021_original.zip`; CSV CAS y SEC de Ayuntamientos A, Diputaciones locales MR y RP. Sólo lectura, sin cambios a base viva. `SECCION` es única en SEC dentro de cada serie; las CAS se sumaron por esa sección. Se compararon válidos, no registrados, nulos, total y lista nominal, preservando vacíos como indeterminados.

| Serie | SEC | CAS | SEC con cinco campos numéricos iguales a CAS | SEC con resta judicial determinada | SEC con al menos un campo vacío en CAS o SEC |
|---|---:|---:|---:|---:|---:|
| A | 3,159 | 7,745 | 3,139 | 18 | 2 |
| DL MR | 3,159 | 7,745 | 3,152 | 1 | 6 |
| DL RP | 3,159 | 7,776 | 3,151 | 1 | 7 |

En A, **23 CAS `TRIBUNAL=ANULADA`** conservan **6,214 votos crudos** en **20 secciones**. En 18 secciones, la resta de cada componente publicado de SEC respecto a CAS coincide con sus CAS anuladas. En las otras dos, **163 y 2541**, los votos SEC están vacíos y LN permanece publicada; CAS conserva 371 y 214+222 votos anulados, respectivamente. No se rellenan los vacíos con cero.

En DL MR y DL RP, la CAS **2251 C01** figura `ANULADA` con **235 votos crudos** en cada archivo; su resta CAS→SEC es exactamente 235 por modalidad. No sumar los dos archivos como si fueran 470 votos anulados de casillas físicas distintas: RP tiene alcance de modalidad y en especiales contiene tanto SMR como SRP.

Los casos de campos vacíos que limitan la igualdad plena son: DL MR secciones **1282, 1518, 1080, 1866, 2270 y 2794**; DL RP añade **1729**. En varias CAS especiales de total **0**, no registrados y nulos están vacíos mientras SEC publica valores numéricos. En **DL RP sección 1080**, CAS B/C01 y SEC tienen `TOTAL_VOTOS` vacío; MR publica total 0 para esa sección. Preservar MR 0 y RP vacío por separado, sin imputar equivalencia. Todos los componentes **numéricamente comparables** fuera de las restas judiciales coinciden; los vacíos impiden afirmar identidad de los cinco campos en esas secciones.

Este cotejo verifica niveles dentro de SICEE; no resuelve las claves especiales repetidas en IEEG ni transforma votos de una modalidad en otra. Mantener originales, estado judicial y el corte antes de integrar a HEYTI.
