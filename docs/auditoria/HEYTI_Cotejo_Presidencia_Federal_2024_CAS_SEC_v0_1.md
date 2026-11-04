# HEYTI — Presidencia federal 2024, cotejo CAS→SEC Guanajuato

Revisión del 29 de septiembre de 2026. Fuente original SICEE `INE_SICEE_PRES_2024_original.zip`, CSV `2024_SEE_PRE_NAL_CAS.csv` y `2024_SEE_PRE_NAL_SEC.csv` filtrados a `ID_ESTADO=11`. Por `(ID_DISTRITO_FEDERAL, ID_MUNICIPIO, SECCION)` se agrupan **8,168 CAS** en **3,234 SEC**; todas las SEC tienen CAS y no sobran grupos CAS. La única SEC=0 agrupa las casillas del voto en el extranjero; no se confunde con secciones ordinarias.

Para todas las **3,234 SEC** coinciden exactamente las sumas CAS de `NUM_VOTOS_VALIDOS`, `NUM_VOTOS_CAN_NREG`, `NUM_VOTOS_NULOS`, `TOTAL_VOTOS` y `LISTA_NOMINAL`. Cero diferencias, cero vacíos en esos cinco campos y cero CAS con `TRIBUNAL` que contenga `ANULAD`. Cobertura CAS: B 3,233; C 4,709; E 161; S 41; A 15; MEC 7; P 2 (total 8,168). La casilla P y las MEC no deben confundirse con el tipo de elección P usado en el maestro.

Es un cotejo de consistencia interna SICEE CAS→SEC; complementa la comparación con cómputo federal en `HEYTI_Cotejo_Federal_2024_GTO_5_Series_v0_1.md`. No implica modificar la base viva ni resolver por extrapolación diferencias frente a otras fuentes.
