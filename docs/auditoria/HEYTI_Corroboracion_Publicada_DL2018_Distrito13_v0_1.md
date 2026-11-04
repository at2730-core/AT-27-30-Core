# HEYTI — Corroboración publicada del distrito local XIII, diputaciones MR 2018

**Fecha de consulta:** 30/09/2026. Se complementa `HEYTI_Rastreo_Externo_DL2018_Distrito13_v0_1.md`. No se modificaron archivos originales ni base viva.

El [Centro de Estudios de la Democracia y Elecciones (CEDE), UAM Iztapalapa, tabla de resultados de diputaciones locales MR Guanajuato 2018](https://cede.izt.uam.mx/wp-content/uploads/2022/09/DIPLOC2018-7.pdf), publica en su **página 1, fila XIII Silao de la Victoria**, `MORENA=19,439` y `TOTAL=87,976`. La tabla señala como fuente al **IEEG, portal de cómputos finales**. Incluye desglose de partidos, coaliciones, no registrados y nulos. Se comparan las columnas MORENA y TOTAL del mismo distrito; no se suman coaliciones a MORENA en este paso.

| Fuente / nivel | MORENA | Total | Relación |
|---|---:|---:|---|
| SICEE DL2018 MR DIS XIII | 9,439 | 77,976 | Fila agregada discordante |
| SICEE suma de 128 SEC XIII | 19,439 | 87,976 | Cuadra con CAS y agregados separados DISPP/DISCAND en total |
| CEDE/UAM, tabla atribuida a IEEG | **19,439** | **87,976** | Corrobora el valor SEC/CAS y la diferencia exacta de 10,000 frente a DIS |

**Alcance:** la tabla CEDE es una *republicación académica con atribución al IEEG*, no el acta original ni una certificación de su versión/corte. Sus cifras respaldan de manera independiente al paquete SICEE la suma seccional, pero no prueban cómo surgió `9,439` en `DIS.csv` ni si hubo rectificación posterior. El [portal oficial IEEG de cómputos 2018](https://sistemas.ieeg.mx/computos-finales-2018/) enlaza la [planilla por casilla de diputaciones](https://sistemas.ieeg.mx/computos-finales-2018/assets/files/Computo%20x%20casillas%20Diputaciones.xlsx), cuyo contenido no se pudo inspeccionar en el visor de búsqueda. Antes de elegir cifra para materialización, cotejar el XLSX/acta IEEG con hash, corte, modalidad y clave XIII, y revisar efecto judicial. Conservar por ahora ambos valores y marcar `DIS2018_DL_MR_13_DIF_10000_CORROBORACION_EXTERNA_SEC`, sin corregir el CSV fuente.

Si falta el acta o su corte, la pregunta para el informe final de Alex será: **¿por qué el campo MORENA y, en consecuencia, el total de la fila DIS XIII en el paquete SICEE difieren en −10,000 de sus 128 secciones y de la tabla CEDE atribuida al cómputo IEEG?** Ninguna solicitud se ha enviado.
