# HEYTI Conceptual Entity Map v1.0

## Mapa Conceptual de Entidades

**Proyecto:** HEYTI-CORE  
**Sprint:** 8  
**Estado:** En construcción  

---

## 1. Objetivo

Representar conceptualmente las entidades fundamentales que se relacionan con la Sección Electoral como unidad mínima de inteligencia territorial de HEYTI-CORE.

Este documento no describe tablas ni implementación PostgreSQL.

Su propósito es identificar qué entidades existen alrededor de una Sección Electoral y cómo se relacionan desde el punto de vista del negocio, la inteligencia territorial y la operación estratégica.

---

## 2. Entidad Central

El modelo conceptual de HEYTI-CORE se organiza alrededor de una única entidad central: la **Sección Electoral**.

De acuerdo con la definición establecida en el *Section Strategic File v1.0*, la Sección Electoral constituye la **unidad mínima de inteligencia territorial**, representando el punto de convergencia de todos los dominios de conocimiento que integran la plataforma.

Cada Sección funciona como un **Expediente Estratégico Territorial**, capaz de concentrar información geográfica, electoral, demográfica, socioeconómica, organizacional, operativa e histórica, permitiendo comprender el comportamiento del territorio, generar inteligencia estratégica y apoyar la toma de decisiones.

En consecuencia, toda entidad incorporada al modelo conceptual de HEYTI-CORE deberá relacionarse directa o indirectamente con una Sección Electoral, garantizando que el conocimiento generado conserve un contexto territorial claramente definido.

Esta decisión arquitectónica constituye uno de los principios fundamentales de HEYTI-CORE y permite mantener un modelo coherente, escalable y orientado a la comprensión integral del territorio.

## 2.1 ¿Qué es un Dominio de Conocimiento?

Dentro de HEYTI-CORE, un Dominio de Conocimiento representa un conjunto organizado de entidades, reglas de negocio, procesos e información que describen un aspecto específico del territorio.

Cada dominio posee responsabilidades claramente definidas, mantiene independencia conceptual respecto de los demás dominios y aporta una perspectiva particular para comprender el comportamiento de una Sección Electoral.

Los dominios no representan módulos de software ni esquemas de base de datos.

Constituyen divisiones conceptuales del conocimiento que posteriormente darán origen a la arquitectura lógica, física y funcional de HEYTI-CORE.

En conjunto, todos los dominios convergen en el Expediente Estratégico Territorial, enriqueciendo la comprensión del territorio desde múltiples perspectivas complementarias.

---

## 3. Dominios Conceptuales de HEYTI-CORE

La Sección Electoral constituye la entidad central del modelo conceptual de HEYTI-CORE.

Alrededor de ella convergen los dominios de conocimiento que permiten comprender el territorio, generar inteligencia territorial y apoyar la toma de decisiones estratégicas.

Los dominios conceptuales de la primera versión de HEYTI-CORE son:

- Territorial
- Electoral
- Socioeconómico
- Capital Territorial
- Operación Territorial
- Inteligencia Territorial
- Productos de Inteligencia
- Riesgo y Seguridad
- Administración del Sistema

---

## 3.1 Dominio Territorial

El Dominio Territorial describe la ubicación, delimitación y organización geográfica de cada Sección Electoral.

Su función es establecer el contexto espacial y administrativo necesario para relacionar la Sección con país, estado, municipio, distrito federal, distrito local y geografía electoral vigente.

Este dominio constituye la base sobre la cual se integran los demás dominios de conocimiento de HEYTI-CORE.


### 3.1.1 Entidades del Dominio Territorial

El Dominio Territorial se compone de las entidades que permiten ubicar, delimitar, versionar y contextualizar una Sección Electoral dentro de la organización territorial de HEYTI-CORE.

| Entidad | Propósito |
|---|---|
| Country | Representa el país al que pertenece la estructura territorial. |
| State | Representa una entidad federativa. |
| Municipality | Representa el municipio al que pertenece una Sección Electoral. |
| Federal District | Representa el Distrito Electoral Federal correspondiente. |
| Local District | Representa el Distrito Electoral Local correspondiente. |
| Electoral Geography | Representa una versión oficial de la geografía electoral. |
| Section | Representa la unidad mínima de inteligencia territorial. |
| Section History | Conserva cambios históricos asociados a una Sección Electoral. |
| Territorial Event | Registra eventos relevantes que modifican o explican la evolución territorial. |

