# HEYTI — Contraste del ZIP de HEYTI-CORE con la auditoría electoral

**Copia examinada:** `AT-27-30-CORE(1).zip`, recibida el 25 de septiembre de 2026. Integridad ZIP correcta. Contiene código, DDL, ETL, pruebas, documentación y frontend. No contiene `datasets/electoral/Datos_Electoral_con_2015.json` ni geometría original, pero esos archivos electorales ya fueron aportados por separado. No se verificó una base PostgreSQL viva ni el estado Git de la carpeta Windows. Esta copia se examina sin modificarla.

## Estado real de la cadena actual

| Capa | Evidencia en el ZIP | Brecha respecto de fuente completa |
| --- | --- | --- |
| Base electoral | `database/ddl/004_create_electoral_base.sql`: `election` único por `(year,type)`; `section_result` único por `(section_id,election_id,party_id)`, `party_id` obligatorio, `votes` obligatorio. | No distingue MR/RP, corte/fuente, tipo de acta ni opción de combinación/independiente/nulos; FK a sección territorial actual limita historia. Requiere esquema aditivo y migración versionada, preservando las tablas actuales hasta validar consumidores. |
| ETL legado | `D:\GitHub\AT-27-30-core\database\etl\008_load_electoral_full.py`: lee la maestra `...con_2015.json`, regex `(15|18|21|24)(A|DF|DL|G|P|S)_([A-Z]+)`, lista de ocho partidos, búsqueda de sección territorial, `ON CONFLICT` por sección/elección/partido. | Descarta por diseño combinaciones con guion bajo, independientes y no registrados/nulos; mezcla modalidad y corte; incluye 2015; omite secciones no presentes en `territorial.section`. No usar para cargar los 23 conjuntos completos sin rediseño. Las credenciales codificadas en ese archivo también deben pasar a configuración segura al revisarlo. |
| Reconstrucción G 2024 | `D:\GitHub\AT-27-30-core\src\heyti\audit\data_truth\gubernatura_2024.py`: función pura que coteja INE/IEEG y actualiza **seis** campos `24G_*` del maestro; tiene pruebas unitarias. | Es una herramienta de reparación de vista legado, no un importador de todas las opciones; exige correspondencia exacta de votos comparables y conserva sin cambio secciones sin evidencia INE. Revisar cortes y discrepancias documentadas antes de ejecutarla sobre la maestra real. |
| DescribeSection | `D:\GitHub\AT-27-30-core\src\heyti\capabilities\describe_section\electoral_result_source.py`: lee cuatro partidos, total y LN del maestro; declara `TRACKED_PARTIES_ONLY`, distingue `ZERO_TOTAL`, empate rastreado e inconsistencia. | La respuesta no puede expresar opciones completas, modalidad/corte ni ganador de candidatura; `leading_tracked_party` no se debe rotular ganador oficial. Diseñar contrato nuevo/versionado y conservar compatibilidad con clientes actuales. |
| Frontend CORE | `apps/heyti-web/src/gateway/electoral.response.ts`: tipos para cuatro partidos y `coverageScope: TRACKED_PARTIES_ONLY`. | Debe extenderse junto con la respuesta certificada antes de mostrar opciones originales o ganador por candidatura. Los HTML V1 auditados son otra copia, no sustituyen este frontend. |

## Verificación crítica de la cuarentena G 2024

La clase `CertifiedElectoralSectionSource` **sí admite** `quarantined_contests=["G"]` y la prueba `D:\GitHub\AT-27-30-core\tests\core\test_describe_section_electoral_result_source.py` verifica que devuelve G `INCONSISTENT` y cifras `NULL`. Pero su argumento por defecto es `()` y la **única composición de runtime** localizada, `D:\GitHub\AT-27-30-core\src\heyti\runtime\guanajuato_2023_composition.py`, construye la fuente **sin** `quarantined_contests`. El test de integración `D:\GitHub\AT-27-30-core\tests\core\test_guanajuato_2023_runtime_electoral.py` espera incluso G `AVAILABLE` con valores 2024 de una maestra que no viene en el ZIP.

Prueba de lectura aislada: al instanciar el proveedor del ZIP con la maestra aportada y sección 1, sin cuarentena explícita, respondió G `AVAILABLE`, `total_votes=925` y líder rastreado PAN; con `quarantined_contests=["G"]`, respondió G `INCONSISTENT` y total `NULL`. El `925` es el valor copiado de 2018 en esa maestra aportada. **Conclusión acotada:** la capacidad de cuarentena existe, pero la ruta de composición incluida en este ZIP no la activa. No se puede afirmar desde esta copia que el checkout Windows o un despliegue distinto entregue esos valores; tampoco se debe declarar la contención end-to-end verificada. Antes de cualquier publicación, fijar el guardarraíl en la composición o sustituir la fuente por una reconstrucción certificada y probar la ruta completa.

Esto corrige el supuesto operativo del registro previo que daba la contención como efectiva en HEYTI-CORE: fue informada en trabajo anterior y comprobada a nivel de proveedor con configuración explícita; **en este ZIP no está conectada al runtime mostrado**. La maestra física continúa sin corregirse en la copia aportada. Las proyecciones `PROY_2027_G_*` aún requieren rastreo de consumidores.

## Orden de integración propuesto

