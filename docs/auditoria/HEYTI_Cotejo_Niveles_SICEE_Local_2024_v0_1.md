# HEYTI — Cotejo entre niveles SICEE local 2024

Fecha: 29/09/2026. Fuente original `INE_SICEE_GTO_PEL_2024_original.zip`, CSV CAS, SEC, MUN y DIS de Ayuntamientos (A), Diputaciones locales MR (DL MR) y Gubernatura (G). Lectura solamente; no se alteró la base viva.

Se compararon cinco campos por elección y territorio: `NUM_VOTOS_VALIDOS`, `NUM_VOTOS_CAN_NREG`, `NUM_VOTOS_NULOS`, `TOTAL_VOTOS` y `LISTA_NOMINAL`. Las claves SEC→CAS conservaron distrito local, municipio y sección; los registros `SECCION=0` de voto anticipado/extranjero se mantuvieron en el ámbito que figura en cada archivo, sin asignarlos a una sección territorial ordinaria.

## SEC → MUN/DIS

| Elección y nivel | Agregados | Cinco campos iguales a suma SEC |
|---|---:|---:|
| A MUN | 46 | 46 |
| DL MR DIS | 22 | 22 |
| DL MR MUN | 46 | 46 |
| G DIS, incluido distrito 0 de voto en el extranjero | 23 | 23 |
| G MUN, incluido municipio 0 de voto en el extranjero | 47 | 47 |
| **Total** | **184** | **184** |

## CAS → SEC

| Elección | SEC | CAS | Cinco campos iguales a suma CAS | SEC con votos menores que suma CAS |
|---|---:|---:|---:|---:|
| A | 3,257 | 8,168 | 3,206 | 51 |
| DL MR | 3,258 | 8,169 | 3,258 | 0 |
| G | 3,259 | 8,176 | 3,259 | 0 |

En las **51 SEC de A**, la diferencia `SUM(CAS.TOTAL_VOTOS) − SEC.TOTAL_VOTOS` coincide **en cada sección** con la suma de sus CAS con `TRIBUNAL=ANULADA`: **58 casillas y 18,318 votos crudos** en total (45 secciones con una CAS anulada, cinco con dos y una con tres). Los cuatro campos de votos también reflejan la resta de esas CAS; **LN permanece igual** entre SEC y la suma de CAS. Las filas CAS anuladas conservan sus votos históricos, pero esos votos no se reincorporan al SEC vigente. Hay además dos CAS A marcadas `MODIFICADA`; esta prueba no interpreta su efecto judicial ni las equipara a las anuladas.

La consistencia aritmética entre niveles confirma este paquete SICEE y sus reglas observadas de agregación; **no constituye cotejo IEEG/SICEE ni certificación judicial completa** de cada caso. Preservar los valores CAS crudos, el campo `TRIBUNAL`, la proyección SEC y la procedencia de cada agregado. Los desacuerdos de LN con el corte IEEG 2024 permanecen documentados por separado.
