# HEYTI Data Truth Governance v1.0

## Capítulo 1. Propósito, alcance y principios de gobernanza de verdad de datos

### 1.1 Propósito

El presente documento establece el marco normativo de gobernanza de verdad de datos de HEYTI-CORE.

Su función es definir, preservar y hacer auditable la diferencia entre:

- datos observados;
- ceros oficiales;
- datos faltantes;
- ceros introducidos por transformaciones;
- valores derivados;
- valores trasladados entre periodos;
- secciones históricas;
- secciones actuales;
- secciones producto de reseccionamiento;
- relaciones territoriales certificadas;
- relaciones territoriales todavía no resueltas;
- datos certificados;
- datos provisionales;
- datos rechazados.

Este documento constituye la referencia normativa principal para cualquier proceso de:

- integración de fuentes;
- ETL;
- carga a base de datos;
- reconciliación fuente → DB;
- ejecución de capabilities;
- Runtime;
- Materialization;
- visualización;
- mapas;
- gráficas;
- tablas;
- reportes;
- respuestas generadas por HEYTI;
- pruebas Golden Case;
- pruebas de regresión;
- auditorías posteriores.

### 1.2 Objetivo fundamental

HEYTI no debe limitarse a conocer un valor.

HEYTI debe conocer también:

> qué representa ese valor,
> de dónde proviene,
> a qué periodo corresponde,
> bajo qué universo territorial fue generado,
> qué transformaciones recibió,
> qué nivel de certificación posee
> y qué restricciones existen para utilizarlo.

Por lo tanto, el sistema deberá preservar la naturaleza semántica y temporal de cada dato a lo largo de toda la cadena:

**Fuente → ETL → Base de Datos → Capability → Runtime → Materialization → UI**

### 1.3 Principio rector

La gobernanza de verdad de datos de HEYTI se fundamenta en el siguiente principio:

> **Una transformación técnica no puede crear una verdad que no exista en la fuente.**

Por consecuencia:

- ausencia no equivale a cero;
- un `fillna(0)` no genera un cero electoral oficial;
- un merge no convierte un dato inexistente en dato observado;
- una copia entre periodos no constituye evidencia electoral nueva;
- una sección ausente del universo territorial actual puede seguir siendo válida históricamente;
- una relación de reseccionamiento no autoriza automáticamente la redistribución de votos, casillas, actores o indicadores.

### 1.4 Alcance

Este marco aplica a todos los dominios actuales y futuros de HEYTI-CORE, incluyendo como mínimo:

- Territorial;
- Spatial;
- Electoral;
- Socioeconómico;
- Campo;
- Día D;
- ET-27;
- Inteligencia Territorial;
- Analytics;
- Productos de Inteligencia;
- Materialization;
- Runtime;
- interfaces de usuario.

También será obligatorio para cualquier nueva fuente, módulo, capability, visualización o producto de inteligencia que se incorpore posteriormente.

### 1.5 Regla de obligatoriedad

Toda persona que participe en el desarrollo, mantenimiento, migración o ampliación de HEYTI-CORE deberá conocer este documento antes de modificar:

- fuentes de datos;
- scripts ETL;
- modelos de base de datos;
- contratos;
- capabilities;
- Runtime;
- Materialization;
- módulos;
- visualizaciones;
- pruebas.

Esta lectura deberá formar parte del proceso obligatorio de incorporación de nuevos desarrolladores definido en:

`docs/onboarding/HEYTI_Developer_Onboarding_Manual_v1.0.md`

### 1.6 Principios de gobernanza

#### 1.6.1 Trazabilidad

Todo dato utilizado por HEYTI deberá poder relacionarse con una fuente, proceso o evidencia identificable.

#### 1.6.2 Temporalidad

La validez territorial y electoral deberá evaluarse de acuerdo con el periodo correspondiente.

#### 1.6.3 No equivalencia entre ausencia y cero

Un dato inexistente, no disponible o no compatible no deberá representarse automáticamente como cero.

#### 1.6.4 No creación de evidencia

Las transformaciones deberán preservar el significado original de la información y no crear observaciones inexistentes.

#### 1.6.5 Separación entre dato observado y dato derivado

Los valores calculados deberán identificarse explícitamente como derivados.

#### 1.6.6 Separación entre historia y territorio vigente

Una sección histórica podrá conservar información electoral válida aunque ya no pertenezca al universo territorial actual.

#### 1.6.7 Reasignación territorial controlada

Ningún dato histórico podrá reasignarse automáticamente a una sección sucesora sin evidencia específica y certificada.

#### 1.6.8 Certificación explícita

HEYTI deberá distinguir entre información certificada, provisional y rechazada.

#### 1.6.9 Propagación de verdad

El estado semántico de un dato deberá mantenerse desde la fuente hasta la capa de presentación.

#### 1.6.10 Auditabilidad

Toda decisión de integración, transformación, clasificación o certificación deberá poder reproducirse y auditarse.

### 1.7 Principio de presentación al usuario

Una visualización no deberá presentar como dato observado aquello que internamente haya sido clasificado como:

- `SOURCE_MISSING`;
- `TRANSFORMATION_ZERO`;
- `CARRY_FORWARD`;
- `UNAVAILABLE`;
- `REJECTED`.

Cuando información provisional o derivada sea utilizada, la interfaz deberá conservar su naturaleza semántica.

### 1.8 Relación con la auditoría HDRM

Este documento nace como resultado directo de la auditoría de preparación de datos y migración de módulos del Sprint 24.

Durante dicha auditoría se identificaron, entre otros, los siguientes fenómenos:

- desalineación entre universo electoral histórico y universo territorial actual;
- secciones históricas ausentes del GeoJSON vigente;
- reseccionamientos certificados;
- secciones sucesoras vigentes;
- omisiones en el universo maestro;
- valores faltantes convertidos en cero por procesos de transformación;
- valores 2024 derivados mediante copia exacta de datos 2018.

Estos hallazgos demostraron la necesidad de establecer un contrato explícito de verdad de datos.

### 1.9 Caso certificado: carry-forward 18G → 24G

La auditoría global del maestro electoral determinó:

- 3,137 secciones comparables;
- 3,137 coincidencias exactas;
- 0 diferencias;
- 100.00 % de igualdad entre `18G_*` y `24G_*`.

Por lo tanto, hasta que exista evidencia primaria independiente que demuestre lo contrario:

`24G_*`

deberá clasificarse como:

`CARRY_FORWARD`

con procedencia:

`DERIVED_FROM_18G`

y no como resultado electoral observado de 2024.

### 1.10 Caso certificado: sección 2788

La sección `2788` fue identificada como sección válida en fuentes oficiales de 2015 para:

- Ayuntamiento;
- Diputación Federal;
- Diputación Local.

También fue localizada en la fuente federal 2015 correspondiente a Guanajuato.

Sin embargo, no existe en:

- `Datos_Electoral_Respaldo.json`;
- `Datos_Electoral.json`;
- `Datos_Electoral_con_2015.json`;
- dataset equivalente integrado en HEYTI-CORE.

La causa auditada es:

`BASE_MASTER_OMISSION`

El proceso de integración de 2015 utilizó el maestro existente como universo base mediante `left merge`, por lo que una sección ausente del maestro no podía incorporarse posteriormente.

### 1.11 Caso certificado: reseccionamiento 2023

La auditoría identificó cinco secciones históricas con sucesores territoriales certificados:

- `343` → `3290–3299`
- `1059` → `3300–3307`
- `1110` → `3308–3313`
- `1634` → `3278–3283`
- `1647` → `3284–3289`

Los 36 sucesores se encuentran presentes tanto en:

- el GeoJSON territorial vigente;
- `territorial.section`.

Esta relación certifica genealogía territorial, pero no autoriza automáticamente la redistribución de datos históricos hacia las secciones sucesoras.

### 1.12 Caso certificado: impacto en casillas

Las cinco secciones reseccionadas anteriores explican exactamente los 97 registros de casillas rechazados durante la carga histórica:

- sección 343 → 22 registros;
- sección 1059 → 18 registros;
- sección 1110 → 17 registros;
- sección 1634 → 20 registros;
- sección 1647 → 20 registros.

Total:

`97`

Reconciliación:

`PASS`

La causa corresponde a una diferencia temporal entre el universo de secciones del archivo histórico de casillas y el universo territorial vigente.

### 1.13 Regla de protección de evidencia histórica

HEYTI deberá preservar información histórica válida aun cuando la entidad territorial asociada ya no forme parte del universo vigente.

Por lo tanto:

> Una sección que deja de existir territorialmente no deja de existir históricamente.

Esta regla será obligatoria en el diseño futuro de:

- `territorial.section_history`;
- consultas históricas;
- capabilities electorales;
- análisis longitudinales;
- Materialization;
- visualizaciones temporales.

### 1.14 Estado del documento

Versión inicial:

`v1.0`

Estado:

`ACTIVE — NORMATIVE BASELINE`

Origen:

`Sprint 24 — HEYTI Data Readiness & Module Migration`

El documento deberá actualizarse únicamente mediante cambios controlados y auditables.

---

## Capítulo 2. Taxonomía formal de estados de verdad

### 2.1 Propósito de la taxonomía

La taxonomía de estados de verdad define cómo HEYTI-CORE deberá clasificar la naturaleza semántica de los datos que recibe, transforma, almacena, consulta, materializa y presenta.

El objetivo es impedir que datos con significados distintos sean tratados como si fueran equivalentes.

Por ejemplo:

- un valor observado no es igual a un valor derivado;
- un cero oficial no es igual a un cero generado por transformación;
- una ausencia de datos no es igual a cero;
- un valor copiado entre periodos no es igual a una observación nueva;
- una sección histórica no es igual a una sección vigente;
- una relación territorial no resuelta no es igual a una genealogía certificada.

La taxonomía será obligatoria para toda la cadena:

**Fuente → ETL → DB → Capability → Runtime → Materialization → UI**

### 2.2 Dimensiones de clasificación

La verdad de datos deberá clasificarse, como mínimo, mediante tres dimensiones independientes:

1. `truth_status`
2. `territorial_status`
3. `certification_status`

Estas dimensiones no deberán mezclarse.

Un dato puede ser, por ejemplo:

- `OBSERVED_DATA`
- asociado a una `HISTORICAL_SECTION`
- y estar `CERTIFIED`.

Otro dato puede ser:

- `CARRY_FORWARD`
- asociado a una `HISTORICAL_SECTION`
- y estar `CERTIFIED` respecto de su condición de copia.

La certificación no significa necesariamente que el dato sea observado.

Puede certificarse precisamente que un dato es derivado, faltante, copiado o histórico.

### 2.3 `truth_status`

`truth_status` describe la naturaleza del valor.

Los valores permitidos en v1.0 son:

- `OBSERVED_DATA`
- `OFFICIAL_ZERO`
- `SOURCE_MISSING`
- `TRANSFORMATION_ZERO`
- `CARRY_FORWARD`
- `DERIVED_DATA`
- `UNAVAILABLE`

### 2.4 `OBSERVED_DATA`

Dato localizado directamente en una fuente identificable y válida para una entidad, sección, elección, periodo o indicador.

Para clasificarse como `OBSERVED_DATA`, deberán conocerse fuente, periodo, entidad, variable, valor y evidencia de procedencia.

### 2.5 `OFFICIAL_ZERO`

Valor igual a cero que aparece explícitamente en una fuente válida.

Un cero solamente podrá clasificarse como `OFFICIAL_ZERO` cuando la fuente exprese explícitamente el valor cero.

No podrá inferirse mediante ausencia, `NULL`, campo inexistente, error de join, `fillna(0)` o valor por defecto.

### 2.6 `SOURCE_MISSING`

Estado utilizado cuando el dato esperado no existe en la fuente correspondiente.

`SOURCE_MISSING` significa:

> No existe evidencia suficiente del valor en la fuente consultada.

No significa `0`.

Regla formal:

`SOURCE_MISSING != OFFICIAL_ZERO`

### 2.7 `TRANSFORMATION_ZERO`

Valor cero creado por una operación técnica y no observado directamente en la fuente.

Ejemplos:

- `fillna(0)`
- `COALESCE(value, 0)`
- inicialización de columnas con cero;
- valor por defecto;
- sustitución posterior a un merge sin coincidencia.

Un `TRANSFORMATION_ZERO` deberá conservar trazabilidad hacia la transformación que lo generó.

### 2.8 `CARRY_FORWARD`

Valor reutilizado desde otro periodo o contexto.

Todo `CARRY_FORWARD` deberá registrar campo y periodo de origen, campo y periodo destino, regla de transformación y evidencia.

Caso certificado HEYTI:

`18G_* == 24G_*` en `3137 / 3137` secciones comparables.

Por lo tanto, `24G_*` se clasifica como `CARRY_FORWARD` hasta que exista evidencia primaria independiente de 2024.

### 2.9 `DERIVED_DATA`

Valor calculado mediante una regla, fórmula o modelo a partir de uno o varios datos de entrada.

Todo `DERIVED_DATA` deberá registrar fuentes de entrada, fórmula o algoritmo, versión, periodo de cálculo y evidencia de reproducibilidad.

### 2.10 `UNAVAILABLE`

Estado utilizado cuando HEYTI no puede proporcionar un valor confiable bajo las reglas de certificación vigentes.

HEYTI deberá preferir `UNAVAILABLE` antes que inventar, completar, estimar o simular silenciosamente un valor.

### 2.11 `territorial_status`

Describe la situación temporal y territorial de una sección o entidad geográfica.

Valores iniciales:

- `CURRENT_SECTION`
- `HISTORICAL_SECTION`
- `RESECTION_PREDECESSOR`
- `RESECTION_SUCCESSOR`

La genealogía y anomalías se mantendrán como dimensiones separadas para evitar mezclar conceptos ortogonales.

### 2.12 `CURRENT_SECTION`

Sección perteneciente al universo territorial vigente certificado.

En la baseline auditada de HEYTI, el universo territorial vigente contiene `3266` secciones.

### 2.13 `HISTORICAL_SECTION`

Sección válida en un periodo anterior pero ausente del universo territorial vigente.

La ausencia actual no invalida los datos históricos observados.

### 2.14 `RESECTION_PREDECESSOR`

Sección histórica cuya sustitución por una o más secciones nuevas ha sido respaldada mediante evidencia de reseccionamiento.

Casos actualmente certificados:

- `343`
- `1059`
- `1110`
- `1634`
- `1647`

### 2.15 `RESECTION_SUCCESSOR`

Sección actual identificada como resultado certificado del reseccionamiento de una sección predecesora.

Casos actualmente certificados: `3278–3313`.

Ser sucesora territorial no implica recibir automáticamente votos, casillas, actores, indicadores, scores o resultados históricos.

### 2.16 `genealogy_status`

La genealogía deberá mantenerse como dimensión independiente.

Valores iniciales:

- `CERTIFIED_MAPPING`
- `UNRESOLVED`
- `NOT_APPLICABLE`

Cuando una sección histórica no tenga sucesión certificada:

`genealogy_status = UNRESOLVED`

### 2.17 `anomaly_code`

Las anomalías de procedencia o integración no deberán competir con el estado territorial.

Ejemplos:

- `MASTER_OMISSION`
- `TEMPORAL_UNIVERSE_MISMATCH`
- `CARRY_FORWARD_18G_TO_24G`
- `TRANSFORMATION_FILLNA_ZERO`

### 2.18 `certification_status`

Representa el grado de validación alcanzado por un dato, relación o hallazgo.

Valores:

- `CERTIFIED`
- `PROVISIONAL`
- `REJECTED`

### 2.19 Independencia de dimensiones

Ejemplo:

```text
truth_status = OBSERVED_DATA
territorial_status = HISTORICAL_SECTION
genealogy_status = UNRESOLVED
certification_status = CERTIFIED
anomaly_code = NONE
```

Ejemplo:

```text
truth_status = CARRY_FORWARD
territorial_status = HISTORICAL_SECTION
certification_status = CERTIFIED
anomaly_code = CARRY_FORWARD_18G_TO_24G
```

Ejemplo 2788:

```text
truth_status = OBSERVED_DATA
territorial_status = HISTORICAL_SECTION
certification_status = CERTIFIED
anomaly_code = MASTER_OMISSION
```

### 2.20 Estados prohibidos por inferencia automática

Queda prohibida cualquier transformación automática de:

```text
SOURCE_MISSING → OFFICIAL_ZERO
TRANSFORMATION_ZERO → OBSERVED_DATA
CARRY_FORWARD → OBSERVED_DATA
UNRESOLVED → CERTIFIED_MAPPING
PROVISIONAL → CERTIFIED
```

sin evidencia y proceso formal de certificación.

### 2.21 Regla de persistencia semántica

El sistema no deberá perder información sobre procedencia, transformación, estado de verdad, temporalidad y certificación durante:

**Fuente → ETL → DB → Capability → Runtime → Materialization → UI**

### 2.22 Compatibilidad con Golden Cases

Los Golden Cases deberán verificar tanto el valor como su estado de verdad correcto.

---

## Capítulo 3. Truth Status Contract y estructura mínima de trazabilidad

### 3.1 Propósito

El Truth Status Contract define la estructura mínima que deberá acompañar a cualquier dato relevante que HEYTI-CORE utilice para almacenamiento, transformación, consulta, razonamiento, materialización, visualización, respuesta y auditoría.

### 3.2 Principio contractual

Todo dato relevante deberá poder representarse conceptualmente mediante:

```text
value
truth_status
territorial_status
genealogy_status
certification_status
anomaly_code
source_dataset
source_period
source_election_type
section_code
derived_from
transformation_rule
evidence_reference
```

### 3.3 Campos de procedencia

Se consideran parte del contrato extendido:

```text
source_field
target_field
target_period
transformation_version
certified_at
certification_evidence
```

### 3.4 `source_dataset`

Identificador lógico de la fuente de origen.

Ejemplos:

```text
ELECTORAL_2015_AYUNTAMIENTO
ELECTORAL_2015_DF
ELECTORAL_2015_DL
CURRENT_SECTION_GEOMETRY
FIELD_POINTS
CASILLA_SOURCE
SOCIOECONOMIC_SECTION_DATA
```

El nombre lógico deberá ser preferentemente independiente del nombre físico del archivo.

### 3.5 `section_code`

El código territorial no deberá interpretarse como identidad eterna.

Conceptualmente:

```text
section_code + period
```

es una identidad más segura que `section_code` aislado.

### 3.6 `derived_from`

Deberá utilizarse para `DERIVED_DATA`, `CARRY_FORWARD` y `TRANSFORMATION_ZERO` cuando sea aplicable.

### 3.7 `transformation_rule`

Ejemplos:

```text
COPY_18G_TO_24G
FILL_MISSING_WITH_ZERO
LEFT_JOIN_BY_SECTION
PARTICIPATION_PERCENTAGE
ELECTORAL_MARGIN
SECTION_SCORE_V1
```

### 3.8 `evidence_reference`

Podrá referir a archivo, hash, reporte HDRM, consulta SQL, prueba, Golden Case o documento oficial.

### 3.9 Ejemplo: dato electoral observado

```text
section_code = 2788
source_period = 2015
source_election_type = DF
value = 83
truth_status = OBSERVED_DATA
territorial_status = HISTORICAL_SECTION
certification_status = CERTIFIED
source_dataset = ELECTORAL_2015_DF
anomaly_code = MASTER_OMISSION
```

### 3.10 Ejemplo: carry-forward certificado

```text
source_field = 18G_TOTAL
target_field = 24G_TOTAL
source_period = 2018
target_period = 2024
truth_status = CARRY_FORWARD
certification_status = CERTIFIED
transformation_rule = COPY_18G_TO_24G
```

### 3.11 Ejemplo: transformación a cero

```text
value = 0
truth_status = TRANSFORMATION_ZERO
certification_status = CERTIFIED
transformation_rule = FILL_MISSING_WITH_ZERO
```

No deberá clasificarse como `OFFICIAL_ZERO`.

### 3.12 Invariantes

- `SOURCE_MISSING` no puede convertirse silenciosamente en `OFFICIAL_ZERO`.
- `CARRY_FORWARD` no puede presentarse como `OBSERVED_DATA`.
- `RESECTION_PREDECESSOR` no autoriza transferencia automática.
- `REJECTED` no puede ingresar a productos certificados.
- La pérdida de `truth_status` en DB → Capability → Runtime → Materialization constituye violación contractual.

### 3.13 Regla para fuentes legacy

Una fuente legacy podrá conservarse como evidencia histórica aunque no cumpla físicamente el contrato, pero deberá disponer de clasificación, procedencia, estado de verdad, evidencia y certificación antes de alimentar HEYTI.

### 3.14 Regla para nuevas fuentes

Toda nueva fuente deberá definir desde su ingreso:

```text
source_dataset
source_period
truth_status
certification_status
```

y, cuando aplique:

```text
territorial_status
genealogy_status
section_code
source_election_type
transformation_rule
```

### 3.15 Regla para Runtime y Materialization

Runtime deberá recibir metadata suficiente para distinguir observado, derivado, histórico, faltante, provisional y no disponible.

Materialization deberá impedir que un `CARRY_FORWARD`, `SOURCE_MISSING`, `TRANSFORMATION_ZERO` o `UNAVAILABLE` se convierta en afirmación observada.

### 3.16 Baseline contractual

La estructura definida constituye:

`HEYTI Truth Status Contract v1.0`

Estado:

`NORMATIVE BASELINE`

---

## Capítulo 4. Reglas de transición y matriz de estados permitidos/prohibidos

### 4.1 Propósito

Define las transiciones permitidas y prohibidas entre estados de verdad, territoriales, genealógicos y de certificación.

### 4.2 Principio de monotonía epistemológica

> Una capa posterior no puede afirmar más de lo que la evidencia disponible permite.

### 4.3 Transiciones permitidas con evidencia adicional

- `SOURCE_MISSING → OBSERVED_DATA`: solo cuando aparece fuente válida.
- `SOURCE_MISSING → OFFICIAL_ZERO`: solo cuando fuente válida expresa cero.
- `UNAVAILABLE → OBSERVED_DATA`: solo con nueva fuente válida.
- `PROVISIONAL → CERTIFIED`: solo mediante certificación formal.
- `UNRESOLVED → CERTIFIED_MAPPING`: solo con genealogía respaldada.

### 4.4 Transiciones prohibidas automáticas

```text
SOURCE_MISSING → OFFICIAL_ZERO
SOURCE_MISSING → OBSERVED_DATA
TRANSFORMATION_ZERO → OFFICIAL_ZERO
TRANSFORMATION_ZERO → OBSERVED_DATA
CARRY_FORWARD → OBSERVED_DATA
DERIVED_DATA → OBSERVED_DATA
UNAVAILABLE → OBSERVED_DATA
```

sin evidencia adicional.

### 4.5 Regla para `CARRY_FORWARD`

Un valor `CARRY_FORWARD` conservará esa clasificación mientras no exista evidencia primaria independiente para el periodo destino.

### 4.6 Regla territorial

`HISTORICAL_SECTION → RESECTION_PREDECESSOR` solo con evidencia suficiente de reseccionamiento.

`genealogy_status = UNRESOLVED` puede pasar a `CERTIFIED_MAPPING` únicamente con evidencia.

### 4.7 Reseccionamiento

La genealogía territorial no autoriza transferir automáticamente votos, casillas, actores, indicadores socioeconómicos, scores o recomendaciones.

### 4.8 Transiciones de certificación

Permitidas:

```text
PROVISIONAL → CERTIFIED
PROVISIONAL → REJECTED
```

Excepcionales y auditadas:

```text
CERTIFIED → PROVISIONAL
CERTIFIED → REJECTED
```

### 4.9 Prohibición de autocertificación

Un ETL, Capability, Runtime o Materialization no puede asignar `CERTIFIED` simplemente porque terminó sin error.

Éxito técnico no equivale a certificación semántica.

### 4.10 Preservación histórica de transiciones

Toda transición deberá conservar estado anterior, estado nuevo, razón, fecha, evidencia, actor o proceso y versión.

### 4.11 Principio final

> **Ningún dato podrá volverse más verdadero por efecto de una transformación técnica.**

Solo nueva evidencia podrá incrementar su nivel de certeza.

---

## Capítulo 5. Modelo temporal de secciones y genealogía territorial

### 5.1 Propósito

Define cómo HEYTI-CORE deberá representar la identidad temporal de las secciones electorales y sus relaciones de sucesión territorial.

### 5.2 Principio de identidad temporal

Conceptualmente:

```text
section_identity =
section_code
+
valid_period
+
territorial_status
```

### 5.3 Sección vigente

`CURRENT_SECTION` cuando forme parte del universo territorial vigente certificado.

Baseline:

`CURRENT_SECTION_UNIVERSE = 3266`

### 5.4 Sección histórica

`HISTORICAL_SECTION` cuando exista evidencia válida de su existencia en un periodo anterior aunque ya no pertenezca al universo territorial vigente.

> Una sección que deja de existir territorialmente no deja de existir históricamente.

### 5.5 Casos certificados de reseccionamiento 2023

```text
343  → 3290–3299
1059 → 3300–3307
1110 → 3308–3313
1634 → 3278–3283
1647 → 3284–3289
```

Validación:

```text
EXPECTED_SUCCESSORS = 36
FOUND_IN_CURRENT_GEO = 36
FOUND_IN_TERRITORIAL_SECTION = 36
SUCCESSOR_RECONCILIATION = PASS
```

### 5.6 Genealogía no implica equivalencia

`343 → 3290–3299` expresa sucesión territorial, no equivalencia numérica ni reparto automático.

### 5.7 Regla para datos electorales históricos

Los resultados históricos deberán permanecer asociados a la sección histórica que los produjo.

### 5.8 Regla para casillas

Los 97 registros rechazados corresponden exactamente a las cinco secciones reseccionadas, pero no se podrá determinar automáticamente a qué sucesora corresponde cada casilla sin evidencia adicional.

### 5.9 Geometría histórica

HEYTI deberá distinguir `CURRENT_GEOMETRY` de `HISTORICAL_GEOMETRY`.

La falta de geometría histórica no deberá eliminar los datos históricos.

### 5.10 Genealogía no resuelta

Las 26 secciones históricas restantes deberán utilizar:

```text
territorial_status = HISTORICAL_SECTION
genealogy_status = UNRESOLVED
```

hasta contar con evidencia de sucesión.

### 5.11 Caso 2788

```text
section_code = 2788
territorial_status = HISTORICAL_SECTION
anomaly_code = MASTER_OMISSION
```

`MASTER_OMISSION` no equivale a inexistencia.

### 5.12 `territorial.section_history`

La estructura existe, pero no contiene genealogía poblada.

No deberá modificarse durante la fase actual de auditoría.

### 5.13 Modelo conceptual futuro

Podrá requerirse una relación especializada:

`territorial.section_lineage`

con soporte para relaciones `1 → N`, `N → 1` y eventualmente `N → N`.

No se autoriza todavía su creación.

### 5.14 Regla de unión temporal

Una unión entre datos electorales y territoriales deberá considerar:

```text
section_code + applicable_period
```

y no solo `section_code`.

### 5.15 Regla de no descarte

El patrón futuro deberá evolucionar de:

```text
SECTION NOT FOUND → SKIP
```

a:

```text
SECTION NOT CURRENT
→ CHECK HISTORY
→ CLASSIFY
→ PRESERVE OR ROUTE
```

### 5.16 Invariantes territoriales

```text
NOT_CURRENT != INVALID
HISTORICAL_SECTION puede conservar OBSERVED_DATA
RESECTION_PREDECESSOR no transfiere automáticamente datos
genealogy_status = UNRESOLVED bloquea reasignación
MASTER_OMISSION no invalida evidencia oficial
```

---

## Capítulo 6. Reglas de fuentes, procedencia y autoridad de datos

### 6.1 Propósito

Define cómo HEYTI-CORE deberá identificar, clasificar y priorizar fuentes de información.

### 6.2 Principio de autoridad

```text
FILE_EXISTS != SOURCE_AUTHORITY
```

Una fuente será autoritativa únicamente cuando exista evidencia suficiente sobre origen, propósito, periodo, dominio, integridad, vigencia y trazabilidad.

### 6.3 Clasificación mínima de fuentes

```text
AUTHORITATIVE_SOURCE
CERTIFIED_SOURCE
DERIVED_SOURCE
INTERMEDIATE_SOURCE
AUDIT_EVIDENCE
BACKUP_SOURCE
LEGACY_SOURCE
UNVERIFIED_SOURCE
REJECTED_SOURCE
SIMULATED_SOURCE
```

### 6.4 Fuente física vs identidad lógica

HEYTI deberá distinguir:

```text
physical_filename
logical_source_id
```

Ejemplo:

`Datos_Electoral_con_2015.json`

podrá representar conceptualmente:

`ELECTORAL_MASTER`

### 6.5 Regla de nombres

Los años no deberán formar parte obligatoria del nombre lógico cuando el dataset representa un dominio continuo.

Durante la auditoría:

`NO_RENAME`

### 6.6 Procedencia mínima

Toda fuente deberá poder describirse mediante:

```text
source_id
source_type
physical_location
logical_name
origin
period
domain
hash
record_count
key_definition
certification_status
```

### 6.7 Hash

Cuando sea apropiado deberá registrarse SHA-256 para verificar identidad, detectar cambios, comparar copias y certificar reproducibilidad.

### 6.8 Universo y cobertura

Toda fuente relevante deberá declarar, cuando aplique:

```text
expected_count
observed_count
unique_keys
duplicates
missing_keys
```

### 6.9 Autoridad por dominio

Una fuente puede ser válida para un propósito y no para otro.

Una fuente electoral puede ser autoritativa para votos, pero no para geometría.

### 6.10 Conflicto entre fuentes

Cuando dos fuentes válidas se contradigan:

`SOURCE_CONFLICT`

HEYTI no deberá escoger silenciosamente una.

### 6.11 Fuente más reciente no siempre gana

Cartografía actual no invalida resultados históricos.

### 6.12 Reconciliación fuente → DB

Antes de certificar una carga deberán compararse conteos, llaves e identidad semántica.

Resultados posibles:

```text
PASS
PASS_WITH_EXPLAINED_DELTA
FAIL
OPEN
BLOCKED
```

### 6.13 Caso casillas

```text
source = 8144
database = 8047
delta = 97
```

Los 97 registros fueron explicados por las cinco secciones reseccionadas.

Resultado:

`PASS_WITH_EXPLAINED_DELTA`

### 6.14 Caso 2788

```text
AUTHORITATIVE_2015_SOURCE = PRESENT
MASTER = ABSENT
anomaly_code = MASTER_OMISSION
```

### 6.15 Regla de transformación

Toda transformación deberá declarar si conserva, agrega, filtra, copia, rellena, proyecta, reasigna o elimina.

`fillna(0)` sobre ausencia deberá producir `TRANSFORMATION_ZERO`.

Una copia entre periodos deberá producir `CARRY_FORWARD`.

### 6.16 Fuente simulada

Toda fuente simulada deberá identificarse:

`SIMULATED_SOURCE`

y nunca presentarse como `AUTHORITATIVE_SOURCE` ni `OBSERVED_DATA`.

### 6.17 Caso socioeconómico V1

Si V1 genera valores DEMO ante ausencia de fuente, HEYTI-CORE deberá tratarlos como simulados.

La simulación silenciosa queda prohibida para respuestas certificadas.

### 6.18 Registro de fuentes

HEYTI deberá evolucionar hacia un catálogo conceptual como:

`metadata.source_registry`

No se autoriza todavía su creación física.

### 6.19 Invariantes de procedencia

```text
FILE_EXISTS != AUTHORITATIVE_SOURCE
BACKUP != ACTIVE_SOURCE
DERIVED_SOURCE debe conocer derived_from
SIMULATED_SOURCE != OBSERVED_DATA
una diferencia fuente→DB no puede cerrarse sin explicación
```

---

## Capítulo 7. Reconciliación, certificación y cierre de incidencias de datos

### 7.1 Propósito

Define cómo HEYTI-CORE deberá registrar, investigar, reconciliar, certificar y cerrar incidencias relacionadas con datos.

### 7.2 Estados de una incidencia

```text
OPEN
UNDER_INVESTIGATION
EXPLAINED
CERTIFIED
BLOCKED
REJECTED
CLOSED
```

### 7.3 Regla crítica

```text
EXPLAINED != CLOSED
CERTIFIED != CORRECTED
IMPLEMENTED != VERIFIED
```

### 7.4 Dimensiones independientes

Toda incidencia deberá distinguir:

```text
diagnosis_status
remediation_status
```

Ejemplo:

```text
diagnosis_status = CERTIFIED
remediation_status = PENDING
```

### 7.5 Estados de remediación

```text
NOT_REQUIRED
PENDING
PLANNED
IN_PROGRESS
IMPLEMENTED
VERIFIED
DEFERRED
```

### 7.6 Incidente 24G

```text
incident_type = TEMPORAL_DATA_PROVENANCE
diagnosis_status = CERTIFIED
remediation_status = PENDING
truth_status = CARRY_FORWARD
```

Hallazgo:

`3137 / 3137` registros comparables tienen `18G_* == 24G_*`.

### 7.7 Incidente sección 2788

```text
incident_type = MASTER_OMISSION
diagnosis_status = CERTIFIED
remediation_status = PENDING
```

Causa:

`BASE_MASTER_OMISSION`

### 7.8 Cinco reseccionamientos

Genealogía certificada:

```text
343  → 3290–3299
1059 → 3300–3307
1110 → 3308–3313
1634 → 3278–3283
1647 → 3284–3289
```

### 7.9 Incidente 97 casillas

```text
SOURCE = 8144
DB = 8047
DELTA = 97
```

Explicación:

```text
343  = 22
1059 = 18
1110 = 17
1634 = 20
1647 = 20
TOTAL = 97
```

Resultado:

`PASS_WITH_EXPLAINED_DELTA`

La reasignación individual de casillas sigue siendo un problema separado.

### 7.10 Genealogías no resueltas

Para las 26 secciones históricas:

```text
territorial_status = HISTORICAL_SECTION
genealogy_status = UNRESOLVED
diagnosis_status = CERTIFIED
```

Cualquier reasignación queda `BLOCKED`.

### 7.11 Tipos de incidencias

```text
SOURCE_MISMATCH
SOURCE_TO_MASTER_OMISSION
SOURCE_TO_DB_OMISSION
TEMPORAL_UNIVERSE_MISMATCH
TERRITORIAL_GENEALOGY_GAP
CARRY_FORWARD_DETECTED
TRANSFORMATION_ZERO_DETECTED
SOURCE_CONFLICT
INVALID_SOURCE
SIMULATED_DATA_RISK
DUPLICATE_KEY
COUNT_MISMATCH
SEMANTIC_MISMATCH
```

### 7.12 Identificador

Se recomienda formato:

```text
DTI-ELECTORAL-001
DTI-TERRITORIAL-001
DTI-CASILLA-001
```

`DTI = Data Truth Incident`

### 7.13 Registro conceptual

```text
incident_id
incident_type
domain
description
source_reference
affected_period
affected_entities
expected_state
observed_state
diagnosis_status
remediation_status
root_cause
truth_impact
business_impact
evidence_reference
resolution_rule
opened_at
certified_at
closed_at
```

### 7.14 Reconciliación cuantitativa, de llaves, semántica y temporal

Deberán compararse:

```text
expected_count
observed_count
delta
source_keys
database_keys
only_in_source
only_in_database
common
duplicates
```

Y además:

```text
section
+
period
+
election_type
```

cuando aplique.

### 7.15 Regla de cero omisiones

> Cero omisiones significa que todo delta está explicado, no necesariamente que el delta sea cero.

### 7.16 Ledger de diferencias

Toda reconciliación con delta deberá poder producir:

```text
key
source_state
target_state
difference_type
explanation
certification_status
```

Y deberá cumplirse:

```text
sum(classified_differences) = total_delta
```

### 7.17 Root Cause Analysis

Toda incidencia crítica deberá distinguir:

```text
ROOT_CAUSE
DOWNSTREAM_EFFECT
```

Ejemplo 2788:

```text
ROOT_CAUSE:
2788 absent from master

DOWNSTREAM_EFFECT:
2015 integration cannot include 2788
```

### 7.18 Criterios de certificación

Una incidencia podrá alcanzar `CERTIFIED` cuando existan:

1. evidencia identificada;
2. causa explicada;
3. resultados reproducibles;
4. diferencias contabilizadas;
5. interpretación semántica definida;
6. ausencia de contradicciones relevantes.

### 7.19 Reapertura

Una incidencia `CLOSED` deberá poder pasar nuevamente a `OPEN` si aparece evidencia nueva, preservando el historial anterior.

### 7.20 Impacto de verdad

Valores conceptuales:

```text
NONE
LOW
MEDIUM
HIGH
CRITICAL
```

Una incidencia será candidata a `CRITICAL` cuando pueda provocar dato falso, atribución electoral incorrecta, pérdida de historia, mapa incorrecto, reasignación territorial falsa o decisión operativa basada en evidencia inexistente.

### 7.21 Regla de bloqueo de migración

Una incidencia deberá bloquear migración cuando:

```text
truth_impact = CRITICAL
```

y:

```text
diagnosis_status != CERTIFIED
```

si afecta directamente a la capacidad que pretende migrarse.

### 7.22 Incidencias y Golden Cases

Toda incidencia crítica cerrada deberá considerarse candidata a convertirse en Golden Case.

Ejemplos:

```text
GC-ELECTORAL-24G-001
GC-ELECTORAL-2788-001
GC-TERR-343-001
GC-CASILLA-RESECTION-001
```

### 7.23 Registro de auditoría

HEYTI deberá evolucionar hacia un registro persistente, conceptualmente:

`metadata.data_truth_incident`

No se autoriza todavía su creación física.

### 7.24 Regla de “0 errores, 0 omisiones”

> Ninguna anomalía conocida se ignora, oculta o transforma silenciosamente en dato válido.

### 7.25 Cierre de auditoría vs remediación

Deberá distinguirse:

```text
AUDIT_CLOSED
REMEDIATION_CLOSED
```

El incidente temporal electoral de las 32 secciones puede considerarse `AUDIT_CLOSED` porque fue clasificado completamente, aunque varias correcciones físicas permanezcan `REMEDIATION_PENDING`.

---

# Baseline consolidada

Este archivo consolida los capítulos 1 al 7 de:

`HEYTI_Data_Truth_Governance_v1.0`

Estado:

`ACTIVE — NORMATIVE BASELINE`

Origen:

`Sprint 24 — HEYTI Data Readiness & Module Migration`

La siguiente sección prevista es:

**Capítulo 8 — Reglas de transformación y ETL seguro**

## Capítulo 8. Reglas de transformación y ETL seguro

### 8.1 Propósito

Este capítulo define las reglas obligatorias que deberán respetar los procesos ETL y cualquier transformación de datos dentro de HEYTI-CORE.

El objetivo es impedir que una operación técnicamente válida produzca una interpretación semánticamente falsa.

Las reglas aplican a extracción, normalización, limpieza, joins, merges, agregaciones, deduplicación, relleno de valores, conversión de tipos, cargas parciales, rechazos, skips, enriquecimiento, proyecciones, exportaciones y migraciones.

### 8.2 Principio rector

Todo ETL deberá preservar:

```text
INPUT_VALUE
INPUT_STATUS
TRANSFORMATION
OUTPUT_VALUE
OUTPUT_STATUS
```

> El resultado técnico de una transformación no deberá ocultar la naturaleza del dato de entrada.

### 8.3 ETL-001 — Ausencia no es cero

Cuando una fuente no contenga un valor:

```text
SOURCE_MISSING
```

el ETL no deberá convertirlo automáticamente en:

```text
OFFICIAL_ZERO
```

Si se aplica `fillna(0)` o equivalente:

```text
truth_status = TRANSFORMATION_ZERO
```

### 8.4 ETL-002 — `fillna(0)` requiere trazabilidad

Deberá poder registrarse:

```text
original_status = SOURCE_MISSING
output_value = 0
truth_status = TRANSFORMATION_ZERO
transformation_rule = FILL_MISSING_WITH_ZERO
```

La ausencia original no podrá borrarse.

### 8.5 ETL-003 — Los joins deben declarar su semántica

Toda unión deberá declarar:

- llave;
- cardinalidad esperada;
- universo izquierdo;
- universo derecho;
- periodo;
- tratamiento de no coincidencias.

Cuando la identidad territorial dependa del tiempo, la llave conceptual deberá considerar:

```text
section_code + period
```

### 8.6 ETL-004 — Un `left join` no define autoridad

El hecho de usar una fuente como lado izquierdo de un merge no convierte su universo en autoritativo.

El caso de la sección `2788` demuestra el riesgo:

```text
BASE_MASTER = LEFT_SIDE
RIGHT_SIDE_ONLY = OFFICIAL SECTION 2788
```

Un `left join` puede impedir estructuralmente la incorporación de una sección válida.

### 8.7 ETL-005 — Toda pérdida debe contabilizarse

Si una transformación elimina registros deberá registrar:

```text
input_count
output_count
removed_count
removed_keys
removal_reason
```

cuando aplique.

Deberá poder comprobarse:

```text
input_count - output_count = removed_count
```

### 8.8 ETL-006 — Todo `skip` debe clasificarse

Queda prohibido el patrón silencioso:

```text
if not found:
    continue
```

cuando la omisión afecte datos relevantes.

HEYTI deberá evolucionar hacia:

```text
NOT_FOUND
→ CLASSIFY
→ RECORD INCIDENT
→ PRESERVE EVIDENCE
→ ROUTE OR REJECT
```

### 8.9 ETL-007 — `SECTION NOT FOUND` no significa sección inválida

Cuando una sección histórica no exista en `territorial.section`, deberán considerarse estados como:

```text
HISTORICAL_SECTION
RESECTION_PREDECESSOR
GENEALOGY_UNRESOLVED
MASTER_OMISSION
SOURCE_ERROR
INVALID_SECTION
```

No deberá descartarse solo porque no pertenezca al universo vigente.

### 8.10 ETL-008 — Rechazo no equivale a pérdida

Un registro rechazado deberá conservar, como mínimo:

```text
source_reference
source_key
reject_reason
truth_status
territorial_status
evidence_reference
```

### 8.11 ETL-009 — Reconciliation ledger obligatorio

Todo ETL crítico deberá poder producir:

```text
input_count
inserted_count
updated_count
rejected_count
skipped_count
duplicate_count
unresolved_count
```

La suma deberá reconciliarse con el universo de entrada según el contrato del pipeline.

### 8.12 ETL-010 — Duplicado técnico vs duplicado semántico

La duplicidad deberá definirse por dominio.

Ejemplo Campo:

```text
Nombre + Teléfono + Sección
```

puede ser la regla de duplicidad, aunque múltiples registros compartan la misma sección.

### 8.13 ETL-011 — Una sección puede tener múltiples casillas

En Día D:

```text
multiple casillas per section
```

es una relación válida y no constituye duplicidad.

### 8.14 ETL-012 — Agregaciones son derivaciones

Toda suma, promedio, porcentaje, índice o agrupamiento que no exista directamente en la fuente deberá producir:

```text
truth_status = DERIVED_DATA
```

y registrar:

```text
aggregation_rule
grouping_key
input_scope
transformation_version
```

### 8.15 ETL-013 — Total observado vs total calculado

Deberán distinguirse:

```text
OBSERVED_TOTAL
DERIVED_TOTAL
```

Un total calculado no sustituirá silenciosamente un total oficial.

### 8.16 ETL-014 — Carry-forward debe ser explícito

Toda copia temporal:

```text
period_A → period_B
```

deberá registrar:

```text
truth_status = CARRY_FORWARD
source_period
target_period
source_field
target_field
transformation_rule
```

### 8.17 ETL-015 — Carry-forward global debe auditarse globalmente

Caso certificado:

```text
18G_* → 24G_*
3137 / 3137 exact copies
```

El patrón deberá permanecer identificado hasta contar con evidencia primaria independiente.

### 8.18 ETL-016 — Conversión de tipos no debe alterar significado

Conversiones de tipos deberán evitar:

- truncamiento;
- pérdida de ceros significativos;
- cambio de códigos;
- colisión de llaves;
- pérdida de `NULL`.

### 8.19 ETL-017 — Los códigos son identificadores

Campos como:

```text
section_code
casilla_code
municipality_code
district_code
```

son identificadores y no cantidades.

### 8.20 ETL-018 — Normalización de nombres no redefine identidad

Mayúsculas, acentos, espacios y abreviaturas pueden normalizarse para comparación, pero no certifican por sí solos identidad.

### 8.21 ETL-019 — Deduplicación debe conservar evidencia

Cuando se elimine un duplicado deberá conservarse, cuando sea viable:

```text
duplicate_key
surviving_record
removed_record
deduplication_rule
reason
```

### 8.22 ETL-020 — No deduplicar por intuición

Queda prohibido eliminar registros únicamente porque:

- se parecen;
- comparten nombre;
- comparten sección;
- están próximos geográficamente.

### 8.23 ETL-021 — Reasignación territorial requiere certificación

Un ETL no deberá convertir automáticamente:

```text
historical_section → current_section
```

sin genealogía certificada.

Aun con genealogía certificada, la transferencia del valor requiere evidencia específica.

### 8.24 ETL-022 — Reseccionamiento no define distribución

Una relación:

```text
1 predecessor → N successors
```

no autoriza, sin evidencia:

```text
equal_split
population_weight
geometric_area_weight
casilla_count_weight
```

como distribución oficial.

### 8.25 ETL-023 — Faltantes y errores son distintos

Deberá distinguirse:

```text
SOURCE_MISSING
```

de:

```text
PARSING_ERROR
VALIDATION_ERROR
FOREIGN_KEY_ERROR
TYPE_ERROR
```

### 8.26 ETL-024 — Error técnico no invalida el dato fuente

Si un registro válido no puede insertarse por incompatibilidad del modelo actual, la fuente no deberá clasificarse automáticamente como inválida.

Las 97 casillas históricas rechazadas constituyen un caso de referencia.

### 8.27 ETL-025 — Una carga exitosa no certifica completitud

```text
PROCESS_EXIT_CODE = 0
```

no significa:

```text
DATA_TRUTH = CERTIFIED
```

La carga deberá reconciliarse contra la fuente.

### 8.28 ETL-026 — Conteo igual no certifica equivalencia

```text
COUNT_MATCH != SEMANTIC_MATCH
```

Deben validarse llaves, valores, significado y temporalidad.

### 8.29 ETL-027 — Hash igual no prueba autoridad

Dos archivos con igual hash son físicamente idénticos, pero eso no determina cuál es:

```text
AUTHORITATIVE_SOURCE
ACTIVE_SOURCE
```

### 8.30 ETL-028 — Fuentes simuladas bloquean certificación

Si la entrada es:

```text
SIMULATED_SOURCE
```

el resultado no podrá convertirse en `OBSERVED_DATA` ni alimentar silenciosamente una respuesta certificada.

### 8.31 ETL-029 — Valores DEMO deben permanecer DEMO

Un fallback de demostración deberá quedar explícitamente identificado.

La simulación podrá utilizarse en pruebas controladas, pero nunca confundirse con verdad operativa.

### 8.32 ETL-030 — Transformaciones deben versionarse

Toda transformación con impacto semántico deberá disponer de:

```text
transformation_rule
transformation_version
```

### 8.33 ETL-031 — La configuración forma parte de la transformación

Cuando el resultado dependa de parámetros deberán preservarse:

```text
configuration_version
parameter_values
execution_context
```

### 8.34 ETL-032 — Toda ejecución crítica deberá ser identificable

Conceptualmente:

```text
run_id
source_hash
etl_version
started_at
finished_at
result_status
```

### 8.35 ETL-033 — No sobrescribir silenciosamente datos certificados

Si una nueva carga cambia datos certificados deberá:

1. detectar el cambio;
2. registrar el delta;
3. revisar la certificación;
4. reconciliar;
5. revalidar Golden Cases.

### 8.36 ETL-034 — Idempotencia deseable

Cuando sea aplicable, la misma fuente deberá producir el mismo estado final sin duplicaciones.

### 8.37 ETL-035 — Upsert requiere política explícita

Todo `UPSERT` deberá declarar:

```text
business_key
update_policy
conflict_policy
```

"Último valor gana" no será válido salvo regla documentada.

### 8.38 ETL-036 — El orden de carga no debe crear verdad accidental

Si el resultado depende del orden de carga, la precedencia deberá estar basada en autoridad y quedar documentada.

### 8.39 ETL-037 — Los defaults requieren procedencia

Todo valor por defecto deberá identificarse como tal y no confundirse con observación de fuente.

### 8.40 ETL-038 — Enriquecimiento no sobrescribe origen

El enriquecimiento con municipio, distrito, coordenadas, categoría o score deberá preservar el valor original y su procedencia.

### 8.41 ETL-039 — Asignación espacial es derivación

Una sección obtenida mediante punto-en-polígono o cálculo espacial deberá registrarse como derivación cuando no provenga directamente de la fuente.

### 8.42 ETL-040 — Incertidumbre espacial debe preservarse

Una asignación espacial ambigua no podrá convertirse automáticamente en relación certificada.

### 8.43 ETL-041 — Exportar no elimina trazabilidad

Un export deberá conservar origen, periodo, fecha de materialización, versión y certificación cuando corresponda.

### 8.44 ETL-042 — Un export es fuente derivada

Un archivo generado desde DB deberá clasificarse como:

```text
DERIVED_SOURCE
```

salvo reproducción exacta de una fuente original.

### 8.45 ETL-043 — Backups no son inputs automáticos

La existencia de un archivo en `backups/` no autoriza su selección como fuente activa.

### 8.46 ETL-044 — Resolución de fuente determinista

Un ETL no deberá escoger "el primer archivo que encuentre".

Deberá resolver la fuente mediante identidad lógica y ubicación esperada, y cuando sea posible por hash o metadata.

### 8.47 ETL-045 — Prohibición de fallbacks silenciosos

Si falta la fuente esperada, queda prohibido:

- usar automáticamente un backup;
- utilizar un archivo de nombre similar;
- generar datos DEMO;
- sustituir la fuente sin registrar el cambio.

El proceso deberá `FAIL` o `BLOCK`, salvo política certificada.

### 8.48 ETL-046 — Contrato de entrada

Todo ETL deberá disponer conceptualmente de:

```text
logical_source_id
expected_schema
required_fields
optional_fields
key_definition
expected_universe
period
domain
allowed_truth_states
```

### 8.49 ETL-047 — Validación previa

Antes de transformar deberá validar, cuando aplique:

```text
schema
required_fields
data_types
keys
duplicates
period
source_identity
```

### 8.50 ETL-048 — Contrato de salida

El ETL deberá declarar:

```text
target_schema
target_table_or_artifact
output_key
output_truth_status
reconciliation_expectation
```

### 8.51 ETL-049 — Reconciliación post-carga

Después de una carga crítica deberán compararse:

```text
source_count
target_count
source_keys
target_keys
rejected_count
unresolved_count
```

Resultado formal:

```text
PASS
PASS_WITH_EXPLAINED_DELTA
FAIL
OPEN
BLOCKED
```

### 8.52 ETL-050 — Ningún delta queda sin clasificación

Todo delta deberá pertenecer a una categoría explícita.

`OTHER` no será un cierre definitivo válido para una incidencia crítica.

### 8.53 Modelo operacional seguro

```text
RESOLVE SOURCE
→ VALIDATE SOURCE
→ CLASSIFY INPUT
→ TRANSFORM
→ CLASSIFY OUTPUT
→ LOAD
→ RECONCILE
→ CERTIFY OR OPEN INCIDENT
```

### 8.54 Flujo prohibido

```text
READ FILE
→ MODIFY VALUES
→ INSERT
→ PROCESS COMPLETED
```

sin clasificación y reconciliación.

### 8.55 Requisito electoral

Todo ETL electoral deberá conservar o poder reconstruir:

```text
section_code
election_year
election_type
party_or_metric
value
truth_status
source_reference
```

### 8.56 Requisito territorial

Deberá distinguir, cuando la evidencia lo permita:

```text
CURRENT
HISTORICAL
PREDECESSOR
SUCCESSOR
UNRESOLVED
```

### 8.57 Requisito socioeconómico

Deberá preservar:

```text
indicator
period
unit
geographic_level
source
truth_status
```

Los valores simulados deberán excluirse de salidas certificadas.

### 8.58 Requisito Campo

Deberá preservar identidad del registro, regla semántica de duplicidad, fuente, fecha y estado de validación.

### 8.59 Requisito Día D

Deberá preservar:

```text
casilla_code
section_code_as_reported
territorial_status
source_reference
reject_or_route_reason
```

### 8.60 Caso 2015

El proceso histórico:

```text
BASE MASTER
LEFT MERGE A2015 / DF2015 / DL2015
FILLNA(0)
```

produce dos efectos distintos:

```text
ABSENT_FROM_BASE_MASTER → MASTER_OMISSION
```

y:

```text
MISSING_AFTER_MERGE + FILLNA(0) → TRANSFORMATION_ZERO
```

### 8.61 Caso casillas

Los 97 registros conocidos deberán conservar:

```text
reject_reason = CURRENT_SECTION_NOT_FOUND
territorial_context = CERTIFIED_RESECTION_PREDECESSOR
```

La reasignación individual continúa bloqueada.

### 8.62 Caso 24G

La presencia de columnas `24G_*` no demuestra observación 2024.

Estado actual:

```text
truth_status = CARRY_FORWARD
source_period = 2018
target_period = 2024
```

### 8.63 Auditoría de ETL existente

Antes de modificar físicamente los ETL actuales, cada uno deberá clasificarse como:

```text
SAFE
NEEDS_ADAPTATION
SEMANTIC_RISK
BLOCKING_RISK
```

### 8.64 No modificar todavía los ETL

Durante la definición normativa:

```text
NO ETL EDIT
NO DATA RELOAD
NO DB REMEDIATION
```

por efecto exclusivo de este capítulo.

### 8.65 Golden Cases ETL

Como mínimo:

```text
GC-ETL-001
SOURCE_MISSING + fillna(0)
→ TRANSFORMATION_ZERO
```

```text
GC-ETL-002
section 2788
→ must not disappear from historical universe
```

```text
GC-ETL-003
343 historical section
→ must not be treated as invalid
```

```text
GC-ETL-004
18G → 24G
→ CARRY_FORWARD
```

```text
GC-ETL-005
97 casillas
→ fully accounted for
```

### 8.66 Pruebas negativas

Deberán verificarse:

```text
SOURCE_MISSING != OFFICIAL_ZERO
TRANSFORMATION_ZERO != OBSERVED_DATA
CARRY_FORWARD != OBSERVED_DATA
HISTORICAL_SECTION != INVALID_SECTION
RESECTION_PREDECESSOR != AUTOMATIC_SUCCESSOR_ASSIGNMENT
SIMULATED_SOURCE != CERTIFIED_OBSERVATION
```

### 8.67 Invariantes ETL

- Toda pérdida debe ser explicable.
- Toda transformación semántica debe estar versionada.
- Todo dato derivado debe conocer su origen.
- Todo rechazo relevante debe conservar evidencia.
- Un ETL no puede certificar verdad únicamente por terminar exitosamente.
- No puede existir reasignación territorial automática sin evidencia suficiente.
- No puede existir fallback silencioso desde fuente faltante hacia fuente simulada.

### 8.68 Resultado esperado

Modelo anterior:

```text
SOURCE
→ TRANSFORM
→ LOAD
```

Modelo HEYTI:

```text
SOURCE
→ IDENTIFY
→ VALIDATE
→ CLASSIFY
→ TRANSFORM
→ TRACE
→ LOAD
→ RECONCILE
→ CERTIFY
```

### 8.69 Principio final

> **Un ETL de HEYTI no deberá limitarse a transportar valores; deberá transportar también su verdad, su historia y su procedencia.**

### 8.70 Baseline ETL

El modelo definido constituye:

```text
HEYTI Safe ETL & Transformation Model v1.0
```

Estado:

```text
NORMATIVE BASELINE
```

Su aplicación física se definirá durante `Truth Contract Physical Mapping` y mediante planes controlados de remediación y migración.

---

## Fin del Capítulo 8

## Capítulo 9. Preservación de verdad desde DB hasta Capability, Runtime, Materialization y UI

### 9.1 Propósito

Este capítulo define las reglas que deberán preservar la verdad, procedencia, temporalidad y certificación de los datos después de su ingreso a la base de datos y durante toda la cadena de ejecución de HEYTI-CORE.

La cadena gobernada es:

```text
DATABASE
→ CAPABILITY
→ RUNTIME
→ MATERIALIZATION
→ UI
```

El objetivo es impedir que un dato correctamente clasificado en una capa inferior pierda su significado al avanzar hacia la respuesta final.

---

### 9.2 Principio rector

> **La verdad de un dato no termina cuando el dato entra a la base de datos.**

Toda capa posterior deberá conservar, como mínimo, la información necesaria para distinguir:

```text
OBSERVED_DATA
OFFICIAL_ZERO
SOURCE_MISSING
TRANSFORMATION_ZERO
CARRY_FORWARD
DERIVED_DATA
UNAVAILABLE
```

y, cuando corresponda:

```text
CURRENT_SECTION
HISTORICAL_SECTION
RESECTION_PREDECESSOR
RESECTION_SUCCESSOR
```

además de su genealogía, procedencia y certificación.

---

### 9.3 Regla LAYER-001 — La base de datos no redefine verdad

La persistencia de un valor en una tabla no lo convierte automáticamente en:

```text
OBSERVED_DATA
```

La DB almacena información; no certifica por sí sola su significado.

---

### 9.4 Regla LAYER-002 — Persistencia semántica

Cuando un dato posea metadata de verdad, las capas posteriores deberán preservarla.

Conceptualmente:

```text
DB.truth_status
=
Capability.truth_status
=
Runtime.truth_status
=
Materialization.truth_status
```

salvo que exista una transformación explícita y trazable.

---

### 9.5 Regla LAYER-003 — Ninguna capa puede fortalecer evidencia

Queda prohibido:

```text
CARRY_FORWARD → OBSERVED_DATA
TRANSFORMATION_ZERO → OFFICIAL_ZERO
SOURCE_MISSING → OBSERVED_DATA
UNAVAILABLE → OBSERVED_DATA
PROVISIONAL → CERTIFIED
```

por efecto exclusivo de Capability, Runtime, Materialization o UI.

---

### 9.6 Regla LAYER-004 — Capability debe conocer el contexto del dato

Una Capability que consulte información gobernada deberá recibir o reconstruir, cuando aplique:

```text
value
truth_status
source_reference
source_period
territorial_status
genealogy_status
certification_status
anomaly_code
```

La Capability no deberá razonar únicamente sobre el valor numérico.

---

### 9.7 Regla LAYER-005 — Capability no corrige silenciosamente

Una Capability no deberá:

- rellenar faltantes con cero;
- sustituir periodos;
- copiar valores;
- reasignar secciones;
- simular datos;
- cambiar certificación;

sin una regla explícita, trazable y autorizada.

---

### 9.8 Regla LAYER-006 — Runtime preserva trazabilidad

El Runtime deberá transportar metadata suficiente para que Materialization pueda determinar:

- qué dato recibió;
- de qué fuente provino;
- qué periodo representa;
- qué transformación recibió;
- qué estado de verdad posee;
- qué nivel de certificación tiene.

---

### 9.9 Regla LAYER-007 — El contrato de respuesta debe preservar verdad

El contrato de respuesta de HEYTI deberá poder representar conceptualmente:

```text
value
truth_status
certification_status
source_reference
period
territorial_context
evidence
warnings
```

cuando esos elementos sean relevantes para la respuesta.

---

### 9.10 Regla LAYER-008 — Materialization no maquilla incertidumbre

Materialization no deberá transformar:

```text
UNAVAILABLE
```

en una respuesta aparentemente completa.

Tampoco deberá convertir:

```text
SOURCE_MISSING
```

en:

```text
0
```

sin conservar su estado real.

---

### 9.11 Regla LAYER-009 — Materialization debe poder degradar presentación, no verdad

La presentación puede simplificarse para el usuario.

La verdad subyacente no.

Ejemplo:

Internamente:

```text
truth_status = CARRY_FORWARD
source_period = 2018
target_period = 2024
```

La UI podrá utilizar una etiqueta breve, pero no podrá presentarlo como:

```text
Resultado observado 2024
```

---

### 9.12 Regla LAYER-010 — La UI no es fuente de verdad

La interfaz es una capa de presentación.

Por tanto:

```text
DISPLAYED_VALUE
```

deberá derivarse de un contrato certificado y no de lógica paralela oculta en JavaScript, HTML o componentes visuales.

---

### 9.13 Regla LAYER-011 — No duplicar reglas de negocio en UI

Las reglas de verdad, temporalidad, certificación y reconciliación deberán residir en capas gobernadas.

La UI no deberá decidir por sí sola:

```text
missing = 0
historical = invalid
carry_forward = observed
provisional = certified
```

---

### 9.14 Regla LAYER-012 — Mapas deben respetar temporalidad

Un mapa deberá conocer el universo territorial correspondiente al dato representado.

No deberá asumir que:

```text
CURRENT_GEOMETRY
```

representa automáticamente todas las observaciones históricas.

---

### 9.15 Regla LAYER-013 — Ausencia de geometría no elimina historia

Cuando exista:

```text
OBSERVED_DATA
+
HISTORICAL_SECTION
+
NO_CURRENT_GEOMETRY
```

HEYTI deberá conservar el dato.

La UI podrá indicar que no existe geometría vigente compatible, pero no deberá eliminar la observación histórica.

---

### 9.16 Regla LAYER-014 — Reseccionamiento en mapas

Una sección predecesora no deberá colorear automáticamente sus sucesoras con el valor histórico del predecesor.

Ejemplo:

```text
343 → 3290–3299
```

no autoriza:

```text
value(343, historical)
→ value(3290...3299, current)
```

---

### 9.17 Regla LAYER-015 — Gráficas temporales deben distinguir procedencia

Una gráfica que compare periodos deberá distinguir:

```text
OBSERVED_DATA
```

de:

```text
CARRY_FORWARD
DERIVED_DATA
SOURCE_MISSING
UNAVAILABLE
```

No deberá dibujar una continuidad temporal falsa.

---

### 9.18 Regla LAYER-016 — Caso 24G en gráficas

Mientras `24G_*` permanezca clasificado como `CARRY_FORWARD`, una gráfica no deberá presentarlo como observación independiente de 2024.

La continuidad:

```text
2018 → 2024
```

deberá conservar la advertencia semántica correspondiente.

---

### 9.19 Regla LAYER-017 — Tablas deben distinguir cero y ausencia

Una tabla no deberá mostrar indistintamente:

```text
OFFICIAL_ZERO
SOURCE_MISSING
TRANSFORMATION_ZERO
```

como:

```text
0
```

sin mecanismo de diferenciación.

---

### 9.20 Regla LAYER-018 — Representación de `UNAVAILABLE`

Cuando el dato no pueda certificarse, HEYTI deberá preferir expresiones como:

```text
No disponible
No certificado
Sin evidencia suficiente
```

según el contexto.

No deberá inventar un valor para completar la visualización.

---

### 9.21 Regla LAYER-019 — Simulación visible

Cuando una interfaz de demostración utilice datos simulados deberá existir una indicación inequívoca de que se trata de:

```text
DEMO / SIMULATED
```

Los datos simulados no deberán mezclarse visualmente con datos certificados sin distinción.

---

### 9.22 Regla LAYER-020 — Respuestas narrativas también están gobernadas

Las respuestas textuales de HEYTI deberán respetar las mismas reglas que mapas, gráficas y tablas.

HEYTI no deberá afirmar:

> “En 2024 la sección obtuvo X votos”

si `X` está clasificado como:

```text
CARRY_FORWARD
```

---

### 9.23 Regla LAYER-021 — Lenguaje proporcional a la evidencia

La redacción deberá corresponder al nivel de certeza.

Ejemplos:

Para `OBSERVED_DATA + CERTIFIED`:

```text
La fuente registra...
```

Para `DERIVED_DATA`:

```text
El cálculo indica...
```

Para `CARRY_FORWARD`:

```text
El dataset conserva un valor trasladado desde...
```

Para `UNAVAILABLE`:

```text
No existe información certificada suficiente para determinar...
```

---

### 9.24 Regla LAYER-022 — No ocultar incidencias críticas

Una incidencia crítica que afecte directamente la respuesta deberá impedir que la UI presente el resultado como certificado.

---

### 9.25 Regla LAYER-023 — Bloqueo controlado

Cuando una respuesta dependa de una incidencia crítica abierta, el sistema podrá:

```text
BLOCK RESPONSE
```

o:

```text
RETURN PARTIAL RESPONSE WITH WARNING
```

según el contrato de la Capability.

Nunca deberá completar silenciosamente el dato.

---

### 9.26 Regla LAYER-024 — Respuesta parcial es válida

Una respuesta incompleta pero verdadera es preferible a una respuesta completa construida con evidencia inexistente.

Principio:

> **HEYTI podrá decir “no lo sé con certeza”; no podrá fingir que lo sabe.**

---

### 9.27 Regla LAYER-025 — Provenance trace

Toda respuesta crítica deberá poder reconstruir conceptualmente:

```text
UI
← Materialization
← Runtime
← Capability
← DB
← ETL
← Source
```

---

### 9.28 Regla LAYER-026 — Identificador de trazabilidad

El contrato podrá evolucionar para incluir:

```text
trace_id
```

que permita relacionar una respuesta con:

- ejecución;
- Capability;
- consultas;
- fuentes;
- materialización;
- evidencia.

---

### 9.29 Regla LAYER-027 — Certificación por bloque

Una respuesta compuesta podrá contener bloques con distintos estados.

Ejemplo:

```text
territorial_summary = CERTIFIED
electoral_2024_governor = CARRY_FORWARD
socioeconomic_indicator = UNAVAILABLE
```

No deberá asignarse una certificación global engañosa.

---

### 9.30 Regla LAYER-028 — Materialización compuesta

Cuando una respuesta mezcle datos observados y derivados, Materialization deberá conservar la clasificación de cada componente relevante.

---

### 9.31 Regla LAYER-029 — No promediar estados de verdad

No existe una operación válida como:

```text
CERTIFIED + PROVISIONAL = CERTIFIED
```

ni:

```text
OBSERVED + CARRY_FORWARD = OBSERVED
```

Los estados deberán conservarse por componente o aplicar una política conservadora explícita.

---

### 9.32 Regla LAYER-030 — Política conservadora

Cuando una salida única dependa inseparablemente de múltiples componentes con diferentes niveles de certificación, el resultado no deberá tener una certificación superior al componente crítico menos certificado.

---

### 9.33 Regla LAYER-031 — Capabilities históricas deben consultar historia

Una Capability que responda sobre periodos históricos no deberá limitarse al universo territorial vigente.

Deberá poder considerar:

```text
CURRENT_SECTION
HISTORICAL_SECTION
RESECTION_PREDECESSOR
```

según corresponda.

---

### 9.34 Regla LAYER-032 — Genealogía no resuelta debe permanecer visible internamente

Cuando:

```text
genealogy_status = UNRESOLVED
```

la Capability no deberá inventar una sucesión para poder responder.

---

### 9.35 Regla LAYER-033 — Caso sección 2788

Una consulta histórica de 2015 deberá poder reconocer que la sección `2788` posee evidencia oficial aunque haya sido omitida del maestro integrado.

La omisión del maestro no deberá convertirse en:

```text
SECTION_DID_NOT_EXIST
```

---

### 9.36 Regla LAYER-034 — Caso 97 casillas

Una Capability de Día D no deberá interpretar las 97 casillas rechazadas como:

```text
INVALID_CASILLA
```

sin considerar el contexto:

```text
RESECTION_PREDECESSOR
```

---

### 9.37 Regla LAYER-035 — Datos certificados esperados

Antes de certificar una visualización deberán definirse valores esperados independientes para casos controlados.

Estos valores constituirán:

```text
CERTIFIED_EXPECTED_VALUES
```

---

### 9.38 Regla LAYER-036 — Prueba controlada de UI

Para cada módulo migrado deberán compararse:

```text
CERTIFIED_EXPECTED_VALUE
vs
DB_VALUE
vs
CAPABILITY_VALUE
vs
RUNTIME_VALUE
vs
MATERIALIZED_VALUE
vs
DISPLAYED_VALUE
```

---

### 9.39 Regla LAYER-037 — Igualdad de valor no basta

La prueba deberá comparar también:

```text
truth_status
period
section
source
certification_status
```

cuando corresponda.

---

### 9.40 Regla LAYER-038 — Criterio de aprobación visual

Una visualización solo podrá certificarse cuando:

```text
DISPLAYED_VALUE = CERTIFIED_EXPECTED_VALUE
```

y la semántica mostrada sea compatible con el Truth Status Contract.

---

### 9.41 Regla LAYER-039 — Golden Cases end-to-end

Los Golden Cases deberán atravesar:

```text
SOURCE
→ DB
→ CAPABILITY
→ RUNTIME
→ MATERIALIZATION
→ UI
```

No bastará con probar una sola capa.

---

### 9.42 Golden Case — dato observado

```text
GC-E2E-OBSERVED-001
```

Deberá verificar que un dato oficial observado permanezca:

```text
OBSERVED_DATA
```

en toda la cadena.

---

### 9.43 Golden Case — cero oficial

```text
GC-E2E-ZERO-001
```

Deberá verificar que:

```text
OFFICIAL_ZERO
```

no sea confundido con ausencia o transformación.

---

### 9.44 Golden Case — dato faltante

```text
GC-E2E-MISSING-001
```

Deberá verificar:

```text
SOURCE_MISSING
```

sin conversión silenciosa a cero.

---

### 9.45 Golden Case — carry-forward

```text
GC-E2E-CARRY-001
```

Caso base:

```text
18G → 24G
```

Deberá permanecer `CARRY_FORWARD` hasta UI.

---

### 9.46 Golden Case — sección histórica

```text
GC-E2E-HISTORICAL-001
```

Una sección histórica con datos válidos no deberá desaparecer porque no exista en el universo territorial vigente.

---

### 9.47 Golden Case — reseccionamiento

```text
GC-E2E-RESECTION-001
```

La sección `343` deberá reconocerse como predecesora de `3290–3299` sin redistribución automática de valores.

---

### 9.48 Golden Case — master omission

```text
GC-E2E-2788-001
```

La sección `2788` deberá preservar:

```text
OBSERVED_DATA
HISTORICAL_SECTION
MASTER_OMISSION
```

según el contexto correspondiente.

---

### 9.49 Golden Case — simulación

```text
GC-E2E-SIMULATION-001
```

Una fuente simulada no podrá producir una respuesta presentada como observación certificada.

---

### 9.50 Golden Case — respuesta parcial

```text
GC-E2E-PARTIAL-001
```

Una respuesta con componentes certificados y no disponibles deberá preservar la diferencia y no inventar los componentes faltantes.

---

### 9.51 Regla LAYER-040 — Regresión visual

Una modificación de UI deberá ejecutar nuevamente los Golden Cases relevantes.

Un cambio puramente visual podrá convertirse en error de datos si altera:

- filtros;
- joins;
- periodos;
- selección de secciones;
- formateo numérico;
- lógica de botones;
- capas de mapa.

---

### 9.52 Regla LAYER-041 — Botones son invocadores, no fuentes

En la nueva interfaz HEYTI:

> No copiamos botones; preservamos funciones.