1. Registrar baseline del checkout Windows y compararlo con este ZIP (sin `.git`, no conocemos su commit); confirmar qué dataset real carga la composición y activar cobertura G 2024 segura mientras se migra.
2. Crear staging de resultados originales con opción, modalidad, versión/corte, estado y sección histórica/acta especial; importar 23 conjuntos conservando 2015 fuera del alcance. No alterar de entrada `electoral.section_result` legado.
3. Conciliar el staging con hashes, conteos, totales, NULL/0, 328 DL 2021, actas especiales y Golden Cases; mantener discrepancias como incidencia y no imputar cifras.
4. Crear vista certificada por candidatura y vista de compatibilidad para cuatro siglas; migrar DescribeSection y su gateway de forma versionada, con pruebas fuente→DB→Capability→Runtime→Materialización→UI.
5. Retirar la cuarentena solo con G 2024 reconstruida y validada en toda la cadena. Después migrar módulos V1 en el orden acordado: Análisis Territorial, Ganar Todo, Campo; luego pendientes.

**Limitación de pruebas:** en este entorno no está instalado `pytest` y el ZIP omite datasets de pruebas que las integraciones esperan; se ejecutó la prueba aislada del proveedor de forma directa, no la suite completa ni PostgreSQL. Las rutas Windows anteriores indican la ubicación esperada en la computadora de Alex; su correspondencia con el ZIP se verificó por ruta interna.

## Seguimiento de integridad y entrega web — 25 de septiembre de 2026

Se volvieron a verificar los 15 ZIP originales que alimentan los 23 conjuntos del catálogo: SHA-256, CRC de todos los miembros y presencia de cada ruta CSV. **15/15 ZIP y 23/23 rutas CSV pasaron**. Dos copias temporales de trabajo (`INE_SICEE_DF_RP_2018_original.zip` y `INE_SICEE_S_RP_2024_original.zip`) estaban truncadas; se recuperaron de los originales conservados, cuyos SHA-256 coinciden con el catálogo. Este incidente no cambia las discrepancias electorales registradas ni indica alteración de los originales.

La entrada HTTP real del ZIP, `D:\GitHub\AT-27-30-core\src\heyti\gateway\guanajuato_2023_http_host.py`, llama a `compose_guanajuato_2023_runtime` sin configuración adicional. Por tanto, hereda la falta de cuarentena G 2024 de la composición. Su prueba HTTP consulta la sección 1524, pero no afirma el estado G 2024 de la sección 1 ni rechaza la cifra copiada.

En `apps/heyti-web/src/gateway/electoral.response.ts`, el contrato acepta `INCONSISTENT` y exige líder rastreado `NULL` en ese estado; los demás números se validan por tipo, pero no se comprueba que **todos** sean `NULL` cuando la contienda está en cuarentena. `apps/heyti-web/src/shell/SectionElectoralSummary.tsx` presenta «Inconsistente» y «No disponible» si recibe los `NULL` esperados. Sin embargo, la comparativa e historial tienen encabezados generales «COMPARATIVA CERTIFICADA», «Serie certificada 2018–2024» y «EVOLUCIÓN CERTIFICADA» que no distinguen una G 2024 en cuarentena. La prueba web revisada no contiene un caso `INCONSISTENT`.

**Puerta de aceptación adicional:** después de activar la cuarentena en la composición, exigir un caso de G 2024 sección 1 en proveedor, runtime materializado, HTTP y parser/UI: `data_status=INCONSISTENT`, seis magnitudes y líder/margen `NULL`, sin cifra ni ganador expuestos; A 2024 debe seguir disponible. La UI debe evitar un rótulo global de certificación para una serie parcialmente en cuarentena. El ensayo HTTP con las fuentes reales espera `datasets/spatial/secciones.geojson` (3,266 geometrías), ausente del ZIP y de los archivos aportados en este entorno. Hasta recibirlo, esta puerta permanece **NO VERIFICADA**; no se simuló geometría para certificarla.

## Alcance efectivo del reparador G 2024

Se inspeccionaron `D:\GitHub\AT-27-30-core\src\heyti\audit\data_truth\gubernatura_2024.py` y `D:\GitHub\AT-27-30-core\scripts\data_truth\rebuild_gubernatura_2024.py`. El reparador exige coincidencia exacta de PAN, PRI, PVEM, MORENA y total entre INE e IEEG para cada sección INE; usa la LN de INE, crea un candidato nuevo y deja intacta la fuente original. No reconstruye otras opciones, `GANADOR_24G` ni proyecciones 2027. Conserva sin modificación toda fila de maestra ausente de la entrada INE.

Cotejo directo de claves entre la maestra aportada (3,310 filas) y `2024_SEE_GOB_GTO_SEC.csv` del ZIP SICEE oficial (3,233 secciones ordinarias): **77 filas de maestra quedan fuera**. Son 32 claves históricas menores de 9000 y 45 claves especiales 9001 o mayores. En **28** de las históricas, `24G_TOTAL` es finito y repite `18G_TOTAL`; las otras cuatro históricas (3486, 4986, 5237, 5885) y las 45 especiales tienen `NaN` en `24G_TOTAL`. Por su contrato actual, aun si verifica y actualiza las 3,233 secciones ordinarias, el reparador dejaría los **28 valores copiados** bajo el nombre `24G_*` y preservaría los `NaN` restantes. La fuente candidata no puede declararse íntegramente saneada sin estados explícitos para secciones históricas y actas especiales. No se debe convertir esos registros en ceros ni identificarlos como secciones ordinarias vigentes.