### 3.1.3 Lo que entrega al MIT

El Dominio Territorial entrega al Motor de Inteligencia Territorial la información necesaria para responder:

- ¿Dónde está la Sección?
- ¿A qué municipio pertenece?
- ¿A qué Distrito Federal pertenece?
- ¿A qué Distrito Local pertenece?
- ¿Bajo qué versión de geografía electoral se analiza?
- ¿Qué eventos territoriales explican su evolución?

Sin esta información, el MIT no puede contextualizar correctamente ningún diagnóstico ni recomendación.

### 3.1.4 Información que recibe del MIT

El Dominio Territorial recibe del Motor de Inteligencia Territorial información derivada del análisis conjunto de todos los dominios de conocimiento.

Entre los principales elementos que pueden incorporarse se encuentran:

- Clasificación estratégica de la Sección Electoral.
- Nivel de prioridad territorial.
- Nivel de competitividad.
- Nivel de riesgo.
- Recomendaciones territoriales.
- Escenarios de intervención.
- Productos de Inteligencia Territorial asociados a la Sección.

Esta retroalimentación permite enriquecer permanentemente el Expediente Estratégico Territorial y fortalecer la capacidad de aprendizaje de HEYTI-CORE.


---

## 3.2 Dominio Electoral

El Dominio Electoral integra el comportamiento histórico y actual de los procesos electorales asociados a cada Sección Electoral.

Su propósito consiste en proporcionar el contexto político necesario para comprender la evolución del territorio, identificar tendencias, evaluar niveles de competitividad y reconocer patrones de comportamiento electoral a lo largo del tiempo.

Este dominio concentra la información relacionada con elecciones, resultados oficiales, partidos políticos, coaliciones y demás elementos que permiten analizar el desempeño electoral del territorio.

La información contenida en este dominio constituye uno de los principales insumos utilizados por el Motor de Inteligencia Territorial para generar diagnósticos, escenarios y recomendaciones estratégicas.


---

## 3.3 Dominio Socioeconómico

El Dominio Socioeconómico incorpora los indicadores demográficos, sociales, económicos y de desarrollo que permiten caracterizar las condiciones de vida existentes dentro de una Sección Electoral.

Su propósito consiste en complementar el análisis político mediante evidencia objetiva sobre las características de la población, facilitando la comprensión del contexto territorial y fortaleciendo la construcción de estrategias diferenciadas.

La información proveniente de este dominio permite identificar oportunidades, riesgos y prioridades de intervención territorial, enriqueciendo las recomendaciones emitidas por el Motor de Inteligencia Territorial.


---

## 3.4 Dominio de Capital Territorial

El Dominio de Capital Territorial integra el conjunto de personas, liderazgos, organizaciones, estructuras y relaciones sociales que representan la capacidad organizativa existente dentro de una Sección Electoral.

Su propósito consiste en comprender no solamente quiénes participan en el territorio, sino cómo interactúan, cuál es su nivel de influencia, qué capacidad de convocatoria poseen y de qué manera contribuyen al desarrollo de estrategias territoriales.

El Capital Territorial constituye uno de los principales activos estratégicos de una Sección Electoral, ya que determina la capacidad real para organizar, comunicar, movilizar y ejecutar acciones dentro del territorio.

La información contenida en este dominio permite identificar fortalezas organizativas, detectar vacíos de estructura, reconocer liderazgos relevantes y estimar el potencial operativo disponible para alcanzar los objetivos estratégicos definidos por HEYTI-CORE.


---

## 3.5 Dominio de Operación Territorial

El Dominio de Operación Territorial integra el conjunto de actividades mediante las cuales una organización interviene de manera planificada sobre el territorio con el propósito de fortalecer su presencia, construir relaciones, consolidar estructuras y alcanzar objetivos estratégicos.

A diferencia de otros dominios que describen el estado del territorio, el Dominio de Operación Territorial representa la capacidad de actuar sobre él.

Comprende las actividades realizadas por promotores, brigadas, coordinadores, representantes, estructuras territoriales y demás actores responsables de ejecutar acciones dentro de una Sección Electoral.