Los botones deberán invocar capacidades gobernadas y no contener lógica paralela de verdad de datos.

---

### 9.53 Regla LAYER-042 — Migramos capacidades, no pantallas

La migración desde V1 deberá preservar la capacidad funcional y reconstruir su interacción sobre contratos HEYTI.

Regla:

> **No migramos pantallas; migramos capacidades.**

---

### 9.54 Regla LAYER-043 — Los nombres visuales no determinan contratos internos

Los nombres finales de módulos, botones o herramientas podrán cambiar durante el rediseño.

La verdad de datos deberá permanecer independiente de la nomenclatura visual.

---

### 9.55 Regla LAYER-044 — V1 no es autoridad semántica automática

El comportamiento actual de una pantalla V1 deberá auditarse antes de reproducirse.

Si V1:

- simula;
- rellena;
- copia;
- descarta;
- usa una fuente legacy;

HEYTI no deberá heredar ese comportamiento por inercia.

---

### 9.56 Regla LAYER-045 — Prueba de paridad funcional controlada

La comparación V1 → HEYTI deberá preguntar:

```text
WHAT CAPABILITY DOES V1 PROVIDE?
WHAT DATA DOES IT USE?
WHAT TRUTH STATUS DOES THAT DATA HAVE?
WHAT SHOULD HEYTI PROVIDE?
```

No únicamente:

```text
DOES THE NEW SCREEN LOOK THE SAME?
```

---

### 9.57 Gate DB → Capability

Antes de certificar una Capability deberán comprobarse:

- fuente DB correcta;
- periodo correcto;
- universo correcto;
- llaves correctas;
- estados de verdad;
- tratamiento de históricos;
- tratamiento de faltantes;
- incidentes críticos.

---

### 9.58 Gate Capability → Runtime

Deberán comprobarse:

- contrato válido;
- metadata preservada;
- errores tipificados;
- trazabilidad;
- ausencia de fortalecimiento semántico.

---

### 9.59 Gate Runtime → Materialization

Deberán comprobarse:

- bloques esperados;
- truth status preservado;
- warnings;
- provenance;
- estados parciales;
- errores.

---

### 9.60 Gate Materialization → UI

Deberán comprobarse:

- valor;
- unidad;
- periodo;
- sección;
- estado de verdad;
- certificación;
- representación de faltantes;
- representación de históricos;
- ausencia de simulación silenciosa.

---

### 9.61 Gate de certificación end-to-end

Una capacidad visual podrá declararse:

```text
E2E_CERTIFIED
```

únicamente cuando todos los gates relevantes hayan pasado.

---

### 9.62 Resultado de gate

Valores iniciales:

```text
PASS
PASS_WITH_WARNINGS
FAIL
BLOCKED
NOT_APPLICABLE
```

---

### 9.63 `PASS_WITH_WARNINGS`

Solo será válido cuando la advertencia no convierta una afirmación incierta en afirmación falsa.

No deberá utilizarse para eludir un `FAIL`.

---

### 9.64 Incidencias descubiertas en capas superiores

Si UI o Materialization revelan una discrepancia, deberá abrirse un Data Truth Incident y rastrearse hacia la capa donde se originó.

No deberá corregirse únicamente en CSS, JavaScript o formateo si la causa está en datos o contratos.

---

### 9.65 Corrección en la capa correcta

Principio:

```text
FIX ROOT CAUSE
NOT DISPLAY SYMPTOM
```

La UI no deberá utilizarse para ocultar errores de DB, ETL o Capability.

---

### 9.66 Observabilidad

HEYTI deberá evolucionar hacia capacidad de inspeccionar:

```text
request
capability
source
period
truth_status
certification_status
materialization
display
```

para respuestas críticas.

---

### 9.67 No exponer complejidad innecesaria al usuario

Preservar trazabilidad no implica saturar la interfaz.

La UI podrá ofrecer:

- estado resumido;
- advertencia contextual;
- detalle bajo demanda;
- evidencia en vistas técnicas.

La simplificación visual nunca deberá alterar el significado.

---

### 9.68 Regla de confianza

La confianza del usuario deberá provenir de trazabilidad y consistencia, no de ocultar incertidumbre.

HEYTI deberá ser capaz de decir:

```text
CERTIFIED
DERIVED
HISTORICAL
CARRY_FORWARD
UNAVAILABLE
```

cuando corresponda.

---

### 9.69 No implementar todavía cambios físicos

Durante la fase normativa actual:

```text
NO CAPABILITY REMEDIATION
NO RUNTIME REMEDIATION
NO MATERIALIZATION REMEDIATION
NO UI MIGRATION
```

por efecto exclusivo de este capítulo.

Primero deberán concluirse el Physical Mapping y los gates de remediación correspondientes.

---

### 9.70 Baseline end-to-end

El modelo definido en este capítulo constituye:

```text
HEYTI End-to-End Data Truth Preservation Model v1.0
```

Estado:

```text
NORMATIVE BASELINE
```

Este modelo será la base para:

- DB → Capability;
- Capability → Runtime;
- Runtime → Materialization;
- Materialization → UI;
- pruebas controladas;
- Golden Cases;
- regresión;
- certificación de módulos.

---

## Fin del Capítulo 9

## Capítulo 10. Golden Cases, regresión y certificación de verdad de datos

### 10.1 Propósito

Este capítulo establece el modelo normativo mediante el cual HEYTI-CORE convertirá los hallazgos certificados de auditoría en pruebas permanentes de protección contra regresiones.

Un Golden Case no deberá limitarse a comprobar que un valor numérico coincide.

Deberá certificar, cuando corresponda:

```text
VALUE
TRUTH_STATUS
SOURCE
PERIOD
TERRITORIAL_STATUS
GENEALOGY_STATUS
CERTIFICATION_STATUS
EXPECTED_BEHAVIOR
```

El objetivo es impedir que futuras modificaciones en datos, ETL, base de datos, Capabilities, Runtime, Materialization o UI reintroduzcan errores ya identificados y comprendidos.

---

### 10.2 Principio rector

> **Todo hallazgo crítico que HEYTI haya aprendido a distinguir deberá convertirse, cuando sea técnicamente posible, en una protección contra regresión.**

La auditoría descubre.

La gobernanza clasifica.

Los Golden Cases preservan.

---

### 10.3 Definición de Golden Case

Un Golden Case es un caso controlado con:

- entrada conocida;
- procedencia conocida;
- contexto temporal conocido;
- comportamiento esperado certificado;
- evidencia reproducible;
- resultado verificable.

Conceptualmente:

```text
KNOWN_INPUT
+
CERTIFIED_CONTEXT
+
EXPECTED_RESULT
=
GOLDEN_CASE
```

---

### 10.4 Golden Case no equivale a fixture

Un fixture puede proporcionar datos de prueba.

Un Golden Case incorpora además una afirmación normativa sobre el comportamiento correcto del sistema.

Por tanto:

```text
FIXTURE != GOLDEN_CASE
```

---

### 10.5 Golden Case no equivale a snapshot visual

Una captura de pantalla puede ayudar a comprobar presentación, pero no certifica por sí sola verdad de datos.

Por tanto:

```text
SCREENSHOT != DATA_TRUTH_CERTIFICATION
```

---

### 10.6 Identificador estable

Todo Golden Case deberá disponer de un identificador estable.

Formato recomendado:

```text
GC-<DOMAIN>-<SUBJECT>-<NNN>
```

Ejemplos:

```text
GC-ELECTORAL-24G-001
GC-ELECTORAL-2788-001
GC-TERR-RESECTION-001
GC-CASILLA-RESECTION-001
GC-ETL-MISSING-ZERO-001
GC-E2E-HISTORICAL-001
```

---

### 10.7 Registro conceptual mínimo

Cada Golden Case deberá poder representar:

```text
golden_case_id
domain
description
input_reference
source_reference
source_hash
period
entity_key
expected_value
expected_truth_status
expected_territorial_status
expected_genealogy_status
expected_certification_status
expected_behavior
evidence_reference
certified_at
version
```

No todos los campos serán obligatorios para todos los dominios.

---

### 10.8 Evidencia de origen

Un Golden Case deberá estar respaldado por evidencia suficiente.

Podrá incluir:

```text
official_source
source_hash
audit_output
SQL_result
ETL_analysis
certified_mapping
reconciliation_ledger
```

---

### 10.9 Regla GC-001 — El valor esperado debe estar certificado

No deberá crearse un Golden Case crítico a partir de un valor simplemente observado en la UI actual.

El valor esperado deberá derivarse de evidencia independiente y reconciliada.

---

### 10.10 Regla GC-002 — V1 no define automáticamente el resultado esperado

La versión V1 podrá utilizarse para identificar comportamiento funcional y detectar diferencias.

Sin embargo:

```text
V1_DISPLAYED_VALUE
```

no deberá convertirse automáticamente en:

```text
CERTIFIED_EXPECTED_VALUE
```

---

### 10.11 Regla GC-003 — Golden Case debe probar semántica

Cuando sea relevante, deberá comprobarse:

```text
actual_value == expected_value
```

y también:

```text
actual_truth_status == expected_truth_status
```

Un valor correcto con clasificación incorrecta constituye fallo.

---

### 10.12 Regla GC-004 — Cero correcto con origen incorrecto es fallo

Ejemplo:

```text
expected_value = 0
expected_truth_status = SOURCE_MISSING
```

Si el sistema devuelve:

```text
value = 0
truth_status = OFFICIAL_ZERO
```

el Golden Case deberá fallar.

---

### 10.13 Regla GC-005 — Periodo incorrecto es fallo

Un valor numéricamente idéntico proveniente de otro periodo no deberá considerarse equivalente.

Caso de referencia:

```text
18G → 24G
```

Aunque los valores coincidan, el origen temporal deberá conservarse.

---

### 10.14 Regla GC-006 — Universo territorial incorrecto es fallo

Una respuesta histórica no deberá invalidarse únicamente porque la sección no pertenezca al universo vigente.

El Golden Case deberá comprobar el contexto territorial correspondiente.

---

### 10.15 Regla GC-007 — Reasignación no certificada es fallo

Si un dato de una sección histórica aparece automáticamente atribuido a una sucesora sin evidencia suficiente, el Golden Case deberá fallar.

---

### 10.16 Regla GC-008 — Simulación silenciosa es fallo

Si una fuente real falta y el sistema presenta datos DEMO como observados:

```text
FAIL
```

---

### 10.17 Regla GC-009 — Omisión silenciosa es fallo

Si una entidad con evidencia histórica certificada desaparece de una consulta sin clasificación o explicación:

```text
FAIL
```

---

### 10.18 Regla GC-010 — Warning no corrige valor falso

Una advertencia visual no convierte un dato incorrectamente clasificado en resultado aceptable.

La corrección deberá ocurrir en la capa responsable.

---

### 10.19 Categorías de Golden Cases

HEYTI deberá mantener, como mínimo, las siguientes familias:

```text
SOURCE_GOLDEN_CASE
ETL_GOLDEN_CASE
DATABASE_GOLDEN_CASE
CAPABILITY_GOLDEN_CASE
RUNTIME_GOLDEN_CASE
MATERIALIZATION_GOLDEN_CASE
UI_GOLDEN_CASE
END_TO_END_GOLDEN_CASE
```

---

### 10.20 Source Golden Case

Valida que una fuente certificada conserve:

- identidad;
- hash esperado cuando aplique;
- esquema;
- universo;
- llaves;
- periodo.

---

### 10.21 ETL Golden Case

Valida una transformación crítica.

Ejemplos:

```text
SOURCE_MISSING + fillna(0)
→ TRANSFORMATION_ZERO
```

o:

```text
RIGHT_SIDE_ONLY + LEFT_JOIN
→ must remain accounted for
```

---

### 10.22 Database Golden Case

Comprueba que el estado persistido corresponda al resultado esperado después de carga y reconciliación.

---

### 10.23 Capability Golden Case

Comprueba que una Capability interprete correctamente:

- valor;
- periodo;
- territorialidad;
- faltantes;
- derivados;
- carry-forward;
- certificación.

---

### 10.24 Runtime Golden Case

Comprueba que Runtime preserve el contrato y no pierda metadata semántica.

---

### 10.25 Materialization Golden Case

Comprueba que la construcción de respuesta conserve:

```text
truth_status
certification
warnings
provenance
```

cuando corresponda.

---

### 10.26 UI Golden Case

Comprueba que la interfaz muestre correctamente un resultado ya certificado por capas inferiores.

No deberá utilizarse como sustituto de las pruebas de esas capas.

---

### 10.27 End-to-End Golden Case

Comprueba la cadena completa:

```text
SOURCE
→ ETL
→ DB
→ CAPABILITY
→ RUNTIME
→ MATERIALIZATION
→ UI
```

Será la forma de certificación más completa para capacidades críticas.

---

### 10.28 Caso base GC-ELECTORAL-24G-001

Objetivo:

Evitar que `24G_*` vuelva a clasificarse como observación independiente de 2024 mientras no exista fuente primaria que lo sustente.

Baseline:

```text
comparable_sections = 3137
exact_18G_24G_copies = 3137
differences = 0
```

Resultado esperado:

```text
truth_status = CARRY_FORWARD
source_period = 2018
target_period = 2024
```

---

### 10.29 Criterio de fallo para 24G

Deberá fallar si cualquier capa transforma el caso en:

```text
truth_status = OBSERVED_DATA
source_period = 2024
```

sin nueva evidencia certificada.

---

### 10.30 Caso base GC-ELECTORAL-2788-001

Objetivo:

Impedir que la sección `2788` vuelva a desaparecer del universo histórico de 2015.

Evidencia:

```text
official_2015_source = PRESENT
base_master = ABSENT
```

Resultado esperado:

```text
territorial_status = HISTORICAL_SECTION
anomaly_code = MASTER_OMISSION
truth_status = OBSERVED_DATA
```

para los valores oficiales correspondientes.

---

### 10.31 Criterio de fallo para 2788

Deberá fallar si:

```text
SECTION_NOT_FOUND
```

se interpreta como:

```text
SECTION_NEVER_EXISTED
```

o si un proceso de integración vuelve a eliminar silenciosamente la sección.

---

### 10.32 Caso base GC-TERR-RESECTION-001

Objetivo:

Preservar la genealogía certificada:

```text
343  → 3290–3299
1059 → 3300–3307
1110 → 3308–3313
1634 → 3278–3283
1647 → 3284–3289
```

---

### 10.33 Criterio de fallo para reseccionamiento

Deberá fallar si:

- desaparece la relación certificada;
- un sucesor no es reconocido;
- se redistribuyen automáticamente valores históricos;
- se considera inválido al predecesor por no ser vigente.

---

### 10.34 Caso base GC-CASILLA-RESECTION-001

Baseline:

```text
source_count = 8144
db_count = 8047
delta = 97
```

Descomposición:

```text
343  = 22
1059 = 18
1110 = 17
1634 = 20
1647 = 20
TOTAL = 97
```

Resultado esperado:

```text
reconciliation = PASS_WITH_EXPLAINED_DELTA
```

---

### 10.35 Criterio de fallo para las 97 casillas

Deberá fallar si:

- el delta deja de sumar 97 sin explicación;
- alguna casilla se pierde sin clasificación;
- se marca como inválida únicamente por pertenecer a sección histórica;
- se reasigna automáticamente a una sucesora.

---

### 10.36 Caso base GC-ETL-MISSING-ZERO-001

Entrada:

```text
SOURCE_MISSING
```

Transformación:

```text
fillna(0)
```

Resultado esperado:

```text
value = 0
truth_status = TRANSFORMATION_ZERO
```

Resultado prohibido:

```text
truth_status = OFFICIAL_ZERO
```

---

### 10.37 Caso base GC-E2E-HISTORICAL-001

Objetivo:

Verificar que una sección histórica con evidencia válida permanezca consultable aunque no tenga geometría vigente.

Resultado esperado:

```text
historical_data = PRESERVED
current_geometry = NOT_REQUIRED_FOR_HISTORICAL_VALIDITY
```

---

### 10.38 Caso base GC-E2E-UNAVAILABLE-001

Objetivo:

Verificar que la falta de evidencia certificada produzca:

```text
UNAVAILABLE
```

y no:

```text
0
SIMULATED_VALUE
INFERRED_VALUE
```

sin clasificación explícita.

---

### 10.39 Caso base GC-E2E-SIMULATION-001

Entrada:

```text
source_type = SIMULATED_SOURCE
```

Resultado esperado:

```text
certified_observation = FALSE
```

La UI deberá identificar la naturaleza DEMO cuando se utilice en un entorno permitido.

---

### 10.40 Certified Expected Values

Para pruebas visuales y end-to-end deberá existir un conjunto controlado de:

```text
CERTIFIED_EXPECTED_VALUES
```

Cada valor deberá conocer:

```text
entity
period
metric
expected_value
expected_truth_status
evidence_reference
```

---

### 10.41 Regla de independencia

Los valores esperados no deberán calcularse mediante exactamente la misma lógica que se está probando.

De lo contrario, un mismo error podría existir en:

```text
SYSTEM_UNDER_TEST
```

y:

```text
EXPECTED_VALUE_GENERATOR
```

sin ser detectado.

---

### 10.42 Certificación de mapas

Un mapa deberá comprobar, cuando aplique:

```text
section_selection
geometry
period
metric
displayed_value
truth_status
legend
tooltip_or_detail
```

---

### 10.43 Certificación de gráficas

Una gráfica deberá comprobar:

```text
series
periods
values
missing_points
carry_forward_points
derived_points
labels
```

---

### 10.44 Certificación de tablas

Una tabla deberá comprobar:

```text
row_identity
column_identity
period
value
format
truth_status_representation
sorting
filtering
```

cuando esas operaciones puedan alterar la interpretación.

---

### 10.45 Certificación de estadísticas

Totales, porcentajes, promedios, márgenes y scores deberán validarse contra fórmulas y entradas certificadas.

---

### 10.46 Regla de redondeo

La presentación podrá redondear valores únicamente cuando:

- la regla sea conocida;
- el valor interno permanezca preservado;
- el redondeo no altere clasificación o decisión.

---

### 10.47 Regla de formato porcentual

Deberá evitarse confundir:

```text
0.42
```

con:

```text
42
```

cuando ambos puedan representar 42 % según distintas convenciones.

El contrato deberá especificar unidad y escala.

---

### 10.48 Regla de filtros

Los filtros visuales deberán formar parte de las pruebas cuando modifiquen el universo mostrado.

Ejemplos:

- municipio;
- distrito;
- sección;
- elección;
- año;
- partido;
- categoría.

---

### 10.49 Regla de selección territorial

Una selección visual deberá resolver exactamente la entidad esperada.

No deberá confundirse:

```text
section_code
```

con índices de arreglo, IDs internos o posiciones gráficas.

---

### 10.50 Regla de interacción

Cuando un botón, selector o herramienta cambie la consulta, deberá comprobarse que invoca la Capability y parámetros correctos.

---

### 10.51 Regla de módulo

Cada módulo migrado deberá disponer de un conjunto mínimo de Golden Cases antes de considerarse certificado.

Los seis módulos objetivo deberán quedar cubiertos progresivamente:

```text
Análisis Territorial
Ganar Todo
Campo
Día D
ET-27
Socioeconómico
```

Los nombres visuales podrán cambiar posteriormente sin invalidar el principio.

---

### 10.52 Matriz de cobertura

Deberá existir conceptualmente una matriz:

```text
MODULE
CAPABILITY
DATA_DOMAIN
GOLDEN_CASE
LAYER_COVERAGE
CERTIFICATION_STATUS
```

---

### 10.53 Cobertura mínima

Una capacidad crítica no deberá considerarse completamente protegida únicamente con pruebas unitarias.

Deberá existir una combinación adecuada de:

- unit tests;
- contract tests;
- reconciliation tests;
- Golden Cases;
- end-to-end tests;
- visual verification cuando aplique.

---

### 10.54 Regresión

Una regresión es cualquier cambio que provoque que un comportamiento previamente certificado deje de cumplir el contrato.

Puede afectar:

```text
VALUE
TRUTH_STATUS
SOURCE
PERIOD
ENTITY
CERTIFICATION
DISPLAY
```

---

### 10.55 Regresión silenciosa

Será especialmente crítica una regresión que no produzca excepción técnica pero cambie el significado.

Ejemplo:

```text
SOURCE_MISSING
```

convertido nuevamente en:

```text
0
```

sin error de ejecución.

---

### 10.56 Gate de regresión

Antes de certificar una migración o cambio relevante deberán ejecutarse los Golden Cases afectados.

Resultado:

```text
PASS
FAIL
BLOCKED
```

---

### 10.57 `FAIL`

Un solo Golden Case crítico fallido deberá bloquear la certificación de la capacidad afectada hasta:

- corregir la causa;
- actualizar justificadamente el baseline;
- o documentar una decisión formal de bloqueo/deferimiento.

---

### 10.58 Cambio legítimo de baseline

Un Golden Case podrá cambiar cuando exista nueva evidencia certificada.

Ejemplo:

si posteriormente aparece una fuente primaria auténtica de `24G_*`, podrá revisarse:

```text
CARRY_FORWARD
```

hacia otra clasificación.

La modificación deberá conservar:

- baseline anterior;
- nueva evidencia;
- razón;
- fecha;
- versión.

---

### 10.59 Prohibición de modificar tests para hacerlos pasar

Queda prohibido alterar un Golden Case únicamente porque una implementación nueva produce un resultado diferente.

Primero deberá determinarse:

```text
IS IMPLEMENTATION WRONG?
OR
IS BASELINE OBSOLETE DUE TO NEW CERTIFIED EVIDENCE?
```

---

### 10.60 Versionado

Los Golden Cases deberán versionarse cuando cambien:

- evidencia;
- reglas;
- universo;
- fórmula;
- contrato;
- resultado esperado.

---

### 10.61 Reproducibilidad

Un Golden Case deberá poder ejecutarse nuevamente con suficiente información para reproducir su contexto.

---

### 10.62 Determinismo

Cuando el caso no dependa legítimamente de aleatoriedad, deberá producir el mismo resultado sobre la misma baseline certificada.

---

### 10.63 Datos mínimos de prueba

Los datasets de Golden Cases deberán ser tan pequeños como sea posible, pero tan completos como sea necesario para reproducir la condición semántica.

---

### 10.64 No depender innecesariamente de producción

Los Golden Cases deberán poder ejecutarse preferentemente sobre fixtures o snapshots certificados controlados, sin depender de cambios externos no gobernados.

---

### 10.65 Evidencia visual

Cuando una prueba requiera revisión visual, la evidencia podrá incluir:

```text
expected_render
actual_render
certified_values
comparison_result
```

La imagen será evidencia complementaria, no sustituto de validación de datos.

---

### 10.66 Auditoría de UI previa a liberación

Antes de liberar una interfaz migrada deberán comprobarse, como mínimo:

1. datos correctos;
2. periodos correctos;
3. universo correcto;
4. mapas correctos;
5. gráficas correctas;
6. tablas correctas;
7. estados de verdad correctos;
8. ausencia de simulación silenciosa;
9. Golden Cases relevantes en `PASS`.

---

### 10.67 Golden Cases como memoria institucional

Los Golden Cases deberán funcionar como memoria técnica de los incidentes que HEYTI ya aprendió a comprender.

Esto reduce la dependencia de conocimiento oral o de que un desarrollador recuerde manualmente una anomalía histórica.

---

### 10.68 Relación con onboarding

El manual de incorporación deberá enseñar al nuevo desarrollador:

- dónde están los Golden Cases;
- qué protegen;
- cómo ejecutarlos;
- qué significa un fallo;
- por qué no deben modificarse sin evidencia.

---

### 10.69 No implementar todavía toda la suite

Durante la fase normativa actual:

```text
NO MASS TEST CREATION
NO UI MIGRATION
NO BASELINE REWRITE
```

por efecto exclusivo de este capítulo.

Primero deberán definirse el Physical Mapping y el plan de implementación.

---

### 10.70 Baseline de certificación

El modelo definido en este capítulo constituye:

```text
HEYTI Golden Case & Regression Certification Model v1.0
```

Estado:

```text
NORMATIVE BASELINE
```

Será utilizado para proteger permanentemente la cadena:

```text
SOURCE
→ ETL
→ DB
→ CAPABILITY
→ RUNTIME
→ MATERIALIZATION
→ UI
```

---

## Fin del Capítulo 10

## Capítulo 11. Gates de migración, remediación y liberación certificada

### 11.1 Propósito

Este capítulo establece los controles obligatorios que deberán cumplirse antes de modificar, migrar, activar o liberar componentes de HEYTI-CORE que dependan de datos gobernados.

El objetivo es transformar la Auditoría de Veracidad de Datos en decisiones operativas verificables.

La secuencia general será:

```text
AUDIT
→ CLASSIFY
→ RECONCILE
→ CERTIFY
→ PLAN REMEDIATION
→ IMPLEMENT
→ VERIFY
→ MIGRATE
→ RELEASE
```

Ninguna etapa posterior deberá utilizarse para ocultar una etapa anterior incompleta.

---

### 11.2 Principio rector

> **HEYTI no migrará una capacidad porque el código esté listo; la migrará cuando sus datos, contratos y comportamiento estén suficientemente certificados.**

---

### 11.3 Gate vs prueba

Una prueba produce evidencia.

Un Gate toma una decisión utilizando evidencia.

Por tanto:

```text
TEST_RESULT
→ EVIDENCE

EVIDENCE + POLICY
→ GATE_DECISION
```

---

### 11.4 Estados de Gate

Los estados normativos serán:

```text
PASS
PASS_WITH_WARNINGS
FAIL
BLOCKED
NOT_APPLICABLE
```

---

### 11.5 `PASS`

Significa que los requisitos obligatorios del Gate han sido satisfechos y existe evidencia suficiente para continuar.

---

### 11.6 `PASS_WITH_WARNINGS`

Podrá utilizarse únicamente cuando:

- la condición pendiente esté comprendida;
- no produzca una afirmación falsa;
- no afecte una verdad crítica;
- exista trazabilidad;
- el riesgo residual sea aceptado.

No deberá utilizarse para evitar un `FAIL`.

---

### 11.7 `FAIL`

Significa que existe evidencia de incumplimiento.

La etapa posterior quedará bloqueada hasta corregir, reclasificar o justificar formalmente el caso.

---

### 11.8 `BLOCKED`

Significa que no existe evidencia suficiente para tomar una decisión responsable.

Ejemplo:

```text
historical_section
+
genealogy_status = UNRESOLVED
+
requested_current_reassignment
```

Resultado:

```text
BLOCKED
```

---

### 11.9 `NOT_APPLICABLE`

Indica que el Gate no corresponde al componente evaluado.

Su uso deberá justificarse; no será un atajo para omitir validaciones.

---

### 11.10 Gate G0 — Source Readiness

Antes de migrar una capacidad deberán estar identificadas sus fuentes.

Validaciones mínimas:

```text
logical_source_id
physical_location
source_type
domain
period
key_definition
record_count
certification_status
```

---

### 11.11 Criterio G0

Resultado `PASS` cuando las fuentes necesarias estén identificadas y clasificadas.

Si una fuente crítica permanece:

```text
UNVERIFIED_SOURCE
```

el Gate deberá ser:

```text
BLOCKED
```

o `FAIL`, según la evidencia disponible.

---

### 11.12 Gate G1 — Source Completeness

Deberá verificarse que el universo requerido por la capacidad esté suficientemente cubierto.

No significa necesariamente:

```text
100% rows present
```

Significa:

```text
100% relevant differences accounted for
```

---

### 11.13 Regla de completitud

> **Completitud certificada no exige delta cero; exige delta totalmente explicado.**

---

### 11.14 Gate G2 — Source → DB Reconciliation

Deberán reconciliarse:

```text
source_count
database_count
source_keys
database_keys
duplicates
rejections
unresolved
```

Resultado permitido:

```text
PASS
PASS_WITH_EXPLAINED_DELTA
```

El segundo deberá mapearse operativamente a un Gate compatible con `PASS_WITH_WARNINGS` solo cuando el delta no comprometa la capacidad.

---

### 11.15 Gate G3 — Temporal Territorial Integrity

Toda capacidad que utilice secciones deberá verificar:

```text
period
territorial_status
current_universe
historical_universe
resection_context
genealogy_status
```

---

### 11.16 Criterio G3

No podrá aprobarse una capacidad que:

- descarte historia por ausencia en cartografía vigente;
- reasigne predecesores automáticamente;
- confunda sección histórica con inválida;
- ignore una genealogía crítica conocida.

---

### 11.17 Gate G4 — Truth Status Integrity

Deberá verificarse que los valores relevantes conserven clasificación correcta.

Como mínimo:

```text
SOURCE_MISSING != OFFICIAL_ZERO
TRANSFORMATION_ZERO != OFFICIAL_ZERO
CARRY_FORWARD != OBSERVED_DATA
DERIVED_DATA != OBSERVED_DATA
SIMULATED_SOURCE != CERTIFIED_OBSERVATION
```

---

### 11.18 Gate G5 — ETL Safety

Los ETL involucrados deberán evaluarse contra el Capítulo 8.

Clasificación inicial:

```text
SAFE
NEEDS_ADAPTATION
SEMANTIC_RISK
BLOCKING_RISK
```

---

### 11.19 Criterio G5

Un ETL con:

```text
BLOCKING_RISK
```

no deberá utilizarse para una migración certificada hasta remediación y verificación.

---

### 11.20 Gate G6 — DB → Capability

La Capability deberá consultar:

- tablas correctas;
- universo correcto;
- periodo correcto;
- llaves correctas;
- estados de verdad correctos;
- históricos cuando corresponda.

---

### 11.21 Gate G7 — Capability → Runtime

Deberá comprobarse:

```text
contract
parameters
result
errors
traceability
truth metadata
certification metadata
```

---

### 11.22 Gate G8 — Runtime → Materialization

Materialization deberá preservar:

```text
value
truth_status
period
territorial_context
certification
warnings
provenance
```

cuando corresponda.

---

### 11.23 Gate G9 — Materialization → UI

La UI deberá representar correctamente:

- valores;
- periodos;
- secciones;
- mapas;
- gráficas;
- tablas;
- faltantes;
- carry-forward;
- históricos;
- advertencias.

---

### 11.24 Gate G10 — Golden Case Regression

Todos los Golden Cases críticos asociados a la capacidad deberán estar:

```text
PASS
```

antes de certificación final.

---

### 11.25 Gate G11 — End-to-End Certification

Deberá comprobarse:

```text
CERTIFIED_EXPECTED_VALUE
=
DB_VALUE
=
CAPABILITY_VALUE
=
RUNTIME_VALUE
=
MATERIALIZED_VALUE
=
DISPLAYED_VALUE
```

cuando la igualdad de valor aplique.

También deberán coincidir los atributos semánticos esperados.

---

### 11.26 Gate G12 — Release Readiness

Antes de liberar una capacidad deberán estar resueltos:

```text
critical_incidents
blocking_incidents
required_golden_cases
required_documentation
rollback_plan
```

---

### 11.27 Matriz de Gates

Cada capacidad deberá poder representarse mediante:

```text
CAPABILITY
G0
G1
G2
G3
G4
G5
G6
G7
G8
G9
G10
G11
G12
```

Esto permitirá conocer exactamente por qué una capacidad puede o no migrarse.

---

### 11.28 Prohibición de certificación por intuición

No serán criterios suficientes:

```text
looks correct
worked in V1
no exception occurred
the map opened
the numbers seem reasonable
```

---

### 11.29 Evidencia requerida

Una decisión de Gate deberá referenciar evidencia verificable.

Ejemplos:

```text
source_hash
audit_artifact
SQL_query_result
test_result
Golden_Case
contract_validation
visual_certification
```

---

### 11.30 Remediación

Una remediación es una modificación destinada a resolver una causa certificada.

Podrá afectar:

```text
SOURCE
ETL
DATABASE
CAPABILITY
RUNTIME
MATERIALIZATION
UI
DOCUMENTATION
```

---

### 11.31 Regla REM-001 — Remediar la causa

La corrección deberá aplicarse tan cerca de la causa raíz como sea razonablemente posible.

```text
FIX ROOT CAUSE
NOT DOWNSTREAM SYMPTOM
```

---

### 11.32 Regla REM-002 — Diagnóstico antes de remediación

No deberá modificarse físicamente un dato crítico mientras su causa permanezca:

```text
UNKNOWN
```

salvo una acción de contención explícita y reversible.

---

### 11.33 Regla REM-003 — Remediación no borra evidencia

Una corrección deberá preservar:

- estado anterior;
- causa;
- evidencia;
- acción;
- resultado;
- fecha;
- versión.

---

### 11.34 Regla REM-004 — Remediación reproducible

Cuando una corrección sea automatizable, deberá preferirse una transformación reproducible frente a una edición manual no trazable.

---

### 11.35 Regla REM-005 — Corrección manual excepcional

Una corrección manual deberá documentar:

```text
entity
old_value
new_value
reason
evidence
operator
timestamp
```

y requerirá validación posterior.

---

### 11.36 Regla REM-006 — No modificar fuente oficial

Una fuente primaria oficial deberá preservarse intacta.

Las correcciones de integración deberán ocurrir en capas derivadas o procesos controlados.

---

### 11.37 Regla REM-007 — No reescribir historia

Una remediación no deberá alterar un valor histórico únicamente para hacerlo compatible con el universo actual.

---

### 11.38 Regla REM-008 — Remediación temporal explícita

Si una corrección afecta temporalidad deberá declarar:

```text
source_period
target_period
valid_from
valid_to
```

cuando aplique.

---

### 11.39 Regla REM-009 — Genealogía primero

Antes de redistribuir información territorial histórica deberá existir una genealogía suficientemente certificada.

La genealogía, por sí sola, tampoco autoriza redistribución de valores.

---

### 11.40 Regla REM-010 — Reconciliar después de corregir

Toda remediación de datos deberá volver a ejecutar:

```text
SOURCE → TARGET RECONCILIATION
```

---

### 11.41 Regla REM-011 — Golden Cases después de corregir

Toda remediación relevante deberá ejecutar los Golden Cases afectados.

---

### 11.42 Regla REM-012 — No cerrar al implementar

```text
IMPLEMENTED != VERIFIED
```

Una remediación solo podrá considerarse verificada después de reconciliación y pruebas.

---

### 11.43 Plan de remediación

Toda remediación crítica deberá disponer de:

```text
remediation_id
incident_id
root_cause
affected_components
planned_change
expected_result
validation_plan
rollback_plan
status
```

---

### 11.44 Orden recomendado de remediación

Cuando exista una cadena de efectos:

```text
SOURCE/MASTER
→ ETL
→ DB
→ CAPABILITY
→ UI
```

deberá evaluarse la corrección desde el punto más cercano a la causa.

---

### 11.45 Caso de remediación — sección 2788

Diagnóstico certificado:

```text
official_2015_source = PRESENT
base_master = ABSENT
integration = LEFT_MERGE
```

Causa:

```text
BASE_MASTER_OMISSION
```

La futura remediación deberá corregir la integración del universo histórico, no inventar un registro únicamente en UI.

---

### 11.46 Gate para 2788

Antes de remediar físicamente deberán definirse:

- representación histórica;
- llave;
- relación con territorialidad;
- comportamiento DB;
- comportamiento Capability;
- Golden Case.

---

### 11.47 Caso de remediación — 2015 transformation zeros

Los ceros creados por `fillna(0)` no deberán simplemente cambiarse masivamente a `NULL` sin reconstruir:

- qué campos estaban ausentes;
- qué registros sí eran cero oficial;
- qué evidencia permite distinguirlos.

---

### 11.48 Caso de remediación — 24G

No deberá eliminarse ni sobrescribirse `24G_*` únicamente porque se detectó carry-forward.

Primero deberá decidirse el modelo físico que preserve:

```text
value
source_period = 2018
target_period = 2024
truth_status = CARRY_FORWARD
```

---

### 11.49 Caso de remediación — cinco resecciones

Las relaciones certificadas deberán poder persistirse posteriormente en el modelo territorial.

Sin embargo:

```text
CERTIFIED_GENEALOGY
```

no deberá provocar automáticamente:

```text
CERTIFIED_VALUE_REALLOCATION
```

---

### 11.50 Caso de remediación — 97 casillas

El objetivo inicial no será "hacer que entren las 97".

Será representar correctamente su condición histórica.

Después podrá evaluarse, casilla por casilla, si existe evidencia para una asignación vigente.

---

### 11.51 Caso de remediación — 26 secciones históricas

Estado:

```text
HISTORICAL_SECTION
genealogy_status = UNRESOLVED
```

La reasignación vigente permanecerá:

```text
BLOCKED
```

hasta nueva evidencia.

---

### 11.52 Migración de módulos

Una migración deberá iniciar por capacidades y contratos, no por reproducción visual.

Regla:

> **No migramos pantallas; migramos capacidades.**

---

### 11.53 Inventario previo de capacidad

Antes de migrar una función V1 deberá registrarse:

```text
V1_MODULE
V1_FUNCTION
V1_DATA_SOURCE
V1_USER_ACTION
HEYTI_CAPABILITY
TARGET_CONTRACT
DATA_TRUTH_DEPENDENCIES
```

---

### 11.54 Nombres V1 vs HEYTI

Deberá mantenerse la distinción:

```text
V1 actual
= cómo se llama y cómo se usa hoy

HEYTI-CORE
= qué capacidad representa realmente

Nueva interfaz
= cómo queremos que el usuario la vea, invoque y opere
```

---

### 11.55 Renombrado controlado

Los nombres físicos legacy con años podrán sustituirse por nombres lógicos temporalmente neutrales durante migración controlada.

Ejemplo conceptual:

```text
Datos_Electoral_con_2015.json
→ Datos_Electoral.json
```

Pero:

```text
NO_RENAME_DURING_AUDIT
```

permanece vigente hasta autorización de migración.

---

### 11.56 Gate de renombrado

Antes de renombrar una fuente deberán conocerse:

- consumidores;
- ETL;
- scripts;
- tests;
- documentación;
- backups;
- referencias runtime.

---

### 11.57 Prohibición de limpieza prematura

No deberán eliminarse:

```text
backup
legacy
duplicate copy
audit artifact
intermediate file
```

hasta conocer su clasificación y haber asegurado la trazabilidad necesaria.

---

### 11.58 Gate de limpieza

La limpieza física requerirá:

```text
CLASSIFIED
RECONCILED
MIGRATED
BACKED_UP
NO_ACTIVE_DEPENDENCY
```

---

### 11.59 Migración incremental

Los módulos deberán migrarse de forma incremental para limitar el radio de impacto y permitir certificación por capacidad.

---

### 11.60 Unidad recomendada de migración

La unidad preferida será:

```text
CAPABILITY + DATA CONTRACT + TESTS + MATERIALIZATION + UI INVOCATION
```

y no:

```text
WHOLE LEGACY SCREEN COPY
```

---

### 11.61 Definition of Ready para migración

Una capacidad estará lista para iniciar migración cuando:

- fuentes identificadas;
- incidentes críticos conocidos;
- contratos definidos;
- dependencias identificadas;
- Golden Cases definidos;
- Gate de datos no bloqueado.

---

### 11.62 Definition of Done para migración

Una capacidad estará terminada cuando:

- implementación completa;
- contratos validados;
- reconciliación aprobada;
- Golden Cases aprobados;
- end-to-end aprobado;
- UI certificada cuando aplique;
- documentación actualizada.

---

### 11.63 Rollback obligatorio

Toda migración con impacto relevante deberá contar con un mecanismo razonable de reversión.

El rollback deberá restaurar un estado conocido sin destruir evidencia.

---

### 11.64 No rollback hacia una falsedad conocida

Si el estado anterior contiene un error de verdad certificado, el rollback deberá entenderse como contingencia técnica y no como baseline semántica válida.

---

### 11.65 Liberación

Una liberación no deberá depender únicamente de:

```text
pytest passed
```

aunque las pruebas automatizadas sean obligatorias.

Deberá considerar también los Gates de verdad correspondientes.

---

### 11.66 Release Evidence Package

Cada liberación relevante deberá poder reunir:

```text
test_results
reconciliation_results
Golden_Case_results
open_incidents
accepted_warnings
migration_version
rollback_reference
```

---

### 11.67 Incidencias críticas y release

Si existe una incidencia:

```text
truth_impact = CRITICAL
```

que afecte directamente una capacidad y cuyo diagnóstico no esté certificado, la capacidad no deberá liberarse como certificada.

---

### 11.68 Excepción controlada

Una capacidad podrá liberarse parcialmente si:

- el componente afectado está bloqueado o marcado no disponible;
- la UI no afirma certeza inexistente;
- el riesgo está documentado;
- las funciones no afectadas están certificadas.

---

### 11.69 Certificación por capacidad

HEYTI no deberá requerir que todo el sistema alcance simultáneamente el mismo nivel de madurez.

Podrá existir:

```text
CAPABILITY_A = CERTIFIED
CAPABILITY_B = PROVISIONAL
CAPABILITY_C = BLOCKED
```

si la interfaz respeta esas diferencias.

---

### 11.70 Certificación de módulo

Un módulo podrá considerarse certificado cuando todas sus capacidades críticas requeridas para la versión estén certificadas y no existan bloqueos ocultos.

---

### 11.71 Certificación de demo

Una demo HEYTI deberá declarar claramente qué capacidades son:

```text
CERTIFIED
PROVISIONAL
DEMO_ONLY
UNAVAILABLE
```

cuando exista diferencia relevante.

---

### 11.72 Regla para el Día D

Las capacidades operativas de Día D deberán recibir un nivel de exigencia especialmente alto cuando sus resultados puedan influir en decisiones inmediatas.

La ausencia de evidencia no deberá ocultarse para mantener continuidad visual.

---

### 11.73 Regla para Análisis Territorial

Los mapas y análisis deberán respetar la temporalidad de las secciones y no proyectar automáticamente historia sobre geometría vigente.

---

### 11.74 Regla para Ganar Todo

Los escenarios y métricas derivadas deberán identificar claramente qué componentes son observados y cuáles calculados.

---

### 11.75 Regla para Campo

La migración deberá conservar reglas semánticas de duplicidad, identidad y validación de registros.

---

### 11.76 Regla para ET-27

Las capacidades de estructura territorial deberán diferenciar estructura actual, historia y relaciones genealógicas certificadas.

---

### 11.77 Regla para Socioeconómico

La ausencia de fuente válida deberá producir:

```text
UNAVAILABLE
```

antes que un fallback simulado silencioso.

---

### 11.78 Auditoría posterior a migración

Una migración aprobada deberá ser seguida por una verificación posterior sobre el entorno integrado.

Esto protege contra diferencias entre:

```text
TEST_ENVIRONMENT
```

y:

```text
INTEGRATED_RUNTIME
```

---

### 11.79 Reapertura

Si después de migración aparece evidencia contradictoria, la certificación correspondiente deberá poder reabrirse.

La certificación no es una declaración irreversible.

---

### 11.80 Trazabilidad de decisión

Toda decisión crítica de:

```text
MIGRATE
BLOCK
DEFER
RELEASE
```

deberá poder explicar:

```text
WHY
BASED_ON_WHAT_EVIDENCE
WHO/WHAT_APPROVED
WHEN
UNDER_WHICH_VERSION
```

---

### 11.81 No cambios físicos por este capítulo

Durante la fase normativa actual:

```text
NO DB MUTATION
NO ETL EDIT
NO FILE RENAME
NO MODULE MIGRATION
NO UI MIGRATION
NO CLEANUP
```

por efecto exclusivo de este capítulo.

---

### 11.82 Invariantes de migración

#### MIG-INV-001

```text
CODE_READY != DATA_READY
```

#### MIG-INV-002

```text
TESTS_PASS != RELEASE_CERTIFIED
```

#### MIG-INV-003

```text
MIGRATED != VERIFIED
```

#### MIG-INV-004

Una incidencia crítica desconocida bloquea la certificación de la capacidad afectada.

#### MIG-INV-005

Toda remediación crítica requiere verificación posterior.

#### MIG-INV-006

Toda migración visual crítica deberá compararse contra valores esperados certificados.

#### MIG-INV-007

Ningún renombrado o cleanup deberá romper trazabilidad.

---

### 11.83 Resultado esperado

El modelo operativo de HEYTI será:

```text
DATA READY?
    ↓
YES
    ↓
CAPABILITY READY?
    ↓
YES
    ↓
RUNTIME / MATERIALIZATION READY?
    ↓
YES
    ↓
GOLDEN CASES PASS?
    ↓
YES
    ↓
UI CERTIFIED?
    ↓
YES
    ↓
RELEASE
```

Cualquier respuesta negativa deberá:

```text
BLOCK
REMEDIATE
OR EXPLICITLY DEFER
```

---

### 11.84 Principio final

> **HEYTI no deberá liberar una capacidad únicamente porque pueda ejecutarla; deberá liberarla cuando pueda demostrar qué sabe, de dónde lo sabe y con qué nivel de certeza lo sabe.**

---

### 11.85 Baseline de migración

El modelo definido en este capítulo constituye:

```text
HEYTI Migration, Remediation & Certified Release Gate Model v1.0
```

Estado:

```text
NORMATIVE BASELINE
```

Será utilizado durante la siguiente etapa para convertir la gobernanza documental en un mapa físico de fuentes, tablas, contratos, Capabilities, Runtime, Materialization, módulos y pruebas.

---

## Fin del Capítulo 11

## Capítulo 12. Truth Contract Physical Mapping

### 12.1 Propósito

Este capítulo define el puente entre la gobernanza normativa de verdad de datos y su futura implementación física en HEYTI-CORE.

Los capítulos anteriores establecieron qué significa un dato confiable, cómo debe clasificarse, cómo debe transformarse, cómo debe preservarse hasta la UI y qué Gates deben cumplirse.

Este capítulo responde ahora:

```text
WHERE DOES EACH TRUTH ATTRIBUTE LIVE?
HOW DOES IT TRAVEL?
WHO OWNS IT?
HOW IS IT VALIDATED?
```

El objetivo no es modificar todavía la base de datos ni el código, sino definir el mapa físico que deberá guiar la implementación posterior.

---

### 12.2 Principio rector

> **Ningún atributo de verdad deberá existir únicamente como conocimiento implícito de un desarrollador.**

Toda propiedad crítica deberá tener una ubicación, propietario y mecanismo de trazabilidad definidos.

---

### 12.3 Modelo de capas físicas

El Physical Mapping deberá considerar:

```text
SOURCE FILE / OFFICIAL SOURCE
        ↓
SOURCE REGISTRY
        ↓
ETL INPUT CONTRACT
        ↓
ETL / TRANSFORMATION
        ↓
DATABASE
        ↓
CAPABILITY PROVIDER
        ↓
CAPABILITY CONTRACT
        ↓
RUNTIME
        ↓
MATERIALIZATION
        ↓
RESPONSE CONTRACT
        ↓
UI
        ↓
GOLDEN CASE / AUDIT EVIDENCE
```

---

### 12.4 Separación entre modelo normativo y modelo físico

El modelo normativo define conceptos como:

```text
truth_status
territorial_status
genealogy_status
certification_status
anomaly_code
```

El modelo físico decidirá posteriormente si estos atributos se representan mediante:

- columnas;
- tablas relacionadas;
- metadata;
- objetos Python;
- contratos;
- enums;
- eventos;
- evidencias;
- combinaciones de los anteriores.

---

### 12.5 Regla PHY-001 — No duplicar semántica sin autoridad

Si un mismo atributo aparece en varias capas, deberá existir una fuente de autoridad claramente definida.

Ejemplo:

```text
truth_status
```

podrá viajar por DB, Capability y Materialization, pero no deberá adquirir significados diferentes en cada capa.

---

### 12.6 Regla PHY-002 — Identidad lógica antes que ruta física

Las fuentes deberán identificarse conceptualmente mediante:

```text
logical_source_id
```

y no depender exclusivamente de una ruta como:

```text
D:\...\archivo.json
```

La ruta será metadata de resolución física.

---

### 12.7 Source Registry conceptual

HEYTI deberá evolucionar hacia un registro de fuentes que pueda representar:

```text
source_id
logical_name
domain
source_type
physical_location
origin
period
schema_version
hash
record_count
key_definition
certification_status
active_status
```

---

### 12.8 Estado del Source Registry

Durante esta fase:

```text
CONCEPTUAL_ONLY
```

No se autoriza todavía la creación de tablas por efecto exclusivo de este capítulo.

---

### 12.9 Logical Source ID

Ejemplos conceptuales:

```text
ELECTORAL_MASTER
SOCIOECONOMIC_MASTER
SECTION_GEOMETRY
FIELD_POINTS
CASILLA_SOURCE
ELECTORAL_2015_A
ELECTORAL_2015_DF
ELECTORAL_2015_DL
```

Estos IDs deberán sobrevivir a futuros renombrados físicos.

---

### 12.10 Temporalidad de fuentes

Una fuente deberá poder declarar:

```text
source_period
target_period
```

cuando ambos sean distintos.

Esto es indispensable para casos como:

```text
18G → 24G
```

---

### 12.11 Input Contract físico

Cada ETL crítico deberá poder resolver un contrato de entrada con:

```text
source_id
expected_schema
required_fields
key_definition
expected_period
expected_domain
allowed_source_types
expected_certification
```

---

### 12.12 Output Contract físico

Cada ETL deberá declarar:

```text
target_schema
target_table
business_key
truth_mapping
reject_policy
reconciliation_policy
```

---

### 12.13 Transformation Registry conceptual

Las transformaciones con impacto semántico deberán poder registrarse mediante:

```text
transformation_id
version
input_source_id
output_target
rule
missing_policy
join_policy
aggregation_policy
temporal_policy
```

---

### 12.14 Ejemplo de transformación 2015

Conceptualmente:

```text
transformation_id = ELECTORAL_2015_INTEGRATION
input =
    ELECTORAL_MASTER
    ELECTORAL_2015_A
    ELECTORAL_2015_DF
    ELECTORAL_2015_DL
join_policy = LEFT_MERGE_ON_SECTION
missing_policy = FILL_ZERO
```

La auditoría ya demuestra que esa política requiere remediación semántica.

---

### 12.15 Truth Status físico

El modelo físico deberá permitir representar al menos:

```text
OBSERVED_DATA
OFFICIAL_ZERO
SOURCE_MISSING
TRANSFORMATION_ZERO
CARRY_FORWARD
DERIVED_DATA
UNAVAILABLE
```

---

### 12.16 Territorial Status físico

Deberá permitir representar:

```text
CURRENT_SECTION
HISTORICAL_SECTION
RESECTION_PREDECESSOR
RESECTION_SUCCESSOR
```

---

### 12.17 Genealogy Status físico

Deberá distinguir:

```text
CERTIFIED_MAPPING
UNRESOLVED
NOT_APPLICABLE
```

---

### 12.18 Certification Status físico

Deberá distinguir:

```text
CERTIFIED
PROVISIONAL
REJECTED
```

---

### 12.19 Anomaly Code físico

Las anomalías deberán poder referenciar códigos estables como:

```text
MASTER_OMISSION
TEMPORAL_UNIVERSE_MISMATCH
CARRY_FORWARD_18G_TO_24G
TRANSFORMATION_FILLNA_ZERO
GENEALOGY_GAP
```

---

### 12.20 Regla PHY-003 — Ejes independientes

Los siguientes atributos no deberán colapsarse en una sola columna o estado:

```text
truth_status
territorial_status
genealogy_status
certification_status
anomaly_code
```

Ejemplo válido:

```text
truth_status = OBSERVED_DATA
territorial_status = HISTORICAL_SECTION
genealogy_status = UNRESOLVED
certification_status = CERTIFIED
anomaly_code = NULL
```

---

### 12.21 Metadata por registro vs metadata por conjunto

No toda metadata deberá repetirse necesariamente por fila.

El diseño físico deberá distinguir:

```text
ROW_LEVEL_METADATA
DATASET_LEVEL_METADATA
TRANSFORMATION_LEVEL_METADATA
RUN_LEVEL_METADATA
```

---

### 12.22 Row-level metadata

Será necesaria cuando dos registros del mismo dataset puedan tener distinto estado.

Ejemplo:

```text
OFFICIAL_ZERO
vs
TRANSFORMATION_ZERO
```

---

### 12.23 Dataset-level metadata

Será apropiada para propiedades compartidas como:

```text
source_hash
source_origin
dataset_period
schema_version
```

---

### 12.24 Transformation-level metadata

Podrá representar:

```text
transformation_id
transformation_version
rule
derived_from
```

---

### 12.25 Run-level metadata

Podrá representar:

```text
run_id
started_at
finished_at
input_count
output_count
reject_count
result_status
```

---

### 12.26 Modelo de evidencia

Las entidades físicas deberán poder referenciar evidencia sin almacenar necesariamente toda la evidencia dentro de la misma tabla.

Conceptualmente:

```text
evidence_reference
```

podrá apuntar a:

- artifact;
- source;
- query result;
- audit report;
- Golden Case;
- official document.

---

### 12.27 Data Truth Incident Registry conceptual

El modelo futuro podrá incorporar:

```text
metadata.data_truth_incident
```

o equivalente.

Campos conceptuales:

```text
incident_id
incident_code
domain
incident_type
diagnosis_status
remediation_status
truth_impact
severity
root_cause
resolution
evidence_reference
```

---

### 12.28 Regla PHY-004 — Incidente no debe mezclarse con estado de dato

Un dato puede estar correctamente clasificado aunque exista una incidencia asociada.

Ejemplo:

```text
truth_status = OBSERVED_DATA
anomaly_code = MASTER_OMISSION
```

La anomalía describe el proceso o universo, no niega necesariamente la observación.

---

### 12.29 Territorial history

La tabla existente:

```text
territorial.section_history
```

demuestra que la arquitectura ya contempla historia territorial.

Sin embargo, la auditoría confirmó que actualmente no contiene la genealogía necesaria para los 32 casos analizados.

---

### 12.30 No poblar `section_history` todavía

Durante esta etapa:

```text
NO INSERT
NO UPDATE
NO BACKFILL
```

por efecto exclusivo de este documento.

Primero deberá definirse el contrato físico exacto.

---

### 12.31 Section Lineage conceptual

El diseño podrá requerir una estructura específica para relaciones:

```text
1 → 1
1 → N
N → 1
N → N
```

Conceptualmente:

```text
section_lineage
```

---

### 12.32 Campos conceptuales de lineage

Podrían incluir:

```text
predecessor_section_code
successor_section_code
effective_period
relationship_type
certification_status
evidence_reference
```

La definición final será materia de diseño físico.

---

### 12.33 Regla PHY-005 — Lineage no almacena redistribución implícita

La existencia de una relación predecesor/sucesor no deberá implicar automáticamente:

```text
allocation_weight
```

Si existiera un peso, deberá tener evidencia y contrato propios.

---

### 12.34 Caso físico de las cinco resecciones

El modelo deberá poder representar sin pérdida:

```text
343  → 3290–3299
1059 → 3300–3307
1110 → 3308–3313
1634 → 3278–3283
1647 → 3284–3289
```

con:

```text
genealogy_status = CERTIFIED_MAPPING
```

---

### 12.35 Caso físico de las 26 secciones

Deberá poder representarse:

```text
territorial_status = HISTORICAL_SECTION
genealogy_status = UNRESOLVED
```

sin fabricar sucesor.

---

### 12.36 Caso físico de 2788

El modelo deberá poder preservar:

```text
section_code = 2788
truth_status = OBSERVED_DATA
territorial_status = HISTORICAL_SECTION
anomaly_code = MASTER_OMISSION
```

para el contexto 2015 certificado.

---

### 12.37 Electoral physical mapping

Los resultados electorales deberán poder vincular:

```text
section
election
party_or_metric
value
truth_status
source
period
transformation
```

sin depender únicamente del valor.

---

### 12.38 Caso de `electoral.section_result`

La tabla actual contiene:

```text
result_id
section_id
election_id
party_id
votes
total_votes
nominal_list
participation_pct
created_at
```

El Physical Mapping deberá determinar posteriormente cómo asociar la metadata de verdad sin romper el modelo existente.

---

### 12.39 No alterar `electoral.section_result` todavía

Este capítulo no autoriza:

```text
ALTER TABLE
ADD COLUMN
DATA RELOAD
```

---

### 12.40 Socioeconomic physical mapping

Los indicadores deberán poder relacionar:

```text
section
indicator
period
value
unit
source
truth_status
certification_status
```

---

### 12.41 Field physical mapping

Campo deberá preservar:

```text
actor_identity
location
assignment
source
validation_status
duplicate_rule
```

y evitar confundir múltiples registros legítimos en una misma sección con duplicidad.

---

### 12.42 Election Day physical mapping

Día D deberá poder preservar tanto:

```text
section_code_as_reported
```

como la resolución territorial utilizada por HEYTI.

Esto permitirá conservar las 97 casillas históricas aunque el modelo vigente no pueda todavía reasignarlas.

---

### 12.43 Regla PHY-006 — Conservar identidad reportada

Una normalización o resolución territorial no deberá sobrescribir la identidad territorial original reportada por la fuente.

---

### 12.44 Capability models

Los modelos Python utilizados por Capabilities deberán evolucionar para transportar metadata semántica cuando sea requerida.

Conceptualmente:

```text
TruthAwareValue
```

podría representar:

```text
value
truth_status
source_reference
period
certification_status
```

---

### 12.45 No imponer una clase todavía

`TruthAwareValue` es un concepto de diseño, no una instrucción de implementación inmediata.

El diseño deberá integrarse con los contratos existentes de HEYTI.

---

### 12.46 Runtime contract mapping

Runtime deberá recibir y devolver objetos cuya semántica pueda preservarse sin depender de convenciones implícitas.

---

### 12.47 Materialization mapping

Materialization deberá disponer de información suficiente para construir:

```text
value blocks
warnings
evidence
trace
availability state
```

sin consultar nuevamente fuentes legacy.

---

### 12.48 Response Contract

El contrato HEYTI_RESPONSE deberá evolucionar de forma compatible para representar, cuando aplique:

```text
truth
provenance
certification
warnings
```

sin convertir toda respuesta simple en una estructura innecesariamente pesada.

---

### 12.49 Regla PHY-007 — Metadata proporcional

No todos los valores necesitan desplegar toda la metadata al usuario.

Pero toda información crítica deberá conservar suficiente trazabilidad internamente.

---

### 12.50 UI mapping

La UI deberá recibir contratos ya gobernados.

No deberá reconstruir truth status a partir de:

- nombre del archivo;
- año del campo;
- ausencia de valor;
- color;
- posición;
- convenciones legacy.

---

### 12.51 Golden Case mapping

Cada Golden Case deberá poder señalar:

```text
source_reference
expected_db_state
expected_capability_state
expected_runtime_state
expected_materialized_state
expected_ui_state
```

según su alcance.

---

### 12.52 Audit artifact mapping

Los artefactos generados durante HDRM deberán clasificarse como:

```text
AUDIT_EVIDENCE
```

y no como fuentes productivas por defecto.

---

### 12.53 Regla PHY-008 — Artifact no es runtime source

Un archivo creado para auditoría no deberá convertirse accidentalmente en fuente de Runtime o ETL.

---

### 12.54 Physical Source Matrix

Deberá construirse una matriz con:

```text
LOGICAL_SOURCE_ID
PHYSICAL_PATH
DOMAIN
PERIOD
SOURCE_TYPE
HASH
KEY
RECORD_COUNT
CONSUMER
STATUS
```

---

### 12.55 ETL Mapping Matrix

Deberá construirse:

```text
ETL
INPUT_SOURCE
INPUT_CONTRACT
TRANSFORMATION
TARGET_TABLE
REJECT_POLICY
RECONCILIATION
TRUTH_RISK
```

---

### 12.56 DB Mapping Matrix

Deberá construirse:

```text
DOMAIN
TABLE
BUSINESS_KEY
TEMPORAL_KEY
SOURCE_LINK
TRUTH_METADATA
KNOWN_GAPS
```

---

### 12.57 Capability Mapping Matrix

Deberá construirse:

```text
CAPABILITY
DOMAIN
DB_DEPENDENCY
INPUT_CONTRACT
OUTPUT_CONTRACT
TRUTH_REQUIREMENTS
GOLDEN_CASES
```

---

### 12.58 Runtime / Materialization Matrix

Deberá registrar:

```text
CAPABILITY
RUNTIME_PATH
MATERIALIZER
RESPONSE_BLOCK
TRUTH_METADATA
WARNINGS
TRACE
```

---

### 12.59 UI Mapping Matrix

Para cada función visual:

```text
V1_MODULE
V1_ACTION
HEYTI_CAPABILITY
UI_CONTROL
DATA_CONTRACT
EXPECTED_VISUAL
GOLDEN_CASE
```

---

### 12.60 Matriz de trazabilidad maestra

Las matrices anteriores deberán poder integrarse conceptualmente en:

```text
SOURCE
→ ETL
→ DB
→ CAPABILITY
→ RUNTIME
→ MATERIALIZATION
→ UI
→ GOLDEN_CASE
```

Esta será una pieza central de la migración.

---

### 12.61 Regla PHY-009 — Cero huérfanos

Ningún elemento crítico deberá quedar sin relación conocida.

Ejemplos de huérfanos prohibidos:

```text
SOURCE_WITHOUT_CONSUMER_CLASSIFICATION
ETL_WITHOUT_SOURCE
TABLE_WITHOUT_PROVENANCE
CAPABILITY_WITHOUT_DATA_DEPENDENCY
UI_CONTROL_WITHOUT_CAPABILITY
GOLDEN_CASE_WITHOUT_EVIDENCE
```

---

### 12.62 Regla PHY-010 — Cero dependencias ocultas

Los módulos no deberán depender silenciosamente de:

- archivos legacy;
- localStorage;
- variables globales V1;
- rutas relativas accidentales;
- fallback DEMO;
- archivos backup.

Toda dependencia deberá quedar clasificada.

---

### 12.63 Estado físico

Cada elemento del mapping deberá poder clasificarse como:

```text
CURRENT
LEGACY
TARGET
TRANSITIONAL
AUDIT_ONLY
UNRESOLVED
```

---

### 12.64 Prioridad de implementación

El Physical Mapping deberá implementarse en orden de dependencia:

```text
SOURCES
→ ETL
→ DB
→ CAPABILITY
→ RUNTIME
→ MATERIALIZATION
→ UI
```

---

### 12.65 No diseñar desde la UI hacia atrás sin datos

El diseño visual podrá definir experiencia de usuario, pero no deberá forzar la invención de datos o contratos inexistentes.

---

### 12.66 Interfaz y capacidad

El rediseño deberá mantener:

```text
UI NAME
≠
INTERNAL CAPABILITY IDENTITY
```

Esto permitirá cambiar nombres y organización visual sin romper contratos de datos.

---

### 12.67 Seguridad de configuración

El Physical Mapping deberá identificar también dependencias sensibles:

```text
database_credentials
connection_strings
secrets
tokens
```

Las nuevas implementaciones deberán resolverlas mediante configuración segura.

---

### 12.68 Credenciales legacy

La existencia de credenciales embebidas en ETL legacy deberá clasificarse como deuda de seguridad.

Durante D4:

```text
DO NOT REPEAT SECRET
DO NOT REFACTOR YET
```

La remediación se ejecutará en fase controlada.

---

### 12.69 Versionado del mapping

Las matrices físicas deberán tener versión.

Un cambio de:

- fuente;
- tabla;
- ETL;
- contrato;
- Capability;
- Materializer;

deberá actualizar la trazabilidad correspondiente.

---

### 12.70 Definition of Complete del Physical Mapping

El mapping estará completo cuando, para cada capacidad objetivo, pueda responderse:

1. ¿Qué fuente utiliza?
2. ¿Dónde está?
3. ¿Qué ETL la transforma?
4. ¿Dónde persiste?
5. ¿Qué llave y periodo usa?
6. ¿Qué truth status puede producir?
7. ¿Qué Capability la consulta?
8. ¿Cómo viaja por Runtime?
9. ¿Cómo se materializa?
10. ¿Cómo se presenta?
11. ¿Qué Golden Case la protege?
12. ¿Qué incidencias siguen abiertas?

---

### 12.71 Resultado de mapping

Cada ruta deberá clasificarse:

```text
READY
READY_WITH_REMEDIATION
BLOCKED
UNRESOLVED
NOT_REQUIRED
```

---

### 12.72 `READY`

Toda la cadena está identificada y no existen bloqueos semánticos conocidos para iniciar implementación controlada.

---

### 12.73 `READY_WITH_REMEDIATION`

La cadena está identificada, la causa de los problemas está certificada y existe un plan de remediación previo o simultáneo claramente definido.

---

### 12.74 `BLOCKED`

Existe una dependencia crítica que no puede resolverse responsablemente con la evidencia disponible.

---

### 12.75 `UNRESOLVED`

El mapping aún no ha determinado una parte de la cadena.

No deberá confundirse con `BLOCKED`: puede tratarse simplemente de investigación pendiente.

---

### 12.76 Physical Mapping y onboarding

El manual de incorporación deberá utilizar la matriz maestra para enseñar la arquitectura real del sistema.

Orden recomendado:

```text
Governance
→ Source Matrix
→ ETL Matrix
→ DB Matrix
→ Capability Matrix
→ Runtime / Materialization Matrix
→ UI Matrix
→ Golden Cases
```

---

### 12.77 No mutación durante construcción del mapping

Mientras se construya la baseline física:

```text
NO FILE MOVE
NO FILE DELETE
NO FILE RENAME
NO DB MUTATION
NO ETL REMEDIATION
NO MODULE MIGRATION
```

salvo autorización explícita y controlada.

---

### 12.78 Invariantes físicas

#### PHY-INV-001

```text
EVERY CRITICAL VALUE HAS PROVENANCE
```

#### PHY-INV-002

```text
EVERY CRITICAL TRANSFORMATION HAS A RULE
```

#### PHY-INV-003

```text
EVERY CRITICAL CAPABILITY HAS DATA DEPENDENCIES
```

#### PHY-INV-004

```text
EVERY CRITICAL UI OUTPUT HAS A CAPABILITY CONTRACT
```

#### PHY-INV-005

```text
EVERY CRITICAL MIGRATED PATH HAS A GOLDEN CASE
```

#### PHY-INV-006

```text
NO HISTORICAL IDENTITY IS LOST BECAUSE CURRENT FK LOOKUP FAILS
```

#### PHY-INV-007

```text
NO SECRET IS PROMOTED INTO DOCUMENTATION OR TEST EVIDENCE
```

---

### 12.79 Resultado esperado

Al finalizar el Physical Mapping, HEYTI deberá disponer de una cadena explícita:

```text
SOURCE_ID
  ↓
PHYSICAL_SOURCE
  ↓
ETL
  ↓
DATABASE_OBJECT
  ↓
CAPABILITY
  ↓
RUNTIME
  ↓
MATERIALIZER
  ↓
RESPONSE_CONTRACT
  ↓
UI_CONTROL
  ↓
GOLDEN_CASE
```

sin dependencias críticas desconocidas.

---

### 12.80 Principio final

> **La gobernanza se vuelve arquitectura cuando cada verdad puede señalar exactamente dónde nace, dónde se transforma, dónde vive, cómo viaja y cómo se demuestra.**

---

### 12.81 Baseline de Physical Mapping

El modelo definido en este capítulo constituye:

```text
HEYTI Truth Contract Physical Mapping Model v1.0
```

Estado:

```text
NORMATIVE BASELINE
```

Su siguiente aplicación será construir las matrices físicas reales de HEYTI-CORE antes de iniciar la remediación y migración de módulos.

---

## Fin del Capítulo 12

## Capítulo 13. Matriz Maestra de Trazabilidad y Certificación de Capacidades

### 13.1 Propósito

Este capítulo define la estructura normativa de la Matriz Maestra de Trazabilidad que deberá conectar, para cada capacidad de HEYTI-CORE, sus fuentes, transformaciones, persistencia, contratos, ejecución, materialización, presentación y evidencia de certificación.

Los capítulos anteriores establecieron las reglas de verdad y el modelo de Physical Mapping.

Este capítulo convierte ese modelo en una unidad operacional de control.

La pregunta central será:

```text
FOR THIS HEYTI CAPABILITY,
CAN WE TRACE EVERY CRITICAL OUTPUT
BACK TO CERTIFIED EVIDENCE?
```

---

### 13.2 Principio rector

> **Una capacidad no estará completamente gobernada mientras no pueda recorrerse su cadena de trazabilidad en ambos sentidos.**

Dirección de producción:

```text
SOURCE
→ ETL
→ DB
→ CAPABILITY
→ RUNTIME
→ MATERIALIZATION
→ UI
```

Dirección de auditoría:

```text
UI
→ MATERIALIZATION
→ RUNTIME
→ CAPABILITY
→ DB
→ ETL
→ SOURCE
```

---

### 13.3 Unidad principal: Capability Trace

La unidad principal de la matriz será una capacidad funcional de HEYTI.

Conceptualmente:

```text
CAPABILITY_TRACE
```

deberá relacionar:

```text
capability_id
business_purpose
data_domains
sources
etl
database_objects
runtime_contract
materializer
ui_invocation
golden_cases
incidents
certification_status
```

---

### 13.4 Capacidad vs módulo

Un módulo visual puede contener múltiples capacidades.

Por tanto:

```text
MODULE != CAPABILITY
```

Ejemplo conceptual:

```text
Análisis Territorial
    ├─ describe_section
    ├─ compare_sections
    ├─ electoral_history
    ├─ territorial_context
    └─ strategic_summary
```

Los nombres son ilustrativos; la definición final se realizará durante migración.

---

### 13.5 Regla TRACE-001 — Trazabilidad por capacidad

La matriz no deberá limitarse a indicar que un módulo usa un archivo.

Deberá mostrar qué capacidad consume qué datos y para producir qué salida.

---

### 13.6 Regla TRACE-002 — Trazabilidad por campo crítico

Cuando un resultado crítico combine múltiples campos, deberá poder conocerse la procedencia de cada componente relevante.

---

### 13.7 Regla TRACE-003 — Trazabilidad bidireccional

Deberá poder responderse:

```text
WHAT PRODUCED THIS OUTPUT?
```

y también:

```text
WHAT OUTPUTS DEPEND ON THIS SOURCE?
```

---

### 13.8 Identidad de Capability

Cada Capability deberá disponer de un identificador estable independiente del nombre visual.

Ejemplo:

```text
describe_section
```

podrá conservar su identidad aunque la UI muestre posteriormente otro nombre al usuario.

---

### 13.9 Business Purpose

Cada Capability deberá declarar brevemente:

```text
WHAT QUESTION DOES THIS CAPABILITY ANSWER?
```

Esto evitará migrar código cuya finalidad real no esté comprendida.

---

### 13.10 Data Domains

La matriz deberá declarar los dominios utilizados:

```text
TERRITORIAL
ELECTORAL
SOCIOECONOMIC
FIELD
ELECTION_DAY
ANALYTICS
```

Una Capability podrá depender de más de uno.

---

### 13.11 Source Dependency

Por cada fuente deberá registrarse:

```text
logical_source_id
period
source_type
certification_status
```

No será suficiente registrar únicamente la ruta física.

---

### 13.12 ETL Dependency

La matriz deberá identificar el proceso que materializa la fuente hacia DB.

Para los procesos existentes, las rutas deberán documentarse de forma completa.

Ejemplos actuales:

```text
D:\GitHub\AT-27-30-core\database\etl\008_load_electoral_full.py
D:\GitHub\AT-27-30-core\database\etl\010_load_socioeconomico_full.py
D:\GitHub\AT-27-30-core\database\etl\003_load_sections_full.py
D:\GitHub\AT-27-30-core\database\etl\etl_011_campo.py
D:\GitHub\AT-27-30-core\database\etl\etl_013_casillas.py
```

Estas referencias describen el estado auditado actual y no autorizan modificaciones.

---

### 13.13 ETL Risk

Cada dependencia ETL deberá poder clasificarse:

```text
SAFE
NEEDS_ADAPTATION
SEMANTIC_RISK
BLOCKING_RISK
NOT_AUDITED
```

---

### 13.14 Database Dependency

La matriz deberá identificar:

```text
schema
table
business_key
temporal_key
join_path
```

cuando corresponda.

---

### 13.15 Truth Dependency

Deberá declararse qué estados de verdad puede encontrar una Capability.

Ejemplo:

```text
OBSERVED_DATA
CARRY_FORWARD
SOURCE_MISSING
HISTORICAL_SECTION
```

Esto permitirá diseñar contratos que no asuman un único estado.

---

### 13.16 Runtime Dependency

La matriz deberá identificar cómo la Capability entra al Runtime y qué contrato utiliza.

---

### 13.17 Materialization Dependency

Deberá registrarse:

```text
materializer
response_contract
response_blocks
warning_behavior
trace_behavior
```

---

### 13.18 UI Invocation

La matriz deberá identificar cómo el usuario invoca la Capability.

Ejemplos conceptuales:

```text
button
map_click
section_search
selector
question
workflow
```

---

### 13.19 Regla TRACE-004 — UI control no es Capability

Un botón podrá cambiar o desaparecer sin que la capacidad deje de existir.

La matriz deberá enlazar:

```text
UI_CONTROL → CAPABILITY
```

y no tratarlos como la misma entidad.

---

### 13.20 V1 Functional Reference

Durante migración podrá registrarse:

```text
v1_module
v1_file
v1_action
```

como referencia de procedencia funcional.

V1 no será automáticamente la especificación final.

---

### 13.21 Target UI Reference

La matriz podrá registrar:

```text
target_module
target_ui_action
```

una vez aprobado el rediseño.

Esto permitirá separar legado, Core y experiencia final.

---

### 13.22 Golden Case Dependency

Toda Capability crítica deberá relacionarse con uno o más Golden Cases.

Ejemplo:

```text
describe_section
→ GC-E2E-HISTORICAL-001
→ GC-E2E-2788-001
```

cuando esas condiciones formen parte de su comportamiento.

---

### 13.23 Incident Dependency

La matriz deberá indicar incidencias de Data Truth que puedan afectar una Capability.

Ejemplo:

```text
CARRY_FORWARD_18G_TO_24G
```

deberá aparecer en cualquier Capability que pretenda utilizar `24G_*`.

---

### 13.24 Certification Status de Capability

Estados recomendados:

```text
NOT_AUDITED
AUDIT_IN_PROGRESS
BLOCKED
PROVISIONAL
READY_FOR_MIGRATION
MIGRATED
E2E_VERIFIED
CERTIFIED
```

---

### 13.25 `NOT_AUDITED`

La capacidad existe o se ha identificado, pero todavía no se ha recorrido su cadena de datos.

---

### 13.26 `AUDIT_IN_PROGRESS`

La trazabilidad se está construyendo y todavía existen elementos sin resolver.

---

### 13.27 `BLOCKED`

Existe una dependencia crítica sin resolución suficiente.

---

### 13.28 `PROVISIONAL`

La capacidad puede operar bajo condiciones conocidas, pero aún no cumple todos los Gates de certificación.

---

### 13.29 `READY_FOR_MIGRATION`

La cadena física está suficientemente comprendida y los riesgos necesarios tienen plan de remediación.

---

### 13.30 `MIGRATED`

La capacidad ha sido implementada en el destino HEYTI, pero aún no implica certificación.

```text
MIGRATED != CERTIFIED
```

---

### 13.31 `E2E_VERIFIED`

La cadena completa ha sido probada contra valores esperados y Golden Cases relevantes.

---

### 13.32 `CERTIFIED`

La Capability cumple los Gates definidos para la versión y alcance correspondiente.

---

### 13.33 Matriz Maestra — columnas mínimas

La matriz deberá contener, como mínimo:

```text
capability_id
module_reference
business_purpose
domains
logical_sources
etl_dependencies
db_dependencies
truth_requirements
runtime_path
materializer
response_contract
ui_invocation
golden_cases
open_incidents
gate_status
certification_status
notes
```

---

### 13.34 Matriz expandida

Cuando sea necesario podrá incluir:

```text
source_hash
source_period
target_period
business_key
territorial_dependency
genealogy_dependency
expected_visualization
remediation_plan
test_reference
evidence_reference
```

---

### 13.35 Regla TRACE-005 — Sin celdas críticas ambiguas

Valores como:

```text
UNKNOWN
?
MAYBE
SOME FILE
```

no deberán permanecer en una matriz declarada completa.

Deberán utilizarse estados formales:

```text
UNRESOLVED
BLOCKED
NOT_APPLICABLE
```

---

### 13.36 Regla TRACE-006 — `UNRESOLVED` es información válida

Durante auditoría, reconocer que una dependencia no está resuelta es preferible a inventar una relación.

---

### 13.37 Regla TRACE-007 — Toda dependencia debe tener estado

Cada fuente, ETL, tabla, contrato y Golden Case relevante deberá poder clasificarse.

---

### 13.38 Regla TRACE-008 — Evidencia enlazada

Las decisiones críticas de la matriz deberán poder apuntar a evidencia.

No deberán depender únicamente de comentarios narrativos.

---

### 13.39 Matriz Source → Capability

Vista derivada:

```text
SOURCE
CAPABILITY
PERIOD
DOMAIN
CERTIFICATION
```

Permitirá conocer qué capacidades se afectan si cambia una fuente.

---

### 13.40 Matriz ETL → Capability

Vista derivada:

```text
ETL
TARGET_TABLE
CAPABILITY
RISK
GOLDEN_CASE
```

---

### 13.41 Matriz DB → Capability

Vista derivada:

```text
TABLE
CAPABILITY
QUERY_PURPOSE
TEMPORAL_RULE
TRUTH_RULE
```

---

### 13.42 Matriz Capability → UI

Vista derivada:

```text
CAPABILITY
TARGET_MODULE
UI_INVOCATION
VISUAL_OUTPUT
CERTIFICATION
```

---

### 13.43 Matriz Incident → Capability

Vista derivada:

```text
INCIDENT
AFFECTED_CAPABILITY
TRUTH_IMPACT
BLOCKING
REMEDIATION_STATUS
```

---

### 13.44 Matriz Golden Case → Capability

Vista derivada:

```text
GOLDEN_CASE
CAPABILITY
LAYER_COVERAGE
LAST_RESULT
```

---

### 13.45 Regla TRACE-009 — Impact analysis obligatorio

Antes de modificar una fuente, ETL, tabla o contrato deberá consultarse la matriz para determinar sus consumidores.

---

### 13.46 Ejemplo de impacto

Si cambia:

```text
ELECTORAL_MASTER
```

la matriz deberá permitir identificar:

```text
affected_etl
affected_tables
affected_capabilities
affected_materializers
affected_ui
affected_golden_cases
```

---

### 13.47 Regla TRACE-010 — No cambiar a ciegas

Una modificación crítica no deberá comenzar mientras su impacto permanezca:

```text
UNRESOLVED
```

---

### 13.48 Certificación por ruta

Una Capability que use múltiples rutas de datos deberá certificar cada ruta crítica.

Ejemplo:

```text
describe_section
├─ territorial path
├─ electoral path
└─ socioeconomic path
```

---

### 13.49 Certificación parcial

Podrá existir:

```text
territorial_path = CERTIFIED
electoral_path = PROVISIONAL
socioeconomic_path = BLOCKED
```

La Capability global deberá representar conservadoramente esta condición.

---

### 13.50 Regla TRACE-011 — No promediar certificación

No deberá calcularse una certificación global por promedio numérico de subcomponentes.

---

### 13.51 Capability Readiness Score

Podrá existir posteriormente un score operacional para planificación.

Sin embargo, nunca deberá sustituir los estados normativos de Gate.

```text
SCORE != CERTIFICATION
```

---

### 13.52 Prioridad de auditoría

La matriz permitirá priorizar capacidades con:

- mayor impacto de usuario;
- mayor cantidad de fuentes;
- incidentes críticos;
- dependencias legacy;
- salida visual estratégica.

---

### 13.53 Prioridad de migración

La migración deberá favorecer capacidades:

```text
HIGH_VALUE
+
DATA_READY
+
LOW_UNRESOLVED_RISK
```

sin sacrificar dependencias arquitectónicas.

---

### 13.54 Dependencias compartidas

Cuando varias capacidades compartan una fuente o tabla, su certificación podrá reutilizar evidencia de la capa común, pero cada contrato de salida deberá validarse por separado.

---

### 13.55 Regla TRACE-012 — Evidencia reutilizable, certificación específica

```text
SHARED_SOURCE_CERTIFICATION
```

puede reutilizarse.

Pero:

```text
CAPABILITY_A_CERTIFIED
```

no implica:

```text
CAPABILITY_B_CERTIFIED
```

---

### 13.56 Trazabilidad de `describe_section`

La Capability ya existente `describe_section` deberá convertirse en uno de los primeros casos reales de aplicación de la Matriz Maestra.

Deberá documentarse posteriormente:

```text
provider
models
implementation
materializer
runtime path
response contract
data dependencies
Golden Cases
```

sin modificarla durante la fase documental actual.

---

### 13.57 Capabilities del Kernel

Capacidades como:

```text
health_check
system_info
version
```

podrán tener una trazabilidad de datos distinta porque no dependen necesariamente de datasets territoriales.

La matriz deberá permitir:

```text
DATA_TRUTH_GATE = NOT_APPLICABLE
```

cuando esté justificado.

---

### 13.58 Regla TRACE-013 — No forzar un modelo de datos donde no aplica

La gobernanza deberá ser rigurosa sin convertir cada Capability técnica en una Capability de inteligencia territorial.

---

### 13.59 Seis módulos objetivo

La Matriz Maestra deberá cubrir progresivamente las capacidades provenientes de:

```text
Análisis Territorial
Ganar Todo
Campo
Día D
ET-27
Socioeconómico
```

---

### 13.60 Análisis Territorial

Deberá mapear como mínimo dependencias:

```text
territorial
spatial
electoral
```

y las fuentes que alimentan sus radiografías, comparaciones y visualizaciones.

---

### 13.61 Ganar Todo

Deberá distinguir datos observados de:

```text
scenario
derived metric
strategic score
projection
```

---

### 13.62 Campo

Deberá mapear:

```text
field source
actor
location
assignment
duplicate rule
export/import path
```

---

### 13.63 Día D

Deberá mapear:

```text
casilla source
section identity
territorial resolution
status
operational output
```

incluyendo el tratamiento de secciones históricas.

---

### 13.64 ET-27

Deberá mapear estructura territorial, representación, cobertura, historia y genealogía cuando corresponda.

---

### 13.65 Socioeconómico

Deberá mapear:

```text
source
indicator
period
section
fallback behavior
```

y bloquear simulación silenciosa en respuestas certificadas.

---

### 13.66 UI redesign mapping

Cuando inicie el rediseño visual, cada control deberá registrarse contra una Capability existente o una Capability nueva explícitamente definida.

No deberá existir:

```text
UI_BUTTON_WITH_UNKNOWN_BACKEND_BEHAVIOR
```

---

### 13.67 Regla TRACE-014 — Todo botón debe tener dueño funcional

Cada acción de usuario deberá apuntar a:

```text
CAPABILITY
WORKFLOW
OR EXPLICIT UI-ONLY ACTION
```

---

### 13.68 Visual outputs

La matriz deberá distinguir:

```text
MAP
CHART
TABLE
STATISTIC
TEXT_RESPONSE
EXPORT
```

para determinar los Golden Cases y pruebas necesarias.

---

### 13.69 Exports

Toda exportación deberá mapear su origen y contrato.

Un archivo exportado no deberá convertirse en una nueva fuente autoritativa sin proceso de certificación.

---

### 13.70 LocalStorage y estado cliente

Toda dependencia V1 de:

```text
localStorage
```

deberá quedar registrada como dependencia legacy o estado cliente.

No deberá migrarse silenciosamente como si fuera persistencia oficial.

---

### 13.71 Variables globales V1

Dependencias como:

```text
AT_PATHS
AT_UNIVERSE
AT_SCOPE
```

deberán documentarse en la referencia V1 y reemplazarse posteriormente por contratos HEYTI cuando corresponda.

---

### 13.72 Regla TRACE-015 — No perder función al eliminar mecanismo legacy

Eliminar una variable, archivo o patrón legacy solo será correcto cuando la capacidad que proporcionaba haya sido reemplazada explícitamente.

---

### 13.73 Artefacto maestro

La Matriz Maestra podrá materializarse posteriormente como uno o más artefactos versionados.

Formato posible:

```text
Markdown
CSV
JSON
database metadata
```

La elección física se realizará en implementación.

---

### 13.74 Fuente de verdad de la matriz

Deberá existir una representación canónica para evitar que múltiples copias divergentes se conviertan en documentación contradictoria.

---

### 13.75 Automatización futura

Partes de la matriz podrán generarse automáticamente mediante inspección de:

- contratos;
- imports;
- registry;
- tests;
- metadata;
- DB schemas.

Sin embargo, las relaciones semánticas seguirán requiriendo certificación humana o evidencia normativa.

---

### 13.76 Regla TRACE-016 — Automatización no certifica semántica por sí sola

Un scanner puede descubrir que un archivo es referenciado.

No puede decidir por sí solo que ese archivo sea autoritativo.

---

### 13.77 Revisión antes de migración

Antes de migrar una Capability deberá revisarse su fila completa de trazabilidad.

No se autorizará una migración basada únicamente en conocer su archivo de código.

---

### 13.78 Revisión después de migración

Después de migrar deberá actualizarse:

```text
target implementation
runtime path
materializer
UI invocation
Golden Case result
certification status
```

---

### 13.79 Revisión ante cambios

Toda modificación estructural deberá preguntar:

```text
DOES THIS CHANGE THE TRACE MATRIX?
```

Si la respuesta es sí, la matriz deberá actualizarse dentro del mismo ciclo de cambio.

---

### 13.80 Invariantes de trazabilidad

#### TRACE-INV-001

```text
EVERY MIGRATED CAPABILITY HAS A TRACE
```

#### TRACE-INV-002

```text
EVERY CRITICAL UI OUTPUT HAS A CAPABILITY OWNER
```

#### TRACE-INV-003

```text
EVERY CRITICAL CAPABILITY HAS IDENTIFIED SOURCES
```

#### TRACE-INV-004

```text
EVERY CRITICAL SOURCE HAS KNOWN CONSUMERS
```

#### TRACE-INV-005

```text
EVERY CERTIFIED CAPABILITY HAS GOLDEN CASE COVERAGE
```

#### TRACE-INV-006

```text
EVERY BLOCKING INCIDENT IDENTIFIES AFFECTED CAPABILITIES
```

#### TRACE-INV-007

```text
NO LEGACY DEPENDENCY IS REMOVED BEFORE ITS FUNCTION IS MAPPED
```

---

### 13.81 No implementación física todavía

Durante la definición normativa de este capítulo:

```text
NO TRACE TABLE CREATION
NO CODE MODIFICATION
NO MODULE MIGRATION
NO UI MIGRATION
NO LEGACY CLEANUP
```

por efecto exclusivo de este capítulo.

---

### 13.82 Definition of Complete de la Matriz Maestra

La Matriz Maestra estará suficientemente completa para iniciar migración cuando todas las capacidades objetivo de la versión puedan responder:

```text
WHAT DOES IT DO?
WHAT DATA DOES IT NEED?
WHERE DOES THAT DATA COME FROM?
HOW IS IT TRANSFORMED?
WHERE IS IT STORED?
HOW IS IT ACCESSED?
HOW IS IT MATERIALIZED?
HOW WILL THE USER INVOKE IT?
WHAT CAN GO WRONG?
WHAT GOLDEN CASE PROVES IT?
IS IT READY?
```

---

### 13.83 Resultado esperado

La Matriz Maestra deberá convertir el repositorio en un sistema navegable conceptualmente:

```text
USER FUNCTION
        ↓
CAPABILITY
        ↓
CONTRACT
        ↓
DATABASE
        ↓
ETL
        ↓
SOURCE
        ↓
EVIDENCE
```

y también en sentido inverso.

---

### 13.84 Principio final

> **En HEYTI, ninguna capacidad crítica deberá ser una caja negra: deberá poder explicar qué hace, qué datos utiliza, de dónde provienen y qué evidencia demuestra que su respuesta es correcta.**

---

### 13.85 Baseline de trazabilidad

El modelo definido en este capítulo constituye:

```text
HEYTI Master Capability Traceability & Certification Matrix Model v1.0
```

Estado:

```text
NORMATIVE BASELINE
```

Será la base para construir, en la fase siguiente, la Matriz Maestra física real de los seis módulos y de las capacidades nativas de HEYTI-CORE.

---

## Fin del Capítulo 13

## Capítulo 14. Data Truth Audit Execution Protocol

### 14.1 Propósito

Este capítulo define el protocolo operativo mediante el cual HEYTI ejecutará auditorías de verdad de datos de forma repetible, documentada y certificable.

Los capítulos anteriores definieron:

```text
WHAT DATA TRUTH MEANS
HOW IT IS CLASSIFIED
HOW IT MUST BE TRANSFORMED
HOW IT MUST TRAVEL
HOW IT IS TESTED
HOW MIGRATION IS GATED
HOW IT IS PHYSICALLY MAPPED
HOW CAPABILITIES ARE TRACED
```

Este capítulo establece ahora:

```text
HOW THE AUDIT IS EXECUTED
```

---

### 14.2 Principio rector

> **Una auditoría de verdad no deberá depender de memoria, intuición o exploración improvisada; deberá seguir un protocolo reproducible que preserve evidencia y permita repetir sus conclusiones.**

---

### 14.3 Objetivo del protocolo

El protocolo deberá permitir:

1. identificar el objeto auditado;
2. resolver sus fuentes;
3. preservar evidencia;
4. medir universos y llaves;
5. reconstruir transformaciones;
6. reconciliar resultados;
7. clasificar diferencias;
8. determinar causa raíz;
9. certificar hallazgos;
10. producir decisiones de Gate;
11. generar Golden Cases;
12. alimentar la Matriz Maestra.

---

### 14.4 Unidad de auditoría

Una auditoría podrá tener como unidad:

```text
SOURCE
DATASET
ETL
TABLE
CAPABILITY
MODULE
INCIDENT
END_TO_END_PATH
```

El alcance deberá declararse antes de ejecutar pruebas.

---

### 14.5 Audit ID

Cada auditoría relevante deberá disponer de un identificador estable.

Formato recomendado:

```text
DTA-<DOMAIN>-<SUBJECT>-<NNN>
```

Ejemplos:

```text
DTA-ELECTORAL-2015-001
DTA-TERR-RESECTION-001
DTA-DIAD-CASILLAS-001
DTA-E2E-DESCRIBE-SECTION-001
```

---

### 14.6 Audit Header

Toda auditoría deberá poder registrar:

```text
audit_id
title
scope
domain
repository
branch
commit
working_tree_state
started_at
completed_at
auditor
status
```

---

### 14.7 Regla AUD-001 — Capturar baseline antes de investigar

Antes de modificar cualquier elemento deberá capturarse el estado inicial.

Como mínimo, cuando aplique:

```text
repository
branch
HEAD
working_tree
source_paths
source_hashes
DB_state
```

---

### 14.8 Working tree no limpio

Un working tree con modificaciones no deberá invalidar automáticamente una auditoría.

Pero deberá registrarse porque puede explicar diferencias entre:

```text
REMOTE_BASELINE
```

y:

```text
LOCAL_OPERATIONAL_BASELINE
```

---

### 14.9 Regla AUD-002 — No limpiar antes de comprender

Durante auditoría:

```text
NO git restore
NO git clean
NO delete
NO rename
```

únicamente para obtener un estado aparentemente limpio.

Los cambios locales pueden contener evidencia funcional o histórica.

---

### 14.10 Fase A — Scope Resolution

La primera fase deberá definir:

```text
WHAT ARE WE AUDITING?
WHY?
WHICH PERIOD?
WHICH DOMAIN?
WHICH OUTPUT?
```

---

### 14.11 Scope Contract

Ejemplo conceptual:

```text
domain = ELECTORAL
period = 2015
subject = section universe
source = official spreadsheets
target = electoral.section_result
objective = reconcile historical coverage
```

---

### 14.12 Fase B — Physical Source Resolution

Deberán localizarse físicamente todas las fuentes candidatas relevantes.

Clasificación inicial:

```text
AUTHORITATIVE_SOURCE
CERTIFIED_SOURCE
DERIVED_SOURCE
INTERMEDIATE_SOURCE
AUDIT_EVIDENCE
BACKUP_SOURCE
LEGACY_SOURCE
UNVERIFIED_SOURCE
SIMULATED_SOURCE
REJECTED_SOURCE
```

---

### 14.13 Regla AUD-003 — Encontrado no significa autorizado

```text
FILE_FOUND != AUTHORITATIVE_SOURCE
```

La auditoría deberá demostrar por qué una fuente es válida.

---

### 14.14 Source Evidence Record

Por cada fuente relevante deberá capturarse:

```text
path
logical_source_id
size
hash
record_count
schema
key
period
origin
classification
```

---

### 14.15 Fase C — Dependency Resolution

Deberán identificarse consumidores y transformaciones:

```text
SOURCE
→ SCRIPT
→ ETL
→ DB
→ CAPABILITY
```

---

### 14.16 Regla AUD-004 — Resolver dependencias con búsquedas acotadas

Las búsquedas deberán comenzar por:

- nombres de archivo;
- imports;
- rutas;
- variables;
- contratos;
- tablas;
- identificadores semánticos.

Deberán evitarse búsquedas recursivas masivas por números genéricos salvo necesidad justificada.

---

### 14.17 Búsquedas numéricas amplias

Las búsquedas de IDs como:

```text
343
1059
2788
```

pueden producir grandes cantidades de falsos positivos.

Por tanto deberán preferirse búsquedas estructuradas sobre:

```text
SECCION
section_code
business_key
```

o parsers del formato correspondiente.

---

### 14.18 Fase D — Schema Inspection

Antes de comparar valores deberán inspeccionarse:

```text
fields
types
keys
nullability
cardinality
nested_structure
```

---

### 14.19 Regla AUD-005 — No asumir nombres de llave

La auditoría deberá resolver explícitamente si una entidad usa:

```text
SECCION
seccion
section_id
section_code
```

u otra representación.

---

### 14.20 Fase E — Universe Measurement

Deberán medirse:

```text
total_records
unique_business_keys
duplicates
null_keys
period_coverage
domain_coverage
```

---

### 14.21 Universe Snapshot

Cada dataset crítico deberá poder producir un snapshot reproducible.

Ejemplo:

```text
TOTAL_ROWS
UNIQUE_SECTIONS
DUPLICATE_SECTIONS
MIN_SECTION
MAX_SECTION
```

cuando aplique.

---

### 14.22 Fase F — Source → Source Reconciliation

Cuando existan múltiples fuentes relacionadas deberán compararse antes de llegar a DB.

Ejemplos:

```text
official source
vs
master

master
vs
enriched master

V1
vs
CORE dataset
```

---

### 14.23 Hash reconciliation

Si dos archivos tienen hash idéntico:

```text
PHYSICAL_CONTENT_EQUAL = TRUE
```

Esto no implica automáticamente:

```text
SEMANTIC_ROLE_EQUAL = TRUE
```

---

### 14.24 Fase G — Transformation Reconstruction

La auditoría deberá reconstruir:

```text
INPUT
TRANSFORMATION
OUTPUT
```

incluyendo:

- joins;
- filters;
- fills;
- aggregation;
- type conversion;
- deduplication;
- temporal copy;
- reject policy.

---

### 14.25 Regla AUD-006 — Leer la transformación real

No deberá inferirse un ETL únicamente por su nombre.

Cuando sea necesario deberá inspeccionarse el código efectivo que ejecuta la transformación.

---

### 14.26 Regla para archivos `.py`

En la documentación operativa de HEYTI, toda referencia a un archivo Python auditado deberá incluir su ruta completa cuando exista riesgo de ambigüedad entre módulos o copias.

---

### 14.27 Fase H — Source → DB Reconciliation

La comparación deberá incluir:

```text
source_count
db_count
common_keys
source_only
db_only
duplicate_keys
rejected_records
```

---

### 14.28 Reconciliation Equation

Toda diferencia deberá poder satisfacer:

```text
SOURCE_TOTAL
=
LOADED
+ REJECTED
+ SKIPPED
+ DUPLICATE_RESOLUTION
+ UNRESOLVED
```

adaptada a la semántica del proceso.

---

### 14.29 Regla AUD-007 — Toda diferencia tiene destino

No deberá existir:

```text
UNEXPLAINED_DISAPPEARANCE
```

en una auditoría cerrada.

---

### 14.30 Fase I — Semantic Reconciliation

Después de reconciliar cantidades deberán compararse significados.

Ejemplos:

```text
0 official
vs
0 generated

2018 observation
vs
2024 carry-forward

historical section
vs
invalid section
```

---

### 14.31 Regla AUD-008 — Count match no cierra auditoría

```text
COUNT_MATCH != SEMANTIC_MATCH
```

---

### 14.32 Fase J — Temporal Reconciliation

Cuando existan años o periodos deberá determinarse:

```text
source_period
target_period
validity_period
territorial_universe
```

---

### 14.33 Regla AUD-009 — Año del campo no prueba origen

Un campo llamado:

```text
24G_TOTAL
```

no demuestra por sí solo que el valor haya sido observado en 2024.

---

### 14.34 Fase K — Territorial Reconciliation

Cuando existan secciones deberá verificarse:

```text
current?
historical?
predecessor?
successor?
genealogy known?
geometry available?
```

---

### 14.35 Fase L — Root Cause Analysis

Toda diferencia crítica deberá distinguir:

```text
ROOT_CAUSE
```

de:

```text
DOWNSTREAM_EFFECT
```

---

### 14.36 Ejemplo 2788

```text
ROOT_CAUSE
= absent from base master

DOWNSTREAM_EFFECT
= left merge cannot introduce section

DOWNSTREAM_EFFECT
= combined dataset omits section

DOWNSTREAM_EFFECT
= DB cannot load its official 2015 values
```

---

### 14.37 Ejemplo de las 97 casillas

```text
ROOT_CAUSE
= source references five historical predecessor sections

DOWNSTREAM_EFFECT
= current territorial FK lookup fails

DOWNSTREAM_EFFECT
= 97 records rejected
```

---

### 14.38 Fase M — Classification

Cada hallazgo deberá clasificarse mediante los ejes definidos:

```text
truth_status
territorial_status
genealogy_status
certification_status
anomaly_code
```

---

### 14.39 Fase N — Incident Registration

Las diferencias relevantes deberán convertirse en incidentes identificables cuando requieran seguimiento.

---

### 14.40 Fase O — Certification

La auditoría deberá determinar qué está certificado y qué permanece provisional o bloqueado.

---

### 14.41 Regla AUD-010 — Certificar el diagnóstico sin fingir remediación

Podrá declararse:

```text
DIAGNOSIS = CERTIFIED
REMEDIATION = PENDING
```

---

### 14.42 Fase P — Gate Decision

Los hallazgos deberán alimentar los Gates definidos en el Capítulo 11.

---

### 14.43 Fase Q — Golden Case Extraction

Todo hallazgo suficientemente estable y relevante deberá evaluarse como candidato a Golden Case.

---

### 14.44 Fase R — Trace Matrix Update

La Matriz Maestra deberá actualizarse con:

```text
source
etl
db
capability
incident
golden_case
certification
```

---

### 14.45 Fase S — Audit Closure

Una auditoría podrá cerrarse cuando:

- alcance completado;
- diferencias clasificadas;
- evidencia preservada;
- causas críticas explicadas o formalmente bloqueadas;
- incidentes registrados;
- próximos pasos definidos.

---

### 14.46 `AUDIT_CLOSED`

No significa necesariamente:

```text
SYSTEM_CORRECTED
```

---

### 14.47 Estados de auditoría

Estados recomendados:

```text
PLANNED
IN_PROGRESS
EVIDENCE_PENDING
BLOCKED
DIAGNOSIS_COMPLETE
AUDIT_CLOSED
REOPENED
```

---

### 14.48 Audit Evidence Package

Cada auditoría relevante deberá poder reunir:

```text
audit_header
commands_or_queries
source_inventory
hashes
schema_snapshot
count_snapshot
difference_ledger
root_cause
classification
incident_references
Golden_Case_candidates
gate_decision
conclusion
```

---

### 14.49 Regla AUD-011 — Preservar comandos útiles

Los comandos o consultas que producen evidencia importante deberán conservarse cuando sean reproducibles y seguros.

---

### 14.50 Regla AUD-012 — No preservar secretos

La evidencia no deberá contener:

```text
password
token
secret
private credential
```

aunque aparezca en código legacy.

---

### 14.51 SQL evidence

Las consultas SQL deberán registrar:

```text
query_purpose
target_schema
target_table
result_summary
```

y, cuando sea necesario, el SQL reproducible.

---

### 14.52 Script evidence

Los scripts temporales de auditoría deberán clasificarse como:

```text
AUDIT_EVIDENCE
```

o herramientas de auditoría, no como Runtime productivo.

---

### 14.53 Temporary artifact policy

Un artefacto temporal podrá conservarse si:

- reproduce evidencia;
- explica una conclusión;
- será útil para regresión;
- forma parte del expediente de auditoría.

De lo contrario podrá proponerse para limpieza posterior.

---

### 14.54 Regla AUD-013 — No limpiar durante investigación activa

La limpieza deberá ocurrir únicamente después de clasificación y cierre de dependencia.

---

### 14.55 Performance safety

Las auditorías deberán considerar costo operacional.

Especialmente en equipos con recursos limitados deberán preferirse:

- consultas dirigidas;
- lectura estructurada;
- filtros tempranos;
- muestras controladas;
- hashes;
- agregaciones.

---

### 14.56 Regla AUD-014 — Evitar escaneos destructivos de productividad

Una auditoría no deberá ejecutar repetidamente búsquedas masivas de bajo valor que saturen el entorno cuando exista una alternativa estructurada.

---

### 14.57 Progressive narrowing

La estrategia recomendada será:

```text
BROAD INVENTORY
→ CANDIDATE SET
→ STRUCTURED FILTER
→ TARGETED INSPECTION
→ CERTIFIED EVIDENCE
```

---

### 14.58 Sampling

El muestreo podrá utilizarse para explorar, pero no deberá sustituir una reconciliación completa cuando la conclusión dependa de totalidad.

---

### 14.59 Regla AUD-015 — Sample evidence must say sample

Toda conclusión basada únicamente en muestra deberá declararse como tal.

---

### 14.60 Negative evidence

La ausencia de coincidencia puede ser evidencia útil solo si la búsqueda fue suficientemente específica y completa.

---

### 14.61 Regla AUD-016 — No confundir "no encontrado" con "no existe"

```text
SEARCH_NOT_FOUND
!=
PROVEN_NONEXISTENCE
```

---

### 14.62 Cross-repository audit

Cuando una cadena atraviese repositorios deberá registrarse la procedencia por repositorio.

En HEYTI podrán intervenir, entre otros:

```text
AT-27-30-core
visualizacion-estrategica-27-30
historical/workspace repositories
```

---

### 14.63 Repository role

Cada repositorio deberá clasificarse conceptualmente:

```text
CURRENT_CORE
V1_OPERATIONAL_REFERENCE
BACKUP
HISTORICAL_EVIDENCE
WORKSPACE
```

según corresponda.

---

### 14.64 Remote vs local

La auditoría deberá distinguir:

```text
REMOTE_STATE
```

de:

```text
LOCAL_STATE
```

cuando el repositorio local contenga trabajo posterior no publicado.

---

### 14.65 Database audit

La base de datos deberá tratarse como materialización de procesos, no como fuente histórica absoluta.

---

### 14.66 Regla AUD-017 — DB is not automatically the truth source

```text
IN_DATABASE
!=
OBSERVED_DATA
```

---

### 14.67 Runtime audit

Cuando se audite una Capability deberá verificarse que el resultado no cambie semánticamente al atravesar Runtime.

---

### 14.68 Materialization audit

Deberá comprobarse que Materialization no convierta:

```text
UNAVAILABLE
```

en una respuesta aparentemente completa.

---

### 14.69 UI audit

La auditoría visual deberá ejecutarse contra valores certificados, no únicamente contra apariencia V1.

---

### 14.70 Controlled UI Test Run

Antes de certificar la nueva interfaz deberá ejecutarse una corrida controlada:

```text
CERTIFIED_INPUT
→ HEYTI
→ DISPLAY
→ COMPARE
```

---

### 14.71 Resultado de UI audit

Deberá comparar:

```text
EXPECTED_VALUE
DISPLAYED_VALUE
EXPECTED_TRUTH_STATUS
DISPLAYED_SEMANTICS
EXPECTED_ENTITY
DISPLAYED_ENTITY
EXPECTED_PERIOD
DISPLAYED_PERIOD
```

---

### 14.72 Auditoría por los seis módulos

El protocolo deberá aplicarse progresivamente a:

```text
Análisis Territorial
Ganar Todo
Campo
Día D
ET-27
Socioeconómico
```

---

### 14.73 Audit readiness de módulo

Un módulo estará listo para migración cuando sus capacidades requeridas tengan:

```text
TRACE
DATA AUDIT
INCIDENT CLASSIFICATION
GATE DECISION
GOLDEN CASE PLAN
```

---

### 14.74 Auditoría de fuentes antes de UI

La construcción visual no deberá adelantarse a la certificación de las fuentes necesarias para responder correctamente.

---

### 14.75 Regla AUD-018 — UI no debe ocultar deuda de datos

Si una visualización requiere un dato que aún no está certificado:

```text
BLOCK
PROVISIONAL
OR UNAVAILABLE
```

según corresponda.

---

### 14.76 Auditoría recurrente

La Data Truth Audit no será un evento único.

Deberá repetirse cuando cambien:

- fuentes;
- periodos;
- ETL;
- esquema;
- contratos;
- capacidades;
- reglas;
- UI crítica.

---

### 14.77 Trigger de reauditoría

Ejemplos:

```text
NEW ELECTION YEAR
NEW SECTION UNIVERSE
NEW OFFICIAL SOURCE
ETL CHANGE
SCHEMA MIGRATION
CAPABILITY CHANGE
MATERIALIZER CHANGE
UI FILTER CHANGE
```

---

### 14.78 Delta audit

Después de establecer una baseline certificada, futuras auditorías podrán enfocarse en cambios respecto de la baseline.

---

### 14.79 Full audit

Deberá ejecutarse nuevamente una auditoría completa cuando el cambio pueda invalidar supuestos fundamentales.

---

### 14.80 Auditoría y onboarding

El manual de incorporación deberá explicar:

```text
HOW TO RUN AN AUDIT
WHERE EVIDENCE LIVES
HOW TO CLASSIFY A FINDING
WHEN TO OPEN AN INCIDENT
HOW TO CREATE A GOLDEN CASE
WHEN A GATE BLOCKS MIGRATION
```

---

### 14.81 Checklist operativo

Antes de cerrar una auditoría deberá verificarse:

```text
[ ] scope defined
[ ] baseline captured
[ ] sources resolved
[ ] sources classified
[ ] hashes/counts captured
[ ] keys identified
[ ] transformations inspected
[ ] source→DB reconciled
[ ] semantic differences classified
[ ] temporal context resolved
[ ] territorial context resolved
[ ] root causes documented
[ ] incidents registered
[ ] Golden Case candidates identified
[ ] Gate decision recorded
[ ] trace matrix updated
[ ] evidence preserved
[ ] secrets excluded
```

---

### 14.82 Invariantes de auditoría

#### AUD-INV-001

```text
NO AUDIT CLOSURE WITH UNCLASSIFIED CRITICAL DELTA
```

#### AUD-INV-002

```text
NO SOURCE AUTHORITY BY FILENAME ALONE
```

#### AUD-INV-003

```text
NO OFFICIAL_ZERO FROM MISSING WITHOUT EVIDENCE
```

#### AUD-INV-004

```text
NO HISTORICAL INVALIDATION FROM CURRENT LOOKUP FAILURE
```

#### AUD-INV-005

```text
NO CERTIFICATION WITHOUT REPRODUCIBLE EVIDENCE
```

#### AUD-INV-006

```text
NO REMEDIATION BEFORE ROOT-CAUSE UNDERSTANDING
```

cuando la evidencia necesaria sea alcanzable.

#### AUD-INV-007

```text
NO UI CERTIFICATION WITHOUT CERTIFIED EXPECTED VALUES
```

---

### 14.83 No remediación automática

Este protocolo produce:

```text
EVIDENCE
CLASSIFICATION
CERTIFICATION
DECISION
```

No produce automáticamente:

```text
DATA MUTATION
ETL EDIT
SCHEMA CHANGE
UI CHANGE
```

---

### 14.84 Resultado esperado

Una auditoría completa deberá dejar una cadena documental:

```text
QUESTION
→ EVIDENCE
→ RECONCILIATION
→ FINDING
→ ROOT CAUSE
→ CLASSIFICATION
→ INCIDENT
→ GATE
→ GOLDEN CASE
→ TRACE MATRIX
```

---

### 14.85 Principio final

> **HEYTI deberá poder repetir no solo sus cálculos, sino también el proceso mediante el cual decidió que esos cálculos eran confiables.**

---

### 14.86 Baseline de ejecución

El modelo definido en este capítulo constituye:

```text
HEYTI Data Truth Audit Execution Protocol v1.0
```

Estado:

```text
NORMATIVE BASELINE
```

Este protocolo será utilizado para continuar la auditoría física de HEYTI-CORE y, posteriormente, para auditar cada capacidad antes y después de su migración.

---

## Fin del Capítulo 14

## Capítulo 15. Data Truth Remediation Planning & Change Control

### 15.1 Propósito

Este capítulo establece el modelo normativo para convertir hallazgos certificados de la Data Truth Audit en cambios físicos controlados dentro de HEYTI-CORE.

Hasta este punto, la gobernanza ha separado deliberadamente:

```text
DIAGNOSIS
```

de:

```text
REMEDIATION
```

El objetivo de este capítulo es definir cómo deberá planearse una corrección antes de modificar fuentes derivadas, ETL, base de datos, contratos, Capabilities, Runtime, Materialization o UI.

---

### 15.2 Principio rector

> **Una corrección de datos no deberá comenzar con “qué valor cambiamos”, sino con “qué verdad estamos restaurando, dónde se perdió y qué componentes dependen de ella”.**

---

### 15.3 Remediación no equivale a edición

Una remediación puede requerir código o modificación de datos, pero conceptualmente es:

```text
CERTIFIED_ROOT_CAUSE
+
CONTROLLED_CHANGE
+
RECONCILIATION
+
REGRESSION_PROTECTION
=
VERIFIED_REMEDIATION
```

---

### 15.4 Estados de remediación

Los estados normativos serán:

```text
NOT_REQUIRED
PENDING
PLANNED
BLOCKED
IN_PROGRESS
IMPLEMENTED
VERIFIED
DEFERRED
REJECTED
```

---

### 15.5 `PENDING`

El diagnóstico está suficientemente comprendido, pero todavía no existe un plan de cambio aprobado.

---

### 15.6 `PLANNED`

Existe un plan que identifica:

- causa raíz;
- componentes afectados;
- cambio propuesto;
- riesgos;
- validación;
- rollback;
- Golden Cases.

---

### 15.7 `BLOCKED`

La corrección no puede ejecutarse responsablemente con la evidencia disponible.

---

### 15.8 `IN_PROGRESS`

La remediación está siendo implementada dentro de un cambio controlado.

---

### 15.9 `IMPLEMENTED`

El cambio físico fue aplicado, pero todavía no ha sido verificado completamente.

---

### 15.10 `VERIFIED`

El cambio fue:

```text
IMPLEMENTED
+
RECONCILED
+
TESTED
+
GOLDEN_CASE_VALIDATED
```

---

### 15.11 `DEFERRED`

La remediación se pospone mediante decisión explícita, conservando el riesgo y la razón.

---

### 15.12 `REJECTED`

Una propuesta de remediación fue evaluada y descartada por ser incorrecta, insegura o semánticamente inválida.

---

### 15.13 Remediation ID

Cada remediación relevante deberá disponer de un identificador estable.

Formato recomendado:

```text
DTR-<DOMAIN>-<SUBJECT>-<NNN>
```

Ejemplos:

```text
DTR-ELECTORAL-2788-001
DTR-ELECTORAL-24G-001
DTR-TERR-RESECTION-001
DTR-DIAD-CASILLAS-001
```

---

### 15.14 Remediation Plan mínimo

Cada plan deberá poder registrar:

```text
remediation_id
incident_id
root_cause
truth_impact
affected_sources
affected_etl
affected_tables
affected_capabilities
affected_ui
proposed_change
expected_result
validation_plan
Golden_Cases
rollback_plan
status
```

---

### 15.15 Regla REMPLAN-001 — Una causa, una estrategia explícita

La propuesta deberá declarar exactamente qué causa pretende resolver.

No deberá utilizarse una corrección genérica para múltiples problemas semánticamente distintos sin demostrar su validez.

---

### 15.16 Regla REMPLAN-002 — Corregir en la capa adecuada

La capa de remediación deberá elegirse según la causa raíz.

Ejemplos:

```text
SOURCE MASTER OMISSION
→ integration/master layer

ETL SILENT DROP
→ ETL layer

CAPABILITY MISINTERPRETATION
→ Capability layer

UI MISLABEL
→ UI layer
```

---

### 15.17 Regla REMPLAN-003 — No corregir upstream con un parche downstream

Si el error nace antes de DB, no deberá ocultarse únicamente en Materialization o UI.

---

### 15.18 Regla REMPLAN-004 — No alterar fuente primaria oficial

Las fuentes oficiales deberán preservarse como evidencia.

La remediación deberá operar sobre:

- integración;
- transformación;
- modelo de persistencia;
- metadata;
- resolución.

---

### 15.19 Regla REMPLAN-005 — Preservar antes/después

Toda remediación crítica deberá poder demostrar:

```text
BEFORE
CHANGE
AFTER
```

---

### 15.20 Change Set

La unidad física de cambio deberá ser suficientemente pequeña para poder:

- revisar;
- probar;
- revertir;
- explicar.

---

### 15.21 Regla REMPLAN-006 — Un cambio no debe mezclar cleanup innecesario

Durante una remediación crítica deberán evitarse cambios no relacionados como:

```text
rename unrelated files
format unrelated code
delete legacy artifacts
redesign UI
```

Esto reduce el radio de incertidumbre.

---

### 15.22 Change Control Gate

Antes de implementar deberá comprobarse:

```text
ROOT_CAUSE_CERTIFIED?
TARGET_LAYER_IDENTIFIED?
DEPENDENCIES_MAPPED?
BACKUP_AVAILABLE?
ROLLBACK_DEFINED?
VALIDATION_DEFINED?
GOLDEN_CASE_DEFINED?
```

Si una respuesta crítica es negativa:

```text
BLOCK
```

---

### 15.23 Backup previo

Cuando una remediación modifique estado persistente deberá existir un respaldo adecuado y verificable.

---

### 15.24 Backup no equivale a fuente

El respaldo será mecanismo de recuperación.

No deberá convertirse automáticamente en nueva fuente autoritativa.

---

### 15.25 Rollback Plan

El rollback deberá definir:

```text
trigger
scope
restore_method
verification
known_limitations
```

---

### 15.26 Rollback y migraciones de esquema

Cuando exista cambio de esquema deberá conocerse si el rollback es:

```text
REVERSIBLE
PARTIALLY_REVERSIBLE
RESTORE_REQUIRED
```

---

### 15.27 Regla REMPLAN-007 — No prometer rollback imposible

Si un cambio destruye información o transforma datos irreversiblemente, deberá bloquearse hasta contar con una estrategia de recuperación suficiente.

---

### 15.28 Remediación de la sección 2788

Baseline certificada:

```text
official_2015_source = PRESENT
base_master = ABSENT
combined_master = ABSENT
```

Causa:

```text
MASTER_OMISSION
```

---

### 15.29 Objetivo de remediación 2788

El objetivo no será simplemente insertar una fila.

Será restaurar correctamente la identidad histórica y sus valores oficiales en la cadena gobernada.

---

### 15.30 Precondiciones 2788

Antes de implementar deberán estar definidos:

```text
historical territorial representation
business key
DB persistence strategy
source provenance
truth metadata
Capability behavior
Golden Case
```

---

### 15.31 Resultado esperado 2788

La cadena futura deberá poder responder:

```text
SECTION 2788 EXISTED IN 2015
OFFICIAL DATA IS AVAILABLE
CURRENT TERRITORIAL ABSENCE DOES NOT INVALIDATE HISTORY
```

---

### 15.32 Remediación de los cinco reseccionamientos

Baseline certificada:

```text
343  → 3290–3299
1059 → 3300–3307
1110 → 3308–3313
1634 → 3278–3283
1647 → 3284–3289
```

---

### 15.33 Objetivo de remediación territorial

Persistir posteriormente la genealogía certificada sin convertirla en redistribución electoral automática.

---

### 15.34 Prohibición

```text
PREDECESSOR_VALUE
→ COPY_TO_ALL_SUCCESSORS
```

queda prohibido sin una regla certificada independiente.

---

### 15.35 Remediación de las 97 casillas

Baseline:

```text
97 SOURCE RECORDS
→ 5 HISTORICAL PREDECESSOR SECTIONS
→ CURRENT LOOKUP FAILURE
```

---

### 15.36 Objetivo para las 97 casillas

Primero deberá preservarse:

```text
original_section_code
historical_context
source_record
resolution_status
```

La eventual asignación vigente será una decisión posterior basada en evidencia.

---

### 15.37 Remediación de `24G_*`

Baseline:

```text
3137 / 3137 comparable values
= exact copy of 18G
```

Clasificación:

```text
CARRY_FORWARD
```

---

### 15.38 Objetivo para `24G_*`

Preservar el valor sin presentarlo como observación independiente de 2024.

El modelo deberá poder declarar:

```text
source_period = 2018
target_period = 2024
truth_status = CARRY_FORWARD
```

---

### 15.39 Remediación de transformation zeros

Los valores creados por:

```text
fillna(0)
```

deberán analizarse para distinguir:

```text
OFFICIAL_ZERO
SOURCE_MISSING
TRANSFORMATION_ZERO
```

---

### 15.40 Prohibición de reemplazo masivo ingenuo

No deberá ejecutarse:

```text
UPDATE all_zero_values → NULL
```

sin reconstruir su procedencia.

---

### 15.41 Remediación socioeconómica

La diferencia entre fuente y DB deberá reconciliarse completamente antes de cualquier corrección masiva.

El fallback DEMO de V1 deberá quedar separado de las fuentes certificadas.

---

### 15.42 Remediación Campo

La validación deberá preservar la regla de duplicidad de negocio.

No deberá utilizarse:

```text
same_section = duplicate
```

como regla general.

---

### 15.43 Remediación Día D

Las casillas deberán mantener identidad operativa y territorial separables cuando el universo histórico lo requiera.

---

### 15.44 Remediación de seguridad

Las credenciales embebidas en scripts legacy deberán eliminarse durante una fase controlada.

La solución objetivo deberá utilizar configuración segura.

---

### 15.45 Regla SEC-REM-001

Nunca deberá copiarse una credencial legacy a:

- documentación;
- fixtures;
- Golden Cases;
- logs;
- artefactos de auditoría.

---

### 15.46 Change Branch / Change Boundary

Toda remediación de código deberá ejecutarse dentro de un límite de cambio claramente identificable.

La estrategia Git concreta dependerá del flujo del repositorio, pero deberá permitir revisar el delta.

---

### 15.47 Pre-change Snapshot

Antes de implementar deberán capturarse, cuando aplique:

```text
git status
git diff
relevant source hashes
DB counts
incident state
Golden Case baseline
```

---

### 15.48 Post-change Snapshot

Después de implementar deberán capturarse:

```text
git diff
DB counts
reconciliation result
test result
Golden Case result
incident state
```

---

### 15.49 Reconciliation after remediation

Toda remediación deberá volver a ejecutar las reconciliaciones afectadas.

---

### 15.50 Regla REMPLAN-008 — La corrección debe cerrar su propia ecuación

Si una remediación pretende resolver un delta de 97, el resultado deberá explicar qué ocurrió con los 97 registros.

---

### 15.51 Regression after remediation

Deberán ejecutarse:

```text
TARGETED_TESTS
+
AFFECTED_GOLDEN_CASES
+
RELEVANT_GLOBAL_REGRESSION
```

según el alcance.

---

### 15.52 Regla REMPLAN-009 — No validar solo el caso corregido

Una corrección puede resolver un incidente y romper otro dominio.

La Matriz Maestra deberá utilizarse para determinar impactos laterales.

---

### 15.53 Verification Gate

Una remediación solo alcanzará:

```text
VERIFIED
```

cuando:

```text
EXPECTED_RESULT = ACTUAL_RESULT
```

y no existan regresiones críticas conocidas causadas por el cambio.

---

### 15.54 Incident closure after remediation

El incidente podrá pasar de:

```text
DIAGNOSIS_CERTIFIED / REMEDIATION_PENDING
```

a:

```text
REMEDIATION_VERIFIED
```

solo después de verificación.

---

### 15.55 Auditoría cerrada vs remediación cerrada

Se mantiene la distinción:

```text
AUDIT_CLOSED
!=
REMEDIATION_CLOSED
```

---

### 15.56 Cambio de baseline

Si la remediación modifica legítimamente el resultado esperado, deberán actualizarse:

```text
certified baseline
Golden Cases
trace matrix
documentation
```

con evidencia.

---

### 15.57 Regla REMPLAN-010 — No borrar el baseline anterior

La nueva baseline deberá conservar la historia de la anterior.

---

### 15.58 Remediation Evidence Package

Toda remediación crítica deberá poder producir:

```text
remediation_plan
incident_reference
before_snapshot
change_diff
migration_or_update_script
after_snapshot
reconciliation
test_results
Golden_Case_results
rollback_reference
verification_result
```

---

### 15.59 Orden de implementación

La secuencia preferida será:

```text
1. PREPARE
2. BACKUP
3. IMPLEMENT ROOT-CAUSE FIX
4. RECONCILE
5. RUN TARGETED TESTS
6. RUN GOLDEN CASES
7. RUN RELEVANT REGRESSION
8. VERIFY
9. UPDATE TRACEABILITY
10. CLOSE OR REOPEN INCIDENT
```

---

### 15.60 Implementación incremental

Cuando una remediación sea grande deberá dividirse en unidades verificables.

---

### 15.61 Regla REMPLAN-011 — No Big Bang innecesario

No deberán mezclarse en una sola operación:

```text
historical model redesign
all ETL rewrites
all module migration
all UI redesign
```

si pueden certificarse incrementalmente.

---

### 15.62 Compatibilidad transitoria

Durante migración podrá ser necesario soportar temporalmente:

```text
LEGACY_CONTRACT
+
TARGET_CONTRACT
```

La coexistencia deberá tener fecha o criterio de retiro.

---

### 15.63 Transitional State

Toda compatibilidad temporal deberá clasificarse:

```text
TRANSITIONAL
```

y no convertirse accidentalmente en arquitectura permanente.

---

### 15.64 Deprecation Plan

Cuando una fuente, ETL o contrato legacy sea reemplazado deberá existir:

```text
replacement
consumer migration
verification
retirement criteria
```

---

### 15.65 Regla REMPLAN-012 — Deprecar antes de borrar

```text
ACTIVE
→ DEPRECATED
→ NO_ACTIVE_CONSUMERS
→ RETIRED
```

será preferible a eliminación directa.

---

### 15.66 Cleanup posterior

Solo después de:

```text
CLASSIFIED
RECONCILED
MIGRATED
VERIFIED
BACKED_UP
NO_ACTIVE_DEPENDENCY
```

podrá ejecutarse limpieza física.

---

### 15.67 Renombrado posterior

Los nombres legacy podrán neutralizarse durante migración controlada.

El renombrado deberá actualizar consumidores y trazabilidad dentro del mismo change set o mediante transición explícita.

---

### 15.68 Regla REMPLAN-013 — Nombre nuevo no borra procedencia

Aunque:

```text
Datos_Electoral_con_2015.json
```

evolucione conceptualmente hacia:

```text
Datos_Electoral.json
```

la metadata deberá conservar la historia de origen.

---

### 15.69 Migración de módulo después de remediación

Una Capability dependiente de un incidente crítico no deberá migrarse como certificada antes de que la remediación necesaria esté verificada o el comportamiento bloqueado explícitamente.

---

### 15.70 Excepción de migración provisional

Podrá migrarse una Capability con deuda conocida si:

```text
certification_status = PROVISIONAL
```

y la salida afectada no se presenta como certeza certificada.

---

### 15.71 Change Approval Record

Toda remediación crítica deberá poder registrar:

```text
what
why
evidence
risk
approved_scope
validation
result
```

---

### 15.72 No aprobación implícita

El hecho de que un script se ejecute correctamente no constituye aprobación de cambio.

---

### 15.73 Observabilidad post-remediation

Después de cambios relevantes deberán existir señales suficientes para detectar:

- rechazos inesperados;
- cambios de cobertura;
- pérdida de llaves;
- nuevas anomalías;
- cambios de truth status.

---

### 15.74 Thresholds

Los umbrales operativos podrán utilizarse para alertas.

Sin embargo:

```text
WITHIN_THRESHOLD
```

no deberá sustituir una regla semántica absoluta cuando corresponda.

---

### 15.75 Ejemplo

Un delta de una sola sección puede ser:

```text
CRITICAL
```

si elimina una identidad histórica legítima.

---

### 15.76 Reauditoría posterior

Una remediación estructural deberá disparar una auditoría delta o completa según su impacto.

---

### 15.77 Change Control y onboarding

El manual de incorporación deberá enseñar:

```text
DO NOT FIX DATA DIRECTLY
FIND INCIDENT
READ EVIDENCE
CHECK TRACE MATRIX
CREATE REMEDIATION PLAN
IMPLEMENT CONTROLLED CHANGE
RECONCILE
RUN GOLDEN CASES
VERIFY
```

---

### 15.78 Checklist previo a implementación

```text
[ ] incident identified
[ ] root cause certified
[ ] affected chain mapped
[ ] target layer selected
[ ] proposed change documented
[ ] backup defined
[ ] rollback defined
[ ] validation defined
[ ] Golden Cases identified
[ ] secrets protected
[ ] unrelated cleanup excluded
```

---

### 15.79 Checklist posterior

```text
[ ] change applied
[ ] diff reviewed
[ ] source/DB reconciled
[ ] targeted tests passed
[ ] Golden Cases passed
[ ] relevant regression passed
[ ] trace matrix updated
[ ] incident status updated
[ ] evidence package preserved
[ ] rollback no longer required or retained per policy
```

---

### 15.80 Invariantes de remediación

#### REM-INV-001

```text
NO CRITICAL REMEDIATION WITHOUT ROOT CAUSE
```

#### REM-INV-002

```text
NO VERIFIED STATUS WITHOUT POST-CHANGE RECONCILIATION
```

#### REM-INV-003

```text
NO CRITICAL FIX WITHOUT REGRESSION PROTECTION
```

#### REM-INV-004

```text
NO PRIMARY OFFICIAL SOURCE MUTATION
```

#### REM-INV-005

```text
NO SILENT HISTORICAL REALLOCATION
```

#### REM-INV-006

```text
NO CLEANUP MIXED INTO CRITICAL REMEDIATION WITHOUT NEED
```

#### REM-INV-007

```text
NO SECRET IN EVIDENCE
```

---

### 15.81 Estado actual

Durante la construcción de este documento:

```text
REMEDIATION EXECUTION = NOT YET AUTHORIZED
```

Los incidentes diagnosticados permanecen como baseline para la siguiente fase.

---

### 15.82 Resultado esperado

El cambio físico futuro deberá seguir:

```text
CERTIFIED INCIDENT
        ↓
REMEDIATION PLAN
        ↓
CHANGE CONTROL GATE
        ↓
BACKUP
        ↓
IMPLEMENT
        ↓
RECONCILE
        ↓
TEST
        ↓
GOLDEN CASES
        ↓
VERIFY
        ↓
UPDATE TRACEABILITY
        ↓
CLOSE / REOPEN
```

---

### 15.83 Principio final

> **En HEYTI, corregir no significará alterar un dato hasta que “se vea bien”; significará restaurar una verdad certificada mediante un cambio trazable, reversible cuando sea necesario y protegido contra regresiones.**

---

### 15.84 Baseline de remediación

El modelo definido en este capítulo constituye:

```text
HEYTI Data Truth Remediation Planning & Change Control Model v1.0
```

Estado:

```text
NORMATIVE BASELINE
```

Su aplicación física deberá comenzar únicamente después de completar y aprobar el mapa de implementación correspondiente.

---

## Fin del Capítulo 15

## Capítulo 16. Data Truth Observability, Monitoring & Drift Control

### 16.1 Propósito

Este capítulo establece el modelo normativo mediante el cual HEYTI deberá detectar, después de una certificación o remediación, cambios que puedan degradar la verdad de los datos sin producir necesariamente un error técnico visible.

La gobernanza no termina cuando una carga funciona o una Capability queda certificada.

Debe poder detectar:

```text
SOURCE DRIFT
SCHEMA DRIFT
UNIVERSE DRIFT
SEMANTIC DRIFT
TEMPORAL DRIFT
TERRITORIAL DRIFT
TRANSFORMATION DRIFT
COVERAGE DRIFT
CAPABILITY DRIFT
DISPLAY DRIFT
```

---

### 16.2 Principio rector

> **Una verdad certificada que no se vigila puede degradarse silenciosamente hasta convertirse en una respuesta incorrecta.**

---

### 16.3 Observabilidad de verdad

La observabilidad tradicional responde preguntas como:

```text
IS THE SERVICE UP?
DID THE JOB FAIL?
HOW LONG DID IT TAKE?
```

La Data Truth Observability deberá responder además:

```text
DID THE SOURCE CHANGE?
DID THE UNIVERSE CHANGE?
DID THE MEANING CHANGE?
DID COVERAGE DROP?
DID MISSING BECOME ZERO?
DID HISTORY DISAPPEAR?
DID A CARRY-FORWARD BECOME OBSERVED?
DID THE UI CHANGE THE INTERPRETATION?
```

---

### 16.4 Regla OBS-001 — Disponibilidad técnica no equivale a verdad

```text
HTTP 200
ETL SUCCESS
TEST PROCESS EXIT 0
```

no significan automáticamente:

```text
DATA_TRUTH_OK
```

---

### 16.5 Baseline observable

Toda ruta crítica certificada deberá disponer de una baseline contra la cual comparar cambios posteriores.

Podrá incluir:

```text
source_hash
schema_signature
record_count
business_key_count
coverage
truth_status_distribution
period_distribution
territorial_distribution
reject_count
Golden_Case_results
```

---

### 16.6 Tipos de drift

HEYTI deberá distinguir, como mínimo:

```text
PHYSICAL_DRIFT
SCHEMA_DRIFT
UNIVERSE_DRIFT
VALUE_DRIFT
SEMANTIC_DRIFT
TEMPORAL_DRIFT
TERRITORIAL_DRIFT
TRANSFORMATION_DRIFT
CERTIFICATION_DRIFT
PRESENTATION_DRIFT
```

---

### 16.7 Physical Drift

Ocurre cuando cambia físicamente una fuente:

```text
hash_before != hash_after
```

El cambio no será automáticamente error, pero deberá disparar evaluación cuando la fuente sea crítica.

---

### 16.8 Schema Drift

Ocurre cuando cambian:

- columnas;
- nombres;
- tipos;
- estructuras;
- nesting;
- campos obligatorios.

---

### 16.9 Universe Drift

Ocurre cuando cambia el conjunto de entidades.

Ejemplo:

```text
3266 current sections
→ new certified territorial universe
```

El cambio puede ser legítimo, pero requiere reconciliación temporal.

---

### 16.10 Value Drift

Ocurre cuando cambian valores respecto de una baseline.

No todo Value Drift es error.

Puede representar nueva información oficial.

---

### 16.11 Semantic Drift

Ocurre cuando el mismo valor comienza a interpretarse de manera distinta.

Ejemplo crítico:

```text
CARRY_FORWARD
→ OBSERVED_DATA
```

sin nueva evidencia.

---

### 16.12 Temporal Drift

Ocurre cuando:

- cambia el periodo atribuido;
- se mezcla información de periodos;
- una fuente histórica se interpreta como vigente;
- un carry-forward pierde su periodo de origen.

---

### 16.13 Territorial Drift

Ocurre cuando cambia la resolución territorial o una identidad histórica deja de encontrarse.

---

### 16.14 Transformation Drift

Ocurre cuando cambia la lógica de:

```text
join
fill
filter
aggregation
deduplication
rejection
mapping
```

---

### 16.15 Certification Drift

Ocurre cuando una fuente o ruta previamente certificada deja de cumplir las condiciones que justificaban su certificación.

---

### 16.16 Presentation Drift

Ocurre cuando los datos internos siguen siendo correctos pero la UI cambia:

- filtro;
- etiqueta;
- escala;
- periodo;
- sección;
- color;
- agregación;
- orden;

de forma que altera la interpretación.

---

### 16.17 Observability Signal

Toda señal deberá poder registrar:

```text
signal_id
domain
subject
baseline
current_value
difference
severity
evidence
timestamp
```

---

### 16.18 Severidad

Estados recomendados:

```text
INFO
LOW
MEDIUM
HIGH
CRITICAL
```

La severidad deberá considerar impacto semántico, no únicamente volumen.

---

### 16.19 Regla OBS-002 — Un registro puede ser crítico

La desaparición de una sola sección histórica legítima puede justificar:

```text
CRITICAL
```

aunque represente una fracción mínima del dataset.

---

### 16.20 Source Monitoring

Para fuentes críticas podrán vigilarse:

```text
existence
hash
size
schema
record_count
business_keys
period
```

---

### 16.21 Regla OBS-003 — Hash change triggers review, not automatic rejection

Un cambio de hash deberá significar:

```text
SOURCE_CHANGED
```

no necesariamente:

```text
SOURCE_INVALID
```

---

### 16.22 Key Monitoring

Deberán detectarse:

```text
new_keys
missing_keys
duplicate_keys
null_keys
```

---

### 16.23 Coverage Monitoring

La cobertura deberá observarse por:

```text
domain
period
territorial universe
metric
```

---

### 16.24 Truth Status Distribution

Cuando exista implementación física del Truth Contract deberá poder observarse la distribución:

```text
OBSERVED_DATA
OFFICIAL_ZERO
SOURCE_MISSING
TRANSFORMATION_ZERO
CARRY_FORWARD
DERIVED_DATA
UNAVAILABLE
```

---

### 16.25 Regla OBS-004 — Cambios de distribución requieren explicación

Ejemplo:

si:

```text
TRANSFORMATION_ZERO
```

cae abruptamente a cero después de un ETL nuevo, deberá verificarse que no haya sido reclasificado incorrectamente como `OFFICIAL_ZERO`.

---

### 16.26 Reject Monitoring

Los rechazos deberán observarse por:

```text
count
reason
entity
period
territorial_status
```

---

### 16.27 Caso de referencia — 97 casillas

La baseline auditada es:

```text
rejected = 97
explained = 97
unexplained = 0
```

Una futura carga deberá comparar su resultado contra la nueva baseline correspondiente.

---

### 16.28 Regla OBS-005 — Menos rechazos no siempre significa mejora

Si los 97 rechazos pasan a cero porque el ETL asigna automáticamente predecesores a sucesores:

```text
TECHNICAL_METRIC_IMPROVED
SEMANTIC_INTEGRITY_FAILED
```

---

### 16.29 Carry-forward Monitoring

Los valores clasificados como `CARRY_FORWARD` deberán conservar:

```text
source_period
target_period
derived_from
```

---

### 16.30 Caso de referencia — 24G

Mientras no exista nueva evidencia certificada:

```text
24G
→ CARRY_FORWARD
→ source_period 2018
```

deberá permanecer protegido por observabilidad y Golden Cases.

---

### 16.31 Historical Identity Monitoring

Las secciones históricas certificadas deberán permanecer consultables dentro de su contexto temporal.

---

### 16.32 Caso de referencia — 2788

Una alerta deberá producirse si una modificación vuelve a provocar:

```text
2788 historical 2015
→ silently absent
```

---

### 16.33 Genealogy Monitoring

Las relaciones certificadas no deberán desaparecer ni modificarse sin evidencia.

---

### 16.34 Unresolved genealogy

Las 26 secciones históricas con:

```text
genealogy_status = UNRESOLVED
```

deberán permanecer así hasta que nueva evidencia permita cambiar su estado.

---

### 16.35 Regla OBS-006 — Resolución automática inesperada es drift

Si una actualización transforma:

```text
UNRESOLVED
→ CERTIFIED_MAPPING
```

sin evidencia registrada, deberá generarse una alerta crítica.

---

### 16.36 ETL Observability

Cada ejecución crítica deberá poder producir métricas como:

```text
input_count
output_count
inserted
updated
rejected
skipped
duplicates
unresolved
duration
result
```

---

### 16.37 Semantic ETL Metrics

Además deberán observarse, cuando aplique:

```text
source_missing_count
transformation_zero_count
carry_forward_count
historical_key_count
unresolved_genealogy_count
```

---

### 16.38 Reconciliation Drift

La ecuación de reconciliación deberá poder compararse con ejecuciones anteriores.

---

### 16.39 Regla OBS-007 — Toda nueva diferencia requiere clasificación

Un delta nuevo no deberá heredarse automáticamente como aceptado porque el ETL terminó.

---

### 16.40 DB Observability

Podrán observarse:

```text
row_count
distinct_business_keys
period_coverage
orphan_relations
null_business_keys
duplicate_business_keys
```

---

### 16.41 Referential Integrity vs Historical Integrity

Una FK técnicamente válida no garantiza integridad histórica completa.

Asimismo, una FK fallida puede revelar una entidad histórica legítima.

---

### 16.42 Capability Observability

Una Capability crítica deberá poder registrar o exponer internamente:

```text
capability_id
request_context
period
data_sources
result_status
truth_summary
warning_summary
trace_id
```

sin exponer información sensible.

---

### 16.43 Runtime Observability

Runtime deberá permitir correlacionar una respuesta con:

```text
capability
execution
materialization
trace
```

---

### 16.44 Materialization Observability

Deberán detectarse pérdidas de metadata entre Runtime y respuesta.

---

### 16.45 Regla OBS-008 — Metadata loss is a data-truth event

Si:

```text
CARRY_FORWARD
```

entra al Materializer y sale como un valor sin contexto cuando ese contexto es necesario, deberá considerarse una degradación.

---

### 16.46 UI Observability

La UI podrá registrar, en entornos apropiados:

```text
capability invoked
filters
period
entity
rendered component
trace_id
```

para facilitar diagnóstico.

---

### 16.47 Privacidad y minimización

La observabilidad no deberá registrar datos personales innecesarios.

Solo deberá capturarse lo necesario para trazabilidad técnica y de verdad.

---

### 16.48 Alertas

Las alertas deberán diferenciar:

```text
TECHNICAL_ALERT
DATA_TRUTH_ALERT
SECURITY_ALERT
```

aunque puedan correlacionarse.

---

### 16.49 Data Truth Alert

Ejemplos:

```text
SOURCE_HASH_CHANGED
UNIVERSE_CHANGED
KEY_DISAPPEARED
UNEXPLAINED_REJECT
TRUTH_STATUS_CHANGED
HISTORICAL_SECTION_LOST
CARRY_FORWARD_RECLASSIFIED
SIMULATION_ACTIVATED
```

---

### 16.50 Alert fatigue

No deberán generarse alertas sin acción posible.

Cada alerta deberá tener:

```text
meaning
severity
owner
next_action
```

---

### 16.51 Threshold vs invariant

Un threshold permite tolerancia cuantitativa.

Un invariant define una condición que no debe violarse.

Ejemplo:

```text
reject_count <= threshold
```

puede ser válido en algunos procesos.

Pero:

```text
SOURCE_MISSING != OFFICIAL_ZERO
```

es un invariant.

---

### 16.52 Regla OBS-009 — Invariant violation overrides threshold

Aunque el número de casos sea pequeño:

```text
INVARIANT_FAIL
→ DATA_TRUTH_FAIL
```

---

### 16.53 Golden Cases como monitores

Algunos Golden Cases podrán ejecutarse periódicamente o después de cambios relevantes.

---

### 16.54 Continuous Regression

La ejecución automática futura podrá incluir:

```text
unit tests
contract tests
Golden Cases
reconciliation checks
```

---

### 16.55 No todos los Golden Cases deben correr siempre

La frecuencia dependerá de:

- costo;
- criticidad;
- dependencia;
- velocidad de cambio.

---

### 16.56 Event-driven checks

Podrán ejecutarse controles cuando ocurra:

```text
SOURCE_UPDATE
ETL_CHANGE
SCHEMA_CHANGE
CAPABILITY_CHANGE
UI_RELEASE
NEW_ELECTION_DATA
NEW_TERRITORIAL_UNIVERSE
```

---

### 16.57 Scheduled checks

También podrán existir revisiones periódicas para fuentes externas o procesos operativos.

---

### 16.58 Baseline version

Toda comparación deberá conocer la versión de baseline.

---

### 16.59 Regla OBS-010 — No comparar contra baseline obsoleta

Una baseline reemplazada por nueva evidencia certificada deberá versionarse y dejar de utilizarse como expectativa vigente.

---

### 16.60 Drift Review

Cuando se detecte drift deberá decidirse:

```text
EXPECTED_CHANGE
UNEXPECTED_CHANGE
INCIDENT
BASELINE_UPDATE_REQUIRED
```

---

### 16.61 Expected Change

Ejemplo:

un nuevo proceso electoral oficial puede modificar legítimamente el universo de datos.

---

### 16.62 Unexpected Change

Ejemplo:

una actualización de CSS cambia el filtro aplicado y elimina secciones de una tabla.

---

### 16.63 Incident creation

Un drift con impacto de verdad deberá abrir o actualizar un Data Truth Incident.

---

### 16.64 Baseline Update

Una baseline solo deberá actualizarse con evidencia suficiente.

---

### 16.65 Regla OBS-011 — No normalizar el error

Queda prohibido actualizar la baseline únicamente para hacer desaparecer una alerta.

---

### 16.66 Drift Ledger

Deberá poder mantenerse:

```text
drift_id
detected_at
subject
baseline
current
classification
impact
incident_id
resolution
```

---

### 16.67 Dashboard conceptual

En una fase posterior podrá existir una vista interna con:

```text
source health
coverage
reconciliation
open incidents
drift
Golden Case status
capability certification
```

---

### 16.68 Dashboard no es fuente de verdad

El dashboard será una materialización de metadata de gobernanza.

No sustituirá evidencia primaria.