El script de ejecución exige archivos preparados `2024_SEE_GOB_GTO_SEC.xlsx` y `GTO_GUB_2024_IEEG.csv` con hashes fijados; los originales aportados son ZIP con el seccional INE en CSV y el IEEG en un ZIP interno. Falta documentar y verificar la preparación reproducible de esos dos insumos y su correspondencia de hashes antes de ejecutar el script. **Puerta bloqueante:** reporte de cobertura por identidad y tipo de acta, rechazo de cualquier `24G_*` finito copiado de 2018 en filas no certificadas como G 2024, y reconciliación independiente de ganador/proyección. La cuarentena de entrega debe permanecer activa hasta superar estas verificaciones.

### Ensayo aislado en memoria con los originales conservados

Se leyeron el seccional `2024_SEE_GOB_GTO_SEC.csv` del ZIP SICEE y `GTO_GUB_2024.csv` del ZIP interno IEEG. Las **3,233** secciones ordinarias INE están presentes en IEEG; IEEG agrega además 22 claves especiales. Por sección ordinaria coinciden **PAN, PRI, PVEM, MORENA y TOTAL_VOTOS en 3,233/3,233**. `LISTA_NOMINAL` difiere en 2,657; la función usa la LN de INE conforme a su contrato. Este cotejo verifica los valores originales empleados en el ensayo, no los hashes de los XLSX/CSV preparados que exige el script de producción.

Se invocó directamente `rebuild_gubernatura_records` con objetos construidos de esos originales y una copia en memoria de la maestra, **sin escribir candidato ni alterar archivos**. Resultado: `total_master_sections=3310`, `verified_sections=3233`, `updated_sections=3233`, `preserved_sections=77`. La sección 1 cambió de `24G_TOTAL=925` copiado a `1037` oficial; las 28 secciones históricas con copia finita permanecieron iguales. Por ello la comparación de votos permitiría reconstruir la parte ordinaria, pero el resultado total todavía no supera la puerta de calidad para su publicación.

### Identidad de las filas preservadas y actas especiales

Las 45 claves especiales `>=9000` de la maestra no representan un bloque homogéneo de gubernatura. El CSV IEEG G 2024 incluye **22** claves especiales: 9001–9021 (21 actas `VA01`) están en la maestra, mientras 9042 (acta MEC con 9,217 votos y LN 0 en ese corte) **no tiene fila en la maestra**. Las otras **24** claves especiales de la maestra (9022–9041 y 9043–9046) no figuran como actas G en ese CSV. El derivado `electoral/G.json` sí conserva 9001–9021 y 9042; por ejemplo 9021 total 4/LN 2 y 9042 total 9,217/LN 0. Esta última cifra no debe sumarse a una sección territorial ni utilizarse para una tasa de participación ordinaria.

Así se desglosan las 77 filas preservadas por el reparador: **28 históricas con copia numérica 18G→24G**, **4 históricas con `NaN`** (3486, 4986, 5237, 5885), y **45 claves especiales con `NaN`** en `24G_TOTAL`. Para la fuente fiel se requieren identidades de sección histórica y de acta especial separadas, con estado de ausencia explícito; el maestro legado no debe convertir ninguno de estos `NaN` en cero. Las 21 actas VA y la MEC 9042 pueden conservarse desde IEEG/derivado en un registro de actas versionado, sin forzar las 24 claves ajenas a G a tener resultado G.

## Validez JSON de la maestra y semántica de ausencia

Una lectura de los bytes originales de `Datos_Electoral_con_2015.json` encontró **15,869 tokens literales `NaN`** distribuidos en 125 columnas y 530 filas de las 3,310. La decodificación JSON estricta rechaza el archivo; el parser permisivo de Python los acepta como flotantes no finitos. Cada uno de los seis derivados `electoral/{A,DF,DL,G,P,S}.json` pasa lectura estricta y no contiene esos tokens. `24G_PAN/PRI/PVEM/MORENA/TOTAL/LN` tienen **173 `NaN` por campo**; `21DL_*` tiene 479 por campo, cifra que incluye ausencias fuera de las 328 secciones ordinarias previamente auditadas. No interpretar `NaN` automáticamente como voto cero, anulación ni «no celebrada».

La función de reconstrucción reemplaza los seis `24G_*` de las 3,233 secciones ordinarias, incluidas las 124 filas G 2024 con ausencia en la maestra, pero `rebuild_gubernatura_file` usa `json.dump` sin `allow_nan=False`. Por tanto, los `NaN` de otros campos y de las 49 filas G no ordinarias permanecerían como literales no estándar en su archivo candidato. **Puerta adicional:** definir un estado tipado por celda/resultado según fuente, modalidad y causal documentada, transformar a `null` solo con su estado y procedencia conservados, serializar con `allow_nan=False` y verificar lectura estricta; hacerlo mediante migración reproducible, no una sustitución ciega `NaN→0`.

### `NaN` en el total de maestra frente al universo oficial de cada elección

Se comparó la clave de cada fila con el CSV seccional SICEE correspondiente. Para DL/DF/S se usó MR en 2018/2021 y RP en 2024, igual que el corte legado identificado para la maestra. «Dentro» significa que la sección está publicada en ese seccional, no que el valor pueda rellenarse sin conservar modalidad/corte.

