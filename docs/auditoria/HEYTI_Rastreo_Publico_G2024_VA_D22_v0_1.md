# HEYTI — Rastreo público de voto anticipado, Gubernatura 2024, distrito local 22

**Fecha de consulta:** 30/09/2026. **Estado:** conflicto de fuente no adjudicado. Sólo se revisaron publicaciones públicas; no se modificaron datos ni se contactó a autoridad.

## Diferencia objeto del rastreo

En el cotejo previo de las descargas originales, IEEG registra una fila de voto anticipado del distrito local 22 (sección sintética 9021, `VA01`) con **4 votos, 2 nulos y LN 2**. SICEE registra en Acámbaro, distrito 22, sección 0, `VA31`, **2 votos, 0 nulos y LN 2**. Los **2 votos válidos agregados coinciden**; los dos votos de diferencia son nulos adicionales en IEEG. Las claves no son literales equivalentes y la correspondencia se hizo por distrito, no por identidad documental de acta. Véase `HEYTI_Cotejo_G2024_LN_CAS_v0_1.md` para campos, cortes y hashes.

## Publicación encontrada

- IEEG, [Acta de la sesión especial de cómputo del Consejo Distrital Electoral 22, Acámbaro, Acta/012/2024](https://api.ieeg.mx/repoinfo/Uploads/240605-especial-cd22-acta-12.pdf). El texto público indexado indica que el consejo reanudó el **6 de junio de 2024** y comenzó el cómputo distrital de Gubernatura mediante cotejo de actas y grupos de trabajo, empezando por la casilla 51 B01. Se identificó el documento, pero el visor de búsqueda no recuperó el PDF completo por tamaño; **no se ha inspeccionado un renglón VA31/VA01, un acta de escrutinio individual ni una resolución sobre esos dos nulos**. Por ello el acta de sesión no prueba cuál CSV refleja el resultado definitivo de voto anticipado.
- IEEG, [nota del cómputo estatal y entrega de constancia](https://ieeg.mx/realiza-ieeg-computo-estatal-y-entrega-constancia-a-gobernadora-electa/). Informa que el estatal resulta de las 22 actas distritales. Su total de nulos publicado corresponde al paquete IEEG según el cotejo previo, pero un total estatal tampoco adjudica el renglón VA del distrito 22.

## Decisión operativa y prueba faltante

Conservar `GUB2024_TOTAL_VOTOS_CONFLICTO_VA_D22_2_NULOS`, ambos CSV y la procedencia de cada valor. Se requiere una imagen legible del acta de escrutinio/cómputo de voto anticipado correspondiente, constancia individual de recuento, o desglose oficial de la resolución/cómputo distrital que permita identificar el acta **y su fecha de corte**. El PDF de sesión identificado es la ruta inicial de búsqueda, no una certificación de los dos nulos. Si no se publica la prueba individual, llevar al reporte final para Alex una pregunta concreta: **¿qué acta y qué operación de cómputo sustentan los 2 votos nulos adicionales del registro VA del distrito local 22 en el CSV IEEG, frente al registro VA31 SICEE?** Alex decidirá personalmente si plantea la cuestión a su contacto; esta auditoría no enviará solicitud alguna.