---

### 16.69 Data Truth SLO conceptual

Para algunas capacidades críticas podrán definirse objetivos como:

```text
0 unexplained critical deltas
0 silent simulations
0 unclassified carry-forwards
100% critical Golden Cases passing
```

---

### 16.70 Regla OBS-012 — No convertir verdad en porcentaje vacío

Un score alto no deberá ocultar una violación crítica.

---

### 16.71 Release Monitoring

Después de una liberación relevante deberá ejecutarse una ventana de verificación para detectar drift inesperado.

---

### 16.72 Post-release checks

Podrán incluir:

```text
source coverage
DB coverage
Capability response
Golden Cases
UI certified cases
logs
warnings
```

---

### 16.73 Reopen policy

Una Capability certificada deberá poder volver a:

```text
PROVISIONAL
```

o:

```text
BLOCKED
```

si aparece evidencia que invalida su baseline.

---

### 16.74 Regla OBS-013 — Certification is revocable

```text
CERTIFIED
```

significa certificado bajo evidencia y versión conocidas, no verdad eterna.

---

### 16.75 New election cycle

Cada nuevo ciclo electoral deberá tratarse como una nueva entrada de evidencia, no como extensión automática de años anteriores.

---

### 16.76 New territorial universe

Un nuevo universo de secciones deberá disparar:

```text
temporal reconciliation
genealogy review
geometry review
historical preservation review
```

---

### 16.77 Socioeconomic source changes

Un cambio de indicadores deberá revisar:

```text
indicator identity
unit
period
coverage
comparability
```

---

### 16.78 Field data changes

Campo deberá observar:

```text
new records
duplicate-rule violations
assignment consistency
location validity
```

---

### 16.79 Día D operational monitoring

Durante operación, Día D podrá requerir mayor frecuencia de observabilidad.

Pero rapidez no deberá eliminar clasificación de incertidumbre.

---

### 16.80 Regla OBS-014 — Operational urgency does not authorize fabricated certainty

En un entorno de alta presión:

```text
UNKNOWN
```

seguirá siendo preferible a:

```text
FALSE CERTAINTY
```

---

### 16.81 ET-27 monitoring

Deberá observar cambios en:

```text
territorial structure
coverage
representation
genealogy
```

---

### 16.82 Análisis Territorial monitoring

Deberá detectar inconsistencias entre:

```text
selected period
selected section
geometry
displayed electoral data
```

---

### 16.83 Ganar Todo monitoring

Los escenarios deberán distinguir cambios en entradas observadas de cambios en reglas de cálculo.

---

### 16.84 Change attribution

Toda variación importante deberá intentar responder:

```text
DATA CHANGED?
RULE CHANGED?
CODE CHANGED?
UI CHANGED?
BASELINE CHANGED?
```

---

### 16.85 Observability evidence retention

Las métricas históricas necesarias para explicar drift deberán conservarse durante un periodo adecuado definido posteriormente.

---

### 16.86 No almacenar todo indefinidamente

La política futura deberá equilibrar:

```text
TRACEABILITY
STORAGE
PRIVACY
OPERATIONAL COST
```

---

### 16.87 Observability y onboarding

El manual de incorporación deberá explicar:

- qué señales existen;
- qué significa un drift;
- qué alertas bloquean;
- cómo revisar evidencia;
- cuándo abrir un incidente;
- cuándo actualizar una baseline.

---

### 16.88 Checklist de observabilidad

Para una ruta crítica:

```text
[ ] source baseline defined
[ ] schema baseline defined
[ ] key/universe baseline defined
[ ] reconciliation baseline defined
[ ] truth-status expectations defined
[ ] Golden Cases defined
[ ] alert conditions defined
[ ] incident path defined
[ ] baseline versioned
```

---

### 16.89 Invariantes de observabilidad

#### OBS-INV-001

```text
NO CRITICAL DRIFT WITHOUT CLASSIFICATION
```

#### OBS-INV-002

```text
NO BASELINE UPDATE JUST TO SILENCE FAILURE
```

#### OBS-INV-003

```text
NO CERTIFICATION IMMUNITY FROM NEW EVIDENCE
```

#### OBS-INV-004

```text
NO TECHNICAL SUCCESS ASSUMED AS SEMANTIC SUCCESS
```

#### OBS-INV-005

```text
NO SILENT LOSS OF HISTORICAL IDENTITY
```

#### OBS-INV-006

```text
NO SILENT CHANGE OF TRUTH_STATUS
```

#### OBS-INV-007

```text
NO SECRET OR UNNECESSARY PERSONAL DATA IN OBSERVABILITY
```

---

### 16.90 No implementación automática

Durante esta fase normativa:

```text
NO MONITORING INFRASTRUCTURE DEPLOYMENT
NO ALERT SYSTEM DEPLOYMENT
NO DB SCHEMA CHANGE
NO ETL CHANGE
NO UI TELEMETRY CHANGE
```

por efecto exclusivo de este capítulo.

---

### 16.91 Resultado esperado

El ciclo futuro deberá ser:

```text
CERTIFY
   ↓
BASELINE
   ↓
OBSERVE
   ↓
DETECT DRIFT
   ↓
CLASSIFY
   ↓
INCIDENT / EXPECTED CHANGE
   ↓
REMEDIATE OR UPDATE CERTIFIED BASELINE
   ↓
VERIFY
   ↓
OBSERVE AGAIN
```

---

### 16.92 Principio final

> **HEYTI no deberá limitarse a demostrar que una respuesta fue correcta una vez; deberá poder detectar cuándo deja de serlo.**

---

### 16.93 Baseline de observabilidad

El modelo definido en este capítulo constituye:

```text
HEYTI Data Truth Observability, Monitoring & Drift Control Model v1.0
```

Estado:

```text
NORMATIVE BASELINE
```

Este modelo cerrará el ciclo entre auditoría, certificación, remediación y vigilancia continua de la verdad de datos.

---

## Fin del Capítulo 16

## Capítulo 17. Data Truth Release Certification & Operational Acceptance

### 17.1 Propósito

Este capítulo define el mecanismo normativo mediante el cual una capacidad, ruta de datos, módulo o versión de HEYTI podrá pasar de un estado técnicamente implementado a un estado formalmente aceptado para uso operacional.

Los capítulos anteriores establecieron cómo:

```text
AUDIT
CLASSIFY
RECONCILE
TRACE
REMEDIATE
VERIFY
OBSERVE
```

Este capítulo establece ahora:

```text
WHEN HEYTI MAY DECLARE A RESULT READY FOR OPERATIONAL USE
```

---

### 17.2 Principio rector

> **Una funcionalidad no estará lista para liberarse porque abra, responda o se vea bien; estará lista cuando su comportamiento, sus datos y su verdad hayan sido aceptados bajo evidencia verificable.**

---

### 17.3 Release Certification

La certificación de liberación deberá integrar:

```text
CODE READINESS
DATA READINESS
CONTRACT READINESS
TRUTH READINESS
TEST READINESS
UI READINESS
OPERATIONAL READINESS
```

---

### 17.4 Regla REL-001 — Release no equivale a deploy

```text
DEPLOYED != RELEASE_CERTIFIED
```

Un componente puede existir físicamente en un entorno sin estar autorizado como salida certificada.

---

### 17.5 Unidad de certificación

La unidad preferida será:

```text
CAPABILITY
```

aunque también podrán certificarse:

```text
DATA_PATH
MODULE
RELEASE
```

cuando exista evidencia suficiente.

---

### 17.6 Certification Record

Cada certificación relevante deberá poder registrar:

```text
certification_id
scope
version
capabilities
data_sources
Golden_Cases
gate_results
open_incidents
known_limitations
evidence_reference
certification_status
certified_at
```

---

### 17.7 Estados de liberación

Estados recomendados:

```text
NOT_READY
BLOCKED
PROVISIONAL
READY_FOR_CONTROLLED_RELEASE
RELEASED_PROVISIONAL
CERTIFIED
SUSPENDED
REVOKED
```

---

### 17.8 `NOT_READY`

La ruta todavía no cumple los requisitos mínimos para evaluación de liberación.

---

### 17.9 `BLOCKED`

Existe una condición crítica que impide liberar responsablemente la funcionalidad.

---

### 17.10 `PROVISIONAL`

La funcionalidad puede evaluarse o utilizarse bajo limitaciones explícitas, pero no deberá presentarse como completamente certificada.

---

### 17.11 `READY_FOR_CONTROLLED_RELEASE`

Los Gates necesarios han sido superados para ejecutar una liberación controlada.

---

### 17.12 `RELEASED_PROVISIONAL`

La funcionalidad está disponible operacionalmente con limitaciones conocidas y visibles.

---

### 17.13 `CERTIFIED`

La funcionalidad ha cumplido los criterios definidos para el alcance y versión correspondientes.

---

### 17.14 `SUSPENDED`

Una certificación previamente válida queda temporalmente suspendida por nueva evidencia, drift o incidente.

---

### 17.15 `REVOKED`

La certificación deja de ser válida.

La historia de la certificación deberá conservarse.

---

### 17.16 Regla REL-002 — Certificación versionada

Una certificación siempre deberá estar asociada a:

```text
VERSION
+
EVIDENCE BASELINE
```

No deberá interpretarse como certificación eterna.

---

### 17.17 Release Gate Package

Antes de liberar una Capability crítica deberá reunirse:

```text
traceability
source certification
source→DB reconciliation
truth-status validation
ETL safety result
Capability tests
Runtime tests
Materialization tests
Golden Cases
UI controlled test
open incident review
rollback plan
observability plan
```

---

### 17.18 Regla REL-003 — Evidencia incompleta produce estado conservador

Cuando falte evidencia crítica:

```text
CERTIFIED
```

no será una opción válida.

---

### 17.19 Criterio de cero errores y cero omisiones

En HEYTI:

```text
ZERO ERRORS
ZERO OMISSIONS
```

no significará necesariamente:

```text
ZERO DELTA
```

Significará:

```text
ZERO UNEXPLAINED CRITICAL DELTA
ZERO SILENT SEMANTIC ERROR
ZERO UNCLASSIFIED CRITICAL OMISSION
```

---

### 17.20 Release Readiness Matrix

Por Capability deberá poder evaluarse:

```text
SOURCE_READY
ETL_READY
DB_READY
TRUTH_READY
CAPABILITY_READY
RUNTIME_READY
MATERIALIZATION_READY
UI_READY
GOLDEN_CASE_READY
OBSERVABILITY_READY
```

---

### 17.21 Resultado de dimensión

Cada dimensión podrá clasificarse:

```text
PASS
PASS_WITH_WARNINGS
FAIL
BLOCKED
NOT_APPLICABLE
```

---

### 17.22 Regla REL-004 — Critical FAIL dominates

Un `FAIL` crítico no deberá compensarse mediante múltiples `PASS`.

---

### 17.23 Known Limitations

Toda liberación provisional deberá registrar limitaciones conocidas.

Ejemplos:

```text
historical genealogy unresolved
data unavailable for period
carry-forward present
source pending certification
```

---

### 17.24 Regla REL-005 — Limitación conocida no debe ocultarse

Una limitación que afecte la interpretación del usuario deberá propagarse hasta la respuesta o interfaz cuando corresponda.

---

### 17.25 Certified Scope

La certificación deberá indicar exactamente qué cubre.

Ejemplo:

```text
CERTIFIED:
territorial current sections 2024

NOT CERTIFIED:
historical genealogy unresolved sections
```

---

### 17.26 Regla REL-006 — No extrapolar certificación

Certificar un periodo no certifica automáticamente otro.

Certificar una elección no certifica otra.

Certificar una Capability no certifica todo el módulo.

---

### 17.27 Controlled Release

Una liberación controlada deberá limitar:

- alcance;
- usuarios;
- datos;
- funciones;
- periodo;

cuando sea necesario para reducir riesgo.

---

### 17.28 Controlled Release Test

La liberación deberá incluir casos certificados que permitan comparar:

```text
EXPECTED
vs
ACTUAL
```

en el entorno real de destino.

---

### 17.29 Operational Acceptance

La aceptación operacional deberá confirmar que la Capability:

1. responde;
2. responde con datos correctos;
3. preserva truth status;
4. preserva temporalidad;
5. preserva identidad territorial;
6. materializa correctamente;
7. se presenta correctamente;
8. produce trazabilidad suficiente.

---

### 17.30 Regla REL-007 — Visual acceptance is semantic acceptance

Para mapas, gráficas, tablas y estadísticas, la aceptación visual deberá comprobar significado, no únicamente diseño.

---

### 17.31 Map Acceptance

Un mapa deberá validar:

```text
correct entity
correct geometry
correct period
correct metric
correct truth status
correct legend
correct filters
```

---

### 17.32 Chart Acceptance

Una gráfica deberá validar:

```text
series identity
period
aggregation
missing behavior
carry-forward behavior
labels
```

---

### 17.33 Table Acceptance

Una tabla deberá validar:

```text
row identity
column meaning
zero semantics
missing semantics
sorting
filters
```

---

### 17.34 Statistic Acceptance

Una estadística deberá validar:

```text
numerator
denominator
universe
period
rounding
truth status
```

---

### 17.35 Narrative Acceptance

Una respuesta textual deberá validar:

```text
claim
evidence
certainty
period
territorial context
```

---

### 17.36 Regla REL-008 — Lenguaje proporcional a evidencia

HEYTI no deberá afirmar como certeza lo que la evidencia solo permite expresar como:

```text
provisional
derived
historical
unavailable
unresolved
```

---

### 17.37 Release Certification de los seis módulos

La liberación deberá ocurrir progresivamente para:

```text
Análisis Territorial
Ganar Todo
Campo
Día D
ET-27
Socioeconómico
```

No será necesario certificar todos simultáneamente.

---

### 17.38 Module Certification

Un módulo podrá considerarse certificado cuando todas las Capabilities requeridas para su alcance de liberación estén:

```text
CERTIFIED
```

o exista una política explícita para componentes no aplicables.

---

### 17.39 Partial Module Release

Podrá liberarse un subconjunto de capacidades.

La UI deberá impedir o identificar claramente funciones aún no certificadas.

---

### 17.40 Regla REL-009 — No placeholders engañosos

Una función pendiente no deberá mostrar datos simulados como si fueran productivos.

---

### 17.41 Socioeconómico

El comportamiento DEMO de V1 no podrá formar parte de una liberación certificada salvo que se presente explícitamente como simulación.

---

### 17.42 Día D

La presión operacional no elimina los requisitos de verdad.

Una casilla no resuelta territorialmente deberá conservar su condición en lugar de recibir una asignación inventada.

---

### 17.43 Campo

La aceptación deberá verificar:

```text
actor
location
assignment
duplicate semantics
```

---

### 17.44 ET-27

La aceptación deberá verificar estructura, cobertura e historia territorial conforme al alcance certificado.

---

### 17.45 Ganar Todo

Los escenarios y productos derivados deberán identificarse como tales.

---

### 17.46 Análisis Territorial

Las visualizaciones deberán respetar universo, periodo y clasificación de datos.

---

### 17.47 Release Evidence Bundle

Toda liberación crítica deberá poder conservar:

```text
release_id
version
commit
configuration_reference
data_baseline
gate_results
Golden_Case_results
UI_acceptance
known_limitations
open_incidents
rollback_reference
certification_record
```

---

### 17.48 Regla REL-010 — Release reproducible

Deberá ser posible reconstruir qué código, datos y contratos produjeron una versión certificada.

---

### 17.49 Configuration

La configuración relevante deberá versionarse o identificarse sin incluir secretos.

---

### 17.50 Secrets

Los secretos deberán resolverse externamente y nunca formar parte del expediente de certificación.

---

### 17.51 Rollback readiness

Antes de una liberación crítica deberá saberse:

```text
HOW TO STOP
HOW TO REVERT
HOW TO RESTORE
HOW TO VERIFY
```

---

### 17.52 Rollback trigger

Ejemplos:

```text
critical Golden Case failure
unexplained data drift
historical identity loss
wrong period display
incorrect territorial mapping
security incident
```

---

### 17.53 Regla REL-011 — Rollback no restaura falsedad conocida

Si el estado anterior contiene una falla de verdad ya certificada, no deberá tratarse como baseline semánticamente correcta.

---

### 17.54 Post-release verification

Después de liberar deberán ejecutarse verificaciones definidas en el modelo de observabilidad.

---

### 17.55 Certification suspension

Una Capability podrá pasar:

```text
CERTIFIED
→ SUSPENDED
```

si:

- cambia una fuente;
- falla un Golden Case crítico;
- aparece nueva evidencia;
- cambia el universo territorial;
- se detecta drift semántico.

---

### 17.56 Regla REL-012 — Suspensión conservadora

Cuando exista evidencia razonable de una posible falla crítica, deberá preferirse suspender la certificación antes que mantener una certeza no demostrada.

---

### 17.57 Recertification

Después de una modificación relevante deberá ejecutarse:

```text
DELTA AUDIT
OR
FULL AUDIT
```

según impacto.

---

### 17.58 Recertification Package

Deberá incluir:

```text
changed components
affected trace paths
new evidence
regression results
Golden Cases
updated limitations
```

---

### 17.59 Certification History

Toda Capability crítica deberá poder conservar:

```text
version
status
date
evidence
reason_for_change
```

---

### 17.60 Regla REL-013 — No reescribir historia de certificación

Una certificación revocada deberá permanecer registrada como parte de la historia.

---

### 17.61 Acceptance Sign-off conceptual

La gobernanza deberá permitir identificar quién o qué proceso autorizó:

```text
TECHNICAL ACCEPTANCE
DATA TRUTH ACCEPTANCE
OPERATIONAL ACCEPTANCE
```

La implementación concreta se definirá posteriormente.

---

### 17.62 Separation of acceptance concerns

Una misma persona o proceso podrá cubrir más de un rol, pero los criterios deberán permanecer conceptualmente separados.

---

### 17.63 Technical Acceptance

Confirma:

```text
code
tests
runtime
deployment
```

---

### 17.64 Data Truth Acceptance

Confirma:

```text
sources
reconciliation
semantics
temporal integrity
territorial integrity
Golden Cases
```

---

### 17.65 Operational Acceptance

Confirma que la funcionalidad satisface el uso previsto sin introducir ambigüedad crítica.

---

### 17.66 Regla REL-014 — Technical acceptance cannot override truth failure

Una implementación técnicamente impecable deberá permanecer bloqueada si sus datos son semánticamente incorrectos.

---

### 17.67 Release Notes

Las notas de liberación deberán distinguir:

```text
NEW CAPABILITIES
DATA CHANGES
TRUTH-SEMANTIC CHANGES
KNOWN LIMITATIONS
FIXED INCIDENTS
OPEN INCIDENTS
```

---

### 17.68 User-visible disclosure

No toda incidencia interna debe mostrarse al usuario.

Pero cualquier condición que cambie la interpretación de una respuesta deberá reflejarse de forma adecuada.

---

### 17.69 Example — carry-forward

Si una visualización usa `24G_*` antes de disponer de observación independiente certificada, deberá evitar presentarlo como dato observado 2024.

---

### 17.70 Example — historical section

Una consulta histórica de 2788 deberá poder responder dentro de su periodo válido aunque no pertenezca al universo territorial vigente.

---

### 17.71 Example — unresolved genealogy

Una Capability no deberá inventar sucesor para una sección histórica cuya genealogía siga `UNRESOLVED`.

---

### 17.72 Example — unavailable data

Cuando el dato requerido no pueda certificarse:

```text
UNAVAILABLE
```

será una respuesta operacional válida.

---

### 17.73 Regla REL-015 — Incomplete truth beats fabricated completeness

Una respuesta parcial pero verdadera es preferible a una respuesta completa construida con supuestos no certificados.

---

### 17.74 Release and onboarding

El manual de incorporación deberá explicar:

```text
HOW A CAPABILITY BECOMES CERTIFIED
WHAT BLOCKS A RELEASE
WHAT PROVISIONAL MEANS
HOW CERTIFICATION CAN BE SUSPENDED
HOW TO READ RELEASE EVIDENCE
```

---

### 17.75 Release checklist

Antes de certificar:

```text
[ ] scope defined
[ ] version identified
[ ] trace complete
[ ] sources certified
[ ] reconciliations passed
[ ] truth statuses validated
[ ] temporal integrity validated
[ ] territorial integrity validated
[ ] ETL safety reviewed
[ ] Capability tests passed
[ ] Runtime tests passed
[ ] Materialization tests passed
[ ] Golden Cases passed
[ ] controlled UI test passed
[ ] critical incidents resolved or blocking policy applied
[ ] rollback ready
[ ] observability ready
[ ] known limitations documented
[ ] evidence bundle preserved
```

---

### 17.76 Release invariants

#### REL-INV-001

```text
NO CERTIFIED RELEASE WITH CRITICAL UNEXPLAINED DELTA
```

#### REL-INV-002

```text
NO CERTIFIED RELEASE WITH FAILED CRITICAL GOLDEN CASE
```

#### REL-INV-003

```text
NO CERTIFIED RELEASE WITH SILENT SIMULATION
```

#### REL-INV-004

```text
NO CERTIFIED RELEASE WITH SILENT CARRY_FORWARD AS OBSERVED
```

#### REL-INV-005

```text
NO CERTIFIED RELEASE WITH UNCONTROLLED HISTORICAL REALLOCATION
```

#### REL-INV-006

```text
NO CERTIFIED RELEASE WITHOUT TRACEABLE VERSION AND EVIDENCE
```

#### REL-INV-007

```text
NO CERTIFICATION ASSUMED PERMANENT
```

---

### 17.77 Current project state

Durante la fase actual:

```text
RELEASE CERTIFICATION EXECUTION = NOT YET AUTHORIZED
```

La finalidad es establecer la norma antes de migrar módulos y rediseñar la interfaz.

---

### 17.78 Resultado esperado

El futuro ciclo de liberación deberá seguir:

```text
IMPLEMENT
   ↓
VERIFY
   ↓
TRACE
   ↓
RUN GATES
   ↓
RUN GOLDEN CASES
   ↓
CONTROLLED UI TEST
   ↓
OPERATIONAL ACCEPTANCE
   ↓
CERTIFY
   ↓
RELEASE
   ↓
OBSERVE
   ↓
RECERTIFY WHEN REQUIRED
```

---

### 17.79 Principio final

> **HEYTI no declarará una capacidad lista porque funcione; la declarará lista cuando pueda demostrar, con evidencia trazable, que funciona con los datos correctos, bajo el significado correcto y dentro del alcance certificado.**

---

### 17.80 Baseline de certificación de liberación

El modelo definido en este capítulo constituye:

```text
HEYTI Data Truth Release Certification & Operational Acceptance Model v1.0
```

Estado:

```text
NORMATIVE BASELINE
```

Este modelo establecerá la frontera formal entre una implementación terminada y una capacidad verdaderamente aceptada para operación.

---

## Fin del Capítulo 17

## Capítulo 18. Data Truth Governance Roles, Decision Rights & Accountability

### 18.1 Propósito

Este capítulo define quién puede proponer, revisar, certificar, implementar, liberar y reabrir decisiones relacionadas con la verdad de datos en HEYTI.

Los capítulos anteriores establecieron:

```text
WHAT IS TRUE
HOW IT IS CLASSIFIED
HOW IT IS AUDITED
HOW IT IS TRACED
HOW IT IS REMEDIATED
HOW IT IS MONITORED
HOW IT IS RELEASED
```

Este capítulo establece:

```text
WHO IS ACCOUNTABLE FOR EACH DECISION
```

---

### 18.2 Principio rector

> **Una decisión crítica de datos no deberá quedar sin dueño, sin evidencia ni sin autoridad claramente identificada.**

---

### 18.3 Accountability no significa burocracia

El objetivo no es crear una estructura administrativa pesada.

El objetivo es impedir situaciones como:

```text
"I thought that file was official."
"I assumed zero meant no votes."
"I changed it because the map looked wrong."
"I copied the 2018 value because 2024 was empty."
"I deleted it because nobody seemed to use it."
```

---

### 18.4 Decision Rights

Toda decisión crítica deberá indicar quién tiene autoridad para:

```text
PROPOSE
ANALYZE
CERTIFY
IMPLEMENT
VERIFY
RELEASE
REOPEN
```

---

### 18.5 Roles conceptuales

HEYTI deberá distinguir, aunque una misma persona pueda ejercer varios:

```text
DATA OWNER
SOURCE STEWARD
DATA TRUTH AUDITOR
DOMAIN REVIEWER
IMPLEMENTER
VERIFIER
RELEASE AUTHORITY
SYSTEM OPERATOR
```

---

### 18.6 Data Owner

Responsable de la interpretación de negocio del dominio o producto de datos.

Deberá poder responder:

```text
WHAT DOES THIS DATA MEAN?
WHAT DECISION DOES IT SUPPORT?
```

---

### 18.7 Source Steward

Responsable de mantener identificada la procedencia de una fuente y su clasificación.

No implica necesariamente ser propietario del organismo que produjo la fuente.

---

### 18.8 Data Truth Auditor

Responsable de ejecutar o revisar el protocolo de auditoría y preservar evidencia.

---

### 18.9 Domain Reviewer

Responsable de validar aspectos semánticos del dominio:

```text
electoral
territorial
socioeconomic
field
election_day
```

---

### 18.10 Implementer

Responsable de ejecutar cambios físicos aprobados.

No deberá redefinir unilateralmente el significado de los datos durante la implementación.

---

### 18.11 Verifier

Responsable de comprobar que la remediación o migración produjo el resultado esperado.

---

### 18.12 Release Authority

Responsable de aceptar que una Capability o release cumple el alcance certificado.

---

### 18.13 System Operator

Responsable de operación, monitoreo y respuesta inicial ante alertas o drift.

---

### 18.14 Regla GOV-001 — Rol no equivale necesariamente a persona distinta

En equipos pequeños, una persona podrá ejercer varios roles.

Lo obligatorio es separar conceptualmente las decisiones.

---

### 18.15 Regla GOV-002 — Implementar no otorga autoridad semántica automática

El hecho de escribir el código no autoriza a decidir que:

```text
SOURCE_MISSING = OFFICIAL_ZERO
```

---

### 18.16 Regla GOV-003 — Evidencia prevalece sobre jerarquía técnica

Una decisión semántica deberá sostenerse en evidencia y reglas de gobernanza.

---

### 18.17 Decision Record

Toda decisión crítica deberá poder registrar:

```text
decision_id
subject
question
options
decision
reason
evidence
impact
authority
date
status
```

---

### 18.18 Decision ID

Formato recomendado:

```text
DTD-<DOMAIN>-<SUBJECT>-<NNN>
```

Ejemplo:

```text
DTD-ELECTORAL-24G-001
```

---

### 18.19 Tipos de decisión

Podrán existir:

```text
SOURCE_AUTHORITY_DECISION
TRUTH_CLASSIFICATION_DECISION
TEMPORAL_DECISION
TERRITORIAL_DECISION
GENEALOGY_DECISION
REMEDIATION_DECISION
MIGRATION_DECISION
RELEASE_DECISION
BASELINE_DECISION
```

---

### 18.20 Source Authority Decision

Determina si una fuente es:

```text
AUTHORITATIVE
CERTIFIED
DERIVED
LEGACY
UNVERIFIED
REJECTED
```

---

### 18.21 Truth Classification Decision

Determina estados como:

```text
OBSERVED_DATA
CARRY_FORWARD
TRANSFORMATION_ZERO
UNAVAILABLE
```

---

### 18.22 Temporal Decision

Determina cómo debe interpretarse un valor entre periodos.

---

### 18.23 Territorial Decision

Determina vigencia e identidad territorial.

---

### 18.24 Genealogy Decision

Determina relaciones predecesor/sucesor.

Una genealogía no deberá certificarse únicamente por proximidad geográfica o intuición.

---

### 18.25 Remediation Decision

Determina si un incidente debe corregirse y en qué capa.

---

### 18.26 Migration Decision

Determina si una Capability cumple Definition of Ready.

---

### 18.27 Release Decision

Determina si una Capability puede pasar a operación bajo un alcance específico.

---

### 18.28 Baseline Decision

Determina cuándo nueva evidencia justifica sustituir una baseline certificada.

---

### 18.29 Regla GOV-004 — Decisión y evidencia deben viajar juntas

No deberá existir una decisión crítica cuyo fundamento sea únicamente:

```text
"se acordó"
```

sin referencia de evidencia.

---

### 18.30 Decision Status

Estados recomendados:

```text
PROPOSED
UNDER_REVIEW
APPROVED
REJECTED
SUPERSEDED
REOPENED
```

---

### 18.31 `SUPERSEDED`

Una decisión podrá ser reemplazada por nueva evidencia.

La decisión anterior deberá conservarse históricamente.

---

### 18.32 Regla GOV-005 — Nueva evidencia puede reabrir una decisión

Ninguna decisión de Data Truth deberá considerarse inmune a evidencia posterior.

---

### 18.33 Separation of Duties conceptual

Para cambios críticos deberá existir al menos una revisión independiente de la implementación, aunque no necesariamente otra persona en todas las circunstancias.

---

### 18.34 Self-review

Cuando el equipo sea reducido y la misma persona implemente y verifique, deberá utilizar evidencia reproducible, pruebas y Golden Cases para reducir sesgo.

---

### 18.35 Regla GOV-006 — La herramienta no sustituye la responsabilidad

Git, tests, CI o una IA pueden asistir.

La responsabilidad de la decisión deberá seguir siendo identificable.

---

### 18.36 IA y gobernanza

Una herramienta de IA podrá:

- explorar;
- comparar;
- generar hipótesis;
- redactar documentación;
- proponer pruebas;
- ayudar a localizar evidencia.

No deberá convertir una inferencia no demostrada en certificación.

---

### 18.37 Regla GOV-007 — AI inference is not certified evidence by itself

Una conclusión propuesta por IA deberá apoyarse en:

```text
SOURCE
QUERY
CODE
DB RESULT
OFFICIAL DOCUMENT
REPRODUCIBLE TEST
```

según corresponda.

---

### 18.38 Human-in-the-loop

Las decisiones con impacto semántico crítico deberán conservar un punto explícito de revisión antes de:

```text
DATA MUTATION
GENEALOGY ASSIGNMENT
CERTIFIED RELEASE
```

---

### 18.39 Emergency Decision

En operación podrá existir una decisión urgente.

Deberá registrar posteriormente:

```text
what happened
temporary action
risk
evidence available
follow-up audit
```

---

### 18.40 Regla GOV-008 — Urgencia no convierte suposición en verdad

Una medida temporal deberá marcarse como temporal.

---

### 18.41 Escalation

Una decisión deberá escalar cuando:

- falta evidencia crítica;
- existe conflicto entre fuentes;
- una remediación puede destruir historia;
- un incidente afecta múltiples módulos;
- una decisión territorial requiere autoridad externa.

---

### 18.42 Conflict Resolution

Ante conflicto entre fuentes deberá evaluarse:

```text
authority
period
granularity
scope
provenance
transformation history
```

---

### 18.43 Regla GOV-009 — "Más nuevo" no gana automáticamente

La fecha de modificación de un archivo no determina su autoridad.

---

### 18.44 Regla GOV-010 — "Está en producción" no gana automáticamente

Un dato ya cargado en DB puede estar semánticamente equivocado.

---

### 18.45 Regla GOV-011 — "V1 lo muestra" no gana automáticamente

La interfaz legacy es evidencia funcional, no autoridad de Data Truth.

---

### 18.46 Data Truth Review

Antes de aprobar una decisión crítica deberá revisarse:

```text
SOURCE
TRANSFORMATION
TEMPORAL CONTEXT
TERRITORIAL CONTEXT
IMPACT
ALTERNATIVES
```

---

### 18.47 Review outcome

Podrá ser:

```text
APPROVE
APPROVE_WITH_CONDITIONS
REJECT
REQUEST_MORE_EVIDENCE
BLOCK
```

---

### 18.48 Conditional Approval

Una aprobación con condiciones deberá especificar:

```text
condition
deadline_or_gate
affected_scope
```

---

### 18.49 Ownership Matrix

La gobernanza podrá mantener:

```text
DOMAIN
DATA_OWNER
SOURCE_STEWARD
AUDITOR
IMPLEMENTER
VERIFIER
RELEASE_AUTHORITY
```

---

### 18.50 Capability Ownership

Cada Capability crítica deberá tener un dueño funcional identificable.

---

### 18.51 Source Ownership

Cada fuente activa deberá tener responsable de clasificación y seguimiento.

---

### 18.52 Incident Ownership

Todo incidente abierto deberá tener:

```text
owner
next_action
status
```

---

### 18.53 Regla GOV-012 — No incident without owner

Un incidente crítico sin responsable deberá considerarse:

```text
GOVERNANCE_FAILURE
```

---

### 18.54 Golden Case Ownership

Los Golden Cases críticos deberán tener responsable de revisar cambios de baseline.

---

### 18.55 Baseline Ownership

Una baseline no deberá cambiar únicamente porque una prueba falla después de una modificación.

---

### 18.56 Release Ownership

La liberación deberá indicar quién o qué proceso certificó el alcance.

---

### 18.57 Audit Ownership

Cada auditoría deberá identificar responsable de cierre.

---

### 18.58 Documentation Ownership

Los documentos normativos deberán tener una autoridad de mantenimiento.

---

### 18.59 Regla GOV-013 — Documentación desactualizada es riesgo operativo

Una arquitectura real que diverge de su gobernanza deberá disparar revisión documental.

---

### 18.60 Change Proposal

Toda modificación crítica podrá comenzar mediante:

```text
CHANGE PROPOSAL
```

con:

```text
problem
evidence
affected trace
proposed solution
risk
validation
```

---

### 18.61 Change Approval

La aprobación deberá revisar:

```text
root cause
scope
rollback
tests
Golden Cases
security
```

---

### 18.62 Change Verification

La verificación deberá comparar:

```text
approved_expected_result
vs
actual_result
```

---

### 18.63 Regla GOV-014 — El implementador no redefine el objetivo durante el cambio

Si aparece nueva evidencia, el cambio deberá detenerse o reabrirse formalmente.

---

### 18.64 Release Approval

La aprobación de release deberá considerar:

```text
Gate status
Golden Cases
known limitations
open incidents
observability
rollback
```

---

### 18.65 Certification Authority

La autoridad de certificación no deberá certificar más allá del alcance demostrado.

---

### 18.66 Regla GOV-015 — Certificación mínima suficiente

Cuando la evidencia solo cubra una Capability, deberá certificarse esa Capability, no todo HEYTI.

---

### 18.67 Reopen Authority

Una alerta crítica o nueva evidencia deberá poder reabrir:

```text
incident
audit
decision
certification
```

sin depender de que el autor original esté disponible.

---

### 18.68 Institutional Memory

La gobernanza deberá conservar por qué se tomaron decisiones importantes.

---

### 18.69 Caso 24G

La clasificación:

```text
24G = CARRY_FORWARD FROM 18G
```

deberá conservar:

- evidencia;
- método de comparación;
- universo comparable;
- fecha de decisión.

---

### 18.70 Caso 2788

La decisión:

```text
MASTER_OMISSION
```

deberá conservar la cadena que demuestra que la sección existe en fuentes oficiales 2015 y falta desde el master base.

---

### 18.71 Caso resecciones

Las cinco genealogías certificadas deberán conservar evidencia de sus sucesores.

---

### 18.72 Caso 97 casillas

La conclusión de que:

```text
97 / 97 rejects
```

corresponden exactamente a las cinco secciones reseccionadas deberá permanecer como evidencia institucional.

---

### 18.73 26 secciones históricas

La decisión correcta actual es:

```text
HISTORICAL_SECTION
genealogy_status = UNRESOLVED
```

No deberá cambiarse por presión de “completar” la matriz.

---

### 18.74 Regla GOV-016 — "No sabemos todavía" puede ser una decisión correcta