| Serie de total | `NaN` en maestra | Dentro del seccional | Fuera del seccional |
|---|---:|---:|---:|
| 18A, 18DL, 18DF, 18G, 18S, 18P (cada una) | 173 | 0 | 173 |
| 21A | 152 | 1 | 151 |
| 21DL MR | 479 | 328 | 151 |
| 21DF MR | 151 | 0 | 151 |
| 24A | 53 | 0 | 53 |
| 24DL RP | 56 | 0 | 56 |
| 24DF RP | 73 | 0 | 73 |
| 24G | 173 | 124 | 49 |
| 24S RP | 73 | 0 | 73 |
| 24P | 74 | 1 | 73 |

Los **454 pares sección–serie con `NaN` dentro del seccional** se concentran en 21A sección 1404, 21DL MR (328), 24G (124) y 24P sección 1150; su recuperación ya tiene fuente oficial o derivado cotejado, pero exige transformación versionada. No interpretar los totales «fuera» como resultados faltantes de esa elección: incluyen identidades históricas, altas posteriores y actas especiales. Tampoco sumar las seis series 2018 como 1,038 secciones distintas; son incidencias de campo en muchos registros compartidos.

### Cotejo de contenido de la maestra: casos A 2021 y P 2024

En A 2021 sección **1404**, la maestra contiene PAN 174, PRI 43, PVEM 16 y MORENA 73, iguales a SICEE y `electoral/A.json`; `21A_TOTAL` y `21A_LN` son `NaN`, frente a **345** y **725** respectivamente en ambas fuentes cotejadas. La recuperación requiere esos dos campos, preservando la evidencia del resto del bloque.

En P 2024 sección **1150**, la maestra tiene `24P_PAN=1546`, mientras SICEE y `electoral/P.json` tienen **1246**; los otros tres partidos, total y LN de la maestra son `NaN` frente a PRI 51, PVEM 7, MORENA 152, total 1596 y LN 2448. Por ello esa fila no es solo un total ausente: también tiene un voto directo discrepante.

Se amplió la comparación de `24P_*` a las **3,233 secciones ordinarias**: hay al menos un campo discrepante o ausente en **2,454 secciones**. Diferencias numéricas por campo: PAN 1,726; PRI 1,073 (más un `NaN`); PVEM 1,239 (más un `NaN`); MORENA 1,847 (más un `NaN`); TOTAL 2,166 (más un `NaN`); LN 15 (más un `NaN`). El derivado `electoral/P.json` coincide con SICEE en PAN/PRI/PVEM/MORENA/TOTAL/LN **3,233/3,233 en cada campo**. Esto acredita el corte de comparación del derivado, pero **no identifica la procedencia ni la causa** de los valores distintos de la maestra. Guardar la maestra como versión legado y no mezclar sus campos `24P_*` con los del derivado/SICEE hasta obtener su linaje y regla de vigencia.

### Barrido transversal de totales de la maestra

Comparación de `*_TOTAL` con el seccional SICEE por año, elección y modalidad del derivado legado (MR en 2018/2021, RP en DL/DF/S 2024). La tabla cuenta diferencias numéricas y ausencias en la maestra; **no atribuye causa** ni suma modalidades alternativas.

| Serie | Secciones oficiales | Total distinto | Total ausente en maestra | Observación |
|---|---:|---:|---:|---|
| 18A / 18DL MR | 3,137 cada una | 37 / 29 | 0 / 0 | Investigar corte y actas. |
| 18DF MR / 18G / 18S MR / 18P | 3,137 cada una | 0 | 0 | `18DF_LN` no existe en el bloque legado, pese a total coincidente. |
| 21A / 21DL MR / 21DF MR | 3,159 cada una | 41 / 43 / 0 | 1 / 328 / 0 | `21DF_*` carece de cuatro votos directos en la maestra. SICEE A tiene además dos totales oficialmente vacíos. |
| 24A / 24DL RP | 3,233 cada una | 53 / 0 | 0 / 0 | LN difiere en 2,657 secciones por corte en ambas; A tiene cambios de votos. |
| 24DF RP / 24S RP / 24P | 3,233 cada una | 2,275 / 2,410 / 2,166 | 0 / 0 / 1 | LN difiere en 15 secciones por serie; procedencia del voto legado pendiente. |
| 24G | 3,233 | 3,096 | 124 | Copia conocida de 2018; 13 coincidencias aisladas no validan la serie. |

Para DF y Senado 2024 se cotejó también la maestra con **MR**: sigue habiendo 2,576 y 2,683 secciones, respectivamente, con al menos un campo distinto o ausente. Por tanto, las diferencias masivas frente a RP **no se explican solo por haber escogido la modalidad equivocada**. No etiquetar aún el legado como error de captura ni reconstruirlo mezclando MR/RP; falta identificar fuente/corte de esos bloques y cotejar sus actas. El conteo de «fila con algún campo distinto» incluye ausencias contractuales como LN 2018 DF y cuatro partidos 2021 DF; no se usa para afirmar que todos sus totales sean erróneos.

### Trazabilidad de la maestra federal y riesgo del ETL legado

En el ZIP aportado no se localizó un generador ni un manifiesto de fuentes para los bloques `24DF_*`, `24S_*` y `24P_*` de la maestra. El ZIP de datos registra una fecha de archivo distinta para la maestra (8 junio 2026) y los seis derivados (9 septiembre 2025); esas marcas no prueban la procedencia electoral ni permiten adjudicar un corte oficial a los valores. Mantener estado **ORIGEN_PENDIENTE** para esos bloques hasta localizar su script de construcción, bitácora o archivo fuente.