Este dominio constituye el vínculo entre el conocimiento generado por el Motor de Inteligencia Territorial y la ejecución de estrategias sobre el territorio.

El Dominio de Operación Territorial constituye el mecanismo mediante el cual las recomendaciones generadas por el Motor de Inteligencia Territorial se convierten en acciones concretas sobre el territorio.

En consecuencia, toda intervención territorial deberá ser susceptible de evaluación, permitiendo medir su impacto y retroalimentar la Memoria Territorial de HEYTI-CORE.

---

## 3.3 Dominio Socioeconómico

### Objetivo

El Dominio Socioeconómico incorpora indicadores demográficos, sociales, económicos y de desarrollo que permiten caracterizar las condiciones de vida existentes dentro de una Sección Electoral.

Su propósito es complementar el análisis territorial y electoral mediante evidencia objetiva sobre la población, el entorno social y las condiciones estructurales del territorio.

### Entidades

| Entidad | Propósito |
|---|---|
| Socioeconomic Indicator | Representa un indicador socioeconómico. |
| Indicator Value | Registra el valor de un indicador asociado a una Sección Electoral. |
| Indicator Source | Identifica la fuente oficial del indicador. |
| Indicator Category | Agrupa indicadores por temática. |
| Socioeconomic Projection | Representa proyecciones futuras asociadas a una Sección Electoral. |

### Relaciones

Los valores socioeconómicos se relacionan directamente con `Section`.

Cada indicador deberá asociarse a una fuente, categoría y periodo de referencia.

### Reglas del Dominio

#### BR-SOC-001

Todo valor socioeconómico deberá pertenecer a una Sección Electoral.

---

#### BR-SOC-002

Todo indicador deberá tener una fuente identificable.

---

#### BR-SOC-003

Los indicadores deberán conservar su periodo de referencia.

---

#### BR-SOC-004

Las proyecciones socioeconómicas deberán distinguirse claramente de los datos observados.

---

#### BR-SOC-005

Los indicadores no deberán sobrescribirse sin conservar trazabilidad de versión, fuente o periodo.

### Información que entrega al MIT

- Población.
- Marginación.
- Rezago educativo.
- Ingreso estimado.
- Acceso a servicios.
- Pobreza.
- Índice urbano-rural.
- Proyecciones demográficas o socioeconómicas.

### Información que recibe del MIT

- Clasificación socioeconómica estratégica.
- Riesgos sociales detectados.
- Oportunidades de intervención.
- Recomendaciones diferenciadas según perfil territorial.
- Productos de Inteligencia Territorial asociados al contexto socioeconómico.


---

## 3.4 Dominio de Capital Territorial

### Objetivo

El Dominio de Capital Territorial integra el conjunto de personas, liderazgos, organizaciones y redes de colaboración que representan la capacidad organizativa existente dentro de una Sección Electoral.

Su propósito consiste en comprender quiénes participan en el territorio, cómo se relacionan entre sí, cuál es su nivel de influencia y de qué manera contribuyen a fortalecer o debilitar la capacidad operativa de una organización política.

### Entidades

| Entidad | Propósito |
|---|---|
| Territorial Actor | Representa a una persona u organización con presencia en el territorio. |
| Actor Role | Define el rol que desempeña un Actor Territorial. |
| Leadership | Representa liderazgos formales o informales. |
| Organization | Representa organizaciones presentes en la Sección. |
| Territorial Network | Representa relaciones entre actores. |
| Influence | Estima el nivel de influencia territorial. |

### Relaciones

Todo Actor Territorial pertenece a una o varias Secciones Electorales.

Un Actor puede desempeñar múltiples roles a lo largo del tiempo.

Las organizaciones agrupan actores y los liderazgos representan capacidades de coordinación o movilización.

### Reglas del Dominio

#### BR-CAP-001

Todo Actor Territorial deberá identificarse de manera única dentro de HEYTI.

---

#### BR-CAP-002

Los roles de un Actor podrán cambiar con el tiempo sin modificar la identidad del Actor.

---

#### BR-CAP-003

Un liderazgo constituye un rol especializado de un Actor Territorial y no una entidad independiente.

---