La gobernanza deberá permitir incertidumbre explícita.

---

### 18.75 Security Accountability

Toda exposición de credenciales deberá tener un responsable de remediación futura.

Los secretos no deberán reproducirse durante la documentación del incidente.

---

### 18.76 Data Privacy Accountability

Si futuras fuentes contienen información personal, deberá definirse quién autoriza su uso y qué minimización corresponde.

---

### 18.77 Access Rights

La futura implementación podrá distinguir permisos para:

```text
READ
AUDIT
CHANGE
CERTIFY
RELEASE
```

---

### 18.78 Regla GOV-017 — Acceso técnico no implica autoridad de cambio

Poder ejecutar SQL no significa estar autorizado para modificar verdad certificada.

---

### 18.79 Governance Audit

La propia gobernanza deberá poder auditarse.

Preguntas:

```text
Are incidents owned?
Are decisions evidenced?
Are baselines versioned?
Are certifications current?
Are unresolved items visible?
```

---

### 18.80 Governance Drift

Podrá existir cuando la práctica real deja de seguir el modelo aprobado.

---

### 18.81 Regla GOV-018 — Excepción repetida debe convertirse en decisión

Si un proceso requiere excepciones frecuentes, deberá revisarse la regla o la arquitectura.

---

### 18.82 Onboarding

El manual de incorporación deberá explicar claramente:

```text
WHO MAY CHANGE WHAT
WHO REVIEWS DATA TRUTH
HOW TO OPEN AN INCIDENT
HOW TO PROPOSE REMEDIATION
HOW TO REQUEST CERTIFICATION
HOW TO REOPEN A DECISION
```

---

### 18.83 Minimal Governance Workflow

```text
FIND
→ EVIDENCE
→ CLASSIFY
→ DECIDE
→ APPROVE
→ IMPLEMENT
→ VERIFY
→ CERTIFY
→ OBSERVE
```

---

### 18.84 Decision checklist

Antes de aprobar una decisión crítica:

```text
[ ] question defined
[ ] evidence attached
[ ] source authority reviewed
[ ] temporal context reviewed
[ ] territorial context reviewed
[ ] alternatives considered
[ ] affected capabilities identified
[ ] risks identified
[ ] authority identified
[ ] decision recorded
```

---

### 18.85 Accountability checklist

```text
[ ] source has steward
[ ] capability has owner
[ ] incident has owner
[ ] remediation has implementer
[ ] remediation has verifier
[ ] release has authority
[ ] Golden Case baseline has owner
```

---

### 18.86 Invariantes de gobernanza

#### GOV-INV-001

```text
NO CRITICAL DECISION WITHOUT EVIDENCE
```

#### GOV-INV-002

```text
NO CRITICAL INCIDENT WITHOUT OWNER
```

#### GOV-INV-003

```text
NO IMPLEMENTATION AUTHORITY ASSUMED AS SEMANTIC AUTHORITY
```

#### GOV-INV-004

```text
NO CERTIFICATION BEYOND EVIDENCE SCOPE
```

#### GOV-INV-005

```text
NO DECISION HISTORY DELETION
```

#### GOV-INV-006

```text
NO AI INFERENCE PROMOTED TO CERTIFIED FACT WITHOUT EVIDENCE
```

#### GOV-INV-007

```text
NO ACCESS RIGHT ASSUMED AS CHANGE AUTHORITY
```

---

### 18.87 No estructura organizacional impuesta todavía

Durante esta fase:

```text
NO RBAC IMPLEMENTATION
NO NEW APPROVAL SYSTEM
NO WORKFLOW ENGINE
NO DATABASE GOVERNANCE TABLE CREATION
```

por efecto exclusivo de este capítulo.

---

### 18.88 Resultado esperado

La cadena de responsabilidad futura deberá poder responder:

```text
WHO FOUND IT?
WHO VERIFIED IT?
WHO DECIDED?
WHO IMPLEMENTED?
WHO CHECKED THE CHANGE?
WHO CERTIFIED THE RELEASE?
WHO OWNS IT NOW?
```

---

### 18.89 Principio final

> **La verdad de datos necesita evidencia para ser demostrable y responsabilidad para ser sostenible.**

---

### 18.90 Baseline de accountability

El modelo definido en este capítulo constituye:

```text
HEYTI Data Truth Governance Roles, Decision Rights & Accountability Model v1.0
```

Estado:

```text
NORMATIVE BASELINE
```

Su aplicación futura permitirá que las decisiones críticas de HEYTI permanezcan trazables incluso cuando cambien desarrolladores, módulos, fuentes o periodos electorales.

---

## Fin del Capítulo 18

## Capítulo 19. Data Truth Governance Enforcement, Compliance & Exception Management

### 19.1 Propósito

Este capítulo establece cómo las reglas de Data Truth Governance deberán convertirse, progresivamente, en controles verificables dentro del ciclo de ingeniería de HEYTI.

Hasta ahora se ha definido:

```text
WHAT THE RULES ARE
HOW DATA IS AUDITED
HOW INCIDENTS ARE DIAGNOSED
HOW CHANGES ARE CONTROLLED
HOW RELEASES ARE CERTIFIED
WHO IS ACCOUNTABLE
```

Este capítulo establece:

```text
HOW HEYTI PREVENTS THOSE RULES FROM BECOMING OPTIONAL
```

---

### 19.2 Principio rector

> **Una regla crítica que depende únicamente de que alguien la recuerde todavía no es un control suficientemente maduro.**

---

### 19.3 Governance Enforcement

La aplicación de gobernanza podrá realizarse mediante:

```text
DOCUMENTED RULES
CHECKLISTS
CONTRACTS
VALIDATORS
TESTS
GATES
CI CHECKS
AUDIT QUERIES
GOLDEN CASES
RELEASE POLICIES
```

No todas deberán automatizarse inmediatamente.

---

### 19.4 Regla ENF-001 — Automatizar después de comprender

No deberá automatizarse una regla cuya semántica aún sea incierta.

```text
UNDERSTAND
→ CERTIFY RULE
→ IMPLEMENT CONTROL
```

---

### 19.5 Control Types

Los controles podrán clasificarse:

```text
PREVENTIVE
DETECTIVE
CORRECTIVE
COMPENSATING
```

---

### 19.6 Preventive Control

Busca impedir que ocurra una violación.

Ejemplo:

```text
reject unclassified truth status
```

---

### 19.7 Detective Control

Busca descubrir una violación.

Ejemplo:

```text
Golden Case detects CARRY_FORWARD shown as OBSERVED_DATA
```

---

### 19.8 Corrective Control

Define cómo restaurar un estado válido después de detectar una falla.

---

### 19.9 Compensating Control

Se utiliza temporalmente cuando el control ideal todavía no puede implementarse.

Deberá ser explícito y limitado.

---

### 19.10 Control Registry conceptual

Cada control podrá registrar:

```text
control_id
rule
type
scope
layer
implementation
severity
evidence
status
owner
```

---

### 19.11 Control ID

Formato recomendado:

```text
DTC-<DOMAIN>-<SUBJECT>-<NNN>
```

Ejemplos:

```text
DTC-CORE-MISSINGZERO-001
DTC-ELECTORAL-CARRYFORWARD-001
DTC-TERR-HISTORY-001
```

---

### 19.12 Enforcement Layers

Los controles podrán ubicarse en:

```text
SOURCE RESOLUTION
ETL
DATABASE
CAPABILITY
RUNTIME
MATERIALIZATION
UI
TEST
CI
RELEASE
```

---

### 19.13 Regla ENF-002 — Control en la capa más cercana al riesgo

Siempre que sea razonable, una violación deberá detectarse antes de llegar a capas posteriores.

---

### 19.14 Ejemplo — Missing vs Zero

Preferible:

```text
ETL preserves SOURCE_MISSING
```

antes que depender exclusivamente de que la UI descubra un cero sospechoso.

---

### 19.15 Defense in Depth

Para reglas críticas podrán existir múltiples controles.

Ejemplo:

```text
ETL classification
+
Capability contract validation
+
Golden Case
+
UI regression
```

---

### 19.16 Regla ENF-003 — Duplicación de control no significa duplicación de verdad

La semántica deberá tener una autoridad normativa única aunque existan varias verificaciones.

---

### 19.17 Contract Enforcement

Los contratos podrán validar:

```text
required metadata
allowed truth statuses
period consistency
territorial context
certification state
```

---

### 19.18 Validator Enforcement

Los validadores deberán producir errores interpretables.

No bastará:

```text
INVALID
```

cuando sea posible identificar:

```text
MISSING_SOURCE_PERIOD
UNCLASSIFIED_ZERO
UNRESOLVED_SECTION
```

---

### 19.19 Database Enforcement

Algunas reglas futuras podrán apoyarse en:

```text
constraints
foreign keys
check constraints
not-null rules
unique indexes
```

pero únicamente cuando representen correctamente la semántica.

---

### 19.20 Regla ENF-004 — No convertir una regla temporal en FK incorrecta

La integridad histórica puede requerir un modelo más rico que una referencia exclusiva al universo vigente.

---

### 19.21 ETL Enforcement

Los ETL críticos deberán poder fallar o bloquear cuando encuentren condiciones que la gobernanza clasifique como no seguras.

---

### 19.22 Fail-fast vs classify-and-continue

La política dependerá del caso.

Podrá utilizarse:

```text
FAIL_FAST
```

para corrupción crítica.

Y:

```text
CLASSIFY_AND_CONTINUE
```

cuando la diferencia sea legítima y trazable.

---

### 19.23 Regla ENF-005 — Continue no significa ignore

Todo `continue` semánticamente relevante deberá dejar evidencia.

---

### 19.24 Capability Enforcement

Una Capability no deberá materializar como certeza un dato cuyo estado lo prohíba.

---

### 19.25 Runtime Enforcement

Runtime podrá impedir respuestas incompatibles con contratos certificados.

---

### 19.26 Materialization Enforcement

Materialization deberá preservar advertencias o estados necesarios para evitar falsa certeza.

---

### 19.27 UI Enforcement

La UI deberá respetar las reglas semánticas de presentación.

No deberá reconstruir una verdad paralela.

---

### 19.28 CI Enforcement

En una fase posterior, CI podrá ejecutar:

```text
unit tests
contract tests
Golden Cases
schema checks
traceability checks
```

---

### 19.29 Regla ENF-006 — CI verde no equivale a Data Truth certificada

CI es evidencia, no autoridad total.

---

### 19.30 Pre-commit / local checks

Algunos controles ligeros podrán ejecutarse antes del commit.

No deberán hacer inviable el desarrollo cotidiano.

---

### 19.31 Pull Request / Change Review

Los cambios críticos deberán responder:

```text
Does this change affect data truth?
Does it change a source?
Does it change an ETL?
Does it change temporal logic?
Does it change territorial resolution?
Does it change presentation semantics?
```

---

### 19.32 Data Truth Impact Flag

Cada cambio podrá clasificarse:

```text
NO_DATA_TRUTH_IMPACT
LOW
MEDIUM
HIGH
CRITICAL
```

---

### 19.33 Regla ENF-007 — Autor del cambio declara impacto; revisión puede elevarlo

Una clasificación inicial no deberá impedir que la revisión detecte mayor riesgo.

---

### 19.34 Mandatory Evidence by Impact

A mayor impacto deberán aumentar los requisitos de evidencia.

Ejemplo conceptual:

```text
LOW
→ targeted tests

HIGH
→ reconciliation + Golden Cases

CRITICAL
→ audit evidence + remediation plan + rollback + E2E certification
```

---

### 19.35 Compliance

Cumplimiento significa que una ruta respeta las reglas aplicables de este documento.

---

### 19.36 Compliance Status

Estados recomendados:

```text
COMPLIANT
COMPLIANT_WITH_EXCEPTIONS
NON_COMPLIANT
NOT_ASSESSED
NOT_APPLICABLE
```

---

### 19.37 Regla ENF-008 — Not assessed no equivale a compliant

La ausencia de evidencia de falla no demuestra cumplimiento.

---

### 19.38 Compliance Evidence

Podrá incluir:

```text
test
audit
query
Golden Case
contract validation
review record
release gate
```

---

### 19.39 Compliance Matrix

Podrá construirse una matriz:

```text
RULE
CONTROL
LAYER
CAPABILITY
EVIDENCE
STATUS
OWNER
```

---

### 19.40 Rule Coverage

Cada regla crítica deberá eventualmente tener al menos un mecanismo de verificación.

---

### 19.41 Regla ENF-009 — Critical rule without control is governance debt

Deberá registrarse como deuda explícita.

---

### 19.42 Governance Debt

Tipos:

```text
UNIMPLEMENTED_CONTROL
MANUAL_ONLY_CONTROL
UNTESTED_RULE
UNOWNED_CONTROL
LEGACY_EXCEPTION
```

---

### 19.43 Governance Debt no equivale a defecto inmediato

Puede existir deuda aceptable temporalmente.

Debe ser visible.

---

### 19.44 Exception Management

Una excepción permite operar temporalmente fuera de una regla bajo condiciones controladas.

---

### 19.45 Regla ENF-010 — Excepción no es permiso permanente

Toda excepción deberá tener:

```text
reason
scope
risk
owner
compensating_control
review_condition
```

---

### 19.46 Exception ID

Formato recomendado:

```text
DTE-<DOMAIN>-<SUBJECT>-<NNN>
```

---

### 19.47 Exception Status

```text
PROPOSED
APPROVED
ACTIVE
EXPIRED
REVOKED
CLOSED
```

---

### 19.48 Exception Scope

Deberá ser mínima.

Ejemplo:

```text
one capability
one period
one dataset
one release
```

---

### 19.49 Regla ENF-011 — No global exception for local problem

Un problema de una Capability no deberá desactivar controles de todo HEYTI.

---

### 19.50 Compensating Control

Toda excepción crítica deberá definir cómo se reduce el riesgo mientras permanezca activa.

---

### 19.51 Example — unresolved genealogy

Una Capability histórica podrá operar con:

```text
genealogy_status = UNRESOLVED
```

si bloquea cualquier reasignación no certificada.

Esto no requiere inventar una genealogía para cumplir.

---

### 19.52 Example — unavailable data

La ausencia certificada podrá manejarse mostrando:

```text
UNAVAILABLE
```

en lugar de crear una excepción para simular información.

---

### 19.53 Regla ENF-012 — Truthful unavailability is preferable to exception abuse

---

### 19.54 Exception Expiration

Toda excepción deberá revisarse cuando:

```text
new evidence arrives
source changes
release changes
remediation completes
```

---

### 19.55 No silent waiver

Una prueba deshabilitada, un warning ignorado o un control comentado deberá tratarse como una excepción explícita si afecta Data Truth.

---

### 19.56 Regla ENF-013 — Disabled critical test requires explanation

---

### 19.57 Suppression

La supresión de una alerta deberá registrar:

```text
why
who
scope
duration
```

---

### 19.58 Regla ENF-014 — Alert suppression does not resolve incident

---

### 19.59 Legacy Compliance

Los componentes V1 podrán clasificarse:

```text
LEGACY_REFERENCE
```

sin exigirles retroactivamente todos los controles nuevos.

Pero su comportamiento deberá entenderse antes de migrarlo.

---

### 19.60 Migration Compliance

Toda Capability migrada deberá cumplir los controles objetivo aplicables.

---

### 19.61 Regla ENF-015 — Legacy behavior is not grandfathered truth

Que una conducta exista desde V1 no la convierte en aceptable para HEYTI-CORE.

---

### 19.62 Source Compliance

Una fuente activa deberá cumplir al menos:

```text
identified
classified
traceable
period-known
key-known
certification-known
```

---

### 19.63 ETL Compliance

Un ETL crítico deberá cumplir:

```text
input contract
explicit transformation
reject accounting
output reconciliation
traceability
```

---

### 19.64 DB Compliance

La persistencia deberá permitir reconstruir suficiente contexto de verdad para los productos que dependan de ella.

---

### 19.65 Capability Compliance

La Capability deberá respetar:

```text
truth contract
temporal contract
territorial contract
certification policy
```

---

### 19.66 Runtime Compliance

Runtime no deberá eliminar contexto crítico requerido downstream.

---

### 19.67 Materialization Compliance

Materialization no deberá convertir incertidumbre en certeza.

---

### 19.68 UI Compliance

La interfaz deberá presentar el alcance y significado correctos.

---

### 19.69 Golden Case Compliance

Los Golden Cases críticos deberán permanecer:

```text
PASS
```

para el alcance certificado.

---

### 19.70 Release Compliance

Una release deberá cumplir los Gates aplicables.

---

### 19.71 Compliance Audit

Podrá realizarse periódicamente o antes de una release crítica.

---

### 19.72 Audit Questions

```text
Are critical rules controlled?
Are exceptions visible?
Are disabled tests justified?
Are incidents owned?
Are Golden Cases current?
Are certifications versioned?
```

---

### 19.73 Non-compliance

Una violación deberá clasificarse por impacto.

---

### 19.74 Non-compliance Response

Podrá resultar en:

```text
WARNING
REMEDIATION_REQUIRED
MIGRATION_BLOCKED
RELEASE_BLOCKED
CERTIFICATION_SUSPENDED
```

---

### 19.75 Regla ENF-016 — Critical semantic non-compliance blocks certification

---

### 19.76 Enforcement of known hard rules

Las siguientes reglas deberán tener controles explícitos antes de la certificación completa:

```text
H-001 SOURCE_MISSING != OFFICIAL_ZERO
H-002 TRANSFORMATION DOES NOT CREATE TRUTH
H-003 TERRITORIAL IDENTITY IS TEMPORAL
H-004 RESECTION DOES NOT AUTHORIZE REDISTRIBUTION
H-005 PROVENANCE MUST SURVIVE THE RESPONSE CHAIN
```

---

### 19.77 Control candidate — H-001

Podrá verificarse mediante:

```text
ETL test
truth-status validator
Golden Case
```

---

### 19.78 Control candidate — H-002

Podrá verificar que:

```text
fillna
copy
merge
```

no eleven automáticamente el estado a `OBSERVED_DATA`.

---

### 19.79 Control candidate — H-003

Deberá incluir casos históricos fuera del universo vigente.

---

### 19.80 Control candidate — H-004

Deberá fallar ante redistribución automática no certificada.

---

### 19.81 Control candidate — H-005

Deberá comprobar continuidad de metadata entre:

```text
DB
Capability
Runtime
Materialization
UI
```

---

### 19.82 Known baseline controls

Casos prioritarios:

```text
24G carry-forward
2788 master omission
5 resection predecessors
36 successors
97 casilla rejects
26 unresolved historical sections
transformation zeros
socioeconomic simulation risk
```

---

### 19.83 Rule Versioning

Las reglas deberán versionarse cuando cambie su significado.

---

### 19.84 Regla ENF-017 — Test version follows rule version

Si cambia una regla, sus controles y Golden Cases deberán revisarse.

---

### 19.85 Policy-as-Code

En una fase madura, algunas reglas podrán expresarse como código.

Pero:

```text
POLICY_AS_CODE
```

no deberá reemplazar la documentación semántica.

---

### 19.86 Regla ENF-018 — Code enforces; governance explains

---

### 19.87 Enforcement Failure

Si un control falla deberá distinguirse:

```text
DATA FAILURE
CONTROL FAILURE
INFRASTRUCTURE FAILURE
```

---

### 19.88 Example

Si un Golden Case no puede ejecutarse por falla del runner:

```text
CONTROL_FAILURE
```

No deberá declararse automáticamente que el dato es incorrecto ni correcto.

---

### 19.89 Bypass

Un bypass crítico deberá requerir autorización explícita y evidencia.

---

### 19.90 Regla ENF-019 — No hidden bypass

---

### 19.91 Emergency bypass

Solo deberá utilizarse para continuidad operacional justificada.

Después deberá abrirse revisión.

---

### 19.92 Enforcement Metrics

En una fase posterior podrán observarse:

```text
critical_rules_with_controls
open_exceptions
expired_exceptions
disabled_critical_tests
non_compliant_capabilities
```

---

### 19.93 Regla ENF-020 — Metrics do not replace review

Los indicadores ayudan a localizar riesgo; no certifican semántica por sí mismos.

---

### 19.94 Developer Experience

Los controles deberán ofrecer mensajes útiles.

Un desarrollador deberá poder entender:

```text
WHAT FAILED
WHY IT MATTERS
WHAT EVIDENCE IS NEEDED
```

---

### 19.95 Onboarding Enforcement

El manual de incorporación deberá enseñar que las reglas no son recomendaciones opcionales.

---

### 19.96 Pre-migration compliance checklist

```text
[ ] source controls identified
[ ] ETL controls identified
[ ] truth contract controls identified
[ ] temporal controls identified
[ ] territorial controls identified
[ ] Golden Cases identified
[ ] exceptions identified
[ ] blocking non-compliance resolved
```

---

### 19.97 Pre-release compliance checklist

```text
[ ] critical rules compliant
[ ] critical Golden Cases pass
[ ] no hidden bypass
[ ] no expired critical exception
[ ] open exceptions documented
[ ] compensating controls active
[ ] certification scope matches evidence
```

---

### 19.98 Invariantes de enforcement

#### ENF-INV-001

```text
NO CRITICAL RULE TREATED AS OPTIONAL
```

#### ENF-INV-002

```text
NO SILENT EXCEPTION
```

#### ENF-INV-003

```text
NO DISABLED CRITICAL CONTROL WITHOUT RECORD
```

#### ENF-INV-004

```text
NO EXCEPTION PROMOTED TO PERMANENT ARCHITECTURE BY ACCIDENT
```

#### ENF-INV-005

```text
NO CRITICAL NON-COMPLIANCE WITH CERTIFIED STATUS
```

#### ENF-INV-006

```text
NO POLICY-AS-CODE WITHOUT NORMATIVE MEANING
```

#### ENF-INV-007

```text
NO AUTOMATION OF UNCERTIFIED SEMANTIC ASSUMPTION
```

---

### 19.99 Estado actual

Durante la fase normativa actual:

```text
NO CI GOVERNANCE ENFORCEMENT DEPLOYMENT
NO NEW DB CONSTRAINTS
NO AUTOMATIC BLOCKING RULES
NO POLICY-AS-CODE IMPLEMENTATION
```

por efecto exclusivo de este capítulo.

Primero se terminará la gobernanza y el mapa físico de aplicación.

---

### 19.100 Resultado esperado

La evolución deberá seguir:

```text
NORMATIVE RULE
     ↓
CONTROL DESIGN
     ↓
CONTROL IMPLEMENTATION
     ↓
EVIDENCE
     ↓
COMPLIANCE CHECK
     ↓
PASS / EXCEPTION / BLOCK
     ↓
CERTIFICATION
```

---

### 19.101 Principio final

> **La gobernanza de HEYTI estará madura cuando sus reglas críticas no dependan solamente de memoria o disciplina individual, sino de controles trazables que ayuden a impedir, detectar y corregir violaciones sin ocultar excepciones.**

---

### 19.102 Baseline de enforcement

El modelo definido en este capítulo constituye:

```text
HEYTI Data Truth Governance Enforcement, Compliance & Exception Management Model v1.0
```

Estado:

```text
NORMATIVE BASELINE
```

Este modelo prepara el tránsito futuro desde una gobernanza documentada hacia una gobernanza verificable y progresivamente automatizable.

---

## Fin del Capítulo 19

## Capítulo 20. Governance Lifecycle, Versioning, Institutional Memory & Normative Closure

### 20.1 Propósito

Este capítulo cierra la baseline normativa de **HEYTI Data Truth Governance v1.0** y establece cómo deberá evolucionar sin perder decisiones, evidencia, trazabilidad ni contexto histórico.

Los capítulos anteriores definieron la verdad, clasificación, procedencia, reconciliación, temporalidad, genealogía, seguridad ETL, preservación end-to-end, Golden Cases, Gates, trazabilidad, auditoría, remediación, observabilidad, certificación, accountability y enforcement.

Este capítulo responde:

```text
HOW DOES THIS GOVERNANCE EVOLVE WITHOUT LOSING ITS MEMORY?
```

### 20.2 Principio rector

> **HEYTI deberá poder evolucionar sin reescribir la historia de por qué sus datos, reglas y decisiones llegaron a ser considerados válidos.**

### 20.3 Gobernanza como sistema vivo

La gobernanza deberá evolucionar cuando cambien fuentes, periodos electorales, universos territoriales, arquitectura, contratos, Capabilities, requisitos operativos o evidencia disponible.

### 20.4 Versioning

La gobernanza utilizará versionado explícito. Los cambios menores podrán aclarar o ampliar controles; los cambios mayores corresponderán a modificaciones incompatibles de taxonomía, contratos de verdad, modelo temporal o certificación.

### 20.5 Normative Change Record

Todo cambio relevante deberá registrar:

```text
version
date
changed_sections
reason
evidence
impact
migration_required
```

### 20.6 Historia normativa

Una regla reemplazada deberá conservarse como `SUPERSEDED`; una regla en retiro podrá marcarse `DEPRECATED`. Ninguna regla histórica necesaria para explicar decisiones pasadas deberá borrarse.

### 20.7 Institutional Memory

La memoria institucional deberá preservar:

```text
WHY
WHAT
WHEN
EVIDENCE
DECISION
IMPACT
```

Podrá residir en documentos de gobernanza, ADR, artefactos de auditoría, incidentes, Golden Cases, matrices de trazabilidad, evidencias de remediación, certificaciones y Git.

### 20.8 Chat no es repositorio normativo final

Las conversaciones podrán ayudar a construir decisiones, pero la baseline deberá residir en artefactos versionados del proyecto.

### 20.9 Documento canónico

El objetivo será:

```text
D:\GitHub\AT-27-30-core\docs\architecture\data\HEYTI_Data_Truth_Governance_v1.0.md
```

Deberá existir una sola baseline canónica por versión.

### 20.10 Normalización de taxonomía

La implementación futura deberá mantener separados:

```text
truth_status
territorial_status
genealogy_status
certification_status
anomaly_code
```

Los ejes ortogonales no deberán colapsarse. Por ejemplo, `MASTER_OMISSION` es una anomalía, no un `territorial_status`.

### 20.11 Normative Errata

Si se detecta una inconsistencia documental deberá corregirse explícitamente mediante errata o nueva versión; no se modificará silenciosamente contenido ya aprobado.

### 20.12 Data Truth Dictionary

La gobernanza mantendrá términos canónicos como:

```text
OBSERVED_DATA
OFFICIAL_ZERO
SOURCE_MISSING
TRANSFORMATION_ZERO
CARRY_FORWARD
DERIVED_DATA
UNAVAILABLE
CURRENT_SECTION
HISTORICAL_SECTION
RESECTION_PREDECESSOR
RESECTION_SUCCESSOR
CERTIFIED_MAPPING
UNRESOLVED
CERTIFIED
PROVISIONAL
REJECTED
```

Un término deberá conservar un significado normativo estable.

### 20.13 Admisión de nuevas fuentes, periodos y dominios

Un nuevo dominio deberá pasar por clasificación, modelo de verdad, temporalidad, llaves, trazabilidad, auditoría, Golden Cases y Gates.

Una nueva fuente crítica deberá seguir:

```text
IDENTIFY → CLASSIFY → PROFILE → RECONCILE → CERTIFY → REGISTER
```

Un nuevo periodo electoral no heredará automáticamente la semántica del periodo anterior.

> **Nuevo año no significa copy-forward autorizado.**

### 20.14 Nuevo universo territorial

Todo nuevo universo deberá activar comparación de universos, preservación histórica, análisis genealógico, reconciliación geométrica, análisis de impacto y revisión de Golden Cases.

### 20.15 Nueva Capability y nueva UI

Una nueva Capability deberá tener `capability_id`, propósito, dependencias, Truth Contract, trazabilidad, pruebas, Golden Cases y Gates según criticidad.

Una nueva pantalla deberá responder:

```text
WHAT CAPABILITY DOES THIS INVOKE?
WHAT DATA DOES IT REPRESENT?
WHAT TRUTH STATES CAN IT DISPLAY?
```

La evolución de UI no redefinirá Data Truth.

### 20.16 Retirement Lifecycle

Los artefactos podrán seguir:

```text
ACTIVE → DEPRECATED → NO_ACTIVE_CONSUMERS → RETIRED → ARCHIVED
```

El retiro requerirá prueba de no dependencia. Un artefacto retirado podrá seguir siendo evidencia histórica.

### 20.17 Governance Review

La gobernanza deberá revisarse ante nuevos ciclos electorales, cambios territoriales, migraciones mayores, incidentes críticos o cambios fundamentales de arquitectura.

### 20.18 Normative Drift

Existe cuando:

```text
DOCUMENTED GOVERNANCE != ACTUAL SYSTEM BEHAVIOR
```

El drift normativo deberá considerarse candidato a incidente.

### 20.19 Onboarding Lifecycle

El manual objetivo será:

```text
D:\GitHub\AT-27-30-core\docs\onboarding\HEYTI_Developer_Onboarding_Manual_v1.0.md
```

Orden mínimo de estudio:

```text
1. Governance
2. Architecture
3. Data Sources
4. ETL
5. Database
6. Capabilities
7. Runtime
8. Materialization
9. Modules
10. UI
11. Tests / Golden Cases
```

Ningún nuevo desarrollador deberá comenzar modificando ETL crítico sin contexto.

### 20.20 Institutional Handover

HEYTI deberá poder transferirse a otro desarrollador sin depender exclusivamente de memoria personal.

> **Knowledge that exists only in one person's memory is project risk.**

### 20.21 Feedback loops

Todo incidente crítico corregido deberá evaluarse como candidato a Golden Case y deberá preguntar si un control pudo prevenirlo o detectarlo antes.

> **Un incidente debe dejar al sistema más difícil de romper de la misma manera.**

### 20.22 Governance Closure Criteria v1.0

La baseline podrá considerarse normativamente cerrada cuando estén definidos:

```text
core principles
taxonomy
source governance
reconciliation
temporal model
ETL safety
end-to-end preservation
Golden Cases
migration gates
physical mapping
traceability
audit protocol
remediation
observability
release certification
accountability
enforcement
lifecycle
```

### 20.23 Significado de Normative Closure

`NORMATIVE CLOSURE` no significa implementación terminada.

Significa:

```text
THE RULES REQUIRED TO IMPLEMENT SAFELY ARE NOW DEFINED
```

El cierre normativo no autoriza mutación física automática.

### 20.24 Frontera de la siguiente fase

Después de aprobar este capítulo, la siguiente fase deberá concentrarse en:

```text
PHYSICAL IMPLEMENTATION MAPPING
+
CONTROLLED DATA REMEDIATION PLANNING
+
CAPABILITY MIGRATION READINESS
```

antes de iniciar cambios destructivos.

### 20.25 Auditoría end-to-end pendiente

La gobernanza deberá aplicarse a los dominios pendientes y a la cadena:

```text
SOURCE → DB → CAPABILITY → RUNTIME → MATERIALIZATION → UI
```

Documento aprobado no sustituye auditoría ejecutada.

### 20.26 Frontera UI

Antes de certificar la nueva interfaz HEYTI deberán existir:

```text
CERTIFIED EXPECTED VALUES
CONTROLLED UI TESTS
GOLDEN CASES
END-TO-END TRACEABILITY
```

### 20.27 Frontera de migración y cleanup

Antes de migrar una Capability crítica deberán resolverse sus Gates aplicables.

No deberá ejecutarse limpieza legacy hasta demostrar:

```text
CLASSIFIED
RECONCILED
MIGRATED
VERIFIED
NO ACTIVE CONSUMERS
BACKUP AVAILABLE
```

Los renombrados de fuentes ocurrirán únicamente durante migración controlada.

### 20.28 Baseline audit facts

La v1.0 reconoce como hechos diagnosticados:

```text
24G_* = CARRY_FORWARD FROM 18G_* FOR 3137/3137 COMPARABLE RECORDS

SECTION 2788 = VALID OFFICIAL 2015 SECTION + MASTER_OMISSION

343, 1059, 1110, 1634, 1647 = RESECTION_PREDECESSORS

3278–3313 = 36 CERTIFIED SUCCESSORS

97 CASILLA REJECTS = EXACTLY EXPLAINED BY THE FIVE RESECTION PREDECESSORS

26 OTHER HISTORICAL SECTIONS = GENEALOGY UNRESOLVED

FILLNA-GENERATED ZEROS != OFFICIAL_ZERO

SILENT SIMULATION != CERTIFIED DATA
```

Estos hechos permanecerán hasta ser reemplazados por nueva evidencia certificada.

### 20.29 Core Hard Rules

```text
H-001 — SOURCE_MISSING != OFFICIAL_ZERO
H-002 — A TRANSFORMATION CANNOT CREATE TRUTH
H-003 — TERRITORIAL IDENTITY IS TEMPORAL
H-004 — RESECTION DOES NOT AUTHORIZE AUTOMATIC REDISTRIBUTION
H-005 — PROVENANCE AND TRUTH MUST SURVIVE THE RESPONSE CHAIN
```

### 20.30 Meta-regla

`0 ERRORES, 0 OMISIONES` deberá entenderse como:

```text
NO UNEXPLAINED CRITICAL ERROR
NO SILENT CRITICAL OMISSION
NO FABRICATED CERTAINTY
```

### 20.31 Definition of Governance Done — v1.0

```text
[ ] normative chapters approved
[ ] canonical consolidated document created
[ ] terminology normalized or errata recorded
[ ] baseline facts preserved
[ ] physical implementation not silently mixed into governance
[ ] next-phase boundaries explicit
[ ] onboarding dependency explicit
```

### 20.32 Invariantes de ciclo de vida

```text
LIFE-INV-001 — NO SILENT NORMATIVE REWRITE
LIFE-INV-002 — NO LOSS OF DECISION HISTORY
LIFE-INV-003 — NO NEW SOURCE AS CERTIFIED WITHOUT ADMISSION PROCESS
LIFE-INV-004 — NO NEW PERIOD BY AUTOMATIC COPY-FORWARD ASSUMPTION
LIFE-INV-005 — NO NEW TERRITORIAL UNIVERSE WITHOUT TEMPORAL RECONCILIATION
LIFE-INV-006 — NO GOVERNANCE CLOSURE INTERPRETED AS IMPLEMENTATION COMPLETION
LIFE-INV-007 — NO INSTITUTIONAL KNOWLEDGE DEPENDENT ONLY ON CHAT OR MEMORY
```

### 20.33 Ciclo completo

```text
DEFINE
   ↓
AUDIT
   ↓
CERTIFY
   ↓
IMPLEMENT
   ↓
VERIFY
   ↓
RELEASE
   ↓
OBSERVE
   ↓
DETECT
   ↓
REMEDIATE
   ↓
LEARN
   ↓
VERSION
   ↓
DEFINE AGAIN
```

### 20.34 Principio final

> **HEYTI deberá recordar no solo qué dato utiliza, sino por qué confía en él, qué transformaciones lo afectaron, qué incertidumbres conserva y qué evidencia permitió certificarlo.**

### 20.35 Cierre normativo de HEYTI Data Truth Governance v1.0

Con la aprobación de este capítulo, el documento:

```text
HEYTI_Data_Truth_Governance_v1.0.md
```

alcanzará:

```text
NORMATIVE BASELINE COMPLETE
```

Esto no autoriza todavía:

```text
DB MUTATION
ETL REMEDIATION
SOURCE RENAME
LEGACY CLEANUP
MODULE MIGRATION
UI MIGRATION
```

### 20.36 Declaración de cierre

```text
HEYTI DATA TRUTH GOVERNANCE v1.0

STATUS:
NORMATIVE BASELINE COMPLETE

PRINCIPLE:
0 ERRORES
0 OMISIONES

NEXT:
PHYSICAL MAPPING
CERTIFIED REMEDIATION
CONTROLLED MIGRATION
END-TO-END VERIFICATION
```

---

## Fin del Capítulo 20