`D:\GitHub\AT-27-30-core\database\etl\008_load_electoral_full.py` lee la maestra mediante el parser permisivo de Python, descarta votos de partido `NaN` y convierte a entero los valores finitos; toma total y LN de la misma fila y hace `ON CONFLICT DO UPDATE` en `electoral.section_result`. No contrasta sus cifras con SICEE/IEEG, no registra corte ni modalidad y su llave única `(section_id,election_id,party_id)` no puede conservar versiones alternativas. **Si se ejecuta con esta maestra**, puede materializar en la base los valores federales 2024 de procedencia aún desconocida. No se ha consultado una base viva ni se afirma que haya ocurrido en la instalación de Alex. Antes de recargar, obtener inventario de filas actuales y comparación de muestras/hashes; preservar respaldo y cargar fuentes versionadas en staging separado.

## Auditoría de la base viva — salida compartida por Alex el 25/09/2026

Alex ejecutó `HEYTI_Auditoria_DB_Electoral_Solo_Lectura.sql` en su PostgreSQL local y compartió la salida de los cuatro bloques. **La base sí fue consultada; este resultado actualiza la limitación anterior**. La consulta fue de solo lectura; no se modificó la DB.

| Serie | Secciones en SICEE | Secciones con resultado en DB | Diferencia de cobertura numérica | Evidencia |
|---|---:|---:|---:|---|
| Cada elección 2018 A/DF/DL/G/P/S | 3,137 | 3,106 | 31 | Cuatro partidos por sección; DF LN nula en 12,424 filas. |
| 2021 A | 3,159 | 3,130 | 29 | Una sección con total y LN nulos entre las filas cargadas: 1404 en el caso semilla. |
| 2021 DL | 3,159 | 2,802 | 357 | Consistente en magnitud con 328 bloques `21DL_*` ausentes y 29 identidades territoriales no cargadas; verificar conjuntos de claves antes de declararlo identidad exacta. |
| 2021 DF | 3,159 | **0** | 3,159 | Elección en catálogo, ningún resultado cargado. La maestra no trae votos directos `21DF_*`; ETL 008 solo inserta partidos. |
| 2024 A/DF/DL/S/P | 3,233 | 3,228 | 5 | Cuatro partidos por sección salvo P 2024 sección 1150, con solo PAN. |
| 2024 G | 3,233 | 3,106 | 127 | 12,424 filas de cuatro partidos, correspondientes a la serie vieja cargada; no representa cobertura certificada G 2024. |

Casos semilla observados en DB: `2024 G`, sección 1: PAN 380, PRI 235, PVEM 42, MORENA 168, total **925**, LN 1535, participación 60.26%. Son los valores copiados de 2018; SICEE G 2024 tiene PAN 492, PRI 160, PVEM 41, MORENA 266, total 1037 y LN 1570. `2024 P`, sección 1150: solo PAN **1546**, total/LN nulos; SICEE y derivado registran PAN 1246, total 1596 y LN 2448. `2021 A`, sección 1404: cuatro votos directos cargados, total/LN nulos; SICEE total 345/LN 725. `2021 DL`, sección 1080: cuatro ceros, total 0 y LN 1346; esto corresponde a MR, no al estado RP de paquete no entregado.

La consulta interna encontró **cero secciones con totales o LN distintos entre partidos de la misma elección**. Eso acredita consistencia de repetición dentro del esquema legado, **no corrección contra fuentes**: G 2024 sección 1 repite la cifra errónea de forma perfectamente uniforme. `territorial.section` no contiene claves 9000 o mayores; las actas especiales requieren identidad separada.

**Bloqueo confirmado en DB:** mantener fuera de salidas confiables G 2024 y sus proyecciones basadas en maestra; verificar la composición HTTP real y aplicar la cuarentena antes de entregar resultados. Preparar respaldo y exportación auditada de las filas actuales antes de una migración aditiva; cargar los 23 conjuntos versionados en staging, sin `UPDATE` de la tabla legado ni ejecutar ETL 008 sobre la maestra durante el cotejo. Los conteos por sí solos no prueban que los faltantes sean exactamente las mismas claves históricas; contrastar listas de sección de DB y SICEE para cerrar esa identidad.

### Identidades verificadas con la segunda consulta de la DB

Alex ejecutó `HEYTI_Auditoria_DB_Electoral_Identidades_Solo_Lectura.sql` y aportó `HEYTI_Auditoria_DB_Electoral_Identidades_Resultado.txt`. La salida en UTF-16 fue leída íntegra. El `FULL OUTER JOIN` de G 2018 y G 2024 por sección y partido devuelve **12,424 pares**, cero exclusivos de 2018, cero exclusivos de 2024 y **cero diferencias** en el triplete `(votes,total_votes,nominal_list)`. La copia 18G→24G está, por tanto, confirmada en todas las filas G cargadas de la DB, no solo en la sección semilla.