#### BR-CAP-004

Toda relación entre actores deberá conservar trazabilidad temporal.

---

#### BR-CAP-005

El Capital Territorial deberá medirse mediante indicadores compuestos y no únicamente por el número de personas registradas.

### Información que entrega al MIT

- Cobertura territorial.
- Nivel de organización.
- Liderazgos disponibles.
- Vacíos organizativos.
- Capacidad de movilización.
- Redes de colaboración.
- Índice de Capital Territorial.

### Información que recibe del MIT

- Prioridad para fortalecimiento.
- Recomendaciones de organización.
- Identificación de zonas críticas.
- Necesidades de nuevos liderazgos.
- Estrategias de fortalecimiento territorial.


---

## 3.5 Dominio de Operación Territorial

### Objetivo

El Dominio de Operación Territorial integra el conjunto de acciones mediante las cuales una organización interviene, fortalece y transforma el territorio.

Su propósito consiste en planear, ejecutar, monitorear y evaluar las intervenciones realizadas dentro de una Sección Electoral, permitiendo medir su impacto y retroalimentar permanentemente la Inteligencia Territorial.

### Entidades

| Entidad | Propósito |
|---|---|
| Territorial Intervention | Representa una intervención estratégica sobre el territorio. |
| Operational Plan | Define la planeación de una intervención. |
| Field Activity | Registra actividades realizadas en campo. |
| Visit | Registra visitas domiciliarias o de seguimiento. |
| Political Event | Representa eventos territoriales organizados. |
| Territorial Commitment | Registra compromisos adquiridos durante la operación. |
| Follow-up | Da seguimiento a compromisos e intervenciones. |
| Structure Assignment | Registra asignaciones dentro de la estructura territorial. |
| Election Day Operation | Representa actividades específicas del Día D. |

### Relaciones

Toda intervención deberá asociarse a una Sección Electoral.

Las actividades de campo, estructura territorial y operación del Día D forman parte del mismo proceso de intervención territorial y deberán conservar continuidad histórica.

### Reglas del Dominio

#### BR-OPS-001

Toda Intervención Territorial deberá estar asociada a una Sección Electoral.

---

#### BR-OPS-002

Toda actividad deberá conservar fecha, responsable y evidencia de ejecución.

---

#### BR-OPS-003

Las intervenciones podrán generar nuevos Actores Territoriales, modificar roles existentes o fortalecer el Capital Territorial.

---

#### BR-OPS-004

Toda intervención deberá producir un resultado medible.

---

#### BR-OPS-005

Los resultados de las intervenciones deberán incorporarse a la Memoria Territorial para fortalecer el aprendizaje del MIT.

### Información que entrega al MIT

- Nivel de actividad territorial.
- Cobertura de operación.
- Cumplimiento de objetivos.
- Resultados de intervenciones.
- Estado de la estructura territorial.
- Evidencias de campo.
- Actividad del Día D.
- Impacto operativo.

### Información que recibe del MIT

- Prioridad de intervención.
- Sectores prioritarios.
- Estrategias recomendadas.
- Asignación óptima de recursos.
- Objetivos operativos.
- Escenarios de intervención territorial.

---

## 3.6 Dominio de Riesgo y Seguridad

### Objetivo

El Dominio de Riesgo y Seguridad integra la información relacionada con las condiciones que pueden afectar la operación territorial dentro de una Sección Electoral.

Su propósito consiste en identificar factores que representen riesgos para la organización, la movilidad, la seguridad, la logística o el desarrollo de actividades estratégicas, permitiendo que el Motor de Inteligencia Territorial incorpore dichas variables al proceso de toma de decisiones.

### Entidades

| Entidad | Propósito |
|---|---|
| Risk Zone | Representa una zona con condiciones de riesgo. |
| Security Event | Registra eventos relevantes relacionados con seguridad. |
| Accessibility | Describe las condiciones de acceso al territorio. |
| Infrastructure | Registra infraestructura estratégica para la operación territorial. |
| Territorial Alert | Representa alertas emitidas sobre una Sección Electoral. |

### Relaciones

Los riesgos y eventos de seguridad se relacionan directamente con una Sección Electoral y podrán mantenerse vigentes durante distintos periodos de tiempo.

