# HEYTI — Cotejo CAS→SEC, Diputaciones locales RP, 2018 y 2024

Fecha de corte de la revisión: 29 de septiembre de 2026. Alcance: Guanajuato, archivos CSV originales del paquete SICEE local 2018 y 2024, únicamente DIP_LOC_RP CAS y SEC; se consultó DIP_LOC_MR CAS para comparar cobertura. Esta es una comprobación de consistencia interna de los paquetes, no una validación externa del resultado electoral ni una modificación de la base viva.

| Año | MR CAS | RP CAS | RP SEC | CAS adicionales en RP | SEC con discrepancia en cinco campos |
|---|---:|---:|---:|---:|---:|
| 2018 | 7,463 | 7,499 | 3,137 | 36 SRP | 0 |
| 2024 | 8,169 | 8,210 | 3,258 | 41 SRP | 0 |

Para cada fila SEC se agruparon las filas RP CAS correspondientes y se compararon exactamente `NUM_VOTOS_VALIDOS`, `NUM_VOTOS_CAN_NREG`, `NUM_VOTOS_NULOS`, `TOTAL_VOTOS` y `LISTA_NOMINAL`. Todas las filas SEC tienen grupo CAS y coinciden en los cinco campos; no hubo vacíos en esos campos ni CAS con `ESTATUS_ACTA` que contuviera `ANULAD`. La comparación no suma las casillas MR otra vez: RP CAS ya contiene la cobertura MR más las SRP. En 2018, el emparejamiento entre modalidades usa `SECCION` + `CASILLA`; tipo e identificador numérico solos confunden SMR con SRP. Para agregar CAS→SEC en 2018 se usa `SECCION`, única dentro de esta serie. En 2024 se usa `(ID_DISTRITO_LOCAL, ID_MUNICIPIO, SECCION)` para preservar las 24 filas SEC=0, cuyas claves de sección se repiten por distrito/municipio. Para comparar cobertura MR/RP en 2024 se emplea esa clave más tipo, identificador y extensión de casilla.

Fuentes exactas: `INE_SICEE_GTO_PEL_2018_original.zip`, CSV `2018_SEE_DIP_LOC_{MR,RP}_GTO_CAS.csv` y `2018_SEE_DIP_LOC_RP_GTO_SEC.csv`; `INE_SICEE_GTO_PEL_2024_original.zip`, CSV equivalentes `2024_SEE_DIP_LOC_*`. Estos conteos no resuelven diferencias con IEEG ni el estado de eventuales sentencias fuera de los campos aquí cotejados. Mantener ambos paquetes originales y sus metadatos; no actualizar aún la base viva.