La comparación de conjuntos A 2021 y DL 2021 muestra 3,130 secciones en la unión, **328 solo A**, cero solo DL y 2,802 compartidas. Se extrajeron las 328 claves de la salida y se cotejaron como conjuntos con `HEYTI_Faltantes_21DL_Maestra_328_Secciones.json`: **328/328 identidades exactas; cero claves exclusivas de DB o expediente**. La recuperación MR desde el derivado y SICEE ya estaba comprobada en seis campos para ese expediente. La diferencia de 357 contra las 3,159 secciones SICEE DL MR se descompone ahora en **328 filas fuente existentes pero bloque DL ausente en DB**, más **29 secciones oficiales no presentes en el conjunto cargado A/DL 2021**. La identidad de esas 29 aún debe cotejarse con el histórico territorial; el conteo no autoriza reasignarlas a sucesoras.

### Identidad cerrada de las 29 secciones 2021 fuera del catálogo territorial — 26/09/2026

Alex ejecutó `HEYTI_Auditoria_DB_Electoral_2021_29_Identidades_Solo_Lectura.sql` (listado incorporado del seccional SICEE de ayuntamientos 2021, SHA-256 del CSV `5501627ea795abc8da1320ced9d5f94e1154926540b26605881d14a0cfba7372`) y aportó la salida de PostgreSQL. El contraste devuelve **3,159 claves oficiales únicas, 3,130 cargadas en A 2021 y 29 faltantes**. Las 29 faltantes **no tienen identidad en `territorial.section` actual**; el contraste inverso no encontró ninguna clave A 2021 cargada fuera del listado oficial. La consulta solo leyó la DB.

Claves faltantes: **145, 315, 336, 343, 892, 899, 966, 1059, 1078, 1099, 1110, 1268, 1285, 1490, 1494, 1495, 1509, 1614, 1634, 1642, 1647, 1681, 1687, 2190, 2193, 2477, 2514, 2860, 2907**.

Las 29 tienen registro en la maestra, `21A_TOTAL` y `21DL_TOTAL` numéricos; también aparecen en los seccionales SICEE A 2018 y A 2021. Por ello son una **pérdida de identidad histórica en la materialización territorial actual**, no ausencia de resultados en esas fuentes. Cinco claves (343, 1059, 1110, 1634 y 1647) figuran además en el CSV A 2024; las otras 24 no figuran allí. Esta pertenencia por clave no establece continuidad geométrica ni equivalencia entre actas o secciones sucesoras.

La brecha DL 2021 de 357 claves queda descompuesta por identidad: **328** claves oficiales con identidad cargada en A pero sin filas DL, exactamente el expediente de bloques `21DL_*` ausentes de la maestra; y **29** claves oficiales sin identidad en `territorial.section`. Para recuperar la historia, diseñar identidad territorial versionada por vigencia y relación documentada, conservar sus resultados A/DL 2021 en staging con modalidad MR, y contrastar fuente→staging→DB antes de exponerlos. No añadir las 29 a la tabla vigente ni imputarlas a sucesoras por coincidencia de código. El estado y contenido de `territorial.section_history` en la base viva no se verificaron con esta consulta; en un respaldo de catálogo del ZIP estaba vacío, lo que no acredita el estado actual.

### Aclaración de la cardinalidad A 2024 — 26/09/2026

El aparente exceso de una clave del seccional A 2024 se explica íntegramente por `SECCION=0`. El archivo `2024_SEE_AYUN_GTO_SEC.csv` contiene **3,257 filas**, de las cuales **3,233** tienen una sección ordinaria positiva y única, y **24** filas usan `SECCION=0` con municipios diferentes. Estas 24 filas suman 135 en `TOTAL_VOTOS` y 162 en `LISTA_NOMINAL`. Por ello hay 3,234 valores distintos del campo `SECCION` si se cuenta el cero como clave, pero **3,233 secciones ordinarias**, de acuerdo con la cardinalidad previa. La identidad de las 24 filas de cero debe conservar también municipio y procedencia; no incorporarlas a `territorial.section` como sección 0 ni mezclarlas con las 3,233 ordinarias. Su naturaleza electoral específica requiere documentar el contrato de origen, más allá de la estructura visible del CSV.

Se preparó una consulta de solo lectura que embebe exclusivamente las 3,233 claves ordinarias de A 2024 para cotejar su pertenencia a A/G 2024 y al catálogo territorial de la DB. El contraste G es de cobertura de claves solamente: la serie G cargada sigue copiada de 2018 y permanece en cuarentena.
### Identidades de A y G 2024 verificadas en la base viva — 26/09/2026

Alex ejecutó `HEYTI_Auditoria_DB_Electoral_2024_A_G_Identidades_Solo_Lectura.sql` y aportó la salida UTF-16. La consulta incrusta las **3,233 claves positivas únicas** del seccional SICEE A 2024; no incluye las 24 filas municipales `SECCION=0` (SHA-256 del CSV A 2024 `b6f952da0c32b7e2750a0d40c1f14e10ed915685525da8347962e224c1c9502f`). En DB hay A 2024 para **3,228/3,233**: faltan **343, 1059, 1110, 1634, 1647**, todas sin entrada en `territorial.section`; no hay claves A 2024 cargadas fuera del listado oficial.

Para las mismas 3,233 claves ordinarias hay G 2024 en **3,104** y no lo hay en **129**. Las 129 se desglosan exactamente en **124** claves presentes en el seccional G 2024 pero ausentes del seccional G 2018, todas con A 2024 e identidad territorial en DB, y las **cinco** claves históricas antes mencionadas, presentes tanto en el seccional G 2018 como en G 2024, pero ausentes de `territorial.section` y de A/G en DB. El cotejo directo de los seccionales G da 3,137 claves positivas en 2018, 3,233 en 2024, 3,109 comunes, 28 solo 2018 y 124 solo 2024. Esta estructura es congruente con la copia integral de las filas G 2018 cargadas como G 2024, ya demostrada por el JOIN de 12,424 filas.