Una Sección podrá registrar múltiples riesgos simultáneamente, cada uno con diferente nivel de impacto.

### Reglas del Dominio

#### BR-RSK-001

Todo riesgo deberá asociarse a una Sección Electoral.

---

#### BR-RSK-002

Todo evento deberá conservar fecha, fuente y nivel de confiabilidad.

---

#### BR-RSK-003

Los riesgos deberán clasificarse por tipo, severidad y vigencia.

---

#### BR-RSK-004

Las alertas territoriales deberán conservar historial y trazabilidad.

---

#### BR-RSK-005

Los niveles de riesgo deberán incorporarse obligatoriamente a los procesos de recomendación del MIT.

### Información que entrega al MIT

- Nivel de riesgo territorial.
- Condiciones de seguridad.
- Accesibilidad.
- Restricciones operativas.
- Alertas territoriales.
- Infraestructura estratégica disponible.

### Información que recibe del MIT

- Prioridad de atención.
- Estrategias de mitigación.
- Recomendaciones operativas.
- Escenarios alternativos.
- Productos de Inteligencia Territorial relacionados con riesgos.


---

## 3.7 Dominio de Inteligencia Territorial

### Objetivo

El Dominio de Inteligencia Territorial constituye el núcleo cognitivo de HEYTI-CORE.

Su propósito consiste en integrar el conocimiento proveniente de todos los dominios territoriales, interpretarlo dentro de un contexto específico, generar hipótesis, evaluar escenarios y producir recomendaciones estratégicas sustentadas en evidencia.

A diferencia de los demás dominios, la Inteligencia Territorial no representa una fuente de información, sino la capacidad de transformar información dispersa en conocimiento útil para apoyar la toma de decisiones.

Este dominio representa el principal elemento diferenciador de HEYTI-CORE y constituye el fundamento conceptual del Motor de Inteligencia Territorial (MIT).

### Entidades

| Entidad | Propósito |
|---|---|
| Territorial Memory | Conserva el conocimiento histórico del territorio. |
| Knowledge Context | Integra el contexto utilizado durante el razonamiento. |
| Strategic Indicator | Representa indicadores derivados por el MIT. |
| Recommendation | Representa recomendaciones estratégicas. |
| Scenario | Representa escenarios prospectivos. |
| Reasoning Process | Conserva la trazabilidad del razonamiento realizado por el MIT. |
| Learning Cycle | Representa el proceso de aprendizaje continuo del MIT. |


### Relaciones

El Dominio de Inteligencia Territorial recibe información proveniente de todos los dominios de conocimiento.

Su función consiste en integrar dicha información, generar nuevo conocimiento y retroalimentar permanentemente el Expediente Estratégico Territorial.

Toda recomendación emitida por el MIT deberá poder relacionarse con la evidencia utilizada durante el proceso de razonamiento.



### Reglas del Dominio

#### BR-INT-001

Toda recomendación emitida por el MIT deberá estar sustentada en evidencia proveniente de uno o más dominios de conocimiento.

---

#### BR-INT-002

El MIT nunca deberá generar recomendaciones sin conservar trazabilidad del proceso de razonamiento.

---

#### BR-INT-003

Toda recomendación podrá ser reevaluada conforme se incorpore nueva información territorial.

---

#### BR-INT-004

La Memoria Territorial deberá conservar el historial de aprendizaje del MIT.

---

#### BR-INT-005

Los indicadores estratégicos deberán derivarse mediante metodologías documentadas y reproducibles.

---

#### BR-INT-006

La Inteligencia Territorial deberá explicar las razones que sustentan cada conclusión emitida.

---

#### BR-INT-007

El aprendizaje del MIT nunca deberá modificar la información histórica; únicamente podrá generar nuevas interpretaciones o recomendaciones.


### Información que entrega al MIT

El propio Dominio de Inteligencia Territorial constituye el núcleo del MIT.

Produce:

- Diagnósticos estratégicos.
- Clasificaciones territoriales.
- Escenarios.
- Recomendaciones.
- Indicadores estratégicos.
- Prioridades territoriales.
- Productos de Inteligencia Territorial.

### Información que recibe del MIT

El Dominio de Inteligencia Territorial recibe información proveniente de:

- Dominio Territorial.
- Dominio Electoral.
- Dominio Socioeconómico.
- Dominio de Capital Territorial.
- Dominio de Operación Territorial.
- Dominio de Riesgo y Seguridad.

La integración de estos dominios permite construir conocimiento territorial de mayor valor que la simple suma de los datos individuales.


---

## 3.8 Dominio de Productos de Inteligencia

### Objetivo

El Dominio de Productos de Inteligencia representa los mecanismos mediante los cuales el conocimiento generado por el Motor de Inteligencia Territorial se presenta al usuario en formatos comprensibles, verificables y orientados a la toma de decisiones.

Su propósito consiste en transformar el análisis territorial en productos ejecutivos capaces de comunicar diagnósticos, escenarios, recomendaciones y evidencia de manera clara, oportuna y contextualizada.

### Entidades

| Entidad | Propósito |
|---|---|
| Intelligence Product | Representa cualquier producto generado por el MIT. |
| Executive Dashboard | Resume el estado estratégico de una Sección Electoral. |
| Strategic Report | Consolida diagnósticos y recomendaciones. |
| Scenario Analysis | Presenta escenarios alternativos. |
| Recommendation Report | Explica recomendaciones emitidas por el MIT. |
| Conversation Session | Conserva la interacción entre el usuario y HEYTI. |

### Relaciones

Todo Producto de Inteligencia deberá relacionarse con uno o más dominios de conocimiento y conservar trazabilidad respecto de la evidencia utilizada para su generación.

### Reglas del Dominio

#### BR-PRD-001

Todo Producto de Inteligencia deberá identificar la evidencia utilizada para su elaboración.

---

#### BR-PRD-002

Todo Producto deberá conservar fecha, versión y contexto de generación.

---

#### BR-PRD-003

Las recomendaciones presentadas deberán corresponder a las emitidas por el MIT.

---

#### BR-PRD-004

Los productos deberán poder regenerarse utilizando la misma evidencia.

---

#### BR-PRD-005

Toda conversación relevante con HEYTI podrá formar parte de la Memoria Territorial cuando genere conocimiento útil para futuras decisiones.

### Información que entrega al MIT

- Retroalimentación del usuario.
- Preferencias de consulta.
- Historial de interacción.
- Confirmación o rechazo de recomendaciones.

### Información que recibe del MIT

- Diagnósticos.
- Recomendaciones.
- Escenarios.
- Indicadores estratégicos.
- Evidencia.
- Explicaciones.


---

## 3.9 Dominio de Administración del Sistema

### Objetivo

El Dominio de Administración del Sistema proporciona los servicios necesarios para operar, proteger y administrar la Plataforma HEYTI-CORE.

Su propósito consiste en gestionar usuarios, permisos, configuraciones, auditoría y seguridad, garantizando el correcto funcionamiento de todos los dominios de conocimiento.

### Entidades

| Entidad | Propósito |
|---|---|
| User | Representa un usuario autorizado. |
| Role | Define permisos y responsabilidades. |
| Organization | Representa una organización usuaria de HEYTI. |
| Permission | Controla el acceso a funcionalidades. |
| Audit Log | Conserva la trazabilidad de las acciones realizadas. |
| System Configuration | Administra parámetros generales del sistema. |

### Relaciones

Los usuarios interactúan con los Productos de Inteligencia y con los diferentes dominios de conocimiento conforme a los permisos asignados.

Toda acción relevante deberá registrarse mediante mecanismos de auditoría.

### Reglas del Dominio

#### BR-SYS-001

Todo usuario deberá pertenecer a una organización.

---

#### BR-SYS-002

Todo acceso deberá validarse mediante roles y permisos.

---

#### BR-SYS-003

Toda modificación relevante deberá registrarse en la Auditoría del Sistema.

---

#### BR-SYS-004

Las configuraciones generales deberán conservar historial de cambios.

---

#### BR-SYS-005

La administración del sistema nunca deberá modificar directamente el conocimiento generado por el MIT.

### Información que entrega al MIT

- Perfil del usuario.
- Contexto organizacional.
- Preferencias de operación.

### Información que recibe del MIT

- Productos personalizados.
- Recomendaciones contextualizadas.
- Configuración adaptativa.