El contraste inverso encontró **dos claves G 2024 cargadas fuera de las 3,233 secciones oficiales ordinarias 2024: 605 y 1938**. Ambas pertenecen al conjunto G 2018 pero no al G 2024; no deben mostrarse como resultados oficiales G 2024. De las 3,106 secciones G cargadas, 3,104 están en el universo ordinario G 2024 y dos quedan fuera. Por tanto, la diferencia neta de 127 entre 3,233 y 3,106 oculta **129 identidades oficiales sin G** y **dos identidades antiguas cargadas en exceso**.

**Impacto de integridad:** el problema G 2024 tiene tanto cifras copiadas en las secciones compartidas como omisión completa de las 124 altas del universo 2024, cinco identidades históricas no materializadas y dos claves de 2018 fuera del corte. Mantener la cuarentena integral G 2024. La recuperación requiere identidad territorial por vigencia y resultados versionados con fuente, modalidad y estatus; no basta actualizar valores de las 3,104 claves compartidas ni ejecutar un `UPSERT` sobre la tabla legado.


### Cobertura por identidad de todas las series 2018 y cinco series 2024 — 26/09/2026

Alex ejecutó `HEYTI_Auditoria_DB_Electoral_2018_2024_Cobertura_Identidades_Solo_Lectura.sql` y aportó su salida UTF-16. El archivo compara las 3,137 claves ordinarias SICEE A 2018 y las 3,233 claves ordinarias SICEE A 2024 con las identidades cargadas de cada elección, y hace el contraste inverso. Los seccionales federales SICEE MR 2018 para DF/S/P y RP 2024 para DF/S, más P 2024, tienen las mismas claves positivas que A del año respectivo; los seccionales locales A/DL/G de esos años también se habían cotejado. La coincidencia de universo de claves no implica igualdad de votos ni de modalidad.

Para **2018 A/DF/DL/G/P/S**, cada serie contiene **3,106/3,137** claves; las **31 ausentes son exactamente el mismo conjunto** en las seis series, todas sin entrada en `territorial.section` actual: **145, 315, 336, 343, 878, 892, 899, 966, 1059, 1078, 1099, 1110, 1268, 1285, 1477, 1490, 1494, 1495, 1509, 1614, 1634, 1642, 1647, 1681, 1687, 2190, 2193, 2477, 2514, 2860, 2907**. Es el conjunto de 29 secciones A 2021 ausentes, más **878 y 1477**, que figuran en el seccional 2018 pero no en el 2021. Ninguna de las seis series 2018 tiene claves DB fuera de la referencia ordinaria 2018.

Para **2024 A/DF/DL/P/S**, cada serie contiene **3,228/3,233** claves; las cinco ausentes son exactamente **343, 1059, 1110, 1634, 1647** en las cinco series, todas sin identidad territorial actual. Ninguna de ellas tiene claves DB fuera de la referencia ordinaria A 2024. G 2024 se contrastó en un bloque anterior: 129 oficiales sin filas y dos antiguas cargadas fuera del universo 2024 (605 y 1938). El contraste por claves no certifica los valores de las 3,228 secciones cargadas en las otras series; persisten diferencias de contenido y linaje ya documentadas.

La pérdida de identidad histórica se escalona así: **31 claves con resultado oficial 2018 no materializadas**, de ellas **29 continúan en el universo 2021**, de las cuales **cinco** continúan en el universo 2024. La DB vigente no preserva por sí sola esas trayectorias. Recuperarlas requiere un catálogo histórico versionado y fuente de geografía con vigencias verificadas; las relaciones con sucesoras no se deducen de esta consulta.

### Valores de P 2024 en la base viva frente a SICEE — 26/09/2026

Alex ejecutó `HEYTI_Auditoria_DB_P2024_Valores_vs_SICEE_Solo_Lectura.sql` y aportó la salida UTF-16. La consulta compara PAN, PRI, PVEM, MORENA, `TOTAL_VOTOS` y `LISTA_NOMINAL` de las 3,233 secciones ordinarias positivas de Guanajuato del seccional SICEE Presidencia 2024 (SHA-256 del CSV original `b7344eeaccf7a61d195b43897f5ab844c0d305383e91d86ff99965d41a2111f4`). El registro con `SECCION=0` de ese archivo se excluyó de la comparación territorial.

De 3,233 secciones fuente, **cinco no tienen filas P en DB** (identidades territoriales faltantes ya verificadas) y **3,228 sí**. Entre las cargadas, **2,449 secciones tienen al menos una diferencia** en los seis campos; 779 coinciden en los seis. Desglose de diferencias dentro de las 3,228: PAN **1,721**, PRI **1,070**, PVEM **1,235**, MORENA **1,844**, total **2,163**, LN **16**. Solo **una** sección cargada tiene menos de cuatro partidos: 1150. En ella la DB conserva únicamente PAN **1546**, con total/LN nulos; SICEE publica PAN **1246**, PRI 51, PVEM 7, MORENA 152, total 1596 y LN 2448.

El patrón de diferencias es consistente en magnitud con el cotejo previo de la maestra, descontando las cinco secciones sin identidad DB, pero el resumen agregado **no prueba igualdad exacta DB↔maestra por sección y campo** ni identifica la causa de las diferencias de la maestra. La tabla de DB no posee metadatos de corte/modalidad para resolverlas. P 2024 no supera la validación fuente→DB; sus resultados no deben etiquetarse como certificados en la entrega hasta recuperar linaje y reconstruir la materialización versionada con contraste íntegro.

### Aislamiento de la discrepancia P 2024: DB frente a maestra legado — 26/09/2026

Alex ejecutó `HEYTI_Auditoria_DB_P2024_vs_Maestra_Legado_Solo_Lectura.sql` y aportó la salida UTF-16. La referencia es el JSON `Datos_Electoral_con_2015.json` original (SHA-256 de bytes `7c0bcbfd5bdb00ac9bfafe6110cf2a916e60d68ff909773d58348e0655e945b8`) restringido a las 3,233 claves positivas de P 2024 en SICEE. Los tokens `NaN` del legado se representaron como ausencia en la consulta, sin alterar fuente o base.

Resultado: **3,228 secciones con filas P 2024 en DB y cinco sin filas**. Dentro de las 3,228, el conteo de partidos cargados coincide con el número de partidos de la maestra que tienen valor finito; hay **cero diferencias** en PAN, PRI, PVEM, MORENA, total y lista nominal, y **cero secciones con alguna diferencia**. El caso 1150 con solo PAN 1546 y total/LN ausentes también procede de la maestra tal como se comparó.

Esto ubica la discrepancia ya constatada con SICEE **antes o en la construcción del archivo maestro legado** para el universo cargado, no en una transformación numérica observable entre esa maestra y DB. La igualdad de valores y ausencias no prueba por sí misma qué ejecución concreta de ETL escribió las filas ni identifica la fuente/corte de los `24P_*` de la maestra. No sustituir silenciosamente el legado: conservarlo y continuar la investigación de su linaje, mientras el candidato oficial se prepara en staging versionado con cotejo completo.

### DF y S 2024 en DB frente a SICEE MR y RP — 26/09/2026

Alex ejecutó `HEYTI_Auditoria_DB_DF_S_2024_MR_RP_vs_SICEE_Solo_Lectura.sql` y aportó la salida UTF-16. Se compararon por separado PAN, PRI, PVEM, MORENA, total y lista nominal de las 3,233 secciones ordinarias de cada seccional federal SICEE DF/S 2024 MR/RP con la base viva. En los cuatro cruces hay cinco secciones oficiales sin filas DB y 3,228 cargadas; las cuatro filas de partido están presentes en cada sección cargada. Los conteos de diferencias son sobre las 3,228 compartidas:

| Elección | Modalidad SICEE | PAN | PRI | PVEM | MORENA | Total | LN | Secciones con algún campo distinto |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| DF 2024 | MR | 1,989 | 1,236 | 1,445 | 1,988 | 2,273 | 15 | **2,571** |
| DF 2024 | RP | 1,980 | 1,221 | 1,431 | 1,985 | 2,270 | 15 | **2,569** |
| S 2024 | MR | 2,120 | 1,295 | 1,461 | 2,131 | 2,404 | 15 | **2,678** |
| S 2024 | RP | 2,118 | 1,286 | 1,450 | 2,130 | 2,405 | 15 | **2,679** |

Las diferencias son extensas frente a **ambas** modalidades. DF tiene dos secciones menos con diferencias frente a RP que frente a MR; S tiene una menos frente a MR que frente a RP. Esas cercanías no acreditan el linaje de la maestra ni justifican asignarle modalidad. Los conteos por campo se superponen: una sección puede diferir en varios campos. El contraste previo con la maestra muestra el mismo patrón amplio al incluir las cinco claves no cargadas; aún falta un cotejo DB↔maestra por valor para DF/S si se quiere localizar formalmente la etapa en que aparecieron estas discrepancias.

### Aislamiento de DF y S 2024: DB frente a maestra legado — 26/09/2026

Alex ejecutó `HEYTI_Auditoria_DB_DF_S_2024_vs_Maestra_Legado_Solo_Lectura.sql` y compartió la salida UTF-16. Se tomaron las 3,233 claves ordinarias positivas de 2024 y los campos `24DF_*` y `24S_*` del JSON maestro original (SHA-256 de bytes `7c0bcbfd5bdb00ac9bfafe6110cf2a916e60d68ff909773d58348e0655e945b8`); los `NaN` se representaron como ausencia solo dentro de la consulta.

En **DF y S**, por separado, hay **3,228 secciones con filas DB** y cinco sin filas. Entre las 3,228 secciones cargadas de cada serie, hay **cero diferencias DB↔maestra** en PAN, PRI, PVEM, MORENA, total y LN, y cero diferencias en el número de partidos presentes. Así, igual que en P 2024, la diferencia observada contra SICEE MR y RP **ya aparece en la maestra legado** de DF/S para el universo cargado; no se observó alteración numérica adicional al materializar esos seis campos en DB.

Este cotejo no identifica el origen/corte de los valores `24DF_*` o `24S_*`, ni prueba por sí mismo qué ejecución cargó la tabla. La coincidencia DB↔maestra no certifica esos bloques contra SICEE; preservarlos como legado y no seleccionar MR/RP por mera proximidad de conteos. Queda pendiente localizar su generador o un manifiesto de fuente, y preparar un candidato con procedencia y modalidad explícitas.
