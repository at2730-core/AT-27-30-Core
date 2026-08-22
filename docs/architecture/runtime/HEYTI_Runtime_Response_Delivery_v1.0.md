# HEYTI Runtime Response Delivery v1.0

**Proyecto:** HEYTI — AT 27–30
**Documento:** HEYTI Runtime Response Delivery
**Versión:** 1.0
**Estado:** Arquitectura Base
**Sprint:** Sprint 23 — HEYTI Runtime Response Delivery
**Clasificación:** Arquitectura de Runtime / Response Delivery
**Sistema:** HEYTI-CORE
**Fecha:** Agosto 2026

---

# Capítulo 1. Propósito, alcance y mandato arquitectónico

## 1.1 Propósito del documento

El presente documento define la arquitectura de **HEYTI Runtime Response Delivery (HRRD)**, responsable de establecer el mecanismo mediante el cual una respuesta producida y materializada por HEYTI puede abandonar de forma controlada el Runtime y ser entregada a un consumidor externo.

Runtime Response Delivery constituye la frontera arquitectónica entre:

- la ejecución interna de HEYTI;
- la materialización de una respuesta;
- y el consumidor responsable de utilizar o representar dicha respuesta.

Su propósito fundamental es garantizar que una respuesta válida producida por HEYTI pueda ser entregada sin perder:

- significado;
- estructura;
- identidad;
- contexto;
- trazabilidad;
- versión;
- estado;
- evidencia;
- metadatos;
- información de error;
- y capacidad de auditoría.

Runtime Response Delivery no constituye una capa de presentación.

Tampoco constituye una nueva capacidad cognitiva.

Su función es transportar de manera controlada el resultado producido por HEYTI desde el dominio interno del Runtime hacia la frontera de consumo del sistema.

---

## 1.2 Problema arquitectónico

Una respuesta correctamente producida dentro del Runtime no es suficiente para que HEYTI pueda operar como sistema completo.

Después de ejecutar una capability y materializar su resultado, todavía existe una pregunta arquitectónica fundamental:

> ¿Cómo abandona esa respuesta el Runtime sin perder su contrato, significado, contexto y trazabilidad?

La respuesta no debe depender directamente de:

- HTML;
- JavaScript;
- Leaflet;
- Chart.js;
- componentes visuales específicos;
- páginas particulares;
- estructuras circunstanciales del Portal;
- ni decisiones propias de una interfaz de usuario.

Si el Runtime conociera directamente estas tecnologías o estructuras, HEYTI quedaría acoplado a su capa de presentación.

Ese acoplamiento limitaría:

- la evolución del sistema;
- la reutilización de capacidades;
- la incorporación de nuevos consumidores;
- la automatización;
- las pruebas;
- la observabilidad;
- la interoperabilidad;
- y la independencia arquitectónica del Core.

Por ello se establece una frontera explícita denominada:

**Runtime Response Delivery.**

---

## 1.3 Mandato arquitectónico

HEYTI Runtime Response Delivery deberá garantizar que toda respuesta entregada por el Runtime:

1. provenga de un resultado válido del proceso de ejecución;
2. respete el contrato de respuesta vigente;
3. preserve la semántica producida durante la materialización;
4. conserve los identificadores necesarios para su trazabilidad;
5. pueda ser serializada mediante una representación estable;
6. pueda ser consumida sin conocimiento de las estructuras internas del Runtime;
7. mantenga separación estricta respecto de la presentación;
8. permita identificar errores de entrega;
9. permita observabilidad y auditoría;
10. soporte evolución mediante contratos versionados.

Este mandato establece una nueva frontera formal dentro de HEYTI.

---

## 1.4 Principio fundamental

El principio central de Runtime Response Delivery será:

> **HEYTI entrega significado estructurado; el consumidor decide cómo representarlo.**

Por lo tanto:

```text
Knowledge
    ↓
Capability
    ↓
Runtime
    ↓
Materialization
    ↓
Response Contract
    ↓
Runtime Response Delivery
    ↓
Consumer
    ↓
Presentation
```

Cada nivel conserva una responsabilidad distinta.

---

## 1.5 Separación de responsabilidades

La arquitectura deberá preservar explícitamente la siguiente separación:

```text
Materialization ≠ Delivery ≠ Presentation
```

### Materialization

Determina cómo el resultado de una ejecución se convierte en una respuesta formal de HEYTI.

Su responsabilidad termina cuando existe un contrato de respuesta válido y materializado.

### Delivery

Determina cómo esa respuesta cruza la frontera del Runtime y llega de forma segura, consistente y trazable a un consumidor.

No modifica el significado de la respuesta.

### Presentation

Determina cómo el consumidor representa la información ante el usuario.

Puede utilizar:

- texto;
- tablas;
- mapas;
- gráficas;
- indicadores;
- tarjetas;
- paneles;
- alertas;
- controles;
- u otros componentes visuales.

Estas decisiones pertenecen exclusivamente a la capa de presentación.

---

## 1.6 Regla de preservación semántica

Runtime Response Delivery deberá cumplir la siguiente regla:

> **Delivery MAY transform representation; Delivery MUST NOT transform meaning.**

Es decir, la capa podrá realizar operaciones necesarias para transportar una respuesta, tales como:

- serialización;
- empaquetado;
- adaptación de transporte;
- incorporación de metadatos de entrega;
- codificación;
- normalización de representación.

Pero no podrá:

- reinterpretar hallazgos;
- modificar conclusiones;
- recalcular indicadores;
- alterar evidencia;
- cambiar niveles de confianza;
- eliminar advertencias cognitivas;
- inventar información;
- modificar reglas de negocio;
- ni sustituir decisiones tomadas durante la ejecución o materialización.

La semántica pertenece a las capas anteriores.

---

## 1.7 Posición dentro de HEYTI

Runtime Response Delivery se ubica después del proceso de materialización y antes de cualquier consumidor externo.

Su posición conceptual es:

```text
┌───────────────────────────────┐
│           Consumer            │
│ Portal / UI / API / Service   │
└───────────────▲───────────────┘
                │
                │ Delivery Boundary
                │
┌───────────────┴───────────────┐
│ HEYTI Runtime Response        │
│ Delivery                      │
└───────────────▲───────────────┘
                │
┌───────────────┴───────────────┐
│ Response Contract             │
│ Materialized Response         │
└───────────────▲───────────────┘
                │
┌───────────────┴───────────────┐
│ Materialization               │
└───────────────▲───────────────┘
                │
┌───────────────┴───────────────┐
│ Runtime / Capabilities        │
└───────────────────────────────┘
```

Esta posición convierte a Response Delivery en una frontera arquitectónica formal.

---

## 1.8 Alcance

HEYTI Runtime Response Delivery v1.0 deberá definir, como mínimo:

- el modelo de entrega de respuestas;
- el Response Delivery Pipeline;
- el contrato de entrega;
- la relación con `HeytiResponseContract`;
- las reglas de serialización;
- los metadatos de entrega;
- los identificadores de correlación;
- la trazabilidad de ejecución;
- la relación con sesiones;
- la clasificación de resultados;
- la representación de errores;
- la relación con consumidores externos;
- la frontera con Gateway;
- las reglas de compatibilidad;
- el versionado de contratos;
- la observabilidad;
- la auditabilidad;
- los criterios de validación;
- y las condiciones de aceptación de una entrega.

---

## 1.9 Fuera de alcance

Runtime Response Delivery v1.0 no será responsable de:

- diseñar la interfaz gráfica final de HEYTI;
- implementar mapas;
- construir gráficas;
- definir estilos CSS;
- administrar componentes HTML;
- decidir colores o iconografía;
- ejecutar consultas cognitivas;
- sustituir al Capability Runtime;
- realizar materialización;
- consultar directamente HKS;
- consultar directamente HES;
- ejecutar reglas de negocio;
- modificar evidencia;
- ni determinar conclusiones estratégicas.

Tampoco deberá convertirse en una segunda capa de materialización.

---

## 1.10 Consumidor

Se define **Consumer** como cualquier componente autorizado capaz de recibir una respuesta entregada por HEYTI.

Ejemplos conceptuales:

```text
Consumer
├── Portal
├── HEYTI User Interface
├── API Client
├── Internal Service
├── Testing Harness
└── Future Integration
```

La arquitectura no deberá asumir que existe un único consumidor.

Esta decisión permite que HEYTI evolucione sin que el Runtime quede ligado permanentemente al Portal actual.

---

## 1.11 Portal como primer consumidor

Dentro de AT 27–30, el Portal constituye el candidato natural para convertirse en uno de los primeros consumidores de respuestas HEYTI.

Sin embargo:

> **Portal es consumidor de HEYTI; Portal no forma parte del núcleo cognitivo de HEYTI.**

Por lo tanto, la arquitectura deberá permitir:

```text
HEYTI Core
     ↓
Response Delivery
     ↓
Delivery Boundary
     ↓
Portal
```

sin introducir dependencias inversas como:

```text
HEYTI Core
     ↓
portal.html
     ↓
DOM
     ↓
componentes específicos
```

Esta última relación queda arquitectónicamente prohibida.

---

## 1.12 Relación con la futura interfaz visual

Runtime Response Delivery deberá permitir que una respuesta pueda contener información estructurada suficiente para que una interfaz represente posteriormente:

- narrativa;
- indicadores;
- estadísticas;
- series;
- comparaciones;
- tablas;
- mapas;
- geometrías;
- referencias territoriales;
- evidencias;
- advertencias;
- recomendaciones;
- y acciones disponibles.

Sin embargo, deberá existir una distinción estricta entre:

```text
"qué información puede representarse"
```

y:

```text
"cómo debe verse esa información"
```

HEYTI puede entregar la primera.

La interfaz será responsable de la segunda.

---

## 1.13 Compatibilidad con los módulos AT 27–30

La arquitectura deberá contemplar que los módulos existentes de AT 27–30 evolucionen progresivamente hacia consumidores o superficies de interacción con HEYTI.

Esto no implica reescribirlos durante este Sprint.

Runtime Response Delivery deberá proporcionar una frontera suficientemente neutral para permitir futuras integraciones con:

- Análisis Territorial;
- Ganar Todo;
- Campo;
- Día D;
- ET-27;
- Socioeconómico;
- y futuras superficies del sistema.

La integración específica con cada módulo deberá desarrollarse mediante contratos y adaptadores posteriores, evitando introducir dependencias particulares dentro del Runtime.

---

## 1.14 Invariantes arquitectónicos

HEYTI Runtime Response Delivery v1.0 establece los siguientes invariantes.

### HRRD-I01 — No Presentation Logic

El Runtime no contendrá lógica de presentación.

### HRRD-I02 — Semantic Preservation

Una respuesta entregada deberá conservar el significado de la respuesta materializada.

### HRRD-I03 — Contract First

Toda entrega deberá estar respaldada por un contrato explícito.

### HRRD-I04 — Traceability

Toda entrega deberá poder relacionarse con la ejecución que la produjo.

### HRRD-I05 — Consumer Independence

El Core no deberá depender de un consumidor específico.

### HRRD-I06 — Deterministic Serialization

Una misma estructura válida deberá poder ser serializada de forma consistente.

### HRRD-I07 — Explicit Failure

Los fallos de entrega deberán ser explícitos y clasificables.

### HRRD-I08 — Version Awareness

Toda entrega deberá poder identificar la versión relevante de su contrato.

### HRRD-I09 — Auditability

La entrega deberá conservar información suficiente para reconstruir su procedencia operacional.

### HRRD-I10 — No Cognitive Mutation

La capa Delivery no podrá modificar decisiones cognitivas previamente materializadas.

---

## 1.15 Regla de no omisión

Una respuesta no deberá considerarse correctamente entregada únicamente porque el transporte técnico haya concluido.

La entrega deberá garantizar que los elementos obligatorios definidos por el contrato permanezcan presentes.

Por tanto:

```text
Transport Success ≠ Valid Delivery
```

Una entrega válida requiere:

```text
Valid Delivery
=
Valid Materialized Response
+
Valid Delivery Contract
+
Valid Serialization
+
Required Metadata
+
Traceability
+
Successful Boundary Transfer
```

Esta regla evita que una respuesta técnicamente transmitida sea considerada válida cuando haya perdido información necesaria durante el proceso.

---

## 1.16 Regla de honestidad de entrega

Response Delivery no deberá ocultar errores ocurridos en etapas anteriores.

Si una respuesta materializada contiene:

- advertencias;
- limitaciones;
- evidencia insuficiente;
- datos incompletos;
- incertidumbre;
- errores parciales;
- o información de confianza;

la capa Delivery deberá preservarlos conforme al contrato.

Nunca deberá convertir artificialmente una respuesta incompleta en una respuesta aparentemente completa.

---

## 1.17 Delivery como frontera auditable

Cada operación de entrega deberá poder asociarse, cuando corresponda, con identificadores tales como:

```text
request_id
session_id
execution_id
response_id
delivery_id
capability_id
contract_version
timestamp
```

La definición exacta de estos elementos será desarrollada en capítulos posteriores.

El objetivo es permitir reconstruir una cadena semejante a:

```text
User Request
   ↓
request_id
   ↓
Runtime Execution
   ↓
execution_id
   ↓
Materialized Response
   ↓
response_id
   ↓
Delivery Operation
   ↓
delivery_id
   ↓
Consumer
```

De esta manera, HEYTI podrá responder no solamente:

> ¿Qué respondió?

sino también:

> ¿Qué ejecución produjo esa respuesta, bajo qué contrato y mediante qué operación fue entregada?

---

## 1.18 Resultado esperado

Al concluir la implementación derivada de esta arquitectura, HEYTI deberá ser capaz de realizar conceptualmente:

```text
execute(request)
      ↓
capability_result
      ↓
materialize(result)
      ↓
HeytiResponseContract
      ↓
deliver(response)
      ↓
DeliveryResult
```

donde `DeliveryResult` permita determinar de forma inequívoca si la respuesta:

- fue aceptada para entrega;
- fue validada;
- fue serializada;
- fue entregada;
- fue rechazada;
- o produjo un error controlado.

---

## 1.19 Criterio de éxito arquitectónico

Runtime Response Delivery será considerado arquitectónicamente correcto cuando pueda sustituirse un consumidor por otro sin modificar:

- las capabilities;
- el conocimiento;
- HKS;
- HES;
- la lógica de materialización;
- ni la semántica del contrato de respuesta.

Conceptualmente:

```text
                ┌── Portal
                │
HEYTI Delivery ─┼── HEYTI UI
                │
                ├── API Client
                │
                └── Future Consumer
```

La incorporación de un nuevo consumidor no deberá requerir una modificación cognitiva de HEYTI.

---

## 1.20 Declaración arquitectónica

HEYTI Runtime Response Delivery se establece como la frontera formal responsable de convertir una respuesta materializada internamente en una respuesta entregable externamente sin alterar su significado.

Su existencia garantiza que HEYTI pueda evolucionar desde un Runtime capaz de producir respuestas hacia una plataforma capaz de exponerlas de manera:

- estable;
- desacoplada;
- trazable;
- auditable;
- versionada;
- interoperable;
- y preparada para múltiples consumidores.

La regla arquitectónica final de este capítulo queda establecida como:

> **HEYTI piensa mediante sus capacidades, materializa mediante sus contratos y entrega mediante una frontera explícita. La presentación comienza únicamente después de esa frontera.**

---

**Fin del Capítulo 1**

# Capítulo 2. Posición arquitectónica y fronteras de Runtime Response Delivery

## 2.1 Propósito del capítulo

Este capítulo define la posición exacta de **HEYTI Runtime Response Delivery (HRRD)** dentro de la arquitectura general de HEYTI y establece las fronteras que separan sus responsabilidades de las correspondientes a:

- Gateway;
- Runtime;
- Capability Registry;
- Capabilities;
- HKS;
- HES;
- Materialization;
- consumidores;
- y Presentation.

El objetivo es impedir que Response Delivery evolucione como una capa ambigua en la que terminen mezclándose responsabilidades de ejecución, conocimiento, transporte y presentación.

La arquitectura deberá poder responder de manera inequívoca:

> ¿Dónde comienza Runtime Response Delivery?

> ¿Dónde termina Runtime Response Delivery?

> ¿Qué puede hacer dentro de esas fronteras?

> ¿Qué tiene expresamente prohibido hacer?

La respuesta a estas preguntas constituye la base para su posterior implementación.

---

## 2.2 Posición arquitectónica general

Runtime Response Delivery ocupa una posición posterior a la materialización de la respuesta y anterior al consumidor.

La cadena general se establece conceptualmente como:

```text
User / External Actor
        │
        ▼
┌─────────────────────────────┐
│          Gateway            │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│           Runtime           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│     Capability Registry     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│         Capability          │
└──────────────┬──────────────┘
               │
        ┌──────┴──────┐
        ▼             ▼
┌─────────────┐ ┌─────────────┐
│     HKS     │ │     HES     │
└──────┬──────┘ └──────┬──────┘
       └───────┬────────┘
               │
               ▼
┌─────────────────────────────┐
│       Capability Result     │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Materialization       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│    HeytiResponseContract    │
└──────────────┬──────────────┘
               │
===============│================
    DELIVERY ENTRY BOUNDARY
===============│================
               ▼
┌─────────────────────────────┐
│ Runtime Response Delivery   │
└──────────────┬──────────────┘
               │
===============│================
    DELIVERY EXIT BOUNDARY
===============│================
               ▼
┌─────────────────────────────┐
│          Consumer           │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│        Presentation         │
└─────────────────────────────┘
```

Este modelo establece dos fronteras diferentes:

1. **Delivery Entry Boundary**
2. **Delivery Exit Boundary**

Estas fronteras deberán permanecer explícitas durante diseño, implementación y pruebas.

---

## 2.3 Delivery Entry Boundary

La **Delivery Entry Boundary** representa el punto en el que Runtime Response Delivery acepta responsabilidad sobre una respuesta.

La entrada primaria de Delivery no deberá ser:

- una consulta del usuario;
- un resultado bruto de una capability;
- una consulta SQL;
- evidencia sin materializar;
- un objeto específico de HKS;
- un objeto específico de HES;
- ni información directamente obtenida de una fuente de datos.

La entrada esperada será una respuesta previamente materializada conforme al contrato vigente.

Conceptualmente:

```text
Materialization
      │
      ▼
HeytiResponseContract
      │
      ▼
[ Delivery Entry Boundary ]
      │
      ▼
Response Delivery
```

Por tanto:

> **Delivery recibe respuestas; no construye conocimiento.**

---

## 2.4 Condiciones de aceptación en la frontera de entrada

Una respuesta no deberá ingresar automáticamente al pipeline de Delivery.

Antes de continuar, la capa deberá poder verificar las precondiciones establecidas por el contrato.

Como mínimo, la arquitectura deberá permitir validar:

- existencia de la respuesta;
- tipo de respuesta aceptado;
- versión contractual;
- identidad de la respuesta;
- estado;
- estructura obligatoria;
- metadatos requeridos;
- integridad básica;
- y trazabilidad mínima disponible.

Conceptualmente:

```text
Incoming Materialized Response
            │
            ▼
┌─────────────────────────────┐
│ Delivery Entry Validation   │
└──────────────┬──────────────┘
               │
        ┌──────┴──────┐
        │             │
      VALID         INVALID
        │             │
        ▼             ▼
 Delivery Pipeline   Reject
```

Una entrada inválida deberá producir un fallo explícito.

Nunca deberá ser corregida silenciosamente por Delivery.

---

## 2.5 Delivery Exit Boundary

La **Delivery Exit Boundary** representa el punto donde HEYTI deja de controlar la operación interna de entrega y el resultado queda disponible para un consumidor.

Conceptualmente:

```text
Response Delivery
       │
       ▼
Delivery Representation
       │
       ▼
[ Delivery Exit Boundary ]
       │
       ▼
Consumer
```

Una vez cruzada esta frontera, la responsabilidad sobre la representación visual corresponde al consumidor.

La capa Delivery no deberá asumir cómo será presentada la información.

---

## 2.6 Frontera con Materialization

La relación entre Materialization y Delivery deberá ser unidireccional.

```text
Materialization
      │
      ▼
Delivery
```

Delivery podrá depender del contrato producido por Materialization.

Materialization no deberá depender de Delivery.

Por tanto, queda prohibida una relación circular como:

```text
Materialization
      ▲     │
      │     ▼
    Delivery
```

La materialización deberá poder existir, ejecutarse y probarse independientemente de la entrega.

De igual forma, Delivery deberá poder probarse utilizando respuestas materializadas conocidas sin necesidad de ejecutar todo el pipeline cognitivo.

---

## 2.7 Frontera con Capability Runtime

Capability Runtime es responsable de ejecutar capacidades.

Response Delivery no deberá:

- seleccionar capabilities;
- registrar capabilities;
- resolver capabilities;
- ejecutar capabilities;
- reintentar una capability;
- modificar parámetros de ejecución;
- decidir qué capability responde una solicitud;
- ni interpretar resultados brutos de capabilities.

La relación permitida es indirecta:

```text
Capability Runtime
       │
       ▼
Capability Result
       │
       ▼
Materialization
       │
       ▼
Response Delivery
```

No deberá existir:

```text
Response Delivery
       │
       ▼
Execute Capability
```

Esta separación impide que Delivery se convierta accidentalmente en un segundo orquestador.

---

## 2.8 Frontera con Capability Registry

Capability Registry conserva la responsabilidad de conocer y resolver las capacidades disponibles en HEYTI.

Response Delivery no deberá consultar el Registry para decidir cómo entregar una respuesta.

La identidad de la capability que originó una respuesta podrá viajar como metadato de trazabilidad, por ejemplo:

```text
capability_id
capability_version
```

pero estos datos serán descriptivos.

No conferirán a Delivery autoridad para:

- cargar una capability;
- resolver una capability;
- activar una capability;
- sustituir una capability;
- ni modificar su registro.

La regla será:

> **Delivery puede conocer la identidad de origen; no controla el origen.**

---

## 2.9 Frontera con HKS

HEYTI Knowledge System (HKS) pertenece al dominio de conocimiento del sistema.

Runtime Response Delivery no deberá realizar consultas directas contra HKS para completar una respuesta.

Queda prohibido el patrón:

```text
Delivery
   │
   ▼
HKS
   │
   ▼
"Completar respuesta"
```

Si falta información necesaria, dicha ausencia deberá resolverse antes de alcanzar Delivery o deberá permanecer explícitamente representada en el contrato.

Delivery no deberá compensar deficiencias cognitivas mediante consultas adicionales.

---

## 2.10 Frontera con HES

HEYTI Evidence System (HES) mantiene la evidencia y su relación con las respuestas cognitivas.

Delivery podrá transportar referencias o estructuras de evidencia que formen parte de la respuesta materializada.

Sin embargo, no deberá:

- buscar evidencia adicional;
- sustituir evidencia;
- reinterpretar evidencia;
- elevar o reducir su peso;
- modificar procedencia;
- ni reconstruir razonamientos.

Conceptualmente:

```text
HES
 │
 ▼
Capability / Cognitive Processing
 │
 ▼
Materialization
 │
 ▼
Evidence Representation
 │
 ▼
Delivery
```

La evidencia atraviesa Delivery.

Delivery no gobierna la evidencia.

---

## 2.11 Frontera con Gateway

Gateway y Response Delivery representan fronteras relacionadas pero conceptualmente distintas.

El Gateway puede constituir la frontera de entrada y salida entre HEYTI y el entorno externo.

Response Delivery constituye la frontera interna especializada en preparar y entregar respuestas.

Conceptualmente:

```text
                  REQUEST
Consumer ───────────► Gateway
                       │
                       ▼
                     Runtime
                       │
                       ▼
                 Materialization
                       │
                       ▼
              Response Delivery
                       │
                       ▼
Gateway ◄──────────────┘
   │
   ▼
Consumer
```

En una implementación concreta, Gateway podrá actuar como adaptador de transporte.

Response Delivery no deberá convertirse automáticamente en:

- servidor HTTP;
- framework web;
- router;
- controlador REST;
- WebSocket server;
- manejador del DOM;
- ni infraestructura específica de red.

La relación exacta entre ambos componentes deberá conservar desacoplamiento.

---

## 2.12 Delivery no es Transport

Es necesario distinguir:

```text
Delivery ≠ Transport
```

**Transport** responde principalmente:

> ¿Por qué mecanismo técnico viajan los datos?

Por ejemplo:

- HTTP;
- WebSocket;
- llamada interna;
- cola;
- archivo;
- IPC;
- u otro mecanismo futuro.

**Delivery** responde:

> ¿Qué condiciones debe cumplir una respuesta para abandonar HEYTI de manera válida, íntegra y trazable?

Por tanto:

```text
Response Delivery
       │
       ▼
Transport Adapter
       │
       ▼
Transport Mechanism
```

Esta separación permitirá sustituir mecanismos técnicos sin modificar la semántica de entrega.

---

## 2.13 Frontera con Consumer

Un Consumer recibe el producto de Delivery.

El consumidor podrá conocer el contrato público necesario para interpretar la respuesta.

No deberá necesitar conocer:

- clases internas del Runtime;
- estructura interna de Capability Registry;
- implementación de HKS;
- implementación de HES;
- materializadores concretos;
- detalles privados del Kernel;
- ni estructuras Python internas no publicadas.

La frontera deberá permitir:

```text
Consumer
   │
   └── conoce → Delivery Contract
```

pero evitar:

```text
Consumer
   ├── conoce → Runtime internals
   ├── conoce → HKS internals
   ├── conoce → HES internals
   └── conoce → Capability internals
```

Esta regla es fundamental para preservar el encapsulamiento de HEYTI.

---

## 2.14 Frontera con Presentation

Presentation comienza después de Delivery.

La presentación podrá decidir que un elemento entregado como:

```text
type: "metric"
label: "Lista nominal"
value: 1842
```

se represente mediante:

- una tarjeta;
- una tabla;
- un indicador;
- una gráfica;
- un panel;
- una etiqueta cartográfica;
- o cualquier otro recurso visual.

Delivery no deberá establecer esa decisión.

De igual forma, una serie entregada como estructura de datos podrá posteriormente utilizarse en una gráfica, pero Delivery no deberá contener instrucciones dependientes de Chart.js.

Una referencia territorial podrá visualizarse mediante Leaflet, pero Delivery no deberá depender de Leaflet.

La regla será:

> **Delivery describe contenido consumible; Presentation decide composición visual.**

---

## 2.15 Frontera con los módulos AT 27–30

Los módulos existentes deberán considerarse consumidores potenciales o superficies especializadas de presentación.

La integración futura podrá adoptar un modelo semejante a:

```text
                        ┌──────────────────────┐
                        │ Análisis Territorial │
                        └──────────▲───────────┘
                                   │
                        ┌──────────┴───────────┐
                        │     Ganar Todo       │
                        └──────────▲───────────┘
                                   │
                        ┌──────────┴───────────┐
                        │        Campo         │
                        └──────────▲───────────┘
                                   │
HEYTI Response Delivery ───────────┼─────────────► Consumers
                                   │
                        ┌──────────┴───────────┐
                        │        Día D         │
                        └──────────▲───────────┘
                                   │
                        ┌──────────┴───────────┐
                        │        ET-27         │
                        └──────────▲───────────┘
                                   │
                        ┌──────────┴───────────┐
                        │   Socioeconómico     │
                        └──────────────────────┘
```

Este esquema es conceptual.

No significa que Delivery conozca individualmente la implementación de cada módulo.

La integración deberá producirse mediante contratos públicos y adaptadores.

---

## 2.16 Prohibición de dependencias visuales

El paquete de Runtime Response Delivery no deberá depender directamente de librerías de presentación.

Quedan fuera de su dominio dependencias como:

```text
Leaflet
Chart.js
HTML
CSS
DOM APIs
html2canvas
jsPDF
component libraries
browser-specific UI state
```

Esto no significa que dichas tecnologías sean incorrectas.

Significa que pertenecen a otra frontera arquitectónica.

La UI podrá utilizarlas libremente cuando corresponda.

El Core no deberá necesitarlas para entregar una respuesta.

---

## 2.17 Dirección de dependencias

La dirección arquitectónica permitida deberá conservarse de manera estricta.

Conceptualmente:

```text
Knowledge
   │
   ▼
Capabilities
   │
   ▼
Runtime
   │
   ▼
Materialization
   │
   ▼
Delivery
   │
   ▼
Adapters
   │
   ▼
Consumers
```

Las dependencias no deberán invertirse de manera que:

```text
Core → Portal implementation
Core → Browser
Core → Leaflet
Core → Chart.js
Core → DOM
```

La evolución de la interfaz no deberá obligar a modificar el núcleo cognitivo.

---

## 2.18 Dependencias permitidas

Runtime Response Delivery podrá depender de componentes estables y explícitamente autorizados, tales como:

- contratos públicos de respuesta;
- tipos de materialización;
- contratos propios de Delivery;
- validadores;
- abstracciones de serialización;
- modelos de trazabilidad;
- modelos de sesión cuando sean necesarios;
- abstracciones de adaptadores;
- infraestructura común autorizada del Core.

Estas dependencias deberán ser mínimas.

La incorporación de cualquier nueva dependencia deberá responder a una responsabilidad real de Delivery.

---

## 2.19 Dependencias prohibidas

Salvo decisión arquitectónica posterior explícita, Runtime Response Delivery no deberá depender directamente de:

- implementaciones concretas de capabilities;
- consultas particulares a PostgreSQL/PostGIS;
- archivos JSON específicos de AT 27–30;
- páginas HTML;
- archivos CSS;
- componentes JavaScript de presentación;
- estructuras DOM;
- librerías cartográficas;
- librerías gráficas;
- rutas específicas de módulos;
- estado visual del navegador;
- ni conocimiento de diseño de pantalla.

Esta prohibición protege la portabilidad del Core.

---

## 2.20 Modelo de puertos y adaptadores

Runtime Response Delivery deberá diseñarse de forma compatible con un modelo conceptual de puertos y adaptadores.

```text
                   HEYTI CORE

┌──────────────────────────────────────────────┐
│                                              │
│          Materialized Response               │
│                    │                         │
│                    ▼                         │
│         ┌────────────────────┐               │
│         │ Response Delivery  │               │
│         └─────────┬──────────┘               │
│                   │                          │
│              Delivery Port                   │
│                   │                          │
└───────────────────┼──────────────────────────┘
                    │
          ┌─────────┼─────────┐
          │         │         │
          ▼         ▼         ▼
      HTTP/API   Internal   Future
      Adapter    Adapter    Adapter
          │         │         │
          ▼         ▼         ▼
       Portal      Tests    Consumer
```

El **Delivery Port** representa la abstracción estable.

Los adaptadores podrán evolucionar independientemente.

---

## 2.21 Responsabilidad del Delivery Port

El Delivery Port deberá expresar la operación de entrega sin imponer una tecnología concreta.

Conceptualmente podrá evolucionar hacia una abstracción semejante a:

```python
deliver(response, context) -> DeliveryResult
```

Esta firma es únicamente conceptual en esta etapa arquitectónica.

No constituye todavía una decisión definitiva de implementación.

El contrato final deberá definirse posteriormente considerando:

- contexto;
- validación;
- serialización;
- destino;
- resultado;
- errores;
- trazabilidad;
- y versionado.

---

## 2.22 Response Delivery como Anti-Corruption Boundary

Runtime Response Delivery deberá actuar también como una frontera de protección entre el modelo interno de HEYTI y consumidores externos.

Un consumidor no deberá obligar al Core a deformar su arquitectura interna.

Por ejemplo, si una interfaz requiere:

```text
datasets
labels
colors
canvas_id
chart_type
```

esas necesidades no deberán incorporarse automáticamente al contrato cognitivo.

Podrá existir posteriormente un adaptador de presentación:

```text
HeytiResponseContract
        │
        ▼
Response Delivery
        │
        ▼
UI Adapter
        │
        ▼
Chart Configuration
```

La configuración visual será producida fuera del núcleo.

---

## 2.23 Regla de sustitución del consumidor

La arquitectura deberá superar la siguiente prueba conceptual:

> Si mañana `portal.html` desapareciera y fuera sustituido por una nueva aplicación, ¿HEYTI-CORE seguiría siendo funcionalmente válido?

La respuesta arquitectónica deberá ser:

**Sí.**

Podrían requerirse:

- un nuevo adaptador;
- una nueva integración;
- una nueva capa de presentación.

Pero no deberían requerirse modificaciones cognitivas en:

- HKS;
- HES;
- Capability Registry;
- capabilities;
- materialización;
- ni reglas de negocio.

Esta prueba será denominada:

**Consumer Substitution Test.**

---

## 2.24 Regla de sustitución del transporte

También deberá superarse:

> Si el mecanismo técnico de transporte cambia, ¿la semántica de Delivery permanece válida?

Por ejemplo:

```text
HTTP
 ↓
WebSocket
```

o:

```text
Internal Call
 ↓
REST API
```

El cambio podrá requerir un adaptador distinto.

No deberá requerir redefinir qué significa una entrega válida.

Esta prueba será denominada:

**Transport Substitution Test.**

---

## 2.25 Regla de aislamiento cognitivo

Ningún fallo exclusivo de Presentation deberá modificar retroactivamente el significado de una respuesta materializada.

Ejemplo:

```text
HEYTI Response
     │
     ▼
Delivery OK
     │
     ▼
Consumer receives response
     │
     ▼
Chart rendering fails
```

En este escenario:

```text
Cognitive Result = VALID
Delivery = VALID
Presentation = FAILED
```

No deberá registrarse falsamente:

```text
HEYTI Cognitive Execution = FAILED
```

Cada frontera deberá conservar su propio estado.

---

## 2.26 Regla de aislamiento de Delivery

De forma inversa, una respuesta cognitivamente válida podrá experimentar un fallo durante Delivery.

Ejemplo:

```text
Capability Execution = VALID
Materialization = VALID
Delivery Serialization = FAILED
```

El sistema deberá conservar la distinción:

```text
Cognitive Result = VALID
Materialized Response = VALID
Delivery = FAILED
```

Esto será esencial para diagnóstico y auditoría.

---

## 2.27 Modelo de estados por frontera

La arquitectura deberá evitar un único estado global ambiguo.

Conceptualmente:

```text
Execution Status
Materialization Status
Delivery Status
Presentation Status
```

podrán representar estados diferentes.

Por ejemplo:

```text
execution_status       = SUCCESS
materialization_status = SUCCESS
delivery_status        = SUCCESS
presentation_status    = ERROR
```

o:

```text
execution_status       = SUCCESS
materialization_status = SUCCESS
delivery_status        = ERROR
presentation_status    = NOT_REACHED
```

Esta separación deberá conservarse cuando posteriormente se definan los contratos concretos.

---

## 2.28 Matriz de responsabilidades

La siguiente matriz establece la distribución conceptual de responsabilidades:

| Responsabilidad | Runtime | Materialization | Delivery | Consumer / Presentation |
|---|---:|---:|---:|---:|
| Ejecutar capability | Sí | No | No | No |
| Consultar conocimiento | Indirectamente | No | No | No |
| Construir respuesta formal | No | Sí | No | No |
| Validar entrada de Delivery | No | No | Sí | No |
| Serializar para entrega | No | No | Sí | No |
| Preservar trazabilidad de entrega | No | Parcial | Sí | No |
| Seleccionar mecanismo visual | No | No | No | Sí |
| Construir gráfica | No | No | No | Sí |
| Renderizar mapa | No | No | No | Sí |
| Manipular DOM | No | No | No | Sí |
| Modificar significado cognitivo | No* | No* | No | No |

\* Las modificaciones semánticas legítimas solamente podrán ocurrir en los componentes específicamente autorizados del procesamiento cognitivo y de materialización, conforme a sus respectivos contratos.

---

## 2.29 Invariantes de frontera

Se establecen los siguientes invariantes adicionales.

### HRRD-B01 — Materialized Input Only

Delivery deberá recibir respuestas materializadas válidas o estructuras explícitamente autorizadas por su contrato.

### HRRD-B02 — No Direct Knowledge Access

Delivery no consultará directamente HKS o HES para completar respuestas.

### HRRD-B03 — No Capability Execution

Delivery no ejecutará capabilities.

### HRRD-B04 — No Presentation Dependency

Delivery no dependerá de tecnologías específicas de presentación.

### HRRD-B05 — Explicit Entry Validation

Toda entrada deberá poder ser validada antes de iniciar la entrega.

### HRRD-B06 — Explicit Exit Result

Toda operación deberá producir un resultado explícito de Delivery.

### HRRD-B07 — Transport Independence

La semántica de Delivery deberá permanecer independiente del mecanismo de transporte.

### HRRD-B08 — Consumer Independence

La arquitectura de Delivery no deberá quedar ligada a un consumidor único.

### HRRD-B09 — Failure Isolation

Los fallos deberán poder atribuirse a la frontera donde realmente ocurrieron.

### HRRD-B10 — Directional Dependency

Las dependencias deberán conservar la dirección arquitectónica establecida.

---

## 2.30 Arquitectura de frontera consolidada

La posición completa de Runtime Response Delivery queda establecida de la siguiente manera:

```text
                     HEYTI INTERNAL DOMAIN

┌────────────────────────────────────────────────────────────┐
│                                                            │
│  HKS / HES                                                 │
│      │                                                     │
│      ▼                                                     │
│  Capability                                                │
│      │                                                     │
│      ▼                                                     │
│  Capability Runtime                                       │
│      │                                                     │
│      ▼                                                     │
│  Materialization                                           │
│      │                                                     │
│      ▼                                                     │
│  HeytiResponseContract                                     │
│      │                                                     │
│  ───────────── DELIVERY ENTRY BOUNDARY ───────────────     │
│      │                                                     │
│      ▼                                                     │
│  Runtime Response Delivery                                 │
│      │                                                     │
│  ───────────── DELIVERY EXIT BOUNDARY ────────────────     │
│      │                                                     │
└──────┼─────────────────────────────────────────────────────┘
       │
       ▼
┌───────────────────────┐
│ Transport / Adapter   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Consumer              │
│ Portal / UI / Service │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Presentation          │
│ Text / Map / Chart    │
│ KPI / Table / Action  │
└───────────────────────┘
```

---

## 2.31 Prueba arquitectónica de independencia

Antes de aceptar una futura implementación de Runtime Response Delivery deberá poder responderse afirmativamente a las siguientes preguntas:

1. ¿Puede probarse Delivery sin levantar una interfaz?
2. ¿Puede probarse Delivery sin abrir un navegador?
3. ¿Puede probarse Delivery utilizando una respuesta materializada conocida?
4. ¿Puede sustituirse el consumidor sin modificar una capability?
5. ¿Puede sustituirse el transporte sin modificar el significado de la respuesta?
6. ¿Puede fallar Presentation sin invalidar una ejecución cognitiva correcta?
7. ¿Puede fallar Delivery sin perder el resultado materializado que originó la operación?
8. ¿Puede reconstruirse qué frontera produjo un fallo?
9. ¿Puede evolucionar el Portal sin introducir dependencias en HEYTI-CORE?
10. ¿Puede HEYTI incorporar nuevos consumidores manteniendo sus contratos internos protegidos?

Si alguna respuesta fuera negativa, deberá revisarse la separación arquitectónica antes de continuar.

---

## 2.32 Declaración arquitectónica del capítulo

Runtime Response Delivery queda formalmente ubicado entre la respuesta materializada y la frontera de consumo.

Su responsabilidad comienza cuando recibe una respuesta elegible para entrega y termina cuando produce un resultado explícito en la frontera de salida.

No ejecuta capacidades.

No consulta conocimiento para completar respuestas.

No interpreta evidencia.

No materializa significado.

No diseña interfaces.

No renderiza mapas.

No construye gráficas.

No manipula el DOM.

Su responsabilidad es más precisa:

> **Recibir una respuesta materializada, verificar que sea entregable, preservar su integridad y trazabilidad, producir una representación válida para su salida y entregar un resultado explícito sin contaminar las fronteras cognitivas ni de presentación de HEYTI.**

Con ello queda establecida la cadena:

```text
HEYTI KNOWS
     ↓
HEYTI EXECUTES
     ↓
HEYTI MATERIALIZES
     ↓
HEYTI DELIVERS
     ↓
CONSUMER PRESENTS
```

Esta separación será obligatoria para el diseño del **Response Delivery Pipeline** que se desarrollará en los capítulos siguientes.

---

**Fin del Capítulo 2**

# Capítulo 3. Principios arquitectónicos de Runtime Response Delivery

## 3.1 Propósito del capítulo

Este capítulo establece los principios arquitectónicos que gobernarán el diseño, implementación, validación y evolución de **HEYTI Runtime Response Delivery (HRRD)**.

Estos principios deberán funcionar como reglas permanentes de decisión.

Cuando existan varias alternativas de implementación técnicamente posibles, deberá preferirse aquella que preserve con mayor fidelidad:

- desacoplamiento;
- trazabilidad;
- integridad;
- auditabilidad;
- claridad contractual;
- independencia de consumidor;
- independencia de transporte;
- honestidad operacional;
- y separación de responsabilidades.

Los principios definidos en este capítulo no describen todavía clases concretas ni estructuras definitivas de código.

Su función es establecer las restricciones arquitectónicas que deberán respetar todas las implementaciones posteriores.

---

## 3.2 Principio HRRD-P01 — Contract First

Toda operación de Delivery deberá estar gobernada por contratos explícitos.

Ninguna respuesta deberá salir del Runtime mediante estructuras implícitas, convenciones circunstanciales o diccionarios arbitrarios cuya semántica dependa del consumidor.

La arquitectura deberá privilegiar:

```text
Explicit Contract
       ↓
Validation
       ↓
Delivery
```

sobre:

```text
Ad-hoc Object
      ↓
"Consumer understands it"
```

El contrato deberá definir de forma inequívoca:

- qué se entrega;
- qué campos son obligatorios;
- qué campos son opcionales;
- qué versión está vigente;
- qué metadatos acompañan la respuesta;
- qué errores pueden producirse;
- y qué resultado genera una operación de entrega.

La regla será:

> **Si una estructura atraviesa la frontera de Delivery, su significado deberá estar definido por contrato.**

---

## 3.3 Principio HRRD-P02 — Semantic Preservation

Delivery deberá preservar la semántica de la respuesta materializada.

La capa podrá modificar la forma técnica necesaria para transportar información, pero nunca su significado cognitivo.

Permitido:

```text
Object
  ↓
Dictionary
  ↓
JSON
```

siempre que el significado permanezca intacto.

No permitido:

```text
"confidence": "low"
        ↓
Delivery decides
        ↓
"confidence": "high"
```

Tampoco será válido:

```text
warning present
      ↓
Delivery
      ↓
warning removed for cleaner UI
```

La preservación semántica deberá considerarse un requisito de integridad.

---

## 3.4 Principio HRRD-P03 — No Cognitive Mutation

Runtime Response Delivery no deberá realizar procesamiento cognitivo.

No podrá:

- inferir conclusiones;
- generar recomendaciones nuevas;
- interpretar tendencias;
- decidir prioridades territoriales;
- recalcular confianza;
- modificar clasificación estratégica;
- agregar evidencia no materializada;
- ni corregir una respuesta con conocimiento adicional.

La regla será:

```text
Delivery transports cognition.
Delivery does not perform cognition.
```

Si se requiere una modificación cognitiva, deberá volver a ejecutarse el componente autorizado correspondiente.

---

## 3.5 Principio HRRD-P04 — Explicit Delivery Boundary

La frontera de Delivery deberá existir conceptualmente y, cuando corresponda, también estructuralmente en el código.

La arquitectura deberá permitir identificar con claridad:

```text
Before Delivery
```

y:

```text
After Delivery
```

Esto permitirá determinar:

- dónde validar;
- dónde instrumentar;
- dónde generar identificadores;
- dónde clasificar errores;
- dónde medir latencia;
- y dónde comienza la responsabilidad del consumidor.

Una frontera difusa generaría ambigüedad operacional.

---

## 3.6 Principio HRRD-P05 — Consumer Independence

La estructura central de Delivery no deberá diseñarse alrededor de un consumidor específico.

Aunque el Portal de AT 27–30 sea uno de los primeros consumidores, la arquitectura deberá soportar otros consumidores sin reconstruir el Core.

Conceptualmente:

```text
                   ┌── Portal
                   │
Delivery Contract ─┼── HEYTI UI
                   │
                   ├── API Client
                   │
                   ├── Internal Tool
                   │
                   └── Future Consumer
```

La semántica central deberá permanecer estable independientemente del consumidor.

---

## 3.7 Principio HRRD-P06 — Transport Independence

Response Delivery deberá ser independiente del mecanismo técnico de transporte.

La entrega no deberá definirse en términos exclusivos de:

- HTTP;
- REST;
- WebSocket;
- archivos;
- pipes;
- colas;
- RPC;
- o llamadas internas.

Estos mecanismos deberán ser tratados como adaptadores o infraestructura de transporte.

La regla será:

```text
Delivery Semantics
        ↓
Transport Adapter
        ↓
Transport Technology
```

y no:

```text
HTTP Semantics
      =
Delivery Semantics
```

---

## 3.8 Principio HRRD-P07 — Deterministic Serialization

La serialización deberá ser consistente y predecible.

Una misma respuesta materializada, bajo:

- la misma versión de contrato;
- la misma política de serialización;
- y el mismo contexto relevante;

deberá producir una representación equivalente.

La arquitectura deberá evitar comportamientos que introduzcan variaciones arbitrarias.

Ejemplo conceptual:

```text
Response A
   ↓
Serializer v1
   ↓
Representation X
```

deberá mantener estabilidad suficiente para:

- pruebas;
- comparación;
- auditoría;
- caché futura;
- diagnóstico;
- y compatibilidad.

---

## 3.9 Principio HRRD-P08 — Traceability by Default

La trazabilidad no deberá considerarse una característica opcional agregada posteriormente.

Deberá formar parte estructural de Delivery.

Toda operación relevante deberá permitir correlacionar, cuando aplique:

```text
request_id
session_id
execution_id
response_id
delivery_id
capability_id
contract_version
timestamp
consumer
```

No todos los campos tendrán necesariamente el mismo nivel de obligatoriedad, pero el modelo deberá soportarlos explícitamente.

La regla será:

> **Una respuesta entregada sin capacidad de reconstruir su origen operativo es una respuesta arquitectónicamente incompleta.**

---

## 3.10 Principio HRRD-P09 — Explicit Failure

Delivery no deberá utilizar fallos silenciosos.

Toda condición anómala deberá producir un resultado explícito o una excepción controlada conforme al contrato.

Queda prohibido:

```python
try:
    ...
except:
    pass
```

como estrategia arquitectónica de Delivery.

Igualmente quedarán prohibidos comportamientos equivalentes que:

- ignoren errores;
- oculten pérdida de campos;
- supriman errores de serialización;
- devuelvan respuestas vacías como si fueran válidas;
- o conviertan errores en éxito aparente.

La regla será:

```text
Failure detected
      ↓
Failure classified
      ↓
Failure represented
      ↓
Failure traceable
```

---

## 3.11 Principio HRRD-P10 — Failure Isolation

Un error de Delivery deberá permanecer atribuido a Delivery.

No deberá contaminar retrospectivamente otros estados correctamente completados.

Ejemplo:

```text
Capability      = SUCCESS
Materialization = SUCCESS
Delivery        = FAILED
```

no deberá convertirse en:

```text
Capability      = FAILED
Materialization = FAILED
Delivery        = FAILED
```

Cada etapa conservará responsabilidad sobre su propio resultado.

Este principio permitirá diagnósticos precisos.

---

## 3.12 Principio HRRD-P11 — No Silent Recovery

Runtime Response Delivery no deberá corregir silenciosamente respuestas inválidas.

Ejemplo incorrecto:

```text
required field missing
        ↓
Delivery invents default
        ↓
SUCCESS
```

Ejemplo correcto:

```text
required field missing
        ↓
Validation Failure
        ↓
Explicit Delivery Error
```

Podrán existir valores predeterminados únicamente cuando hayan sido definidos expresamente por contrato.

Nunca por conveniencia circunstancial de implementación.

---

## 3.13 Principio HRRD-P12 — Fail Before Boundary Crossing

Cuando sea posible, los errores deberán detectarse antes de cruzar la frontera externa.

La secuencia preferida será:

```text
Materialized Response
        ↓
Validate
        ↓
Normalize
        ↓
Serialize
        ↓
Validate Deliverable Representation
        ↓
Cross Boundary
```

y no:

```text
Send partially
      ↓
Discover error
      ↓
Unknown external state
```

Este principio reduce estados indeterminados.

---

## 3.14 Principio HRRD-P13 — Minimal Transformation

Delivery deberá realizar la menor transformación posible.

Cada transformación adicional aumenta el riesgo de:

- pérdida semántica;
- errores;
- incompatibilidad;
- divergencia contractual;
- dificultad de auditoría;
- y acoplamiento.

La arquitectura deberá favorecer:

```text
Materialized Contract
        ↓
Validation
        ↓
Minimal Representation Transformation
        ↓
Delivery
```

sobre pipelines innecesariamente complejos.

---

## 3.15 Principio HRRD-P14 — Representation Is Not Meaning

Una representación técnica no deberá confundirse con la respuesta cognitiva.

Por ejemplo:

```json
{
  "section_id": "1234",
  "winner": "PAN"
}
```

es una representación de información.

No constituye por sí misma toda la semántica si el contrato formal contiene además:

- contexto;
- evidencia;
- advertencias;
- confianza;
- metadatos;
- trazabilidad;
- o limitaciones.

Por ello:

```text
Serialized Payload
      ≠
Complete Cognitive Meaning
```

salvo que el contrato garantice explícitamente equivalencia.

---

## 3.16 Principio HRRD-P15 — Public Contract / Private Internals

Los consumidores deberán depender de contratos públicos.

No de estructuras internas privadas de HEYTI.

Conceptualmente:

```text
HEYTI Internal Models
        │
        ▼
Public Delivery Contract
        │
        ▼
Consumer
```

Esto permitirá modificar componentes internos sin romper consumidores siempre que se preserve compatibilidad contractual.

---

## 3.17 Principio HRRD-P16 — Version Explicitly

Los contratos deberán evolucionar mediante versionado explícito.

La arquitectura deberá impedir que una estructura cambie de significado sin indicación de versión.

Ejemplo permitido:

```text
delivery_contract_version = "1.0"
```

Posteriormente:

```text
delivery_contract_version = "1.1"
```

o:

```text
delivery_contract_version = "2.0"
```

con reglas de compatibilidad definidas.

Queda prohibido:

```text
same version
different semantics
```

---

## 3.18 Principio HRRD-P17 — Backward Compatibility by Policy

La compatibilidad no deberá depender de coincidencias accidentales.

Deberá existir una política explícita que determine:

- qué cambios son compatibles;
- cuáles requieren nueva versión;
- qué campos pueden añadirse;
- qué campos pueden eliminarse;
- qué consumidores continúan soportados;
- y cuándo una versión queda obsoleta.

La definición detallada se desarrollará en capítulos posteriores.

---

## 3.19 Principio HRRD-P18 — Observability Without Semantic Intrusion

Delivery deberá poder ser observado sin modificar el significado de las respuestas.

La instrumentación podrá registrar:

- tiempo de inicio;
- tiempo de finalización;
- duración;
- tamaño de payload;
- estado;
- error;
- adaptador;
- consumidor;
- identificadores de correlación;
- versión contractual.

Pero no deberá alterar la respuesta cognitiva.

Conceptualmente:

```text
Response
   │
   ├──────────────► Consumer
   │
   └──────────────► Observability
```

Observability observa.

No reescribe.

---

## 3.20 Principio HRRD-P19 — Auditability

Una operación de Delivery deberá poder ser examinada posteriormente.

La auditoría deberá permitir responder preguntas tales como:

- ¿qué respuesta se intentó entregar?;
- ¿qué identificador tenía?;
- ¿qué versión contractual utilizó?;
- ¿qué consumidor estaba involucrado?;
- ¿qué representación fue producida?;
- ¿la validación fue satisfactoria?;
- ¿ocurrió algún error?;
- ¿cuándo ocurrió?;
- ¿qué ejecución originó la respuesta?

Esto no exige necesariamente persistir todo el payload en todos los escenarios.

Sí exige que la arquitectura soporte un nivel de evidencia operacional suficiente.

---

## 3.21 Principio HRRD-P20 — Security Context Preservation

Delivery deberá ser capaz de preservar el contexto de seguridad relevante para una operación.

Sin definir todavía un modelo completo de autorización, la arquitectura deberá permitir incorporar información como:

```text
principal_id
consumer_id
session_id
authorization_context
request_origin
```

cuando el sistema lo requiera.

Delivery no deberá eliminar contexto de seguridad necesario para decisiones posteriores.

---

## 3.22 Principio HRRD-P21 — Least Privilege

Response Delivery deberá operar con el mínimo acceso necesario.

No deberá recibir acceso directo a:

- bases de datos completas;
- HKS completo;
- HES completo;
- Capability Registry editable;
- configuración sensible innecesaria;
- o recursos de presentación.

Su función puede ejecutarse utilizando únicamente los recursos requeridos para:

- validar;
- serializar;
- registrar;
- adaptar;
- y entregar.

Este principio reducirá riesgos de arquitectura y seguridad.

---

## 3.23 Principio HRRD-P22 — Idempotency Awareness

La arquitectura deberá contemplar que una operación de entrega pueda ser repetida accidental o deliberadamente.

Aunque la idempotencia concreta dependerá del tipo de consumidor o transporte, Delivery deberá permitir identificar operaciones mediante un `delivery_id` u otros elementos de correlación.

Esto permitirá distinguir:

```text
same delivery retried
```

de:

```text
new delivery
```

La semántica detallada de reintentos se desarrollará posteriormente.

---

## 3.24 Principio HRRD-P23 — No Implicit Retry

Delivery no deberá reintentar automáticamente operaciones fallidas sin una política explícita.

Un reintento puede tener consecuencias diferentes según el consumidor.

Por ejemplo:

```text
Retry GET-like delivery
```

puede ser inocuo.

Pero:

```text
Retry state-changing delivery
```

podría duplicar efectos.

Por ello:

> **Retry es una política explícita, no un reflejo automático.**

---

## 3.25 Principio HRRD-P24 — Delivery Result Is First-Class

El resultado de una entrega deberá ser tratado como un objeto formal.

No deberá reducirse a:

```text
True / False
```

cuando sea necesaria mayor información.

Conceptualmente, un `DeliveryResult` podrá requerir elementos como:

```text
delivery_id
status
timestamp
consumer
adapter
contract_version
error
warnings
metadata
```

La definición exacta se realizará posteriormente.

El principio es:

> **La operación de entrega debe poder explicarse a sí misma.**

---

## 3.26 Principio HRRD-P25 — Consumer Capability Awareness Without Coupling

En el futuro distintos consumidores podrán soportar diferentes capacidades de representación.

Ejemplo:

```text
Consumer A:
- text
- metrics
- tables

Consumer B:
- text
- metrics
- maps
- charts
```

Response Delivery podrá necesitar conocer capacidades declaradas por el consumidor.

Sin embargo, deberá hacerlo mediante contratos o perfiles abstractos.

No mediante lógica del tipo:

```python
if consumer == "portal.html":
    ...
```

La arquitectura deberá favorecer:

```text
Consumer Profile
      ↓
Supported Capabilities
```

sobre identificación rígida por implementación concreta.

---

## 3.27 Principio HRRD-P26 — Presentation Neutrality

Una estructura entregada deberá permanecer neutral respecto a decisiones visuales.

Ejemplo correcto:

```json
{
  "type": "metric",
  "label": "Participación",
  "value": 61.4,
  "unit": "percent"
}
```

Ejemplo incorrecto dentro del Core:

```json
{
  "type": "metric",
  "css_class": "blue-kpi-card",
  "chartjs_dataset_color": "#4A90E2",
  "dom_target": "#panel-right"
}
```

La segunda estructura acopla Delivery a Presentation.

Estas decisiones deberán mantenerse fuera del Core.

---

## 3.28 Principio HRRD-P27 — Structured Before Decorative

Cuando la respuesta contenga información susceptible de representación visual, deberá priorizarse la entrega de datos estructurados.

Por ejemplo:

```text
series
categories
values
units
territorial_reference
geometry_reference
```

antes que instrucciones decorativas.

La UI podrá construir posteriormente:

- gráficas;
- tablas;
- mapas;
- indicadores;
- paneles.

Así se preserva reutilización.

---

## 3.29 Principio HRRD-P28 — Data Provenance Preservation

Cuando una respuesta materializada incluya procedencia de datos, Delivery deberá preservarla.

Ejemplos:

```text
source
source_version
dataset_id
knowledge_version
evidence_id
generated_at
```

Delivery no deberá eliminar procedencia por considerarla innecesaria para presentación.

La UI podrá decidir no mostrarla.

La arquitectura deberá conservarla cuando forme parte del contrato.

---

## 3.30 Principio HRRD-P29 — Honest Incompleteness

Una respuesta incompleta deberá permanecer identificable como incompleta.

Delivery no deberá transformar:

```text
partial response
```

en:

```text
complete response
```

únicamente porque el consumidor prefiera una presentación limpia.

Si el contrato contiene:

```text
completeness = PARTIAL
warnings = [...]
```

estos elementos deberán preservarse.

La regla será:

> **La comodidad visual nunca justifica ocultar incertidumbre o incompletitud.**

---

## 3.31 Principio HRRD-P30 — Null Has Meaning

Los valores ausentes deberán diferenciarse de valores equivalentes a cero, falso o vacío cuando el dominio lo requiera.

Ejemplo:

```text
participation = 0
```

no significa necesariamente lo mismo que:

```text
participation = null
```

El primero puede representar una medición válida.

El segundo puede significar:

- desconocido;
- no disponible;
- no aplicable;
- no calculado;
- o faltante.

Los contratos deberán preservar esta distinción.

---

## 3.32 Principio HRRD-P31 — Explicit Temporal Semantics

Los datos temporales deberán transportar semántica suficiente para evitar ambigüedad.

Cuando sea relevante deberán utilizarse estructuras capaces de distinguir:

- fecha del dato;
- fecha de cálculo;
- fecha de ejecución;
- fecha de materialización;
- fecha de entrega;
- zona horaria;
- versión temporal de conocimiento.

Ejemplo conceptual:

```text
execution_at
materialized_at
delivered_at
data_as_of
```

No deberán mezclarse como un único `timestamp` ambiguo cuando representen hechos diferentes.

---

## 3.33 Principio HRRD-P32 — Stable Identifiers

Los identificadores utilizados para trazabilidad deberán permanecer estables durante el ciclo de una operación.

Por ejemplo:

```text
response_id
```

no deberá cambiar únicamente porque la respuesta fue serializada.

De igual forma:

```text
delivery_id
```

deberá identificar una operación concreta de entrega.

Esto permitirá reconstruir cadenas confiables.

---

## 3.34 Principio HRRD-P33 — Correlation Over Guessing

La relación entre eventos deberá establecerse mediante identificadores explícitos.

No mediante inferencia basada solamente en:

- timestamps;
- orden de logs;
- coincidencia de texto;
- o proximidad temporal.

Preferido:

```text
request_id     = R-001
execution_id   = E-005
response_id    = RESP-009
delivery_id    = D-002
```

y relaciones explícitas entre ellos.

---

## 3.35 Principio HRRD-P34 — Validation at Every Contract Boundary

Cada frontera contractual deberá validar aquello de lo que es responsable.

Conceptualmente:

```text
Materialization
      ↓
Materialization Contract Validation
      ↓
Delivery Entry
      ↓
Delivery Contract Validation
      ↓
Serialization
      ↓
Serializable Representation Validation
      ↓
Adapter
```

Esto no significa duplicar validaciones arbitrariamente.

Significa validar las invariantes propias de cada frontera.

---

## 3.36 Principio HRRD-P35 — No Hidden Global State

Response Delivery deberá evitar depender de estado global mutable no declarado.

Ejemplos problemáticos:

```text
global current_consumer
global current_session
global last_response
global active_contract_version
```

sin contexto explícito.

La información necesaria para una entrega deberá introducirse preferentemente mediante:

- parámetros;
- contexto;
- dependencias explícitas;
- o servicios formalmente definidos.

Esto mejora:

- pruebas;
- concurrencia;
- trazabilidad;
- aislamiento;
- y determinismo.

---

## 3.37 Principio HRRD-P36 — Testability by Construction

La arquitectura deberá permitir probar Response Delivery de manera aislada.

Una prueba no debería requerir obligatoriamente:

- navegador;
- Portal;
- PostgreSQL;
- HKS real;
- HES real;
- capability real;
- conexión de red.

Deberá ser posible utilizar:

```text
Known Materialized Response
        ↓
Delivery Component
        ↓
Known Delivery Result
```

Esto permitirá pruebas deterministas y rápidas.

---

## 3.38 Principio HRRD-P37 — Adapter Substitutability

Los adaptadores deberán poder sustituirse sin alterar el Core.

Ejemplo:

```text
InMemoryAdapter
       ↓
tests
```

y:

```text
HttpAdapter
       ↓
production
```

podrán compartir la misma semántica de Delivery.

Este principio facilitará:

- testing;
- integración;
- migración;
- y evolución tecnológica.

---

## 3.39 Principio HRRD-P38 — No Business Rules in Delivery

Delivery no deberá contener reglas de negocio propias de AT 27–30.

Ejemplos prohibidos:

```text
if margin < 3%:
    mark_as_priority
```

o:

```text
if abstention > threshold:
    recommend_field_action
```

Estas reglas pertenecen al dominio cognitivo o analítico.

Delivery únicamente deberá transportar sus resultados.

---

## 3.40 Principio HRRD-P39 — No Territorial Logic in Delivery

De igual manera, Delivery no deberá interpretar:

- municipios;
- distritos;
- secciones;
- casillas;
- colindancias;
- geometrías;
- cobertura territorial;
- ni jerarquías electorales.

Podrá transportar estructuras que representen estos elementos.

No deberá ejecutar lógica territorial sobre ellas.

---

## 3.41 Principio HRRD-P40 — No UI Workflow Logic

Runtime Response Delivery no deberá controlar navegación visual.

Ejemplos prohibidos:

```text
open module
close previous panel
zoom map
show modal
activate tab
render chart
```

Estas acciones pertenecen a Presentation o a un adaptador especializado de interfaz.

Delivery podrá entregar una acción semántica abstracta si el contrato futuro lo contempla.

Por ejemplo:

```json
{
  "action": "OPEN_TERRITORIAL_CONTEXT",
  "section_id": "1234"
}
```

pero no deberá contener detalles de DOM como:

```json
{
  "onclick": "document.querySelector('#btnAT').click()"
}
```

---

## 3.42 Principio HRRD-P41 — Extensibility Without Core Distortion

La incorporación futura de:

- nuevos consumidores;
- nuevos formatos;
- nuevos transportes;
- nuevas capacidades visuales;
- nuevas integraciones;

deberá realizarse preferentemente mediante extensiones controladas.

No deformando el contrato central cada vez que aparece un requerimiento particular.

La arquitectura deberá favorecer:

```text
Stable Core
   +
Adapters
   +
Profiles
   +
Versioned Contracts
```

---

## 3.43 Principio HRRD-P42 — Simplicity Before Generalization

La arquitectura deberá evitar construir complejidad especulativa.

No deberán implementarse desde v1.0 mecanismos complejos únicamente porque podrían ser útiles en un futuro hipotético.

La regla será:

> **Generalizar únicamente cuando exista una frontera real que deba permanecer estable.**

Esto implica mantener equilibrio entre:

- extensibilidad;
- claridad;
- y simplicidad operacional.

---

## 3.44 Principio HRRD-P43 — Zero Omission Discipline

La disciplina de no omisión deberá aplicarse específicamente a Delivery.

Una entrega no podrá eliminar silenciosamente elementos obligatorios.

Si el contrato materializado contiene:

```text
answer
evidence
warnings
metadata
traceability
```

y todos son obligatorios, el serializer o adaptador no podrá entregar solamente:

```text
answer
```

por considerar el resto innecesario.

La integridad contractual tiene prioridad sobre conveniencia.

---

## 3.45 Principio HRRD-P44 — Delivery Must Be Explainable

Toda operación de entrega deberá poder explicarse mediante una secuencia comprensible.

Por ejemplo:

```text
1. Response received
2. Entry validation passed
3. Delivery context created
4. Response serialized
5. Adapter selected
6. Delivery attempted
7. Consumer accepted response
8. Delivery result generated
```

La arquitectura deberá evitar operaciones opacas cuya lógica resulte difícil de inspeccionar.

---

## 3.46 Principio HRRD-P45 — Delivery Is Infrastructure With Governance

Aunque Delivery tenga naturaleza principalmente operacional, no deberá considerarse infraestructura trivial.

La capa cruza una frontera crítica del sistema.

Por ello deberá estar sometida a:

- contratos;
- versionado;
- pruebas;
- observabilidad;
- auditoría;
- seguridad;
- gobernanza arquitectónica.

La regla será:

> **La salida de HEYTI tiene tanta importancia arquitectónica como su entrada.**

---

## 3.47 Jerarquía de decisión

Cuando dos principios entren en tensión, deberá utilizarse la siguiente prioridad general:

```text
1. Semantic Integrity
2. Contract Integrity
3. Traceability
4. Explicit Failure
5. Security
6. Boundary Separation
7. Compatibility
8. Observability
9. Extensibility
10. Convenience
```

La conveniencia de implementación nunca deberá superar:

- integridad;
- seguridad;
- trazabilidad;
- ni claridad contractual.

---

## 3.48 Ejemplo de aplicación de principios

Supóngase que una futura UI solicita recibir únicamente:

```json
{
  "message": "La sección presenta alta competitividad."
}
```

pero la respuesta materializada contiene:

```text
answer
confidence
evidence
warnings
section_id
knowledge_version
response_id
```

La solución incorrecta sería modificar Delivery para descartar todo salvo `answer`.

La solución arquitectónicamente correcta sería una de las siguientes:

```text
A) entregar el contrato completo
```

o:

```text
B) utilizar un adaptador público autorizado que produzca
   una vista reducida conforme a un contrato explícito
```

Nunca:

```text
discard fields silently
```

Este ejemplo combina:

- Contract First;
- Semantic Preservation;
- Zero Omission;
- Consumer Independence;
- Public Contract / Private Internals.

---

## 3.49 Matriz consolidada de principios

| ID | Principio | Obligación principal |
|---|---|---|
| HRRD-P01 | Contract First | Toda entrega se rige por contrato |
| HRRD-P02 | Semantic Preservation | No alterar significado |
| HRRD-P03 | No Cognitive Mutation | No ejecutar cognición |
| HRRD-P04 | Explicit Boundary | Fronteras identificables |
| HRRD-P05 | Consumer Independence | No acoplarse a consumidor |
| HRRD-P06 | Transport Independence | No acoplar Delivery a transporte |
| HRRD-P07 | Deterministic Serialization | Serialización consistente |
| HRRD-P08 | Traceability by Default | Trazabilidad estructural |
| HRRD-P09 | Explicit Failure | Fallos visibles |
| HRRD-P10 | Failure Isolation | Fallos atribuidos correctamente |
| HRRD-P11 | No Silent Recovery | No corregir silenciosamente |
| HRRD-P12 | Fail Before Boundary | Detectar antes de enviar |
| HRRD-P13 | Minimal Transformation | Transformar lo mínimo |
| HRRD-P14 | Representation Is Not Meaning | No confundir formato con semántica |
| HRRD-P15 | Public Contract / Private Internals | Proteger internals |
| HRRD-P16 | Version Explicitly | Versionar contratos |
| HRRD-P17 | Compatibility by Policy | Compatibilidad gobernada |
| HRRD-P18 | Observable | Instrumentar sin alterar |
| HRRD-P19 | Auditable | Poder reconstruir la operación |
| HRRD-P20 | Security Context | Preservar contexto relevante |
| HRRD-P21 | Least Privilege | Acceso mínimo |
| HRRD-P22 | Idempotency Awareness | Distinguir repetición |
| HRRD-P23 | No Implicit Retry | Reintento explícito |
| HRRD-P24 | First-Class Delivery Result | Resultado formal |
| HRRD-P25 | Consumer Capability Awareness | Capacidades vía contrato |
| HRRD-P26 | Presentation Neutrality | Sin decisiones visuales |
| HRRD-P27 | Structured Before Decorative | Datos antes que decoración |
| HRRD-P28 | Provenance Preservation | Conservar procedencia |
| HRRD-P29 | Honest Incompleteness | No ocultar incompletitud |
| HRRD-P30 | Null Has Meaning | Preservar ausencia semántica |
| HRRD-P31 | Temporal Semantics | Tiempos sin ambigüedad |
| HRRD-P32 | Stable Identifiers | Identidad estable |
| HRRD-P33 | Correlation Over Guessing | Correlación explícita |
| HRRD-P34 | Boundary Validation | Validar cada frontera |
| HRRD-P35 | No Hidden Global State | Estado explícito |
| HRRD-P36 | Testability by Construction | Probar en aislamiento |
| HRRD-P37 | Adapter Substitutability | Adaptadores sustituibles |
| HRRD-P38 | No Business Rules | Sin reglas de negocio |
| HRRD-P39 | No Territorial Logic | Sin interpretación territorial |
| HRRD-P40 | No UI Workflow Logic | Sin navegación visual |
| HRRD-P41 | Extensibility Without Distortion | Extender sin deformar Core |
| HRRD-P42 | Simplicity Before Generalization | Evitar complejidad especulativa |
| HRRD-P43 | Zero Omission Discipline | No omitir contrato |
| HRRD-P44 | Explainable Delivery | Flujo explicable |
| HRRD-P45 | Infrastructure With Governance | Delivery bajo gobierno formal |

---

## 3.50 Prueba de conformidad arquitectónica

Una futura implementación de Response Delivery deberá considerarse no conforme si presenta cualquiera de las siguientes condiciones:

- depende directamente de HTML;
- depende directamente del DOM;
- consulta HKS para completar una respuesta;
- ejecuta una capability;
- modifica confianza o evidencia;
- elimina advertencias;
- inventa valores faltantes;
- oculta errores;
- cambia de contrato sin versionarlo;
- utiliza estado global no controlado;
- mezcla Presentation con Delivery;
- depende exclusivamente de HTTP;
- carece de resultado explícito;
- carece de trazabilidad;
- o no puede probarse independientemente de la UI.

La presencia de cualquiera de estas condiciones deberá activar revisión arquitectónica.

---

## 3.51 Declaración arquitectónica del capítulo

Los principios establecidos en este capítulo definen la conducta esperada de Runtime Response Delivery.

Su objetivo no es convertir Delivery en una capa compleja.

Su objetivo es impedir que una frontera aparentemente sencilla se convierta con el tiempo en un punto de mezcla entre:

- cognición;
- contratos;
- transporte;
- presentación;
- estado;
- reglas de negocio;
- y detalles tecnológicos.

La regla consolidada será:

> **Runtime Response Delivery deberá ser contractualmente explícito, semánticamente conservador, operacionalmente trazable, tecnológicamente desacoplado y visualmente neutral.**

Sobre estos principios podrá construirse el pipeline operacional de entrega sin comprometer la arquitectura general de HEYTI.

---

**Fin del Capítulo 3**

# Capítulo 4. Modelo conceptual de Runtime Response Delivery

## 4.1 Propósito del capítulo

Este capítulo define el modelo conceptual de **HEYTI Runtime Response Delivery (HRRD)**.

Mientras los capítulos anteriores establecieron:

- propósito;
- alcance;
- fronteras;
- responsabilidades;
- y principios arquitectónicos;

este capítulo introduce las entidades conceptuales que deberán existir para representar formalmente una operación de entrega.

El objetivo es responder con precisión:

> ¿Qué elementos intervienen en una entrega?

> ¿Qué relación existe entre una respuesta materializada, un contexto de entrega, un consumidor, un adaptador y un resultado de entrega?

> ¿Qué entidades deben distinguirse para evitar mezclar identidad, transporte, trazabilidad y presentación?

El modelo definido aquí servirá como base para los contratos y estructuras de implementación posteriores.

---

## 4.2 Entidades conceptuales principales

Runtime Response Delivery deberá modelarse, como mínimo, mediante las siguientes entidades conceptuales:

```text
MaterializedResponse
DeliveryRequest
DeliveryContext
DeliveryTarget
ConsumerProfile
DeliveryAdapter
DeliveryPayload
DeliveryResult
DeliveryError
DeliveryTrace
```

Estas entidades no implican todavía nombres definitivos de clases.

Representan responsabilidades arquitectónicas distintas.

---

## 4.3 MaterializedResponse

`MaterializedResponse` representa la respuesta producida por la etapa de materialización y aceptada como entrada potencial a Delivery.

Conceptualmente:

```text
MaterializedResponse
├── response_id
├── request_id
├── execution_id
├── capability_id
├── contract_version
├── status
├── content
├── evidence
├── warnings
├── metadata
└── traceability
```

La estructura exacta dependerá del `HeytiResponseContract` vigente.

Runtime Response Delivery no deberá modificar la semántica de esta entidad.

---

## 4.4 DeliveryRequest

`DeliveryRequest` representa la intención explícita de entregar una respuesta.

No deberá confundirse con la solicitud original del usuario.

La solicitud del usuario responde:

```text
"What does the user want?"
```

DeliveryRequest responde:

```text
"What response must be delivered, to whom, under what delivery context?"
```

Conceptualmente:

```text
DeliveryRequest
├── delivery_id
├── response
├── target
├── consumer_profile
├── delivery_context
├── policy
└── requested_at
```

La creación de un DeliveryRequest permite separar:

```text
response exists
```

de:

```text
response must now be delivered
```

---

## 4.5 Diferencia entre Request y DeliveryRequest

Es fundamental distinguir:

```text
UserRequest
```

de:

```text
DeliveryRequest
```

El primero inicia una operación cognitiva.

El segundo inicia una operación de entrega.

Conceptualmente:

```text
UserRequest
    │
    ▼
Runtime Execution
    │
    ▼
MaterializedResponse
    │
    ▼
DeliveryRequest
    │
    ▼
Delivery Operation
```

Esto permite que una misma respuesta pueda, en escenarios futuros, ser entregada:

- una vez;
- varias veces;
- a distintos consumidores;
- por diferentes adaptadores;
- o bajo diferentes políticas.

Sin necesidad de volver a ejecutar la capability.

---

## 4.6 DeliveryContext

`DeliveryContext` representa la información operacional necesaria para ejecutar una entrega.

Podrá contener, cuando corresponda:

```text
request_id
session_id
execution_id
response_id
delivery_id
consumer_id
principal_id
correlation_id
requested_at
timezone
environment
```

El contexto no deberá contener información arbitraria.

Su propósito será proporcionar aquello que la operación necesita para:

- correlación;
- seguridad;
- observabilidad;
- versionado;
- diagnóstico;
- y auditoría.

---

## 4.7 Contexto explícito

La arquitectura deberá evitar depender de contexto implícito.

Incorrecto:

```text
"Use whichever session is currently active"
```

Correcto:

```text
delivery_context.session_id
```

Incorrecto:

```text
"Use the current consumer from a global variable"
```

Correcto:

```text
delivery_context.consumer_id
```

La regla será:

> **Si una decisión de Delivery depende de contexto, dicho contexto deberá ser explícito.**

---

## 4.8 DeliveryTarget

`DeliveryTarget` representa el destino lógico de la operación.

No deberá confundirse necesariamente con una dirección técnica.

Un Target podría representar:

```text
Portal
HEYTI_UI
InternalService
TestingConsumer
FutureIntegration
```

mientras que el mecanismo técnico podría ser:

```text
HTTP endpoint
internal function
message channel
WebSocket
```

La separación será:

```text
Target = logical destination
Transport = technical mechanism
```

---

## 4.9 ConsumerProfile

`ConsumerProfile` representa las capacidades declaradas por un consumidor.

Podrá describir elementos como:

```text
consumer_id
supported_contract_versions
supported_content_types
supports_text
supports_metrics
supports_tables
supports_maps
supports_charts
supports_actions
supports_streaming
```

La finalidad no será imponer UI.

Será permitir que Delivery conozca qué representaciones públicas puede aceptar un consumidor.

---

## 4.10 ConsumerProfile no es configuración visual

ConsumerProfile no deberá contener:

```text
colors
css
fonts
coordinates
DOM selectors
Chart.js config
Leaflet layer config
```

Ejemplo correcto:

```text
supports_maps = true
```

Ejemplo incorrecto:

```text
map_library = "Leaflet"
map_container = "#main-map"
```

El primero expresa capacidad.

El segundo expresa implementación visual.

---

## 4.11 DeliveryAdapter

`DeliveryAdapter` representa el componente encargado de cruzar la frontera técnica correspondiente.

Conceptualmente:

```text
Delivery Core
     │
     ▼
DeliveryAdapter
     │
     ▼
External Boundary
```

Posibles adaptadores futuros:

```text
InMemoryDeliveryAdapter
HttpDeliveryAdapter
WebSocketDeliveryAdapter
InternalServiceAdapter
```

El adaptador deberá implementar una interfaz estable.

No deberá definir la semántica cognitiva de la respuesta.

---

## 4.12 Responsabilidad del DeliveryAdapter

El adaptador podrá ser responsable de:

- establecer comunicación;
- enviar payload;
- recibir confirmación técnica;
- mapear errores de infraestructura;
- reportar resultado de transporte;
- registrar información técnica relevante.

No deberá:

- completar una respuesta;
- reinterpretar datos;
- modificar evidencia;
- decidir prioridades;
- ni construir contenido cognitivo.

---

## 4.13 DeliveryPayload

`DeliveryPayload` representa la forma entregable producida después de validar y serializar la respuesta.

Conceptualmente:

```text
MaterializedResponse
        │
        ▼
Delivery Serialization
        │
        ▼
DeliveryPayload
```

El payload podrá ser:

```text
dict
JSON
bytes
message object
```

dependiendo del adaptador.

Sin embargo, su estructura deberá permanecer gobernada por contrato.

---

## 4.14 Payload no es respuesta original

Aunque puedan ser equivalentes en contenido, deberán distinguirse conceptualmente:

```text
MaterializedResponse
```

y:

```text
DeliveryPayload
```

La primera pertenece al dominio interno de respuesta.

El segundo pertenece al dominio de entrega.

Esta distinción permite:

- serialización;
- adaptación;
- versionado;
- validación;
- instrumentación;
- y pruebas;

sin contaminar el contrato interno.

---

## 4.15 DeliveryResult

`DeliveryResult` representa el resultado formal de una operación de Delivery.

Deberá ser una entidad de primera clase.

Conceptualmente podrá contener:

```text
delivery_id
response_id
status
target
adapter
started_at
completed_at
duration_ms
contract_version
payload_size
warnings
error
metadata
```

El resultado deberá permitir distinguir claramente:

```text
SUCCESS
FAILED
REJECTED
PARTIAL
```

si esos estados son finalmente adoptados por el contrato.

---

## 4.16 Resultado de entrega vs resultado cognitivo

La arquitectura deberá distinguir:

```text
Cognitive Result
```

de:

```text
Delivery Result
```

Por ejemplo:

```text
Cognitive Result = SUCCESS
Delivery Result  = FAILED
```

es un estado completamente válido.

También:

```text
Cognitive Result = SUCCESS
Delivery Result  = SUCCESS
```

La existencia de `DeliveryResult` impide reducir toda la operación a un único estado genérico.

---

## 4.17 DeliveryError

`DeliveryError` representará un fallo propio de la etapa de entrega.

Los errores deberán poder clasificarse.

Ejemplos conceptuales:

```text
DELIVERY_VALIDATION_ERROR
DELIVERY_SERIALIZATION_ERROR
DELIVERY_ADAPTER_ERROR
DELIVERY_TARGET_UNAVAILABLE
DELIVERY_CONTRACT_MISMATCH
DELIVERY_UNSUPPORTED_CONSUMER
DELIVERY_TIMEOUT
DELIVERY_INTERNAL_ERROR
```

La taxonomía definitiva será desarrollada posteriormente.

---

## 4.18 Error estructurado

Un DeliveryError debería poder expresar información como:

```text
code
message
category
recoverable
delivery_id
response_id
adapter
details
timestamp
```

La información sensible deberá tratarse conforme a políticas de seguridad.

No todos los detalles internos deberán salir hacia el consumidor.

---

## 4.19 DeliveryTrace

`DeliveryTrace` representa la información necesaria para reconstruir una operación.

Conceptualmente:

```text
DeliveryTrace
├── request_id
├── session_id
├── execution_id
├── response_id
├── delivery_id
├── consumer_id
├── adapter_id
├── contract_version
├── started_at
├── completed_at
└── status
```

DeliveryTrace podrá estar:

- integrado en DeliveryResult;
- asociado mediante metadata;
- o representado por infraestructura de observabilidad.

La decisión concreta se establecerá posteriormente.

---

## 4.20 DeliveryPolicy

La arquitectura deberá contemplar una entidad conceptual de política de entrega.

`DeliveryPolicy` podrá controlar aspectos como:

```text
validation_mode
serialization_policy
retry_policy
timeout_policy
compatibility_policy
logging_policy
audit_policy
```

No todos deberán existir desde v1.0.

Sin embargo, el modelo deberá evitar dispersar estas decisiones mediante condiciones arbitrarias dentro del código.

---

## 4.21 Política explícita vs comportamiento oculto

Incorrecto:

```python
if error:
    retry_three_times()
```

sin política definida.

Correcto conceptualmente:

```text
DeliveryPolicy
    retry = NONE
```

o:

```text
DeliveryPolicy
    retry = SAFE_ONCE
```

si en el futuro se aprueba.

La regla será:

> **El comportamiento operacional relevante deberá estar gobernado por política, no por sorpresa.**

---

## 4.22 Relación entre entidades

El modelo conceptual completo podrá representarse como:

```text
MaterializedResponse
        │
        ▼
DeliveryRequest
        │
        ├──────────────► DeliveryContext
        │
        ├──────────────► DeliveryTarget
        │
        ├──────────────► ConsumerProfile
        │
        └──────────────► DeliveryPolicy
        │
        ▼
Entry Validation
        │
        ▼
Serialization
        │
        ▼
DeliveryPayload
        │
        ▼
DeliveryAdapter
        │
        ▼
Boundary Crossing
        │
        ▼
DeliveryResult
        │
        ├──────────────► DeliveryTrace
        │
        └──────────────► DeliveryError
```

Esta estructura será la base del futuro Response Delivery Pipeline.

---

## 4.23 Identidad de la respuesta

`response_id` deberá identificar la respuesta materializada.

Una operación de entrega no deberá crear una nueva identidad cognitiva para la misma respuesta.

Ejemplo:

```text
response_id = RESP-001
```

La respuesta podrá entregarse dos veces:

```text
delivery_id = DEL-001
delivery_id = DEL-002
```

pero ambas operaciones podrán referenciar:

```text
response_id = RESP-001
```

Esta distinción es fundamental.

---

## 4.24 Identidad de la entrega

Cada operación de entrega deberá disponer de identidad propia cuando el contrato así lo requiera.

Conceptualmente:

```text
Response RESP-001
     │
     ├── Delivery DEL-001 → Portal
     │
     └── Delivery DEL-002 → Internal Service
```

Esto permitirá conocer:

- cuál entrega falló;
- cuál tuvo éxito;
- cuál fue reintentada;
- y qué consumidor recibió cada una.

---

## 4.25 Correlation ID

Además de identificadores específicos, la arquitectura podrá utilizar un `correlation_id` para relacionar múltiples eventos pertenecientes al mismo flujo operacional.

Ejemplo:

```text
correlation_id = CORR-9001
```

podría estar asociado con:

```text
request_id
execution_id
response_id
delivery_id
```

Su incorporación definitiva dependerá de la arquitectura global de observabilidad.

---

## 4.26 Session ID

Cuando una operación ocurra dentro de una sesión HEYTI, Delivery deberá preservar el `session_id` correspondiente.

Esto permitirá reconstruir:

```text
Session
  │
  ├── Request 1
  │      └── Response
  │             └── Delivery
  │
  └── Request 2
         └── Response
                └── Delivery
```

Delivery no deberá crear sesiones nuevas salvo que una arquitectura posterior lo establezca explícitamente.

---

## 4.27 Consumer ID

El consumidor deberá poder identificarse mediante una identidad lógica estable.

Ejemplo:

```text
consumer_id = "AT_PORTAL"
```

es preferible a:

```text
consumer_id = "portal.html"
```

porque el primero representa responsabilidad lógica.

El segundo representa un archivo concreto de implementación.

La arquitectura deberá favorecer identidades semánticas.

---

## 4.28 Adapter ID

Los adaptadores también deberán poder identificarse.

Ejemplos conceptuales:

```text
IN_MEMORY
HTTP_JSON
WEBSOCKET_JSON
INTERNAL_CALL
```

Esto permitirá instrumentación y diagnóstico sin acoplar el contrato cognitivo al mecanismo.

---

## 4.29 Contract Version

El modelo deberá conservar explícitamente la versión contractual relevante.

Podrán existir múltiples versiones:

```text
response_contract_version
delivery_contract_version
payload_schema_version
```

No necesariamente deberán aparecer las tres desde el inicio.

Pero deberán distinguirse cuando tengan semánticas diferentes.

---

## 4.30 Temporalidad de una operación

Una entrega deberá modelar el tiempo de manera no ambigua.

Conceptualmente:

```text
requested_at
started_at
serialized_at
delivered_at
completed_at
```

La implementación v1.0 podrá reducir estos campos si no todos son necesarios.

Sin embargo, deberá quedar claro qué representa cada timestamp utilizado.

---

## 4.31 Modelo conceptual de estados

Una operación de Delivery podrá atravesar estados semejantes a:

```text
CREATED
   ↓
VALIDATING
   ↓
VALIDATED
   ↓
SERIALIZING
   ↓
READY
   ↓
DELIVERING
   ↓
DELIVERED
```

o terminar en:

```text
REJECTED
FAILED
```

Este modelo es conceptual.

La máquina de estados definitiva será establecida en capítulos posteriores.

---

## 4.32 Estado terminal

Los estados terminales deberán ser explícitos.

Conceptualmente:

```text
DELIVERED
REJECTED
FAILED
```

Un resultado no deberá permanecer ambiguamente en:

```text
PROCESSING
```

si la operación ya terminó.

La determinación explícita del estado final será esencial para trazabilidad.

---

## 4.33 Diferencia entre REJECTED y FAILED

La arquitectura deberá considerar la distinción entre:

```text
REJECTED
```

y:

```text
FAILED
```

`REJECTED` podría representar una operación que no cruzó la frontera porque no cumplió precondiciones.

Ejemplo:

```text
unsupported contract version
```

`FAILED` podría representar una operación válida que comenzó pero experimentó un error operacional.

Ejemplo:

```text
adapter connection failure
```

Esta distinción mejora diagnóstico y auditoría.

---

## 4.34 Resultado parcial

La arquitectura deberá decidir explícitamente si v1.0 soportará:

```text
PARTIAL
```

como estado de Delivery.

Este estado podría ser necesario en escenarios donde:

- parte del payload fue entregado;
- múltiples targets tuvieron resultados diferentes;
- o un consumidor aceptó parcialmente una estructura.

Sin embargo, deberá evitarse introducir `PARTIAL` sin semántica precisa.

Mientras no se defina formalmente:

> **La implementación deberá preferir estados inequívocos.**

---

## 4.35 Delivery Envelope

La arquitectura podrá utilizar conceptualmente un **Delivery Envelope**.

El envelope encapsularía:

```text
header
payload
metadata
trace
```

Ejemplo conceptual:

```json
{
  "delivery": {
    "delivery_id": "DEL-001",
    "contract_version": "1.0"
  },
  "response": {
    "...": "..."
  },
  "trace": {
    "request_id": "REQ-001",
    "execution_id": "EXE-001"
  }
}
```

La estructura definitiva deberá definirse por contrato.

---

## 4.36 Razón del Delivery Envelope

Un envelope permite separar:

```text
Delivery Metadata
```

de:

```text
Response Content
```

Esto evita modificar el contenido cognitivo únicamente para agregar información operacional.

Conceptualmente:

```text
DeliveryEnvelope
├── delivery metadata
├── traceability
└── materialized response
```

Así, la respuesta conserva su identidad semántica.

---

## 4.37 No duplicación semántica

El Delivery Envelope no deberá duplicar arbitrariamente campos de la respuesta.

Por ejemplo, si `response_id` ya se encuentra en un lugar contractual claro, no deberá repetirse en múltiples niveles salvo necesidad explícita.

La duplicación crea riesgos de divergencia:

```text
response.response_id = RESP-001
delivery.response_id = RESP-002
```

La arquitectura deberá privilegiar una única fuente de verdad.

---

## 4.38 Snapshot de Delivery

La arquitectura podrá requerir que ciertos metadatos se congelen al iniciar una operación.

Ejemplo:

```text
consumer_profile_version
contract_version
adapter_id
```

Si estos valores cambian durante la operación, podría volverse imposible reconstruir exactamente qué condiciones gobernaron la entrega.

Por ello deberá evaluarse el uso de snapshots inmutables de contexto.

---

## 4.39 Inmutabilidad preferente

Las estructuras críticas de Delivery deberán favorecer inmutabilidad o mutación controlada.

Especialmente:

```text
response identity
delivery identity
contract version
trace identifiers
consumer identity
```

no deberán cambiar arbitrariamente durante una operación.

Esto reduce errores de concurrencia y auditoría.

---

## 4.40 DeliveryContext vs Metadata

Debe distinguirse:

```text
DeliveryContext
```

de:

```text
Metadata
```

DeliveryContext contiene información necesaria para ejecutar la operación.

Metadata contiene información descriptiva o complementaria.

Ejemplo:

```text
session_id
```

puede formar parte del contexto.

Mientras que:

```text
deployment_name = "production"
```

podría ser metadata.

La frontera exacta deberá mantenerse clara.

---

## 4.41 Metadata extensible

La arquitectura podrá permitir metadata extensible.

Sin embargo, metadata no deberá convertirse en una vía para evadir contratos.

Incorrecto:

```json
{
  "metadata": {
    "everything_we_did_not_model": "..."
  }
}
```

La información estructuralmente importante deberá poseer campos formales.

Metadata deberá reservarse para datos secundarios o extensibles.

---

## 4.42 DeliveryReceipt

En ciertos transportes podrá existir un concepto de confirmación o recibo.

Conceptualmente:

```text
DeliveryAdapter
      │
      ▼
Consumer
      │
      ▼
DeliveryReceipt
```

Un receipt podría indicar:

```text
accepted
received_at
remote_reference
```

No todos los adaptadores necesitarán este concepto.

Por ello deberá permanecer opcional y abstracto.

---

## 4.43 Receipt no es presentación

Una confirmación de recepción no indica que la UI haya mostrado correctamente la respuesta.

Ejemplo:

```text
DeliveryReceipt = ACCEPTED
```

significa que el consumidor aceptó la entrega.

No significa necesariamente:

```text
Chart rendered successfully
```

La frontera con Presentation continúa siendo independiente.

---

## 4.44 Modelo de consumidor único

En v1.0 deberá preferirse inicialmente el caso simple:

```text
1 DeliveryRequest
      ↓
1 Target
      ↓
1 Adapter
      ↓
1 DeliveryResult
```

Esto reduce complejidad.

La distribución a múltiples consumidores podrá incorporarse posteriormente mediante una capa explícita si se requiere.

---

## 4.45 Prohibición de fan-out implícito

Delivery no deberá asumir silenciosamente que una respuesta debe enviarse a múltiples destinos.

Incorrecto:

```text
deliver(response)
    automatically sends to:
    Portal
    logs
    websocket
    analytics
```

Correcto:

```text
explicit delivery operation
```

para cada destino relevante, o una política de fan-out formal.

El comportamiento deberá ser visible y auditable.

---

## 4.46 Modelo conceptual de una operación completa

Una operación típica se representará así:

```text
1. MaterializedResponse exists

2. DeliveryRequest is created
      │
      ├── Target
      ├── ConsumerProfile
      ├── DeliveryContext
      └── DeliveryPolicy

3. Entry validation

4. DeliveryPayload is produced

5. DeliveryAdapter is selected

6. Boundary crossing occurs

7. Adapter returns technical result

8. DeliveryResult is generated

9. DeliveryTrace is completed
```

Esta secuencia servirá como base del pipeline formal.

---

## 4.47 Ejemplo conceptual

Supóngase una respuesta:

```text
response_id = RESP-120
section_id = 1481
capability_id = describe_section
status = SUCCESS
```

La operación de entrega podría conceptualizarse como:

```text
DeliveryRequest
├── delivery_id = DEL-331
├── response_id = RESP-120
├── consumer_id = AT_PORTAL
├── adapter_id = HTTP_JSON
└── contract_version = 1.0
```

Después:

```text
Validation = SUCCESS
Serialization = SUCCESS
Adapter = SUCCESS
```

Resultado:

```text
DeliveryResult
├── delivery_id = DEL-331
├── response_id = RESP-120
├── status = DELIVERED
└── consumer_id = AT_PORTAL
```

La respuesta cognitiva conserva:

```text
response_id = RESP-120
```

La operación de entrega posee:

```text
delivery_id = DEL-331
```

Ambas identidades permanecen separadas.

---

## 4.48 Ejemplo con fallo

Supóngase:

```text
response_id = RESP-121
```

La respuesta es válida.

Se crea:

```text
delivery_id = DEL-332
```

pero ocurre:

```text
SerializationError
```

El estado correcto será:

```text
MaterializedResponse = VALID
DeliveryRequest      = VALID
DeliveryResult       = FAILED
DeliveryError        = DELIVERY_SERIALIZATION_ERROR
```

No deberá alterarse:

```text
response.status
```

para convertirlo en error cognitivo.

---

## 4.49 Modelo conceptual consolidado

```text
┌──────────────────────────────┐
│ MaterializedResponse         │
│                              │
│ response_id                  │
│ content                      │
│ evidence                     │
│ warnings                     │
│ metadata                     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DeliveryRequest              │
│                              │
│ delivery_id                  │
│ target                       │
│ context                      │
│ consumer_profile             │
│ policy                       │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Delivery Validation          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DeliveryPayload              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DeliveryAdapter              │
└──────────────┬───────────────┘
               │
               ▼
       DELIVERY BOUNDARY
               │
               ▼
┌──────────────────────────────┐
│ Consumer                     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DeliveryResult               │
│                              │
│ status                       │
│ trace                        │
│ error                        │
│ metadata                     │
└──────────────────────────────┘
```

---

## 4.50 Invariantes del modelo conceptual

Se establecen los siguientes invariantes.

### HRRD-M01 — Response Identity

`response_id` identifica una respuesta materializada y no una operación de entrega.

### HRRD-M02 — Delivery Identity

`delivery_id` identifica una operación concreta de entrega.

### HRRD-M03 — Explicit Target

Toda entrega deberá poseer un destino lógico explícito.

### HRRD-M04 — Explicit Context

El contexto necesario para la entrega deberá declararse explícitamente.

### HRRD-M05 — Adapter Separation

El mecanismo técnico deberá permanecer encapsulado por un adaptador.

### HRRD-M06 — Payload Distinction

La representación entregable deberá distinguirse conceptualmente de la respuesta interna.

### HRRD-M07 — First-Class Result

Toda operación deberá producir un DeliveryResult.

### HRRD-M08 — Error Ownership

Los errores propios de Delivery deberán representarse como errores de Delivery.

### HRRD-M09 — Traceability

Las relaciones entre request, execution, response y delivery deberán conservarse explícitamente.

### HRRD-M10 — Presentation Exclusion

Ninguna entidad central de este modelo deberá requerir conocimiento de implementación visual.

---

## 4.51 Prueba de consistencia del modelo

Una implementación será consistente con este modelo si puede responder claramente:

1. ¿Qué respuesta se está entregando?
2. ¿Cuál es su `response_id`?
3. ¿Cuál es la operación concreta de entrega?
4. ¿Cuál es su `delivery_id`?
5. ¿A qué consumidor se dirige?
6. ¿Qué adaptador se utilizó?
7. ¿Qué contexto gobernó la operación?
8. ¿Qué payload se generó?
9. ¿Cuál fue el resultado?
10. ¿Dónde ocurrió un eventual error?

Si estas preguntas no pueden responderse sin ambigüedad, el modelo de implementación deberá revisarse.

---

## 4.52 Declaración arquitectónica del capítulo

Runtime Response Delivery deberá construirse sobre un modelo explícito de entidades y relaciones.

Una respuesta materializada no es una entrega.

Un consumidor no es un transporte.

Un adaptador no es una capability.

Un payload no es una interfaz visual.

Un error de Delivery no es un error cognitivo.

Y una operación de entrega no debe perderse dentro de una cadena de funciones sin identidad propia.

La regla arquitectónica consolidada queda establecida como:

> **Toda entrega HEYTI deberá ser una operación identificable, contextualizada, contractualmente gobernada, ejecutada mediante una frontera explícita y capaz de producir un resultado trazable independiente de la respuesta cognitiva que la originó.**

Este modelo conceptual permitirá definir a continuación el flujo operacional completo de Runtime Response Delivery.

---

**Fin del Capítulo 4**

# Capítulo 5. Runtime Response Delivery Pipeline

## 5.1 Propósito del capítulo

Este capítulo define el **Runtime Response Delivery Pipeline**, es decir, la secuencia operacional mediante la cual una respuesta materializada es transformada en una entrega válida, trazable y consumible.

Los capítulos anteriores establecieron:

- propósito;
- fronteras;
- principios;
- entidades conceptuales;
- y relaciones.

Este capítulo convierte esos elementos en un flujo operativo explícito.

El objetivo es responder:

> ¿Qué pasos debe recorrer una respuesta desde que entra a Delivery hasta que abandona la frontera del Runtime?

> ¿En qué orden deben ocurrir las validaciones?

> ¿Dónde se genera el payload?

> ¿Dónde interviene el adaptador?

> ¿Cómo se produce el resultado final?

El pipeline deberá ser suficientemente claro para poder ser:

- implementado;
- probado;
- observado;
- auditado;
- y evolucionado sin ambigüedad.

---

## 5.2 Definición del pipeline

Se define **Runtime Response Delivery Pipeline** como la secuencia controlada de etapas responsables de:

1. recibir una respuesta materializada;
2. crear una operación de entrega;
3. validar sus precondiciones;
4. resolver contexto y destino;
5. validar compatibilidad;
6. construir la representación entregable;
7. serializar;
8. seleccionar un adaptador;
9. ejecutar la entrega;
10. interpretar el resultado técnico;
11. producir un `DeliveryResult`;
12. completar trazabilidad y observabilidad.

Conceptualmente:

```text
MaterializedResponse
        │
        ▼
Create DeliveryRequest
        │
        ▼
Entry Validation
        │
        ▼
Context Validation
        │
        ▼
Consumer Compatibility
        │
        ▼
Build Delivery Envelope
        │
        ▼
Serialization
        │
        ▼
Payload Validation
        │
        ▼
Adapter Resolution
        │
        ▼
Delivery Execution
        │
        ▼
Technical Result
        │
        ▼
DeliveryResult
        │
        ▼
Trace / Observability
```

---

## 5.3 Regla de secuencia

Las etapas del pipeline deberán ejecutarse en orden lógico.

No deberá ejecutarse transporte antes de:

- validar la respuesta;
- validar el contrato;
- verificar compatibilidad;
- producir un payload válido.

Por tanto, queda prohibido un patrón como:

```text
send first
validate later
```

La regla será:

> **Validate before crossing the boundary.**

---

## 5.4 Etapa 1 — Receipt

La primera etapa consiste en recibir la respuesta materializada.

Entrada conceptual:

```text
MaterializedResponse
```

La operación deberá registrar al menos:

```text
response_id
received_at
```

cuando dichos campos estén disponibles.

En esta etapa todavía no se considera que la entrega sea válida.

Únicamente existe una respuesta candidata a Delivery.

---

## 5.5 Etapa 2 — DeliveryRequest Creation

A partir de la respuesta deberá crearse una operación explícita de entrega.

Conceptualmente:

```text
DeliveryRequest
```

deberá asociar:

```text
response
target
consumer
context
policy
delivery_id
```

La generación de `delivery_id` deberá producir una identidad única para esa operación.

---

## 5.6 Momento de creación de delivery_id

El `delivery_id` deberá generarse antes de cualquier operación relevante de Delivery que necesite trazabilidad.

Preferentemente:

```text
Receive Response
      ↓
Generate delivery_id
      ↓
Begin Delivery Pipeline
```

Esto permite registrar incluso operaciones rechazadas antes de cruzar la frontera.

Ejemplo:

```text
delivery_id = DEL-450
status      = REJECTED
reason      = unsupported_contract_version
```

La operación continúa siendo auditable aunque nunca haya intentado transporte.

---

## 5.7 Etapa 3 — Entry Validation

La respuesta deberá superar validación de entrada.

La validación deberá comprobar, como mínimo, según contrato:

- respuesta no nula;
- estructura reconocida;
- `response_id`;
- versión del contrato;
- estado válido;
- contenido obligatorio;
- metadatos obligatorios;
- trazabilidad mínima.

Conceptualmente:

```text
MaterializedResponse
        │
        ▼
Entry Validator
        │
   ┌────┴────┐
   │         │
 VALID     INVALID
   │         │
   ▼         ▼
continue   REJECTED
```

---

## 5.8 Rechazo en Entry Validation

Una respuesta que no cumpla las precondiciones no deberá ser reparada silenciosamente.

Resultado conceptual:

```text
DeliveryResult
├── status = REJECTED
├── error.code = DELIVERY_VALIDATION_ERROR
└── delivery_id = ...
```

La respuesta original deberá permanecer intacta.

---

## 5.9 Etapa 4 — DeliveryContext Resolution

El contexto requerido deberá estar disponible antes de continuar.

Podrán validarse elementos como:

```text
session_id
consumer_id
principal_id
correlation_id
environment
request_origin
```

No todos serán obligatorios en v1.0.

La obligatoriedad dependerá de los contratos y políticas.

---

## 5.10 Context Resolution no es inferencia arbitraria

Delivery no deberá deducir contexto mediante heurísticas frágiles.

Incorrecto:

```text
take last active session
```

Correcto:

```text
DeliveryContext.session_id
```

La resolución podrá utilizar servicios autorizados cuando corresponda, pero deberá permanecer explícita y trazable.

---

## 5.11 Etapa 5 — DeliveryTarget Validation

El destino lógico deberá ser válido.

Deberá comprobarse, cuando aplique:

```text
target exists
consumer exists
target is enabled
target is authorized
adapter mapping exists
```

Un target desconocido deberá provocar rechazo explícito.

Ejemplo:

```text
DELIVERY_UNSUPPORTED_CONSUMER
```

o una clasificación equivalente definida posteriormente.

---

## 5.12 Etapa 6 — Consumer Compatibility Validation

Antes de producir una representación específica deberá comprobarse la compatibilidad contractual del consumidor.

Podrán verificarse:

```text
response_contract_version
delivery_contract_version
supported_content_types
consumer_profile_version
required_features
```

Ejemplo:

```text
Response requires:
- text
- metrics
- map_reference

Consumer supports:
- text
- metrics
- map_reference

Compatibility = VALID
```

---

## 5.13 Incompatibilidad

Si el consumidor no soporta un elemento obligatorio de la respuesta, Delivery no deberá eliminarlo automáticamente.

Incorrecto:

```text
consumer does not support evidence
       ↓
remove evidence
       ↓
send
```

Correcto:

```text
consumer incompatibility
       ↓
explicit policy evaluation
       ↓
reject or use authorized adapter contract
```

La compatibilidad deberá estar gobernada por contrato.

---

## 5.14 Etapa 7 — Delivery Envelope Construction

Después de validar entrada, contexto y compatibilidad podrá construirse el **Delivery Envelope**.

Conceptualmente:

```text
DeliveryEnvelope
├── delivery
├── response
├── trace
└── metadata
```

Ejemplo:

```json
{
  "delivery": {
    "delivery_id": "DEL-450",
    "contract_version": "1.0"
  },
  "response": {
    "response_id": "RESP-120"
  },
  "trace": {
    "execution_id": "EXE-020"
  }
}
```

La estructura definitiva será establecida en el capítulo de contratos.

---

## 5.15 Envelope Construction no modifica cognición

La construcción del envelope podrá agregar información operacional.

No podrá modificar la respuesta cognitiva.

Conceptualmente:

```text
Response
   │
   ├── unchanged
   │
   ▼
DeliveryEnvelope
   ├── delivery metadata
   ├── traceability
   └── response
```

---

## 5.16 Etapa 8 — Normalization

Podrá existir una fase de normalización técnica previa a serialización.

Ejemplos:

- convertir enumeraciones a valores contractuales;
- normalizar timestamps;
- representar UUID como texto;
- convertir tipos internos autorizados a estructuras públicas.

La normalización deberá ser:

- determinista;
- contractual;
- no cognitiva.

---

## 5.17 Normalization no es corrección semántica

Incorrecto:

```text
confidence = null
      ↓
normalizer
      ↓
confidence = 0.5
```

Correcto:

```text
datetime object
      ↓
normalizer
      ↓
ISO-8601 string
```

La primera altera significado.

La segunda cambia representación.

---

## 5.18 Etapa 9 — Serialization

Después de construir y normalizar el envelope deberá generarse una representación entregable.

Ejemplo:

```text
DeliveryEnvelope
        │
        ▼
Serializer
        │
        ▼
JSON Payload
```

El serializer deberá conocer:

- versión de esquema;
- reglas de encoding;
- tratamiento de null;
- representación temporal;
- tipos válidos.

---

## 5.19 Propiedades de la serialización

La serialización deberá ser:

```text
deterministic
validatable
version-aware
lossless with respect to contract semantics
```

No significa necesariamente que produzca bytes idénticos en todos los escenarios, salvo que el contrato así lo requiera.

Sí significa que la representación equivalente deberá conservar significado.

---

## 5.20 Etapa 10 — Payload Validation

Antes de cruzar la frontera, el payload deberá poder validarse.

La validación podrá comprobar:

```text
schema
required fields
types
version
encoding
size constraints
```

La finalidad es detectar errores antes del transporte.

---

## 5.21 Doble validación justificada

Podrán existir dos validaciones diferentes:

```text
MaterializedResponse Validation
```

y:

```text
DeliveryPayload Validation
```

No son redundantes.

La primera verifica:

```text
is this a valid response?
```

La segunda verifica:

```text
is this a valid deliverable representation?
```

Esta distinción será importante para diagnóstico.

---

## 5.22 Etapa 11 — Adapter Resolution

Una vez validado el payload deberá resolverse el adaptador correspondiente.

Conceptualmente:

```text
DeliveryTarget
      +
DeliveryPolicy
      +
ConsumerProfile
      ↓
Adapter Resolver
      ↓
DeliveryAdapter
```

La selección deberá evitar lógica rígida dispersa.

---

## 5.23 Adapter Registry

La implementación futura podrá requerir un registro de adaptadores.

Conceptualmente:

```text
DeliveryAdapterRegistry
├── IN_MEMORY
├── HTTP_JSON
├── WEBSOCKET_JSON
└── INTERNAL_CALL
```

Este registro deberá ser independiente del Capability Registry.

Son responsabilidades distintas.

---

## 5.24 Prohibición de confusión entre registries

Deberá preservarse:

```text
CapabilityRegistry
      ≠
DeliveryAdapterRegistry
```

El primero responde:

> ¿Qué capacidades puede ejecutar HEYTI?

El segundo respondería:

> ¿Qué mecanismos de entrega están disponibles?

No deberán mezclarse.

---

## 5.25 Etapa 12 — Pre-Delivery Observability

Antes de cruzar la frontera podrá registrarse un evento de inicio.

Ejemplo conceptual:

```text
DELIVERY_STARTED
```

con campos como:

```text
delivery_id
response_id
consumer_id
adapter_id
started_at
contract_version
```

La instrumentación deberá evitar registrar información sensible innecesaria.

---

## 5.26 Etapa 13 — Delivery Execution

El adaptador ejecutará la operación técnica.

Conceptualmente:

```text
adapter.deliver(payload, context)
```

La firma concreta se definirá durante implementación.

La operación podrá devolver:

```text
AdapterResult
```

con información técnica.

---

## 5.27 Responsabilidad del adaptador durante ejecución

Durante la operación el adaptador podrá:

- establecer conexión;
- aplicar timeout;
- enviar payload;
- recibir respuesta técnica;
- interpretar código técnico;
- producir receipt;
- mapear fallos.

No podrá reinterpretar el contenido cognitivo.

---

## 5.28 Etapa 14 — Technical Result Interpretation

El resultado técnico deberá traducirse al modelo común de Delivery.

Ejemplo:

```text
HTTP 200
```

podría convertirse en:

```text
DeliveryResult.status = DELIVERED
```

según política.

Mientras que:

```text
HTTP 503
```

podría convertirse en:

```text
DeliveryResult.status = FAILED
error = DELIVERY_TARGET_UNAVAILABLE
```

La traducción deberá ser explícita y testeable.

---

## 5.29 Transport Success no implica Semantic Success

Un transporte exitoso no deberá utilizarse para validar la calidad cognitiva de la respuesta.

Por ejemplo:

```text
HTTP 200
```

solo indica éxito técnico conforme al adaptador.

No significa:

```text
answer is correct
```

o:

```text
evidence is sufficient
```

Estas dimensiones pertenecen a etapas anteriores.

---

## 5.30 Etapa 15 — DeliveryReceipt Processing

Si el mecanismo devuelve un receipt, podrá incorporarse al resultado.

Ejemplo:

```text
remote_reference
accepted_at
consumer_status
```

El receipt deberá considerarse evidencia técnica de recepción.

No evidencia de presentación visual correcta.

---

## 5.31 Etapa 16 — DeliveryResult Construction

Toda operación deberá finalizar construyendo un `DeliveryResult`.

Ejemplo conceptual:

```text
DeliveryResult
├── delivery_id
├── response_id
├── status
├── consumer_id
├── adapter_id
├── started_at
├── completed_at
├── duration_ms
├── warnings
├── error
└── receipt
```

El resultado deberá reflejar el estado real de la operación.

---

## 5.32 Estados de resultado propuestos

Como base conceptual se propone:

```text
DELIVERED
REJECTED
FAILED
```

Podrá evaluarse posteriormente:

```text
PARTIAL
```

si existe una semántica operacional real que lo justifique.

---

## 5.33 Estado DELIVERED

`DELIVERED` deberá significar:

```text
entry valid
+
payload valid
+
adapter executed
+
delivery accepted according to adapter policy
```

No deberá significar que el consumidor mostró visualmente el contenido.

---

## 5.34 Estado REJECTED

`REJECTED` deberá representar una operación que no avanzó al transporte debido a una precondición incumplida.

Ejemplos:

```text
invalid response
unsupported contract
unknown consumer
incompatible consumer profile
missing required context
```

---

## 5.35 Estado FAILED

`FAILED` deberá representar una operación que superó las precondiciones iniciales pero experimentó un error durante procesamiento o entrega.

Ejemplos:

```text
serialization failure
adapter failure
timeout
target unavailable
internal delivery error
```

La frontera exacta entre REJECTED y FAILED deberá quedar formalizada en el contrato de errores.

---

## 5.36 Etapa 17 — Trace Completion

Al concluir la operación deberá completarse la información de trazabilidad.

Conceptualmente:

```text
DeliveryTrace
├── delivery_id
├── response_id
├── started_at
├── completed_at
├── status
├── adapter
└── error_code
```

Esto deberá suceder incluso cuando la operación falle.

---

## 5.37 Etapa 18 — Final Observability Event

La operación deberá poder emitir un evento final.

Ejemplos:

```text
DELIVERY_COMPLETED
DELIVERY_REJECTED
DELIVERY_FAILED
```

Estos eventos deberán ser coherentes con `DeliveryResult`.

---

## 5.38 Flujo exitoso completo

```text
MaterializedResponse
        │
        ▼
Create DeliveryRequest
        │
        ▼
Generate delivery_id
        │
        ▼
Entry Validation
        │
        ▼
Context Validation
        │
        ▼
Target Validation
        │
        ▼
Consumer Compatibility
        │
        ▼
Build Envelope
        │
        ▼
Normalize
        │
        ▼
Serialize
        │
        ▼
Validate Payload
        │
        ▼
Resolve Adapter
        │
        ▼
DELIVERY_STARTED
        │
        ▼
Adapter.deliver()
        │
        ▼
Technical Success
        │
        ▼
Build DeliveryResult
        │
        ▼
Complete Trace
        │
        ▼
DELIVERY_COMPLETED
        │
        ▼
status = DELIVERED
```

---

## 5.39 Flujo rechazado

```text
MaterializedResponse
        │
        ▼
Create DeliveryRequest
        │
        ▼
Generate delivery_id
        │
        ▼
Entry Validation
        │
        ▼
INVALID
        │
        ▼
DeliveryError
        │
        ▼
DeliveryResult
        │
        ▼
status = REJECTED
        │
        ▼
Trace Completion
```

No se ejecuta el adaptador.

---

## 5.40 Flujo con fallo de serialización

```text
MaterializedResponse
        │
        ▼
Validation
        │
        ▼
VALID
        │
        ▼
Envelope
        │
        ▼
Serialization
        │
        ▼
ERROR
        │
        ▼
DeliveryError
        │
        ▼
DeliveryResult
        │
        ▼
status = FAILED
```

La respuesta original permanece válida.

---

## 5.41 Flujo con fallo de adaptador

```text
MaterializedResponse
        │
        ▼
Validation
        │
        ▼
Serialization
        │
        ▼
Payload Valid
        │
        ▼
Adapter
        │
        ▼
Connection Error
        │
        ▼
DeliveryError
        │
        ▼
DeliveryResult
        │
        ▼
status = FAILED
```

La falla deberá atribuirse correctamente al adaptador o infraestructura.

---

## 5.42 Pipeline síncrono inicial

Para v1.0 deberá preferirse inicialmente un flujo síncrono y explícito, salvo que una necesidad arquitectónica real exija asincronía.

Conceptualmente:

```python
result = deliver(response, context)
```

produce un resultado final dentro de la misma operación.

Esto simplifica:

- pruebas;
- trazabilidad;
- errores;
- depuración;
- implementación inicial.

La asincronía podrá incorporarse posteriormente mediante una frontera formal.

---

## 5.43 Preparación para asincronía futura

Aunque v1.0 pueda iniciar síncrono, el modelo deberá evitar decisiones que impidan:

```text
queued delivery
background worker
event-driven delivery
streamed delivery
```

en futuras versiones.

La preparación deberá lograrse mediante:

- `delivery_id`;
- estados;
- contratos;
- adaptadores;
- trazabilidad explícita.

No mediante complejidad anticipada.

---

## 5.44 Pipeline y streaming

Streaming deberá considerarse un caso especializado.

No deberá asumirse desde el inicio que toda respuesta se entrega como un único payload.

En el futuro podrían existir:

```text
START
CHUNK
CHUNK
CHUNK
END
```

Sin embargo, esto requeriría contratos adicionales para:

- orden;
- integridad;
- finalización;
- errores parciales;
- reensamblado.

No forma parte obligatoria de v1.0.

---

## 5.45 Pipeline y múltiples consumidores

La versión base deberá favorecer:

```text
one DeliveryRequest
→ one consumer
→ one DeliveryResult
```

Si posteriormente una respuesta necesita distribuirse a múltiples consumidores, deberá utilizarse una capa explícita de orquestación de Delivery.

Ejemplo futuro:

```text
DeliveryFanout
├── DeliveryRequest A
├── DeliveryRequest B
└── DeliveryRequest C
```

Cada entrega mantendrá su propio `delivery_id`.

---

## 5.46 No fan-out oculto

Queda prohibido que el pipeline básico envíe silenciosamente la respuesta a múltiples consumidores.

Toda entrega deberá poder identificarse de forma independiente.

---

## 5.47 Pipeline y reintentos

Los reintentos no forman parte automática del pipeline base.

Flujo base:

```text
delivery attempt
     ↓
success / failure
```

Un retry deberá ser activado únicamente por una política explícita.

Ejemplo futuro:

```text
DeliveryResult = FAILED
       │
       ▼
Retry Policy
       │
       ├── NO RETRY
       └── RETRY
```

---

## 5.48 Identidad en reintentos

La arquitectura deberá decidir posteriormente si un reintento conserva:

```text
delivery_id
```

o genera:

```text
new delivery_id
```

acompañado de:

```text
parent_delivery_id
```

Para auditabilidad, la segunda opción puede resultar más clara.

La decisión definitiva será documentada cuando se formalice Retry Policy.

---

## 5.49 Pipeline y timeouts

Los timeouts deberán pertenecer principalmente al adaptador o a DeliveryPolicy.

Un timeout deberá generar un error explícito.

Ejemplo:

```text
DELIVERY_TIMEOUT
```

No deberá quedar como operación indefinida.

---

## 5.50 Pipeline y cancelación

La arquitectura deberá permitir futura cancelación cuando exista una operación suficientemente larga.

Sin embargo, en v1.0 una entrega síncrona simple puede no requerir este mecanismo.

No deberá introducirse complejidad si no existe una necesidad real.

---

## 5.51 Pipeline y observabilidad

Cada etapa relevante podrá generar observabilidad.

Ejemplo conceptual:

```text
delivery.request.created
delivery.validation.completed
delivery.serialization.completed
delivery.adapter.started
delivery.adapter.completed
delivery.finished
```

No todos los eventos deberán persistirse.

La política de observabilidad definirá qué nivel es necesario.

---

## 5.52 Pipeline y métricas

El sistema podrá medir:

```text
delivery_total
delivery_success_total
delivery_failure_total
delivery_rejected_total
delivery_duration_ms
payload_size_bytes
serialization_duration_ms
adapter_duration_ms
```

Estas métricas deberán ser operacionales.

No cognitivas.

---

## 5.53 Pipeline y logging

Los logs deberán contener identificadores suficientes para correlación.

Ejemplo:

```text
delivery_id=DEL-450
response_id=RESP-120
consumer=AT_PORTAL
adapter=HTTP_JSON
status=DELIVERED
```

No deberán incluir indiscriminadamente:

- payload completo;
- datos personales;
- evidencia sensible;
- credenciales;
- tokens.

La observabilidad deberá respetar seguridad.

---

## 5.54 Pipeline y auditoría

Auditoría deberá poder reconstruir:

```text
what was intended
what was validated
what was serialized
what adapter was used
what happened
what result was produced
```

Esto no implica almacenar todos los datos para siempre.

Implica preservar suficiente evidencia operacional conforme a política.

---

## 5.55 Pipeline y seguridad

La seguridad podrá intervenir antes del boundary crossing.

Conceptualmente:

```text
Entry Validation
      ↓
Authorization / Delivery Policy
      ↓
Payload
      ↓
Adapter
```

Una entrega no autorizada deberá rechazarse antes del transporte siempre que sea posible.

---

## 5.56 Pipeline y privacidad

El pipeline no deberá añadir información sensible que no forme parte del contrato.

También deberá evitar copiar información innecesaria a:

- metadata;
- logs;
- traces;
- receipts.

La regla será:

> **Transport only what is contractually required.**

---

## 5.57 Pipeline y compresión

La compresión, si se requiere, deberá pertenecer al adaptador o infraestructura de transporte.

Conceptualmente:

```text
DeliveryPayload
      ↓
Transport Adapter
      ↓
Compression
      ↓
Network
```

No deberá alterar la semántica del contrato.

---

## 5.58 Pipeline y cifrado

De manera similar, cifrado y protección de canal deberán estar encapsulados por infraestructura o adaptadores autorizados.

Delivery podrá requerir determinadas garantías de seguridad.

No deberá implementar criptografía improvisada dentro del Core.

---

## 5.59 Pipeline y Presentation

El pipeline termina antes de Presentation.

Conceptualmente:

```text
Delivery Pipeline
      ↓
Consumer receives payload
==============================
     DELIVERY COMPLETE
==============================
      ↓
Presentation Adapter
      ↓
Map / Chart / Table / Text
```

Por ello:

```text
render()
```

no forma parte del pipeline de Delivery.

---

## 5.60 Pipeline y acciones de UI

Si la respuesta futura contiene acciones abstractas como:

```text
OPEN_MODULE
SHOW_SECTION
DISPLAY_MAP_CONTEXT
```

Delivery podrá transportarlas como parte de la respuesta.

No deberá ejecutarlas.

Ejemplo:

```text
Delivery
   ↓
{ action: OPEN_MODULE, module: TERRITORIAL }
   ↓
Consumer
   ↓
Presentation Controller
   ↓
actual UI navigation
```

---

## 5.61 Pipeline y geometría

Si una respuesta contiene geometría o referencias territoriales, Delivery podrá:

- validarlas estructuralmente;
- serializarlas;
- transportarlas.

No deberá:

- dibujarlas;
- aplicar estilos;
- elegir zoom;
- crear capas Leaflet.

Estas operaciones ocurren después de Delivery.

---

## 5.62 Pipeline y gráficas

Si una respuesta contiene:

```text
series
categories
values
units
```

Delivery podrá transportarlas.

No deberá generar:

```text
Chart.js datasets
canvas elements
legend colors
```

La UI deberá adaptar los datos.

---

## 5.63 Pipeline y tablas

Una estructura tabular podrá representarse como:

```text
columns
rows
types
```

y ser entregada de forma neutral.

No deberá incluir necesariamente:

```text
HTML <table>
CSS classes
column widths
```

a menos que exista un contrato específico de presentación externo al Core.

---

## 5.64 Pipeline y texto

El texto generado por una capability o materializador podrá viajar como contenido.

Delivery deberá preservar:

- contenido;
- idioma;
- advertencias;
- estructura semántica relevante.

No deberá reescribirlo para adaptarlo visualmente.

---

## 5.65 Pipeline y errores previos

Si la respuesta materializada representa un resultado cognitivo con advertencias o error parcial, Delivery deberá preservarlo.

Por ejemplo:

```text
response.status = PARTIAL
response.warnings = [...]
```

Delivery podrá aun ser:

```text
delivery.status = DELIVERED
```

Esto significa:

```text
a partial cognitive response
was successfully delivered
```

No existe contradicción.

---

## 5.66 Pipeline y errores terminales

Si Delivery falla, deberá producir un resultado terminal.

No deberá dejar la operación en estado indefinido.

Conceptualmente:

```text
DELIVERED
REJECTED
FAILED
```

serán estados terminales.

---

## 5.67 Pipeline y limpieza

Los recursos técnicos utilizados por adaptadores deberán liberarse correctamente.

Ejemplos:

```text
connections
streams
temporary buffers
```

Esto será responsabilidad de infraestructura o del adaptador.

El Core deberá exigir comportamiento seguro y testeable.

---

## 5.68 Pipeline y determinismo

Dado:

```text
same response
same target
same context
same policy
same adapter behavior
```

el pipeline debería producir un resultado equivalente.

Los elementos naturalmente variables, como:

```text
delivery_id
timestamp
duration
```

podrán diferir.

El significado operacional deberá permanecer consistente.

---

## 5.69 Pipeline y side effects

El side effect principal autorizado es la entrega al consumidor.

Otros side effects deberán estar gobernados explícitamente.

Ejemplos aceptables:

```text
logging
metrics
audit record
```

cuando estén autorizados.

Ejemplos problemáticos:

```text
modify database business data
change campaign priority
update section classification
```

Estas acciones están fuera de Delivery.

---

## 5.70 Pipeline y pruebas por etapa

Cada etapa deberá poder probarse independientemente.

Ejemplos:

```text
test_entry_validation
test_context_validation
test_envelope_builder
test_serializer
test_payload_validator
test_adapter_resolution
test_delivery_result_mapping
```

Además deberá existir prueba end-to-end del pipeline de Delivery.

---

## 5.71 Pipeline mínimo para v1.0

La versión inicial podrá implementar el siguiente núcleo:

```text
1. Receive MaterializedResponse
2. Create DeliveryContext
3. Validate Response
4. Build Envelope
5. Serialize
6. Validate Payload
7. Deliver through InMemory or Internal Adapter
8. Produce DeliveryResult
9. Trace
```

Este núcleo permitirá probar completamente la arquitectura sin requerir todavía integración HTTP real.

---

## 5.72 Razón para un adaptador InMemory inicial

Un `InMemoryDeliveryAdapter` resultaría especialmente útil para v1.0 porque permitiría validar:

- contratos;
- serialización;
- trazabilidad;
- errores;
- estados;
- independencia de transporte;

sin introducir complejidad de red.

Conceptualmente:

```text
HEYTI
  ↓
Delivery
  ↓
InMemoryAdapter
  ↓
Captured Payload
```

Esto permitiría una prueba controlada antes de conectar Portal.

---

## 5.73 Evolución posterior del pipeline

Una vez validado el núcleo podrá incorporarse:

```text
HTTP Adapter
```

y posteriormente:

```text
WebSocket Adapter
```

si la experiencia visual lo requiere.

La secuencia recomendada será:

```text
Core Delivery
      ↓
InMemory verification
      ↓
Internal integration
      ↓
HTTP/API integration
      ↓
Portal/UI integration
```

La arquitectura deberá permanecer estable durante esta evolución.

---

## 5.74 Diagrama de secuencia conceptual

```text
Consumer      Adapter      Delivery      Materialization      Runtime
   │             │             │               │                │
   │             │             │               │                │
   │             │             │               │◄───────────────┤
   │             │             │               │ CapabilityResult
   │             │             │               │                │
   │             │             │◄──────────────┤                │
   │             │             │ MaterializedResponse           │
   │             │             │               │                │
   │             │             │ validate()    │                │
   │             │             │──────────┐    │                │
   │             │             │          │    │                │
   │             │             │◄─────────┘    │                │
   │             │             │               │                │
   │             │             │ serialize()   │                │
   │             │             │──────────┐    │                │
   │             │             │          │    │                │
   │             │             │◄─────────┘    │                │
   │             │◄────────────┤               │                │
   │             │ deliver()   │               │                │
   │◄────────────┤             │               │                │
   │ payload     │             │               │                │
   │────────────►│             │               │                │
   │ accepted    │             │               │                │
   │             │────────────►│               │                │
   │             │ AdapterResult               │                │
   │             │             │               │                │
   │             │             │ DeliveryResult│                │
   │             │             │               │                │
```

Este diagrama es conceptual y deberá refinarse durante implementación.

---

## 5.75 Diagrama de flujo operacional

```text
          ┌───────────────────────┐
          │ MaterializedResponse  │
          └───────────┬───────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │ Create DeliveryRequest│
          └───────────┬───────────┘
                      │
                      ▼
          ┌───────────────────────┐
          │ Entry Validation      │
          └───────────┬───────────┘
                      │
            ┌─────────┴─────────┐
            │                   │
          VALID               INVALID
            │                   │
            ▼                   ▼
┌───────────────────────┐   ┌────────────────┐
│ Context / Target      │   │ REJECTED       │
│ Validation            │   │ DeliveryResult │
└───────────┬───────────┘   └────────────────┘
            │
            ▼
┌───────────────────────┐
│ Compatibility Check   │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Build Envelope        │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Serialize             │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Validate Payload      │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Resolve Adapter       │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Deliver               │
└───────────┬───────────┘
            │
        ┌───┴────┐
        │        │
      SUCCESS   ERROR
        │        │
        ▼        ▼
┌─────────────┐ ┌─────────────┐
│ DELIVERED   │ │ FAILED      │
│ Result      │ │ Result      │
└─────────────┘ └─────────────┘
```

---

## 5.76 Invariantes del pipeline

Se establecen los siguientes invariantes.

### HRRD-PL01 — Validate Before Delivery

No deberá ejecutarse un adaptador con una respuesta no validada.

### HRRD-PL02 — Explicit Operation Identity

Toda operación deberá poseer identidad de Delivery cuando corresponda.

### HRRD-PL03 — No Silent Field Loss

Ninguna etapa podrá eliminar silenciosamente información obligatoria.

### HRRD-PL04 — Serialization Before Boundary

La representación deberá estar completamente serializada y validada antes de cruzar la frontera.

### HRRD-PL05 — Explicit Adapter

Toda entrega deberá identificar el adaptador utilizado.

### HRRD-PL06 — Explicit Terminal Result

Toda ejecución del pipeline deberá terminar en un resultado explícito.

### HRRD-PL07 — Failure Attribution

El error deberá atribuirse a la etapa donde ocurrió.

### HRRD-PL08 — Trace Completion

La trazabilidad deberá completarse incluso ante fallo o rechazo.

### HRRD-PL09 — Presentation Exclusion

El pipeline termina antes de cualquier renderizado visual.

### HRRD-PL10 — No Implicit Retry

El pipeline base no deberá reintentar silenciosamente.

---

## 5.77 Prueba de conformidad operacional

Una implementación del pipeline deberá poder demostrar:

1. que no entrega respuestas inválidas;
2. que no cruza la frontera antes de serializar;
3. que preserva `response_id`;
4. que genera o conserva `delivery_id`;
5. que distingue rechazo de fallo;
6. que identifica el adaptador;
7. que produce `DeliveryResult`;
8. que conserva trazabilidad;
9. que puede probarse sin UI;
10. que puede probarse sin red utilizando un adaptador de prueba.

---

## 5.78 Criterio de éxito del pipeline

El pipeline será considerado correcto cuando sea posible ejecutar:

```text
MaterializedResponse
      ↓
Runtime Response Delivery Pipeline
      ↓
DeliveryResult
```

y responder sin ambigüedad:

```text
What response?
Which delivery?
Which consumer?
Which adapter?
Which contract?
Was it valid?
Was it serialized?
Was it delivered?
If not, where did it fail?
```

---

## 5.79 Declaración arquitectónica del capítulo

Runtime Response Delivery no deberá ser implementado como una única función opaca que simplemente convierta una respuesta a JSON y la envíe.

Deberá existir un pipeline explícito en el que cada etapa tenga:

- propósito;
- precondiciones;
- resultado;
- responsabilidad;
- y capacidad de diagnóstico.

La regla consolidada queda establecida como:

> **Una respuesta HEYTI solo podrá cruzar la frontera de Delivery después de haber sido identificada, validada, contextualizada, verificada respecto a su consumidor, convertida a una representación contractual válida y asociada con un adaptador explícito. Toda operación deberá finalizar con un DeliveryResult trazable.**

Este pipeline constituye la base operacional sobre la cual se definirá el **Delivery Contract** de HEYTI.

---

**Fin del Capítulo 5**


# Capítulo 6. Delivery Contract y estructura formal de la entrega

## 6.1 Propósito del capítulo

Este capítulo define el **Delivery Contract** de HEYTI Runtime Response Delivery.

Los capítulos anteriores establecieron:

- la posición arquitectónica de Delivery;
- sus fronteras;
- sus principios;
- sus entidades conceptuales;
- y su pipeline operacional.

A partir de este punto resulta necesario formalizar qué información debe acompañar a una respuesta durante una operación de entrega.

El Delivery Contract deberá responder con claridad:

> ¿Qué estructura cruza la frontera de Delivery?

> ¿Qué elementos son obligatorios?

> ¿Qué información pertenece a la respuesta materializada?

> ¿Qué información pertenece exclusivamente a la operación de entrega?

> ¿Qué campos permiten trazabilidad, compatibilidad, versionado y auditoría?

El contrato deberá proteger simultáneamente:

- la semántica cognitiva de HEYTI;
- la estabilidad de la integración;
- la independencia respecto del consumidor;
- y la posibilidad de evolución futura.

---

## 6.2 Principio Contract First

El Delivery Contract constituye la autoridad formal sobre la estructura entregable.

Por tanto:

```text
Implementation
     ↓
MUST conform to
     ↓
Delivery Contract
```

y no:

```text
Existing implementation
        ↓
defines contract accidentally
```

La estructura del contrato deberá existir antes de depender de ella desde consumidores externos.

---

## 6.3 Separación contractual

La arquitectura deberá distinguir al menos tres dominios contractuales:

```text
1. Response Contract
2. Delivery Contract
3. Transport Contract
```

Cada uno posee una responsabilidad diferente.

---

## 6.4 Response Contract

El **Response Contract** representa la respuesta materializada.

Conceptualmente:

```text
HeytiResponseContract
```

contiene el significado producido por HEYTI.

Podrá incluir:

- contenido;
- resultados;
- evidencia;
- advertencias;
- nivel de confianza;
- metadatos;
- referencias;
- trazabilidad cognitiva.

Este contrato no deberá alterarse únicamente para satisfacer necesidades técnicas del transporte.

---

## 6.5 Delivery Contract

El **Delivery Contract** encapsula la respuesta materializada dentro del contexto de una operación de entrega.

Conceptualmente:

```text
DeliveryEnvelope
├── delivery
├── response
├── trace
└── metadata
```

La finalidad del contrato será permitir que el consumidor pueda conocer:

- qué está recibiendo;
- qué respuesta es;
- qué operación de entrega la produjo;
- qué versión contractual utiliza;
- qué trazabilidad relevante posee;
- y cómo interpretar su estructura.

---

## 6.6 Transport Contract

El **Transport Contract** representa los detalles específicos del mecanismo técnico.

Ejemplo:

```text
HTTP
├── method
├── route
├── headers
├── status code
└── content type
```

o:

```text
WebSocket
├── event type
├── channel
└── frame
```

Estos elementos deberán permanecer fuera del Delivery Contract central cuando sean puramente tecnológicos.

---

## 6.7 Jerarquía contractual

La arquitectura deberá preservar:

```text
Cognitive Meaning
      │
      ▼
Response Contract
      │
      ▼
Delivery Contract
      │
      ▼
Transport Adapter
      │
      ▼
Transport Contract
```

Cada nivel podrá agregar información propia.

Ningún nivel inferior deberá reinterpretar el superior.

---

## 6.8 Delivery Envelope

Se propone como estructura contractual central el concepto de:

```text
DeliveryEnvelope
```

Conceptualmente:

```text
DeliveryEnvelope
├── delivery
├── response
├── trace
├── consumer
└── metadata
```

No todos los bloques deberán necesariamente exponerse con esta misma jerarquía en la implementación final.

Sin embargo, la separación conceptual deberá preservarse.

---

## 6.9 Bloque delivery

El bloque `delivery` deberá describir la operación de entrega.

Conceptualmente podrá contener:

```text
delivery_id
delivery_contract_version
status
requested_at
started_at
completed_at
adapter_id
target_id
```

No todos los campos deberán existir obligatoriamente desde v1.0.

La estructura definitiva deberá obedecer a las necesidades reales del Runtime.

---

## 6.10 delivery_id

`delivery_id` deberá identificar una operación concreta.

Propiedades esperadas:

```text
unique
stable during operation
opaque to consumers
traceable
```

Un consumidor no deberá extraer lógica de negocio desde este identificador.

Ejemplo correcto:

```text
DEL-9f21...
```

Su formato exacto podrá ser:

- UUID;
- ULID;
- identificador interno equivalente.

La arquitectura no deberá depender semánticamente del formato.

---

## 6.11 response_id

`response_id` identifica la respuesta materializada.

Deberá conservarse sin modificación durante Delivery.

Relación conceptual:

```text
response_id
   identifies
MaterializedResponse
```

mientras:

```text
delivery_id
   identifies
DeliveryOperation
```

Ambos deberán permanecer inequívocamente separados.

---

## 6.12 delivery_contract_version

Toda estructura de Delivery deberá poder indicar su versión.

Ejemplo:

```text
delivery_contract_version = "1.0"
```

Esto permitirá:

- compatibilidad;
- validación;
- evolución;
- auditoría;
- depuración.

La ausencia de versión explícita deberá considerarse una debilidad contractual salvo que exista una política formal alternativa.

---

## 6.13 response_contract_version

Cuando la respuesta posea su propio contrato versionado, dicha versión deberá permanecer accesible.

Conceptualmente:

```text
delivery_contract_version = 1.0
response_contract_version = 1.0
```

Estas versiones no deberán considerarse necesariamente iguales.

Podrán evolucionar de manera independiente.

---

## 6.14 Ejemplo de evolución independiente

Podría existir:

```text
Response Contract 1.2
Delivery Contract 1.0
```

si Delivery sigue siendo capaz de encapsular la nueva versión.

Posteriormente podría existir:

```text
Response Contract 2.0
Delivery Contract 2.0
```

si un cambio incompatible requiere evolución coordinada.

---

## 6.15 Bloque response

El bloque `response` deberá transportar la respuesta materializada sin alterar su semántica.

Conceptualmente:

```text
response:
    response_id
    status
    content
    evidence
    warnings
    metadata
```

La estructura concreta deberá respetar `HeytiResponseContract`.

Delivery no deberá redefinir arbitrariamente estos campos.

---

## 6.16 Regla de encapsulación

La preferencia arquitectónica será:

```text
DeliveryEnvelope
    contains
HeytiResponseContract
```

en lugar de:

```text
DeliveryEnvelope
    reconstructs
HeytiResponseContract
```

La primera opción preserva separación.

La segunda aumenta riesgo de pérdida o divergencia.

---

## 6.17 Bloque trace

El bloque `trace` deberá permitir correlacionar la entrega con el flujo que la originó.

Conceptualmente podrá contener:

```text
request_id
session_id
execution_id
response_id
delivery_id
correlation_id
capability_id
```

La obligatoriedad de cada campo dependerá del contexto.

---

## 6.18 Relación de trazabilidad

La cadena ideal será:

```text
request_id
    ↓
execution_id
    ↓
response_id
    ↓
delivery_id
```

Cuando exista sesión:

```text
session_id
    │
    └── request_id
           ↓
       execution_id
           ↓
       response_id
           ↓
       delivery_id
```

Esta estructura deberá permitir reconstrucción operacional.

---

## 6.19 correlation_id

`correlation_id` podrá utilizarse cuando sea útil conectar múltiples eventos o operaciones.

No deberá convertirse en sustituto indiscriminado de identificadores específicos.

La regla será:

```text
Specific IDs identify entities.
Correlation ID groups related activity.
```

---

## 6.20 capability_id

La identidad de la capability podrá formar parte de la trazabilidad.

Ejemplo:

```text
capability_id = "describe_section"
```

Su presencia permitirá responder:

> ¿Qué capability originó esta respuesta?

Delivery no deberá utilizar este campo para ejecutar nuevamente la capability.

---

## 6.21 capability_version

Cuando exista versionado formal de capabilities, podrá incluirse:

```text
capability_version
```

si es necesario para auditoría.

No deberá añadirse únicamente por anticipación especulativa.

---

## 6.22 Bloque consumer

El contrato podrá incluir información lógica del consumidor.

Conceptualmente:

```text
consumer:
    consumer_id
    consumer_profile_version
```

Ejemplo:

```text
consumer_id = "AT_PORTAL"
```

La información deberá representar identidad lógica, no detalles visuales.

---

## 6.23 target_id

`target_id` podrá identificar el destino lógico.

Dependiendo de la arquitectura:

```text
consumer_id
```

y:

```text
target_id
```

podrán ser equivalentes o diferentes.

Por ejemplo:

```text
consumer_id = AT_PORTAL
target_id   = HEYTI_RESPONSE_PANEL
```

Si esta distinción resulta necesaria.

No deberá introducirse si no existe necesidad real.

---

## 6.24 adapter_id

El contrato operacional deberá permitir identificar el adaptador utilizado.

Ejemplo:

```text
adapter_id = "IN_MEMORY"
```

o:

```text
adapter_id = "HTTP_JSON"
```

Esto será especialmente útil para observabilidad.

---

## 6.25 Bloque metadata

El bloque `metadata` deberá contener información descriptiva no central.

Podría incluir:

```text
environment
node
schema_id
payload_encoding
generated_at
```

si se requiere.

Metadata no deberá utilizarse para esconder campos estructurales importantes.

---

## 6.26 Metadata no es cajón de sastre

Queda prohibido el patrón:

```json
{
  "metadata": {
    "required_field_but_we_did_not_model_it": "..."
  }
}
```

La información esencial deberá formar parte formal del contrato.

Metadata será extensible, pero gobernada.

---

## 6.27 Estado de Delivery

El contrato deberá poder expresar el estado de la operación.

Para v1.0 se propone mantener:

```text
DELIVERED
REJECTED
FAILED
```

cuando el envelope corresponda a una operación concluida.

Sin embargo, durante el pipeline interno podrán existir estados transitorios.

---

## 6.28 Estado transitorio vs estado público

La arquitectura deberá distinguir:

```text
internal pipeline state
```

de:

```text
public DeliveryResult status
```

No todo estado interno necesita exponerse al consumidor.

Ejemplo interno:

```text
SERIALIZING
```

puede no formar parte del contrato público.

---

## 6.29 Error Contract

Cuando exista un fallo, el Delivery Contract deberá poder representar un error estructurado.

Conceptualmente:

```text
error:
    code
    category
    message
    recoverable
    details
```

La estructura exacta deberá considerar seguridad.

---

## 6.30 error.code

El `code` deberá ser estable y legible por máquina.

Ejemplos conceptuales:

```text
DELIVERY_VALIDATION_ERROR
DELIVERY_SERIALIZATION_ERROR
DELIVERY_TARGET_UNAVAILABLE
DELIVERY_TIMEOUT
DELIVERY_ADAPTER_ERROR
```

Los consumidores no deberán depender únicamente de mensajes humanos para interpretar errores.

---

## 6.31 error.message

El mensaje deberá ser útil para diagnóstico o presentación controlada.

Sin embargo, no deberá exponer:

- stack traces;
- rutas internas sensibles;
- credenciales;
- consultas SQL;
- secretos;
- datos privados innecesarios.

---

## 6.32 error.category

La categoría podrá agrupar errores.

Ejemplos:

```text
VALIDATION
SERIALIZATION
COMPATIBILITY
TRANSPORT
TIMEOUT
INTERNAL
```

Esto permitirá métricas y diagnóstico.

---

## 6.33 recoverable

La arquitectura podrá incluir:

```text
recoverable = true | false
```

si existe una política clara.

Este campo no deberá utilizarse para activar reintentos automáticos sin política explícita.

---

## 6.34 warnings

El Delivery Contract deberá poder preservar advertencias de la respuesta materializada.

También podrá contener advertencias propias de Delivery si se distinguen claramente.

Ejemplo:

```text
response.warnings
```

versus:

```text
delivery.warnings
```

No deberán mezclarse sin origen identificable.

---

## 6.35 Warning origin

Toda advertencia debería poder asociarse a su dominio.

Ejemplos:

```text
COGNITIVE
MATERIALIZATION
DELIVERY
```

si el modelo final lo requiere.

La UI podrá posteriormente presentarlas de manera adecuada.

---

## 6.36 Datos temporales

El contrato deberá definir formatos temporales estables.

Se recomienda conceptualmente:

```text
ISO-8601
```

con información de zona horaria cuando corresponda.

Ejemplo:

```text
2026-08-20T15:42:11-06:00
```

Deberá evitarse:

```text
08/20/26 3:42
```

por su ambigüedad.

---

## 6.37 requested_at

Representa cuándo se solicitó la operación de entrega.

No necesariamente coincide con:

```text
response.generated_at
```

---

## 6.38 started_at

Representa cuándo comenzó efectivamente el pipeline o la operación de entrega.

---

## 6.39 completed_at

Representa cuándo concluyó la operación.

---

## 6.40 duration_ms

Podrá calcularse como información operacional.

Conceptualmente:

```text
duration_ms
```

deberá considerarse metadata operacional.

No forma parte de la semántica cognitiva.

---

## 6.41 data_as_of

Si la respuesta materializada contiene:

```text
data_as_of
```

Delivery deberá preservarlo.

Este campo indica la fecha de vigencia de la información, no la fecha de entrega.

La diferencia es fundamental.

---

## 6.42 Ejemplo temporal

```text
data_as_of     = 2024-06-02
generated_at   = 2026-08-20T15:30:00-06:00
delivered_at   = 2026-08-20T15:30:01-06:00
```

Cada campo representa un hecho diferente.

---

## 6.43 Nullability

El contrato deberá especificar qué campos aceptan:

```text
null
```

y qué significado tiene la ausencia.

No deberá asumirse que:

```text
null
```

es equivalente a:

```text
0
false
""
[]
```

---

## 6.44 Required vs Optional

Todos los campos deberán clasificarse conceptualmente como:

```text
REQUIRED
OPTIONAL
CONDITIONAL
```

Ejemplo:

```text
delivery_id        REQUIRED
response            REQUIRED
error               CONDITIONAL
receipt             OPTIONAL
```

Esto deberá formalizarse durante implementación.

---

## 6.45 Campos condicionales

Un campo condicional aparece únicamente cuando determinada condición se cumple.

Ejemplo:

```text
error
```

podría ser obligatorio cuando:

```text
status = FAILED
```

y prohibido o nulo cuando:

```text
status = DELIVERED
```

Este tipo de reglas deberá documentarse.

---

## 6.46 Invariantes de consistencia

El contrato deberá imponer invariantes.

Ejemplo:

```text
status = DELIVERED
⇒ error = null
```

o:

```text
status = FAILED
⇒ error != null
```

si la política final así lo establece.

Las combinaciones inválidas deberán rechazarse.

---

## 6.47 Schema Validation

El Delivery Contract deberá ser validable mediante un esquema o validador formal.

Posibles mecanismos:

```text
Python dataclass validation
Pydantic model
JSON Schema
custom validator
```

La elección concreta deberá integrarse con la arquitectura actual de HEYTI.

El requisito es:

> **El contrato deberá poder validarse automáticamente.**

---

## 6.48 Canonical Dictionary Representation

La implementación podrá utilizar una representación canónica basada en diccionarios antes de JSON.

Conceptualmente:

```python
delivery_envelope.to_dict()
```

podrá producir una estructura serializable.

Esto sería coherente con la estrategia utilizada en materialización si ya existe un patrón similar.

---

## 6.49 JSON Representation

JSON deberá considerarse un formato natural para integración con Portal y futuras APIs.

Sin embargo:

```text
Delivery Contract ≠ JSON
```

JSON será una representación del contrato.

El contrato seguirá siendo una definición semántica independiente.

---

## 6.50 Orden de campos

El orden de campos en JSON no deberá poseer semántica.

Un consumidor correcto deberá interpretar por nombre.

Ejemplo:

```json
{
  "delivery": {},
  "response": {}
}
```

deberá ser semánticamente equivalente a una representación con orden distinto.

---

## 6.51 Encoding

La representación JSON deberá utilizar:

```text
UTF-8
```

salvo decisión explícita distinta.

Esto permitirá manejar correctamente español y otros caracteres.

---

## 6.52 Números

Los números deberán conservar tipos semánticos adecuados.

Ejemplo:

```text
section_id
```

aunque visualmente parezca numérico, podrá necesitar ser tratado como identificador textual.

La arquitectura deberá evitar conversiones automáticas que puedan:

- eliminar ceros;
- alterar claves;
- introducir precisión incorrecta.

---

## 6.53 Identificadores territoriales

Campos como:

```text
section_id
municipality_id
district_id
casilla_id
```

deberán tratarse como identificadores.

No como cantidades aritméticas salvo que el dominio indique lo contrario.

---

## 6.54 Unidades

Los valores cuantitativos deberán transportar unidad cuando sea necesaria para interpretación.

Ejemplo:

```json
{
  "value": 61.4,
  "unit": "percent"
}
```

mejor que:

```json
{
  "value": 61.4
}
```

si el significado no puede inferirse inequívocamente.

---

## 6.55 Content Types Semánticos

La respuesta podrá contener bloques estructurados.

Ejemplos:

```text
text
metric
table
series
territorial_reference
evidence
warning
action
```

Estos tipos deberán representar semántica.

No tecnología visual.

---

## 6.56 Tipo text

Ejemplo:

```json
{
  "type": "text",
  "content": "..."
}
```

La UI decidirá:

- tipografía;
- tamaño;
- ubicación.

---

## 6.57 Tipo metric

Ejemplo:

```json
{
  "type": "metric",
  "label": "Participación",
  "value": 61.4,
  "unit": "percent"
}
```

La UI podrá representarlo como KPI, tabla u otra vista.

---

## 6.58 Tipo series

Ejemplo conceptual:

```json
{
  "type": "series",
  "name": "Participación histórica",
  "x": [2018, 2021, 2024],
  "y": [55.1, 58.7, 61.4],
  "unit": "percent"
}
```

Delivery no deberá añadir:

```text
chart_type
chart_color
canvas_id
```

salvo que esos campos pertenezcan a un contrato de presentación separado.

---

## 6.59 Tipo table

Ejemplo:

```json
{
  "type": "table",
  "columns": ["Año", "PAN", "MORENA"],
  "rows": [
    [2018, 500, 420],
    [2024, 460, 610]
  ]
}
```

La estructura deberá ser neutral.

---

## 6.60 Tipo territorial_reference

Ejemplo:

```json
{
  "type": "territorial_reference",
  "section_id": "1481",
  "municipality_id": "..."
}
```

La presentación podrá decidir si abre un mapa.

Delivery únicamente transportará la referencia.

---

## 6.61 Tipo geometry

Si en algún momento se requiere entregar geometría, deberá utilizarse una representación estándar.

GeoJSON podría ser una alternativa natural.

Sin embargo, la decisión deberá evaluarse respecto de:

- tamaño;
- seguridad;
- rendimiento;
- necesidad real.

No toda respuesta territorial necesita transportar geometría completa.

---

## 6.62 Geometry Reference vs Geometry Payload

La arquitectura deberá distinguir:

```text
geometry_reference
```

de:

```text
geometry_payload
```

Una referencia puede ser suficiente para que el consumidor consulte una geometría conocida.

Esto reduce payload y acoplamiento.

---

## 6.63 Tipo action

Una acción deberá ser semántica.

Ejemplo:

```json
{
  "type": "action",
  "action": "OPEN_MODULE",
  "module": "TERRITORIAL",
  "context": {
    "section_id": "1481"
  }
}
```

La UI decide cómo ejecutar la acción.

---

## 6.64 Acciones prohibidas

No deberán entregarse acciones con código ejecutable.

Prohibido:

```json
{
  "javascript": "document.querySelector(...).click()"
}
```

o estructuras equivalentes.

Esto violaría:

- seguridad;
- desacoplamiento;
- neutralidad de presentación.

---

## 6.65 Tipo evidence

La evidencia podrá representarse mediante referencias estructuradas.

Ejemplo conceptual:

```json
{
  "type": "evidence",
  "evidence_id": "EVD-001",
  "source": "...",
  "data_as_of": "..."
}
```

La estructura deberá respetar el contrato definido por HES y materialización.

---

## 6.66 Tipo warning

Ejemplo:

```json
{
  "type": "warning",
  "code": "INCOMPLETE_DATA",
  "message": "..."
}
```

Delivery deberá preservar advertencias cognitivas.

---

## 6.67 Contract Projection

Podrá existir en el futuro una proyección controlada del contrato para consumidores específicos.

Conceptualmente:

```text
Full Delivery Contract
        ↓
Authorized Projection
        ↓
Consumer-Specific Public View
```

La proyección deberá estar:

- explícitamente definida;
- versionada;
- validada;
- y no deberá eliminar semántica obligatoria sin política.

---

## 6.68 No ad-hoc projection

Queda prohibido:

```text
if portal:
    delete evidence
```

La adaptación deberá utilizar contratos formales.

---

## 6.69 Contract Compatibility

Dos versiones serán compatibles cuando un consumidor autorizado pueda interpretar la nueva estructura sin ambigüedad ni pérdida de significado requerido.

Cambios potencialmente compatibles:

```text
add optional field
add optional metadata
```

Cambios potencialmente incompatibles:

```text
remove required field
rename required field
change field meaning
change type
```

La política formal se desarrollará en el capítulo de versionado.

---

## 6.70 Unknown Fields

La arquitectura deberá definir cómo tratar campos desconocidos.

Una política razonable podrá permitir que consumidores ignoren campos opcionales desconocidos dentro de la misma versión compatible.

Sin embargo, deberá evitarse depender de este comportamiento sin contrato.

---

## 6.71 Strict Validation Interna

Dentro de HEYTI, la validación deberá ser suficientemente estricta para detectar:

- campos obligatorios faltantes;
- tipos incorrectos;
- versiones inválidas;
- combinaciones inconsistentes.

---

## 6.72 Tolerancia externa controlada

Un consumidor podrá ser más tolerante frente a campos adicionales.

Pero nunca deberá asumir automáticamente significado no definido.

---

## 6.73 DeliveryReceipt Contract

Cuando un adaptador soporte confirmación, el receipt podrá tener una estructura como:

```text
receipt:
    accepted
    remote_reference
    received_at
```

La obligatoriedad dependerá del adaptador.

---

## 6.74 remote_reference

Podrá representar un identificador proporcionado por el consumidor o transporte.

No deberá confundirse con:

```text
response_id
delivery_id
```

---

## 6.75 Payload Size

El contrato o la política podrán registrar:

```text
payload_size_bytes
```

como metadata operacional.

Esto permitirá monitorear crecimiento de respuestas.

---

## 6.76 Payload Hash

La arquitectura podrá considerar un hash del payload para auditoría o integridad.

Ejemplo conceptual:

```text
payload_hash
```

Sin embargo, no deberá introducirse hasta definir:

- algoritmo;
- canonicalización;
- propósito;
- política de persistencia.

No deberá agregarse de forma improvisada.

---

## 6.77 Canonicalization

Si en el futuro se utilizan hashes o firmas, será necesario definir una representación canónica.

Esto está fuera del alcance obligatorio de v1.0.

La arquitectura deberá dejar la puerta abierta sin sobreconstruir.

---

## 6.78 Ejemplo conceptual de DeliveryEnvelope exitoso

```json
{
  "delivery": {
    "delivery_id": "DEL-331",
    "delivery_contract_version": "1.0",
    "status": "DELIVERED",
    "adapter_id": "IN_MEMORY",
    "requested_at": "2026-08-20T15:30:00-06:00",
    "completed_at": "2026-08-20T15:30:00-06:00"
  },
  "response": {
    "response_id": "RESP-120",
    "response_contract_version": "1.0",
    "status": "SUCCESS",
    "content": {}
  },
  "trace": {
    "request_id": "REQ-001",
    "execution_id": "EXE-001",
    "session_id": "SES-001",
    "capability_id": "describe_section"
  },
  "consumer": {
    "consumer_id": "AT_PORTAL"
  },
  "metadata": {}
}
```

Este ejemplo es conceptual.

No constituye todavía un schema definitivo.

---

## 6.79 Ejemplo conceptual de DeliveryResult fallido

```json
{
  "delivery": {
    "delivery_id": "DEL-332",
    "delivery_contract_version": "1.0",
    "status": "FAILED",
    "adapter_id": "HTTP_JSON"
  },
  "response": {
    "response_id": "RESP-121"
  },
  "trace": {
    "request_id": "REQ-002",
    "execution_id": "EXE-002"
  },
  "error": {
    "code": "DELIVERY_TARGET_UNAVAILABLE",
    "category": "TRANSPORT",
    "message": "Target unavailable",
    "recoverable": true
  }
}
```

La respuesta materializada podrá haber sido completamente válida.

El error pertenece exclusivamente a Delivery.

---

## 6.80 Ejemplo conceptual de rechazo

```json
{
  "delivery": {
    "delivery_id": "DEL-333",
    "delivery_contract_version": "1.0",
    "status": "REJECTED"
  },
  "response": {
    "response_id": "RESP-122"
  },
  "error": {
    "code": "DELIVERY_CONTRACT_MISMATCH",
    "category": "VALIDATION",
    "message": "Unsupported response contract version",
    "recoverable": false
  }
}
```

El adaptador no debería haberse ejecutado.

---

## 6.81 Contrato mínimo v1.0

Para evitar sobreconstrucción, la implementación inicial debería considerar como mínimo:

```text
DeliveryEnvelope
├── delivery_id
├── delivery_contract_version
├── response
├── consumer_id
├── adapter_id
├── trace
└── status/result
```

junto con:

```text
error
```

cuando corresponda.

---

## 6.82 Extensiones futuras

Podrán incorporarse posteriormente:

```text
receipt
retry
security context
payload hash
consumer profile version
streaming metadata
fan-out metadata
```

únicamente cuando exista necesidad real.

---

## 6.83 Invariantes del Delivery Contract

Se establecen los siguientes invariantes.

### HRRD-C01 — Explicit Contract Version

Toda entrega deberá estar asociada con una versión contractual.

### HRRD-C02 — Response Preservation

El contrato de Delivery no deberá modificar la semántica del Response Contract.

### HRRD-C03 — Distinct Identities

`response_id` y `delivery_id` representan entidades diferentes.

### HRRD-C04 — Traceability

Toda entrega deberá poder conservar la trazabilidad mínima definida.

### HRRD-C05 — Structured Error

Los fallos deberán representarse mediante errores estructurados.

### HRRD-C06 — No Visual Implementation

El contrato no deberá contener dependencias directas de HTML, DOM, Leaflet, Chart.js o CSS.

### HRRD-C07 — Explicit Optionality

La obligatoriedad y opcionalidad de campos deberá estar definida.

### HRRD-C08 — Type Stability

Los tipos públicos no deberán cambiar silenciosamente.

### HRRD-C09 — Null Semantics

Los valores nulos deberán conservar significado explícito.

### HRRD-C10 — Machine Validatable

El contrato deberá poder validarse automáticamente.

---

## 6.84 Prueba de conformidad contractual

Una implementación deberá poder demostrar:

1. que cada entrega tiene identidad;
2. que la respuesta conserva identidad propia;
3. que existe versión de contrato;
4. que el consumidor se identifica de manera lógica;
5. que el adaptador es identificable;
6. que los errores tienen códigos estables;
7. que la estructura puede serializarse;
8. que la estructura puede validarse;
9. que no contiene dependencias visuales;
10. que puede evolucionar sin romper arbitrariamente consumidores.

---

## 6.85 Criterio de éxito contractual

El Delivery Contract será considerado adecuado cuando un consumidor pueda recibir una respuesta y determinar, sin conocimiento de internals:

```text
what response is this?
which contract version?
which delivery operation?
which consumer context?
which trace?
what status?
what error, if any?
```

sin depender de:

- clases internas;
- estado global;
- HTML;
- implementación de capabilities;
- o convenciones informales.

---

## 6.86 Declaración arquitectónica del capítulo

El Delivery Contract representa el pacto formal entre HEYTI Runtime Response Delivery y sus consumidores autorizados.

Su función no es describir cómo se verá una respuesta.

Su función es establecer qué significa recibirla correctamente.

La regla consolidada queda establecida como:

> **HEYTI deberá entregar respuestas mediante contratos explícitos, versionados y validables que separen rigurosamente la semántica cognitiva de la información operacional de Delivery y de los detalles técnicos de transporte.**

A partir de esta definición contractual podrá formalizarse la siguiente pieza fundamental:

**la serialización y representación canónica de las respuestas entregables.**

---

**Fin del Capítulo 6**

# Capítulo 7. Serialización, representación canónica y preservación semántica

## 7.1 Propósito del capítulo

Este capítulo define las reglas arquitectónicas para la **serialización** de respuestas dentro de HEYTI Runtime Response Delivery.

La serialización constituye el proceso mediante el cual una estructura válida de Delivery se convierte en una representación apta para ser transportada, registrada, validada o consumida externamente.

El objetivo es garantizar que este proceso:

- no altere significado;
- no elimine campos obligatorios;
- preserve tipos y unidades;
- mantenga trazabilidad;
- sea determinista;
- sea validable;
- y permita interoperabilidad.

La serialización deberá considerarse una transformación de representación.

Nunca una transformación cognitiva.

---

## 7.2 Principio fundamental

La regla central será:

```text
Serialization changes form.
Serialization MUST NOT change meaning.
```

Conceptualmente:

```text
DeliveryEnvelope
      ↓
Serializer
      ↓
Serializable Representation
```

La semántica deberá permanecer equivalente.

---

## 7.3 Serialización no es materialización

Debe preservarse la separación:

```text
Materialization
      ≠
Serialization
```

Materialization responde:

> ¿Qué significa y cómo se estructura la respuesta de HEYTI?

Serialization responde:

> ¿Cómo representamos técnicamente esa estructura para entregarla?

Ejemplo:

```text
Materialization
    produces
Metric(value=61.4, unit="percent")
```

Serialization podría producir:

```json
{
  "value": 61.4,
  "unit": "percent"
}
```

El serializer no decidió que el valor fuera 61.4.

Únicamente representó algo ya determinado.

---

## 7.4 Serialización no es presentación

Debe preservarse igualmente:

```text
Serialization
      ≠
Presentation
```

Un serializer podrá producir:

```json
{
  "type": "metric",
  "label": "Participación",
  "value": 61.4,
  "unit": "percent"
}
```

Pero no deberá decidir:

```text
blue card
large font
top right position
animated gauge
```

Estas decisiones pertenecen al consumidor.

---

## 7.5 Representación canónica

HEYTI deberá contar con una representación canónica intermedia suficientemente estable.

Conceptualmente:

```text
Internal Delivery Object
        ↓
Canonical Representation
        ↓
Transport Serialization
```

La representación canónica podría basarse en:

```text
dict
list
string
number
boolean
null
```

es decir, tipos simples y estructurados ampliamente serializables.

---

## 7.6 Ventajas de una representación canónica

La representación canónica permitirá:

- comparar salidas;
- validar contratos;
- generar JSON;
- implementar adaptadores;
- construir pruebas;
- calcular hashes futuros;
- registrar auditoría;
- desacoplar modelos Python de consumidores externos.

---

## 7.7 Regla de tipos simples

La representación canónica deberá evitar exponer directamente tipos internos complejos como:

```text
Python objects
database sessions
ORM models
custom runtime classes
open file handles
network objects
```

Estos tipos deberán convertirse previamente a estructuras públicas.

---

## 7.8 Canonical Object Graph

Conceptualmente, toda estructura entregable debería poder convertirse a:

```text
CanonicalValue :=
    null
    | boolean
    | number
    | string
    | list[CanonicalValue]
    | map[string, CanonicalValue]
```

Este modelo facilita interoperabilidad.

---

## 7.9 Método conceptual to_dict()

Una implementación coherente podrá utilizar una operación como:

```python
to_dict()
```

para convertir contratos en representación canónica.

Ejemplo conceptual:

```python
delivery_envelope.to_dict()
```

podría producir:

```python
{
    "delivery": {...},
    "response": {...},
    "trace": {...}
}
```

El nombre definitivo podrá variar.

La responsabilidad deberá permanecer explícita.

---

## 7.10 Serialización en capas

La arquitectura podrá organizar la serialización en dos niveles:

```text
Contract Object
      ↓
Canonical Serializer
      ↓
Canonical Dictionary
      ↓
Format Serializer
      ↓
JSON / bytes / message
```

Esto permite separar:

- estructura contractual;
- del formato técnico final.

---

## 7.11 Canonical Serializer

El Canonical Serializer deberá encargarse de convertir los tipos internos autorizados a estructuras canónicas.

Ejemplos:

```text
Enum     → string
UUID     → string
datetime → ISO-8601 string
dataclass→ map
tuple    → list
```

Estas reglas deberán ser explícitas.

---

## 7.12 Format Serializer

El Format Serializer podrá encargarse de convertir la representación canónica a un formato de transporte.

Ejemplo:

```text
Canonical Dictionary
      ↓
JSON Serializer
      ↓
UTF-8 JSON
```

En el futuro podría existir:

```text
Canonical Dictionary
      ↓
MessagePack Serializer
```

sin alterar el contrato.

---

## 7.13 JSON como formato inicial

Para v1.0, JSON constituye una opción natural para integración con consumidores web.

La arquitectura deberá permitir:

```text
DeliveryEnvelope
      ↓
Canonical Representation
      ↓
JSON
```

Esto facilitará integración con:

- Portal;
- JavaScript;
- APIs;
- pruebas;
- herramientas externas.

---

## 7.14 JSON no define el contrato

Debe mantenerse:

```text
Delivery Contract
      ≠
JSON
```

JSON únicamente representa el contrato.

El mismo contrato podría representarse mediante otro formato en el futuro.

---

## 7.15 UTF-8

La serialización JSON deberá utilizar:

```text
UTF-8
```

como encoding base.

Esto permitirá representar correctamente:

```text
á
é
í
ó
ú
ñ
¿
¡
```

y otros caracteres necesarios.

---

## 7.16 Regla de no pérdida

La serialización deberá cumplir:

```text
Required Contract Field
      ↓
Serialization
      ↓
Required Serialized Field
```

Ninguna etapa podrá eliminar campos obligatorios por conveniencia.

---

## 7.17 Omission vs null

Debe distinguirse:

```text
field omitted
```

de:

```text
field = null
```

Si el contrato define una diferencia semántica, el serializer deberá preservarla.

Ejemplo:

```text
warning: null
```

puede significar:

> El campo existe pero no hay advertencia.

Mientras:

```text
warning omitted
```

podría significar:

> Este contrato no incluye ese campo.

La política deberá definirse explícitamente.

---

## 7.18 Regla de campos opcionales

Para campos opcionales, la arquitectura deberá definir una política consistente.

Opciones posibles:

```text
omit when absent
```

o:

```text
serialize as null
```

La implementación no deberá alternar arbitrariamente.

---

## 7.19 Booleans

Los valores booleanos deberán conservarse como:

```text
true
false
```

y no como:

```text
"true"
"false"
1
0
```

salvo que el contrato indique otra representación.

---

## 7.20 Números enteros

Los enteros deberán serializarse como números cuando representen cantidades.

Ejemplo:

```json
{
  "votes": 1842
}
```

---

## 7.21 Identificadores numéricos aparentes

Los identificadores deberán tratarse con precaución.

Ejemplo:

```text
section_id = "0012"
```

no deberá convertirse automáticamente a:

```text
12
```

si los ceros forman parte de la identidad.

Por ello, muchos identificadores deberán serializarse como string.

---

## 7.22 Números decimales

Los valores decimales deberán preservar precisión suficiente.

Ejemplo:

```text
participation = 61.4
```

No deberá sufrir conversiones arbitrarias como:

```text
61
```

o:

```text
0.614
```

salvo que exista transformación contractual explícita.

---

## 7.23 Porcentajes

Un porcentaje deberá transportar semántica clara.

Ejemplo:

```json
{
  "value": 61.4,
  "unit": "percent"
}
```

La arquitectura deberá evitar ambigüedad entre:

```text
61.4
```

y:

```text
0.614
```

---

## 7.24 Moneda

Si HEYTI llegara a manejar valores monetarios, deberá preservarse:

```text
value
currency
```

Ejemplo:

```json
{
  "value": 300.0,
  "currency": "MXN"
}
```

Nunca deberá inferirse la moneda únicamente por contexto visual.

---

## 7.25 Fechas

Las fechas deberán utilizar una representación no ambigua.

Ejemplo:

```text
2026-08-20
```

Preferiblemente ISO-8601.

---

## 7.26 DateTime

Los timestamps deberán incluir zona horaria cuando corresponda.

Ejemplo:

```text
2026-08-20T15:30:00-06:00
```

Debe evitarse:

```text
2026-08-20 15:30
```

si el huso horario es relevante.

---

## 7.27 UTC vs zona local

La arquitectura deberá establecer una política temporal consistente.

Podrá decidir:

```text
always UTC
```

o:

```text
preserve offset-aware timestamps
```

Lo importante es evitar timestamps ingenuos y ambiguos.

---

## 7.28 Enums

Los enumerados deberán representarse mediante valores públicos estables.

Ejemplo:

```text
DeliveryStatus.DELIVERED
```

podrá serializarse como:

```text
"DELIVERED"
```

No deberá serializarse mediante representaciones internas como:

```text
"<DeliveryStatus.DELIVERED: 1>"
```

---

## 7.29 Strings

Las cadenas deberán preservar contenido.

La serialización podrá aplicar escaping técnico necesario.

Ejemplo:

```text
"Sección \"1481\""
```

podrá representarse válidamente en JSON.

El escaping no cambia significado.

---

## 7.30 Whitespace

El contrato no deberá depender de espacios de presentación.

Los serializers podrán producir:

```text
pretty JSON
```

o:

```text
compact JSON
```

sin cambiar semántica.

---

## 7.31 Pretty vs compact

Ejemplo pretty:

```json
{
  "status": "DELIVERED"
}
```

Ejemplo compact:

```json
{"status":"DELIVERED"}
```

Ambos deberán ser equivalentes.

---

## 7.32 Orden de propiedades

El orden de propiedades no deberá poseer significado contractual.

Sin embargo, para:

- pruebas snapshot;
- hashes;
- auditoría;

podrá definirse posteriormente una canonicalización ordenada.

No deberá confundirse orden técnico con semántica.

---

## 7.33 Listas

Las listas sí deberán preservar orden cuando el dominio lo requiera.

Ejemplo:

```text
historical_series:
2018
2021
2024
```

No deberá reordenarse arbitrariamente.

---

## 7.34 Sets

Los conjuntos internos deberán convertirse cuidadosamente.

Un `set` no posee orden garantizado.

Si el contrato requiere orden determinista:

```text
set
 ↓
sorted list
```

podría ser necesario.

La regla deberá documentarse.

---

## 7.35 Diccionarios

Los mapas deberán utilizar claves textuales públicas.

Se deberá evitar:

```text
object instance as key
```

o claves no serializables.

---

## 7.36 Nested Structures

Las estructuras anidadas deberán permanecer comprensibles.

Ejemplo:

```text
response
  ├── content
  │    ├── summary
  │    ├── metrics
  │    └── evidence
  └── metadata
```

La profundidad excesiva deberá evitarse cuando no exista necesidad semántica.

---

## 7.37 Serialización de evidencia

La evidencia deberá serializarse conforme a su contrato.

Delivery no deberá reducir arbitrariamente:

```text
EvidenceObject
```

a:

```text
"source name"
```

si se requieren más campos.

---

## 7.38 Serialización de advertencias

Las advertencias deberán conservar:

```text
code
message
severity
origin
```

cuando esos campos existan.

No deberán convertirse únicamente a texto si ello elimina estructura útil.

---

## 7.39 Serialización de errores

Los errores de Delivery deberán serializarse mediante estructura controlada.

Ejemplo:

```json
{
  "error": {
    "code": "DELIVERY_TIMEOUT",
    "category": "TRANSPORT",
    "message": "Delivery timeout"
  }
}
```

No deberá enviarse directamente:

```text
repr(exception)
```

como contrato público.

---

## 7.40 Stack traces

Los stack traces deberán permanecer internos.

Podrán utilizarse en:

- logs;
- debugging;
- observabilidad interna.

No deberán incluirse en payload público por defecto.

---

## 7.41 Serialización de metadatos

Los metadatos deberán serializarse únicamente cuando:

- formen parte del contrato;
- sean seguros;
- sean útiles para el consumidor o auditoría.

No toda metadata interna deberá salir.

---

## 7.42 Metadata pública vs interna

La arquitectura deberá distinguir:

```text
public_metadata
```

de:

```text
internal_metadata
```

si resulta necesario.

Ejemplo:

```text
public:
knowledge_version
generated_at
```

versus:

```text
internal:
hostname
process_id
debug_flags
```

---

## 7.43 Serialización de geometría

Cuando sea necesaria geometría, deberá utilizarse un formato interoperable.

GeoJSON constituye una opción natural para:

```text
Point
LineString
Polygon
MultiPolygon
Feature
FeatureCollection
```

No obstante, la incorporación de geometría completa deberá justificarse.

---

## 7.44 GeoJSON y Presentation

GeoJSON contiene geometría y propiedades.

No deberá incluir estilos dependientes de Leaflet si el contrato central busca neutralidad.

Ejemplo preferible:

```json
{
  "type": "Feature",
  "geometry": {...},
  "properties": {
    "section_id": "1481"
  }
}
```

No:

```json
{
  "leafletStyle": {
    "fillColor": "#e91e63"
  }
}
```

---

## 7.45 Referencias en lugar de geometría completa

Cuando el consumidor ya dispone del dataset cartográfico, deberá preferirse una referencia.

Ejemplo:

```json
{
  "section_id": "1481"
}
```

en lugar de repetir un polígono grande.

Esto reduce:

- tamaño;
- duplicación;
- latencia.

---

## 7.46 Serialización de tablas

Una tabla podrá estructurarse como:

```json
{
  "columns": [
    {"key": "year", "label": "Año", "type": "integer"},
    {"key": "votes", "label": "Votos", "type": "integer"}
  ],
  "rows": [
    {"year": 2018, "votes": 1200},
    {"year": 2024, "votes": 1450}
  ]
}
```

Esta forma puede ser más robusta que arrays posicionales cuando se requiere evolución.

---

## 7.47 Arrays posicionales

También podrán utilizarse arrays posicionales cuando el contrato sea simple.

Ejemplo:

```json
{
  "columns": ["year", "votes"],
  "rows": [
    [2018, 1200],
    [2024, 1450]
  ]
}
```

La elección deberá ser consistente.

---

## 7.48 Serialización de series

Las series deberán preservar correspondencia entre ejes y valores.

Ejemplo:

```json
{
  "categories": [2018, 2021, 2024],
  "values": [55.4, 57.2, 61.4]
}
```

Debe garantizarse:

```text
len(categories) == len(values)
```

cuando el contrato lo requiera.

---

## 7.49 Datos faltantes en series

Un dato faltante no deberá convertirse automáticamente a cero.

Ejemplo correcto:

```json
{
  "values": [55.4, null, 61.4]
}
```

si 2021 no tiene dato.

Incorrecto:

```json
{
  "values": [55.4, 0, 61.4]
}
```

si cero no representa una medición real.

---

## 7.50 Serialización de acciones

Las acciones abstractas deberán convertirse a estructuras declarativas.

Ejemplo:

```json
{
  "action": "OPEN_MODULE",
  "target": "TERRITORIAL",
  "context": {
    "section_id": "1481"
  }
}
```

No deberá serializarse código ejecutable.

---

## 7.51 Seguridad de acciones

El consumidor deberá validar qué acciones está autorizado a ejecutar.

Delivery transporta la acción.

No concede automáticamente autoridad.

---

## 7.52 Serialización determinista

La arquitectura deberá buscar determinismo suficiente para que:

```text
same contract state
      ↓
same canonical representation
```

excluyendo elementos variables como:

```text
timestamps
delivery_id
duration
```

---

## 7.53 Determinismo y pruebas

El determinismo facilitará:

```text
expected
   ==
actual
```

en pruebas unitarias.

También facilitará:

- snapshots;
- auditoría;
- comparación de regresiones.

---

## 7.54 Serializer Registry

Si aparecen múltiples formatos, podrá existir:

```text
SerializerRegistry
├── JSON
├── INTERNAL
└── FUTURE
```

No deberá confundirse con:

```text
CapabilityRegistry
```

ni con:

```text
DeliveryAdapterRegistry
```

---

## 7.55 Serializer ID

Podrá existir:

```text
serializer_id
```

si resulta útil para observabilidad.

Ejemplo:

```text
JSON_V1
```

No deberá añadirse si no aporta valor.

---

## 7.56 Serializer Version

Una política de serialización podrá necesitar versión si cambian reglas sin cambiar el contrato.

Ejemplo:

```text
serializer_version
```

Sin embargo, deberá evitarse proliferación innecesaria de versiones.

La prioridad debe ser mantener el contrato como autoridad.

---

## 7.57 Validation After Serialization

Después de serializar, deberá poder verificarse:

```text
is valid JSON?
```

y:

```text
does it conform to Delivery Contract?
```

cuando aplique.

---

## 7.58 Round-Trip Validation

La arquitectura podrá considerar pruebas de round-trip:

```text
Object
  ↓ serialize
JSON
  ↓ deserialize
Canonical Object
```

y verificar equivalencia semántica.

Esto será útil para contratos críticos.

---

## 7.59 Round-Trip no siempre implica identidad de objeto

No se requiere que:

```text
original Python object
==
deserialized Python object
```

en identidad interna.

Se requiere preservar:

```text
contract semantics
```

---

## 7.60 Serializer Errors

Los errores de serialización deberán clasificarse.

Ejemplos conceptuales:

```text
UNSUPPORTED_TYPE
INVALID_TEMPORAL_VALUE
INVALID_ENUM
INVALID_NESTED_STRUCTURE
ENCODING_ERROR
```

Podrán mapearse al código general:

```text
DELIVERY_SERIALIZATION_ERROR
```

con detalle interno.

---

## 7.61 Unsupported Type

Si un tipo no puede serializarse, el serializer deberá fallar explícitamente.

No deberá convertir automáticamente cualquier objeto a:

```text
str(object)
```

porque esto puede destruir estructura.

---

## 7.62 Fallbacks controlados

Los fallbacks únicamente serán permitidos si están especificados por política.

Ejemplo permitido:

```text
Enum unknown
→ serialization failure
```

Preferible a:

```text
Enum unknown
→ "UNKNOWN_OBJECT"
```

inventado silenciosamente.

---

## 7.63 Circular References

Las estructuras contractuales no deberán contener referencias circulares.

Ejemplo problemático:

```text
A → B → A
```

Los validadores deberán detectar o impedir este patrón.

---

## 7.64 Payload Size

La serialización deberá poder medir:

```text
payload_size_bytes
```

cuando sea necesario.

Esto permitirá identificar respuestas excesivamente grandes.

---

## 7.65 Límites de tamaño

Los límites deberán pertenecer a:

```text
DeliveryPolicy
```

o al adaptador.

No deberán fijarse arbitrariamente dentro del serializer sin gobernanza.

---

## 7.66 Large Payload Handling

Una respuesta muy grande podrá requerir en el futuro:

```text
reference delivery
chunking
streaming
compression
```

No deberá resolverse automáticamente en v1.0 sin necesidad real.

---

## 7.67 Compresión

La compresión ocurre después de serialización:

```text
Canonical Object
      ↓
JSON
      ↓
Compression
      ↓
Transport
```

No deberá considerarse parte de la semántica del serializer.

---

## 7.68 Encriptación

De forma similar:

```text
JSON
 ↓
Encryption
 ↓
Transport
```

pertenece a infraestructura.

No a materialización ni serialización semántica.

---

## 7.69 Content Type

Un adaptador HTTP podría declarar:

```text
application/json
```

pero `Content-Type` pertenece al transporte.

No al contrato cognitivo.

---

## 7.70 MIME y neutralidad

El Delivery Contract deberá permanecer independiente de MIME types específicos cuando no sean necesarios.

---

## 7.71 Canonical JSON

Si en el futuro se requieren:

- firmas;
- hashes;
- comparación byte a byte;

podrá definirse una política de Canonical JSON.

Esta política podría fijar:

```text
key ordering
number formatting
whitespace
escaping
```

No forma parte obligatoria de v1.0.

---

## 7.72 Payload Hash

Si se utiliza un hash:

```text
payload_hash = hash(canonical_payload)
```

deberá calcularse sobre una representación canónica formal.

No sobre una salida arbitraria de pretty-print.

---

## 7.73 Preservación de procedencia

Campos como:

```text
source
dataset_version
knowledge_version
evidence_id
data_as_of
```

deberán sobrevivir al proceso cuando formen parte del contrato.

---

## 7.74 Preservación de advertencias

La serialización deberá incluir advertencias conforme al contrato.

Nunca deberán omitirse por razones de:

```text
payload size
clean UI
simplicity
```

sin una política contractual explícita.

---

## 7.75 Preservación de confianza

Cuando exista un campo de confianza:

```text
confidence
```

deberá serializarse sin reinterpretación.

No deberá convertirse:

```text
LOW → 0
MEDIUM → 1
HIGH → 2
```

salvo que ese mapping forme parte del contrato.

---

## 7.76 Preservación de orden semántico

Cuando el orden tenga significado deberá conservarse.

Ejemplos:

```text
ranking
chronological sequence
priority list
steps
```

El serializer no deberá ordenar alfabéticamente por comodidad.

---

## 7.77 Localization

La serialización no deberá localizar números o fechas para presentación.

Ejemplo incorrecto dentro del Core:

```text
1,842 votos
```

como único valor.

Preferible:

```json
{
  "value": 1842,
  "unit": "votes"
}
```

La UI podrá mostrar:

```text
1,842 votos
```

o:

```text
1 842 votes
```

según idioma y locale.

---

## 7.78 Idioma del contenido narrativo

El contenido textual generado por HEYTI podrá tener idioma definido.

Ejemplo:

```text
language = "es-MX"
```

si el contrato lo requiere.

Delivery deberá preservarlo.

---

## 7.79 Locale no es semántica cognitiva

Delivery no deberá reescribir contenido automáticamente para otro locale salvo que exista una capa autorizada específica.

---

## 7.80 Versiones y serialización

El serializer deberá conocer la versión contractual que está representando.

Conceptualmente:

```text
serialize(contract_version="1.0")
```

No deberá asumir siempre la versión más nueva.

---

## 7.81 Compatibilidad

Un serializer podrá soportar varias versiones.

Ejemplo:

```text
JSONSerializer
├── DeliveryContract 1.0
└── DeliveryContract 1.1
```

Si una versión no es soportada deberá producir error explícito.

---

## 7.82 Forward Compatibility

La representación deberá evitar decisiones que impidan añadir campos opcionales en futuras versiones.

---

## 7.83 Backward Compatibility

Un consumidor de versión anterior no deberá recibir una estructura incompatible sin negociación o adaptación explícita.

---

## 7.84 Serialización de DeliveryResult

El resultado de Delivery también deberá poder serializarse.

Ejemplo:

```json
{
  "delivery_id": "DEL-001",
  "status": "DELIVERED"
}
```

Esto será útil para:

- API;
- pruebas;
- auditoría.

---

## 7.85 DeliveryResult exitoso

La representación exitosa deberá evitar incluir errores falsos.

Conceptualmente:

```text
status = DELIVERED
error  = null
```

---

## 7.86 DeliveryResult fallido

Ejemplo:

```text
status = FAILED
error != null
```

La validación deberá comprobar consistencia.

---

## 7.87 Serialización de REJECTED

Un rechazo deberá conservar información suficiente para saber por qué la operación no cruzó la frontera.

---

## 7.88 No serializar excepciones internas directamente

Debe evitarse:

```python
{
    "error": exception.__dict__
}
```

Las excepciones deberán mapearse a contratos públicos controlados.

---

## 7.89 Separación Serializer / Error Mapper

Podrá existir:

```text
Exception
   ↓
Error Mapper
   ↓
DeliveryError
   ↓
Serializer
```

El serializer no debería decidir semántica de errores.

---

## 7.90 Separación Serializer / Validator

También deberá distinguirse:

```text
Validator
```

de:

```text
Serializer
```

El validator responde:

> ¿Es válida esta estructura?

El serializer responde:

> ¿Cómo la represento?

---

## 7.91 Serializer no corrige

Si el validator detecta:

```text
missing response_id
```

el serializer no deberá inventarlo.

---

## 7.92 Serialización y logs

Los logs no deberán utilizar el serializer público para volcar automáticamente todo el payload.

El logging deberá tener política propia.

Esto evita exponer:

- PII;
- evidencia;
- contenido sensible.

---

## 7.93 Safe Logging Representation

Podrá existir una vista resumida para logs:

```text
delivery_id
response_id
consumer_id
status
payload_size
```

sin incluir `response.content`.

---

## 7.94 Auditoría

La auditoría podrá requerir una representación más completa que logging.

Deberán distinguirse ambos propósitos.

---

## 7.95 Test vectors

La arquitectura deberá desarrollar ejemplos canónicos de serialización.

Ejemplo:

```text
Known DeliveryEnvelope
      ↓
Expected Canonical Dictionary
      ↓
Expected JSON semantics
```

Estos ejemplos servirán como test vectors.

---

## 7.96 Golden Files

En el futuro podrán utilizarse archivos golden para detectar cambios no intencionales.

Por ejemplo:

```text
tests/fixtures/delivery/v1/
```

La introducción deberá realizarse si resulta útil para control de regresiones.

---

## 7.97 Property-Based Testing

Las estructuras contractuales podrían beneficiarse posteriormente de pruebas generativas.

Por ejemplo:

```text
serialize(valid_contract)
must never lose required fields
```

No es obligatorio para v1.0.

---

## 7.98 Fuzz Testing

En etapas de endurecimiento se podrá probar:

- strings extremos;
- listas grandes;
- Unicode;
- valores nulos;
- tipos inválidos.

Esto fortalecerá la frontera.

---

## 7.99 Canonical Serializer v1.0 mínimo

Para la primera implementación se recomienda soportar únicamente:

```text
None
bool
int
float
str
list
dict
Enum
UUID
datetime
date
dataclass / approved contract object
```

Cualquier otro tipo deberá:

```text
fail explicitly
```

salvo adaptación formal.

---

## 7.100 No generic magic serializer

Deberá evitarse una estrategia excesivamente permisiva como:

```python
json.dumps(obj, default=str)
```

para toda la arquitectura.

Aunque técnicamente funcione, puede ocultar tipos no soportados y destruir semántica.

---

## 7.101 Arquitectura recomendada

Conceptualmente:

```text
┌──────────────────────────────┐
│ DeliveryEnvelope             │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Delivery Contract Validator  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Canonical Serializer         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Canonical Representation     │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ JSON Serializer              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ JSON Payload                 │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Payload Validator            │
└──────────────────────────────┘
```

---

## 7.102 Invariantes de serialización

Se establecen los siguientes invariantes.

### HRRD-S01 — Semantic Preservation

Serializar nunca deberá alterar significado.

### HRRD-S02 — Required Field Preservation

Ningún campo obligatorio podrá perderse.

### HRRD-S03 — Explicit Type Mapping

Los tipos deberán convertirse mediante reglas conocidas.

### HRRD-S04 — Unsupported Type Failure

Los tipos desconocidos deberán fallar explícitamente.

### HRRD-S05 — Deterministic Representation

La representación deberá ser consistente.

### HRRD-S06 — Temporal Explicitness

Fechas y timestamps deberán representarse sin ambigüedad.

### HRRD-S07 — Null Preservation

Los valores nulos deberán conservar semántica.

### HRRD-S08 — Identifier Preservation

Los identificadores no deberán sufrir conversiones destructivas.

### HRRD-S09 — Presentation Neutrality

La serialización no incorporará detalles visuales específicos.

### HRRD-S10 — Validation Before Boundary

El payload serializado deberá poder validarse antes de ser entregado.

---

## 7.103 Prueba de no pérdida

Para una respuesta `R`, deberá poder verificarse conceptualmente:

```text
meaning(R)
=
meaning(deserialize(serialize(R)))
```

dentro de los límites del contrato público.

Esta será la **Semantic Round-Trip Rule**.

---

## 7.104 Prueba de neutralidad visual

Un payload será considerado neutral cuando pueda ser consumido por:

```text
Portal
CLI
Test Harness
Future UI
```

sin requerir cambiar su contenido semántico.

---

## 7.105 Prueba de independencia tecnológica

El serializer deberá poder ejecutarse sin:

```text
browser
DOM
Leaflet
Chart.js
HTTP server
```

Si requiere alguno de estos elementos, deberá revisarse la separación arquitectónica.

---

## 7.106 Prueba de estabilidad

Dados los mismos valores contractuales:

```text
serialize(A)
```

y:

```text
serialize(A)
```

deberán producir representaciones equivalentes.

---

## 7.107 Prueba de error explícito

Dado un objeto no soportado:

```text
UnsupportedObject
```

el resultado deberá ser:

```text
SerializationError
```

y no:

```text
"<UnsupportedObject object at 0x...>"
```

---

## 7.108 Flujo de serialización exitoso

```text
DeliveryEnvelope
      │
      ▼
Contract Validation
      │
      ▼
Canonical Serializer
      │
      ▼
Canonical Representation
      │
      ▼
JSON Serializer
      │
      ▼
UTF-8 JSON Payload
      │
      ▼
Payload Validation
      │
      ▼
READY FOR DELIVERY
```

---

## 7.109 Flujo de serialización fallido

```text
DeliveryEnvelope
      │
      ▼
Canonical Serializer
      │
      ▼
Unsupported Type
      │
      ▼
SerializationError
      │
      ▼
DeliveryResult
      │
      ▼
FAILED
```

La frontera externa no deberá cruzarse.

---

## 7.110 Relación con el Pipeline

Dentro del pipeline general:

```text
Entry Validation
      ↓
Envelope Construction
      ↓
Normalization
      ↓
SERIALIZATION
      ↓
Payload Validation
      ↓
Adapter Resolution
```

La serialización deberá ser una etapa claramente identificable.

---

## 7.111 Relación con DeliveryAdapter

El adaptador deberá recibir un payload ya preparado.

Preferido:

```text
Serializer
   ↓
Validated Payload
   ↓
Adapter
```

No:

```text
Adapter
   ↓
random object
   ↓
adapter invents serialization
```

Esto evita divergencias entre adaptadores.

---

## 7.112 Excepción controlada

Un adaptador podrá aplicar framing técnico adicional.

Ejemplo WebSocket:

```text
JSON Payload
      ↓
WebSocket Frame
```

Pero no deberá redefinir la serialización contractual.

---

## 7.113 Relación con consumidores AT 27–30

La serialización neutral permitirá que consumidores actuales o futuros transformen:

```text
metrics
series
territorial references
tables
actions
```

en componentes visuales especializados.

Por ejemplo:

```text
HEYTI Series
      ↓
Delivery JSON
      ↓
Portal Adapter
      ↓
Chart.js
```

o:

```text
HEYTI Territorial Reference
      ↓
Delivery JSON
      ↓
Portal Adapter
      ↓
Leaflet
```

HEYTI-CORE permanece independiente.

---

## 7.114 Regla para gráficas

HEYTI deberá entregar:

```text
data
```

y no necesariamente:

```text
chart configuration
```

La diferencia deberá conservarse como principio permanente.

---

## 7.115 Regla para mapas

HEYTI deberá entregar:

```text
territorial semantics
geometry or reference
```

no:

```text
Leaflet instructions
```

---

## 7.116 Regla para KPIs

HEYTI podrá entregar:

```text
label
value
unit
semantic status
```

La UI decide si se representa:

- grande;
- pequeño;
- con color;
- con icono.

---

## 7.117 Regla para tablas

HEYTI podrá entregar datos tabulares estructurados.

La UI decide:

- paginación;
- ancho de columna;
- color;
- orden visual;
- scroll.

---

## 7.118 Regla de honestidad

Si un dato no está disponible:

```text
null
```

deberá permanecer como tal conforme al contrato.

El serializer no deberá transformarlo a:

```text
0
"N/A"
"Sin dato"
```

si esas son decisiones de presentación.

---

## 7.119 Diferencia entre dato y etiqueta visual

Ejemplo:

```text
null
```

es dato contractual.

```text
"Sin información disponible"
```

puede ser una representación visual decidida posteriormente.

---

## 7.120 Criterio de implementación mínima

Para v1.0, deberá ser posible ejecutar:

```python
payload = serializer.serialize(delivery_envelope)
```

y obtener una estructura:

```text
valid
JSON-compatible
deterministic
contract-preserving
```

sin requerir infraestructura externa.

---

## 7.121 Tests mínimos esperados

La futura implementación deberá incluir pruebas equivalentes a:

```text
test_serialize_successful_delivery
test_serialize_failed_delivery
test_preserves_response_id
test_preserves_delivery_id
test_serializes_datetime
test_serializes_enum
test_serializes_uuid
test_preserves_null
test_rejects_unsupported_type
test_preserves_required_fields
test_json_round_trip
```

---

## 7.122 Pruebas de no omisión

Deberán existir pruebas explícitas para confirmar que campos obligatorios:

```text
response
trace
warnings
contract_version
```

no desaparecen durante serialización.

---

## 7.123 Pruebas de neutralidad

Podrá comprobarse que el payload no contenga campos prohibidos como:

```text
css_class
dom_id
canvas_id
leaflet_layer
chartjs_options
onclick
```

salvo que una futura especificación externa lo autorice.

---

## 7.124 Criterio de éxito

La serialización será correcta cuando una respuesta pueda transformarse desde su estructura contractual interna hacia una representación pública entregable sin:

- pérdida;
- reinterpretación;
- dependencia visual;
- ambigüedad temporal;
- corrupción de identificadores;
- ni ocultamiento de errores.

---

## 7.125 Declaración arquitectónica del capítulo

La serialización de Runtime Response Delivery deberá actuar como una frontera técnica rigurosa entre el contrato interno y su representación entregable.

No deberá convertirse en una segunda materialización.

No deberá convertirse en una capa de presentación.

No deberá actuar como mecanismo silencioso de reparación.

Su responsabilidad es más precisa:

> **Convertir estructuras contractualmente válidas en representaciones canónicas y transportables, preservando íntegramente su significado, identidad, trazabilidad, temporalidad y estructura pública.**

La regla final queda establecida como:

```text
Materialized Meaning
      ↓
Delivery Contract
      ↓
Canonical Representation
      ↓
Serialized Payload
      ↓
Same Meaning
```

Sobre esta base podrá definirse con precisión el siguiente componente crítico de Runtime Response Delivery:

**la validación formal de entrada, contrato, payload y salida.**

---

**Fin del Capítulo 7**

# Capítulo 8. Validación formal de entrada, contrato, payload y salida

## 8.1 Propósito del capítulo

Este capítulo define la arquitectura de validación de **HEYTI Runtime Response Delivery (HRRD)**.

La validación constituye el mecanismo mediante el cual HEYTI determina si una respuesta, una operación de entrega, un payload y un resultado cumplen las reglas contractuales necesarias para avanzar dentro del pipeline.

El objetivo no es únicamente detectar errores.

El objetivo es impedir que una estructura inválida cruce una frontera arquitectónica y genere:

- pérdida de trazabilidad;
- corrupción semántica;
- respuestas incompletas;
- errores difíciles de atribuir;
- incompatibilidades con consumidores;
- o entregas técnicamente exitosas pero contractualmente defectuosas.

La regla fundamental será:

> **Cada frontera valida aquello que le corresponde antes de delegar responsabilidad a la siguiente.**

---

## 8.2 Validación por fronteras

La arquitectura deberá evitar una única validación monolítica.

Deberán existir validaciones diferenciadas para:

```text
Materialized Response
Delivery Request
Delivery Context
Consumer Compatibility
Delivery Envelope
Serialized Payload
Adapter Result
Delivery Result
```

Conceptualmente:

```text
Response
   ↓
Response Validation
   ↓
DeliveryRequest
   ↓
Request Validation
   ↓
Envelope
   ↓
Envelope Validation
   ↓
Payload
   ↓
Payload Validation
   ↓
Adapter
   ↓
Adapter Result Validation
   ↓
DeliveryResult
```

Cada etapa valida invariantes diferentes.

---

## 8.3 Principio de responsabilidad local

Una etapa no deberá intentar validar responsabilidades pertenecientes a otras fronteras si ello genera acoplamiento.

Ejemplo:

`PayloadValidator` podrá verificar:

```text
required fields
types
schema version
encoding
```

pero no deberá decidir:

```text
"¿Es correcta la interpretación electoral de esta respuesta?"
```

Ese problema pertenece al dominio cognitivo.

---

## 8.4 Tipos de validación

Se establecen conceptualmente los siguientes tipos:

```text
Structural Validation
Contract Validation
Semantic Contract Validation
Context Validation
Compatibility Validation
Serialization Validation
Transport Result Validation
Result Consistency Validation
```

La palabra "semantic" en este capítulo deberá entenderse exclusivamente como semántica del contrato de Delivery.

No como razonamiento cognitivo.

---

## 8.5 Structural Validation

La validación estructural deberá comprobar la forma básica de una entidad.

Ejemplos:

```text
object exists
field exists
field type is valid
collection has expected shape
```

Ejemplo:

```text
delivery_id exists
```

o:

```text
response is an object
```

---

## 8.6 Contract Validation

La validación contractual deberá verificar que la entidad cumple el contrato vigente.

Por ejemplo:

```text
delivery_contract_version = "1.0"
```

deberá corresponder a un schema o modelo soportado.

La estructura no deberá aceptarse únicamente porque "parece correcta".

---

## 8.7 Semantic Contract Validation

Además de tipos y campos, algunas combinaciones deberán obedecer reglas de consistencia.

Ejemplo:

```text
status = FAILED
⇒ error != null
```

o:

```text
status = DELIVERED
⇒ delivery_id != null
```

Estas son invariantes semánticas del contrato.

---

## 8.8 Validación de MaterializedResponse

Antes de iniciar Delivery deberá comprobarse que la respuesta materializada es elegible.

Podrán validarse:

```text
response != null
response_id exists
response contract version supported
response status valid
required content exists
required metadata exists
traceability available
```

Delivery no deberá intentar completar los campos faltantes.

---

## 8.9 MaterializedResponse inválida

Ejemplo:

```text
response_id = null
```

si `response_id` es obligatorio.

Resultado:

```text
DeliveryRejected
code = DELIVERY_VALIDATION_ERROR
```

No deberá generarse:

```text
response_id = random UUID
```

dentro de Delivery si esa identidad corresponde a Materialization.

---

## 8.10 Validación del DeliveryRequest

El `DeliveryRequest` deberá validarse antes de comenzar el pipeline.

Como mínimo:

```text
delivery_id exists
response exists
target exists
consumer context valid
policy valid
```

La implementación podrá generar `delivery_id` antes de esta validación.

---

## 8.11 Validación de delivery_id

Cuando el identificador sea requerido deberá comprobarse:

```text
not null
not empty
valid format if applicable
stable
```

No deberá depender de información visual.

---

## 8.12 Validación del DeliveryContext

El contexto deberá verificar que la información necesaria para una operación esté presente.

Ejemplos:

```text
consumer_id
session_id
principal_id
correlation_id
```

según política.

Un contexto incompleto deberá generar rechazo antes del transporte.

---

## 8.13 Validación condicional del contexto

No todos los campos serán obligatorios siempre.

Ejemplo:

```text
session_id
```

podría ser obligatorio para un consumidor interactivo y opcional para una prueba `InMemory`.

Por tanto:

```text
Context Requirements
=
Delivery Policy
+
Consumer Profile
+
Contract Version
```

---

## 8.14 Validación del consumidor

El consumidor deberá estar reconocido.

Ejemplo:

```text
consumer_id = "AT_PORTAL"
```

deberá corresponder a un consumidor registrado o permitido.

Un consumidor desconocido deberá provocar:

```text
DELIVERY_UNSUPPORTED_CONSUMER
```

o código equivalente.

---

## 8.15 Validación del ConsumerProfile

El perfil podrá comprobar:

```text
supported_contract_versions
supported_content_types
required capabilities
adapter compatibility
```

No deberá validar preferencias visuales específicas.

---

## 8.16 Compatibility Validation

La compatibilidad deberá responder:

> ¿Este consumidor puede interpretar correctamente esta entrega?

Ejemplo:

```text
DeliveryContract = 1.0
Consumer supports = [1.0, 1.1]
```

Resultado:

```text
COMPATIBLE
```

---

## 8.17 Incompatibilidad contractual

Ejemplo:

```text
DeliveryContract = 2.0
Consumer supports = [1.0]
```

Resultado:

```text
REJECTED
DELIVERY_CONTRACT_MISMATCH
```

La entrega no deberá continuar.

---

## 8.18 Validación por Content Types

Supóngase que una respuesta requiere:

```text
text
metric
territorial_reference
```

y el consumidor soporta:

```text
text
metric
```

Si `territorial_reference` es obligatorio:

```text
INCOMPATIBLE
```

Si es opcional y una política contractual permite omitirlo:

```text
COMPATIBLE WITH AUTHORIZED PROJECTION
```

La decisión deberá ser explícita.

---

## 8.19 No degradación silenciosa

Queda prohibido:

```text
Consumer unsupported field
      ↓
drop field
      ↓
send anyway
```

La degradación deberá estar regida por una proyección contractual autorizada.

---

## 8.20 Validación del DeliveryEnvelope

Después de construir el envelope deberá comprobarse que todos sus bloques sean consistentes.

Ejemplo:

```text
delivery.delivery_id
response.response_id
trace.response_id
```

si aparecen en varios lugares, deberán ser coherentes.

---

## 8.21 Regla de identidad consistente

Si se mantiene referencia duplicada por razones contractuales:

```text
delivery.response_id
=
response.response_id
```

deberá validarse.

Cualquier discrepancia deberá detener el pipeline.

---

## 8.22 Validación de versiones

Deberá verificarse:

```text
delivery_contract_version supported
response_contract_version supported
serializer supports version
adapter supports representation
consumer supports version
```

Una versión debe ser entendida por todos los componentes necesarios del flujo.

---

## 8.23 Matriz de compatibilidad

Conceptualmente podrá existir:

| Response Contract | Delivery Contract | Serializer | Consumer | Resultado |
|---|---|---|---|---|
| 1.0 | 1.0 | Sí | Sí | Válido |
| 1.1 | 1.0 | Sí | Sí | Válido si política lo permite |
| 2.0 | 1.0 | No | Sí | Rechazar |
| 1.0 | 2.0 | Sí | No | Rechazar |

La matriz real deberá formalizarse en el capítulo de versionado.

---

## 8.24 Validación de campos obligatorios

Todo campo REQUIRED deberá verificarse.

Ejemplo conceptual:

```text
delivery_id            REQUIRED
delivery_contract_version REQUIRED
response               REQUIRED
consumer_id            REQUIRED
status                 REQUIRED
```

La ausencia de cualquiera deberá generar error controlado.

---

## 8.25 Validación de campos condicionales

Ejemplo:

```text
if status == FAILED:
    error MUST exist
```

y:

```text
if status == DELIVERED:
    error SHOULD be null
```

según política final.

---

## 8.26 Validación de enums

Los valores enumerados deberán pertenecer al conjunto permitido.

Ejemplo:

```text
status ∈ {
  DELIVERED,
  REJECTED,
  FAILED
}
```

No deberá aceptarse:

```text
"OK"
```

si no está definido.

---

## 8.27 Validación de timestamps

Los timestamps deberán ser:

```text
valid
timezone-aware when required
ordered consistently
```

Ejemplo:

```text
started_at <= completed_at
```

---

## 8.28 Validación temporal

Ejemplo inválido:

```text
started_at   = 16:00
completed_at = 15:59
```

salvo que exista una explicación de clocks distribuidos formalmente soportada.

En v1.0 deberá evitarse esa complejidad.

---

## 8.29 Validación de duración

Si existe:

```text
duration_ms
```

deberá ser:

```text
>= 0
```

y coherente con timestamps dentro de tolerancias definidas.

---

## 8.30 Validación de identificadores

Identificadores como:

```text
request_id
session_id
execution_id
response_id
delivery_id
```

deberán validarse estructuralmente.

No deberán validarse mediante reglas de negocio ajenas.

---

## 8.31 Validación de section_id

Si `section_id` forma parte del contenido de respuesta, Delivery podrá verificar únicamente su tipo contractual.

Ejemplo:

```text
must be non-empty string
```

Delivery no deberá consultar la base territorial para saber si la sección existe.

Eso pertenece a otro dominio.

---

## 8.32 Validación de unidades

Si un `metric` declara:

```text
unit = "percent"
```

el contrato podrá validar que `unit` pertenezca a un vocabulario permitido.

No deberá recalcular el porcentaje.

---

## 8.33 Validación de series

Podrán verificarse invariantes estructurales.

Ejemplo:

```text
len(categories) == len(values)
```

o:

```text
all series values are serializable
```

No deberá analizarse la tendencia.

---

## 8.34 Validación de tablas

Podrán comprobarse:

```text
columns defined
row shape compatible
types valid
```

No deberá decidirse qué columnas son "importantes".

---

## 8.35 Validación de territorial_reference

Podrá comprobarse:

```text
type
identifier presence
schema
```

No deberá abrir Leaflet ni cargar GeoJSON para validar Presentation.

---

## 8.36 Validación de geometry

Si el contrato soporta GeoJSON, podrá validarse que la estructura cumpla el schema autorizado.

Ejemplo:

```text
Feature
geometry
coordinates
```

No deberá evaluar estética cartográfica.

---

## 8.37 Validación de action

Una acción deberá pertenecer a un catálogo permitido.

Ejemplo:

```text
OPEN_MODULE
SHOW_SECTION
DISPLAY_CONTEXT
```

Queda prohibido aceptar cualquier string arbitrario como acción ejecutable.

---

## 8.38 Validación de action context

El contexto de una acción también deberá ajustarse al contrato.

Ejemplo:

```text
OPEN_MODULE
requires:
module
```

y:

```text
SHOW_SECTION
requires:
section_id
```

---

## 8.39 Validación de seguridad de acciones

La validación contractual no sustituye autorización.

La secuencia podrá ser:

```text
Action Contract Valid
      ↓
Authorization Policy
      ↓
Consumer decides whether to execute
```

---

## 8.40 Validación de warnings

Las advertencias deberán poseer estructura válida.

Ejemplo:

```text
code
message
origin
severity
```

cuando dichos campos estén definidos.

---

## 8.41 Validación de evidence

La validación deberá respetar el contrato de evidencia ya materializado.

Delivery no deberá volver a calificar evidencia.

---

## 8.42 Validación del Canonical Representation

Después de normalización deberá verificarse que la estructura solamente contenga tipos canónicos soportados.

Conceptualmente:

```text
null
boolean
number
string
list
map
```

Si permanece un objeto interno:

```text
CustomPythonObject
```

la validación deberá fallar antes del format serializer.

---

## 8.43 Validación pre-serialización

Podrá existir una validación como:

```text
is_canonical(value)
```

que recorra la estructura.

Si encuentra:

```text
file handle
database connection
function
class instance not approved
```

deberá producir error.

---

## 8.44 Validación JSON

Después de serializar:

```text
json payload
```

deberá verificarse al menos que:

```text
serialization succeeded
encoding valid
payload not empty when prohibited
```

---

## 8.45 Schema Validation del payload

Idealmente:

```text
payload
  ↓
schema validator
  ↓
VALID / INVALID
```

El schema deberá corresponder a la versión contractual.

---

## 8.46 Payload inválido

Un payload inválido deberá producir:

```text
DeliveryResult = FAILED
error = DELIVERY_SERIALIZATION_ERROR
```

o:

```text
DELIVERY_PAYLOAD_VALIDATION_ERROR
```

si se adopta un código separado.

La taxonomía definitiva deberá evitar granularidad innecesaria.

---

## 8.47 Validación de tamaño

La política podrá establecer:

```text
max_payload_size
```

Si se excede:

```text
FAILED
```

o:

```text
REJECTED
```

según la fase donde se compruebe.

La clasificación deberá ser consistente.

---

## 8.48 Validación del Adapter

Antes de utilizarlo deberá verificarse:

```text
adapter exists
adapter enabled
adapter supports target
adapter supports payload format
adapter contract version compatible
```

---

## 8.49 Adapter no disponible

Ejemplo:

```text
target = AT_PORTAL
required adapter = HTTP_JSON
registered adapters = [IN_MEMORY]
```

Resultado:

```text
REJECTED
DELIVERY_ADAPTER_NOT_AVAILABLE
```

o código equivalente.

---

## 8.50 Validación de AdapterResult

El resultado técnico del adaptador deberá cumplir una interfaz esperada.

Ejemplo conceptual:

```text
success
status_code
receipt
error
metadata
```

No deberá confiarse ciegamente en cualquier estructura retornada.

---

## 8.51 AdapterResult inconsistente

Ejemplo inválido:

```text
success = true
error = CONNECTION_FAILED
```

El mapper deberá detectar inconsistencias.

---

## 8.52 Validación de DeliveryResult

Antes de devolver el resultado final deberá comprobarse que sea internamente consistente.

Ejemplos:

```text
DELIVERED
⇒ error is null
```

```text
FAILED
⇒ error exists
```

```text
REJECTED
⇒ adapter execution not required
```

si esa semántica queda formalmente adoptada.

---

## 8.53 DeliveryResult siempre válido

Incluso cuando Delivery falla, el objeto `DeliveryResult` debería ser válido como contrato.

Dicho de otra manera:

```text
failed operation
```

no debe producir:

```text
invalid result object
```

La descripción del fallo debe estar correctamente estructurada.

---

## 8.54 Validación y excepciones

La arquitectura deberá decidir qué validaciones:

- retornan resultados;
- y cuáles generan excepciones internas controladas.

Conceptualmente puede utilizarse:

```text
ValidationResult
```

para validaciones esperadas.

Y:

```text
DeliveryValidationException
```

para condiciones excepcionales internas.

La API pública deberá permanecer predecible.

---

## 8.55 ValidationResult

Podrá definirse conceptualmente:

```text
ValidationResult
├── valid
├── errors
├── warnings
└── metadata
```

Esto permitirá recopilar múltiples errores cuando sea útil.

---

## 8.56 Fail-fast vs collect-all

La arquitectura podrá aplicar dos políticas:

```text
FAIL_FAST
```

o:

```text
COLLECT_ERRORS
```

Para Runtime Delivery, una estrategia razonable será:

- fail-fast para errores críticos que impiden avanzar;
- collect-all en validadores puros cuando mejore diagnóstico.

La política deberá ser consistente.

---

## 8.57 Ejemplo fail-fast

Si falta:

```text
response
```

no tiene sentido continuar validando:

```text
response.contract_version
response.status
```

Puede detenerse inmediatamente.

---

## 8.58 Ejemplo collect-all

En un payload ya construido, podría ser útil reportar simultáneamente:

```text
missing consumer_id
invalid version
invalid timestamp
```

durante pruebas o auditoría.

---

## 8.59 Severidad de validación

Los hallazgos podrán clasificarse como:

```text
ERROR
WARNING
INFO
```

si aporta valor.

Un `ERROR` bloquea la entrega.

Una `WARNING` no necesariamente.

---

## 8.60 Warning no es error

Ejemplo:

```text
payload_size approaching limit
```

podría ser warning.

No deberá marcarse la entrega como fallida si la política permite continuar.

---

## 8.61 Validación estricta en Core

Dentro del Core deberá preferirse validación estricta.

La tolerancia excesiva en esta frontera puede ocultar problemas.

La regla será:

> **Be strict about what HEYTI emits.**

---

## 8.62 Tolerancia del consumidor

El consumidor podrá ser relativamente tolerante al recibir campos opcionales adicionales.

La generación dentro de HEYTI deberá seguir siendo rigurosa.

---

## 8.63 Validación y versionado

Cada validator deberá ser consciente de la versión que valida.

Ejemplo:

```text
DeliveryValidatorV1
```

podrá conocer reglas distintas de una futura:

```text
DeliveryValidatorV2
```

La estrategia concreta deberá evitar duplicación innecesaria.

---

## 8.64 Validator Registry

Si existen varias versiones podrá utilizarse:

```text
ValidatorRegistry
├── delivery/1.0
├── delivery/1.1
└── delivery/2.0
```

solo si la complejidad lo justifica.

---

## 8.65 No validar versión incorrecta

Queda prohibido:

```text
payload version = 2.0
      ↓
validate using 1.0 rules
```

si no existe compatibilidad formal.

---

## 8.66 Validación y serialización

La secuencia recomendada será:

```text
Contract Object
      ↓
Contract Validation
      ↓
Canonicalization
      ↓
Canonical Validation
      ↓
Serialization
      ↓
Payload Validation
```

Esto reduce errores difíciles de localizar.

---

## 8.67 Validación y Adapter Resolution

El adaptador deberá resolverse después de que el payload sea conocido como válido.

Sin embargo, su disponibilidad podrá verificarse antes si ayuda a fallar temprano.

La implementación deberá mantener claridad sobre ambas validaciones.

---

## 8.68 Preflight Validation

Podrá existir conceptualmente una fase:

```text
Delivery Preflight
```

que verifique:

```text
response
context
target
consumer
versions
adapter availability
```

antes de construir el payload.

Esto puede mejorar eficiencia.

---

## 8.69 Preflight exitoso

```text
PRECHECK
├── response valid
├── context valid
├── consumer compatible
├── adapter available
└── policy valid
```

Resultado:

```text
READY TO SERIALIZE
```

---

## 8.70 Preflight fallido

La entrega termina como:

```text
REJECTED
```

sin ejecutar serialización o transporte.

---

## 8.71 Validación de política

La propia `DeliveryPolicy` deberá ser válida.

Ejemplo inválido:

```text
timeout_ms = -500
```

o:

```text
retry_count = -1
```

---

## 8.72 Policy Compatibility

La política también deberá ser compatible con el adaptador.

Ejemplo:

```text
streaming = required
adapter supports streaming = false
```

deberá rechazarse.

---

## 8.73 Validación de timeout

El timeout deberá ser:

```text
positive
within permitted bounds
```

cuando exista.

---

## 8.74 Validación de retry

Si la política permite retry deberá comprobarse:

```text
retry allowed
adapter supports safe retry
operation semantics allow retry
```

No deberá asumirse.

---

## 8.75 Validación de receipt

Cuando un receipt sea obligatorio para considerar `DELIVERED`, deberá comprobarse su presencia.

Si el adaptador no produce receipt y la política lo requiere:

```text
FAILED
```

---

## 8.76 Validación de remote_reference

Si existe una referencia remota, deberá tratarse como metadata técnica.

Su formato podrá validarse solo si el adaptador lo conoce.

---

## 8.77 Validación de seguridad

El pipeline podrá realizar verificaciones como:

```text
consumer authorized
principal authorized
target permitted
```

antes de la entrega.

Estas comprobaciones deberán mantenerse separadas de la validez estructural.

---

## 8.78 Authentication vs Validation

Debe distinguirse:

```text
Is this structure valid?
```

de:

```text
Is this actor authorized?
```

Ambas pueden bloquear Delivery, pero por razones diferentes.

---

## 8.79 Security rejection

Una entrega válida estructuralmente pero no autorizada deberá producir un error de seguridad explícito.

No deberá presentarse como error de serialización.

---

## 8.80 Redacción de errores públicos

Los mensajes públicos deberán ser controlados.

Ejemplo:

```text
"Delivery not authorized."
```

preferible a:

```text
"JWT validation failed because secret key..."
```

---

## 8.81 Validación y privacidad

Podrá existir validación para impedir que campos internos sensibles ingresen al contrato público.

Ejemplos:

```text
password
token
secret
raw database credentials
```

La política deberá bloquearlos.

---

## 8.82 Denylist vs Allowlist

Para contratos críticos deberá preferirse una allowlist estructural basada en schema.

Mejor:

```text
only declared fields
```

que:

```text
allow everything except known secrets
```

---

## 8.83 Unknown fields internos

En modo estricto, un campo desconocido podrá provocar error.

Esto ayuda a detectar divergencias accidentales.

---

## 8.84 Unknown fields externos

La política de consumidores podrá ser más tolerante en cambios compatibles.

La asimetría puede ser útil:

```text
producer strict
consumer tolerant
```

dentro de límites documentados.

---

## 8.85 Validación de metadata

Metadata extensible deberá tener límites.

Por ejemplo:

```text
keys must be strings
values must be canonical
max nesting controlled
```

---

## 8.86 Metadata prohibida

Podrán prohibirse keys reservadas.

Ejemplo:

```text
__internal__
password
token
```

si corresponde.

---

## 8.87 Validación de profundidad

Para evitar estructuras patológicas, la arquitectura podrá establecer:

```text
max nesting depth
```

si resulta necesario.

No es obligatorio inicialmente.

---

## 8.88 Validación de colecciones

También podrán existir límites para:

```text
max items
max tables
max evidence references
```

cuando el rendimiento lo exija.

---

## 8.89 No mezclar validación con truncamiento

Si se supera un límite:

```text
too many items
```

el validator no deberá truncar silenciosamente.

Deberá:

```text
reject
```

o utilizar una política explícita de proyección.

---

## 8.90 Validación y observabilidad

Cada fallo de validación deberá poder registrarse con:

```text
delivery_id
validation_stage
error_code
```

cuando sea seguro.

---

## 8.91 No loggear payload completo por defecto

Para diagnosticar una validación no deberá volcarse automáticamente toda la respuesta.

Deberán preferirse identificadores y paths.

Ejemplo:

```text
path=response.content.metrics[2].value
error=INVALID_TYPE
```

---

## 8.92 Error Path

Los errores estructurados podrán incluir:

```text
field_path
```

Ejemplo:

```text
response.content.metrics[0].value
```

Esto mejora depuración.

---

## 8.93 ValidationError conceptual

Ejemplo:

```text
ValidationError
├── code
├── field_path
├── message
├── expected
├── actual_type
└── severity
```

Los detalles públicos deberán reducirse si son sensibles.

---

## 8.94 Taxonomía inicial de validación

Se propone conceptualmente:

```text
MISSING_REQUIRED_FIELD
INVALID_FIELD_TYPE
INVALID_FIELD_VALUE
INVALID_CONTRACT_VERSION
INCONSISTENT_STATE
UNSUPPORTED_CONTENT_TYPE
CONSUMER_INCOMPATIBLE
INVALID_CONTEXT
INVALID_PAYLOAD
```

Estos códigos podrán ser internos.

Podrán mapearse a códigos Delivery de mayor nivel.

---

## 8.95 Mapping a DeliveryError

Ejemplo:

```text
MISSING_REQUIRED_FIELD
      ↓
DELIVERY_VALIDATION_ERROR
```

con detalle:

```text
field_path = delivery.consumer_id
```

---

## 8.96 Diferencia entre validation code y delivery error code

Podrán existir dos niveles:

```text
DeliveryError.code
=
DELIVERY_VALIDATION_ERROR
```

y:

```text
details.validation_code
=
MISSING_REQUIRED_FIELD
```

Esto evita inflar excesivamente la API pública.

---

## 8.97 Validación durante desarrollo

En entorno de desarrollo podrán habilitarse mensajes más detallados.

En producción deberá preservarse una salida controlada.

---

## 8.98 Validación en pruebas

Las pruebas deberán verificar tanto:

```text
valid structures pass
```

como:

```text
invalid structures fail
```

Los tests negativos son fundamentales.

---

## 8.99 Tests mínimos de MaterializedResponse

Ejemplos:

```text
test_accepts_valid_materialized_response
test_rejects_null_response
test_rejects_missing_response_id
test_rejects_unsupported_response_version
```

---

## 8.100 Tests mínimos de DeliveryRequest

```text
test_accepts_valid_delivery_request
test_rejects_missing_target
test_rejects_missing_consumer
test_rejects_invalid_policy
```

---

## 8.101 Tests mínimos de envelope

```text
test_envelope_ids_are_consistent
test_envelope_requires_contract_version
test_envelope_preserves_response
test_envelope_rejects_invalid_status
```

---

## 8.102 Tests mínimos de payload

```text
test_payload_is_json_serializable
test_payload_matches_schema
test_payload_rejects_unknown_required_type
test_payload_preserves_null
```

---

## 8.103 Tests mínimos de compatibilidad

```text
test_supported_consumer_version_passes
test_unsupported_consumer_version_rejects
test_required_content_type_missing_rejects
```

---

## 8.104 Tests mínimos de DeliveryResult

```text
test_delivered_result_has_no_error
test_failed_result_requires_error
test_rejected_result_does_not_claim_delivery_success
```

---

## 8.105 Boundary tests

Deberán probarse específicamente las fronteras:

```text
Materialization → Delivery
Delivery → Adapter
Adapter → DeliveryResult
Delivery → Consumer
```

---

## 8.106 Mutation testing conceptual

En etapas posteriores podrá resultar útil modificar intencionalmente:

```text
field names
types
versions
```

para comprobar que los validadores detectan la corrupción.

---

## 8.107 No reliance on UI validation

Aunque el Portal valide datos, HEYTI no deberá confiar en esa validación para proteger su frontera.

Debe mantenerse:

```text
UI validation
      +
Core validation
```

con responsabilidades distintas.

---

## 8.108 No reliance on transport validation

Que HTTP acepte JSON no significa que el contrato sea válido.

Ejemplo:

```json
{"foo":"bar"}
```

es JSON válido.

Pero puede ser un Delivery Contract inválido.

---

## 8.109 No reliance on Python typing alone

Type hints ayudan, pero no sustituyen validación runtime cuando la frontera lo requiere.

Ejemplo:

```python
consumer_id: str
```

no impide por sí solo recibir:

```text
None
```

si no existe validación.

---

## 8.110 Model validation

La implementación podrá utilizar dataclasses con validadores, Pydantic u otro mecanismo consistente.

La decisión deberá alinearse con la arquitectura actual de HEYTI.

---

## 8.111 Evitar duplicación de validadores

No deberán existir varias implementaciones independientes de las mismas reglas.

Ejemplo problemático:

```text
validator.py
serializer.py
adapter.py
```

cada uno definiendo diferentes requisitos para `delivery_id`.

La regla deberá residir en un punto contractual claro.

---

## 8.112 Single Source of Truth

Para cada regla deberá existir una autoridad.

Ejemplo:

```text
Delivery Contract
  defines required fields
```

Los componentes deberán consultar o implementar coherentemente esa definición.

---

## 8.113 Validation Pipeline consolidado

```text
┌──────────────────────────────┐
│ MaterializedResponse         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Response Validator           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DeliveryRequest Validator    │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Context / Consumer Validator │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Compatibility Validator      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Envelope Validator           │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Canonical Serializer         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Payload Validator            │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Adapter                      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ AdapterResult Validator      │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DeliveryResult Validator     │
└──────────────────────────────┘
```

---

## 8.114 Flujo de validación exitoso

```text
Response       VALID
Request        VALID
Context        VALID
Compatibility  VALID
Envelope       VALID
Payload        VALID
AdapterResult  VALID
DeliveryResult VALID
```

Resultado:

```text
DELIVERED
```

---

## 8.115 Flujo de rechazo temprano

```text
Response       VALID
Request        VALID
Context        INVALID
```

Resultado:

```text
REJECTED
```

No deberá continuar:

```text
Envelope
Serializer
Adapter
```

---

## 8.116 Flujo de fallo posterior

```text
Response       VALID
Request        VALID
Envelope       VALID
Payload        INVALID
```

Resultado:

```text
FAILED
```

si el error ocurrió durante construcción o serialización de una operación ya aceptada.

La clasificación definitiva deberá permanecer consistente con el pipeline.

---

## 8.117 Regla de clasificación

Como principio general:

```text
Precondition Failure
      ↓
REJECTED
```

```text
Operational Failure after acceptance
      ↓
FAILED
```

Esta regla deberá refinarse durante implementación, pero no contradecirse arbitrariamente.

---

## 8.118 Validación y trazabilidad

Cada validator deberá poder asociar fallos con:

```text
delivery_id
```

desde el momento en que exista.

Antes de ello podrá utilizarse:

```text
response_id
request_id
```

---

## 8.119 Validación y métricas

Podrán medirse:

```text
delivery_validation_failure_total
consumer_incompatibility_total
payload_validation_failure_total
invalid_contract_version_total
```

Estas métricas ayudarán a detectar regresiones.

---

## 8.120 Validación y auditoría

La auditoría deberá poder responder:

```text
Which validation failed?
At which stage?
Why?
Did the adapter execute?
```

---

## 8.121 Validación y honestidad operacional

La arquitectura nunca deberá marcar como `DELIVERED` una estructura que no superó validación.

Tampoco deberá ocultar:

```text
validation warnings
```

cuando sean contractualmente relevantes.

---

## 8.122 Invariantes de validación

Se establecen los siguientes invariantes.

### HRRD-V01 — Validate Every Boundary

Toda frontera contractual crítica deberá contar con validación.

### HRRD-V02 — No Silent Repair

Los validadores no deberán reparar silenciosamente estructuras inválidas.

### HRRD-V03 — No Cognitive Validation

Delivery no validará conclusiones cognitivas.

### HRRD-V04 — Explicit Version Validation

Toda versión contractual deberá validarse.

### HRRD-V05 — Consumer Compatibility Before Delivery

La compatibilidad deberá comprobarse antes de cruzar la frontera.

### HRRD-V06 — Payload Validation Before Adapter

El adaptador deberá recibir payload validado.

### HRRD-V07 — Explicit Failure Attribution

Toda falla deberá poder atribuirse a una etapa.

### HRRD-V08 — Result Consistency

Todo `DeliveryResult` deberá satisfacer sus propias invariantes.

### HRRD-V09 — Strict Producer

HEYTI deberá ser estricto respecto de lo que emite.

### HRRD-V10 — No Presentation Validation

La validez visual queda fuera del Core.

---

## 8.123 Criterios mínimos de aceptación

La implementación del subsistema de validación no deberá considerarse completa hasta demostrar:

1. rechazo de respuestas inválidas;
2. rechazo de consumidores incompatibles;
3. rechazo de versiones no soportadas;
4. detección de campos obligatorios faltantes;
5. detección de inconsistencias de estado;
6. validación de payload antes de entrega;
7. validación de AdapterResult;
8. validación de DeliveryResult;
9. producción de errores estructurados;
10. trazabilidad del punto exacto de fallo.

---

## 8.124 Prueba de cero omisiones

Para cada campo obligatorio deberá existir al menos una prueba negativa que elimine o corrompa dicho campo y confirme que la validación falla.

Conceptualmente:

```text
Valid Envelope
     ↓
Remove required field
     ↓
Validation MUST fail
```

Esta será una de las pruebas centrales de la disciplina:

```text
0 errores
0 omisiones
```

---

## 8.125 Declaración arquitectónica del capítulo

La validación constituye el sistema inmunológico de Runtime Response Delivery.

No crea respuestas.

No corrige conocimiento.

No decide presentación.

Su responsabilidad es proteger cada frontera contractual y evitar que errores estructurales, incompatibilidades o estados incoherentes avancen silenciosamente dentro del sistema.

La regla arquitectónica consolidada queda establecida como:

> **Ninguna respuesta deberá avanzar dentro del Runtime Response Delivery Pipeline únicamente porque pueda ser procesada técnicamente; deberá demostrar, en cada frontera relevante, que cumple el contrato, el contexto, la compatibilidad y las invariantes correspondientes.**

La secuencia fundamental queda establecida como:

```text
Validate
   ↓
Trust
   ↓
Transform
   ↓
Validate Again
   ↓
Deliver
```

Con esta arquitectura de validación queda preparada la siguiente dimensión crítica del sistema:

**identidad, correlación y trazabilidad integral de cada operación de Delivery.**

---

**Fin del Capítulo 8**


# Capítulo 9. Identidad, correlación y trazabilidad integral de Delivery

## 9.1 Propósito del capítulo

Este capítulo define el modelo formal de **identidad, correlación y trazabilidad** de HEYTI Runtime Response Delivery.

La finalidad es garantizar que toda operación de entrega pueda reconstruirse de manera inequívoca desde su origen hasta su resultado final.

Runtime Response Delivery deberá permitir responder, cuando la información exista:

> ¿Qué solicitud originó esta respuesta?

> ¿Qué ejecución produjo el resultado?

> ¿Qué respuesta materializada fue entregada?

> ¿Qué operación concreta de Delivery se ejecutó?

> ¿A qué consumidor fue dirigida?

> ¿Qué adaptador intervino?

> ¿Qué contrato y versión fueron utilizados?

> ¿Cuándo ocurrió?

> ¿Cuál fue el resultado?

> ¿Dónde falló si ocurrió un error?

La trazabilidad deberá formar parte estructural de Delivery.

No deberá depender de reconstrucciones manuales posteriores.

---

## 9.2 Principio fundamental

La regla central será:

> **Toda operación importante deberá tener identidad propia y toda relación importante deberá poder correlacionarse explícitamente.**

Conceptualmente:

```text
User Request
    │
    ▼
request_id
    │
    ▼
Runtime Execution
    │
    ▼
execution_id
    │
    ▼
Materialized Response
    │
    ▼
response_id
    │
    ▼
Delivery Operation
    │
    ▼
delivery_id
    │
    ▼
Consumer
```

Esta cadena constituye la columna vertebral de trazabilidad operacional.

---

## 9.3 Identidad no es correlación

Debe distinguirse:

```text
Identity
```

de:

```text
Correlation
```

**Identity** responde:

> ¿Qué entidad concreta es esta?

**Correlation** responde:

> ¿Con qué otras entidades está relacionada?

Ejemplo:

```text
delivery_id = DEL-9001
```

identifica una entrega.

Mientras:

```text
response_id = RESP-410
```

permite correlacionarla con la respuesta que originó esa entrega.

---

## 9.4 Entidades mínimas identificables

La arquitectura deberá poder distinguir al menos:

```text
Request
Execution
Response
Delivery
Consumer
Adapter
Session
```

cuando cada concepto aplique.

Sus identificadores conceptuales serán:

```text
request_id
execution_id
response_id
delivery_id
consumer_id
adapter_id
session_id
```

---

## 9.5 request_id

`request_id` identifica la solicitud original que entra al flujo de HEYTI.

Conceptualmente:

```text
User
  │
  ▼
Request
  │
  ▼
request_id
```

Delivery no deberá crear o modificar este identificador si ya fue establecido por una capa anterior.

Su responsabilidad será preservarlo.

---

## 9.6 execution_id

`execution_id` identifica una ejecución concreta del Runtime.

Debe distinguirse de `request_id`.

Una misma solicitud podría, en escenarios futuros, producir más de una ejecución.

Ejemplo:

```text
REQ-001
   │
   ├── EXE-001
   └── EXE-002
```

La arquitectura no deberá asumir una relación obligatoria 1:1.

---

## 9.7 response_id

`response_id` identifica la respuesta materializada producida por una ejecución.

Conceptualmente:

```text
execution_id
     ↓
Materialization
     ↓
response_id
```

`response_id` deberá permanecer estable durante las distintas representaciones técnicas de una misma respuesta.

Por ejemplo:

```text
Python object
     ↓
dict
     ↓
JSON
```

deberán conservar:

```text
response_id = RESP-001
```

---

## 9.8 delivery_id

`delivery_id` identifica una operación concreta de entrega.

Debe considerarse una identidad diferente de `response_id`.

Una respuesta podrá originar múltiples entregas:

```text
RESP-001
   │
   ├── DEL-001 → Portal
   ├── DEL-002 → Internal Consumer
   └── DEL-003 → Future Integration
```

Cada operación deberá poder rastrearse independientemente.

---

## 9.9 Regla de unicidad conceptual

Cada identificador deberá ser único dentro de su dominio correspondiente.

Por ejemplo:

```text
delivery_id
```

deberá identificar exactamente una operación de Delivery.

No deberá reutilizarse para otra operación distinta.

---

## 9.10 Formato de identificadores

La arquitectura no deberá depender semánticamente de un formato concreto.

Podrán utilizarse tecnologías como:

```text
UUID
ULID
opaque string
```

u otra estrategia consistente.

La regla será:

```text
identifier format
≠
identifier meaning
```

---

## 9.11 Identificadores opacos

Los identificadores deberán preferentemente ser opacos para consumidores.

El consumidor no deberá inferir información como:

```text
date
consumer
capability
priority
```

a partir del formato del identificador, salvo que una política formal lo establezca.

---

## 9.12 session_id

`session_id` identifica una sesión lógica de interacción con HEYTI.

Conceptualmente:

```text
Session
 ├── Request 1
 │     └── Execution
 │            └── Response
 │                   └── Delivery
 │
 ├── Request 2
 │     └── Execution
 │            └── Response
 │                   └── Delivery
 │
 └── Request 3
```

Delivery deberá preservar la sesión cuando la respuesta pertenezca a una.

---

## 9.13 Sesión no es Delivery

Debe mantenerse:

```text
session_id
   ≠
delivery_id
```

La sesión agrupa interacción.

Delivery identifica una operación puntual.

---

## 9.14 consumer_id

`consumer_id` identifica lógicamente al consumidor.

Ejemplos:

```text
AT_PORTAL
HEYTI_UI
INTERNAL_TEST_CLIENT
```

No deberá utilizarse una identidad basada exclusivamente en:

```text
filename
DOM element
URL route
```

si esos elementos pueden cambiar sin alterar la responsabilidad lógica.

---

## 9.15 adapter_id

`adapter_id` identifica el adaptador responsable del mecanismo técnico de entrega.

Ejemplos conceptuales:

```text
IN_MEMORY
HTTP_JSON
WEBSOCKET_JSON
INTERNAL_CALL
```

Esto permitirá conocer:

> ¿Por qué mecanismo fue entregada la respuesta?

---

## 9.16 correlation_id

La arquitectura podrá utilizar un `correlation_id` para agrupar eventos relacionados.

Ejemplo:

```text
correlation_id = CORR-001
```

podrá acompañar:

```text
REQ-001
EXE-001
RESP-001
DEL-001
```

pero no sustituirá sus identidades propias.

---

## 9.17 Función de correlation_id

`correlation_id` será útil para:

- logs;
- tracing;
- debugging;
- observabilidad;
- búsquedas operacionales.

Ejemplo:

```text
grep CORR-001
```

podría reconstruir el flujo completo.

---

## 9.18 Correlación explícita

La relación entre entidades deberá quedar explícita mediante campos.

Ejemplo:

```text
DeliveryTrace
├── request_id
├── execution_id
├── response_id
├── delivery_id
└── correlation_id
```

No deberá depender únicamente de timestamps.

---

## 9.19 Prohibición de correlación por proximidad

No deberá utilizarse una lógica como:

```text
"this delivery happened 100 ms after that response,
therefore they probably belong together"
```

La correlación deberá estar basada en identidad explícita.

---

## 9.20 Modelo de trazabilidad

Se propone conceptualmente:

```text
DeliveryTrace
```

como estructura responsable de representar la cadena operacional.

Podrá contener:

```text
request_id
session_id
execution_id
response_id
delivery_id
correlation_id
capability_id
consumer_id
adapter_id
contract_versions
timestamps
status
```

---

## 9.21 Trazabilidad mínima

Para v1.0 deberá definirse un conjunto mínimo.

Conceptualmente:

```text
response_id
delivery_id
consumer_id
adapter_id
delivery_contract_version
status
```

y, cuando estén disponibles:

```text
request_id
execution_id
session_id
```

---

## 9.22 Trazabilidad enriquecida

En versiones posteriores podrán añadirse:

```text
principal_id
node_id
deployment_id
retry_parent_id
transport_reference
audit_reference
```

únicamente cuando exista necesidad real.

---

## 9.23 capability_id en trazabilidad

`capability_id` podrá conservarse para identificar la capability responsable de la respuesta.

Ejemplo:

```text
capability_id = describe_section
```

Esto permitirá reconstruir:

```text
Request
  ↓
Capability
  ↓
Response
  ↓
Delivery
```

---

## 9.24 capability_id no controla Delivery

La presencia de:

```text
capability_id
```

es descriptiva.

Delivery no deberá realizar:

```text
if capability_id == "describe_section":
    special delivery logic
```

salvo contrato formal justificado.

---

## 9.25 Versiones en la trazabilidad

Deberán preservarse las versiones relevantes.

Conceptualmente:

```text
response_contract_version
delivery_contract_version
capability_version
knowledge_version
```

cuando estén disponibles y sean necesarias para auditoría.

---

## 9.26 knowledge_version

Si Materialization ya proporciona:

```text
knowledge_version
```

Delivery deberá preservarla.

No deberá consultar HKS para calcularla nuevamente.

---

## 9.27 data_as_of

La trazabilidad cognitiva podrá incluir:

```text
data_as_of
```

Este campo indica vigencia del dato.

No deberá confundirse con:

```text
delivered_at
```

---

## 9.28 Timestamps de trazabilidad

Deberán distinguirse eventos temporales.

Conceptualmente:

```text
request_received_at
execution_started_at
response_materialized_at
delivery_requested_at
delivery_started_at
delivery_completed_at
```

No todos deberán estar presentes en Delivery.

Pero cuando se conserven, su significado deberá ser inequívoco.

---

## 9.29 Timestamp de Delivery

Como mínimo, Delivery debería poder conservar:

```text
started_at
completed_at
```

o un timestamp de finalización si la implementación inicial es más simple.

---

## 9.30 Orden temporal

La secuencia normal será:

```text
request
  ↓
execution
  ↓
materialization
  ↓
delivery
```

Por tanto:

```text
request_received_at
<= execution_started_at
<= response_materialized_at
<= delivery_completed_at
```

dentro de las limitaciones de relojes y sistemas distribuidos.

---

## 9.31 Monotonicidad local

Para medir duración interna deberá preferirse un reloj monotónico cuando el lenguaje o infraestructura lo permita.

Conceptualmente:

```text
duration_ms
```

no debería depender de ajustes del reloj del sistema durante una operación.

---

## 9.32 Tiempo de pared

Para auditoría deberán utilizarse timestamps de calendario.

Por ejemplo:

```text
2026-08-20T16:25:30-06:00
```

Cada tipo de reloj tiene propósito diferente.

---

## 9.33 DeliveryTrace inmutable

La estructura de trazabilidad deberá favorecer inmutabilidad.

Especialmente:

```text
request_id
execution_id
response_id
delivery_id
consumer_id
```

no deberán modificarse después de establecida la operación.

---

## 9.34 Trace Builder

La implementación podrá utilizar conceptualmente un:

```text
DeliveryTraceBuilder
```

para construir la traza de forma controlada.

Sin embargo, deberá evitarse complejidad si una dataclass inmutable es suficiente.

---

## 9.35 Snapshot de contexto

Al iniciar Delivery podrá capturarse un snapshot de:

```text
consumer_id
adapter_id
contract_version
session_id
```

Esto permitirá reconstruir exactamente bajo qué contexto comenzó la operación.

---

## 9.36 Cambio de configuración durante Delivery

Si la configuración global cambia mientras una operación está ejecutándose, la traza deberá conservar el snapshot usado por esa operación.

Ejemplo:

```text
AdapterRegistry switches from HTTP_V1 to HTTP_V2
```

Una entrega iniciada con:

```text
HTTP_V1
```

deberá conservar esa identidad.

---

## 9.37 Identidad y reintentos

Los reintentos requieren una política clara.

Se propone conceptualmente:

```text
DEL-001
   ↓ failed
DEL-002
   parent_delivery_id = DEL-001
```

Esto preserva:

- identidad independiente;
- relación explícita;
- auditabilidad.

---

## 9.38 parent_delivery_id

En una futura política de retry podrá existir:

```text
parent_delivery_id
```

o:

```text
retry_of
```

No será obligatorio en v1.0 si no existen reintentos.

---

## 9.39 attempt_number

También podría utilizarse:

```text
attempt_number
```

si se adopta un modelo formal.

Ejemplo:

```text
attempt 1
attempt 2
attempt 3
```

Deberá evitarse mezclar esta información con `delivery_id`.

---

## 9.40 Identidad y fan-out

Si una respuesta se entrega a múltiples consumidores:

```text
RESP-001
├── DEL-001 → AT_PORTAL
├── DEL-002 → HEYTI_UI
└── DEL-003 → SERVICE_X
```

cada operación deberá poseer su propia identidad.

---

## 9.41 batch_id

En escenarios futuros de fan-out podría existir:

```text
delivery_batch_id
```

para agrupar las entregas.

No deberá incorporarse a v1.0 si no existe fan-out.

---

## 9.42 Identidad y streaming

Una entrega streaming podría requerir:

```text
delivery_id
stream_id
chunk_id
sequence_number
```

No forma parte obligatoria de v1.0.

La existencia de `delivery_id` facilita evolución futura.

---

## 9.43 Traceability Context

Podrá existir conceptualmente:

```text
TraceContext
```

para transmitir identificadores entre capas.

Ejemplo:

```text
TraceContext
├── correlation_id
├── request_id
├── session_id
└── execution_id
```

Materialization podrá extenderlo con:

```text
response_id
```

Delivery con:

```text
delivery_id
```

---

## 9.44 Propagación de contexto

Cada capa deberá preservar los identificadores anteriores y agregar únicamente aquellos de los que es responsable.

Conceptualmente:

```text
Gateway
  adds request_id
       ↓
Runtime
  adds execution_id
       ↓
Materialization
  adds response_id
       ↓
Delivery
  adds delivery_id
```

Este patrón establece responsabilidad clara.

---

## 9.45 Prohibición de regeneración

Delivery no deberá regenerar:

```text
request_id
execution_id
response_id
```

si ya existen.

Regenerarlos rompería trazabilidad.

---

## 9.46 Ausencia de identificador anterior

Si un identificador anterior es opcional y no está disponible, Delivery deberá preservar esa ausencia.

No deberá inventarlo.

Ejemplo:

```text
session_id = null
```

puede ser legítimo en una operación no interactiva.

---

## 9.47 Identificador obligatorio ausente

Si el contrato requiere un identificador y está ausente:

```text
Validation Failure
```

deberá detener el pipeline.

---

## 9.48 Trace Completeness

La arquitectura podrá definir un nivel de completitud.

Ejemplo conceptual:

```text
FULL
PARTIAL
MINIMAL
```

si resulta útil.

Sin embargo, no deberá introducirse si basta con validación explícita de campos.

---

## 9.49 Honest Traceability

Una traza incompleta no deberá presentarse como completa.

Si falta:

```text
execution_id
```

deberá quedar explícita la ausencia.

---

## 9.50 Trazabilidad y DeliveryResult

El `DeliveryResult` deberá incluir o referenciar suficiente trazabilidad.

Ejemplo:

```text
DeliveryResult
├── delivery_id
├── response_id
├── status
└── trace
```

---

## 9.51 Trace en DeliveryEnvelope

El envelope entregado al consumidor podrá incluir una versión pública de la traza.

No toda la trazabilidad interna deberá exponerse.

---

## 9.52 Public Trace vs Internal Trace

La arquitectura deberá distinguir, si es necesario:

```text
PublicTrace
```

y:

```text
InternalTrace
```

Ejemplo:

Public:

```text
response_id
delivery_id
contract_version
```

Internal:

```text
process_id
node_id
stack correlation
```

---

## 9.53 Seguridad de trazabilidad

Los identificadores no deberán exponer información sensible.

Ejemplo problemático:

```text
delivery_id = username-section-precise-address
```

Preferible:

```text
opaque identifier
```

---

## 9.54 PII y trazabilidad

No deberán utilizarse como identificadores:

```text
email
phone
full name
precise address
```

salvo necesidad formal y autorizada.

La trazabilidad técnica deberá preferir IDs opacos.

---

## 9.55 Trazabilidad y logs

Los logs deberán incluir suficientes IDs para reconstruir el flujo.

Ejemplo:

```text
request_id=REQ-001
execution_id=EXE-001
response_id=RESP-001
delivery_id=DEL-001
status=DELIVERED
```

---

## 9.56 Structured Logging

Se deberá favorecer logging estructurado.

Ejemplo conceptual:

```json
{
  "event": "delivery.completed",
  "delivery_id": "DEL-001",
  "response_id": "RESP-001",
  "consumer_id": "AT_PORTAL",
  "status": "DELIVERED"
}
```

sobre mensajes exclusivamente libres.

---

## 9.57 Logs humanos

También podrán existir mensajes legibles.

Pero la trazabilidad automática deberá depender preferentemente de campos estructurados.

---

## 9.58 Trace Event

Conceptualmente cada evento podrá tener:

```text
event_name
timestamp
delivery_id
response_id
stage
status
metadata
```

---

## 9.59 Eventos mínimos de Delivery

Podrían existir:

```text
delivery.requested
delivery.validation.started
delivery.validation.failed
delivery.serialization.started
delivery.serialization.failed
delivery.adapter.started
delivery.adapter.failed
delivery.completed
```

La instrumentación concreta deberá evitar exceso innecesario.

---

## 9.60 Trace Span

Si en el futuro se adopta tracing distribuido, una operación de Delivery podrá corresponder a un span.

Conceptualmente:

```text
Request Span
 └── Runtime Span
      └── Materialization Span
           └── Delivery Span
```

Esto facilitaría integración con herramientas estándar de observabilidad.

---

## 9.61 OpenTelemetry compatibility

La arquitectura deberá evitar decisiones que impidan futura integración con estándares de tracing como OpenTelemetry.

No es obligatorio implementarlo en v1.0.

La existencia de:

```text
correlation_id
delivery_id
timestamps
stages
```

facilita esa evolución.

---

## 9.62 Trace ID externo

En una futura integración podría existir un:

```text
trace_id
```

proporcionado por infraestructura.

No deberá confundirse necesariamente con:

```text
correlation_id
```

La política deberá definir su relación.

---

## 9.63 Auditoría

La trazabilidad operacional y la auditoría están relacionadas pero no son idénticas.

```text
Traceability
```

permite reconstruir el flujo.

```text
Audit
```

permite demostrar y revisar hechos relevantes bajo una política de conservación.

---

## 9.64 Audit Record

En el futuro podrá existir un registro como:

```text
DeliveryAuditRecord
```

con:

```text
delivery_id
response_id
consumer_id
adapter_id
contract_version
status
timestamps
error_code
payload_reference
```

según política.

---

## 9.65 No confundir auditoría con logging

Los logs pueden:

- rotar;
- cambiar nivel;
- contener información técnica.

La auditoría puede necesitar:

- retención;
- inmutabilidad;
- evidencia de operación.

La arquitectura deberá mantener la posibilidad de separar ambos dominios.

---

## 9.66 Payload completo en auditoría

No deberá asumirse que auditoría exige almacenar el payload completo.

Podrán utilizarse:

```text
response_id
payload_hash
storage_reference
```

en el futuro.

Esto reduce riesgos de privacidad.

---

## 9.67 payload_hash

Un hash podría ayudar a verificar:

> ¿El payload auditado corresponde a la misma representación?

Pero únicamente deberá implementarse cuando exista canonicalización formal.

No forma parte obligatoria de v1.0.

---

## 9.68 Trazabilidad de errores

Todo error deberá poder correlacionarse con la entrega.

Ejemplo:

```text
DeliveryError
├── delivery_id
├── response_id
├── error_code
└── stage
```

---

## 9.69 error_stage

Podrá utilizarse conceptualmente:

```text
VALIDATION
SERIALIZATION
ADAPTER_RESOLUTION
TRANSPORT
RESULT_MAPPING
```

Esto permite diagnosticar rápidamente.

---

## 9.70 Error correlation

Una excepción interna deberá mapearse a un evento trazable.

Ejemplo:

```text
TimeoutError
      ↓
DeliveryError
      ↓
delivery_id=DEL-001
stage=TRANSPORT
code=DELIVERY_TIMEOUT
```

---

## 9.71 Trazabilidad de REJECTED

Una operación `REJECTED` deberá conservar traza aunque nunca haya cruzado la frontera externa.

Ejemplo:

```text
DEL-001
status = REJECTED
stage = COMPATIBILITY
```

---

## 9.72 Trazabilidad de FAILED

Una operación `FAILED` deberá indicar hasta qué punto llegó.

Ejemplo:

```text
stage = SERIALIZATION
```

o:

```text
stage = TRANSPORT
```

---

## 9.73 Trazabilidad de DELIVERED

Una operación exitosa deberá poder confirmar:

```text
adapter executed
delivery result produced
completed_at recorded
```

---

## 9.74 Receipt y trazabilidad

Si existe receipt:

```text
remote_reference
received_at
```

podrá incorporarse a la traza técnica.

---

## 9.75 Consumer acknowledgement

La traza podrá distinguir:

```text
sent
accepted
acknowledged
```

si el transporte lo soporta.

No deberá inventarse confirmación inexistente.

---

## 9.76 No false acknowledgement

Un adaptador que solo sabe que envió bytes no deberá declarar:

```text
consumer_received = true
```

si no existe evidencia.

La honestidad operacional deberá preservarse.

---

## 9.77 DeliveryStatus y evidencia

Cada estado deberá estar respaldado por evidencia técnica suficiente.

Ejemplo:

```text
DELIVERED
```

debe corresponder al criterio definido por el adaptador.

No a una suposición.

---

## 9.78 Trazabilidad y sesiones concurrentes

La existencia de `session_id`, `request_id` y `delivery_id` permitirá separar operaciones concurrentes.

Ejemplo:

```text
Session A
  REQ-01 → DEL-01

Session B
  REQ-02 → DEL-02
```

Los logs no deberán depender de un global:

```text
current_session
```

---

## 9.79 Trazabilidad y concurrencia

Cada contexto de Delivery deberá ser independiente.

No deberá existir riesgo de que:

```text
DEL-001
```

herede accidentalmente:

```text
session_id
```

de otra operación concurrente.

---

## 9.80 Context variables

La implementación podrá utilizar mecanismos seguros de contexto si son apropiados.

Pero la arquitectura deberá preservar siempre una representación explícita del contexto.

---

## 9.81 Trazabilidad y pruebas

Las pruebas deberán verificar:

```text
IDs generated correctly
IDs preserved
relations preserved
errors correlated
timestamps consistent
consumer recorded
adapter recorded
```

---

## 9.82 Test de preservación de request_id

Ejemplo:

```text
request_id = REQ-001
      ↓
Materialization
      ↓
Delivery
      ↓
DeliveryResult.trace.request_id
```

deberá continuar siendo:

```text
REQ-001
```

---

## 9.83 Test de preservación de response_id

```text
RESP-001
```

deberá permanecer igual antes y después de serialización.

---

## 9.84 Test de delivery_id único

Dos operaciones:

```text
deliver(response)
deliver(response)
```

deberán generar, si son operaciones distintas:

```text
DEL-001
DEL-002
```

---

## 9.85 Test de correlación

Deberá comprobarse:

```text
DeliveryResult.response_id
==
MaterializedResponse.response_id
```

---

## 9.86 Test de error trace

Un fallo de serialización deberá producir:

```text
delivery_id
error code
error stage
```

correctamente correlacionados.

---

## 9.87 Test de consumer trace

Una entrega dirigida a:

```text
AT_PORTAL
```

deberá registrar exactamente:

```text
consumer_id = AT_PORTAL
```

---

## 9.88 Test de adapter trace

Con:

```text
InMemoryDeliveryAdapter
```

la traza deberá reflejar:

```text
adapter_id = IN_MEMORY
```

---

## 9.89 Test de sesión ausente válida

Si `session_id` es opcional:

```text
session_id = null
```

no deberá ser inventado.

---

## 9.90 Test de sesión obligatoria

Si una política exige sesión y falta:

```text
REJECTED
```

con error de contexto.

---

## 9.91 Trazabilidad y Consumer Substitution Test

Si cambia:

```text
AT_PORTAL
```

por:

```text
HEYTI_UI
```

la estructura de trazabilidad deberá continuar funcionando.

Solo cambiará:

```text
consumer_id
```

y posiblemente:

```text
adapter_id
```

---

## 9.92 Trazabilidad y Transport Substitution Test

Si cambia:

```text
IN_MEMORY
```

por:

```text
HTTP_JSON
```

deberá mantenerse:

```text
request_id
execution_id
response_id
delivery_id
```

La trazabilidad principal no deberá romperse.

---

## 9.93 Trazabilidad y versión de contrato

Una operación deberá poder reconstruirse sabiendo exactamente:

```text
delivery_contract_version
```

utilizada.

Esto será esencial cuando existan múltiples versiones coexistiendo.

---

## 9.94 Trazabilidad y versionado de consumidor

Si existe:

```text
consumer_profile_version
```

podrá preservarse para explicar compatibilidad.

Ejemplo:

```text
AT_PORTAL profile 1.0
```

---

## 9.95 Trazabilidad y deployment

En operaciones futuras de producción podrá resultar útil:

```text
environment
deployment_version
```

para saber qué versión de HEYTI produjo la entrega.

No deberá sobrecargarse v1.0 si todavía no es necesario.

---

## 9.96 Trazabilidad y Git commit

En ambientes de desarrollo o auditoría podrá registrarse:

```text
build_version
git_commit
```

como metadata de deployment.

Esto no pertenece a la semántica cognitiva.

---

## 9.97 Trazabilidad y Knowledge Version

Cuando una respuesta utilice una versión particular del conocimiento:

```text
knowledge_version
```

deberá preservarse si Materialization la incluye.

Esto permitirá responder:

> ¿Con qué estado del conocimiento fue producida esta respuesta?

---

## 9.98 Trazabilidad y datos

De forma similar:

```text
dataset_version
data_as_of
```

podrán formar parte de la procedencia cognitiva.

Delivery deberá conservarlos.

---

## 9.99 No duplicar procedencia innecesariamente

Si la respuesta ya contiene procedencia, la traza no deberá duplicarla arbitrariamente.

Podrá referenciarla.

---

## 9.100 Trace Schema

La traza deberá poseer un schema explícito si forma parte del contrato público.

Conceptualmente:

```text
TraceContract v1.0
```

podrá formar parte del Delivery Contract.

---

## 9.101 Trace Version

No será necesario crear una versión independiente de Trace si evoluciona dentro de Delivery Contract.

Deberá evitarse proliferación de versiones sin necesidad.

---

## 9.102 Modelo consolidado de trazabilidad

```text
┌───────────────────────┐
│ Session               │
│ session_id            │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Request               │
│ request_id            │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Execution             │
│ execution_id          │
│ capability_id         │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Response              │
│ response_id           │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ Delivery              │
│ delivery_id           │
│ consumer_id           │
│ adapter_id            │
└───────────┬───────────┘
            │
            ▼
┌───────────────────────┐
│ DeliveryResult        │
│ status                │
│ completed_at          │
└───────────────────────┘
```

---

## 9.103 Correlation tree

En escenarios complejos:

```text
CORR-001
│
├── REQ-001
│   └── EXE-001
│       └── RESP-001
│           ├── DEL-001
│           └── DEL-002
│
└── REQ-002
    └── EXE-002
        └── RESP-002
            └── DEL-003
```

La arquitectura deberá soportar relaciones 1:N sin perder claridad.

---

## 9.104 Invariantes de identidad y trazabilidad

Se establecen los siguientes invariantes.

### HRRD-T01 — Stable Response Identity

`response_id` deberá conservarse durante toda la entrega.

### HRRD-T02 — Unique Delivery Identity

Cada operación de Delivery deberá poseer identidad propia.

### HRRD-T03 — Explicit Correlation

Las relaciones deberán registrarse mediante identificadores explícitos.

### HRRD-T04 — No ID Regeneration

Delivery no regenerará identidades pertenecientes a capas anteriores.

### HRRD-T05 — Consumer Traceability

Toda entrega deberá poder identificar su consumidor.

### HRRD-T06 — Adapter Traceability

Toda entrega deberá poder identificar su adaptador.

### HRRD-T07 — Version Traceability

La versión contractual utilizada deberá permanecer disponible.

### HRRD-T08 — Error Traceability

Todo fallo deberá poder correlacionarse con una entrega.

### HRRD-T09 — Terminal Trace

La traza deberá completarse incluso en `FAILED` o `REJECTED`.

### HRRD-T10 — No Sensitive Identity Leakage

Los identificadores deberán evitar información sensible innecesaria.

---

## 9.105 Prueba de trazabilidad mínima

Para una operación terminada deberá poder responderse:

```text
Which response?
Which delivery?
Which consumer?
Which adapter?
Which status?
Which contract version?
When?
```

---

## 9.106 Prueba de trazabilidad completa

Cuando el contexto lo permita deberá poder responderse también:

```text
Which session?
Which request?
Which execution?
Which capability?
Which knowledge version?
Which data version?
```

---

## 9.107 Prueba de fallo

Ante un error deberá poder responderse:

```text
Which delivery failed?
At which stage?
With which error code?
Was the response itself valid?
Did the adapter execute?
```

---

## 9.108 Prueba de múltiples entregas

Dada una misma respuesta:

```text
RESP-001
```

deberá poder distinguirse:

```text
DEL-001
DEL-002
DEL-003
```

sin perder la relación común.

---

## 9.109 Prueba de aislamiento concurrente

Dos entregas simultáneas no deberán intercambiar:

```text
session_id
delivery_id
consumer_id
adapter_id
```

---

## 9.110 Criterios mínimos de implementación

Para v1.0, la implementación deberá permitir como mínimo:

```text
generate delivery_id
preserve response_id
preserve request/execution identifiers when present
record consumer_id
record adapter_id
record delivery_contract_version
record timestamps
record terminal status
correlate errors
```

---

## 9.111 DeliveryTrace v1.0 mínimo

Conceptualmente podría adoptar una forma como:

```text
DeliveryTrace
├── delivery_id
├── response_id
├── request_id?
├── execution_id?
├── session_id?
├── correlation_id?
├── capability_id?
├── consumer_id
├── adapter_id
├── delivery_contract_version
├── started_at
├── completed_at
└── status
```

El símbolo `?` indica campos potencialmente opcionales según contrato.

---

## 9.112 Serialización de Trace

DeliveryTrace deberá poder convertirse a representación canónica.

Ejemplo:

```json
{
  "delivery_id": "DEL-001",
  "response_id": "RESP-001",
  "request_id": "REQ-001",
  "execution_id": "EXE-001",
  "consumer_id": "AT_PORTAL",
  "adapter_id": "IN_MEMORY",
  "status": "DELIVERED"
}
```

---

## 9.113 Trazabilidad y Presentation

Presentation podrá utilizar algunos identificadores para:

- debug;
- soporte;
- vistas de auditoría.

Pero no deberá depender de ellos para decisiones visuales ordinarias.

---

## 9.114 Identificador visible al usuario

La futura UI podrá mostrar:

```text
response_id
```

o:

```text
delivery_id
```

en un modo avanzado de auditoría.

No es obligatorio en la interfaz principal.

---

## 9.115 Trazabilidad y soporte operativo

Una ventaja importante será poder recibir un reporte como:

> "La respuesta no apareció correctamente."

y solicitar:

```text
response_id
```

o:

```text
delivery_id
```

para reconstruir exactamente lo ocurrido.

---

## 9.116 Trazabilidad y confianza institucional

La trazabilidad fortalece HEYTI porque permite distinguir:

```text
what HEYTI concluded
what HEYTI materialized
what HEYTI delivered
what the UI displayed
```

Estas etapas no deberán confundirse.

---

## 9.117 Cadena completa de responsabilidad

```text
Knowledge / Evidence
       ↓
Capability
       ↓
Execution
       ↓
Materialization
       ↓
Response
       ↓
Delivery
       ↓
Consumer
       ↓
Presentation
```

Cada etapa deberá poder identificarse y auditarse cuando corresponda.

---

## 9.118 Criterio de éxito

La trazabilidad será considerada adecuada cuando un `DeliveryResult` pueda relacionarse de forma inequívoca con la respuesta que originó la operación y, cuando la información esté disponible, con el request, sesión y ejecución correspondientes.

---

## 9.119 Declaración arquitectónica del capítulo

Runtime Response Delivery no deberá producir operaciones anónimas.

Toda entrega deberá existir como un hecho identificable dentro de la historia operacional de HEYTI.

La identidad de la respuesta y la identidad de la entrega deberán permanecer separadas.

La correlación deberá ser explícita.

Los errores deberán poder localizarse.

Y la reconstrucción de un flujo no deberá depender de conjeturas basadas en timestamps o mensajes de log.

La regla arquitectónica consolidada queda establecida como:

> **HEYTI deberá poder reconstruir la historia completa de una respuesta desde la solicitud que la originó hasta la operación mediante la cual fue entregada, preservando identidades estables, relaciones explícitas y evidencia operacional suficiente para diagnóstico y auditoría.**

La cadena mínima queda formalizada como:

```text
request_id
    ↓
execution_id
    ↓
response_id
    ↓
delivery_id
    ↓
DeliveryResult
```

Con esta base queda preparado el siguiente componente fundamental de Runtime Response Delivery:

**el modelo formal de errores, fallos, rechazo y recuperación controlada.**

---

**Fin del Capítulo 9**


# Capítulo 10. Modelo formal de errores, rechazo, fallo y recuperación controlada

## 10.1 Propósito del capítulo

Este capítulo define el modelo formal de errores de **HEYTI Runtime Response Delivery (HRRD)**.

La finalidad es garantizar que toda condición anómala ocurrida dentro del proceso de entrega pueda ser:

- detectada;
- clasificada;
- representada;
- trazada;
- diagnosticada;
- y tratada de manera controlada.

El objetivo no es únicamente "manejar excepciones".

El objetivo es establecer una semántica operacional clara que permita distinguir entre:

```text
respuesta inválida
operación rechazada
fallo de serialización
fallo de adaptador
fallo de transporte
timeout
incompatibilidad
fallo interno
```

sin convertir todos estos escenarios en un único:

```text
ERROR
```

ambiguo.

La regla central será:

> **Todo fallo de Delivery deberá tener identidad semántica, origen atribuible y resultado explícito.**

---

## 10.2 Error no es excepción

Debe distinguirse:

```text
DeliveryError
```

de:

```text
Exception
```

Una excepción es un mecanismo técnico del lenguaje.

Un `DeliveryError` es una representación contractual y operacional del problema.

Conceptualmente:

```text
Internal Exception
       ↓
Error Mapping
       ↓
DeliveryError
       ↓
DeliveryResult
```

La arquitectura no deberá exponer excepciones internas directamente como contrato público.

---

## 10.3 Error no es fallo cognitivo

Debe preservarse estrictamente:

```text
Delivery Error
      ≠
Cognitive Error
```

Ejemplo:

```text
Capability Result = VALID
Materialization   = VALID
Delivery          = FAILED
```

La existencia de un fallo de transporte no deberá modificar retrospectivamente el resultado cognitivo.

---

## 10.4 Error no es rechazo

La arquitectura deberá distinguir:

```text
REJECTED
```

de:

```text
FAILED
```

Aunque ambos representan que la entrega no concluyó exitosamente, su significado es distinto.

---

## 10.5 Definición de REJECTED

Una operación deberá considerarse `REJECTED` cuando no cumple una precondición necesaria para iniciar o continuar la entrega.

Ejemplos:

```text
invalid response contract
missing required context
unsupported consumer
unsupported contract version
consumer incompatibility
unauthorized target
adapter unavailable before execution
```

Conceptualmente:

```text
Precondition not satisfied
        ↓
REJECTED
```

---

## 10.6 Definición de FAILED

Una operación deberá considerarse `FAILED` cuando:

- fue aceptada como válida para Delivery;
- comenzó procesamiento operacional;
- y posteriormente ocurrió un error que impidió completar la entrega.

Ejemplos:

```text
serialization failure
payload generation failure
timeout
network failure
adapter exception
target unavailable during execution
internal delivery failure
```

Conceptualmente:

```text
Valid operation
      ↓
Operational processing
      ↓
Failure
      ↓
FAILED
```

---

## 10.7 Definición de DELIVERED

Una operación deberá considerarse `DELIVERED` cuando se cumplan las condiciones de éxito definidas por el contrato y el adaptador.

Como mínimo:

```text
response valid
payload valid
adapter execution valid
delivery acceptance criteria satisfied
```

No deberá interpretarse automáticamente como:

```text
UI rendered successfully
```

---

## 10.8 Tabla de estados terminales

| Estado | Significado |
|---|---|
| `DELIVERED` | La operación cumplió los criterios de entrega |
| `REJECTED` | La operación no cumplió precondiciones para entrega |
| `FAILED` | La operación válida experimentó un fallo durante procesamiento o entrega |

Estos estados serán la base mínima de v1.0.

---

## 10.9 Estado PARTIAL

La arquitectura podrá evaluar en el futuro:

```text
PARTIAL
```

pero únicamente cuando exista una semántica precisa.

Ejemplos potenciales:

```text
multiple targets
streaming
chunked delivery
partial acknowledgement
```

Mientras no exista una necesidad real:

> **v1.0 deberá preferir estados terminales inequívocos.**

---

## 10.10 DeliveryError

Se define conceptualmente:

```text
DeliveryError
```

como la representación estructurada de un problema ocurrido en Delivery.

Podrá contener:

```text
code
category
message
stage
recoverable
details
timestamp
delivery_id
response_id
```

La estructura definitiva deberá mantenerse mínima y suficiente.

---

## 10.11 error.code

`error.code` deberá ser:

```text
stable
machine-readable
documented
```

Ejemplos:

```text
DELIVERY_VALIDATION_ERROR
DELIVERY_CONTRACT_MISMATCH
DELIVERY_UNSUPPORTED_CONSUMER
DELIVERY_SERIALIZATION_ERROR
DELIVERY_ADAPTER_NOT_AVAILABLE
DELIVERY_TARGET_UNAVAILABLE
DELIVERY_TIMEOUT
DELIVERY_ADAPTER_ERROR
DELIVERY_INTERNAL_ERROR
```

---

## 10.12 Código estable vs mensaje variable

Los consumidores deberán depender de:

```text
error.code
```

y no de:

```text
error.message
```

porque el mensaje podrá evolucionar.

Ejemplo:

```text
code = DELIVERY_TIMEOUT
```

puede permanecer estable aunque cambie:

```text
"Delivery timed out."
```

por:

```text
"Target did not respond before timeout."
```

---

## 10.13 error.category

La categoría deberá agrupar errores relacionados.

Propuesta conceptual:

```text
VALIDATION
COMPATIBILITY
SERIALIZATION
ADAPTER
TRANSPORT
TIMEOUT
SECURITY
INTERNAL
```

Esto facilitará:

- métricas;
- logging;
- alertas;
- auditoría.

---

## 10.14 error.stage

El campo `stage` deberá indicar dónde ocurrió el problema.

Ejemplos:

```text
ENTRY_VALIDATION
CONTEXT_VALIDATION
COMPATIBILITY
ENVELOPE_BUILD
SERIALIZATION
PAYLOAD_VALIDATION
ADAPTER_RESOLUTION
DELIVERY_EXECUTION
RESULT_MAPPING
TRACE_COMPLETION
```

No todos los valores deberán formar parte necesariamente del contrato público.

---

## 10.15 Importancia de error.stage

Supóngase:

```text
DELIVERY_SERIALIZATION_ERROR
```

Sin `stage`, podría existir duda sobre:

- canonicalización;
- JSON encoding;
- payload validation.

Con:

```text
stage = SERIALIZATION
```

la localización mejora.

---

## 10.16 error.message

El mensaje deberá ser:

- claro;
- seguro;
- útil;
- no engañoso.

Ejemplo:

```text
"Unsupported delivery contract version."
```

No deberá exponer detalles internos innecesarios.

---

## 10.17 Mensajes públicos e internos

La arquitectura podrá distinguir:

```text
public_message
```

de:

```text
internal_message
```

si existe necesidad.

Ejemplo:

Public:

```text
"Delivery could not be completed."
```

Internal:

```text
"HTTP adapter connection refused at upstream target."
```

La implementación deberá evitar duplicación innecesaria.

---

## 10.18 details

`details` podrá contener información estructurada adicional.

Ejemplo:

```json
{
  "expected_version": "1.0",
  "received_version": "2.0"
}
```

No deberá convertirse en un contenedor arbitrario de internals sensibles.

---

## 10.19 recoverable

`recoverable` podrá indicar si una operación podría ser intentada nuevamente bajo condiciones distintas.

Ejemplo:

```text
DELIVERY_TIMEOUT
recoverable = true
```

pero:

```text
DELIVERY_CONTRACT_MISMATCH
recoverable = false
```

según política.

Este campo no deberá activar automáticamente reintentos.

---

## 10.20 Retryable vs recoverable

Debe distinguirse:

```text
recoverable
```

de:

```text
retryable
```

Una situación puede ser recuperable mediante corrección manual, pero no segura para retry automático.

Ejemplo:

```text
invalid consumer configuration
```

podría ser recuperable tras configuración, pero no inmediatamente reintentable.

---

## 10.21 Taxonomía inicial de errores

Se propone la siguiente taxonomía base:

```text
DeliveryError
├── ValidationError
├── CompatibilityError
├── SerializationError
├── AdapterResolutionError
├── TransportError
├── TimeoutError
├── SecurityError
└── InternalDeliveryError
```

La implementación no necesariamente requerirá una clase distinta para cada uno.

La taxonomía representa categorías semánticas.

---

## 10.22 ValidationError

Corresponde a estructuras inválidas.

Ejemplos:

```text
missing required field
invalid field type
invalid status combination
invalid timestamp
```

Resultado habitual:

```text
REJECTED
```

si ocurre durante preflight.

---

## 10.23 CompatibilityError

Corresponde a incompatibilidad entre:

```text
response contract
delivery contract
consumer profile
serializer
adapter
```

Ejemplo:

```text
consumer does not support delivery contract 2.0
```

Resultado habitual:

```text
REJECTED
```

---

## 10.24 SerializationError

Corresponde a fallos al convertir una estructura válida en representación entregable.

Ejemplos:

```text
unsupported type
invalid canonical structure
JSON encoding failure
```

Resultado habitual:

```text
FAILED
```

---

## 10.25 AdapterResolutionError

Corresponde a la imposibilidad de resolver un adaptador apropiado.

Ejemplo:

```text
target requires HTTP_JSON
but adapter is not registered
```

Según el momento de detección podría clasificarse como:

```text
REJECTED
```

si se detecta antes de aceptar la operación.

La política deberá ser consistente.

---

## 10.26 TransportError

Representa fallos durante el mecanismo técnico.

Ejemplos:

```text
connection refused
network unreachable
broken pipe
remote reset
```

Resultado:

```text
FAILED
```

---

## 10.27 TimeoutError

Representa una operación que excede el límite temporal permitido.

Resultado:

```text
FAILED
```

con:

```text
code = DELIVERY_TIMEOUT
```

---

## 10.28 SecurityError

Representa una operación que no cumple requisitos de autorización o seguridad.

Ejemplos:

```text
consumer unauthorized
target forbidden
principal lacks permission
```

Resultado habitual:

```text
REJECTED
```

si se detecta antes de transporte.

---

## 10.29 InternalDeliveryError

Representa un fallo inesperado dentro del subsistema.

Ejemplo:

```text
unexpected invariant violation
```

Debe utilizarse como categoría de último recurso.

No deberá sustituir errores específicos conocidos.

---

## 10.30 No catch-all indiscriminado

Queda prohibido convertir cualquier excepción automáticamente a:

```text
DELIVERY_INTERNAL_ERROR
```

sin intentar clasificar primero condiciones conocidas.

---

## 10.31 Exception Mapping

La arquitectura deberá contar con un mecanismo claro de mapeo.

Conceptualmente:

```text
ValueError
      ↓
known context?
      ↓
DeliveryValidationError
```

o:

```text
TimeoutException
      ↓
DELIVERY_TIMEOUT
```

El mapping deberá estar centralizado cuando sea posible.

---

## 10.32 Error Mapper

Podrá existir conceptualmente:

```text
DeliveryErrorMapper
```

responsable de transformar errores internos a errores contractuales.

No deberá contener reglas cognitivas.

---

## 10.33 Ejemplo de mapping

```text
json.JSONEncodeError
      ↓
DeliveryError
├── code = DELIVERY_SERIALIZATION_ERROR
├── category = SERIALIZATION
└── stage = SERIALIZATION
```

---

## 10.34 Preservación de causa interna

Internamente podrá conservarse:

```text
cause
```

para debugging.

No deberá salir necesariamente al consumidor.

---

## 10.35 Exception chaining

En Python podrá utilizarse:

```python
raise DeliverySerializationError(...) from exc
```

para preservar causa interna.

La arquitectura podrá aprovechar esta capacidad sin exponer detalles públicamente.

---

## 10.36 ErrorResult siempre válido

Cuando ocurre un fallo, HEYTI deberá producir un `DeliveryResult` válido.

Ejemplo:

```text
Delivery failed
      ↓
DeliveryResult(
    status=FAILED,
    error=...
)
```

No deberá terminar con una estructura incompleta.

---

## 10.37 Fallo al construir DeliveryResult

Si incluso la construcción del resultado falla, deberá existir una estrategia mínima de emergencia interna.

Pero esta condición deberá considerarse crítica.

La arquitectura deberá diseñar `DeliveryResult` para ser simple y robusto.

---

## 10.38 Error mínimo de emergencia

Como último recurso interno podría existir:

```text
DELIVERY_INTERNAL_ERROR
```

con:

```text
delivery_id
response_id
```

si están disponibles.

No deberá utilizarse como camino normal.

---

## 10.39 Fail Fast

Los errores de precondición deberán detectarse cuanto antes.

Ejemplo:

```text
unsupported contract
```

debe detectarse antes de:

```text
serialization
network
```

---

## 10.40 No enviar parcialmente

La regla preferida será:

```text
complete valid payload
      ↓
send
```

y no:

```text
begin sending
      ↓
discover structure invalid
```

---

## 10.41 Atomicidad conceptual

Para entregas simples v1.0 deberá intentarse una semántica conceptual:

```text
Delivered
or
Not Delivered
```

Esto reduce estados ambiguos.

La atomicidad técnica dependerá del transporte.

---

## 10.42 Imposibilidad de atomicidad absoluta

En sistemas distribuidos puede ocurrir:

```text
sender times out
```

pero:

```text
receiver actually received payload
```

Por ello algunos estados pueden ser epistemológicamente inciertos.

La arquitectura deberá evitar afirmar más de lo que sabe.

---

## 10.43 Estado UNKNOWN futuro

En escenarios distribuidos podría resultar necesario:

```text
UNKNOWN
```

o:

```text
DELIVERY_UNCONFIRMED
```

si no puede determinarse el resultado real.

No se incorpora obligatoriamente en v1.0.

Pero la arquitectura deberá reconocer la posibilidad.

---

## 10.44 Honestidad operacional

Si HEYTI no puede confirmar recepción, no deberá declarar:

```text
DELIVERED
```

únicamente porque envió el payload.

El significado dependerá del criterio del adaptador.

---

## 10.45 Delivery acceptance criteria

Cada adaptador deberá definir qué evidencia técnica considera suficiente para:

```text
DELIVERED
```

Ejemplo InMemory:

```text
payload accepted into target buffer
```

Ejemplo HTTP:

```text
successful response code according to policy
```

---

## 10.46 Adaptador InMemory

Para un adaptador de pruebas:

```text
capture(payload)
```

podrá considerarse éxito si:

```text
payload stored successfully
```

Esto facilita pruebas deterministas.

---

## 10.47 HTTP success policy

Un adaptador HTTP futuro deberá definir cuáles códigos representan éxito.

No deberá asumir automáticamente:

```text
any response = DELIVERED
```

---

## 10.48 HTTP redirects

La política deberá definir si redirects:

```text
3xx
```

son:

- seguidos;
- rechazados;
- o considerados error.

Esto pertenece al adaptador, no al Delivery Contract central.

---

## 10.49 HTTP client errors

Respuestas:

```text
4xx
```

podrán mapearse según naturaleza.

Ejemplo:

```text
401 / 403
→ SECURITY
```

```text
404
→ TARGET / CONFIGURATION
```

---

## 10.50 HTTP server errors

Respuestas:

```text
5xx
```

normalmente corresponderán a:

```text
TARGET_UNAVAILABLE
TRANSPORT_ERROR
```

según política.

---

## 10.51 Timeout policy

Toda operación de red deberá contar con timeout explícito cuando se implemente.

Queda prohibido depender de espera indefinida.

---

## 10.52 Tipos de timeout

En un adaptador futuro podrán distinguirse:

```text
connect timeout
read timeout
overall timeout
```

No es necesario exponer esta granularidad en el contrato público.

---

## 10.53 Recovery

La recuperación deberá entenderse como una política controlada para responder a un fallo.

Podrá incluir:

```text
retry
fallback adapter
manual intervention
consumer notification
audit record
```

Ninguna estrategia deberá ejecutarse automáticamente sin política.

---

## 10.54 No Silent Recovery

Queda prohibido:

```text
HTTP failed
      ↓
silently use another consumer
      ↓
report success
```

Toda recuperación relevante deberá ser observable.

---

## 10.55 Retry Policy

Los reintentos deberán estar gobernados por una política explícita.

Conceptualmente:

```text
RetryPolicy
├── enabled
├── max_attempts
├── allowed_error_categories
├── backoff
└── idempotency_requirement
```

No es obligatorio implementar toda esta estructura en v1.0.

---

## 10.56 v1.0 sin retry automático

Para la primera implementación se recomienda:

```text
automatic_retry = false
```

Esto permite:

- simplicidad;
- trazabilidad clara;
- pruebas deterministas;
- evitar duplicación accidental.

---

## 10.57 Razón para evitar retry inicial

Antes de reintentar automáticamente debe conocerse:

```text
Did the consumer receive the first attempt?
```

Si no puede saberse, un retry podría duplicar efectos.

---

## 10.58 Idempotency

Un consumidor o adaptador podrá soportar idempotencia.

Conceptualmente:

```text
idempotency_key = delivery_id
```

o una clave específica.

Sin embargo, esta decisión deberá formalizarse antes de activar reintentos.

---

## 10.59 Reintentos con nueva identidad

Si en el futuro se habilitan retries, la preferencia arquitectónica será considerar cada intento como una operación trazable.

Ejemplo:

```text
DEL-001
  status=FAILED

DEL-002
  retry_of=DEL-001
  status=DELIVERED
```

Esto preserva historia.

---

## 10.60 Backoff

Una política futura podría aplicar:

```text
fixed
linear
exponential
```

backoff.

No deberá incorporarse hasta que exista un transporte que lo justifique.

---

## 10.61 Fallback Adapter

Podría existir en el futuro:

```text
Primary Adapter
     ↓ fail
Fallback Adapter
```

Pero esta estrategia deberá estar explícitamente autorizada.

---

## 10.62 Prohibición de fallback semántico

No deberá sustituirse:

```text
consumer A
```

por:

```text
consumer B
```

únicamente porque A falló.

Eso cambiaría el destino lógico.

---

## 10.63 Fallback técnico permitido

Podría existir:

```text
HTTP adapter implementation A
```

a:

```text
HTTP adapter implementation B
```

si ambos representan el mismo target y la política lo permite.

Aun así deberá registrarse.

---

## 10.64 Circuit Breaker futuro

En escenarios de producción podría resultar útil un:

```text
circuit breaker
```

para targets repetidamente fallidos.

No forma parte obligatoria de v1.0.

La arquitectura de adaptadores deberá permitir añadirlo externamente.

---

## 10.65 Dead Letter futuro

Si en el futuro existen colas asíncronas, podría existir:

```text
dead-letter queue
```

para entregas fallidas.

No pertenece al alcance inicial.

---

## 10.66 Manual Recovery

Para determinados errores, la respuesta correcta puede ser:

```text
operator fixes configuration
      ↓
new DeliveryRequest
```

en lugar de retry automático.

---

## 10.67 Recovery no modifica response_id

Una recuperación no deberá generar nueva respuesta cognitiva si se reutiliza la misma respuesta materializada.

Por ejemplo:

```text
RESP-001
   ├── DEL-001 FAILED
   └── DEL-002 DELIVERED
```

---

## 10.68 Nueva ejecución cognitiva

Si es necesario cambiar el contenido de la respuesta, entonces deberá producirse:

```text
new execution
new response_id
```

No debe utilizarse Delivery para corregir significado.

---

## 10.69 Error propagation

Los errores deberán propagarse de manera controlada hacia el nivel apropiado.

Ejemplo:

```text
Adapter exception
      ↓
DeliveryError
      ↓
DeliveryResult
      ↓
Gateway/API
      ↓
Consumer
```

No todo detalle deberá propagarse.

---

## 10.70 Public Error Projection

Podrá existir una proyección pública del error.

Ejemplo interno:

```text
code = DELIVERY_ADAPTER_ERROR
cause = ConnectionRefusedError
host = internal-host
port = 9000
```

Public:

```text
code = DELIVERY_TARGET_UNAVAILABLE
message = "Delivery target is unavailable."
```

---

## 10.71 Seguridad en errores

Los errores no deberán revelar:

```text
passwords
tokens
database URLs
internal paths
stack traces
server secrets
```

---

## 10.72 No ocultar error semántico relevante

Seguridad no significa convertir todos los fallos en:

```text
"Something went wrong."
```

El código estable deberá conservar suficiente significado.

---

## 10.73 Error logging

El logging interno podrá registrar mayor detalle.

Ejemplo:

```text
delivery_id
error code
stage
exception type
duration
adapter
```

---

## 10.74 Error metrics

Podrán generarse métricas como:

```text
delivery_error_total
delivery_timeout_total
delivery_serialization_error_total
delivery_rejected_total
delivery_transport_error_total
```

---

## 10.75 Error alerting

En producción, determinados errores podrán activar alertas.

Ejemplo:

```text
repeated INTERNAL errors
```

o:

```text
target unavailable for sustained period
```

La política de alertas queda fuera del contrato central.

---

## 10.76 Error auditability

Una entrega fallida deberá poder ser auditada.

Debe poder determinarse:

```text
response_id
delivery_id
consumer
adapter
stage
error code
timestamp
```

---

## 10.77 Error y DeliveryTrace

Conceptualmente:

```text
DeliveryTrace
      +
DeliveryError
      =
explainable failure
```

---

## 10.78 Error correlation

Un `DeliveryError` deberá referenciar el `delivery_id` correspondiente cuando sea posible.

Nunca deberá quedar como error aislado sin contexto.

---

## 10.79 Error antes de delivery_id

Si falla la generación del propio `delivery_id`, la arquitectura deberá utilizar contexto anterior como:

```text
response_id
request_id
```

para registrar el fallo.

Esta situación debería ser extremadamente rara.

---

## 10.80 Error durante tracing

Si el trace falla después de una entrega técnicamente exitosa, deberá distinguirse:

```text
delivery execution success
```

de:

```text
observability failure
```

La política deberá decidir si esto degrada el resultado global.

---

## 10.81 Observability failure

Un fallo de logging no debería necesariamente cambiar:

```text
DELIVERED
```

a:

```text
FAILED
```

si la entrega ya ocurrió correctamente.

Pero un fallo de auditoría obligatoria podría ser más serio.

La política deberá definir esta diferencia.

---

## 10.82 Core Delivery vs auxiliary services

Debe distinguirse:

```text
critical path
```

de:

```text
auxiliary observability
```

para evitar que servicios auxiliares rompan Delivery sin necesidad.

---

## 10.83 Error de payload demasiado grande

Si el payload supera un límite:

```text
DELIVERY_PAYLOAD_TOO_LARGE
```

podría ser un código futuro.

La operación deberá detenerse antes del transporte cuando sea posible.

---

## 10.84 Error de encoding

Ejemplo:

```text
DELIVERY_ENCODING_ERROR
```

podrá mapearse bajo:

```text
DELIVERY_SERIALIZATION_ERROR
```

si se prefiere una API más simple.

---

## 10.85 Error de schema

Ejemplo:

```text
DELIVERY_PAYLOAD_VALIDATION_ERROR
```

podría utilizarse internamente.

La taxonomía pública deberá evitar demasiados códigos.

---

## 10.86 Error de contrato

El error:

```text
DELIVERY_CONTRACT_MISMATCH
```

deberá utilizarse cuando las versiones no sean compatibles.

No deberá utilizarse para tipos incorrectos ordinarios.

---

## 10.87 Error de consumidor

```text
DELIVERY_UNSUPPORTED_CONSUMER
```

deberá indicar identidad lógica desconocida o no soportada.

---

## 10.88 Error de adaptador

```text
DELIVERY_ADAPTER_NOT_AVAILABLE
```

deberá diferenciarse de:

```text
DELIVERY_ADAPTER_ERROR
```

El primero significa que no existe o no puede resolverse.

El segundo significa que existía pero falló durante ejecución.

---

## 10.89 Error de target

```text
DELIVERY_TARGET_UNAVAILABLE
```

significa que el destino no pudo ser alcanzado o aceptado según política.

---

## 10.90 Error de timeout

```text
DELIVERY_TIMEOUT
```

deberá mantenerse separado cuando sea útil para políticas futuras.

---

## 10.91 Error interno

```text
DELIVERY_INTERNAL_ERROR
```

deberá indicar una condición no esperada dentro de HEYTI Delivery.

La aparición frecuente de este código deberá considerarse señal de defecto arquitectónico o de implementación.

---

## 10.92 Catálogo inicial recomendado

Se propone para v1.0 un catálogo público reducido:

```text
DELIVERY_VALIDATION_ERROR
DELIVERY_CONTRACT_MISMATCH
DELIVERY_UNSUPPORTED_CONSUMER
DELIVERY_SERIALIZATION_ERROR
DELIVERY_ADAPTER_NOT_AVAILABLE
DELIVERY_TARGET_UNAVAILABLE
DELIVERY_TIMEOUT
DELIVERY_ADAPTER_ERROR
DELIVERY_NOT_AUTHORIZED
DELIVERY_INTERNAL_ERROR
```

Los detalles internos podrán utilizar subcódigos.

---

## 10.93 Razón para catálogo reducido

Demasiados códigos públicos producen:

- dependencia excesiva de consumidores;
- dificultad de versionado;
- semántica fragmentada.

La granularidad fina puede permanecer internamente.

---

## 10.94 Subcode

Conceptualmente podrá existir:

```text
error.code = DELIVERY_VALIDATION_ERROR
error.subcode = MISSING_REQUIRED_FIELD
```

si se requiere.

No es obligatorio desde el inicio.

---

## 10.95 Result mapping

El mapping de error a estado deberá ser explícito.

Ejemplo:

| Error | Estado sugerido |
|---|---|
| DELIVERY_VALIDATION_ERROR | REJECTED |
| DELIVERY_CONTRACT_MISMATCH | REJECTED |
| DELIVERY_UNSUPPORTED_CONSUMER | REJECTED |
| DELIVERY_NOT_AUTHORIZED | REJECTED |
| DELIVERY_SERIALIZATION_ERROR | FAILED |
| DELIVERY_ADAPTER_NOT_AVAILABLE | REJECTED |
| DELIVERY_TARGET_UNAVAILABLE | FAILED |
| DELIVERY_TIMEOUT | FAILED |
| DELIVERY_ADAPTER_ERROR | FAILED |
| DELIVERY_INTERNAL_ERROR | FAILED |

La implementación deberá mantener una política consistente.

---

## 10.96 Error classification function

Podrá existir conceptualmente:

```python
classify_error(error) -> DeliveryStatus
```

pero deberá estar gobernada por reglas claras.

---

## 10.97 Error invariants

Se establecen invariantes como:

```text
status = FAILED
⇒ error exists
```

```text
status = REJECTED
⇒ error exists
```

```text
status = DELIVERED
⇒ fatal error absent
```

---

## 10.98 Warning con DELIVERED

Una entrega `DELIVERED` sí podrá contener:

```text
warnings
```

Ejemplo:

```text
payload size high
```

si no impidió la entrega.

---

## 10.99 Cognitive warning con DELIVERED

Una respuesta cognitiva podrá contener advertencias y aun ser entregada correctamente.

Ejemplo:

```text
response.status = PARTIAL
delivery.status = DELIVERED
```

Esto significa que una respuesta parcial fue entregada exitosamente.

---

## 10.100 Error de Presentation

Un error posterior de UI deberá representarse fuera de Delivery.

Ejemplo:

```text
Delivery = DELIVERED
Presentation = FAILED
```

No deberá modificarse el `DeliveryResult`.

---

## 10.101 Error boundary

Conceptualmente:

```text
Materialization Error Boundary
      ↓
Delivery Error Boundary
      ↓
Transport Error Boundary
      ↓
Presentation Error Boundary
```

Cada frontera deberá conservar atribución propia.

---

## 10.102 Error containment

Un error deberá quedar contenido en la capa responsable siempre que sea posible.

Esto evita propagación semántica incorrecta.

---

## 10.103 Recovery boundary

La recuperación de Delivery deberá ocurrir dentro de políticas de Delivery.

No deberá invocar automáticamente:

```text
new capability
new cognition
```

para compensar un error técnico.

---

## 10.104 Ejemplo: serialización fallida

```text
MaterializedResponse = VALID
      ↓
DeliveryRequest = VALID
      ↓
Serialization
      ↓
Unsupported Type
      ↓
DeliveryError
      code = DELIVERY_SERIALIZATION_ERROR
      category = SERIALIZATION
      stage = SERIALIZATION
      ↓
DeliveryResult
      status = FAILED
```

---

## 10.105 Ejemplo: consumidor incompatible

```text
Response Contract = 2.0
Consumer Supports = 1.0
      ↓
Compatibility Validation
      ↓
DeliveryError
      code = DELIVERY_CONTRACT_MISMATCH
      category = COMPATIBILITY
      ↓
DeliveryResult
      status = REJECTED
```

El adaptador no se ejecuta.

---

## 10.106 Ejemplo: timeout

```text
Payload = VALID
      ↓
Adapter = HTTP_JSON
      ↓
Target does not respond
      ↓
Timeout
      ↓
DeliveryError
      code = DELIVERY_TIMEOUT
      category = TIMEOUT
      ↓
DeliveryResult
      status = FAILED
```

---

## 10.107 Ejemplo: no autorizado

```text
Consumer = VALID
Principal = NOT AUTHORIZED
      ↓
Security Validation
      ↓
DeliveryError
      code = DELIVERY_NOT_AUTHORIZED
      category = SECURITY
      ↓
DeliveryResult
      status = REJECTED
```

---

## 10.108 Ejemplo: fallo inesperado

```text
Unexpected Internal Exception
      ↓
Error Mapper
      ↓
DeliveryError
      code = DELIVERY_INTERNAL_ERROR
      category = INTERNAL
      ↓
DeliveryResult
      status = FAILED
```

Internamente deberá conservarse información suficiente para diagnóstico.

---

## 10.109 State machine conceptual

```text
CREATED
   │
   ▼
VALIDATING
   │
   ├──────────────► REJECTED
   │
   ▼
READY
   │
   ▼
SERIALIZING
   │
   ├──────────────► FAILED
   │
   ▼
DELIVERING
   │
   ├──────────────► FAILED
   │
   ▼
DELIVERED
```

Los estados transitorios podrán simplificarse en implementación.

---

## 10.110 Estados terminales

```text
DELIVERED
REJECTED
FAILED
```

deberán ser terminales para una operación individual.

Un retry deberá considerarse nueva operación o intento formalmente relacionado.

---

## 10.111 No reabrir operación terminal

Una vez:

```text
DEL-001 = FAILED
```

no deberá cambiar posteriormente a:

```text
DEL-001 = DELIVERED
```

si se realiza un nuevo intento independiente.

Preferible:

```text
DEL-002 = DELIVERED
retry_of = DEL-001
```

---

## 10.112 Ventaja de inmutabilidad histórica

Este modelo conserva la historia real.

```text
Attempt 1 failed.
Attempt 2 succeeded.
```

No la reescribe como:

```text
Delivery succeeded.
```

ocultando el fallo previo.

---

## 10.113 Error Contract conceptual

```text
DeliveryError
├── code
├── category
├── message
├── stage
├── recoverable
├── timestamp
├── details?
└── internal_cause?   [internal only]
```

---

## 10.114 DeliveryResult conceptual

```text
DeliveryResult
├── delivery_id
├── response_id
├── status
├── consumer_id
├── adapter_id
├── started_at
├── completed_at
├── error?
├── warnings
├── receipt?
└── trace
```

---

## 10.115 Error serializable

Todo `DeliveryError` público deberá poder convertirse a representación canónica.

No deberá depender de objetos de excepción activos.

---

## 10.116 Error determinista

Una misma condición conocida deberá mapearse de manera consistente al mismo código.

Ejemplo:

```text
unsupported contract version
```

no deberá producir unas veces:

```text
DELIVERY_VALIDATION_ERROR
```

y otras:

```text
DELIVERY_INTERNAL_ERROR
```

sin razón.

---

## 10.117 Testing de errores

Los errores deberán probarse como parte central del sistema.

No únicamente los flujos exitosos.

---

## 10.118 Tests mínimos de validación

```text
test_missing_required_field_is_rejected
test_invalid_contract_is_rejected
test_unsupported_consumer_is_rejected
```

---

## 10.119 Tests mínimos de serialización

```text
test_unsupported_type_produces_serialization_error
test_serialization_failure_does_not_execute_adapter
```

---

## 10.120 Tests mínimos de adaptador

```text
test_adapter_failure_returns_failed_result
test_target_unavailable_is_classified
test_timeout_is_classified
```

---

## 10.121 Tests mínimos de seguridad

```text
test_unauthorized_delivery_is_rejected
test_rejected_security_delivery_does_not_execute_adapter
```

---

## 10.122 Tests mínimos de trazabilidad de error

```text
test_failed_result_preserves_delivery_id
test_failed_result_preserves_response_id
test_error_records_stage
```

---

## 10.123 Tests de no ocultamiento

Deberá verificarse que:

```text
adapter raises error
```

no termine en:

```text
DELIVERED
```

---

## 10.124 Tests de no mutación cognitiva

Ante fallo de Delivery:

```text
MaterializedResponse
```

deberá permanecer sin cambios.

---

## 10.125 Tests de estado terminal

Una operación terminada deberá tener exactamente uno de:

```text
DELIVERED
REJECTED
FAILED
```

---

## 10.126 Tests de error/result consistency

Ejemplo:

```text
FAILED without error
```

deberá ser inválido.

---

## 10.127 Fault Injection

En etapas posteriores podrán introducirse fallos artificiales:

```text
serializer failure
adapter failure
timeout
invalid receipt
```

para comprobar robustez.

---

## 10.128 InMemory failing adapter

La implementación inicial debería considerar un adaptador de prueba capaz de simular:

```text
success
failure
timeout-like error
```

Esto facilitará pruebas sin red.

---

## 10.129 Recovery tests

Cuando exista retry futuro deberán probarse:

```text
retry only permitted errors
no retry on validation error
new delivery identity on retry
trace parent relationship
```

---

## 10.130 Métricas de errores

Como mínimo, la arquitectura deberá permitir medir:

```text
delivery_total
delivery_delivered_total
delivery_rejected_total
delivery_failed_total
```

y opcionalmente por código:

```text
delivery_error_total{code=...}
```

---

## 10.131 Error rate

Podrá derivarse:

```text
failure_rate
rejection_rate
```

para detectar degradación.

---

## 10.132 Distinción de rejection rate

Una tasa alta de `REJECTED` puede indicar:

- contrato incompatible;
- integración incorrecta;
- consumidor desactualizado.

No necesariamente infraestructura caída.

---

## 10.133 Distinción de failure rate

Una tasa alta de `FAILED` puede indicar:

- problema de serializer;
- transporte;
- target;
- adaptador.

Esta separación tiene valor operacional.

---

## 10.134 Error budget futuro

En una fase madura podrían definirse objetivos de confiabilidad.

No forma parte de v1.0.

---

## 10.135 Alertas por INTERNAL_ERROR

`DELIVERY_INTERNAL_ERROR` deberá tratarse como señal importante.

La existencia ocasional puede ocurrir.

Su repetición deberá activar investigación.

---

## 10.136 Error documentation

Cada error público deberá documentarse con:

```text
code
meaning
typical cause
terminal status
recoverable
consumer action
```

cuando se formalice el catálogo final.

---

## 10.137 Ejemplo de documentación

```text
Code:
DELIVERY_CONTRACT_MISMATCH

Meaning:
The consumer or delivery subsystem does not support the required contract version.

Status:
REJECTED

Retry:
No, unless configuration or version support changes.
```

---

## 10.138 Consumer behavior

El contrato deberá permitir al consumidor decidir cómo representar errores.

Ejemplo:

```text
DELIVERY_TIMEOUT
```

podrá mostrarse como:

> No fue posible recibir la respuesta en este momento.

Pero esa traducción pertenece a Presentation.

---

## 10.139 Delivery no escribe mensajes visuales finales

Delivery podrá proporcionar:

```text
code
message
```

pero no deberá decidir:

```text
red modal
toast
retry button
```

---

## 10.140 Error actions

Una futura respuesta de error podrá incluir acciones abstractas autorizadas.

Ejemplo:

```text
RETRY
CONTACT_SUPPORT
REFRESH
```

Sin embargo, deberá existir un contrato explícito.

No forma parte necesaria de v1.0.

---

## 10.141 Error and Gateway

El Gateway podrá mapear `DeliveryError` a códigos de protocolo.

Ejemplo HTTP futuro:

```text
DELIVERY_NOT_AUTHORIZED
→ 403
```

```text
DELIVERY_CONTRACT_MISMATCH
→ 409 or 422
```

La política HTTP pertenece al Gateway/adapter.

---

## 10.142 DeliveryError no debe contener HTTP status

El contrato central no debería requerir:

```text
http_status
```

si quiere preservar independencia de transporte.

Un adapter específico podrá añadirlo como metadata técnica.

---

## 10.143 Error and WebSocket

Un adaptador WebSocket futuro podría mapear:

```text
DeliveryError
```

a un evento:

```text
heyti.delivery.error
```

sin modificar el modelo central.

---

## 10.144 Error and InMemory

Un adaptador InMemory podrá devolver directamente:

```text
AdapterResult
```

para pruebas.

El mismo `DeliveryError` deberá continuar siendo válido.

---

## 10.145 No technology-specific error codes in core

El catálogo central debería evitar códigos como:

```text
HTTP_503_ERROR
WEBSOCKET_FRAME_ERROR
```

como primera abstracción pública.

Preferible:

```text
DELIVERY_TARGET_UNAVAILABLE
DELIVERY_ADAPTER_ERROR
```

con detalle técnico interno.

---

## 10.146 Regla de abstracción

El error central describe:

```text
what happened semantically in Delivery
```

El adaptador describe:

```text
how it happened technically
```

---

## 10.147 Matriz de responsabilidad de errores

| Tipo de error | Responsable |
|---|---|
| Respuesta inválida | Materialization/Delivery Boundary |
| Consumer incompatible | Delivery |
| Serialización | Delivery |
| Adapter resolution | Delivery |
| Network | Adapter/Transport |
| Timeout | Adapter/Transport |
| UI rendering | Presentation |
| Cognitive conclusion error | Cognitive Domain |

Esta matriz deberá evitar atribución incorrecta.

---

## 10.148 Invariantes de errores y recuperación

Se establecen los siguientes invariantes.

### HRRD-E01 — Explicit Error

Todo fallo deberá producir representación explícita.

### HRRD-E02 — Error Ownership

Cada error deberá atribuirse a la frontera responsable.

### HRRD-E03 — No Silent Catch

Ninguna excepción relevante deberá ocultarse silenciosamente.

### HRRD-E04 — Stable Error Codes

Los códigos públicos deberán permanecer estables dentro de una versión contractual.

### HRRD-E05 — Failure Does Not Mutate Response

Un fallo de Delivery no modifica la respuesta materializada.

### HRRD-E06 — Rejection Before Boundary

Los errores de precondición deberán impedir la entrega.

### HRRD-E07 — No Implicit Retry

No habrá reintentos automáticos sin política.

### HRRD-E08 — Terminal State Integrity

Toda operación deberá terminar en un estado terminal consistente.

### HRRD-E09 — Traceable Error

Todo error deberá correlacionarse con la operación correspondiente.

### HRRD-E10 — Secure Error Exposure

Los errores públicos no deberán filtrar información sensible.

---

## 10.149 Prueba de conformidad de errores

Una implementación deberá poder demostrar:

1. que diferencia `REJECTED` y `FAILED`;
2. que no marca errores como éxito;
3. que los errores tienen código estable;
4. que existe categoría y etapa suficientes para diagnóstico;
5. que se conserva `delivery_id`;
6. que se conserva `response_id`;
7. que las excepciones internas se mapean;
8. que no se exponen secretos;
9. que no se ejecutan retries implícitos;
10. que la respuesta original no se modifica.

---

## 10.150 Flujo consolidado de error

```text
Operation
   │
   ▼
Error Detected
   │
   ▼
Classify
   │
   ▼
Map to DeliveryError
   │
   ▼
Determine Terminal Status
   │
   ├── REJECTED
   └── FAILED
   │
   ▼
Complete Trace
   │
   ▼
Build DeliveryResult
   │
   ▼
Emit Observability
```

---

## 10.151 Flujo consolidado de recuperación futura

```text
DeliveryResult = FAILED
        │
        ▼
Recovery Policy
        │
        ├── NO RECOVERY
        │
        ├── MANUAL RECOVERY
        │
        └── RETRY
                 │
                 ▼
         New Delivery Operation
```

La operación fallida original permanece inmutable.

---

## 10.152 Criterio de éxito

El modelo de errores será considerado correcto cuando cualquier fallo conocido pueda responder:

```text
What failed?
Where?
Why?
Which delivery?
Which response?
Was it rejected or failed?
Did the adapter execute?
Can it be recovered?
Was anything delivered?
```

sin depender de conjeturas.

---

## 10.153 Declaración arquitectónica del capítulo

El tratamiento de errores de Runtime Response Delivery deberá ser explícito, estructurado, trazable y honesto.

HEYTI no deberá ocultar fallos.

No deberá atribuirlos a capas incorrectas.

No deberá modificar respuestas cognitivas para compensarlos.

No deberá reintentar silenciosamente.

Y no deberá declarar una entrega exitosa cuando carezca de evidencia suficiente para hacerlo.

La regla arquitectónica consolidada queda establecida como:

> **Todo error de Delivery deberá convertirse en un hecho operacional identificable: con código, categoría, etapa, identidad de entrega, relación con la respuesta y estado terminal inequívoco. La recuperación, cuando exista, deberá ser una decisión explícita y trazable, nunca una corrección silenciosa.**

La separación fundamental queda formalizada como:

```text
INVALID PRECONDITION
        ↓
REJECTED

VALID OPERATION + OPERATIONAL ERROR
        ↓
FAILED

VALID OPERATION + SUCCESS CRITERIA SATISFIED
        ↓
DELIVERED
```

Con esta arquitectura de errores queda preparada la siguiente dimensión de Runtime Response Delivery:

**la relación formal entre Delivery, Session Management y contexto operacional de ejecución.**

---

**Fin del Capítulo 10**


# Capítulo 11. Session Management y contexto operacional de Delivery

## 11.1 Propósito del capítulo

Este capítulo define la relación formal entre **HEYTI Runtime Response Delivery (HRRD)**, el **Session Management** y el contexto operacional que acompaña a una entrega.

La finalidad es garantizar que una respuesta pueda ser entregada conservando, cuando corresponda, la información necesaria para identificar:

- la sesión en la que se originó;
- la solicitud asociada;
- la ejecución correspondiente;
- el consumidor;
- el actor o principal involucrado;
- el contexto temporal;
- y las condiciones operativas bajo las cuales se realizó Delivery.

El contexto no deberá utilizarse como un contenedor arbitrario de estado.

Su función será más precisa:

> **Proporcionar a Delivery la información explícita necesaria para ejecutar, correlacionar, autorizar, observar y auditar una operación sin depender de estado global oculto.**

---

## 11.2 Principio fundamental

La regla central será:

```text
Explicit Context
      >
Implicit Global State
```

Toda información necesaria para una entrega deberá provenir preferentemente de:

```text
DeliveryRequest
DeliveryContext
Session Context
Consumer Profile
Delivery Policy
```

y no de variables globales circunstanciales.

---

## 11.3 Session Management

Session Management constituye el componente responsable de mantener la identidad y continuidad de una sesión HEYTI.

Conceptualmente:

```text
Session
├── session_id
├── lifecycle
├── context
├── requests
└── metadata
```

Delivery podrá utilizar información de sesión.

No deberá convertirse en administrador de sesiones.

---

## 11.4 Frontera con SessionManager

La relación permitida será:

```text
SessionManager
      │
      ▼
Session Context
      │
      ▼
DeliveryContext
```

Queda prohibido:

```text
Response Delivery
      │
      ▼
create / destroy / mutate session arbitrarily
```

salvo que una arquitectura posterior establezca explícitamente una responsabilidad adicional.

---

## 11.5 Responsabilidad de SessionManager

SessionManager será responsable de funciones como:

- crear sesión;
- identificar sesión;
- recuperar contexto de sesión;
- actualizar estado permitido;
- cerrar sesión;
- administrar ciclo de vida.

Runtime Response Delivery no deberá duplicar esas responsabilidades.

---

## 11.6 Responsabilidad de Delivery

Delivery utilizará el contexto de sesión únicamente cuando sea necesario para:

- correlación;
- trazabilidad;
- seguridad;
- selección de consumidor;
- auditoría;
- o continuidad operacional.

---

## 11.7 Session ID como referencia

Delivery deberá tratar:

```text
session_id
```

como una referencia.

No como una estructura completa de sesión.

Ejemplo:

```text
DeliveryContext
    session_id = SES-001
```

es preferible a transportar:

```text
entire session object
```

sin necesidad.

---

## 11.8 Principio de mínimo contexto

La arquitectura deberá aplicar:

> **Transport and retain only the context required for Delivery.**

Esto reduce:

- acoplamiento;
- riesgo de privacidad;
- exposición innecesaria;
- dificultad de pruebas;
- dependencia de SessionManager.

---

## 11.9 DeliveryContext

Se define conceptualmente:

```text
DeliveryContext
```

como la estructura operacional que acompaña a una operación.

Podrá contener:

```text
session_id
request_id
execution_id
response_id
delivery_id
correlation_id
consumer_id
principal_id
request_origin
environment
timezone
locale
```

No todos los campos serán obligatorios.

---

## 11.10 Contexto mínimo v1.0

Para v1.0 se recomienda considerar como mínimo:

```text
response_id
delivery_id
consumer_id
adapter_id
```

y preservar cuando estén disponibles:

```text
session_id
request_id
execution_id
correlation_id
```

---

## 11.11 Contexto obligatorio vs opcional

La arquitectura deberá clasificar campos como:

```text
REQUIRED
OPTIONAL
CONDITIONAL
```

Ejemplo:

```text
delivery_id = REQUIRED
consumer_id = REQUIRED
session_id  = OPTIONAL
```

para operaciones no interactivas.

---

## 11.12 Contexto condicional

Un consumidor interactivo podría requerir sesión.

Ejemplo:

```text
consumer_id = HEYTI_UI
⇒ session_id REQUIRED
```

Mientras:

```text
consumer_id = TEST_HARNESS
⇒ session_id OPTIONAL
```

La regla deberá depender de contrato o política.

---

## 11.13 Session Context

SessionManager podrá exponer conceptualmente:

```text
SessionContext
├── session_id
├── principal_id
├── created_at
├── last_activity_at
├── attributes
└── state
```

Delivery no deberá copiar automáticamente todos estos elementos.

---

## 11.14 Context Projection

Deberá existir conceptualmente una proyección:

```text
SessionContext
      ↓
Delivery Context Projection
      ↓
DeliveryContext
```

Solo los elementos relevantes deberán atravesar la frontera.

---

## 11.15 No compartir objeto mutable de sesión

Delivery no debería recibir una referencia mutable directa al objeto interno de sesión si puede evitarse.

Preferible:

```text
immutable snapshot
```

o:

```text
explicit context values
```

Esto evita mutaciones accidentales.

---

## 11.16 Snapshot de sesión

Al iniciar una entrega podrá capturarse un snapshot de los campos necesarios.

Ejemplo:

```text
session_id = SES-001
principal_id = PR-001
consumer_id = AT_PORTAL
```

Estos valores deberán permanecer estables durante la operación.

---

## 11.17 Cambio de sesión durante Delivery

Si la sesión cambia mientras Delivery está en curso, la operación deberá conservar el snapshot con el que comenzó.

Esto garantiza auditoría.

---

## 11.18 Session lifecycle y Delivery

La arquitectura deberá considerar estados de sesión como:

```text
ACTIVE
EXPIRED
CLOSED
INVALID
```

si SessionManager los define.

Una sesión inválida podrá bloquear Delivery cuando sea requerida.

---

## 11.19 Sesión expirada

Ejemplo:

```text
session_id = SES-001
session_status = EXPIRED
```

Si la política requiere sesión activa:

```text
REJECTED
```

antes de cruzar la frontera.

---

## 11.20 Sesión no requerida

Una operación interna podrá no depender de sesión.

Ejemplo:

```text
scheduled internal test
```

En ese escenario:

```text
session_id = null
```

podrá ser válido.

---

## 11.21 No inventar sesión

Delivery no deberá crear una sesión implícita únicamente para satisfacer un campo ausente.

Si una sesión es necesaria, deberá provenir del flujo correcto.

---

## 11.22 Request Context

Además de la sesión podrá existir un contexto de solicitud.

Conceptualmente:

```text
RequestContext
├── request_id
├── session_id
├── principal_id
├── origin
├── requested_at
└── metadata
```

Delivery deberá preservar únicamente aquello necesario.

---

## 11.23 Execution Context

Runtime podrá producir:

```text
ExecutionContext
├── execution_id
├── request_id
├── capability_id
├── started_at
└── runtime metadata
```

Materialization y Delivery deberán conservar las referencias relevantes.

---

## 11.24 Context chain

La cadena conceptual será:

```text
SessionContext
      ↓
RequestContext
      ↓
ExecutionContext
      ↓
MaterializationContext
      ↓
DeliveryContext
```

Cada capa podrá agregar información de su responsabilidad.

---

## 11.25 Regla de propagación

La propagación deberá ser:

```text
preserve previous identifiers
+
add own identifiers
```

Ejemplo:

```text
SessionManager
  session_id

Gateway
  request_id

Runtime
  execution_id

Materialization
  response_id

Delivery
  delivery_id
```

---

## 11.26 No regenerar contexto previo

Delivery no deberá regenerar:

```text
session_id
request_id
execution_id
response_id
```

cuando ya existan.

---

## 11.27 Context consistency

Los identificadores deberán permanecer coherentes.

Ejemplo:

```text
DeliveryContext.response_id
==
MaterializedResponse.response_id
```

Una discrepancia deberá generar error de validación.

---

## 11.28 Consumer Context

La operación también deberá identificar:

```text
consumer_id
```

y, cuando sea necesario:

```text
consumer_profile_version
```

Esto forma parte del contexto operacional.

---

## 11.29 Principal Context

En escenarios con seguridad podrá existir:

```text
principal_id
```

representando al actor autenticado o autorizado.

Delivery deberá preservar este identificador cuando sea necesario para autorización o auditoría.

---

## 11.30 Principal no es usuario visual

`principal_id` representa identidad de seguridad.

No necesariamente corresponde directamente a un nombre mostrado en UI.

La capa de Delivery deberá tratarlo como referencia técnica.

---

## 11.31 Authentication Context

Podrá existir:

```text
authentication_context
```

con información como:

```text
authentication_method
authenticated_at
```

si la infraestructura lo requiere.

No deberá transportarse información sensible innecesaria.

---

## 11.32 Authorization Context

Delivery podrá recibir una decisión previa o contexto necesario para verificar:

```text
may this principal deliver to this consumer?
```

Pero deberá evitar reimplementar todo el sistema de autorización.

---

## 11.33 Autorización explícita

La secuencia conceptual podrá ser:

```text
Principal
   ↓
Authorization Policy
   ↓
Delivery Allowed?
   │
   ├── NO → REJECTED
   └── YES
         ↓
      Delivery
```

---

## 11.34 Contexto de origen

`request_origin` podrá indicar conceptualmente:

```text
PORTAL
API
INTERNAL
TEST
```

Esto podrá ser útil para observabilidad.

No deberá utilizarse para decisiones cognitivas.

---

## 11.35 Environment

Podrá preservarse:

```text
environment
```

con valores como:

```text
development
testing
staging
production
```

si ayuda a auditoría.

---

## 11.36 Environment no modifica semántica

Una respuesta no deberá cambiar cognitivamente porque:

```text
environment = development
```

El entorno podrá cambiar:

- transporte;
- logging;
- adapter;
- configuración operacional.

No significado cognitivo.

---

## 11.37 Timezone

El contexto podrá incluir:

```text
timezone
```

cuando sea necesario interpretar eventos temporales.

Ejemplo:

```text
America/Mexico_City
```

La arquitectura deberá preferir timestamps con offset explícito.

---

## 11.38 Locale

Podrá existir:

```text
locale
```

como:

```text
es-MX
```

Esto puede ser útil para consumidores.

Sin embargo, Delivery no deberá reescribir contenido para adaptar presentación.

---

## 11.39 Contexto y personalización

Una futura UI podría utilizar el contexto para decidir presentación.

Ejemplo:

```text
locale = es-MX
```

Pero esa decisión pertenece al consumidor.

---

## 11.40 Context Metadata

Podrá existir metadata contextual extensible.

Ejemplo:

```text
channel
client_version
device_type
```

si existe necesidad.

No deberá convertirse en un mecanismo sin gobernanza.

---

## 11.41 Context Size

DeliveryContext deberá permanecer pequeño.

No deberá incluir:

```text
entire user profile
entire session history
entire capability registry
entire HKS state
```

---

## 11.42 Context is not memory

Debe distinguirse:

```text
DeliveryContext
```

de:

```text
Conversational Memory
```

El primero transporta información operacional.

El segundo pertenece a sistemas de memoria o sesión cognitiva.

---

## 11.43 Context is not knowledge

DeliveryContext tampoco deberá contener conocimiento territorial o electoral para ser interpretado por Delivery.

Ejemplo incorrecto:

```text
context.margin = 2.4%
therefore change delivery priority
```

Eso es regla de negocio.

---

## 11.44 Context is not Presentation State

No deberá incluirse:

```text
current_tab
map_zoom
open_panel
chart_color
selected_dom_element
```

dentro del contexto central de Delivery.

Estos elementos pertenecen a Presentation.

---

## 11.45 Excepción: acciones semánticas

Podrá transportarse un contexto semántico para una acción.

Ejemplo:

```text
section_id = 1481
module = TERRITORIAL
```

pero no estado visual de implementación.

---

## 11.46 Session continuity

La sesión permitirá que múltiples respuestas estén relacionadas.

Ejemplo:

```text
Session SES-001

REQ-001
  ↓
RESP-001
  ↓
DEL-001

REQ-002
  ↓
RESP-002
  ↓
DEL-002
```

Esto permite continuidad sin mezclar identidades.

---

## 11.47 Delivery y conversación

En una futura interfaz HEYTI conversacional, cada respuesta podrá conservar:

```text
session_id
```

para vincularla con el diálogo.

Delivery no deberá interpretar la conversación.

---

## 11.48 Conversation turn

Podrá existir en el futuro:

```text
turn_id
```

o:

```text
interaction_id
```

si el modelo conversacional lo necesita.

No es obligatorio en v1.0.

---

## 11.49 No sobre-modelar turnos

Mientras no exista una interfaz conversacional implementada, no deberá incorporarse complejidad innecesaria.

---

## 11.50 Contexto de Capability

Podrá preservarse:

```text
capability_id
```

dentro del trace o contexto.

No deberá incluirse el objeto completo de capability.

---

## 11.51 Contexto de conocimiento

Podrá preservarse:

```text
knowledge_version
```

si viene de Materialization.

Delivery no deberá recuperar o calcularlo.

---

## 11.52 Contexto de datos

Podrá preservarse:

```text
data_as_of
dataset_version
```

como procedencia.

No deberá copiarse de forma redundante si ya forma parte de Response Contract.

---

## 11.53 DeliveryContext y Trace

Debe distinguirse:

```text
DeliveryContext
```

de:

```text
DeliveryTrace
```

DeliveryContext representa:

> Información disponible y necesaria durante la operación.

DeliveryTrace representa:

> Evidencia de lo que ocurrió durante la operación.

---

## 11.54 Ejemplo

Antes de Delivery:

```text
DeliveryContext
├── session_id = SES-001
├── consumer_id = AT_PORTAL
└── correlation_id = CORR-001
```

Después:

```text
DeliveryTrace
├── session_id = SES-001
├── consumer_id = AT_PORTAL
├── adapter_id = IN_MEMORY
├── started_at = ...
├── completed_at = ...
└── status = DELIVERED
```

---

## 11.55 Context becomes evidence

Parte del contexto inicial puede terminar registrada en la traza.

Sin embargo:

```text
Context ≠ Trace
```

La traza incorpora hechos ocurridos.

---

## 11.56 DeliveryContext y Policy

La política puede depender de contexto.

Ejemplo:

```text
environment = testing
      ↓
adapter = IN_MEMORY
```

si está configurado formalmente.

No deberá implementarse con condiciones dispersas.

---

## 11.57 Policy resolution

Conceptualmente:

```text
DeliveryContext
      +
ConsumerProfile
      +
DeliveryPolicy
      ↓
Resolved Delivery Configuration
```

---

## 11.58 Resolved Delivery Configuration

Podrá incluir:

```text
adapter_id
serializer_id
timeout
contract_version
```

La configuración resuelta deberá ser trazable.

---

## 11.59 No hidden defaults

Si se utilizan defaults, deberán ser explícitos y documentados.

Ejemplo:

```text
default adapter = IN_MEMORY
```

en testing.

No deberá depender de "lo que esté registrado primero".

---

## 11.60 Context validation

DeliveryContext deberá validarse.

Ejemplos:

```text
delivery_id not empty
consumer_id known
session_id valid when required
response_id consistent
```

---

## 11.61 Context Validation Error

Un contexto inválido deberá producir:

```text
REJECTED
```

con un error como:

```text
DELIVERY_VALIDATION_ERROR
```

o subcódigo:

```text
INVALID_CONTEXT
```

---

## 11.62 Session lookup

Si Delivery necesita verificar una sesión, deberá utilizar una interfaz controlada.

Conceptualmente:

```text
SessionReader
```

o:

```text
SessionProvider
```

preferible a depender de una implementación concreta completa.

---

## 11.63 Read-only session dependency

Cuando sea posible, Delivery deberá tener acceso de lectura.

No de escritura.

Esto aplica el principio de mínimo privilegio.

---

## 11.64 SessionProvider conceptual

```text
SessionProvider
└── get_session_context(session_id)
```

La firma concreta deberá definirse solo si es necesaria.

---

## 11.65 Delivery no persiste sesión por defecto

Una entrega no deberá modificar:

```text
last_response
current_module
visual_state
```

dentro de SessionManager automáticamente.

Si posteriormente se requiere registrar actividad, deberá existir un contrato explícito.

---

## 11.66 Session activity event

Una alternativa futura podría ser emitir:

```text
DELIVERY_COMPLETED
```

y permitir que SessionManager actualice su estado mediante EventBus.

Esto preserva desacoplamiento.

---

## 11.67 Relación con EventBus

La arquitectura futura podrá utilizar EventBus para eventos como:

```text
delivery.started
delivery.completed
delivery.failed
```

SessionManager u otros componentes podrán observarlos.

Delivery no deberá conocer directamente a todos esos consumidores internos.

---

## 11.68 Event-driven context updates

Ejemplo:

```text
Delivery
   ↓
EventBus
   ↓
SessionManager
```

podría registrar actividad sin dependencia directa.

No es obligatorio para v1.0.

---

## 11.69 Context propagation y EventBus

Los eventos deberán conservar:

```text
delivery_id
response_id
session_id
```

cuando estén disponibles.

---

## 11.70 Concurrencia

DeliveryContext deberá ser seguro frente a múltiples operaciones concurrentes.

Dos entregas no deberán compartir contexto mutable.

---

## 11.71 Ejemplo concurrente

```text
DEL-001
session = SES-A
consumer = AT_PORTAL

DEL-002
session = SES-B
consumer = TEST_CLIENT
```

Los valores deberán permanecer aislados.

---

## 11.72 No global current_session

Queda prohibido depender arquitectónicamente de:

```text
global current_session
```

cuando múltiples operaciones puedan coexistir.

---

## 11.73 ContextVars

En Python podrían utilizarse mecanismos como `contextvars` para infraestructura interna si son apropiados.

Sin embargo, no deberán sustituir el contrato explícito de contexto.

---

## 11.74 Context object remains authoritative

Aunque existan herramientas de propagación automática:

```text
DeliveryContext
```

deberá continuar siendo la representación explícita y auditable.

---

## 11.75 Inmutabilidad

Una vez iniciada una operación, campos críticos deberán ser inmutables:

```text
delivery_id
response_id
session_id
consumer_id
correlation_id
```

cuando correspondan.

---

## 11.76 Mutation controlled

Campos operativos como:

```text
started_at
completed_at
status
```

podrán evolucionar mediante mecanismos controlados.

---

## 11.77 Context Builder

La implementación podrá contar con:

```text
DeliveryContextBuilder
```

si ayuda a combinar fuentes de manera segura.

Pero no deberá introducirse si una construcción directa es más clara.

---

## 11.78 Context factory conceptual

Podría existir:

```python
context = DeliveryContext.from_response(
    response=response,
    consumer_id="AT_PORTAL",
    session_id="SES-001",
)
```

Esta firma es ilustrativa.

No una decisión definitiva.

---

## 11.79 Context creation authority

La arquitectura deberá definir quién crea `DeliveryContext`.

Opciones:

```text
Gateway
Runtime orchestration
Delivery service
```

Para v1.0 podrá construirse en Delivery a partir de argumentos explícitos.

Lo importante es evitar ambigüedad.

---

## 11.80 Context and DeliveryRequest

Una opción coherente será:

```text
DeliveryRequest
├── response
├── target
├── context
└── policy
```

El contexto forma parte de la intención de entrega.

---

## 11.81 Session ownership

SessionManager continuará siendo autoridad sobre:

```text
session lifecycle
```

Delivery solamente preserva referencia y contexto.

---

## 11.82 Session expiration race

Puede ocurrir:

```text
session active at start
session expires during delivery
```

La política deberá definir si:

- se permite terminar;
- se cancela;
- se registra advertencia.

Para v1.0 deberá preferirse una regla simple y documentada.

---

## 11.83 Regla inicial sugerida

Para una entrega síncrona corta:

> **La validez de sesión se verifica al inicio de Delivery.**

Una expiración posterior no invalida retroactivamente una entrega ya completada.

---

## 11.84 Seguridad y expiración

Para operaciones sensibles futuras podrá requerirse verificación adicional.

No deberá sobreconstruirse v1.0.

---

## 11.85 Session closed

Una sesión cerrada antes de iniciar una entrega que la requiera deberá provocar:

```text
REJECTED
```

---

## 11.86 Delivery posterior al cierre

Una respuesta ya materializada podría ser entregada fuera de sesión si la política lo permite.

La existencia de un `response_id` no implica obligatoriamente una sesión activa.

---

## 11.87 Context and replay

Si una respuesta antigua se entrega nuevamente:

```text
RESP-001
```

la nueva operación tendrá:

```text
new delivery_id
```

y podrá conservar:

```text
original session_id
```

como trazabilidad histórica.

Pero el contexto de nueva operación también deberá distinguirse.

---

## 11.88 Original Context vs Current Delivery Context

En replay podría existir:

```text
response_origin.session_id = SES-001
```

y:

```text
delivery_context.session_id = SES-099
```

si una nueva sesión solicita volver a entregar una respuesta histórica.

Esta distinción deberá modelarse solo si aparece ese caso real.

---

## 11.89 No confundir procedencia y ejecución actual

La arquitectura deberá mantener capacidad para diferenciar:

```text
where response came from
```

de:

```text
where response is being delivered now
```

---

## 11.90 Consumer context and permissions

Un mismo consumidor podrá tener permisos diferentes según principal.

Ejemplo:

```text
principal A → allowed
principal B → denied
```

Por ello:

```text
consumer_id
```

no sustituye:

```text
principal_id
```

---

## 11.91 Context sanitization

Antes de serializar contexto público deberá aplicarse una proyección segura.

No todo el DeliveryContext deberá salir al consumidor.

---

## 11.92 Public Delivery Context

Ejemplo de campos potencialmente públicos:

```text
response_id
delivery_id
session_id
contract_version
```

si la política lo permite.

---

## 11.93 Internal Delivery Context

Ejemplo:

```text
principal_id
deployment
authorization flags
internal correlation metadata
```

podrá permanecer interno.

---

## 11.94 Public/Private boundary

La arquitectura deberá definir claramente:

```text
Internal Context
      ↓
Public Projection
      ↓
Delivery Envelope
```

---

## 11.95 No accidental context leakage

El serializer no deberá ejecutar automáticamente:

```text
context.__dict__
```

y exponer todo.

Solo los campos declarados deberán salir.

---

## 11.96 Context versioning

DeliveryContext interno no necesariamente requiere versión pública.

Si forma parte del contrato externo, su estructura deberá evolucionar bajo Delivery Contract.

---

## 11.97 SessionManager version independence

Delivery no deberá depender de una clase concreta de SessionManager de tal forma que cambios internos rompan el contrato.

Preferible:

```text
Session Context abstraction
```

---

## 11.98 Testabilidad

Delivery deberá poder probarse sin SessionManager real.

Ejemplo:

```text
FakeSessionProvider
```

podrá devolver:

```text
SessionContext
```

conocido.

---

## 11.99 Tests mínimos de sesión

```text
test_delivery_preserves_session_id
test_delivery_allows_missing_session_when_optional
test_delivery_rejects_missing_required_session
test_delivery_rejects_expired_required_session
```

---

## 11.100 Tests mínimos de contexto

```text
test_context_preserves_request_id
test_context_preserves_execution_id
test_context_preserves_response_id
test_context_preserves_consumer_id
test_context_is_not_mutated_during_delivery
```

---

## 11.101 Tests de aislamiento

```text
test_concurrent_delivery_contexts_do_not_leak
```

deberá comprobar que una operación no hereda valores de otra.

---

## 11.102 Tests de consumer context

```text
test_consumer_id_is_explicit
test_unknown_consumer_is_rejected
```

---

## 11.103 Tests de principal

Si se implementa seguridad:

```text
test_authorized_principal_can_deliver
test_unauthorized_principal_is_rejected
```

---

## 11.104 Tests de proyección pública

Deberá comprobarse que información interna sensible no aparece en payload.

---

## 11.105 Context observability

Los logs podrán incluir:

```text
session_id
request_id
execution_id
response_id
delivery_id
consumer_id
```

si la política de privacidad lo permite.

---

## 11.106 No log sensitive context

Deberá excluirse:

```text
tokens
passwords
raw authorization headers
```

---

## 11.107 Context auditability

La auditoría deberá poder reconstruir:

```text
which session?
which request?
which consumer?
which delivery?
```

cuando esos campos existan.

---

## 11.108 Session and DeliveryResult

El resultado podrá preservar:

```text
session_id
```

mediante su `trace`.

No necesariamente como campo raíz.

---

## 11.109 DeliveryResult no muta sesión

Completar Delivery no deberá modificar directamente el ciclo de vida de la sesión.

---

## 11.110 Session closure

El cierre de sesión deberá continuar siendo responsabilidad de SessionManager o del componente de orquestación autorizado.

---

## 11.111 Modelo conceptual consolidado

```text
┌──────────────────────────────┐
│ SessionManager               │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ SessionContext               │
└──────────────┬───────────────┘
               │
               │ projection
               ▼
┌──────────────────────────────┐
│ DeliveryContext              │
│                              │
│ session_id                   │
│ request_id                   │
│ execution_id                 │
│ response_id                  │
│ delivery_id                  │
│ consumer_id                  │
│ correlation_id               │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DeliveryRequest              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Response Delivery Pipeline   │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DeliveryTrace / Result       │
└──────────────────────────────┘
```

---

## 11.112 Flujo de sesión válido

```text
Session = ACTIVE
      ↓
SessionContext loaded
      ↓
DeliveryContext constructed
      ↓
Context validation
      ↓
VALID
      ↓
Delivery
```

---

## 11.113 Flujo de sesión inválida

```text
Session = EXPIRED
      ↓
Context validation
      ↓
INVALID
      ↓
DeliveryError
      ↓
REJECTED
```

El adaptador no deberá ejecutarse.

---

## 11.114 Flujo sin sesión

```text
DeliveryPolicy
session_required = false
      ↓
session_id = null
      ↓
Context validation
      ↓
VALID
      ↓
Delivery
```

---

## 11.115 Invariantes de Session y Context

Se establecen los siguientes invariantes.

### HRRD-SC01 — Explicit Context

Toda información operacional necesaria deberá ser explícita.

### HRRD-SC02 — Session Ownership

SessionManager conserva autoridad sobre el ciclo de vida de la sesión.

### HRRD-SC03 — No Session Mutation

Delivery no modificará arbitrariamente estado interno de sesión.

### HRRD-SC04 — No Hidden Global Session

Delivery no dependerá de una sesión global implícita.

### HRRD-SC05 — Context Isolation

Cada operación tendrá contexto independiente.

### HRRD-SC06 — Preserve Previous IDs

Delivery conservará los identificadores recibidos de capas anteriores.

### HRRD-SC07 — No ID Invention

No se inventarán identificadores previos ausentes.

### HRRD-SC08 — Conditional Session Requirement

La obligatoriedad de sesión dependerá de contrato o política.

### HRRD-SC09 — Minimal Context

Delivery transportará únicamente contexto necesario.

### HRRD-SC10 — Public Context Projection

Solo campos explícitamente autorizados podrán exponerse al consumidor.

---

## 11.116 Prueba de conformidad

Una implementación deberá poder demostrar:

1. que Delivery funciona con contexto explícito;
2. que no requiere variables globales de sesión;
3. que conserva `session_id` cuando existe;
4. que soporta operaciones sin sesión cuando estén permitidas;
5. que rechaza sesiones inválidas cuando sean obligatorias;
6. que no modifica SessionManager directamente sin contrato;
7. que contextos concurrentes permanecen aislados;
8. que información sensible no se filtra al payload;
9. que el consumidor está explícitamente identificado;
10. que la traza final conserva el contexto relevante.

---

## 11.117 Criterio de éxito

La relación entre Session Management y Delivery será considerada correcta cuando una operación pueda ejecutarse de forma totalmente determinista utilizando:

```text
MaterializedResponse
+
DeliveryContext
+
DeliveryPolicy
+
ConsumerProfile
```

sin depender de estado global oculto.

---

## 11.118 Declaración arquitectónica del capítulo

Session Management y Runtime Response Delivery deberán permanecer estrechamente correlacionados pero arquitectónicamente separados.

SessionManager mantiene la continuidad de interacción.

Delivery utiliza únicamente la porción de contexto necesaria para ejecutar una operación concreta.

La sesión no deberá convertirse en un contenedor universal de estado.

Delivery no deberá administrar sesiones.

Y ninguna operación deberá depender silenciosamente de una variable global que represente "la sesión actual".

La regla arquitectónica consolidada queda establecida como:

> **Toda entrega HEYTI deberá ejecutarse bajo un contexto operacional explícito, mínimo, validable e independiente, preservando las referencias de sesión y ejecución necesarias sin invadir las responsabilidades del SessionManager ni exponer estado interno innecesario.**

La relación fundamental queda formalizada como:

```text
SessionManager
      ↓
SessionContext
      ↓
DeliveryContext
      ↓
Runtime Response Delivery
      ↓
DeliveryTrace
```

Con esta base queda preparada la siguiente dimensión arquitectónica:

**Consumer Model, perfiles de consumidor y negociación de capacidades de entrega.**

---

**Fin del Capítulo 11**


# Capítulo 12. Consumer Model, perfiles de consumidor y negociación de capacidades de entrega

## 12.1 Propósito del capítulo

Este capítulo define el **Consumer Model** de HEYTI Runtime Response Delivery.

La finalidad es establecer cómo HEYTI deberá representar, identificar y validar a los consumidores capaces de recibir respuestas entregadas por el Runtime.

La arquitectura deberá permitir que un consumidor declare, de forma explícita y desacoplada:

- su identidad lógica;
- las versiones de contrato que soporta;
- los tipos de contenido que puede interpretar;
- las modalidades de entrega compatibles;
- y las capacidades necesarias para recibir correctamente una respuesta.

El objetivo es evitar que Delivery dependa de condiciones específicas como:

```text
if consumer == portal.html
```

o:

```text
if consumer uses Leaflet
```

y sustituirlas por un modelo formal de capacidades.

La regla fundamental será:

> **HEYTI no deberá conocer cómo está construido un consumidor; deberá conocer únicamente qué contratos y capacidades declara soportar.**

---

## 12.2 Definición de Consumer

Se define **Consumer** como cualquier componente autorizado capaz de recibir una respuesta de HEYTI Runtime Response Delivery.

Ejemplos conceptuales:

```text
AT Portal
HEYTI UI
Internal Service
Testing Harness
API Client
Future Integration
```

El consumidor constituye una frontera lógica.

No una tecnología específica.

---

## 12.3 Consumer no es Presentation

Debe mantenerse:

```text
Consumer
    ≠
Presentation
```

Un Consumer recibe una respuesta.

Presentation decide cómo representarla.

Conceptualmente:

```text
Delivery
   ↓
Consumer
   ↓
Presentation
```

En algunos sistemas ambos podrán formar parte de la misma aplicación.

Arquitectónicamente deberán continuar diferenciados.

---

## 12.4 Consumer no es Transport

También deberá distinguirse:

```text
Consumer
    ≠
Transport
```

Ejemplo:

```text
consumer_id = AT_PORTAL
```

podría utilizar:

```text
HTTP_JSON
```

como adaptador.

Posteriormente podría utilizar:

```text
WEBSOCKET_JSON
```

sin dejar de ser el mismo consumidor lógico.

---

## 12.5 Consumer Identity

Cada consumidor deberá poder identificarse mediante:

```text
consumer_id
```

Ejemplos:

```text
AT_PORTAL
HEYTI_UI
INTERNAL_TEST_CLIENT
```

La identidad deberá ser:

- estable;
- lógica;
- independiente de archivos concretos;
- independiente de rutas;
- independiente de implementación visual.

---

## 12.6 Identidades de consumidor no recomendadas

Deberán evitarse identificadores como:

```text
portal.html
index.html
192.168.1.20
localhost:8000
#heyti-panel
```

porque representan detalles técnicos o de implementación.

---

## 12.7 ConsumerProfile

Se define conceptualmente:

```text
ConsumerProfile
```

como la estructura que describe las capacidades declaradas por un consumidor.

Podrá contener:

```text
consumer_id
profile_version
supported_delivery_contracts
supported_response_contracts
supported_content_types
supported_encodings
supported_delivery_modes
required_features
optional_features
```

No todos los campos deberán implementarse desde v1.0.

---

## 12.8 Propósito del ConsumerProfile

ConsumerProfile permitirá responder:

> ¿Puede este consumidor interpretar correctamente esta entrega?

No deberá responder:

> ¿Cómo quiere verse la interfaz?

---

## 12.9 Ejemplo conceptual

```text
ConsumerProfile
consumer_id = AT_PORTAL

supports:
- Delivery Contract 1.0
- Response Contract 1.0
- text
- metric
- table
- series
- territorial_reference
- action
```

Esto permite a Delivery verificar compatibilidad antes de cruzar la frontera.

---

## 12.10 profile_version

El perfil podrá tener:

```text
profile_version
```

cuando evolucione.

Ejemplo:

```text
AT_PORTAL profile 1.0
```

Posteriormente:

```text
AT_PORTAL profile 1.1
```

La versión del perfil no deberá confundirse con la versión de Delivery Contract.

---

## 12.11 Versiones independientes

Podrán coexistir:

```text
consumer_profile_version = 1.2
delivery_contract_version = 1.0
response_contract_version = 1.1
```

Cada versión representa una responsabilidad diferente.

---

## 12.12 Supported Delivery Contracts

ConsumerProfile deberá poder declarar las versiones de Delivery Contract que soporta.

Ejemplo:

```text
supported_delivery_contracts = [
    "1.0"
]
```

Posteriormente:

```text
[
    "1.0",
    "1.1"
]
```

---

## 12.13 Supported Response Contracts

Cuando sea necesario, el consumidor también podrá declarar qué versiones del Response Contract interpreta.

Ejemplo:

```text
supported_response_contracts = [
    "1.0"
]
```

Esto será útil si Delivery encapsula respuestas de diferentes versiones.

---

## 12.14 Supported Content Types

ConsumerProfile deberá poder declarar tipos semánticos de contenido.

Ejemplos:

```text
text
metric
table
series
territorial_reference
geometry
evidence
warning
action
```

La lista deberá representar capacidades semánticas.

No componentes visuales concretos.

---

## 12.15 Ejemplo correcto

```text
supports:
- series
```

Esto indica que el consumidor puede interpretar una serie de datos.

---

## 12.16 Ejemplo incorrecto

```text
supports:
- Chart.js line chart
```

Esto introduce tecnología de presentación.

---

## 12.17 Map Capability

El consumidor podrá declarar:

```text
supports:
- territorial_reference
- geometry
```

Esto permite trabajar con información cartográfica.

No significa que HEYTI conozca si utiliza:

```text
Leaflet
Mapbox
OpenLayers
```

---

## 12.18 Chart Capability

Podrá declarar:

```text
supports:
- series
```

sin indicar biblioteca gráfica.

---

## 12.19 Table Capability

Podrá declarar:

```text
supports:
- table
```

La UI decidirá cómo renderizar la tabla.

---

## 12.20 Action Capability

Podrá declarar:

```text
supports:
- action
```

Esto significa que el consumidor puede interpretar acciones semánticas.

No significa que ejecute cualquier acción sin validación.

---

## 12.21 Evidence Capability

Un consumidor podrá soportar:

```text
evidence
```

para mostrar o utilizar procedencia.

Otro consumidor podría no mostrarla visualmente.

Sin embargo, si evidencia es obligatoria por contrato, Delivery no deberá eliminarla silenciosamente.

---

## 12.22 Warnings Capability

Las advertencias deberán tratarse como contenido contractual importante.

Un consumidor que no pueda interpretar advertencias requeridas podrá considerarse incompatible.

---

## 12.23 Required Feature

El ConsumerProfile podrá distinguir:

```text
required capabilities
```

de:

```text
optional capabilities
```

Ejemplo:

```text
required:
- text

optional:
- series
- territorial_reference
```

---

## 12.24 Consumer requirements vs Response requirements

Debe distinguirse:

```text
Consumer Supports
```

de:

```text
Response Requires
```

La compatibilidad será una relación entre ambos.

---

## 12.25 Response Capability Manifest

La respuesta o Delivery Envelope podrá exponer conceptualmente qué tipos de contenido contiene.

Ejemplo:

```text
content_types = [
  text,
  metric,
  territorial_reference
]
```

Delivery podrá comparar esta información con ConsumerProfile.

---

## 12.26 Capability Negotiation

Se define **Capability Negotiation** como el proceso mediante el cual Delivery determina si una respuesta puede entregarse correctamente a un consumidor.

Conceptualmente:

```text
Response Requirements
      +
Consumer Capabilities
      +
Contract Versions
      +
Delivery Policy
      ↓
Compatibility Decision
```

---

## 12.27 Negotiation no es regateo dinámico necesariamente

El término negociación no implica obligatoriamente una conversación de red.

En v1.0 podrá ser simplemente:

```text
validate compatibility
```

usando perfiles previamente registrados.

---

## 12.28 Resultado de negociación

El resultado podrá ser:

```text
COMPATIBLE
INCOMPATIBLE
COMPATIBLE_WITH_PROJECTION
```

si en el futuro se implementan proyecciones contractuales.

Para v1.0 podrá bastar:

```text
VALID
INVALID
```

---

## 12.29 Compatibility Decision

Conceptualmente:

```text
CompatibilityResult
├── compatible
├── required_contract
├── consumer_contract
├── unsupported_content_types
├── warnings
└── reason
```

La implementación deberá mantenerse simple inicialmente.

---

## 12.30 Negociación de versión

Ejemplo:

```text
Response Delivery Contract:
1.0

Consumer supports:
1.0, 1.1
```

Resultado:

```text
COMPATIBLE
```

---

## 12.31 Versión incompatible

```text
Required:
2.0

Consumer:
1.0
```

Resultado:

```text
INCOMPATIBLE
```

y:

```text
DELIVERY_CONTRACT_MISMATCH
```

---

## 12.32 Selección de versión

Si varias versiones son compatibles, la arquitectura deberá definir una regla.

Ejemplo:

```text
prefer highest mutually supported stable version
```

o:

```text
use response-defined delivery version
```

Para v1.0 deberá preferirse una regla simple.

---

## 12.33 Regla v1.0 sugerida

En v1.0:

> **La versión de Delivery Contract será determinada por el Runtime y el consumidor deberá declararla como soportada.**

No se realizará negociación dinámica de versión.

Esto reduce complejidad.

---

## 12.34 Evolución futura

Posteriormente podría implementarse:

```text
producer supports [1.0, 1.1]
consumer supports [1.0]
      ↓
choose 1.0
```

si existe necesidad real.

---

## 12.35 Supported Encoding

ConsumerProfile podrá declarar:

```text
JSON
```

como formato soportado.

En v1.0 podría existir un único encoding.

No es necesario sobre-modelar esta capacidad inicialmente.

---

## 12.36 Supported Delivery Mode

Podrá declararse:

```text
SYNC
ASYNC
STREAMING
```

cuando existan esos modos.

Para v1.0 probablemente:

```text
SYNC
```

será suficiente.

---

## 12.37 Delivery Mode no es Adapter

Debe distinguirse:

```text
delivery_mode = SYNC
```

de:

```text
adapter_id = HTTP_JSON
```

Son conceptos distintos.

---

## 12.38 ConsumerRegistry

La arquitectura podrá utilizar un registro formal:

```text
ConsumerRegistry
```

responsable de conocer consumidores disponibles.

Conceptualmente:

```text
ConsumerRegistry
├── AT_PORTAL
├── HEYTI_UI
└── TEST_CLIENT
```

---

## 12.39 ConsumerRegistry no es CapabilityRegistry

Debe preservarse:

```text
ConsumerRegistry
       ≠
CapabilityRegistry
```

El Capability Registry sabe:

> Qué puede ejecutar HEYTI.

El Consumer Registry sabe:

> Quién puede recibir respuestas y bajo qué perfil.

---

## 12.40 ConsumerRegistry no es AdapterRegistry

También:

```text
ConsumerRegistry
       ≠
DeliveryAdapterRegistry
```

Consumer Registry conoce destinos lógicos.

Adapter Registry conoce mecanismos técnicos.

---

## 12.41 Relación entre registries

Conceptualmente:

```text
ConsumerRegistry
      │
      ▼
ConsumerProfile
      │
      ▼
Adapter Mapping
      │
      ▼
DeliveryAdapterRegistry
      │
      ▼
Adapter
```

---

## 12.42 ConsumerProfile Resolution

El pipeline podrá ejecutar:

```text
consumer_id
    ↓
ConsumerRegistry
    ↓
ConsumerProfile
```

Si no existe:

```text
REJECTED
```

---

## 12.43 Consumer not found

Resultado conceptual:

```text
DELIVERY_UNSUPPORTED_CONSUMER
```

El adaptador no deberá ejecutarse.

---

## 12.44 Consumer enabled

El perfil podrá incluir:

```text
enabled = true | false
```

si existe necesidad operativa.

Un consumidor deshabilitado deberá rechazarse.

---

## 12.45 Consumer status

Podrían existir estados:

```text
ACTIVE
DISABLED
DEPRECATED
```

No es necesario implementarlos todos desde v1.0.

---

## 12.46 Consumer deprecado

Un consumidor deprecado podría continuar funcionando mientras emite advertencias.

La política deberá definirse si ese escenario aparece.

---

## 12.47 Mapping Consumer → Adapter

Un consumidor podrá estar asociado con uno o más adaptadores autorizados.

Ejemplo:

```text
AT_PORTAL
├── HTTP_JSON
└── WEBSOCKET_JSON
```

La selección dependerá de DeliveryPolicy.

---

## 12.48 Default Adapter

ConsumerProfile podrá definir un adaptador predeterminado si resulta útil.

Ejemplo:

```text
default_adapter = HTTP_JSON
```

Pero deberá ser una decisión explícita.

---

## 12.49 Testing Consumer

Para v1.0 deberá existir conceptualmente un consumidor de prueba:

```text
TEST_CLIENT
```

asociado con:

```text
IN_MEMORY
```

Esto permitirá validar Delivery sin Portal.

---

## 12.50 AT_PORTAL como consumidor inicial

Dentro de AT 27–30, el Portal podrá modelarse conceptualmente como:

```text
consumer_id = AT_PORTAL
```

Su perfil inicial podría soportar:

```text
text
metric
table
series
territorial_reference
action
warning
evidence_reference
```

La lista definitiva deberá derivarse de los casos reales de interfaz.

---

## 12.51 Portal no entra al Core

Aunque `AT_PORTAL` exista como identidad lógica, HEYTI-CORE no deberá importar:

```text
portal.html
```

ni JavaScript del Portal.

El perfil será una abstracción.

---

## 12.52 Futuro HEYTI_UI

Una futura interfaz dedicada podrá registrarse como:

```text
consumer_id = HEYTI_UI
```

sin modificar capabilities.

---

## 12.53 Módulos AT como consumidores especializados

Los módulos podrán evolucionar como consumidores o subconsumidores especializados.

Ejemplos conceptuales:

```text
AT_TERRITORIAL
AT_GANAR_TODO
AT_CAMPO
AT_DIA_D
AT_ET27
AT_SOCIOECONOMICO
```

La decisión de modelarlos como consumidores independientes o superficies de un mismo consumidor deberá tomarse cuando se implemente la UI integrada.

---

## 12.54 No decidir demasiado pronto

En este Sprint deberá evitarse fijar prematuramente:

```text
one consumer per HTML page
```

El Consumer Model deberá permanecer lógico.

---

## 12.55 Consumer hierarchy

En el futuro podría existir:

```text
AT_PORTAL
├── TERRITORIAL_SURFACE
├── FIELD_SURFACE
└── ELECTION_DAY_SURFACE
```

Pero solo deberá incorporarse si mejora realmente la integración.

---

## 12.56 Consumer capability inheritance

No deberá introducirse herencia compleja de perfiles hasta que sea necesaria.

La composición de capacidades será preferible inicialmente.

---

## 12.57 ConsumerProfile como dato

El perfil deberá ser tratable como configuración estructurada.

Ejemplo conceptual:

```json
{
  "consumer_id": "AT_PORTAL",
  "profile_version": "1.0",
  "supported_delivery_contracts": ["1.0"],
  "supported_content_types": [
    "text",
    "metric",
    "table",
    "series",
    "territorial_reference"
  ]
}
```

---

## 12.58 Ubicación de perfiles

Los perfiles podrán declararse:

- en código;
- configuración;
- registro;
- archivos controlados.

La elección deberá favorecer:

- claridad;
- versionado;
- pruebas;
- no dependencia de servicios externos.

---

## 12.59 v1.0 perfiles en código

Para la implementación inicial puede ser razonable registrar perfiles directamente en Python.

Esto evita infraestructura prematura.

La arquitectura deberá permitir migrarlos posteriormente a configuración.

---

## 12.60 Immutability de ConsumerProfile

Los perfiles cargados durante una operación deberán tratarse como snapshots inmutables.

Una modificación global no deberá alterar una entrega ya iniciada.

---

## 12.61 Profile Snapshot

DeliveryTrace podrá conservar:

```text
consumer_profile_version
```

para saber qué perfil se utilizó.

---

## 12.62 Contract Negotiation vs Content Negotiation

Debe distinguirse:

```text
Contract Negotiation
```

de:

```text
HTTP Content Negotiation
```

No son lo mismo.

El primero es semántico.

El segundo es protocolo.

---

## 12.63 No depender de HTTP Accept

Un futuro header:

```text
Accept: application/json
```

no determina por sí solo compatibilidad del Delivery Contract.

---

## 12.64 Consumer capability check

La validación deberá poder comprobar:

```text
required_types ⊆ supported_types
```

Ejemplo:

```text
required = {text, metric}
supported = {text, metric, series}
```

Resultado:

```text
COMPATIBLE
```

---

## 12.65 Incompatibility by type

```text
required = {text, geometry}
supported = {text, metric}
```

Resultado:

```text
INCOMPATIBLE
```

si geometry es obligatorio.

---

## 12.66 Optional Type

Si:

```text
geometry = optional
```

podrá existir una proyección autorizada sin geometry.

Pero esa política deberá estar definida por contrato.

---

## 12.67 ConsumerProjection

Conceptualmente, una proyección podrá adaptar:

```text
Full Delivery Contract
       ↓
Consumer Projection
       ↓
Compatible Contract
```

sin alterar significado obligatorio.

---

## 12.68 Proyección no es mutilación

Una proyección deberá definir explícitamente:

- campos conservados;
- campos opcionales omitibles;
- versión resultante.

No deberá ser una eliminación arbitraria.

---

## 12.69 Projection Registry futuro

Si aparecen varias proyecciones podrá existir:

```text
ProjectionRegistry
```

No es necesario en v1.0.

---

## 12.70 Preferencia v1.0

Para la primera versión deberá preferirse:

```text
consumer supports full contract
```

en lugar de implementar proyecciones complejas.

Esto protege la disciplina de cero omisiones.

---

## 12.71 Consumer Actions

El perfil podrá declarar qué acciones semánticas reconoce.

Ejemplo:

```text
supported_actions:
- OPEN_MODULE
- SHOW_SECTION
```

Esto podría utilizarse en una futura UI.

---

## 12.72 Acción no soportada

Si una acción es obligatoria para la respuesta y el consumidor no la soporta:

```text
INCOMPATIBLE
```

---

## 12.73 Acción opcional

Si es opcional, una proyección contractual futura podría omitirla.

---

## 12.74 Consumer security classification

ConsumerProfile podría incluir:

```text
trust_level
```

o:

```text
security_class
```

si se requiere.

No deberá añadirse sin un modelo de seguridad formal.

---

## 12.75 Consumer authorization

La existencia en ConsumerRegistry no significa automáticamente:

```text
authorized
```

Un consumidor puede ser conocido pero una operación concreta no estar autorizada.

---

## 12.76 Identity vs Authorization

Debe mantenerse:

```text
known consumer
≠
authorized delivery
```

---

## 12.77 Consumer-specific policies

Podrán existir políticas como:

```text
timeout
max_payload_size
allowed_content_types
```

por consumidor.

Estas políticas deberán permanecer separadas del perfil semántico cuando sea conveniente.

---

## 12.78 Profile vs Policy

ConsumerProfile responde:

> ¿Qué puede interpretar el consumidor?

DeliveryPolicy responde:

> ¿Cómo debe ejecutarse la entrega?

La distinción deberá preservarse.

---

## 12.79 Consumer-specific serializer

Un consumidor podría necesitar un serializer específico en el futuro.

Sin embargo, deberá preferirse compartir representación contractual.

Un serializer particular solo deberá introducirse cuando exista necesidad real.

---

## 12.80 Consumer-specific presentation

Una UI puede adaptar:

```text
series
```

a Chart.js.

Otra puede convertirla a:

```text
ASCII chart
```

HEYTI Delivery no deberá distinguir ambas visualizaciones.

---

## 12.81 ConsumerProfile y mapas

Ejemplo:

```text
AT_PORTAL supports territorial_reference
```

El Portal podrá resolver:

```text
section_id
```

contra su mapa local.

Esto puede ser preferible a enviar geometría completa.

---

## 12.82 ConsumerProfile y geometría

Otro consumidor podría requerir:

```text
geometry
```

porque no posee datos territoriales locales.

El perfil permite distinguir ambos casos.

---

## 12.83 ConsumerProfile y evidencias

Podrá declarar:

```text
evidence_reference
```

sin requerir evidencia completa.

Esto puede reducir payload.

Sin embargo, deberá respetarse Response Contract.

---

## 12.84 ConsumerProfile y datos históricos

Un consumidor que soporte:

```text
series
table
```

podrá recibir históricos electorales.

No deberá conocer internamente cómo fueron calculados.

---

## 12.85 ConsumerProfile y KPIs

Un KPI es semánticamente un:

```text
metric
```

No será necesario declarar:

```text
kpi_card
```

como capability central.

---

## 12.86 ConsumerProfile y narrative

Podrá soportar:

```text
text
```

o un tipo más específico:

```text
narrative
```

si el modelo de respuesta lo requiere.

La taxonomía deberá mantenerse pequeña y útil.

---

## 12.87 Avoid capability explosion

Queda desaconsejado crear tipos como:

```text
blue_metric
map_popup
small_table
horizontal_chart
```

porque son Presentation.

---

## 12.88 Consumer Capability Catalog

La arquitectura deberá mantener un catálogo limitado de capacidades semánticas.

Propuesta inicial:

```text
TEXT
METRIC
TABLE
SERIES
TERRITORIAL_REFERENCE
GEOMETRY
EVIDENCE
WARNING
ACTION
```

Este catálogo deberá alinearse con Materialization.

---

## 12.89 Capabilities públicas y evolución

Agregar un nuevo Content Type deberá considerarse una evolución contractual.

No deberá aparecer de manera informal.

---

## 12.90 Unknown Content Type

Si el consumidor recibe un tipo obligatorio desconocido:

```text
INCOMPATIBLE
```

---

## 12.91 Optional Unknown Content Type

Un consumidor podrá ignorar tipos opcionales desconocidos únicamente si la política de compatibilidad lo permite.

---

## 12.92 Consumer registry lifecycle

El registro deberá permitir conceptualmente:

```text
register
resolve
list
validate uniqueness
```

No necesariamente deberá permitir mutación dinámica en producción desde v1.0.

---

## 12.93 Duplicate consumer_id

Dos perfiles con el mismo:

```text
consumer_id
```

deberán provocar error de configuración.

---

## 12.94 Duplicate profile version

También deberá impedirse:

```text
AT_PORTAL v1.0
AT_PORTAL v1.0
```

con definiciones diferentes.

---

## 12.95 Consumer profile validation

El propio perfil deberá validarse.

Ejemplos:

```text
consumer_id non-empty
profile_version valid
supported_contracts non-empty
content types known
```

---

## 12.96 Invalid ConsumerProfile

Un perfil inválido no deberá registrarse.

Esto debe detectarse durante bootstrap o configuración.

---

## 12.97 Registry bootstrap

Los consumidores v1.0 podrán registrarse durante:

```text
Runtime bootstrap
```

de manera similar a otros registros, manteniendo responsabilidades separadas.

---

## 12.98 Registry read-only after bootstrap

Para simplificar v1.0 podría utilizarse:

```text
register at startup
read-only at runtime
```

Esto reduce estados inesperados.

---

## 12.99 Consumer profile not found at runtime

Si un `consumer_id` solicitado no existe:

```text
REJECTED
```

con error explícito.

---

## 12.100 Compatibility service

Podrá existir conceptualmente:

```text
ConsumerCompatibilityValidator
```

o:

```text
ConsumerNegotiator
```

responsable de comparar respuesta y perfil.

---

## 12.101 Simplicidad v1.0

Para v1.0 un único validator puede ser suficiente.

No deberán crearse múltiples servicios si una implementación simple cumple la arquitectura.

---

## 12.102 Algoritmo conceptual de compatibilidad

```text
1. Resolve ConsumerProfile
2. Validate Delivery Contract version
3. Validate Response Contract version
4. Extract required content types
5. Compare against supported content types
6. Validate required delivery mode
7. Validate adapter compatibility
8. Return CompatibilityResult
```

---

## 12.103 Flujo compatible

```text
DeliveryRequest
      ↓
consumer_id
      ↓
ConsumerRegistry
      ↓
ConsumerProfile
      ↓
Compatibility Validation
      ↓
COMPATIBLE
      ↓
Continue Pipeline
```

---

## 12.104 Flujo incompatible

```text
DeliveryRequest
      ↓
ConsumerProfile
      ↓
Compatibility Validation
      ↓
INCOMPATIBLE
      ↓
DeliveryError
      ↓
REJECTED
```

El serializer y adapter no deberán ejecutarse.

---

## 12.105 Consumer selection

La selección del consumidor deberá ser explícita.

Delivery no deberá decidir por sí solo:

```text
"this looks territorial, send it to Análisis Territorial"
```

Eso sería orquestación o Presentation logic.

---

## 12.106 Selector externo

Un componente de orquestación podrá decidir:

```text
consumer_id = AT_PORTAL
```

y pasar la decisión a Delivery.

---

## 12.107 Consumer default

Si existe un consumidor predeterminado:

```text
AT_PORTAL
```

deberá estar definido por configuración o política.

No hardcoded de manera accidental.

---

## 12.108 Consumer and Gateway

Gateway podrá identificar al consumidor que realizó una solicitud.

Ejemplo:

```text
Gateway
  ↓
consumer_id
  ↓
DeliveryContext
```

Delivery no deberá depender de HTTP headers específicos directamente.

---

## 12.109 Consumer and authentication

Un consumidor podrá autenticarse mediante Gateway.

Delivery recibirá identidad lógica ya resuelta o un contexto verificable.

---

## 12.110 Consumer and session

Un consumidor podrá asociarse a una sesión.

Ejemplo:

```text
session_id = SES-001
consumer_id = HEYTI_UI
```

Ambas identidades deberán permanecer separadas.

---

## 12.111 Consumer and trace

DeliveryTrace deberá conservar:

```text
consumer_id
```

y opcionalmente:

```text
consumer_profile_version
```

---

## 12.112 Consumer substitution test

El Consumer Model deberá superar:

> Si `AT_PORTAL` se sustituye por `HEYTI_UI`, ¿deben modificarse capabilities?

Respuesta requerida:

```text
NO
```

---

## 12.113 Consumer substitution and adapters

El cambio podrá requerir:

```text
new ConsumerProfile
new Adapter
```

pero no modificar:

```text
HKS
HES
Capability
Materialization semantics
```

---

## 12.114 Transport substitution test

Si el mismo consumidor cambia:

```text
HTTP_JSON
```

por:

```text
WEBSOCKET_JSON
```

su identidad lógica deberá permanecer:

```text
AT_PORTAL
```

---

## 12.115 Profile version trace

Una entrega deberá poder registrar qué perfil se utilizó.

Esto ayudará a diagnosticar incompatibilidades históricas.

---

## 12.116 Consumer profile auditability

Deberá poder responderse:

```text
Which consumer profile accepted this response?
```

---

## 12.117 Testing ConsumerRegistry

Deberán existir pruebas como:

```text
test_register_consumer_profile
test_reject_duplicate_consumer_id
test_resolve_known_consumer
test_unknown_consumer_returns_none_or_error
```

---

## 12.118 Testing ConsumerProfile

```text
test_profile_requires_consumer_id
test_profile_rejects_unknown_content_type
test_profile_requires_supported_contract
```

---

## 12.119 Testing Compatibility

```text
test_compatible_consumer_passes
test_contract_mismatch_rejects
test_missing_required_content_type_rejects
test_optional_content_type_does_not_reject_when_policy_allows
```

---

## 12.120 Testing Consumer Independence

Una prueba deberá confirmar que Delivery puede utilizar:

```text
TEST_CLIENT
```

y:

```text
AT_PORTAL
```

sin modificar la respuesta.

---

## 12.121 Testing Presentation Neutrality

Los perfiles no deberán contener:

```text
css_class
chart_color
leaflet_options
dom_id
```

---

## 12.122 ConsumerProfile serialization

Si el perfil se expone para debugging o administración, podrá serializarse.

No es necesario incluirlo en cada DeliveryEnvelope completo.

---

## 12.123 Consumer profile exposure

El consumidor no necesita recibir necesariamente su propio perfil.

Delivery solo necesita utilizarlo para validación.

---

## 12.124 ConsumerProfile caching

Los perfiles podrán mantenerse en memoria después de bootstrap.

Dado que son pequeños y relativamente estáticos, esto será suficiente inicialmente.

---

## 12.125 Dynamic profile discovery

Descubrir capacidades dinámicamente mediante red podría ser útil en el futuro.

No deberá implementarse en v1.0 sin necesidad.

---

## 12.126 Consumer handshake futuro

Una arquitectura futura podría permitir:

```text
Consumer
   ↓
HELLO
   ↓
supported contracts/capabilities
   ↓
HEYTI
```

pero este handshake no es requisito inicial.

---

## 12.127 Static negotiation first

v1.0 deberá favorecer:

```text
registered profile
+
local compatibility validation
```

Esto es más determinista y auditable.

---

## 12.128 Consumer Profile and Security

El perfil deberá ser configuración confiable.

No deberá aceptarse ciegamente un perfil arbitrario enviado por un consumidor externo para ampliar sus propios permisos.

---

## 12.129 Declared capability does not grant authorization

Aunque un consumidor declare:

```text
supports geometry
```

eso no significa que tenga autorización para recibir cualquier geometría.

Capability y autorización son dimensiones distintas.

---

## 12.130 Consumer capability vs data authorization

Debe preservarse:

```text
Can interpret data
      ≠
May receive data
```

---

## 12.131 Security validation flow

Conceptualmente:

```text
Consumer known?
      ↓
Consumer compatible?
      ↓
Consumer authorized?
      ↓
Deliver
```

El orden podrá variar por eficiencia, pero las tres dimensiones deberán existir cuando sean necesarias.

---

## 12.132 ConsumerModel y mínimo privilegio

Delivery deberá enviar únicamente la información permitida por el contrato y autorización.

No deberá utilizar ConsumerProfile para justificar exposición adicional.

---

## 12.133 ConsumerProfile y filtros de datos

Los filtros de datos no deberán ser decisión de ConsumerProfile salvo que exista un contrato formal de proyección.

No deberá contener reglas de negocio como:

```text
AT_PORTAL only sees municipalities 1-20
```

sin una política de autorización separada.

---

## 12.134 ConsumerModel y observabilidad

Podrán medirse:

```text
delivery_total by consumer
delivery_failure_total by consumer
compatibility_failure_total by consumer
```

---

## 12.135 ConsumerModel y alertas

Una tasa alta de incompatibilidad para:

```text
AT_PORTAL
```

podría indicar que la UI quedó desactualizada respecto al contrato.

---

## 12.136 ConsumerModel y evolución coordinada

Cuando se publique una nueva versión contractual deberá revisarse:

```text
producer support
consumer support
adapter support
serializer support
```

antes de activarla.

---

## 12.137 Consumer compatibility matrix

Podrá mantenerse conceptualmente una matriz:

| Consumer | Profile | Delivery Contract | Response Contract | Content Types |
|---|---|---|---|---|
| AT_PORTAL | 1.0 | 1.0 | 1.0 | TEXT, METRIC, TABLE, SERIES, TERRITORIAL_REFERENCE |
| TEST_CLIENT | 1.0 | 1.0 | 1.0 | ALL V1 |
| HEYTI_UI | Future | Future | Future | Future |

Esta matriz será útil para gobernanza.

---

## 12.138 AT Portal como transición

El Portal existente deberá considerarse un consumidor de transición hacia una experiencia HEYTI más integrada.

El Consumer Model deberá permitir esa evolución sin reemplazar el Core.

---

## 12.139 UI future-proofing

Cuando la interfaz futura incorpore:

- conversación;
- mapas;
- estadísticas;
- gráficas;
- navegación por módulos;

la ampliación deberá reflejarse en:

```text
ConsumerProfile
```

y adaptadores de Presentation.

No en capacidades cognitivas de Delivery.

---

## 12.140 Capacidad visual vs capacidad semántica

Debe distinguirse:

```text
supports SERIES
```

de:

```text
supports BAR_CHART
```

El primero pertenece al contrato.

El segundo puede pertenecer a Presentation.

---

## 12.141 Semántica territorial y módulo visual

Debe distinguirse:

```text
territorial_reference = section 1481
```

de:

```text
open analisis_territorial.html and zoom to polygon
```

El primero es contenido.

El segundo es workflow visual.

---

## 12.142 Action contract bridge

Una acción semántica podrá actuar como puente:

```text
OPEN_TERRITORIAL_CONTEXT
section_id = 1481
```

El Consumer sabrá cómo implementarla.

---

## 12.143 No hardcoded module file

Delivery no deberá producir:

```text
url = "analisis_territorial.html"
```

como semántica central.

Podrá producir:

```text
module = TERRITORIAL
```

si existe un catálogo formal.

---

## 12.144 Consumer adapter de Presentation

Fuera del Core podrá existir:

```text
HEYTI UI Adapter
```

que convierta:

```text
module = TERRITORIAL
```

a:

```text
analisis_territorial.html
```

o una futura ruta React/Vue/etc.

Así HEYTI permanece desacoplado.

---

## 12.145 Invariantes del Consumer Model

Se establecen los siguientes invariantes.

### HRRD-CO01 — Logical Consumer Identity

Todo consumidor deberá poseer identidad lógica estable.

### HRRD-CO02 — Consumer Is Not Transport

La identidad del consumidor será independiente del adaptador técnico.

### HRRD-CO03 — Consumer Is Not Presentation

Las capacidades deberán expresarse semánticamente, no visualmente.

### HRRD-CO04 — Explicit Capability Declaration

Las capacidades soportadas deberán estar declaradas.

### HRRD-CO05 — Version Compatibility

Las versiones contractuales deberán validarse antes de Delivery.

### HRRD-CO06 — No Silent Capability Degradation

Los tipos obligatorios no soportados no podrán eliminarse silenciosamente.

### HRRD-CO07 — Registry Separation

ConsumerRegistry permanecerá separado de CapabilityRegistry y AdapterRegistry.

### HRRD-CO08 — Consumer Substitutability

La sustitución de consumidor no deberá modificar la cognición de HEYTI.

### HRRD-CO09 — Authorization Separation

Capacidad de interpretación no equivale a autorización.

### HRRD-CO10 — Presentation Neutrality

Los perfiles no contendrán detalles específicos de HTML, CSS, DOM, Leaflet o Chart.js.

---

## 12.146 Perfil mínimo recomendado para v1.0

Conceptualmente:

```text
ConsumerProfile
├── consumer_id
├── profile_version
├── supported_delivery_contracts
├── supported_response_contracts
├── supported_content_types
└── enabled
```

Este núcleo será suficiente para comenzar.

---

## 12.147 ConsumerRegistry mínimo recomendado

Conceptualmente:

```text
register(profile)
get(consumer_id)
contains(consumer_id)
```

La primera versión no necesita descubrimiento dinámico.

---

## 12.148 Negotiation mínimo recomendado

Para v1.0:

```text
1. Resolve profile
2. Check enabled
3. Check delivery contract
4. Check response contract
5. Check required content types
6. Return compatible / incompatible
```

---

## 12.149 Flujo operacional consolidado

```text
DeliveryRequest
      │
      ▼
consumer_id
      │
      ▼
┌────────────────────────┐
│ ConsumerRegistry       │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ ConsumerProfile        │
└───────────┬────────────┘
            │
            ▼
┌────────────────────────┐
│ Compatibility Check    │
└───────────┬────────────┘
            │
      ┌─────┴─────┐
      │           │
 COMPATIBLE   INCOMPATIBLE
      │           │
      ▼           ▼
 Continue       REJECTED
 Pipeline
```

---

## 12.150 Relación con Adapter Resolution

Una vez validado el consumidor:

```text
ConsumerProfile
      ↓
DeliveryPolicy
      ↓
Adapter Resolver
```

podrá seleccionar un adaptador permitido.

Esto mantiene las responsabilidades separadas.

---

## 12.151 Relación con serialización

El ConsumerProfile podrá determinar qué versión contractual es compatible.

Pero no deberá manipular directamente el serializer.

El pipeline resolverá el serializer apropiado.

---

## 12.152 Relación con DeliveryResult

El resultado deberá conservar:

```text
consumer_id
```

y cuando aporte valor:

```text
consumer_profile_version
```

---

## 12.153 Prueba arquitectónica principal

La implementación deberá superar:

> Si mañana el Portal actual es sustituido completamente por una nueva interfaz, ¿puede HEYTI continuar produciendo y entregando las mismas respuestas mediante un nuevo ConsumerProfile y adaptador?

La respuesta deberá ser:

```text
YES
```

sin modificar:

```text
HKS
HES
Capability Registry
Capabilities
Materialization semantics
```

---

## 12.154 Prueba de módulo

La incorporación de una nueva superficie visual deberá poder resolverse mediante:

```text
Consumer/Profile/Presentation Adapter
```

sin introducir dependencias DOM dentro de HEYTI-CORE.

---

## 12.155 Prueba de incompatibilidad

Si un consumidor soporta únicamente:

```text
TEXT
```

y una respuesta requiere:

```text
TEXT
METRIC
TERRITORIAL_REFERENCE
```

la entrega deberá ser rechazada, salvo que exista una proyección contractual formal.

---

## 12.156 Prueba de transport independence

El mismo perfil:

```text
AT_PORTAL
```

deberá poder funcionar conceptualmente con:

```text
IN_MEMORY
```

en pruebas y:

```text
HTTP_JSON
```

en integración.

---

## 12.157 Prueba de neutralidad

ConsumerProfile deberá ser interpretable sin instalar:

```text
Leaflet
Chart.js
browser
```

---

## 12.158 Criterios mínimos de aceptación

El Consumer Model será considerado correctamente implementado cuando:

1. exista identidad lógica de consumidor;
2. exista un perfil validable;
3. pueda registrarse y resolverse un consumidor;
4. pueda validarse una versión contractual;
5. puedan compararse Content Types;
6. un consumidor desconocido sea rechazado;
7. una incompatibilidad sea rechazada antes del adaptador;
8. el perfil no contenga lógica visual específica;
9. el consumidor pueda sustituirse sin modificar capabilities;
10. `consumer_id` permanezca trazable en DeliveryResult.

---

## 12.159 Declaración arquitectónica del capítulo

Runtime Response Delivery deberá conocer a sus consumidores por lo que **declaran poder interpretar**, no por la tecnología con la que fueron construidos.

El Portal actual no deberá convertirse en una dependencia estructural de HEYTI.

Los módulos de AT 27–30 no deberán obligar al Core a adoptar HTML, Leaflet, Chart.js ni workflows visuales.

La arquitectura deberá utilizar consumidores lógicos, perfiles explícitos, contratos versionados y validación de capacidades.

La regla arquitectónica consolidada queda establecida como:

> **Un consumidor HEYTI es una identidad lógica asociada a un perfil explícito de contratos y capacidades semánticas. Runtime Response Delivery deberá validar compatibilidad antes de entregar, manteniendo independientes el consumidor, el transporte y la presentación.**

La relación fundamental queda formalizada como:

```text
Consumer ID
     ↓
Consumer Profile
     ↓
Compatibility Validation
     ↓
Delivery Contract
     ↓
Adapter
     ↓
Consumer
     ↓
Presentation
```

Con este modelo queda preparada la siguiente dimensión de la arquitectura:

**Delivery Adapter Model, registro de adaptadores y abstracción formal del transporte.**

---

**Fin del Capítulo 12**


# Capítulo 13. Delivery Adapter Model, registro de adaptadores y abstracción formal del transporte

## 13.1 Propósito del capítulo

Este capítulo define el **Delivery Adapter Model** de HEYTI Runtime Response Delivery.

La finalidad es establecer una arquitectura explícita para desacoplar la semántica de entrega del mecanismo técnico utilizado para transportar una respuesta hacia un consumidor.

El objetivo es impedir que Runtime Response Delivery quede ligado directamente a una tecnología concreta como:

```text
HTTP
WebSocket
archivo
memoria
IPC
cola
```

y permitir que estas tecnologías se incorporen mediante adaptadores sustituibles, testeables y trazables.

La regla fundamental será:

> **Delivery define qué significa entregar; el Adapter define cómo se ejecuta técnicamente esa entrega.**

---

## 13.2 DeliveryAdapter

Se define conceptualmente:

```text
DeliveryAdapter
```

como la abstracción responsable de ejecutar el cruce técnico de la frontera de Delivery.

Conceptualmente:

```text
Delivery Core
      ↓
DeliveryAdapter
      ↓
Transport / Boundary
      ↓
Consumer
```

El adaptador deberá ocultar los detalles específicos del transporte al resto del Core.

---

## 13.3 Responsabilidad del DeliveryAdapter

Un DeliveryAdapter podrá ser responsable de:

- aceptar un payload previamente validado;
- utilizar un mecanismo técnico concreto;
- aplicar parámetros operacionales del transporte;
- enviar o transferir el payload;
- recibir una confirmación técnica cuando exista;
- detectar errores de infraestructura;
- producir un resultado técnico normalizado.

No deberá:

- ejecutar capabilities;
- consultar HKS;
- consultar HES;
- materializar respuestas;
- modificar contenido cognitivo;
- decidir prioridades;
- transformar semántica;
- ejecutar workflows visuales.

---

## 13.4 Adapter no es Delivery

Debe preservarse:

```text
Delivery
   ≠
Adapter
```

Delivery representa la operación semántica.

Adapter representa una estrategia técnica.

Ejemplo:

```text
Delivery:
"entregar RESP-001 a AT_PORTAL"
```

Adapter:

```text
HTTP_JSON
```

---

## 13.5 Adapter no es Consumer

Debe mantenerse también:

```text
DeliveryAdapter
      ≠
Consumer
```

Un consumidor puede utilizar distintos adaptadores.

Ejemplo:

```text
AT_PORTAL
├── HTTP_JSON
└── WEBSOCKET_JSON
```

La identidad lógica del consumidor permanece igual.

---

## 13.6 Adapter no es Transport Protocol

Incluso el adaptador deberá considerarse una abstracción por encima del protocolo.

Por ejemplo:

```text
HTTP_JSON Adapter
```

puede encapsular:

```text
HTTP client
TLS
headers
timeouts
serialization framing
```

sin que Delivery conozca estos detalles.

---

## 13.7 Interface conceptual

La abstracción mínima podrá conceptualizarse como:

```python
deliver(payload, context) -> AdapterResult
```

Esta firma no constituye todavía una API definitiva.

Su intención es expresar que:

- el adapter recibe algo ya preparado;
- ejecuta transporte;
- devuelve un resultado técnico estructurado.

---

## 13.8 Adapter Input

El adaptador deberá recibir preferentemente:

```text
Validated DeliveryPayload
+
AdapterContext
+
DeliveryPolicy
```

No deberá recibir directamente:

```text
raw capability result
HKS object
HES object
DOM element
HTML component
```

---

## 13.9 AdapterContext

Podrá existir conceptualmente un contexto específico del adaptador.

Ejemplo:

```text
timeout
endpoint
headers
channel
transport metadata
```

Este contexto deberá permanecer separado de la semántica del Delivery Contract.

---

## 13.10 AdapterResult

Se define conceptualmente:

```text
AdapterResult
```

como el resultado técnico devuelto por el adapter.

Podrá contener:

```text
success
accepted
status
remote_reference
received_at
duration_ms
technical_code
error
metadata
```

La estructura deberá ser estable y normalizable.

---

## 13.11 AdapterResult no es DeliveryResult

Debe distinguirse:

```text
AdapterResult
      ≠
DeliveryResult
```

AdapterResult responde:

> ¿Qué ocurrió técnicamente en el transporte?

DeliveryResult responde:

> ¿Cuál fue el resultado formal de la operación de Delivery?

La traducción será responsabilidad del pipeline.

---

## 13.12 Ejemplo

AdapterResult:

```text
success = true
transport_status = 200
```

podrá mapearse a:

```text
DeliveryResult.status = DELIVERED
```

según política.

---

## 13.13 Adapter Error

Un adapter deberá convertir fallos técnicos conocidos a una estructura predecible.

Ejemplo:

```text
connection refused
```

podrá producir:

```text
AdapterResult
success = false
error_kind = TARGET_UNAVAILABLE
```

Delivery realizará luego el mapping contractual.

---

## 13.14 No exception leakage

El adapter no deberá obligar al resto del Core a conocer excepciones específicas de librerías.

Ejemplo incorrecto:

```text
requests.ConnectionError
```

como dependencia pública.

Preferible:

```text
AdapterTransportError
```

o un AdapterResult estructurado.

---

## 13.15 Adapter abstraction boundary

Conceptualmente:

```text
Core
──────────────────────────────
DeliveryAdapter Interface
──────────────────────────────
requests / httpx / websocket /
memory / file / future tech
```

Las librerías concretas deberán permanecer debajo de la interfaz.

---

## 13.16 DeliveryAdapterRegistry

La arquitectura podrá utilizar un:

```text
DeliveryAdapterRegistry
```

responsable de registrar y resolver adaptadores disponibles.

Conceptualmente:

```text
DeliveryAdapterRegistry
├── IN_MEMORY
├── HTTP_JSON
├── WEBSOCKET_JSON
└── INTERNAL_CALL
```

---

## 13.17 AdapterRegistry no es CapabilityRegistry

Debe preservarse:

```text
DeliveryAdapterRegistry
      ≠
CapabilityRegistry
```

CapabilityRegistry responde:

> ¿Qué puede ejecutar HEYTI?

DeliveryAdapterRegistry responde:

> ¿Qué mecanismos de entrega están disponibles?

---

## 13.18 AdapterRegistry no es ConsumerRegistry

Debe preservarse también:

```text
DeliveryAdapterRegistry
      ≠
ConsumerRegistry
```

ConsumerRegistry conoce:

```text
destinos lógicos
```

AdapterRegistry conoce:

```text
mecanismos técnicos
```

---

## 13.19 Adapter ID

Cada adapter deberá poseer una identidad estable.

Ejemplos:

```text
IN_MEMORY
HTTP_JSON
WEBSOCKET_JSON
INTERNAL_CALL
```

`adapter_id` deberá ser lógico.

No el nombre de una clase concreta.

---

## 13.20 Identidad lógica del adapter

Preferible:

```text
adapter_id = HTTP_JSON
```

a:

```text
adapter_id = HttpxAdapterV3Class
```

La implementación podrá cambiar sin alterar identidad semántica.

---

## 13.21 Adapter version

Podrá existir:

```text
adapter_version
```

si la implementación tiene cambios relevantes para auditoría.

No deberá introducirse si no aporta valor.

---

## 13.22 Adapter capabilities

Un adapter podrá declarar capacidades como:

```text
supports_sync
supports_async
supports_streaming
supports_receipt
supports_retry
max_payload_size
supported_encodings
```

Estas capacidades son técnicas.

No deben confundirse con Content Types del ConsumerProfile.

---

## 13.23 Consumer Capability vs Adapter Capability

Ejemplo:

Consumer:

```text
supports SERIES
```

Adapter:

```text
supports JSON payload up to N bytes
```

Son dimensiones distintas.

---

## 13.24 AdapterProfile

Podrá existir conceptualmente:

```text
AdapterProfile
```

si la complejidad lo justifica.

Para v1.0 probablemente bastará con atributos o metadata del adapter.

---

## 13.25 Adapter selection

La selección deberá basarse en información explícita como:

```text
consumer mapping
delivery policy
delivery mode
payload encoding
adapter availability
```

No en lógica arbitraria.

---

## 13.26 Adapter Resolver

Podrá existir:

```text
DeliveryAdapterResolver
```

responsable de determinar qué adapter utilizar.

Conceptualmente:

```text
ConsumerProfile
      +
DeliveryPolicy
      +
AdapterRegistry
      ↓
AdapterResolver
      ↓
Adapter
```

---

## 13.27 Resolver no ejecuta Delivery

El resolver únicamente selecciona.

No transporta.

La separación deberá permanecer clara.

---

## 13.28 Default Adapter

Puede existir un adapter predeterminado por consumidor o entorno.

Ejemplo:

```text
AT_PORTAL → HTTP_JSON
TEST_CLIENT → IN_MEMORY
```

La asociación deberá ser explícita.

---

## 13.29 No implicit first adapter

Queda prohibido seleccionar:

```text
the first registered adapter
```

como regla accidental.

---

## 13.30 Adapter mapping

Podrá existir una configuración conceptual:

```text
consumer_adapter_mapping
```

Ejemplo:

```text
AT_PORTAL:
    default = HTTP_JSON

TEST_CLIENT:
    default = IN_MEMORY
```

---

## 13.31 DeliveryPolicy override

Una política podrá solicitar:

```text
adapter_id = IN_MEMORY
```

para pruebas.

La selección deberá validar que el adapter sea compatible con el consumer.

---

## 13.32 Adapter compatibility

Antes de ejecutar deberá comprobarse:

```text
adapter supports requested delivery mode
adapter supports payload format
adapter permitted for consumer
adapter enabled
```

---

## 13.33 Adapter not found

Si:

```text
adapter_id = HTTP_JSON
```

no está registrado:

```text
REJECTED
```

con:

```text
DELIVERY_ADAPTER_NOT_AVAILABLE
```

---

## 13.34 Adapter disabled

Un adapter podrá estar configurado como:

```text
enabled = false
```

si existe necesidad operativa.

La resolución deberá tratarlo como no disponible.

---

## 13.35 Registro en bootstrap

Para v1.0 se recomienda registrar adaptadores durante bootstrap.

Ejemplo:

```text
IN_MEMORY
```

primero.

Posteriormente:

```text
HTTP_JSON
```

---

## 13.36 Registry read-only

Después de bootstrap, el registro deberá poder operar en modo:

```text
read-only
```

para evitar cambios inesperados durante ejecución.

---

## 13.37 Duplicate adapter_id

Registrar dos adapters con el mismo:

```text
adapter_id
```

deberá producir error.

---

## 13.38 Adapter factory

Si un adapter requiere construcción compleja podrá utilizarse una factory.

No deberá introducirse si una instancia simple es suficiente.

---

## 13.39 Dependency Injection

Los adapters deberán ser susceptibles de inyección.

Esto permitirá:

```text
real adapter
fake adapter
failing adapter
```

sin modificar Delivery Core.

---

## 13.40 Test Adapter

La implementación deberá incluir al menos un adapter controlado para pruebas.

El candidato natural es:

```text
InMemoryDeliveryAdapter
```

---

## 13.41 InMemoryDeliveryAdapter

Su responsabilidad será:

```text
receive validated payload
store/capture payload in memory
return deterministic AdapterResult
```

Sin red.

Sin navegador.

Sin servicios externos.

---

## 13.42 Ventajas del InMemory Adapter

Permitirá probar:

- AdapterRegistry;
- adapter resolution;
- Delivery pipeline;
- payload transfer;
- DeliveryResult;
- tracing;
- errores;
- consumer substitution.

---

## 13.43 InMemory success

Ejemplo conceptual:

```text
payload
  ↓
InMemoryAdapter
  ↓
append to captured_deliveries
  ↓
AdapterResult(success=true)
```

---

## 13.44 Captured delivery

El adapter podrá conservar:

```text
payload
context
timestamp
```

solo para tests.

No deberá convertirse en almacenamiento productivo.

---

## 13.45 InMemory failing mode

Podrá configurarse para simular:

```text
failure
timeout
rejection-like technical error
```

Esto será útil para pruebas negativas.

---

## 13.46 FailingDeliveryAdapter

También podrá existir un adapter específico de prueba:

```text
FailingDeliveryAdapter
```

si resulta más claro que parametrizar el InMemory Adapter.

---

## 13.47 Adapter test determinism

Los adapters de prueba deberán producir resultados deterministas.

Esto facilita:

```text
expected == actual
```

---

## 13.48 InternalCallAdapter

Una evolución temprana podría incorporar:

```text
InternalCallAdapter
```

para entregar a un consumidor dentro del mismo proceso.

Conceptualmente:

```text
Delivery
  ↓
InternalCallAdapter
  ↓
consumer callback
```

---

## 13.49 InternalCallAdapter y desacoplamiento

Incluso dentro del mismo proceso deberá utilizarse una interfaz.

No deberá llamar arbitrariamente funciones específicas de Portal.

---

## 13.50 HTTP_JSON Adapter

Un futuro adapter HTTP podrá:

```text
receive JSON payload
resolve endpoint configuration
set headers
apply timeout
perform request
interpret response
produce AdapterResult
```

---

## 13.51 HTTP Adapter no debe conocer UI

Aunque entregue al Portal, no deberá conocer:

```text
DOM
buttons
panels
Leaflet
Chart.js
```

Su responsabilidad termina en el transporte HTTP.

---

## 13.52 Endpoint configuration

La URL deberá provenir de:

```text
configuration
consumer mapping
environment
```

No de strings hardcoded en la semántica de Delivery.

---

## 13.53 HTTP headers

Headers técnicos podrán incluir:

```text
Content-Type
Authorization
Correlation-ID
```

según infraestructura.

No forman parte del Delivery Contract cognitivo.

---

## 13.54 Correlation headers

En transportes que lo permitan, podrá propagarse:

```text
correlation_id
delivery_id
```

como headers.

Esto mejora tracing.

---

## 13.55 WebSocket Adapter

Una futura interfaz conversacional puede beneficiarse de:

```text
WEBSOCKET_JSON
```

especialmente para:

- updates;
- streaming;
- interactividad.

No deberá implementarse hasta que la UI realmente lo requiera.

---

## 13.56 WebSocket Event Envelope

Un adapter podría envolver el payload en:

```text
event_type
event_id
```

como framing técnico.

El contenido Delivery deberá permanecer intacto.

---

## 13.57 Streaming adapter

En el futuro un adapter streaming podría manejar:

```text
START
CHUNK
END
```

pero requerirá contratos especializados.

No deberá contaminar la versión síncrona inicial.

---

## 13.58 File Adapter

Un adapter a archivo podría ser útil para:

- auditoría;
- exportación;
- pruebas.

Sin embargo, exportación a archivo no deberá confundirse con logging.

---

## 13.59 FileAdapter semantics

Si existe:

```text
FileDeliveryAdapter
```

deberá definir claramente:

> ¿Guardar el payload en archivo constituye DELIVERED?

Solo para el consumidor lógico correspondiente.

---

## 13.60 Queue Adapter futuro

En sistemas asíncronos podría existir:

```text
QUEUE_JSON
```

que considere éxito:

```text
message accepted by queue
```

No necesariamente procesado por el consumidor final.

---

## 13.61 Acceptance semantics per adapter

Cada adapter deberá documentar qué significa:

```text
success
```

en su contexto.

---

## 13.62 AdapterResult.success

No deberá existir un `success=true` ambiguo.

Su significado deberá alinearse con un criterio técnico documentado.

---

## 13.63 Receipt support

Un adapter podrá indicar:

```text
supports_receipt = true
```

si obtiene confirmación externa.

---

## 13.64 Receipt optional

Si no existe confirmación:

```text
receipt = null
```

puede ser válido.

Delivery no deberá inventarla.

---

## 13.65 Adapter timeout

Cada adapter que interactúe con infraestructura externa deberá aplicar timeout.

El timeout deberá provenir de política o configuración.

---

## 13.66 No infinite wait

Queda prohibido diseñar adapters que puedan bloquear indefinidamente.

---

## 13.67 Adapter retry

Los adapters no deberán implementar retries silenciosos por su cuenta.

Si una librería subyacente reintenta automáticamente, esa configuración deberá estar controlada.

---

## 13.68 Retry belongs to policy

La política de retry deberá permanecer visible al pipeline.

No escondida dentro del adapter.

---

## 13.69 Adapter idempotency

Los adapters deberán declarar o documentar si soportan operaciones idempotentes.

Esto será relevante antes de introducir retries.

---

## 13.70 Adapter cancellation

En una futura operación asíncrona podría soportarse cancelación.

No es requisito v1.0.

---

## 13.71 Adapter resource management

Los adapters deberán liberar correctamente recursos como:

```text
connections
sessions
streams
file handles
```

---

## 13.72 Context manager

En Python podrá utilizarse un context manager si ayuda al manejo seguro de recursos.

No constituye requisito conceptual.

---

## 13.73 Connection pooling

Un HTTP adapter futuro podrá utilizar pooling.

Esto pertenece a infraestructura.

No deberá modificar semántica de Delivery.

---

## 13.74 Adapter state

Los adapters deberán preferir ser:

```text
stateless
```

o tener estado controlado.

No deberán almacenar:

```text
current user
current session
last response
```

como variables globales.

---

## 13.75 Stateless adapter

Un adapter ideal recibe:

```text
payload
context
policy
```

y produce:

```text
AdapterResult
```

sin depender de invocaciones previas.

---

## 13.76 Connection state

Estado técnico como un pool de conexiones puede existir.

No deberá mezclarse con estado semántico de Delivery.

---

## 13.77 Thread safety

Si el Runtime opera concurrentemente, los adapters compartidos deberán ser seguros para concurrencia o utilizarse por instancia.

La implementación deberá documentar su modelo.

---

## 13.78 Async safety

La futura introducción de asyncio requerirá adapters compatibles.

No deberá imponerse async en v1.0 sin necesidad.

---

## 13.79 Sync Adapter v1.0

Para la primera versión se recomienda:

```text
synchronous adapter interface
```

por claridad y facilidad de pruebas.

---

## 13.80 Future async interface

En el futuro podrá evaluarse:

```python
async deliver(...)
```

mediante una abstracción separada o evolución del contrato interno.

---

## 13.81 No dual sync/async complexity initially

Queda desaconsejado soportar simultáneamente:

```text
sync
async
streaming
```

desde la primera versión.

---

## 13.82 Adapter configuration

La configuración técnica podrá incluir:

```text
endpoint
timeout
TLS settings
headers
queue name
file path
```

según adapter.

Deberá mantenerse fuera del Response Contract.

---

## 13.83 Configuration validation

Cada adapter deberá validar su configuración durante bootstrap cuando sea posible.

Ejemplo:

```text
HTTP adapter requires endpoint
```

Debe detectarse antes de una operación real.

---

## 13.84 Fail at startup when configuration invalid

Para configuraciones estáticas críticas, deberá preferirse:

```text
bootstrap failure
```

a descubrir el error en la primera entrega.

---

## 13.85 Runtime unavailable target

Aunque la configuración sea válida, el target puede estar caído.

Eso deberá producir:

```text
FAILED
```

durante ejecución.

---

## 13.86 Adapter error taxonomy

Los adapters deberán mapear errores técnicos a un conjunto pequeño.

Conceptualmente:

```text
TARGET_UNAVAILABLE
TIMEOUT
TRANSPORT_FAILURE
PROTOCOL_FAILURE
INVALID_RECEIPT
INTERNAL_ADAPTER_FAILURE
```

---

## 13.87 Mapping to DeliveryError

Ejemplo:

```text
Adapter TIMEOUT
      ↓
DeliveryError
code = DELIVERY_TIMEOUT
```

---

## 13.88 Protocol failure

Ejemplo HTTP:

```text
invalid response protocol
```

podría mapearse a:

```text
DELIVERY_ADAPTER_ERROR
```

con detalle interno.

---

## 13.89 Target unavailable

Ejemplo:

```text
connection refused
DNS failure
service unavailable
```

podrá mapearse a:

```text
DELIVERY_TARGET_UNAVAILABLE
```

---

## 13.90 Adapter internal failure

Una excepción no esperada dentro del adapter deberá mapearse:

```text
DELIVERY_ADAPTER_ERROR
```

o:

```text
DELIVERY_INTERNAL_ERROR
```

según frontera.

La política deberá ser estable.

---

## 13.91 AdapterResult validation

El pipeline deberá validar el resultado.

Ejemplo inválido:

```text
success = true
error != null
```

deberá rechazarse como inconsistente.

---

## 13.92 Adapter result status

Podrá existir:

```text
ACCEPTED
REJECTED
FAILED
UNKNOWN
```

como estado técnico si se requiere.

Para InMemory v1.0 puede ser mucho más simple.

---

## 13.93 Keep AdapterResult simple

La implementación inicial deberá evitar una máquina de estados excesiva.

Podrá bastar:

```text
success
receipt
error
metadata
```

---

## 13.94 Adapter receipt

Ejemplo:

```text
AdapterReceipt
├── accepted
├── remote_reference
└── received_at
```

Solo cuando el transporte lo proporcione.

---

## 13.95 Receipt identity

Una referencia remota deberá permanecer separada de:

```text
delivery_id
response_id
```

---

## 13.96 Adapter observability

El adapter deberá permitir medir:

```text
adapter_duration_ms
success
failure
timeout
payload_size
```

---

## 13.97 Adapter logs

Logs mínimos podrán incluir:

```text
delivery_id
adapter_id
target
status
duration
```

sin payload completo.

---

## 13.98 Sensitive configuration

No deberán registrarse:

```text
authorization tokens
passwords
private keys
```

---

## 13.99 Adapter auditability

La traza deberá permitir responder:

```text
which adapter?
which configuration version?
which target?
what result?
```

cuando corresponda.

---

## 13.100 Adapter selection trace

DeliveryTrace deberá registrar:

```text
adapter_id
```

del adapter realmente utilizado.

---

## 13.101 Adapter profile version trace

Podrá registrarse versión de adapter o configuración si existe necesidad.

No es obligatorio v1.0.

---

## 13.102 Adapter metrics by consumer

Podrá analizarse:

```text
AT_PORTAL + HTTP_JSON
```

para detectar problemas específicos de integración.

---

## 13.103 Adapter substitution test

La arquitectura deberá superar:

> ¿Puede sustituirse `IN_MEMORY` por `HTTP_JSON` sin modificar Materialization ni Response Contract?

La respuesta deberá ser:

```text
YES
```

---

## 13.104 Consumer substitution test

También:

> ¿Puede `HTTP_JSON` entregar a un consumidor distinto sin modificar su semántica central?

Siempre que el mapping y perfil lo permitan:

```text
YES
```

---

## 13.105 Serializer substitution

Un adapter no deberá depender de un objeto Python específico.

Deberá recibir una representación estable.

Esto permitirá cambiar el serializer sin reescribir la lógica completa del adapter.

---

## 13.106 Payload abstraction

Podrá existir:

```text
DeliveryPayload
├── content
├── encoding
├── content_type
└── size
```

como estructura técnica intermedia.

---

## 13.107 Payload bytes

Un adapter de red podrá preferir:

```text
bytes
```

ya serializados.

Un adapter InMemory podrá almacenar el diccionario o bytes según diseño.

La semántica deberá ser equivalente.

---

## 13.108 Adapter should not reserialize arbitrarily

Queda desaconsejado:

```text
each adapter serializes response differently
```

Esto generaría divergencia.

La serialización contractual deberá ocurrir antes.

---

## 13.109 Adapter framing

Un adapter podrá añadir framing técnico.

Ejemplo:

```text
WebSocket event wrapper
```

o:

```text
HTTP request headers
```

sin tocar el payload semántico.

---

## 13.110 Adapter and Gateway

Gateway podrá utilizar o alojar adapters.

La relación exacta dependerá de la implementación.

Sin embargo:

```text
Delivery Core
```

no deberá convertirse en framework web.

---

## 13.111 Gateway outbound flow

Conceptualmente:

```text
Delivery
   ↓
HTTP Adapter
   ↓
Gateway / Network Boundary
   ↓
Consumer
```

o:

```text
Gateway
   ↓
Delivery
   ↓
response returned through gateway
```

La arquitectura física podrá variar.

La semántica deberá permanecer.

---

## 13.112 Response return adapter

Para una API síncrona, la "entrega" podría consistir en retornar un payload al Gateway.

En ese caso podría existir:

```text
GatewayResponseAdapter
```

o un adapter interno equivalente.

---

## 13.113 No unnecessary outbound HTTP

Si el consumidor ya realizó una solicitud HTTP al Gateway, HEYTI no deberá necesariamente realizar una segunda llamada HTTP hacia el mismo consumidor.

La arquitectura deberá elegir el patrón de integración correcto.

---

## 13.114 Request/Response path

Una futura implementación probable podría ser:

```text
Browser
   │ HTTP Request
   ▼
HEYTI API / Gateway
   │
   ▼
Runtime
   │
   ▼
Materialization
   │
   ▼
Delivery
   │
   ▼
Gateway Response Adapter
   │
   ▼
HTTP Response
   │
   ▼
Browser
```

Este patrón podrá utilizar la misma semántica de Delivery.

---

## 13.115 Push path

Otro caso futuro:

```text
HEYTI
   ↓
WebSocket Adapter
   ↓
Browser
```

El modelo de adapters soportará ambos patrones.

---

## 13.116 Adapter taxonomy

Se propone conceptualmente distinguir:

```text
RETURN adapters
PUSH adapters
INTERNAL adapters
TEST adapters
```

No es obligatorio representarlo como clases.

---

## 13.117 Return Adapter

Representa una respuesta devuelta por la misma interacción.

Ejemplo:

```text
Gateway Response
```

---

## 13.118 Push Adapter

Inicia envío hacia un consumidor.

Ejemplo:

```text
WebSocket
Webhook
```

No es necesario desde v1.0.

---

## 13.119 Internal Adapter

Entrega dentro del proceso o sistema.

---

## 13.120 Test Adapter

Existe para pruebas controladas.

---

## 13.121 No webhook assumptions

Runtime Response Delivery no deberá asumir que Delivery significa "hacer POST a una URL".

Ese es solamente un caso posible.

---

## 13.122 Adapter Security

Los adapters deberán respetar configuración de seguridad.

Podrán requerir:

```text
TLS
authentication
authorization headers
certificate validation
```

cuando corresponda.

---

## 13.123 No custom crypto

Los adapters no deberán implementar algoritmos criptográficos improvisados.

Deberán utilizar mecanismos estándar y librerías confiables.

---

## 13.124 Certificate verification

Un HTTP adapter productivo deberá validar certificados por defecto.

Deshabilitar verificación deberá ser una excepción explícita de desarrollo.

---

## 13.125 SSRF considerations

Si endpoints pueden configurarse dinámicamente, deberá existir control para evitar entregas a destinos no autorizados.

La política de seguridad deberá restringir targets.

---

## 13.126 ConsumerRegistry as target authority

Una estrategia segura será que Delivery únicamente pueda resolver targets registrados.

No URLs arbitrarias suministradas directamente por un usuario.

---

## 13.127 Endpoint allowlist

En producción podrá existir una allowlist de endpoints por consumer.

Esto pertenece a configuración de adapter/seguridad.

---

## 13.128 Payload privacy

El adapter no deberá modificar el payload para añadir datos internos sensibles.

---

## 13.129 Compression

Un adapter podrá aplicar:

```text
gzip
```

u otra compresión estándar.

Esto será transparente para Delivery semantics.

---

## 13.130 Payload size threshold

La decisión de comprimir podrá pertenecer al adapter.

No al materializador.

---

## 13.131 Transport encoding

Detalles como:

```text
Content-Encoding
```

pertenecen al adapter.

---

## 13.132 Adapter error boundary

Conceptualmente:

```text
Validated Payload
      ↓
ADAPTER BOUNDARY
      ↓
Transport Technology
```

Cualquier fallo inferior deberá mapearse al AdapterResult.

---

## 13.133 No transport exception escape

Ninguna excepción específica del transporte deberá escapar sin control hacia la UI.

---

## 13.134 Adapter lifecycle

Conceptualmente:

```text
initialize
validate configuration
ready
deliver
shutdown
```

No todos estos métodos serán necesarios en la primera versión.

---

## 13.135 Bootstrap validation

El Registry deberá poder verificar que adapters registrados sean válidos.

---

## 13.136 Adapter health

En el futuro podrá existir:

```text
health_check()
```

para adapters externos.

No deberá confundirse con una entrega real.

---

## 13.137 Health does not guarantee delivery

Un adapter saludable puede experimentar fallos puntuales.

La entrega deberá seguir manejando errores.

---

## 13.138 Adapter circuit state

En versiones futuras podría existir:

```text
OPEN
HALF_OPEN
CLOSED
```

si se implementa circuit breaker.

No debe introducirse ahora.

---

## 13.139 Adapter observability events

Podrán emitirse eventos:

```text
adapter.started
adapter.completed
adapter.failed
adapter.timeout
```

correlacionados por `delivery_id`.

---

## 13.140 Adapter duration

Se deberá poder medir:

```text
adapter_duration_ms
```

separadamente de:

```text
total_delivery_duration_ms
```

Esto ayuda a distinguir tiempo de validación de tiempo de transporte.

---

## 13.141 Adapter payload size

El adapter deberá poder conocer:

```text
payload_size_bytes
```

si requiere límites.

---

## 13.142 Adapter response size

Un HTTP adapter podrá limitar también:

```text
response_size
```

para evitar respuestas técnicas inesperadamente grandes.

---

## 13.143 No arbitrary remote content

El adapter no deberá aceptar y propagar al Core cualquier cuerpo remoto sin validación.

---

## 13.144 Receipt parsing

La respuesta técnica deberá mapearse solo a los campos necesarios de AdapterResult.

---

## 13.145 Adapter testability

Todo adapter deberá poder probarse independientemente del Runtime completo.

---

## 13.146 Unit tests de Registry

```text
test_register_adapter
test_reject_duplicate_adapter_id
test_resolve_adapter
test_unknown_adapter
```

---

## 13.147 Unit tests de InMemory Adapter

```text
test_inmemory_adapter_delivers_payload
test_inmemory_adapter_captures_context
test_inmemory_adapter_returns_success_result
```

---

## 13.148 Failure tests

```text
test_failing_adapter_returns_failure
test_adapter_exception_is_mapped
test_timeout_is_mapped
```

---

## 13.149 Compatibility tests

```text
test_adapter_rejects_unsupported_encoding
test_adapter_rejects_unsupported_mode
```

---

## 13.150 Isolation tests

```text
test_adapter_does_not_modify_payload
```

deberá verificar que el adapter no muta la estructura recibida.

---

## 13.151 Payload immutability

Preferentemente, el adapter deberá tratar payload como:

```text
read-only
```

durante la operación.

---

## 13.152 Context immutability

De igual manera:

```text
DeliveryContext
```

deberá considerarse read-only desde el adapter.

---

## 13.153 DeliveryResult mapping tests

Deberá probarse que:

```text
AdapterResult success
→ DELIVERED
```

y:

```text
AdapterResult failure
→ FAILED
```

según reglas.

---

## 13.154 Adapter selection tests

```text
test_portal_resolves_configured_adapter
test_test_client_resolves_inmemory_adapter
```

---

## 13.155 Transport substitution test

La misma respuesta deberá poder pasar por:

```text
IN_MEMORY
```

y después:

```text
HTTP_JSON
```

sin cambiar `response_id`.

---

## 13.156 Consumer substitution test

Un InMemory Adapter deberá poder utilizarse con distintos perfiles de prueba.

Esto demuestra desacoplamiento entre consumer y adapter.

---

## 13.157 Adapter MVP para Sprint 23

Para la primera implementación se recomienda desarrollar únicamente:

```text
DeliveryAdapter base contract
AdapterResult
DeliveryAdapterRegistry
InMemoryDeliveryAdapter
```

y sus pruebas.

No deberá implementarse HTTP hasta que el núcleo esté completamente verificado.

---

## 13.158 Razón del MVP

El objetivo inicial es probar:

```text
MaterializedResponse
      ↓
Delivery Pipeline
      ↓
Serialized Payload
      ↓
InMemoryDeliveryAdapter
      ↓
DeliveryResult
```

sin introducir errores de red.

---

## 13.159 Segundo paso de implementación

Una vez estable:

```text
InMemory Delivery
```

podrá evaluarse:

```text
Gateway/Internal Return Adapter
```

como puente inicial hacia Portal.

---

## 13.160 HTTP posterior

El HTTP outbound dedicado deberá incorporarse solo si el patrón de integración realmente lo requiere.

---

## 13.161 WebSocket posterior

WebSocket deberá introducirse cuando exista necesidad de:

- push;
- streaming;
- actualización interactiva.

No por anticipación.

---

## 13.162 Estructura conceptual del paquete

La futura implementación podría evolucionar hacia algo semejante a:

```text
src/heyti/delivery/
├── __init__.py
├── contracts.py
├── context.py
├── errors.py
├── serializer.py
├── validator.py
├── service.py
└── adapters/
    ├── __init__.py
    ├── base.py
    ├── registry.py
    └── in_memory.py
```

Esta estructura es conceptual.

La estructura definitiva deberá armonizar con el repositorio real antes de crear archivos.

---

## 13.163 No implementación todavía

La estructura anterior no autoriza a crear código antes de concluir la arquitectura del Sprint.

Primero deberá cerrarse el documento rector.

Posteriormente se realizará auditoría contra la estructura real de HEYTI-CORE.

---

## 13.164 Adapter Base Contract conceptual

Podrá definirse mediante una abstracción similar a:

```python
class DeliveryAdapter:
    adapter_id: str

    def deliver(self, payload, context):
        ...
```

La firma definitiva deberá decidirse durante implementación.

---

## 13.165 AdapterResult conceptual

```python
class AdapterResult:
    success: bool
    receipt: object | None
    error: object | None
    metadata: dict
```

Esta estructura deberá mantenerse simple.

---

## 13.166 InMemory Adapter conceptual

```python
class InMemoryDeliveryAdapter(DeliveryAdapter):
    adapter_id = "IN_MEMORY"

    def deliver(self, payload, context):
        self.captured.append(payload)
        return AdapterResult(success=True)
```

Este código es exclusivamente conceptual.

No deberá copiarse todavía como implementación definitiva.

---

## 13.167 Registry conceptual

```python
registry.register(adapter)
adapter = registry.get("IN_MEMORY")
```

La resolución deberá ser determinista.

---

## 13.168 Registro y bootstrap

El bootstrap podría registrar:

```text
IN_MEMORY
```

como adapter base del Runtime.

Esto deberá integrarse sin alterar CapabilityRegistry.

---

## 13.169 EventBus integration

En el futuro el adapter o Delivery Service podrá emitir:

```text
delivery.started
delivery.completed
delivery.failed
```

a EventBus.

No deberá ser responsabilidad del adapter notificar directamente a múltiples sistemas.

---

## 13.170 Adapter purity

Idealmente, el adapter tendrá un único efecto principal:

```text
attempt delivery
```

y producirá un resultado.

Los efectos auxiliares deberán mantenerse mínimos.

---

## 13.171 Adapter does not persist business state

Queda prohibido que un adapter modifique:

```text
electoral results
field records
section priority
campaign strategy
```

como efecto lateral de Delivery.

---

## 13.172 Consumer callback safety

Si un InternalCallAdapter invoca un callback del consumidor, deberá aislar sus errores.

Una excepción del consumer deberá mapearse a un error técnico de Delivery.

---

## 13.173 Consumer processing vs acceptance

Si el callback procesa completamente la respuesta dentro de la misma llamada, la política deberá definir qué constituye éxito.

---

## 13.174 Adapter acknowledgement semantics

La definición de éxito deberá documentarse por adapter.

Ejemplo:

```text
IN_MEMORY:
success when payload captured.

INTERNAL_CALL:
success when consumer callback returns accepted.

HTTP:
success according to configured status policy.
```

---

## 13.175 Adapter documentation

Cada adapter deberá documentar:

```text
adapter_id
transport type
delivery mode
input payload
success criteria
failure mapping
timeout policy
receipt semantics
idempotency behavior
```

---

## 13.176 Adapter governance

Agregar un adapter nuevo deberá requerir:

1. contrato compatible;
2. implementación;
3. registro;
4. pruebas;
5. documentación;
6. revisión de seguridad;
7. verificación de trazabilidad.

---

## 13.177 No adapter without tests

Ningún adapter productivo deberá registrarse sin pruebas mínimas.

---

## 13.178 No adapter-specific cognitive logic

Una prueba arquitectónica deberá confirmar que no existen condiciones como:

```text
if section.margin < 3:
    HTTP adapter behaves differently
```

---

## 13.179 No adapter-specific presentation logic

También deberá prohibirse:

```text
if adapter == HTTP_JSON:
    add chart colors
```

---

## 13.180 Adapter only technical transformation

Las únicas transformaciones autorizadas serán técnicas.

Ejemplos:

```text
JSON → bytes
bytes → compressed bytes
payload → HTTP body
```

---

## 13.181 Invariantes del Delivery Adapter Model

Se establecen los siguientes invariantes.

### HRRD-A01 — Adapter Encapsulation

Todo mecanismo técnico de entrega deberá quedar encapsulado por un adapter.

### HRRD-A02 — Transport Independence

Delivery Core no dependerá directamente de librerías o protocolos concretos.

### HRRD-A03 — Adapter Identity

Todo adapter deberá poseer identidad lógica estable.

### HRRD-A04 — Adapter Result

Toda ejecución deberá producir un resultado técnico normalizado.

### HRRD-A05 — No Semantic Mutation

El adapter no deberá modificar el significado del payload.

### HRRD-A06 — No Presentation Logic

El adapter no conocerá DOM, Leaflet, Chart.js ni componentes visuales.

### HRRD-A07 — Explicit Resolution

La selección del adapter deberá ser explícita y determinista.

### HRRD-A08 — Registry Separation

AdapterRegistry permanecerá separado de ConsumerRegistry y CapabilityRegistry.

### HRRD-A09 — No Hidden Retry

Los adapters no deberán reintentar silenciosamente.

### HRRD-A10 — Test Substitutability

Todo adapter deberá poder sustituirse por un adapter de prueba sin modificar Delivery Core.

---

## 13.182 Prueba de conformidad

Una implementación deberá demostrar:

1. que Delivery puede ejecutarse con InMemory Adapter;
2. que el adapter recibe payload previamente validado;
3. que el adapter no modifica la respuesta;
4. que el adapter puede resolverse por `adapter_id`;
5. que un adapter desconocido genera error explícito;
6. que adapters duplicados no pueden registrarse;
7. que errores técnicos se normalizan;
8. que `adapter_id` aparece en trazabilidad;
9. que el Core no depende de tecnología de red;
10. que cambiar el adapter no obliga a cambiar Materialization.

---

## 13.183 Flujo operacional consolidado

```text
DeliveryRequest
      │
      ▼
ConsumerProfile
      │
      ▼
DeliveryPolicy
      │
      ▼
Adapter Resolver
      │
      ▼
DeliveryAdapterRegistry
      │
      ▼
DeliveryAdapter
      │
      ▼
Validated Payload
      │
      ▼
Transport / Boundary
      │
      ▼
AdapterResult
      │
      ▼
Delivery Result Mapper
      │
      ▼
DeliveryResult
```

---

## 13.184 Flujo con adapter inexistente

```text
Requested Adapter
      │
      ▼
AdapterRegistry
      │
      ▼
NOT FOUND
      │
      ▼
DeliveryError
DELIVERY_ADAPTER_NOT_AVAILABLE
      │
      ▼
REJECTED
```

---

## 13.185 Flujo con fallo técnico

```text
Adapter
  ↓
Transport
  ↓
ERROR
  ↓
AdapterResult(success=false)
  ↓
Error Mapping
  ↓
DeliveryResult(status=FAILED)
```

---

## 13.186 Flujo exitoso

```text
Validated Payload
      ↓
Adapter
      ↓
Boundary Crossing
      ↓
Acceptance Criteria Met
      ↓
AdapterResult(success=true)
      ↓
DeliveryResult
      ↓
DELIVERED
```

---

## 13.187 Criterio de éxito arquitectónico

El Delivery Adapter Model será considerado correcto cuando HEYTI pueda ejecutar la misma operación de Delivery mediante dos adapters diferentes sin alterar:

```text
response semantics
response_id
delivery contract
capability
materialization logic
```

y cuando el único cambio relevante corresponda a:

```text
adapter_id
transport metadata
technical result
```

---

## 13.188 Declaración arquitectónica del capítulo

Runtime Response Delivery no deberá convertirse en una colección de llamadas directas a tecnologías de red.

Todo mecanismo técnico deberá permanecer encapsulado detrás de una abstracción explícita de Adapter.

El Adapter conoce el transporte.

Delivery conoce el contrato.

El Consumer conoce el contenido.

Presentation conoce la visualización.

La regla arquitectónica consolidada queda establecida como:

> **Todo cruce técnico de la frontera de Runtime Response Delivery deberá ejecutarse mediante un DeliveryAdapter identificable, sustituible, validable y trazable. Los adapters podrán transformar la representación técnica necesaria para transportar un payload, pero no podrán modificar su significado, ejecutar cognición ni introducir lógica de presentación.**

La separación fundamental queda formalizada como:

```text
Response Contract
      ↓
Delivery Contract
      ↓
Validated Payload
      ↓
DeliveryAdapter
      ↓
Transport
      ↓
Consumer
```

Con este modelo queda preparada la siguiente dimensión de la arquitectura:

**la frontera formal entre Runtime Response Delivery, Gateway y exposición externa de HEYTI.**

---

**Fin del Capítulo 13**


# Capítulo 14. Frontera formal entre Runtime Response Delivery, Gateway y exposición externa de HEYTI

## 14.1 Propósito del capítulo

Este capítulo define la relación arquitectónica entre **HEYTI Runtime Response Delivery (HRRD)**, el **Gateway** y los mecanismos mediante los cuales HEYTI expone respuestas hacia consumidores externos.

La finalidad es establecer una separación rigurosa entre:

- la semántica de entrega;
- la exposición externa del sistema;
- los protocolos de transporte;
- el enrutamiento;
- y la presentación.

El objetivo es impedir que Runtime Response Delivery se convierta en:

```text
servidor HTTP
router
controlador REST
WebSocket server
framework web
handler del navegador
```

y, al mismo tiempo, permitir que sus resultados puedan exponerse correctamente mediante estas tecnologías cuando corresponda.

La regla fundamental será:

> **Delivery prepara y formaliza la salida; Gateway expone esa salida al exterior.**

---

## 14.2 Gateway como frontera externa

Se define conceptualmente **Gateway** como la frontera encargada de mediar entre HEYTI y consumidores externos.

El Gateway podrá encargarse de:

- recibir solicitudes;
- autenticar;
- autorizar;
- validar protocolo;
- convertir entradas externas a contratos internos;
- invocar Runtime;
- recibir DeliveryResult o DeliveryPayload;
- mapear resultados al protocolo externo;
- devolver respuestas.

Conceptualmente:

```text
External Consumer
       │
       ▼
Gateway
       │
       ▼
HEYTI Runtime
       │
       ▼
Materialization
       │
       ▼
Runtime Response Delivery
       │
       ▼
Gateway
       │
       ▼
External Consumer
```

---

## 14.3 Gateway no es Runtime

Debe preservarse:

```text
Gateway
   ≠
Runtime
```

Gateway media interacción externa.

Runtime ejecuta capacidades y coordinación interna.

---

## 14.4 Gateway no es Delivery

También debe mantenerse:

```text
Gateway
   ≠
Delivery
```

Gateway responde:

> ¿Cómo entra o sale una interacción mediante un protocolo externo?

Delivery responde:

> ¿Qué condiciones debe cumplir una respuesta para ser entregable?

---

## 14.5 Gateway no es Presentation

Gateway tampoco deberá:

```text
renderizar mapas
dibujar gráficas
manipular DOM
decidir colores
```

aunque pueda entregar datos a una UI.

---

## 14.6 Cadena de responsabilidad

La cadena recomendada será:

```text
Consumer
   ↓
Gateway
   ↓
Runtime
   ↓
Materialization
   ↓
Delivery
   ↓
Gateway
   ↓
Consumer
   ↓
Presentation
```

Esto establece dos pasos por Gateway:

- entrada;
- salida.

---

## 14.7 Gateway inbound

En entrada, Gateway podrá transformar una petición externa en una estructura interna.

Ejemplo futuro:

```text
HTTP Request
   ↓
Gateway
   ↓
HeytiRequest
```

El Runtime no deberá depender directamente del request HTTP.

---

## 14.8 Gateway outbound

En salida, Gateway podrá transformar:

```text
DeliveryResult
```

o:

```text
DeliveryPayload
```

en una respuesta de protocolo.

Ejemplo:

```text
DeliveryResult
   ↓
Gateway
   ↓
HTTP Response
```

---

## 14.9 Delivery Boundary vs Gateway Boundary

Debe distinguirse:

```text
Delivery Boundary
```

de:

```text
External Protocol Boundary
```

Conceptualmente:

```text
HEYTI Core
────────────────────────────
Delivery Boundary
────────────────────────────
Gateway / Adapter
────────────────────────────
Protocol Boundary
────────────────────────────
Consumer
```

---

## 14.10 Gateway como adaptador de borde

Arquitectónicamente, Gateway podrá actuar como:

```text
Boundary Adapter
```

encapsulando detalles como:

```text
HTTP
headers
status codes
routes
WebSocket frames
```

sin contaminar el Core.

---

## 14.11 Request/Response Path

Para una interacción síncrona típica:

```text
Browser
  │
  │ HTTP Request
  ▼
Gateway
  │
  ▼
Runtime
  │
  ▼
Capability
  │
  ▼
Materialization
  │
  ▼
Delivery
  │
  ▼
Gateway Response Adapter
  │
  │ HTTP Response
  ▼
Browser
```

Este patrón será probablemente el más natural para una primera integración con Portal.

---

## 14.12 Push Path

En un escenario futuro:

```text
Runtime
   ↓
Delivery
   ↓
WebSocket Adapter
   ↓
Gateway
   ↓
Consumer
```

podrá utilizarse para respuestas push o streaming.

---

## 14.13 No outbound HTTP innecesario

Si la interacción ya ocurre mediante request/response HTTP, HEYTI no deberá necesariamente realizar una segunda llamada HTTP hacia el navegador.

Debe preferirse:

```text
return through existing gateway response
```

cuando el patrón lo permita.

---

## 14.14 Gateway Response Adapter

Podrá existir conceptualmente:

```text
GatewayResponseAdapter
```

como implementación de DeliveryAdapter para devolver una respuesta por el mismo flujo de entrada.

---

## 14.15 Responsabilidad del GatewayResponseAdapter

Podrá encargarse de:

- aceptar payload;
- asociarlo a la respuesta pendiente;
- devolverlo al Gateway;
- producir AdapterResult.

No deberá modificar semántica.

---

## 14.16 HTTP Adapter vs GatewayResponseAdapter

Debe distinguirse:

```text
HTTP outbound adapter
```

de:

```text
gateway return adapter
```

El primero inicia una llamada.

El segundo devuelve por la interacción existente.

---

## 14.17 Integración recomendada inicial

Para el primer puente hacia una UI, la arquitectura debería preferir:

```text
Consumer Request
      ↓
Gateway
      ↓
Runtime
      ↓
Delivery
      ↓
Gateway Response
      ↓
Consumer
```

antes que:

```text
Runtime
      ↓
new outbound HTTP request
      ↓
Browser
```

---

## 14.18 HTTP como detalle de protocolo

Runtime Response Delivery no deberá contener directamente:

```text
GET
POST
PUT
DELETE
HTTP 200
HTTP 404
headers
cookies
```

Estos conceptos pertenecen al Gateway o adapter.

---

## 14.19 Mapping DeliveryResult → HTTP

Gateway podrá mapear estados a HTTP.

Ejemplo conceptual:

```text
DELIVERED
→ 200
```

```text
REJECTED
→ 4xx
```

```text
FAILED
→ 5xx
```

La correspondencia exacta deberá definirse en una especificación de Gateway.

---

## 14.20 No equivalencia universal

No deberá asumirse:

```text
REJECTED = 400
FAILED = 500
```

en todos los casos.

Por ejemplo:

```text
DELIVERY_NOT_AUTHORIZED
```

podría mapearse a:

```text
403
```

---

## 14.21 HTTP mapping fuera del Core

Los códigos HTTP no deberán formar parte obligatoria de DeliveryError.

El Gateway realizará el mapping.

---

## 14.22 Ejemplo de mapping

Conceptualmente:

```text
DELIVERY_CONTRACT_MISMATCH
      ↓
Gateway
      ↓
HTTP 409 / 422
```

La decisión concreta deberá permanecer fuera de HRRD.

---

## 14.23 Content-Type

Gateway podrá declarar:

```text
Content-Type: application/json
```

si el payload es JSON.

Esto no pertenece al Response Contract.

---

## 14.24 Correlation headers

Gateway podrá propagar:

```text
X-Correlation-ID
X-Request-ID
X-Delivery-ID
```

si la política lo permite.

Los nombres concretos no deberán formar parte de HRRD Core.

---

## 14.25 Security headers

Headers de seguridad deberán gestionarse en Gateway.

Ejemplos:

```text
Authorization
CORS
CSP
CSRF-related mechanisms
```

según la arquitectura de aplicación.

---

## 14.26 Authentication

Gateway será el lugar natural para autenticar consumidores externos.

Conceptualmente:

```text
External Request
      ↓
Authentication
      ↓
principal_id
      ↓
DeliveryContext
```

---

## 14.27 Authorization

Gateway podrá ejecutar autorización inicial.

Delivery podrá verificar autorización contextual adicional si es necesario.

No deberán duplicarse reglas sin gobernanza.

---

## 14.28 Input validation

Gateway deberá validar aspectos del protocolo.

Ejemplo:

```text
valid JSON body
allowed route
required request parameters
```

Runtime validará el contrato interno.

---

## 14.29 Dual validation

Debe mantenerse:

```text
Protocol Validation
      ↓
Contract Validation
```

Son responsabilidades distintas.

---

## 14.30 Gateway Request Contract

Podrá existir una futura especificación:

```text
HEYTI Gateway Request Contract
```

separada de:

```text
HEYTI Runtime Response Delivery Contract
```

---

## 14.31 Ruta futura conceptual

Una API podría exponer:

```text
POST /heyti/query
```

pero este endpoint es ilustrativo.

No constituye decisión de este capítulo.

---

## 14.32 No hardcode route in Core

HEYTI-CORE no deberá depender de:

```text
/heyti/query
```

La ruta pertenece al Gateway.

---

## 14.33 Gateway Controller

Un controlador podría:

1. recibir request;
2. construir request interno;
3. invocar Runtime;
4. recibir DeliveryPayload;
5. mapear resultado;
6. responder.

La lógica deberá mantenerse delgada.

---

## 14.34 Thin Gateway

El Gateway deberá evitar contener:

- reglas cognitivas;
- reglas territoriales;
- materialización;
- lógica de negocio.

Su función principal será adaptación de frontera.

---

## 14.35 No duplicate Materialization in Gateway

Queda prohibido:

```text
Runtime returns raw capability result
      ↓
Gateway invents response structure
```

La estructura deberá venir ya materializada y entregable.

---

## 14.36 No duplicate Delivery in Gateway

Gateway no deberá revalidar semántica de Delivery de manera independiente.

Podrá verificar protocolo y mapear resultados.

---

## 14.37 Gateway y ConsumerProfile

Gateway podrá ayudar a identificar:

```text
consumer_id
```

a partir de:

- cliente autenticado;
- aplicación;
- configuración;
- ruta;
- sesión.

Pero deberá entregar una identidad lógica a Delivery.

---

## 14.38 No derive consumer from filename

Ejemplo incorrecto:

```text
if Referer contains portal.html:
    consumer = AT_PORTAL
```

como base arquitectónica.

Preferible:

```text
registered client identity
```

o configuración explícita.

---

## 14.39 Gateway y Session

Gateway podrá recuperar:

```text
session_id
```

y propagarlo a Runtime/DeliveryContext.

---

## 14.40 Gateway y request_id

Gateway es un lugar natural para generar:

```text
request_id
```

al ingresar una solicitud externa.

---

## 14.41 request_id propagation

La secuencia será:

```text
Gateway generates request_id
      ↓
Runtime
      ↓
Materialization
      ↓
Delivery
      ↓
Gateway response
```

El mismo ID deberá conservarse.

---

## 14.42 correlation_id propagation

Si existe `correlation_id`, Gateway deberá preservarlo o generarlo conforme a política.

---

## 14.43 External correlation

Si un consumidor proporciona un correlation ID válido, Gateway podrá aceptarlo o mapearlo.

Esto deberá estar gobernado para evitar abuso.

---

## 14.44 No trust arbitrary tracing IDs blindly

Los IDs externos deberán validarse en:

- formato;
- longitud;
- seguridad.

---

## 14.45 Gateway y errores

Gateway deberá recibir errores ya clasificados por Delivery.

Ejemplo:

```text
DeliveryError
```

y convertirlos a protocolo.

---

## 14.46 Gateway error response

Ejemplo conceptual:

```json
{
  "status": "error",
  "code": "DELIVERY_TIMEOUT",
  "delivery_id": "DEL-001"
}
```

La forma exacta deberá ser parte del contrato de exposición externa.

---

## 14.47 Public error projection

Gateway podrá reducir detalle interno.

Por ejemplo:

```text
internal:
cause = ConnectionRefusedError
```

no deberá salir.

---

## 14.48 Gateway y stack traces

Stack traces no deberán exponerse en producción.

---

## 14.49 Gateway y logging

Gateway deberá registrar:

```text
request_id
consumer_id
route
result
```

cuando corresponda.

Delivery registrará:

```text
delivery_id
response_id
adapter_id
```

La correlación permitirá reconstruir todo el flujo.

---

## 14.50 End-to-end trace

Conceptualmente:

```text
Gateway Request Log
 request_id=REQ-001

Runtime Log
 execution_id=EXE-001

Materialization Log
 response_id=RESP-001

Delivery Log
 delivery_id=DEL-001

Gateway Response Log
 request_id=REQ-001
 delivery_id=DEL-001
```

---

## 14.51 Gateway observability

Gateway podrá medir:

```text
request_latency
HTTP status
request_count
```

Delivery medirá:

```text
delivery_latency
delivery failures
serialization time
adapter time
```

---

## 14.52 No metric duplication

No deberán mezclarse métricas sin distinguir qué frontera miden.

---

## 14.53 Gateway timeout vs Delivery timeout

Debe distinguirse:

```text
Gateway request timeout
```

de:

```text
Delivery adapter timeout
```

Pueden ser distintos.

---

## 14.54 Timeout hierarchy

Conceptualmente:

```text
Gateway overall timeout
   >
Runtime execution budget
      +
Delivery budget
```

La política exacta deberá definirse posteriormente.

---

## 14.55 Cancellation propagation

Si el consumidor cancela una solicitud, Gateway podrá propagar cancelación.

No es requisito obligatorio en v1.0.

---

## 14.56 Client disconnect

Un navegador podría cerrar conexión mientras HEYTI sigue procesando.

La arquitectura deberá decidir en el futuro si:

- cancela Runtime;
- completa procesamiento;
- conserva respuesta.

No debe resolverse improvisadamente en Delivery.

---

## 14.57 Synchronous MVP

Para v1.0 deberá favorecerse un flujo síncrono simple:

```text
request
→ runtime
→ materialization
→ delivery
→ response
```

Esto facilita integración inicial.

---

## 14.58 Asynchronous future

En el futuro:

```text
request accepted
→ job_id
→ processing
→ delivery later
```

requerirá contratos adicionales.

No forma parte de v1.0.

---

## 14.59 Streaming future

Un Gateway podría soportar:

```text
SSE
WebSocket
chunked HTTP
```

No deberá incorporarse hasta existir necesidad de UX.

---

## 14.60 SSE

Server-Sent Events podría ser apropiado para:

- respuestas progresivas;
- notificaciones unidireccionales.

No deberá considerarse requisito actual.

---

## 14.61 WebSocket

WebSocket podría soportar:

- conversación;
- updates en tiempo real;
- Día D;
- Campo;
- flujos operativos.

Pero deberá mantenerse separado del contrato base.

---

## 14.62 Long polling

No deberá adoptarse salvo necesidad concreta.

---

## 14.63 Gateway y Portal actual

El Portal actual puede evolucionar para realizar solicitudes a un Gateway HEYTI.

Conceptualmente:

```text
Portal JavaScript
      ↓
fetch()
      ↓
HEYTI Gateway
      ↓
Runtime
      ↓
Delivery
      ↓
JSON response
      ↓
Portal Adapter
```

---

## 14.64 Portal Adapter

En Presentation podrá existir una capa JavaScript que interprete Delivery Contract.

Ejemplo:

```text
HEYTI response
      ↓
portal adapter
      ↓
render text / chart / map
```

Esta capa deberá permanecer fuera de Python Core.

---

## 14.65 Gateway no debe devolver HTML de HEYTI Core

El Core deberá preferir datos estructurados.

No HTML renderizado.

---

## 14.66 JSON-first integration

Para primera integración deberá favorecerse:

```text
JSON
```

por:

- interoperabilidad;
- depuración;
- pruebas;
- facilidad de consumo desde JavaScript.

---

## 14.67 JSON response contract

La respuesta JSON deberá derivar directamente del Delivery Contract.

No deberá existir un shape independiente inventado por cada endpoint.

---

## 14.68 API consistency

Si existen varios endpoints futuros, deberán reutilizar contratos comunes.

No deberá existir:

```text
endpoint A response shape
endpoint B response shape
endpoint C response shape
```

sin necesidad.

---

## 14.69 API versioning

Gateway podrá versionar API de manera independiente.

Ejemplo:

```text
/api/v1/...
```

No necesariamente coincide con:

```text
delivery_contract_version
```

---

## 14.70 Version dimensions

Debe distinguirse:

```text
API version
Delivery Contract version
Response Contract version
Consumer Profile version
```

Cada una tiene propósito diferente.

---

## 14.71 No forced lockstep

No deberá exigirse:

```text
API v1
=
Delivery Contract 1.0
=
Response Contract 1.0
```

salvo decisión explícita.

---

## 14.72 Gateway Contract Mapper

Podrá existir:

```text
GatewayResponseMapper
```

responsable de transformar DeliveryResult en respuesta HTTP.

No deberá alterar la respuesta cognitiva.

---

## 14.73 Mapper ejemplo

```text
DeliveryResult:
status = DELIVERED
payload = ...

      ↓

HTTP:
200
application/json
payload
```

---

## 14.74 Error mapper ejemplo

```text
DeliveryResult:
status = REJECTED
error.code = DELIVERY_NOT_AUTHORIZED

      ↓

HTTP:
403
error payload
```

---

## 14.75 No reverse semantic mapping

El Gateway no deberá interpretar:

```text
section margin
```

para decidir HTTP status.

---

## 14.76 Gateway y CORS

Si Portal y Gateway se sirven desde orígenes distintos, CORS deberá configurarse en Gateway.

No en Delivery.

---

## 14.77 CORS policy

Deberá utilizar allowlist de orígenes cuando corresponda.

No:

```text
allow all
```

por defecto en producción sin justificación.

---

## 14.78 CSRF

Si se utilizan cookies para autenticación y operaciones mutables, deberá considerarse protección CSRF.

No forma parte de Delivery.

---

## 14.79 Authentication token

Si se utilizan bearer tokens:

```text
Authorization: Bearer ...
```

Gateway deberá procesarlos.

Delivery deberá recibir solamente identidad/contexto autorizado.

---

## 14.80 No token propagation in payload

Los tokens no deberán entrar al DeliveryEnvelope.

---

## 14.81 Rate limiting

Gateway podrá implementar:

```text
rate limiting
```

para proteger HEYTI.

No pertenece a Delivery.

---

## 14.82 Quotas

Podrán existir quotas por consumidor.

También pertenecen al borde externo.

---

## 14.83 Request size limits

Gateway deberá controlar tamaño máximo de request.

Delivery podrá controlar tamaño de response payload.

---

## 14.84 Response size limits

DeliveryPolicy/adapter podrán definir límites de salida.

Gateway podrá aplicar límites técnicos adicionales.

---

## 14.85 Compression

Gateway podrá aplicar:

```text
gzip
brotli
```

a HTTP responses.

No deberá modificar Delivery semantics.

---

## 14.86 TLS termination

TLS podrá terminar en Gateway o infraestructura frontal.

HEYTI Core no deberá conocer certificados directamente salvo configuración del adapter.

---

## 14.87 Reverse proxy

Una arquitectura productiva podría utilizar:

```text
Nginx
Traefik
cloud gateway
```

delante de HEYTI.

Esto no deberá alterar HRRD.

---

## 14.88 Gateway health endpoints

El Gateway podrá exponer:

```text
/health
```

sin involucrar Delivery completo.

---

## 14.89 HEYTI health capability

La capability `health_check` del Core es conceptualmente distinta de un health endpoint de infraestructura.

No deberán confundirse.

---

## 14.90 Gateway readiness

Readiness puede indicar:

- Runtime cargado;
- adapters registrados;
- contratos disponibles.

Esto podrá ayudar en despliegue futuro.

---

## 14.91 Gateway and AdapterRegistry

Gateway no deberá registrar adapters ad hoc durante cada request.

Los adapters deberán estar listos desde bootstrap.

---

## 14.92 Gateway and ConsumerRegistry

Gateway podrá usar ConsumerRegistry para validar consumidores externos.

Pero Delivery sigue siendo responsable de compatibilidad de entrega.

---

## 14.93 Gateway and CapabilityRegistry

Gateway no deberá invocar directamente implementaciones de capabilities específicas.

Debe delegar a Runtime.

---

## 14.94 Gateway routing vs Capability routing

Debe distinguirse:

```text
HTTP route resolution
```

de:

```text
Capability resolution
```

El primero pertenece a Gateway.

El segundo al Runtime/Capability Registry.

---

## 14.95 Example incorrect architecture

```text
POST /describe-section
      ↓
controller imports DescribeSectionImplementation
      ↓
calls provider directly
      ↓
returns dict
```

Este patrón acopla Gateway a capability concreta.

---

## 14.96 Preferred architecture

```text
HTTP Request
      ↓
Gateway
      ↓
HEYTI Request
      ↓
Runtime
      ↓
Capability Registry
      ↓
Capability
      ↓
Materialization
      ↓
Delivery
      ↓
Gateway Response
```

---

## 14.97 Generic HEYTI Query Gateway

A largo plazo podrá existir una entrada más genérica para "Pregúntale a HEYTI".

El Gateway deberá permitir que Runtime determine la capability apropiada según arquitectura futura.

No deberá codificarse prematuramente.

---

## 14.98 Transitional endpoints

Durante implementación pueden existir endpoints específicos de prueba.

Ejemplo:

```text
/describe-section
```

pero deberán considerarse adaptadores temporales o de integración.

No arquitectura definitiva necesariamente.

---

## 14.99 Integration harness

Antes de Portal podrá utilizarse un harness de API para probar:

```text
request
response
delivery contract
```

---

## 14.100 Contract tests Gateway ↔ Delivery

Deberán existir pruebas que confirmen:

```text
Gateway receives valid DeliveryResult
```

y:

```text
maps it without semantic loss
```

---

## 14.101 Contract tests Gateway ↔ Consumer

Deberán probarse respuestas JSON desde la perspectiva del consumidor.

---

## 14.102 No browser required for Gateway tests

Las pruebas del Gateway no deberán requerir UI completa.

Podrán utilizar un cliente de pruebas HTTP.

---

## 14.103 Portal tests later

Las pruebas del Portal deberán verificar:

```text
consumer receives contract
consumer adapter parses it
presentation renders it
```

como una frontera separada.

---

## 14.104 Gateway unit tests

Ejemplos:

```text
test_gateway_maps_delivered_result_to_success
test_gateway_maps_rejected_result
test_gateway_maps_failed_result
test_gateway_preserves_request_id
```

---

## 14.105 Security tests

```text
test_unauthorized_request_rejected
test_invalid_consumer_rejected
test_sensitive_error_details_not_exposed
```

---

## 14.106 Contract tests

```text
test_gateway_response_matches_delivery_schema
test_gateway_does_not_drop_required_fields
```

---

## 14.107 Trace tests

```text
test_request_id_propagates_end_to_end
test_delivery_id_returned_when_available
```

---

## 14.108 Integration test conceptual

```text
Test Client
   ↓
Gateway
   ↓
Runtime
   ↓
DescribeSection
   ↓
Materialization
   ↓
Delivery
   ↓
Gateway
   ↓
JSON
```

La prueba deberá confirmar:

```text
status
response_id
delivery_id
content
trace
```

---

## 14.109 InMemory before HTTP

Antes de construir Gateway externo deberá verificarse primero:

```text
MaterializedResponse
      ↓
Delivery
      ↓
InMemory Adapter
      ↓
DeliveryResult
```

Una vez estable, se integra el Gateway.

---

## 14.110 Gateway MVP

El primer Gateway podrá ser mínimo.

Responsabilidades:

```text
receive request
create context
invoke runtime
return delivery payload
map errors
```

No deberá incluir lógica visual.

---

## 14.111 Technology choice later

La tecnología concreta del Gateway podrá ser:

```text
FastAPI
Flask
another framework
```

según decisión de implementación.

Este documento no fija aún la tecnología.

---

## 14.112 Python compatibility

La selección deberá ser compatible con:

- Python actual del Core;
- modelo de dependencias;
- testing;
- deployment.

---

## 14.113 Avoid framework-driven architecture

La arquitectura no deberá diseñarse "como diga FastAPI" o cualquier framework.

El framework deberá adaptarse al contrato HEYTI.

---

## 14.114 Hexagonal relation

Conceptualmente:

```text
External World
      ↓
Gateway Adapter
      ↓
Port
      ↓
HEYTI Core
      ↓
Delivery Port
      ↓
Gateway Adapter
      ↓
External World
```

Esto mantiene el Core independiente.

---

## 14.115 Gateway Port

Podrá existir conceptualmente un port de entrada:

```text
HeytiRuntimePort
```

o equivalente.

No deberá crearse sin revisar la arquitectura existente del Runtime.

---

## 14.116 Outbound Delivery Port

Response Delivery ya representa la frontera de salida.

El Gateway podrá ser uno de sus adaptadores.

---

## 14.117 Return adapter as primary UI bridge

Para la primera interfaz visual, el adapter más útil probablemente será un mecanismo de retorno síncrono a Gateway.

Esto minimiza complejidad.

---

## 14.118 UI workflow

La secuencia futura podría ser:

```text
User asks HEYTI
      ↓
Portal/UI sends request
      ↓
Gateway
      ↓
Runtime
      ↓
Response Delivery
      ↓
Gateway JSON
      ↓
UI Adapter
      ↓
Text + KPIs + Map + Chart
```

---

## 14.119 Presentation begins after Gateway response

Una vez que el consumidor recibe JSON:

```text
Delivery responsibility ends
```

y:

```text
Presentation begins
```

---

## 14.120 UI failure after valid response

Si el Portal recibe correctamente pero falla Chart.js:

```text
Gateway = SUCCESS
Delivery = DELIVERED
Presentation = FAILED
```

Esta separación deberá conservarse.

---

## 14.121 Gateway failure after Delivery

En un modelo de retorno síncrono, si Delivery produce un resultado válido pero Gateway falla al escribir la respuesta de red, deberá distinguirse el punto de fallo.

Puede requerir una semántica especial porque aún no se confirmó entrega externa.

---

## 14.122 Delivery finality and Gateway

Por ello, cuando Gateway forma parte del cruce real de frontera, el criterio de `DELIVERED` deberá alinearse con el adapter correspondiente.

No deberá marcarse éxito antes de que el adapter haya completado su responsabilidad.

---

## 14.123 GatewayResponseAdapter success criterion

Podrá ser:

```text
payload accepted by Gateway response mechanism
```

o, dependiendo de implementación:

```text
response successfully written
```

La definición deberá ser precisa.

---

## 14.124 Network acknowledgement limits

Incluso una respuesta HTTP escrita correctamente no garantiza que el usuario la haya leído.

La semántica de `DELIVERED` deberá limitarse a evidencia técnica disponible.

---

## 14.125 No user-read semantics

Queda prohibido interpretar:

```text
DELIVERED
```

como:

```text
USER_READ
```

Son eventos distintos.

---

## 14.126 Read receipts future

Si en el futuro la UI envía confirmación de visualización, eso constituirá otro evento.

No parte del DeliveryResult inicial.

---

## 14.127 Consumer acknowledgement future

Podrá existir:

```text
ACK
```

como evento separado en WebSocket.

No deberá mezclarse prematuramente.

---

## 14.128 External exposure policy

Gateway deberá exponer solamente campos públicos del Delivery Contract.

No estructuras internas.

---

## 14.129 Internal object leakage prohibited

Queda prohibido serializar:

```text
__dict__
```

de objetos internos indiscriminadamente.

---

## 14.130 Public schema

El Gateway deberá utilizar la representación pública validada.

---

## 14.131 API documentation

Cuando exista API, deberá documentarse mediante un contrato verificable.

OpenAPI podría ser útil si se utiliza FastAPI u otra tecnología compatible.

No es requisito de HRRD.

---

## 14.132 OpenAPI as projection

OpenAPI sería una documentación del Gateway.

No reemplaza Delivery Contract.

---

## 14.133 Gateway version governance

Cualquier cambio de API deberá revisar impacto en:

- consumidores;
- Delivery Contract;
- adapters.

---

## 14.134 Gateway deprecation

Los endpoints podrán deprecarse sin modificar HEYTI Core si los adapters mantienen contratos.

---

## 14.135 Portal migration

Esto permitirá migrar gradualmente:

```text
existing HTML modules
      ↓
HEYTI-integrated Portal
      ↓
future unified HEYTI UI
```

sin reescribir cognición.

---

## 14.136 Coexistencia

Durante transición, podrán coexistir:

```text
legacy module data access
```

y:

```text
HEYTI Gateway responses
```

La migración deberá ser controlada y auditable.

---

## 14.137 No big-bang rewrite

La arquitectura no exige reescribir todos los módulos durante este Sprint.

La integración puede ser progresiva.

---

## 14.138 First vertical slice

Una estrategia futura adecuada será integrar primero:

```text
DescribeSection
```

como vertical slice completo:

```text
Portal
→ Gateway
→ Runtime
→ DescribeSection
→ Materialization
→ Delivery
→ Portal
```

---

## 14.139 Vertical slice value

Esto permitirá validar:

- contratos;
- datos;
- mapas;
- KPIs;
- UI;
- trazabilidad;
- errores.

Antes de expandir a otras capabilities.

---

## 14.140 Gateway and six modules

La futura capa Gateway deberá permitir que respuestas HEYTI alimenten:

- Análisis Territorial;
- Ganar Todo;
- Campo;
- Día D;
- ET-27;
- Socioeconómico.

Sin que cada módulo defina un protocolo incompatible.

---

## 14.141 Unified contract

La prioridad deberá ser:

```text
one coherent HEYTI delivery model
```

con adaptadores de Presentation por módulo.

---

## 14.142 Module-specific endpoint caution

Podrán existir endpoints especializados, pero deberán reutilizar el mismo modelo contractual.

---

## 14.143 Gateway and data-source audit

Cuando comience integración visual real, deberá verificarse que cada módulo posea las fuentes necesarias para responder correctamente.

Gateway no deberá esconder vacíos de datos.

---

## 14.144 Missing data

Si una capability determina datos incompletos:

```text
response warnings
```

deberán llegar intactos al consumidor.

Gateway no deberá eliminarlos.

---

## 14.145 Gateway and honest incompleteness

Una respuesta parcial puede producir:

```text
HTTP 200
```

si técnicamente fue una respuesta válida y el contrato marca:

```text
response.status = PARTIAL
```

La semántica cognitiva permanece en el payload.

---

## 14.146 HTTP code not cognitive status

Debe preservarse:

```text
HTTP status
      ≠
Cognitive response status
```

---

## 14.147 Example

```text
HTTP 200
delivery.status = DELIVERED
response.status = PARTIAL
warnings = [...]
```

es completamente válido.

---

## 14.148 Gateway and user-facing message

La UI podrá presentar:

> HEYTI encontró información parcial.

Gateway no deberá generar esa redacción salvo que pertenezca al contrato de error externo.

---

## 14.149 Gateway resilience

El Gateway deberá ser delgado y robusto.

Cuanto menos lógica de negocio contenga, más fácil será sustituirlo.

---

## 14.150 Gateway substitution test

La arquitectura deberá superar:

> Si se sustituye FastAPI por otra tecnología, ¿HEYTI Core continúa funcionando?

La respuesta requerida será:

```text
YES
```

---

## 14.151 Protocol substitution test

También:

> Si el consumidor deja HTTP y usa WebSocket, ¿deben cambiar capabilities?

Respuesta:

```text
NO
```

---

## 14.152 Portal substitution test

Y:

> Si el Portal actual desaparece, ¿Delivery Contract sigue siendo válido?

Respuesta:

```text
YES
```

---

## 14.153 Gateway tests without UI

El Gateway deberá poder probarse sin navegador.

---

## 14.154 Delivery tests without Gateway

Delivery deberá poder probarse sin Gateway mediante InMemory Adapter.

---

## 14.155 Separation test

Esto produce una prueba poderosa:

```text
Delivery works without Gateway.
Gateway works with mocked Runtime/Delivery.
UI works with mocked Gateway payload.
```

Cada frontera puede validarse de forma aislada.

---

## 14.156 Architecture package boundary

La futura implementación podría organizarse conceptualmente:

```text
src/heyti/
├── runtime/
├── materialization/
├── delivery/
└── gateway/
```

si la arquitectura real del repositorio lo justifica.

No deberá crearse esta estructura sin auditoría previa.

---

## 14.157 No gateway code in delivery package

Queda recomendado evitar:

```text
delivery/http_routes.py
```

si esas rutas pertenecen a Gateway.

---

## 14.158 No delivery code in portal

De igual forma, el Portal no deberá reconstruir Delivery semantics por su cuenta.

Podrá interpretar el contrato.

---

## 14.159 Gateway dependency direction

La dirección deberá ser:

```text
Gateway
  depends on
Core public ports/contracts
```

No:

```text
Core
  depends on
Gateway framework
```

---

## 14.160 Framework imports

Idealmente, módulos centrales de Delivery no deberán importar:

```text
fastapi
flask
starlette
```

---

## 14.161 Gateway module may import framework

La capa Gateway sí podrá hacerlo.

---

## 14.162 Invariantes Gateway/Delivery

Se establecen los siguientes invariantes.

### HRRD-G01 — Gateway Separation

Gateway permanecerá separado de Runtime Response Delivery.

### HRRD-G02 — Protocol Independence

Delivery no dependerá de HTTP, WebSocket u otro protocolo concreto.

### HRRD-G03 — Thin Gateway

Gateway no ejecutará cognición ni materialización.

### HRRD-G04 — Public Contract Only

Gateway expondrá únicamente estructuras públicas autorizadas.

### HRRD-G05 — Request ID Propagation

Los identificadores de entrada deberán preservarse durante el flujo.

### HRRD-G06 — Error Mapping

Gateway mapeará errores de Delivery al protocolo sin alterar su significado.

### HRRD-G07 — No Presentation Logic

Gateway no realizará renderizado visual.

### HRRD-G08 — Security at Boundary

Autenticación y controles de protocolo deberán residir principalmente en Gateway.

### HRRD-G09 — Adapter-Based Exposure

La salida deberá realizarse mediante un adapter o frontera explícita.

### HRRD-G10 — Gateway Substitutability

El Core deberá permanecer funcional aunque cambie la tecnología de Gateway.

---

## 14.163 Pruebas mínimas de conformidad

La futura implementación deberá demostrar:

1. que Delivery funciona sin Gateway;
2. que Gateway puede recibir un DeliveryResult público;
3. que Gateway no importa implementaciones de capabilities específicas;
4. que el request ID se preserva;
5. que errores se mapean correctamente;
6. que datos sensibles no se exponen;
7. que el payload conserva el Delivery Contract;
8. que no existe lógica de Presentation;
9. que el protocolo puede cambiar sin modificar Materialization;
10. que la UI puede consumir respuestas estructuradas sin conocer internals.

---

## 14.164 Flujo consolidado de exposición externa

```text
┌─────────────────────────┐
│ External Consumer       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Gateway                 │
│ Protocol / Security     │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Runtime                 │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Materialization         │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Response Delivery       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Gateway Response Adapter│
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Protocol Response       │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Consumer Presentation   │
└─────────────────────────┘
```

---

## 14.165 Flujo de error externo

```text
Runtime / Delivery
      ↓
DeliveryError
      ↓
DeliveryResult
      ↓
Gateway Error Mapper
      ↓
Protocol Error Response
      ↓
Consumer
      ↓
Presentation
```

---

## 14.166 Flujo de éxito

```text
MaterializedResponse
      ↓
DeliveryEnvelope
      ↓
Serialized Payload
      ↓
Gateway Response Adapter
      ↓
Protocol Response
      ↓
Consumer
      ↓
Presentation
```

---

## 14.167 Criterio de éxito arquitectónico

La frontera Gateway/Delivery será considerada correcta cuando una respuesta pueda atravesar:

```text
Core
→ Delivery
→ Gateway
→ Consumer
```

sin que:

```text
Runtime
Materialization
Capability
HKS
HES
```

conozcan:

```text
HTTP routes
DOM
browser implementation
Leaflet
Chart.js
```

---

## 14.168 Declaración arquitectónica del capítulo

Gateway y Runtime Response Delivery deberán colaborar estrechamente, pero nunca fusionarse conceptualmente.

Gateway representa la frontera externa del sistema.

Delivery representa la frontera interna que formaliza la salida de una respuesta.

El Gateway puede conocer HTTP.

Delivery no necesita conocerlo.

El Gateway puede conocer headers.

Delivery no necesita conocerlos.

El Portal puede conocer DOM, mapas y gráficas.

Ni Gateway ni Delivery deben conocer esos detalles de presentación.

La regla arquitectónica consolidada queda establecida como:

> **HEYTI expondrá sus respuestas hacia el exterior mediante una frontera Gateway desacoplada, alimentada por Runtime Response Delivery a través de contratos públicos y adapters explícitos. El protocolo podrá evolucionar sin alterar la semántica cognitiva ni la arquitectura interna del Core.**

La relación fundamental queda formalizada como:

```text
HEYTI Core
      ↓
Materialization
      ↓
Runtime Response Delivery
      ↓
Gateway / Boundary Adapter
      ↓
External Protocol
      ↓
Consumer
      ↓
Presentation
```

Con esta frontera establecida queda preparada la siguiente dimensión de Runtime Response Delivery:

**seguridad, autorización, privacidad y protección de la frontera de salida.**

---

**Fin del Capítulo 14**


# Capítulo 15. Seguridad, autorización, privacidad y protección de la frontera de salida

## 15.1 Propósito del capítulo

Este capítulo define los principios de **seguridad, autorización, privacidad y protección** aplicables a HEYTI Runtime Response Delivery.

La finalidad es garantizar que una respuesta correctamente producida por HEYTI no sea entregada:

- a un consumidor no autorizado;
- mediante un canal no permitido;
- con información sensible innecesaria;
- con trazabilidad manipulada;
- o bajo condiciones que comprometan la integridad de la respuesta.

Runtime Response Delivery constituye una frontera sensible.

Por ello deberá proteger:

```text
what leaves HEYTI
who receives it
under what authorization
through which adapter
with what context
```

La regla fundamental será:

> **Una respuesta válida cognitivamente no implica automáticamente una entrega autorizada.**

---

## 15.2 Seguridad como dimensión independiente

Debe distinguirse:

```text
Response Validity
      ≠
Delivery Authorization
```

Una respuesta puede ser completamente válida y, sin embargo, no estar autorizada para un consumidor determinado.

Ejemplo:

```text
MaterializedResponse = VALID
Consumer = KNOWN
Authorization = DENIED
```

Resultado:

```text
Delivery = REJECTED
```

---

## 15.3 Seguridad no es Presentation

La seguridad de Delivery deberá resolverse antes de Presentation.

La UI podrá ocultar botones.

Pero la ausencia de un botón no constituye control de seguridad.

Queda prohibido confiar únicamente en:

```text
hidden UI element
disabled button
client-side JavaScript
```

para impedir una entrega no autorizada.

---

## 15.4 Principio Zero Trust en la frontera

Runtime Response Delivery deberá asumir:

> **Toda operación debe demostrar que está permitida antes de cruzar la frontera.**

No deberá asumirse que un consumidor es confiable únicamente porque:

- está dentro de la aplicación;
- pertenece al Portal;
- utiliza una ruta conocida;
- proviene del mismo navegador;
- o ya recibió otra respuesta anteriormente.

---

## 15.5 Authentication

La autenticación responde:

> ¿Quién es el actor o consumidor?

Conceptualmente:

```text
External Actor
      ↓
Authentication
      ↓
principal_id
consumer_id
```

La autenticación deberá ocurrir preferentemente en Gateway o infraestructura especializada.

---

## 15.6 Authorization

La autorización responde:

> ¿Puede este actor realizar esta entrega hacia este consumidor bajo este contexto?

Conceptualmente:

```text
principal_id
consumer_id
delivery_context
policy
      ↓
Authorization Decision
      ↓
ALLOW / DENY
```

---

## 15.7 Authentication no implica Authorization

Debe mantenerse:

```text
authenticated
      ≠
authorized
```

Un actor puede estar correctamente autenticado y aun así no tener permiso para determinada operación.

---

## 15.8 Principal

Se define conceptualmente:

```text
principal_id
```

como la identidad de seguridad del actor asociado a la operación.

Podrá representar:

- usuario;
- servicio;
- proceso;
- sistema interno.

No deberá confundirse con:

```text
consumer_id
```

---

## 15.9 Principal vs Consumer

Ejemplo:

```text
principal_id = USER-001
consumer_id  = AT_PORTAL
```

El primero identifica al actor.

El segundo identifica la superficie lógica que recibe la respuesta.

---

## 15.10 Autorización por política

La autorización deberá estar gobernada por reglas explícitas.

Conceptualmente:

```text
AuthorizationPolicy
├── principal
├── consumer
├── response classification
├── action
└── environment
```

La estructura exacta deberá definirse cuando se implemente seguridad completa.

---

## 15.11 No hardcoded authorization

Queda prohibido un patrón como:

```python
if consumer_id == "AT_PORTAL":
    allow = True
```

sin una política formal.

La identidad del consumidor no equivale a permiso universal.

---

## 15.12 Delivery Security Context

El `DeliveryContext` podrá conservar:

```text
principal_id
consumer_id
session_id
authorization_context
request_origin
```

cuando sea necesario.

No deberá incluir credenciales secretas en el payload público.

---

## 15.13 Credenciales

Credenciales como:

```text
password
token
API key
private key
session secret
```

no deberán formar parte del DeliveryEnvelope.

---

## 15.14 Token handling

Si Gateway utiliza tokens, deberá validarlos y convertirlos a identidad/contexto.

Delivery deberá recibir algo como:

```text
principal_id = PR-001
authorization = ALLOWED
```

en lugar de:

```text
raw_token = ...
```

cuando sea posible.

---

## 15.15 Least Privilege

Runtime Response Delivery deberá operar con el mínimo privilegio necesario.

No deberá recibir acceso directo innecesario a:

```text
database write credentials
HKS administration
Capability Registry mutation
session administration
filesystem unrestricted access
```

---

## 15.16 Read-only preference

Cuando Delivery necesite consultar:

```text
SessionProvider
ConsumerRegistry
AdapterRegistry
```

deberá preferirse acceso de lectura.

---

## 15.17 Security Boundary

Conceptualmente:

```text
MaterializedResponse
      ↓
Delivery Request
      ↓
Security Validation
      ↓
Authorization Decision
      ↓
Authorized?
   ┌──┴──┐
   │     │
  YES    NO
   │     │
   ▼     ▼
Delivery REJECTED
```

---

## 15.18 Security before serialization

Cuando sea posible, la autorización deberá comprobarse antes de producir un payload completo.

Esto evita procesar o exponer información que nunca debió avanzar.

---

## 15.19 Security before adapter

La regla obligatoria será:

```text
Authorization
      ↓
Adapter execution
```

Nunca:

```text
Adapter executes
      ↓
Authorization checked
```

---

## 15.20 DeliveryNotAuthorized

Una operación no autorizada deberá producir un error estructurado.

Ejemplo:

```text
code = DELIVERY_NOT_AUTHORIZED
category = SECURITY
status = REJECTED
```

---

## 15.21 No information leakage

Un rechazo de autorización deberá evitar revelar:

- existencia de datos sensibles;
- estructura interna;
- capabilities restringidas;
- razones internas excesivamente detalladas.

---

## 15.22 Ejemplo

Preferible:

```text
"Delivery not authorized."
```

en lugar de:

```text
"User cannot access section 1481 because internal security group X..."
```

si ese detalle no debe exponerse.

---

## 15.23 Consumer authorization

Un consumidor conocido podrá estar:

```text
registered
compatible
```

pero aún:

```text
not authorized
```

La secuencia deberá distinguir estas dimensiones.

---

## 15.24 Flujo completo de decisión

```text
Consumer exists?
      ↓
YES
      ↓
Consumer compatible?
      ↓
YES
      ↓
Principal authenticated?
      ↓
YES
      ↓
Delivery authorized?
      ↓
YES
      ↓
Delivery
```

Cualquier `NO` deberá producir rechazo apropiado.

---

## 15.25 Privacy by Design

Delivery deberá aplicar privacidad desde el diseño.

La regla será:

> **No entregar información que no sea necesaria para cumplir el contrato y la autorización.**

---

## 15.26 Data Minimization

El payload deberá contener únicamente:

- contenido contractual;
- trazabilidad pública autorizada;
- metadata necesaria;
- evidencia permitida.

No deberá transportar información interna "por si acaso".

---

## 15.27 Ejemplo incorrecto

```json
{
  "response": {...},
  "internal_session_object": {...},
  "database_row": {...},
  "auth_token": "...",
  "debug_state": {...}
}
```

---

## 15.28 Ejemplo correcto

```json
{
  "response": {...},
  "trace": {
    "response_id": "...",
    "delivery_id": "..."
  }
}
```

con la información estrictamente necesaria.

---

## 15.29 Sensitive Data Classification

La arquitectura deberá permitir que determinados campos sean clasificados conceptualmente como:

```text
PUBLIC
INTERNAL
RESTRICTED
SENSITIVE
```

si el sistema lo requiere.

No es obligatorio implementar toda la clasificación en v1.0.

---

## 15.30 Public Projection

El DeliveryEnvelope público deberá ser una proyección segura del estado interno.

Conceptualmente:

```text
Internal Delivery State
      ↓
Public Projection
      ↓
Consumer Payload
```

---

## 15.31 No automatic __dict__ exposure

Queda prohibido serializar objetos internos mediante:

```python
obj.__dict__
```

como estrategia general.

Esto puede exponer campos no contractuales.

---

## 15.32 Allowlist de campos

Deberá preferirse:

```text
explicitly declared public fields
```

sobre:

```text
everything except known secrets
```

---

## 15.33 Evidence privacy

La evidencia podrá contener información sensible.

Delivery deberá respetar el nivel de exposición definido por HES y Materialization.

No deberá asumir que toda evidencia es pública.

---

## 15.34 Evidence reference preferred

Cuando sea suficiente, deberá preferirse:

```text
evidence_id
source_reference
```

en lugar de transportar evidencia completa.

---

## 15.35 Geometry privacy

Algunas geometrías o puntos podrían representar información sensible.

Especialmente datos operativos o de Campo.

Delivery deberá respetar políticas de autorización.

---

## 15.36 Precise location

La ubicación precisa no deberá entregarse automáticamente si el contrato solo requiere una referencia territorial general.

---

## 15.37 Territorial reference minimization

Ejemplo:

```text
section_id = 1481
```

puede ser suficiente.

No siempre es necesario entregar:

```text
exact coordinates
full geometry
personal address
```

---

## 15.38 Field Module sensitivity

Información de Campo puede contener:

- nombres;
- teléfonos;
- ubicaciones;
- observaciones.

La integración futura deberá aplicar controles estrictos.

Runtime Response Delivery no deberá convertir estos datos en payload público sin autorización explícita.

---

## 15.39 Election Day sensitivity

Día D puede contener información operacional sensible.

Los mismos principios deberán aplicarse:

```text
known consumer
+
authorization
+
minimum necessary data
```

---

## 15.40 No security by obscurity

El hecho de que una URL o endpoint no sea visible no constituye control suficiente.

La autorización deberá existir en servidor/Gateway/Core correspondiente.

---

## 15.41 Encryption in transit

Cuando Delivery utilice red, deberá emplearse transporte seguro.

Conceptualmente:

```text
HTTPS
WSS
TLS
```

según protocolo.

---

## 15.42 Encryption responsibility

El cifrado en tránsito será responsabilidad del Gateway, adapter o infraestructura.

No del materializador.

---

## 15.43 No custom cryptography

Queda prohibido implementar criptografía casera dentro de Delivery.

Deberán utilizarse estándares y librerías maduras.

---

## 15.44 Certificate validation

Los adapters productivos deberán validar certificados cuando aplique.

Deshabilitar esta verificación deberá limitarse a ambientes controlados de desarrollo y ser explícito.

---

## 15.45 Encryption at rest

Si Delivery Audit persiste información sensible, el almacenamiento deberá aplicar las políticas de protección correspondientes.

Esto pertenece a infraestructura de persistencia.

---

## 15.46 Secrets Management

Credenciales necesarias por adapters deberán cargarse mediante mecanismos apropiados:

```text
environment variables
secret stores
secure configuration
```

No deberán estar hardcoded.

---

## 15.47 No secrets in Git

Queda prohibido guardar:

```text
API keys
passwords
private tokens
```

en archivos versionados.

---

## 15.48 No secrets in logs

Los logs deberán aplicar redacción o exclusión.

---

## 15.49 Authorization headers

Un adapter HTTP podrá usar un header de autorización.

Ese valor no deberá incluirse en:

```text
DeliveryTrace
public metadata
error payload
```

---

## 15.50 Logging privacy

El logging deberá evitar:

```text
full payload
PII
raw evidence
credentials
```

por defecto.

---

## 15.51 Safe structured logging

Ejemplo:

```json
{
  "delivery_id": "DEL-001",
  "response_id": "RESP-001",
  "consumer_id": "AT_PORTAL",
  "status": "DELIVERED"
}
```

---

## 15.52 Debug logging

En desarrollo podrá habilitarse mayor detalle.

Pero deberá existir una separación clara entre:

```text
debug mode
production mode
```

---

## 15.53 Debug mode no puede exponer secrets

Incluso en debug no deberán registrarse secretos completos.

---

## 15.54 Error privacy

Los errores públicos deberán ser sanitizados.

Ejemplo interno:

```text
ConnectionError to internal-host:9000
```

Público:

```text
DELIVERY_TARGET_UNAVAILABLE
```

---

## 15.55 Stack trace handling

Los stack traces deberán permanecer internos.

---

## 15.56 Security events

Podrán emitirse eventos como:

```text
delivery.authorization.denied
delivery.consumer.unknown
delivery.security.validation.failed
```

si la observabilidad lo requiere.

---

## 15.57 Security logging

Los eventos de seguridad deberán incluir:

```text
delivery_id
principal_id
consumer_id
reason_code
timestamp
```

cuando sea seguro.

---

## 15.58 Audit trail

Los rechazos de autorización importantes deberán poder auditarse.

---

## 15.59 Audit immutability

En una arquitectura madura, los registros de auditoría deberán ser resistentes a modificaciones no autorizadas.

No forma parte obligatoria del código inicial.

---

## 15.60 No payload replay without policy

Una respuesta previamente entregada no deberá poder reenviarse a otro consumidor únicamente porque existe un `response_id`.

Toda nueva entrega deberá pasar de nuevo por autorización.

---

## 15.61 Replay authorization

Ejemplo:

```text
RESP-001
delivered to AT_PORTAL
```

no implica:

```text
authorized to deliver to EXTERNAL_CLIENT
```

---

## 15.62 Delivery replay

Una nueva entrega deberá crear:

```text
new delivery_id
```

y repetir:

```text
consumer validation
authorization
compatibility
```

---

## 15.63 Idempotency security

Las claves de idempotencia no deberán ser predecibles de manera que permitan interferencia entre usuarios o consumidores.

---

## 15.64 Consumer identity spoofing

Un cliente externo no deberá poder declarar arbitrariamente:

```text
consumer_id = ADMIN_CONSUMER
```

y recibir privilegios adicionales.

Gateway deberá resolver o validar la identidad.

---

## 15.65 Trusted consumer identity

El `consumer_id` deberá provenir de:

- configuración;
- autenticación;
- registro;
- integración confiable.

No de input no validado.

---

## 15.66 Principal spoofing

De igual manera:

```text
principal_id
```

no deberá aceptarse directamente desde un campo arbitrario del request sin autenticación.

---

## 15.67 Session security

El `session_id` deberá validarse.

No bastará con que tenga formato correcto.

Cuando sea requerido deberá corresponder a una sesión válida.

---

## 15.68 Session hijacking

La arquitectura futura deberá proteger contra uso de session IDs ajenos.

Esto pertenece principalmente a SessionManager/Gateway.

---

## 15.69 Session fixation

La creación y rotación de sesiones deberá ser responsabilidad de SessionManager.

Delivery no deberá controlar estos mecanismos.

---

## 15.70 Authorization caching

Una decisión de autorización podría cachearse en el futuro.

Pero deberá tener:

- TTL;
- contexto;
- invalidación.

No deberá introducirse en v1.0 sin necesidad.

---

## 15.71 Consumer capability is not permission

Debe reiterarse:

```text
supports GEOMETRY
      ≠
authorized for GEOMETRY
```

---

## 15.72 Content authorization

Una futura política podrá permitir:

```text
TEXT
METRIC
```

pero restringir:

```text
EVIDENCE
GEOMETRY
FIELD_PERSON_DATA
```

según consumidor.

---

## 15.73 Authorization Projection

En escenarios autorizados podrá existir una proyección de datos.

Ejemplo:

```text
Full Response
      ↓
Authorization Projection
      ↓
Permitted Response View
```

Pero deberá ser explícita, versionada y semánticamente segura.

---

## 15.74 No silent redaction of required content

Si un campo obligatorio no puede entregarse por seguridad, la respuesta correcta puede ser:

```text
REJECTED
```

No necesariamente eliminar el campo y enviar una respuesta incompleta.

---

## 15.75 Redaction Contract

Si se requieren redacciones parciales en el futuro, deberá existir un contrato que indique:

```text
field redacted
reason
response completeness
```

No se implementará como simple borrado silencioso.

---

## 15.76 Honest redaction

Un consumidor deberá poder saber que cierta información fue omitida por política cuando sea apropiado.

Ejemplo:

```text
redacted = true
```

si el contrato lo contempla.

---

## 15.77 Authorization before projection

La secuencia adecuada será:

```text
Response
      ↓
Authorization Decision
      ↓
Authorized Projection
      ↓
Delivery
```

---

## 15.78 Security Policy

Podrá existir conceptualmente:

```text
DeliverySecurityPolicy
```

con reglas como:

```text
allowed_consumers
required_principal
allowed_content_types
require_active_session
```

No deberá sobreconstruirse inicialmente.

---

## 15.79 Security Policy vs DeliveryPolicy

Podrán permanecer separadas:

```text
DeliveryPolicy
```

para comportamiento operacional;

```text
SecurityPolicy
```

para permisos.

---

## 15.80 Security policy evaluation

Podrá producir:

```text
AuthorizationResult
```

conceptualmente:

```text
allowed
reason_code
restrictions
```

---

## 15.81 AuthorizationResult

La implementación inicial podrá ser mucho más simple:

```text
bool + error
```

si basta.

La arquitectura deberá preservar la posibilidad de enriquecerla.

---

## 15.82 Secure defaults

Ante ausencia de configuración de seguridad, la regla deberá favorecer:

```text
DENY
```

cuando la operación requiera autorización.

No:

```text
ALLOW
```

por conveniencia.

---

## 15.83 Fail closed

La frontera deberá aplicar:

> **Security failures fail closed.**

Ejemplo:

```text
authorization service unavailable
```

no deberá interpretarse automáticamente como:

```text
authorized
```

---

## 15.84 Fail-open prohibido por defecto

Cualquier política fail-open deberá estar explícitamente aprobada y documentada.

---

## 15.85 Adapter allowlist

Cada consumidor podrá tener una allowlist de adapters autorizados.

Ejemplo:

```text
AT_PORTAL:
- GATEWAY_RETURN
- WEBSOCKET_JSON
```

---

## 15.86 Target allowlist

Los adapters que utilicen endpoints externos deberán resolver únicamente targets autorizados.

---

## 15.87 SSRF protection

No deberá permitirse a input de usuario determinar libremente:

```text
http://arbitrary-host
```

para Delivery.

---

## 15.88 URL validation

Si existe configuración dinámica, deberá validarse:

- esquema;
- hostname;
- puerto;
- allowlist.

---

## 15.89 File Adapter security

Un futuro File Adapter deberá restringir paths.

No deberá permitir traversal:

```text
../../sensitive-file
```

---

## 15.90 Path allowlist

Las rutas permitidas deberán definirse por configuración.

---

## 15.91 Internal Call security

Un InternalCallAdapter deberá invocar únicamente consumidores registrados.

No callbacks arbitrarios proporcionados externamente.

---

## 15.92 Serialization security

El serializer deberá rechazar tipos arbitrarios.

Esto reduce riesgo de ejecutar comportamientos inesperados.

---

## 15.93 No executable payload

Queda prohibido incluir:

```text
Python code
JavaScript code
eval strings
```

como acción ejecutable central.

---

## 15.94 Declarative actions only

Las acciones deberán ser:

```text
declarative
allowlisted
validated
```

Ejemplo:

```text
OPEN_MODULE
SHOW_SECTION
```

---

## 15.95 Consumer action validation

El consumidor deberá validar nuevamente las acciones que recibe.

Defensa en profundidad.

---

## 15.96 No eval in UI

La integración futura no deberá utilizar:

```javascript
eval(response.action)
```

ni mecanismos equivalentes.

---

## 15.97 XSS considerations

Si HEYTI entrega texto que será renderizado en browser, la UI deberá tratarlo como datos.

No HTML ejecutable por defecto.

---

## 15.98 Plain text preference

El contenido narrativo deberá ser entregado preferentemente como texto estructurado.

Si se requiere Markdown o rich text, deberá existir contrato específico y sanitización adecuada.

---

## 15.99 HTML content

No deberá permitirse HTML arbitrario generado por el Core sin una política de sanitización y presentación explícita.

---

## 15.100 Markdown future

Si se utiliza Markdown, la UI deberá renderizarlo mediante una librería segura y sanitización.

Delivery únicamente transportará el contenido.

---

## 15.101 CSP

La Content Security Policy pertenece al Gateway/Portal.

No a HRRD Core.

---

## 15.102 CORS

CORS también pertenece al Gateway.

---

## 15.103 CSRF

CSRF corresponde a la capa web cuando aplique.

---

## 15.104 Rate limiting

Rate limiting pertenece principalmente al Gateway.

Pero sus decisiones pueden formar parte de la trazabilidad de la interacción.

---

## 15.105 Denial of Service

Delivery deberá protegerse de payloads excesivos mediante límites definidos.

---

## 15.106 Payload size limit

Podrá existir:

```text
max_payload_size_bytes
```

en DeliveryPolicy o AdapterPolicy.

---

## 15.107 Collection limits

Podrán establecerse límites a:

```text
number of evidence items
geometry size
table rows
series length
```

si existe riesgo operacional.

---

## 15.108 No silent truncation

Si un límite se supera, la respuesta no deberá truncarse silenciosamente.

Deberá existir:

```text
error
projection policy
pagination
reference-based delivery
```

según caso.

---

## 15.109 Geometry size

Las geometrías territoriales pueden ser grandes.

Deberá preferirse:

```text
reference
```

cuando el consumidor ya dispone de la geometría.

---

## 15.110 Evidence size

La evidencia extensa también puede entregarse mediante referencias.

---

## 15.111 Timeouts as security

Los timeouts reducen riesgo de agotamiento de recursos.

---

## 15.112 Resource quotas

En el futuro podrán existir:

```text
max concurrent deliveries
```

por consumidor.

No es requisito v1.0.

---

## 15.113 Concurrency isolation

Una operación no deberá poder acceder al contexto mutable de otra.

---

## 15.114 Context leakage

Deberán probarse explícitamente escenarios concurrentes para evitar fuga de:

```text
session_id
principal_id
consumer_id
```

---

## 15.115 Secure identifiers

IDs como `delivery_id` deberán ser suficientemente difíciles de adivinar si se exponen externamente y si la adivinación crea riesgos.

UUID/ULID pueden ser apropiados.

---

## 15.116 Identifier authorization

Conocer un:

```text
response_id
```

no deberá otorgar acceso a la respuesta.

Toda recuperación futura deberá verificar autorización.

---

## 15.117 IDOR protection

La arquitectura deberá evitar vulnerabilidades de referencia directa insegura.

Ejemplo:

```text
GET /response/RESP-001
```

no deberá devolver datos solo porque el ID existe.

---

## 15.118 Audit access

Las herramientas de auditoría también deberán tener autorización.

---

## 15.119 Audit data sensitivity

Los registros de auditoría pueden contener:

- IDs;
- timestamps;
- consumer;
- principal;
- error codes.

Deberán protegerse adecuadamente.

---

## 15.120 Retention

La retención de traces y auditoría deberá definirse mediante política.

No todos los datos deberán conservarse indefinidamente.

---

## 15.121 Data deletion

Si ciertas regulaciones o políticas requieren borrado, la arquitectura de auditoría deberá contemplarlo sin destruir evidencias obligatorias de manera indebida.

Esta gobernanza deberá definirse posteriormente.

---

## 15.122 Integrity

Delivery deberá preservar integridad del payload.

Una vez serializado, no deberá modificarse silenciosamente antes de transporte.

---

## 15.123 Payload mutation

El Adapter deberá tratar el payload como read-only.

---

## 15.124 Integrity checks

En el futuro podrá utilizarse:

```text
payload_hash
```

para verificar integridad.

No deberá implementarse hasta tener canonicalización formal.

---

## 15.125 Signatures

Firmas digitales podrían ser útiles en integraciones externas de alta seguridad.

No forman parte del MVP.

---

## 15.126 Anti-tampering

La arquitectura deberá permitir incorporar mecanismos de integridad sin modificar la semántica cognitiva.

---

## 15.127 Secure serialization

La serialización deberá evitar:

- ejecución de objetos;
- loaders inseguros;
- formatos que permitan código arbitrario.

JSON es adecuado inicialmente por esta razón.

---

## 15.128 No pickle across trust boundary

Queda desaconsejado utilizar:

```text
pickle
```

como formato de Delivery externo.

---

## 15.129 Deserialization security

El consumidor deberá validar schema antes de confiar en estructuras recibidas.

---

## 15.130 Consumer trust boundary

Aunque HEYTI produzca el payload, una UI robusta deberá validar:

- tipos;
- campos;
- acciones.

Especialmente si en el futuro existen intermediarios.

---

## 15.131 Security and versioning

Una versión contractual vulnerable podrá necesitar deprecación urgente.

El modelo de versionado deberá permitir bloquearla.

---

## 15.132 Consumer deprecation

Un consumidor antiguo que no soporte controles nuevos podrá ser deshabilitado.

---

## 15.133 Adapter deprecation

De igual manera, un adapter inseguro podrá retirarse sin cambiar capabilities.

---

## 15.134 Security review for new adapter

Agregar un adapter nuevo deberá incluir revisión de:

- authentication;
- authorization;
- target validation;
- timeout;
- TLS;
- secret handling;
- logging;
- error exposure.

---

## 15.135 Security review for new Consumer

Agregar un consumidor deberá revisar:

- identidad;
- perfil;
- autorización;
- datos permitidos;
- Content Types;
- acciones permitidas.

---

## 15.136 Security review for new Content Type

Agregar un tipo como:

```text
HTML
FILE
GEOMETRY
ACTION
```

deberá evaluar riesgos específicos.

---

## 15.137 File delivery

Si en el futuro se entregan archivos, deberá controlarse:

- tipo;
- tamaño;
- nombre;
- path;
- contenido;
- autorización.

---

## 15.138 Binary content

Contenido binario deberá utilizar un contrato separado o referencias cuando corresponda.

No deberá introducirse arbitrariamente dentro de JSON.

---

## 15.139 URLs

Si HEYTI entrega URLs, deberán ser tratadas como datos.

El consumidor deberá validar esquemas permitidos.

---

## 15.140 URL scheme allowlist

Ejemplo:

```text
https
```

podrá estar permitido.

No:

```text
javascript:
```

---

## 15.141 Security events and EventBus

En el futuro podrán emitirse:

```text
security.delivery.denied
security.consumer.invalid
```

al EventBus.

No deberán contener secretos.

---

## 15.142 Security metrics

Podrán medirse:

```text
delivery_authorization_denied_total
unknown_consumer_total
invalid_session_total
```

---

## 15.143 Repeated denial detection

Una tasa anómala de rechazos podría indicar:

- configuración incorrecta;
- abuso;
- ataque.

---

## 15.144 No auto-blocking in Delivery v1.0

La respuesta automática a abuso deberá pertenecer al Gateway o seguridad.

Delivery no deberá implementar bloqueo dinámico arbitrario inicialmente.

---

## 15.145 Security testing

La seguridad deberá probarse, no solamente documentarse.

---

## 15.146 Test: unauthorized consumer

```text
test_unauthorized_consumer_is_rejected
```

---

## 15.147 Test: known but unauthorized

```text
test_known_consumer_without_permission_is_rejected
```

---

## 15.148 Test: no adapter execution

```text
test_unauthorized_delivery_does_not_execute_adapter
```

---

## 15.149 Test: sensitive metadata

```text
test_sensitive_internal_metadata_not_serialized
```

---

## 15.150 Test: secret redaction

```text
test_tokens_not_present_in_logs_or_public_error
```

---

## 15.151 Test: session security

```text
test_invalid_required_session_is_rejected
```

---

## 15.152 Test: consumer spoofing

```text
test_untrusted_consumer_id_cannot_elevate_permissions
```

cuando Gateway implemente esa frontera.

---

## 15.153 Test: payload mutation

```text
test_adapter_does_not_mutate_payload
```

---

## 15.154 Test: action safety

```text
test_unknown_action_is_rejected
test_executable_code_action_is_not_allowed
```

---

## 15.155 Test: HTML safety

Si se introduce rich text:

```text
test_unsafe_html_not_accepted_without_explicit_contract
```

---

## 15.156 Test: geometry authorization

Cuando aplique:

```text
test_restricted_geometry_not_delivered_to_unauthorized_consumer
```

---

## 15.157 Test: field personal data

Cuando Campo sea integrado:

```text
test_personal_field_data_requires_explicit_authorization
```

---

## 15.158 Security and zero omission

La disciplina de cero omisiones también aplica a seguridad.

No deberá omitirse:

- autorización;
- validación;
- sanitización;
- trazabilidad de rechazos.

---

## 15.159 Security failure isolation

Un rechazo de seguridad deberá conservar:

```text
MaterializedResponse = VALID
Delivery = REJECTED
```

La respuesta cognitiva no se modifica.

---

## 15.160 Security error example

```text
MaterializedResponse
      ↓
Consumer = AT_PORTAL
      ↓
Principal = PR-001
      ↓
Authorization = DENIED
      ↓
DeliveryError
    code = DELIVERY_NOT_AUTHORIZED
    category = SECURITY
      ↓
DeliveryResult
    status = REJECTED
```

---

## 15.161 Authorized flow example

```text
MaterializedResponse
      ↓
Consumer = AT_PORTAL
      ↓
Principal authenticated
      ↓
Consumer compatible
      ↓
Authorization = ALLOW
      ↓
Serialize
      ↓
Adapter
      ↓
DELIVERED
```

---

## 15.162 Public projection example

Internal state:

```text
delivery_id
response_id
principal_id
authorization_details
adapter_secret
internal_node
response
```

Public:

```text
delivery_id
response_id
response
```

según política.

---

## 15.163 Privacy boundary

Conceptualmente:

```text
Internal Delivery State
      ↓
Security / Privacy Projection
      ↓
Public Delivery Envelope
      ↓
Consumer
```

---

## 15.164 Projection order

La arquitectura deberá decidir con cuidado la relación entre:

- autorización;
- proyección;
- serialización.

Una secuencia segura será:

```text
Authorize
      ↓
Build authorized public projection
      ↓
Validate projection
      ↓
Serialize
      ↓
Deliver
```

---

## 15.165 No post-serialization redaction

Deberá evitarse construir un payload completo con datos sensibles y después borrarlos mediante reemplazos textuales.

La proyección segura deberá ocurrir antes.

---

## 15.166 Security Context immutability

Campos como:

```text
principal_id
authorization decision
consumer_id
```

deberán permanecer estables durante una operación.

---

## 15.167 Time-of-check/time-of-use

En operaciones largas podría ocurrir que permisos cambien después de autorización.

Para v1.0 síncrono y corto deberá bastar la verificación al inicio.

---

## 15.168 Future high-risk revalidation

Operaciones de alto riesgo futuras podrían requerir revalidación antes del boundary crossing.

No deberá imponerse sin necesidad.

---

## 15.169 Consumer session binding

La arquitectura podrá requerir en el futuro que:

```text
session_id
```

esté asociado con:

```text
principal_id
consumer_id
```

Esto pertenecerá al modelo de seguridad de SessionManager/Gateway.

---

## 15.170 Security and observability

Los eventos deberán ser suficientemente informativos para detectar fallos sin convertirse en filtración de datos.

---

## 15.171 Security and audit separation

Los registros de seguridad podrán tener una política de retención distinta de logs normales.

---

## 15.172 Security posture for v1.0

La primera versión deberá implementar al menos los fundamentos:

```text
explicit consumer
validated context
no secrets in payload
no secrets in logs
public field allowlist
structured authorization failure
no executable actions
adapter target control
```

---

## 15.173 Security features diferidas

Podrán diferirse, si no son necesarias para el MVP:

```text
fine-grained RBAC
ABAC
payload signing
encryption at field level
distributed authorization service
dynamic consumer handshake
advanced audit retention
```

---

## 15.174 Diferir no significa ignorar

La arquitectura deberá dejar claras estas extensiones para evitar decisiones que las hagan imposibles.

---

## 15.175 Modelo mínimo de autorización v1.0

Conceptualmente podría comenzar con:

```text
consumer known
consumer enabled
session valid when required
operation allowed by static policy
```

Esto es suficiente para demostrar la frontera.

---

## 15.176 Evolución a RBAC

Posteriormente podría existir:

```text
principal
      ↓
role
      ↓
permission
      ↓
delivery authorization
```

si el sistema lo requiere.

---

## 15.177 Evolución a ABAC

También podría existir autorización basada en atributos:

```text
principal
consumer
content classification
environment
territorial scope
```

No forma parte del Sprint 23.

---

## 15.178 No political/business authorization logic in Delivery

La seguridad no deberá confundirse con reglas estratégicas.

Ejemplo incorrecto:

```text
allow response only if margin < 3%
```

Eso no es autorización técnica.

---

## 15.179 Security policy must be domain-appropriate

Si en el futuro existen restricciones territoriales reales por usuario, deberán definirse mediante una política de acceso formal.

No condiciones ad hoc.

---

## 15.180 Invariantes de seguridad y privacidad

Se establecen los siguientes invariantes.

### HRRD-SEC01 — Authorization Before Delivery

Ninguna entrega protegida deberá cruzar la frontera sin autorización.

### HRRD-SEC02 — Authentication Is Not Authorization

Una identidad autenticada no implica permiso automático.

### HRRD-SEC03 — Least Privilege

Delivery deberá operar con privilegios mínimos.

### HRRD-SEC04 — Data Minimization

Solo información necesaria y autorizada deberá exponerse.

### HRRD-SEC05 — No Secret Exposure

Credenciales y secretos no deberán formar parte del payload público ni de logs.

### HRRD-SEC06 — Explicit Public Projection

La salida pública deberá construirse a partir de campos autorizados.

### HRRD-SEC07 — Secure Failure

Los fallos de seguridad deberán producir rechazo explícito y seguro.

### HRRD-SEC08 — Fail Closed

La incapacidad para comprobar autorización deberá impedir la entrega cuando esta sea requerida.

### HRRD-SEC09 — Declarative Actions Only

Delivery no transportará código ejecutable como acción.

### HRRD-SEC10 — Security Does Not Mutate Cognition

Un rechazo de seguridad no modifica la respuesta cognitiva original.

---

## 15.181 Prueba de conformidad de seguridad

Una futura implementación deberá demostrar:

1. que consumidores desconocidos son rechazados;
2. que consumidores no autorizados son rechazados;
3. que un rechazo no ejecuta el adapter;
4. que tokens y secretos no aparecen en payload;
5. que información interna no se expone automáticamente;
6. que acciones arbitrarias son rechazadas;
7. que el contexto de seguridad permanece trazable;
8. que la respuesta original permanece intacta;
9. que el sistema falla cerrado cuando autorización obligatoria no puede verificarse;
10. que la seguridad puede probarse sin UI.

---

## 15.182 Prueba de privacidad

Dada una respuesta que contenga datos internos no públicos:

```text
Internal Response State
      ↓
Public Projection
```

el payload final deberá contener únicamente los campos autorizados.

---

## 15.183 Prueba de minimización

Un consumer que solo necesita:

```text
section_id
summary
metrics
```

no deberá recibir automáticamente objetos completos de:

```text
session
database
runtime
```

---

## 15.184 Prueba de independencia de Presentation

La seguridad deberá funcionar aunque no exista browser.

---

## 15.185 Prueba de independencia de transporte

La misma política de autorización deberá poder aplicarse tanto con:

```text
IN_MEMORY
```

como con:

```text
HTTP_JSON
```

sin cambiar sus principios.

---

## 15.186 Arquitectura consolidada de seguridad

```text
┌──────────────────────────────┐
│ MaterializedResponse         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DeliveryRequest              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Consumer Validation          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Session / Principal Context  │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ Authorization Policy         │
└──────────────┬───────────────┘
               │
         ┌─────┴─────┐
         │           │
       ALLOW        DENY
         │           │
         ▼           ▼
┌────────────────┐ ┌─────────────────┐
│ Public         │ │ DeliveryResult  │
│ Projection     │ │ REJECTED        │
└───────┬────────┘ └─────────────────┘
        │
        ▼
┌──────────────────────────────┐
│ Validate / Serialize         │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│ DeliveryAdapter              │
└──────────────┬───────────────┘
               │
               ▼
           Consumer
```

---

## 15.187 Criterio de éxito arquitectónico

La seguridad de Runtime Response Delivery será considerada adecuada cuando HEYTI pueda responder, para cada operación protegida:

```text
Who initiated it?
Which consumer receives it?
Was the consumer known?
Was the operation authorized?
What information was allowed to leave?
Which adapter was used?
Was any sensitive information exposed?
What happened if authorization failed?
```

sin depender de controles exclusivamente visuales.

---

## 15.188 Declaración arquitectónica del capítulo

Runtime Response Delivery constituye una frontera de confianza.

Por ello, una respuesta no deberá abandonar HEYTI únicamente porque exista y sea técnicamente serializable.

La salida deberá estar controlada por identidad, contexto, autorización, minimización de datos y políticas explícitas.

La seguridad no podrá delegarse al Portal.

La privacidad no podrá depender de ocultar campos mediante CSS.

Los adapters no podrán elegir libremente destinos.

Los errores no deberán revelar internals.

Y conocer un identificador no deberá equivaler a tener permiso sobre la información que representa.

La regla arquitectónica consolidada queda establecida como:

> **Toda respuesta HEYTI deberá cruzar la frontera de Delivery únicamente cuando exista un consumidor identificado, un contexto válido, una autorización suficiente y una proyección pública explícita que contenga solo la información necesaria y permitida. La seguridad deberá fallar cerrada y permanecer independiente de la presentación y del transporte concreto.**

La secuencia fundamental queda formalizada como:

```text
Valid Response
      ↓
Known Consumer
      ↓
Valid Context
      ↓
Authorized Operation
      ↓
Minimal Public Projection
      ↓
Validated Payload
      ↓
Secure Adapter
      ↓
Consumer
```

Con esta dimensión de seguridad establecida queda preparada la siguiente pieza de Runtime Response Delivery:

**versionado, compatibilidad, evolución contractual y política de deprecación.**

---

**Fin del Capítulo 15**


# Capítulo 16. Versionado, compatibilidad, evolución contractual y política de deprecación

## 16.1 Propósito del capítulo

Este capítulo define la estrategia de **versionado, compatibilidad, evolución contractual y deprecación** aplicable a HEYTI Runtime Response Delivery.

La finalidad es garantizar que los contratos de salida puedan evolucionar sin introducir cambios silenciosos, romper consumidores existentes o generar interpretaciones ambiguas.

Runtime Response Delivery deberá permitir que HEYTI evolucione de forma controlada en:

```text
Response Contract
Delivery Contract
Consumer Profile
Serializer
Adapter
Gateway Exposure
```

sin obligar a que todos los componentes cambien simultáneamente.

La regla fundamental será:

> **Toda evolución contractual deberá ser explícita, versionada, compatible por política y trazable.**

---

## 16.2 Versionar no es numerar archivos

El versionado no deberá reducirse a:

```text
file_v1.py
file_v2.py
```

Versionar significa declarar formalmente:

- qué estructura existe;
- qué significado posee;
- qué cambios incorpora;
- qué consumidores la soportan;
- y qué compatibilidad mantiene.

---

## 16.3 Dimensiones de versión

La arquitectura deberá distinguir varias dimensiones.

Conceptualmente:

```text
response_contract_version
delivery_contract_version
consumer_profile_version
adapter_version
gateway_api_version
knowledge_version
capability_version
```

Estas versiones no deberán confundirse.

---

## 16.4 Response Contract Version

Representa la versión de la estructura materializada.

Ejemplo:

```text
response_contract_version = "1.0"
```

Controla la semántica pública de la respuesta.

---

## 16.5 Delivery Contract Version

Representa la versión del envelope y reglas de Delivery.

Ejemplo:

```text
delivery_contract_version = "1.0"
```

Puede evolucionar independientemente del Response Contract.

---

## 16.6 Consumer Profile Version

Representa la versión de capacidades declaradas por un consumidor.

Ejemplo:

```text
consumer_profile_version = "1.2"
```

No deberá confundirse con la versión del contrato.

---

## 16.7 Adapter Version

Podrá representar una versión técnica de implementación cuando resulte útil para trazabilidad.

No será obligatoria si:

```text
adapter_id
```

es suficiente.

---

## 16.8 Gateway API Version

Un Gateway externo podrá exponer:

```text
/api/v1
```

mientras internamente utiliza:

```text
Delivery Contract 1.0
```

No deberán forzarse a evolucionar al mismo ritmo.

---

## 16.9 Knowledge Version

`knowledge_version` pertenece a la procedencia cognitiva.

No deberá utilizarse como versión de Delivery.

---

## 16.10 Capability Version

`capability_version` identifica la evolución de una capability.

Delivery podrá preservarla en trazabilidad.

No deberá utilizarla para versionar payload.

---

## 16.11 No lockstep obligatorio

La arquitectura deberá evitar:

```text
Response 2.0
requires
Delivery 2.0
requires
API v2
requires
Consumer Profile 2.0
```

salvo que exista una dependencia real.

El desacoplamiento permitirá evolución independiente.

---

## 16.12 Versioning Policy

Deberá existir una política explícita de versionado.

Para v1.0 se recomienda adoptar semántica similar a:

```text
MAJOR.MINOR
```

Ejemplo:

```text
1.0
1.1
2.0
```

---

## 16.13 Cambio MAJOR

Un cambio MAJOR deberá representar una incompatibilidad significativa.

Ejemplos:

```text
remove required field
rename required field
change field meaning
change field type incompatibly
change status semantics
change required content structure
```

Ejemplo:

```text
1.2 → 2.0
```

---

## 16.14 Cambio MINOR

Un cambio MINOR podrá representar una extensión compatible.

Ejemplos:

```text
add optional field
add optional metadata
add optional content type
add new optional error detail
```

Ejemplo:

```text
1.0 → 1.1
```

---

## 16.15 Patch Version

La arquitectura podrá utilizar:

```text
MAJOR.MINOR.PATCH
```

si necesita distinguir correcciones sin cambios contractuales.

Sin embargo, deberá evitarse complejidad innecesaria.

---

## 16.16 Corrección sin cambio contractual

Ejemplo:

```text
serializer bug fixed
```

sin cambiar estructura pública.

No necesariamente requiere nueva:

```text
delivery_contract_version
```

Puede corresponder a versión de implementación.

---

## 16.17 Contract SemVer

La arquitectura podrá inspirarse en Semantic Versioning, pero deberá definir sus propias reglas formales.

No deberá asumir que SemVer de librerías se aplica automáticamente a contratos.

---

## 16.18 Compatibilidad hacia atrás

Se define:

```text
Backward Compatibility
```

como la capacidad de un consumidor antiguo de interpretar una nueva versión compatible.

Ejemplo:

```text
Consumer supports 1.0
Producer emits 1.1
```

podría ser compatible si 1.1 únicamente añade campos opcionales y la política permite ignorarlos.

---

## 16.19 Compatibilidad hacia adelante

Se define:

```text
Forward Compatibility
```

como la capacidad de un consumidor de tolerar elementos futuros desconocidos dentro de límites definidos.

No deberá asumirse automáticamente.

---

## 16.20 Producer Strictness

HEYTI deberá ser estricto respecto de los contratos que produce.

Debe evitar:

```text
unknown fields
invalid types
undocumented semantics
```

---

## 16.21 Consumer Tolerance

Los consumidores podrán tolerar:

```text
unknown optional fields
```

cuando la política lo permita.

Esta combinación puede expresarse como:

```text
Strict Producer
+
Controlled Tolerant Consumer
```

---

## 16.22 Breaking Change

Un cambio deberá considerarse incompatible cuando pueda provocar:

- pérdida de interpretación;
- ambigüedad;
- reinterpretación;
- error estructural;
- ruptura de consumer;
- alteración semántica.

---

## 16.23 Ejemplo de breaking change

Versión 1.0:

```json
{
  "status": "DELIVERED"
}
```

Versión 2.0:

```json
{
  "state": 1
}
```

sin mapping formal.

Esto rompe consumidores.

---

## 16.24 Ejemplo compatible

Versión 1.0:

```json
{
  "status": "DELIVERED"
}
```

Versión 1.1:

```json
{
  "status": "DELIVERED",
  "duration_ms": 14
}
```

si `duration_ms` es opcional.

---

## 16.25 Cambio de significado

Incluso si el nombre y tipo permanecen, cambiar significado constituye breaking change.

Ejemplo:

```text
confidence = 0.8
```

en v1 significa:

```text
probability
```

y en v2 significa:

```text
normalized ranking
```

Esto exige nueva versión MAJOR.

---

## 16.26 Cambio de unidad

Cambiar:

```text
percent 61.4
```

a:

```text
fraction 0.614
```

sin cambiar contrato constituye ruptura semántica.

---

## 16.27 Cambio de null semantics

Cambiar el significado de:

```text
null
```

también puede ser incompatible.

Ejemplo:

v1:

```text
null = unknown
```

v2:

```text
null = zero
```

no deberá ocurrir silenciosamente.

---

## 16.28 Cambio de optionalidad

Cambiar un campo de:

```text
OPTIONAL
```

a:

```text
REQUIRED
```

puede romper producers o consumers y deberá tratarse cuidadosamente.

---

## 16.29 Cambio de required a optional

Puede ser compatible estructuralmente, pero podría cambiar expectativas semánticas.

Debe evaluarse.

---

## 16.30 Version Negotiation

La arquitectura deberá distinguir:

```text
version validation
```

de:

```text
version negotiation
```

v1.0 podrá implementar solamente validación.

---

## 16.31 Política v1.0

Para v1.0:

```text
Runtime selects contract version
Consumer declares support
Delivery validates support
```

No se negociará dinámicamente una versión alternativa.

---

## 16.32 Flujo v1.0

```text
Delivery Contract = 1.0
      ↓
ConsumerProfile
supports = [1.0]
      ↓
VALID
```

---

## 16.33 Flujo incompatible

```text
Delivery Contract = 1.0
      ↓
ConsumerProfile
supports = [2.0]
      ↓
REJECTED
DELIVERY_CONTRACT_MISMATCH
```

---

## 16.34 Negociación futura

En una versión posterior:

```text
Producer supports:
1.0, 1.1

Consumer supports:
1.0
      ↓
select 1.0
```

podría implementarse.

No deberá anticiparse sin necesidad.

---

## 16.35 Contract Registry

La arquitectura podrá utilizar conceptualmente:

```text
ContractRegistry
```

para conocer versiones disponibles.

Ejemplo:

```text
DeliveryContractRegistry
├── 1.0
├── 1.1
└── 2.0
```

---

## 16.36 Registry necessity

No deberá crearse un ContractRegistry si v1.0 solo soporta una versión.

Puede comenzar con una constante explícita.

La arquitectura deberá evitar infraestructura prematura.

---

## 16.37 Current Version

Podrá existir:

```text
CURRENT_DELIVERY_CONTRACT_VERSION = "1.0"
```

si existe una sola versión activa.

---

## 16.38 Supported Versions

Podrá existir:

```text
SUPPORTED_DELIVERY_CONTRACT_VERSIONS = {"1.0"}
```

para validación.

---

## 16.39 Consumer support matrix

Deberá poder conocerse conceptualmente:

| Consumer | Profile | Delivery Contracts |
|---|---:|---|
| AT_PORTAL | 1.0 | 1.0 |
| TEST_CLIENT | 1.0 | 1.0 |
| HEYTI_UI | Future | Future |

---

## 16.40 Compatibility Matrix

La arquitectura deberá poder representar compatibilidad como:

```text
Delivery 1.0 ↔ Consumer Profile X
```

y no asumirla.

---

## 16.41 Serializer compatibility

Un serializer deberá declarar qué versiones soporta.

Ejemplo:

```text
JSONSerializer
supports Delivery 1.0
```

---

## 16.42 Adapter compatibility

Un adapter podrá ser neutral respecto de versión si solo transporta bytes.

Pero deberá declarar limitaciones si existen.

---

## 16.43 Gateway compatibility

Gateway deberá saber mapear versiones expuestas.

No deberá devolver contratos que su API pública no soporta.

---

## 16.44 Multi-version coexistence

En el futuro podrían coexistir:

```text
Delivery 1.0
Delivery 2.0
```

durante una migración.

Esto deberá ser temporal y gobernado.

---

## 16.45 No indefinite version accumulation

La arquitectura no deberá mantener todas las versiones para siempre.

Debe existir deprecación y retiro.

---

## 16.46 Deprecation

Se define **deprecación** como el estado en el que una versión continúa soportada temporalmente pero no debe utilizarse para nuevas integraciones.

Conceptualmente:

```text
ACTIVE
DEPRECATED
RETIRED
```

---

## 16.47 ACTIVE

Una versión `ACTIVE` puede utilizarse normalmente.

---

## 16.48 DEPRECATED

Una versión `DEPRECATED`:

- continúa disponible temporalmente;
- deberá generar advertencia operacional;
- no debería utilizarse para nuevos consumidores;
- tendrá una fecha o criterio de retiro.

---

## 16.49 RETIRED

Una versión `RETIRED` ya no deberá ser aceptada.

Una operación que la solicite deberá resultar:

```text
REJECTED
```

---

## 16.50 Estado de versiones

Conceptualmente:

```text
ContractVersion
├── version
├── status
├── introduced_at
├── deprecated_at?
├── retirement_at?
└── successor?
```

No es obligatorio implementar esta estructura completa desde v1.0.

---

## 16.51 Política de deprecación

La deprecación deberá incluir:

1. anuncio;
2. documentación;
3. periodo de coexistencia;
4. migración de consumidores;
5. pruebas;
6. retiro.

---

## 16.52 No silent retirement

Una versión no deberá desaparecer sin registro.

---

## 16.53 Deprecation Warning

Una operación usando contrato deprecado podrá producir:

```text
delivery warning
```

si la política lo permite.

Ejemplo:

```text
CONTRACT_VERSION_DEPRECATED
```

---

## 16.54 Warning no rompe entrega

Si la versión aún está soportada:

```text
status = DELIVERED
warnings = [deprecated version]
```

podrá ser válido.

---

## 16.55 Retired Version

Si ya está retirada:

```text
REJECTED
DELIVERY_CONTRACT_MISMATCH
```

o código específico si se considera útil.

---

## 16.56 Consumer deprecation

ConsumerProfile también podrá pasar por:

```text
ACTIVE
DEPRECATED
DISABLED
```

---

## 16.57 Adapter deprecation

Un adapter antiguo podrá deprecarse sin cambiar contratos.

Ejemplo:

```text
HTTP_JSON_V1 implementation
```

se sustituye por otra.

---

## 16.58 API deprecation

Gateway podrá deprecar:

```text
/api/v1
```

mientras Core sigue soportando Delivery Contract 1.0.

---

## 16.59 Coordinated Migration

Una migración puede requerir secuencia:

```text
1. Add new contract support
2. Add serializer support
3. Add consumer support
4. Verify integration
5. Mark old version deprecated
6. Migrate traffic
7. Retire old version
```

---

## 16.60 Expand-and-Contract

Se recomienda el patrón:

```text
EXPAND
   add new compatible support
      ↓
MIGRATE
   consumers move
      ↓
CONTRACT
   remove old support
```

Este patrón reduce riesgo.

---

## 16.61 No in-place breaking mutation

Queda prohibido:

```text
modify contract 1.0 semantics
```

para convertirlo silenciosamente en una nueva versión.

---

## 16.62 Schema immutability

Una versión publicada deberá tratarse como:

```text
semantically immutable
```

Las correcciones de documentación pueden ocurrir.

No cambios de significado.

---

## 16.63 Contract fixture immutability

Los test vectors de una versión deberán permanecer estables.

---

## 16.64 Golden payloads

Podrán mantenerse ejemplos canónicos:

```text
delivery_v1_success.json
delivery_v1_failed.json
delivery_v1_rejected.json
```

para detectar regresiones.

---

## 16.65 Contract change review

Todo cambio deberá revisar:

```text
field names
types
requiredness
nullability
semantics
content types
errors
status behavior
```

---

## 16.66 Change Classification

Cada cambio deberá clasificarse como:

```text
NON-CONTRACTUAL
BACKWARD-COMPATIBLE
BREAKING
```

---

## 16.67 NON-CONTRACTUAL

Ejemplos:

```text
internal refactor
performance improvement
logging enhancement
```

No requieren nueva versión contractual.

---

## 16.68 BACKWARD-COMPATIBLE

Ejemplos:

```text
new optional field
new optional metadata
```

Podrían requerir:

```text
minor version
```

---

## 16.69 BREAKING

Ejemplos:

```text
required field removal
type change
meaning change
```

Requieren:

```text
major version
```

---

## 16.70 Changelog

Cada versión deberá documentar cambios.

Conceptualmente:

```text
Delivery Contract Changelog
```

---

## 16.71 Changelog mínimo

Deberá indicar:

```text
version
date
change summary
compatibility
migration impact
```

---

## 16.72 Architecture Decision Record

Cambios importantes podrán requerir un ADR.

Ejemplos:

- cambio de estrategia de versionado;
- incorporación de streaming;
- cambio de semántica de DELIVERED;
- introducción de proyecciones contractuales.

---

## 16.73 No ADR for trivial patch

No todo cambio requiere ADR.

La gobernanza deberá ser proporcional.

---

## 16.74 Consumer migration guide

Un cambio MAJOR deberá incluir guía de migración.

Ejemplo:

```text
1.x → 2.0
```

con:

- campos removidos;
- campos nuevos;
- mapping;
- cambios de comportamiento.

---

## 16.75 Serializer migration

Los serializers deberán mantener soporte paralelo durante la transición si es necesario.

---

## 16.76 Adapter migration

Los adapters que solo transportan payload podrían no requerir cambios.

Esto demuestra desacoplamiento.

---

## 16.77 Gateway migration

Gateway podrá mapear múltiples versiones durante transición.

---

## 16.78 Portal migration

La UI podrá migrar a un nuevo contrato sin modificar Capability.

---

## 16.79 Compatibility Adapter

En el futuro podría existir:

```text
ContractCompatibilityAdapter
```

capaz de convertir:

```text
Response/Delivery v2
→ v1
```

si la transformación es semánticamente segura.

---

## 16.80 Down-conversion

La conversión hacia versión anterior solo deberá permitirse cuando no pierda información obligatoria.

---

## 16.81 Unsafe down-conversion

Si v2 introduce información obligatoria inexistente en v1:

```text
down-conversion
```

podría ser imposible.

La entrega deberá rechazarse.

---

## 16.82 Up-conversion

Convertir v1 a v2 podría requerir información no disponible.

No deberá inventarse.

---

## 16.83 No fabricated defaults

Una conversión no deberá rellenar datos semánticos ausentes con valores inventados.

---

## 16.84 Projection and versioning

Una proyección para consumidor deberá estar asociada a una versión contractual.

---

## 16.85 Versioned Content Types

Un Content Type podrá evolucionar.

Ejemplo:

```text
TABLE v1
```

a una estructura nueva.

La política deberá decidir si esto implica cambio del Delivery Contract completo o sub-schema.

---

## 16.86 Evitar micro-versiones

Debe evitarse versionar cada subobjeto independientemente salvo necesidad real.

Demasiadas versiones aumentan complejidad.

---

## 16.87 Coarse-grained versioning preference

Para v1.0 deberá preferirse:

```text
one Delivery Contract version
```

que gobierne la estructura completa.

---

## 16.88 Response Contract remains separate

El Response Contract podrá evolucionar independientemente si ya posee gobernanza propia.

---

## 16.89 Error codes and versioning

Agregar un nuevo error code puede ser compatible si consumers toleran códigos desconocidos.

Sin embargo, cambiar el significado de un error existente no lo es.

---

## 16.90 Status enum changes

Agregar un nuevo estado terminal como:

```text
UNKNOWN
```

puede romper consumidores con switches exhaustivos.

Deberá evaluarse como cambio potencialmente MAJOR.

---

## 16.91 Enum extensibility

Los consumidores deberán diseñarse para manejar valores desconocidos de forma segura cuando la política lo permita.

---

## 16.92 Unknown enum safe handling

Ejemplo:

```text
unknown status
→ display generic state
→ log compatibility warning
```

pero no asumir `DELIVERED`.

---

## 16.93 Contract strictness

Producer no deberá emitir valores desconocidos dentro de una versión existente.

---

## 16.94 Compatibility tests

Deberán existir pruebas entre versiones.

Ejemplo:

```text
consumer_v1_accepts_delivery_v1_1_optional_extension
```

si la política lo garantiza.

---

## 16.95 Breaking-change tests

Deberá demostrarse que:

```text
consumer_v1 rejects delivery_v2
```

si son incompatibles.

---

## 16.96 Schema diff

En el futuro podrá utilizarse una herramienta de comparación de schemas.

No es obligatorio.

---

## 16.97 Contract snapshot tests

Los snapshots ayudarán a detectar:

```text
accidental field removal
renaming
type change
```

---

## 16.98 Compatibility gate

Una futura CI podrá impedir cambios incompatibles no versionados.

Conceptualmente:

```text
Contract changed?
      ↓
Compatibility check
      ↓
Breaking?
      ↓
Version bumped?
```

---

## 16.99 Zero omission and versioning

La disciplina de cero omisiones exige revisar todo cambio contractual para asegurar que campos obligatorios no desaparecen accidentalmente.

---

## 16.100 Change checklist

Antes de publicar una nueva versión deberá verificarse:

```text
contracts
serializer
validator
consumer profiles
adapter support
gateway mapping
tests
documentation
migration
```

---

## 16.101 Consumer compatibility test

Cada consumidor activo deberá probarse contra la nueva versión antes de activarla.

---

## 16.102 Canary future

En producción avanzada podría activarse una nueva versión para un subconjunto de consumidores.

No es necesario inicialmente.

---

## 16.103 Feature Flags

Podrían utilizarse feature flags para activar nuevas versiones.

Pero deberán evitar crear combinaciones de contrato no auditables.

---

## 16.104 Version flag trace

Si se utiliza un flag, la traza deberá registrar qué versión se seleccionó.

---

## 16.105 Contract selection deterministic

Dado:

```text
consumer
policy
supported versions
```

la versión seleccionada deberá ser determinista.

---

## 16.106 No "latest" magic

Debe evitarse:

```text
use latest version
```

sin definir qué significa.

Preferible:

```text
explicit version
```

---

## 16.107 CURRENT alias

Puede existir internamente:

```text
CURRENT = "1.0"
```

pero deberá resolverse antes de construir la entrega.

La traza deberá registrar:

```text
1.0
```

no:

```text
CURRENT
```

---

## 16.108 API version query

Un Gateway futuro podría recibir:

```text
Accept-Version
```

o usar rutas versionadas.

La selección deberá validarse.

---

## 16.109 Consumer cannot force unsupported version

Si un cliente solicita:

```text
99.0
```

deberá recibir rechazo.

---

## 16.110 Version spoofing

La versión recibida del exterior deberá validarse.

No deberá utilizarse para cargar código arbitrario.

---

## 16.111 Version parser

Las versiones deberán analizarse mediante una regla estricta.

Ejemplo:

```text
^\d+\.\d+$
```

si ese es el formato adoptado.

---

## 16.112 Version normalization

No deberá alternarse entre:

```text
1
1.0
v1
V1
```

sin política.

---

## 16.113 Canonical version string

Para v1.0 se recomienda:

```text
"1.0"
```

como formato canónico.

---

## 16.114 Contract lifecycle

Conceptualmente:

```text
DRAFT
   ↓
ACTIVE
   ↓
DEPRECATED
   ↓
RETIRED
```

---

## 16.115 DRAFT

Una versión en diseño no deberá ser utilizada por consumidores productivos.

---

## 16.116 ACTIVE

Versión estable y soportada.

---

## 16.117 DEPRECATED

Versión soportada temporalmente con migración requerida.

---

## 16.118 RETIRED

Versión no aceptada.

---

## 16.119 Experimental contracts

Podría existir en el futuro:

```text
EXPERIMENTAL
```

pero deberá mantenerse fuera de consumidores críticos.

No es necesario para v1.0.

---

## 16.120 Stable default

La versión por defecto deberá ser `ACTIVE`.

Nunca experimental.

---

## 16.121 Deprecation timeline

Una deprecación deberá tener idealmente:

```text
deprecated_at
retirement_target
```

o criterio equivalente.

---

## 16.122 No arbitrary deadline

La fecha de retiro deberá permitir migración razonable.

---

## 16.123 Urgent security retirement

Una vulnerabilidad crítica puede exigir retiro inmediato.

La seguridad tiene prioridad sobre compatibilidad.

---

## 16.124 Security override

En la jerarquía de decisión:

```text
Security
>
Backward Compatibility
```

cuando exista riesgo real.

---

## 16.125 Deprecation notification

Los consumidores deberán recibir advertencia mediante:

- documentación;
- logs;
- métricas;
- warnings contractuales cuando sea apropiado.

---

## 16.126 No user-facing technical noise

Las advertencias de deprecación no necesariamente deberán mostrarse al usuario final.

Presentation decidirá.

---

## 16.127 Operational warning

Un log podría incluir:

```text
consumer=AT_PORTAL
contract=1.0
warning=DEPRECATED_CONTRACT
```

---

## 16.128 Deprecation metrics

Podrán medirse:

```text
delivery_deprecated_contract_total
```

para saber si aún existe uso.

---

## 16.129 Retirement readiness

Una versión podrá retirarse cuando:

```text
active consumers on old version = 0
```

o según política.

---

## 16.130 Contract inventory

Deberá existir una fuente de verdad que indique:

- versiones activas;
- consumers;
- serializers;
- adapters;
- estado.

Inicialmente puede ser documentación.

---

## 16.131 Documentation architecture

El documento rector deberá mantenerse alineado con:

```text
code
tests
schemas
consumer profiles
```

---

## 16.132 Version drift

Se define `version drift` como la divergencia entre lo documentado y lo implementado.

La arquitectura deberá prevenirlo mediante pruebas y revisión.

---

## 16.133 Source of truth

La versión contractual activa deberá estar declarada en código y documentación de manera consistente.

---

## 16.134 Automated check future

Podrá existir una prueba que verifique:

```text
documentation version
schema version
code constant
```

si resulta práctico.

---

## 16.135 Version traceability

Cada DeliveryResult deberá poder indicar:

```text
delivery_contract_version
```

y preservar:

```text
response_contract_version
```

cuando corresponda.

---

## 16.136 Why trace version?

Porque permite responder:

> ¿Qué interpretación contractual aplicaba cuando ocurrió esta entrega?

---

## 16.137 Historical replay

Si se analiza una entrega antigua, deberá utilizarse la versión que existía entonces.

No la semántica actual.

---

## 16.138 Audit reproducibility

La auditoría debe poder reconstruir una entrega con:

```text
contract version
consumer profile version
adapter identity
```

cuando estén disponibles.

---

## 16.139 Contract migration and audit

Migrar consumidores no deberá reescribir registros históricos.

---

## 16.140 Historical immutability

Un DeliveryResult antiguo:

```text
contract_version = 1.0
```

deberá continuar indicando 1.0 aunque 2.0 sea ahora la versión actual.

---

## 16.141 Serializer historical support

No necesariamente deberá mantenerse código capaz de reserializar todas las versiones antiguas para siempre.

Pero deberán conservarse artefactos suficientes para auditoría.

---

## 16.142 Schema archive

Podrán archivarse schemas históricos.

Ejemplo:

```text
contracts/delivery/1.0.schema.json
contracts/delivery/2.0.schema.json
```

cuando existan schemas formales.

---

## 16.143 No overwrite schema

Un schema publicado no deberá sobrescribirse con semántica diferente manteniendo el mismo número.

---

## 16.144 Example version evolution

### Delivery Contract 1.0

```text
delivery_id
response
trace
consumer_id
adapter_id
status
error?
```

### Delivery Contract 1.1

Podría añadir:

```text
duration_ms?
```

como opcional.

### Delivery Contract 2.0

Podría cambiar una estructura fundamental y requerir migración.

---

## 16.145 Content Type evolution example

Versión 1.0:

```text
metric:
label
value
unit
```

Versión 1.1:

```text
metric:
label
value
unit
description?
```

Compatible si `description` es opcional.

---

## 16.146 Breaking Content Type example

Cambiar:

```text
value: number
```

por:

```text
value: string
```

sin nueva versión MAJOR será inválido.

---

## 16.147 Action evolution

Agregar una nueva acción:

```text
OPEN_MODULE
```

podría ser compatible si las acciones son opcionales y consumers manejan desconocidas.

Si la acción es obligatoria, debe verificarse ConsumerProfile.

---

## 16.148 Error evolution

Agregar un error code nuevo debe acompañarse de una estrategia de fallback para consumidores.

---

## 16.149 Generic error handling

Un consumidor deberá poder manejar un error desconocido de manera segura:

```text
generic delivery error
```

sin interpretarlo como éxito.

---

## 16.150 Versioning and security projections

Una proyección de seguridad que cambie campos públicos podría requerir nueva versión contractual.

---

## 16.151 Versioning and privacy

Eliminar un campo por razones de privacidad puede romper contrato.

En ese caso, la seguridad prevalece, pero el cambio deberá documentarse y versionarse.

---

## 16.152 Versioning and performance

Cambiar solo compresión o encoding técnico no necesariamente cambia Delivery Contract.

---

## 16.153 Versioning and adapter internals

Cambiar librería:

```text
requests → httpx
```

no debería cambiar contrato.

---

## 16.154 Versioning and Gateway framework

Cambiar:

```text
FastAPI → otro framework
```

no deberá cambiar Delivery Contract por sí mismo.

---

## 16.155 Versioning and Portal UI

Cambiar estilos, layout o librerías visuales no afecta contratos salvo que cambien capacidades semánticas soportadas.

---

## 16.156 ConsumerProfile change example

Si Portal añade soporte para:

```text
GEOMETRY
```

su perfil puede evolucionar:

```text
1.0 → 1.1
```

sin cambiar Delivery Contract.

---

## 16.157 ConsumerProfile breaking change

Si Portal deja de soportar un Content Type obligatorio:

```text
TABLE
```

deberá actualizarse perfil y validarse impacto.

---

## 16.158 Adapter capability evolution

Un adapter que agrega streaming podría cambiar su profile técnico sin alterar la entrega síncrona existente.

---

## 16.159 No accidental consumer breakage

Antes de activar un nuevo contrato deberá ejecutarse la suite completa de compatibilidad.

---

## 16.160 Contract Compatibility Test Suite

Deberá incluir:

```text
valid contract accepted
old consumer compatibility
unsupported consumer rejection
serializer support
payload schema validation
gateway mapping
```

---

## 16.161 Regression suite

Las pruebas existentes deberán permanecer verdes.

Una nueva versión no justifica romper arbitrariamente la anterior durante coexistencia.

---

## 16.162 Consumer fixtures

Cada consumidor importante podrá tener fixtures representativos.

---

## 16.163 Golden contract test

Ejemplo:

```text
DescribeSection
      ↓
MaterializedResponse
      ↓
Delivery 1.0
      ↓
expected structure
```

Esto ayudará a detectar drift.

---

## 16.164 Contract change approval

Todo cambio MAJOR deberá pasar revisión arquitectónica explícita.

---

## 16.165 Change proposal

La propuesta deberá indicar:

```text
problem
current contract
proposed contract
breaking changes
migration plan
consumer impact
security impact
test plan
```

---

## 16.166 ADR candidate

Un cambio MAJOR deberá normalmente producir un ADR o equivalente.

---

## 16.167 Contract owner

La arquitectura deberá definir responsabilidad sobre aprobación contractual.

Dentro de HEYTI, esto deberá formar parte de la gobernanza del Core.

---

## 16.168 No consumer-owned core contract

Un consumidor no deberá modificar unilateralmente el Delivery Contract.

---

## 16.169 Feedback loop

Los consumidores podrán solicitar nuevas capacidades.

La decisión deberá evaluarse arquitectónicamente.

---

## 16.170 Avoid UI-driven contract pollution

Ejemplo:

Portal solicita:

```text
card_color
```

Eso no debería añadirse al contrato central si es Presentation.

---

## 16.171 Legitimate contract evolution

Portal solicita:

```text
metric unit
```

porque sin ella el valor es ambiguo.

Esto sí podría justificar evolución semántica.

---

## 16.172 Contract design test

Antes de añadir un campo deberá preguntarse:

> ¿Este campo describe significado o implementación visual?

Si es implementación visual, probablemente no pertenece al Core.

---

## 16.173 Deprecation example

Supóngase:

```text
Delivery Contract 1.0
```

es reemplazado por:

```text
2.0
```

Secuencia:

```text
1. Publish 2.0
2. Support 1.0 + 2.0
3. Migrate TEST_CLIENT
4. Migrate AT_PORTAL
5. Mark 1.0 DEPRECATED
6. Observe remaining usage
7. Retire 1.0
```

---

## 16.174 Retirement example

Después del retiro:

```text
consumer requests 1.0
      ↓
REJECTED
```

---

## 16.175 Version fallback prohibition

No deberá ocurrir:

```text
requested 2.0 unsupported
      ↓
silently send 1.0
```

salvo negociación explícita.

---

## 16.176 Explicit downgrade

Si se permite downgrade:

```text
requested = 2.0
selected = 1.0
```

deberá informarse y trazarse.

---

## 16.177 Version selection trace

DeliveryTrace deberá registrar la versión efectiva.

---

## 16.178 Version mismatch error

Se mantendrá:

```text
DELIVERY_CONTRACT_MISMATCH
```

como error público base.

---

## 16.179 Version detail

Internamente podrán registrarse:

```text
required_version
supported_versions
consumer_profile_version
```

---

## 16.180 Security of version details

No toda lista interna de versiones deberá exponerse al cliente.

---

## 16.181 Invariantes de versionado

Se establecen los siguientes invariantes.

### HRRD-VER01 — Explicit Version

Toda entrega deberá identificar la versión contractual efectiva.

### HRRD-VER02 — Immutable Published Semantics

Una versión publicada no cambiará silenciosamente de significado.

### HRRD-VER03 — Breaking Change Requires Major Evolution

Todo cambio incompatible deberá producir nueva versión MAJOR.

### HRRD-VER04 — Compatibility Is Policy

La compatibilidad deberá definirse y probarse explícitamente.

### HRRD-VER05 — Consumer Support Validation

Ningún consumidor recibirá una versión no soportada.

### HRRD-VER06 — No Silent Downgrade

La selección de una versión alternativa deberá ser explícita.

### HRRD-VER07 — Deprecation Before Retirement

Las versiones deberán retirarse mediante proceso gobernado salvo emergencia de seguridad.

### HRRD-VER08 — Historical Traceability

Las entregas históricas conservarán la versión con la que fueron realizadas.

### HRRD-VER09 — Independent Version Dimensions

Response, Delivery, Consumer y API podrán evolucionar independientemente.

### HRRD-VER10 — Security Overrides Compatibility

Una versión insegura podrá retirarse aun si afecta compatibilidad.

---

## 16.182 Pruebas mínimas de versionado

La implementación deberá incluir pruebas equivalentes a:

```text
test_delivery_contract_version_is_explicit
test_supported_version_is_accepted
test_unsupported_version_is_rejected
test_consumer_profile_version_is_preserved
test_contract_version_survives_serialization
```

---

## 16.183 Pruebas de compatibilidad

```text
test_optional_field_extension_is_compatible
test_required_field_removal_is_not_compatible
test_type_change_is_breaking
test_semantic_change_requires_new_major_version
```

Estas últimas pueden comenzar como pruebas de schema/documentación.

---

## 16.184 Pruebas de deprecación

Cuando se implemente lifecycle:

```text
test_active_version_is_accepted
test_deprecated_version_is_accepted_with_warning
test_retired_version_is_rejected
```

---

## 16.185 Prueba de trazabilidad histórica

Una entrega realizada con:

```text
1.0
```

deberá continuar reportando:

```text
1.0
```

aunque:

```text
CURRENT = 2.0
```

posteriormente.

---

## 16.186 Prueba de Consumer Substitution

Un consumidor nuevo podrá soportar únicamente:

```text
2.0
```

sin exigir modificar respuestas históricas 1.0.

---

## 16.187 Prueba de Adapter Independence

Un cambio de adapter no deberá incrementar Delivery Contract por sí mismo.

---

## 16.188 Prueba de Gateway Independence

Un cambio de API version no deberá modificar Delivery Contract si la semántica sigue igual.

---

## 16.189 Versioning MVP para Sprint 23

Para la implementación inicial se recomienda:

```text
DELIVERY_CONTRACT_VERSION = "1.0"
SUPPORTED_DELIVERY_CONTRACT_VERSIONS = {"1.0"}
```

y validación explícita contra ConsumerProfile.

---

## 16.190 Sin multi-version complexity inicial

No será necesario implementar desde el primer momento:

```text
dynamic negotiation
multiple serializers
downgrade adapters
deprecation registry
```

---

## 16.191 Preparación arquitectónica

Sin embargo, el código deberá evitar hardcodear la versión en múltiples lugares.

Deberá existir una fuente de verdad clara.

---

## 16.192 Fuente de verdad v1.0

Conceptualmente:

```text
delivery/contracts.py
```

o ubicación equivalente podrá declarar la versión activa.

La ubicación definitiva se decidirá tras auditoría del repositorio.

---

## 16.193 ConsumerProfile v1.0

Cada perfil deberá declarar:

```text
supported_delivery_contracts = ("1.0",)
```

o estructura equivalente.

---

## 16.194 Serializer v1.0

El serializer deberá verificar que soporta:

```text
1.0
```

---

## 16.195 Trace v1.0

Todo DeliveryResult deberá registrar:

```text
delivery_contract_version = "1.0"
```

---

## 16.196 Gateway v1.0

El Gateway deberá exponer el contrato 1.0 sin inventar una segunda estructura incompatible.

---

## 16.197 Documentation v1.0

El presente documento constituirá la especificación arquitectónica de la versión 1.0.

Los schemas y código posteriores deberán alinearse con él.

---

## 16.198 Modelo conceptual de evolución

```text
                    ┌─────────────┐
                    │ Contract 1.0│
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Contract 1.1│
                    │ compatible  │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │ Contract 2.0│
                    │ breaking    │
                    └─────────────┘
```

---

## 16.199 Modelo de coexistencia

```text
            ┌────────────────────┐
            │ Runtime Delivery   │
            └─────────┬──────────┘
                      │
           ┌──────────┴──────────┐
           │                     │
           ▼                     ▼
     Contract 1.0          Contract 2.0
           │                     │
           ▼                     ▼
   Legacy Consumer         New Consumer
```

Solo cuando exista una migración real.

---

## 16.200 Modelo de retiro

```text
ACTIVE
  │
  ▼
DEPRECATED
  │
  ▼
RETIRED
```

La transición deberá ser auditable.

---

## 16.201 Matriz de cambio contractual

| Cambio | Compatibilidad esperada | Versión |
|---|---|---|
| Agregar campo opcional | Compatible | MINOR |
| Agregar metadata opcional | Compatible | MINOR |
| Eliminar campo opcional | Evaluar impacto | MINOR/MAJOR |
| Eliminar campo requerido | Incompatible | MAJOR |
| Renombrar campo requerido | Incompatible | MAJOR |
| Cambiar tipo | Normalmente incompatible | MAJOR |
| Cambiar significado | Incompatible | MAJOR |
| Refactor interno | Sin cambio contractual | Ninguna |
| Cambiar adapter | Sin cambio contractual si semántica igual | Ninguna |
| Cambiar framework Gateway | Sin cambio contractual si semántica igual | Ninguna |

---

## 16.202 Matriz de responsabilidad de versiones

| Versión | Responsable principal |
|---|---|
| Response Contract | Materialization / Response Model |
| Delivery Contract | Runtime Response Delivery |
| Consumer Profile | Consumer Model |
| Adapter implementation | Delivery Infrastructure |
| Gateway API | Gateway |
| Knowledge Version | HKS / Knowledge Governance |
| Capability Version | Capability Governance |

---

## 16.203 Prueba arquitectónica consolidada

La arquitectura deberá ser capaz de responder:

```text
What contract version produced this payload?
Was that version active at the time?
Did the consumer support it?
Which serializer handled it?
Which adapter transported it?
Is the version now deprecated?
Can the historical delivery still be interpreted?
```

---

## 16.204 Criterio de éxito

La estrategia de versionado será considerada correcta cuando HEYTI pueda introducir cambios compatibles sin romper consumidores y cambios incompatibles mediante una migración explícita, preservando siempre la interpretación histórica de entregas anteriores.

---

## 16.205 Declaración arquitectónica del capítulo

Los contratos de Runtime Response Delivery deberán evolucionar como artefactos gobernados.

Una versión no será simplemente un número.

Será una promesa semántica.

Mientras una versión esté activa, HEYTI deberá respetarla.

Si necesita extenderla, deberá hacerlo mediante reglas de compatibilidad.

Si necesita romperla, deberá crear una nueva versión.

Si necesita retirarla, deberá hacerlo mediante deprecación controlada.

La regla arquitectónica consolidada queda establecida como:

> **Toda versión contractual de HEYTI Runtime Response Delivery deberá ser explícita, semánticamente estable, trazable y gobernada por una política de compatibilidad. Ningún cambio incompatible podrá introducirse silenciosamente, y ninguna entrega histórica deberá reinterpretarse bajo una versión diferente a aquella con la que fue realizada.**

La evolución fundamental queda formalizada como:

```text
Stable Contract
      ↓
Compatible Extension
      ↓
Controlled Migration
      ↓
New Major Contract
      ↓
Deprecation
      ↓
Retirement
```

Con la política de versionado establecida queda preparada la siguiente dimensión arquitectónica:

**observabilidad, métricas, logging, auditoría operacional y diagnóstico de Runtime Response Delivery.**

---

**Fin del Capítulo 16**


# Capítulo 17. Observabilidad, métricas, logging, auditoría operacional y diagnóstico

## 17.1 Propósito del capítulo

Este capítulo define la arquitectura de **observabilidad, métricas, logging, auditoría operacional y diagnóstico** de HEYTI Runtime Response Delivery.

La finalidad es garantizar que una operación de entrega pueda ser comprendida no solamente mientras ocurre, sino también después de haber concluido.

Runtime Response Delivery deberá permitir observar:

- qué operación se ejecutó;
- qué respuesta fue involucrada;
- qué consumidor participó;
- qué adapter fue utilizado;
- qué etapas se completaron;
- cuánto tiempo consumieron;
- qué errores ocurrieron;
- y cuál fue el resultado terminal.

La regla fundamental será:

> **Una operación de Delivery deberá ser observable sin alterar su semántica ni exponer información sensible innecesaria.**

---

## 17.2 Observabilidad no es logging

Debe distinguirse:

```text
Observability
      ≠
Logging
```

Logging es una de las fuentes de observabilidad.

La observabilidad podrá incluir:

```text
logs
metrics
traces
events
audit records
health indicators
```

Cada mecanismo cumple una función diferente.

---

## 17.3 Objetivos de observabilidad

La observabilidad deberá permitir responder preguntas como:

```text
How many deliveries occurred?
How many succeeded?
How many failed?
How many were rejected?
Which consumers fail most?
Which adapters are slow?
Where does latency accumulate?
Which contract versions are still used?
Which errors repeat?
```

---

## 17.4 Principio de observabilidad por defecto

Runtime Response Delivery deberá diseñarse para ser observable desde el inicio.

No deberá añadirse observabilidad únicamente cuando aparezcan problemas en producción.

Conceptualmente:

```text
Delivery Operation
      │
      ├── result
      ├── metrics
      ├── logs
      └── trace
```

---

## 17.5 Observability Without Semantic Intrusion

La instrumentación no deberá modificar:

```text
response content
evidence
warnings
confidence
recommendations
```

La arquitectura deberá preservar:

```text
Observe
      ≠
Transform
```

---

## 17.6 Delivery Event Model

Podrá existir conceptualmente un modelo de eventos de Delivery.

Ejemplos:

```text
delivery.requested
delivery.validation.started
delivery.validation.completed
delivery.validation.failed
delivery.serialization.started
delivery.serialization.completed
delivery.serialization.failed
delivery.adapter.started
delivery.adapter.completed
delivery.adapter.failed
delivery.completed
delivery.rejected
delivery.failed
```

No será necesario emitir todos los eventos desde v1.0.

---

## 17.7 Eventos mínimos v1.0

Se recomienda comenzar con:

```text
delivery.started
delivery.completed
delivery.rejected
delivery.failed
```

y agregar mayor granularidad únicamente cuando aporte valor.

---

## 17.8 delivery.started

Este evento deberá representar que una operación de Delivery ha sido creada y comenzó procesamiento.

Podrá incluir:

```text
delivery_id
response_id
consumer_id
adapter_id
contract_version
started_at
```

cuando esos valores ya estén disponibles.

---

## 17.9 delivery.completed

Representa una operación concluida exitosamente.

Conceptualmente:

```text
status = DELIVERED
```

Podrá incluir:

```text
delivery_id
response_id
consumer_id
adapter_id
duration_ms
payload_size_bytes
completed_at
```

---

## 17.10 delivery.rejected

Representa una operación detenida por incumplimiento de precondiciones.

Podrá incluir:

```text
delivery_id
response_id
consumer_id
error_code
stage
completed_at
```

---

## 17.11 delivery.failed

Representa una operación aceptada que experimentó un fallo operacional.

Podrá incluir:

```text
delivery_id
response_id
adapter_id
error_code
stage
duration_ms
completed_at
```

---

## 17.12 EventBus

HEYTI ya contempla conceptualmente EventBus dentro de su arquitectura.

Runtime Response Delivery podrá utilizarlo para publicar eventos operacionales si ello se integra de forma coherente con la arquitectura existente.

Conceptualmente:

```text
Delivery
   ↓
EventBus
   ├── Observability
   ├── Audit
   └── Future Internal Consumers
```

---

## 17.13 EventBus no deberá ser requisito para Delivery

La entrega deberá poder completarse aunque el EventBus no sea necesario para el camino crítico, salvo que una política de auditoría obligatoria establezca lo contrario.

---

## 17.14 Fallo del EventBus

Si:

```text
Delivery = DELIVERED
```

pero:

```text
EventBus publish = FAILED
```

la arquitectura deberá distinguir ambos hechos.

No deberá modificar retroactivamente el significado cognitivo.

---

## 17.15 Observability Auxiliary Failure

Los fallos de observabilidad podrán clasificarse como:

```text
auxiliary
```

cuando no afecten el resultado de Delivery.

Sin embargo, deberán registrarse cuando sea posible.

---

## 17.16 Auditoría obligatoria

Si una política futura exige que determinada entrega tenga un registro de auditoría exitoso antes de considerarse válida, entonces:

```text
audit write
```

podrá convertirse en parte del critical path.

Esto deberá ser explícito.

---

## 17.17 Logging

Runtime Response Delivery deberá favorecer logging estructurado.

Ejemplo:

```json
{
  "event": "delivery.completed",
  "delivery_id": "DEL-001",
  "response_id": "RESP-001",
  "consumer_id": "AT_PORTAL",
  "adapter_id": "IN_MEMORY",
  "status": "DELIVERED",
  "duration_ms": 12
}
```

---

## 17.18 Structured Logging

El logging estructurado permite:

- búsquedas;
- correlación;
- métricas derivadas;
- análisis;
- automatización.

Deberá preferirse sobre mensajes exclusivamente libres.

---

## 17.19 Human-readable logs

Podrán coexistir mensajes legibles para desarrollo.

Ejemplo:

```text
Delivery DEL-001 completed for AT_PORTAL in 12 ms.
```

Pero la automatización deberá basarse preferentemente en campos estructurados.

---

## 17.20 Campos mínimos de logging

Cuando sea posible, cada evento debería conservar:

```text
delivery_id
response_id
consumer_id
adapter_id
status
stage
timestamp
```

No todos serán obligatorios en todos los eventos.

---

## 17.21 Correlation fields

Podrán añadirse:

```text
request_id
execution_id
session_id
correlation_id
```

para reconstruir el flujo completo.

---

## 17.22 No payload completo por defecto

Queda prohibido registrar automáticamente:

```text
full response payload
```

en cada operación.

Esto puede producir:

- exposición de datos;
- logs enormes;
- duplicación;
- problemas de privacidad.

---

## 17.23 Safe Logging Projection

Se deberá preferir una vista resumida.

Ejemplo:

```text
delivery_id
response_id
consumer
status
payload_size
```

---

## 17.24 Debug Payload Logging

En desarrollo podrá habilitarse logging detallado mediante una política explícita.

Nunca deberá habilitarse accidentalmente en producción.

---

## 17.25 Redacción

Los logs deberán excluir o redactar:

```text
tokens
passwords
PII
raw evidence
precise addresses
sensitive field data
```

según políticas.

---

## 17.26 Log Levels

Podrán utilizarse niveles como:

```text
DEBUG
INFO
WARNING
ERROR
CRITICAL
```

de manera consistente.

---

## 17.27 INFO

Ejemplos:

```text
delivery started
delivery completed
```

---

## 17.28 WARNING

Ejemplos:

```text
deprecated contract version
payload approaching size limit
optional trace unavailable
```

---

## 17.29 ERROR

Ejemplos:

```text
delivery failed
serialization failed
adapter failed
```

---

## 17.30 CRITICAL

Podrá reservarse para:

```text
systemic delivery corruption
audit subsystem unavailable when mandatory
unrecoverable registry inconsistency
```

No deberá utilizarse para fallos ordinarios.

---

## 17.31 Metrics

La arquitectura deberá permitir métricas cuantitativas.

Métricas mínimas conceptuales:

```text
delivery_total
delivery_delivered_total
delivery_rejected_total
delivery_failed_total
```

---

## 17.32 delivery_total

Cuenta operaciones de Delivery iniciadas o terminadas, según definición precisa.

La definición deberá ser consistente.

Preferiblemente:

```text
number of created delivery operations
```

---

## 17.33 delivery_delivered_total

Cuenta operaciones con:

```text
status = DELIVERED
```

---

## 17.34 delivery_rejected_total

Cuenta operaciones con:

```text
status = REJECTED
```

---

## 17.35 delivery_failed_total

Cuenta operaciones con:

```text
status = FAILED
```

---

## 17.36 Invariante de contadores

En un modelo simple:

```text
delivery_total
=
delivered
+
rejected
+
failed
+
currently_active
```

según momento de observación.

---

## 17.37 Delivery Duration

Deberá poder medirse:

```text
delivery_duration_ms
```

desde inicio del pipeline hasta estado terminal.

---

## 17.38 Stage Duration

Podrán medirse adicionalmente:

```text
validation_duration_ms
serialization_duration_ms
adapter_duration_ms
```

si existe necesidad de optimización.

---

## 17.39 No premature micro-metrics

v1.0 deberá evitar instrumentar decenas de tiempos internos sin necesidad.

La granularidad deberá aumentar conforme aparezcan preguntas operacionales reales.

---

## 17.40 Payload Size

Podrá medirse:

```text
payload_size_bytes
```

para:

- rendimiento;
- límites;
- detección de crecimiento accidental.

---

## 17.41 Payload Size by Consumer

Podrá analizarse:

```text
AT_PORTAL payload average
```

frente a otros consumers.

---

## 17.42 Metrics by Adapter

Podrán segmentarse:

```text
delivery_total{adapter="HTTP_JSON"}
```

conceptualmente.

---

## 17.43 Metrics by Consumer

Ejemplo:

```text
delivery_failed_total{consumer="AT_PORTAL"}
```

---

## 17.44 Metrics by Contract Version

Ejemplo:

```text
delivery_total{contract_version="1.0"}
```

Será útil durante deprecación.

---

## 17.45 Metrics by Error Code

Ejemplo:

```text
delivery_error_total{code="DELIVERY_TIMEOUT"}
```

Esto permitirá detectar patrones.

---

## 17.46 Cardinality Control

Las labels de métricas deberán evitar cardinalidad alta.

No deberán utilizarse como labels:

```text
delivery_id
response_id
session_id
```

porque cada valor sería prácticamente único.

---

## 17.47 Safe metric dimensions

Buenos candidatos:

```text
status
consumer_id
adapter_id
contract_version
error_code
```

si el número de valores permanece controlado.

---

## 17.48 Trace IDs en logs, no métricas

IDs individuales deberán permanecer en:

```text
logs / traces
```

no en labels de métricas.

---

## 17.49 Tracing

La arquitectura deberá soportar conceptualmente tracing de extremo a extremo.

Ejemplo:

```text
Gateway Span
   ↓
Runtime Span
   ↓
Capability Span
   ↓
Materialization Span
   ↓
Delivery Span
   ↓
Adapter Span
```

---

## 17.50 Delivery Span

Podrá registrar:

```text
delivery_id
consumer_id
adapter_id
status
```

como atributos.

---

## 17.51 Trace propagation

Si existe un `trace_id` externo, deberá propagarse sin sustituir:

```text
delivery_id
response_id
```

---

## 17.52 OpenTelemetry

La arquitectura deberá permanecer compatible con una futura implementación OpenTelemetry.

No es obligatorio incorporarla durante Sprint 23.

---

## 17.53 No proprietary lock-in

El Core no deberá depender de un proveedor específico de observabilidad.

---

## 17.54 Observability Port

Si la abstracción lo justifica, podría existir:

```text
DeliveryObserver
```

o:

```text
ObservabilitySink
```

para desacoplar instrumentación.

No deberá crearse si logging estándar y EventBus son suficientes.

---

## 17.55 Auditability

La auditoría deberá permitir reconstruir hechos relevantes de Delivery.

Como mínimo:

```text
delivery_id
response_id
consumer_id
adapter_id
contract_version
status
timestamps
error_code
```

cuando correspondan.

---

## 17.56 Audit Record

Conceptualmente:

```text
DeliveryAuditRecord
├── delivery_id
├── response_id
├── request_id?
├── execution_id?
├── consumer_id
├── adapter_id
├── contract_version
├── started_at
├── completed_at
├── status
├── error_code?
└── payload_reference?
```

No es obligatorio persistir exactamente esta estructura desde v1.0.

---

## 17.57 Audit vs Trace

Debe distinguirse:

```text
Trace
```

de:

```text
Audit Record
```

Trace ayuda a seguir ejecución.

Audit preserva hechos con finalidad de revisión formal.

---

## 17.58 Audit vs Logging

También:

```text
Audit
      ≠
Logging
```

Los logs pueden rotar.

La auditoría puede requerir retención definida.

---

## 17.59 Audit persistence

La persistencia de auditoría deberá diseñarse cuando exista necesidad operacional.

Podrá utilizar:

- base de datos;
- archivo estructurado;
- sistema especializado.

No deberá añadirse sin gobernanza.

---

## 17.60 Audit retention

Deberá existir una política de retención.

No deberán conservarse datos indefinidamente por defecto.

---

## 17.61 Audit privacy

Los registros deberán aplicar minimización y protección.

Especialmente para:

- datos personales;
- información de Campo;
- operaciones sensibles de Día D.

---

## 17.62 Payload audit strategy

Se deberán considerar opciones como:

```text
no payload
payload reference
payload hash
redacted payload
full payload under restricted policy
```

La decisión dependerá del nivel de riesgo.

---

## 17.63 Full payload caution

Guardar el payload completo puede facilitar auditoría pero aumentar:

- almacenamiento;
- privacidad;
- exposición.

No deberá adoptarse automáticamente.

---

## 17.64 Payload Reference

Una estrategia puede ser:

```text
response_id
```

más una referencia a la respuesta persistida en otra capa.

---

## 17.65 Payload Hash futuro

Un hash podrá ayudar a verificar integridad.

Solo deberá incorporarse después de establecer canonicalización formal.

---

## 17.66 Audit immutability

Los registros de auditoría deberán favorecer inmutabilidad.

Una operación histórica no deberá reescribirse para aparentar éxito.

---

## 17.67 Failed then retried

Ejemplo correcto:

```text
DEL-001 FAILED
DEL-002 DELIVERED
retry_of = DEL-001
```

No:

```text
DEL-001 changed from FAILED to DELIVERED
```

---

## 17.68 Historical truth

La auditoría deberá preservar:

> Lo que realmente ocurrió.

No el estado final deseado.

---

## 17.69 Diagnostic Model

El diagnóstico deberá permitir ubicar una incidencia por etapas.

Conceptualmente:

```text
REQUEST
EXECUTION
MATERIALIZATION
VALIDATION
SERIALIZATION
ADAPTER
TRANSPORT
GATEWAY
PRESENTATION
```

---

## 17.70 Diagnostic Question

Ante una incidencia:

> "HEYTI no mostró la respuesta"

deberá poder determinarse:

```text
Did Runtime execute?
Was Response materialized?
Did Delivery validate?
Did Serialization succeed?
Did Adapter deliver?
Did Gateway expose?
Did Consumer receive?
Did Presentation render?
```

---

## 17.71 Diagnostic Ladder

Se establece la siguiente escalera de diagnóstico:

```text
1. request_id exists?
2. execution_id exists?
3. response_id exists?
4. delivery_id exists?
5. delivery status?
6. adapter status?
7. gateway status?
8. presentation status?
```

---

## 17.72 No speculative diagnosis

La observabilidad deberá reducir afirmaciones como:

```text
"probably the map failed"
```

sin evidencia.

---

## 17.73 Delivery Diagnostic Record

Podrá existir conceptualmente una vista agregada:

```text
DeliveryDiagnosticView
```

que reúna:

```text
trace
result
metrics
error
```

para soporte.

No deberá formar parte del contrato público ordinario.

---

## 17.74 Support Mode

La futura UI de administración podría mostrar:

```text
response_id
delivery_id
status
contract version
adapter
error
```

para diagnóstico.

---

## 17.75 User-facing UI

La interfaz principal no necesita mostrar todos estos detalles.

Presentation decidirá.

---

## 17.76 Correlation-first debugging

Todo diagnóstico deberá comenzar preferentemente por:

```text
delivery_id
```

o:

```text
response_id
```

en lugar de buscar mensajes por texto.

---

## 17.77 Diagnostic example

Supóngase:

```text
response_id = RESP-500
delivery_id = DEL-900
```

La investigación podrá seguir:

```text
DEL-900
→ status DELIVERED
→ adapter HTTP_JSON
→ Gateway 200
```

Entonces el problema probablemente está después de Delivery.

---

## 17.78 Diagnostic example 2

```text
DEL-901
→ FAILED
→ stage SERIALIZATION
→ DELIVERY_SERIALIZATION_ERROR
```

Entonces el problema está dentro de Delivery.

---

## 17.79 Diagnostic example 3

```text
No delivery_id
but response_id exists
```

podría indicar que nunca se inició Delivery.

---

## 17.80 Diagnostic example 4

```text
request_id exists
no execution_id
```

el problema está antes del Runtime Execution.

---

## 17.81 Operational Dashboard futuro

En una fase posterior podrá construirse un dashboard con:

```text
delivery success rate
average latency
errors by type
consumer health
adapter health
contract versions
```

---

## 17.82 Dashboard no forma parte del Core

El dashboard será un consumidor de observabilidad.

No deberá introducir lógica en Delivery.

---

## 17.83 Health Indicators

Podrán definirse indicadores como:

```text
Delivery Health = HEALTHY / DEGRADED / UNHEALTHY
```

a partir de métricas.

No deberá confundirse con una respuesta cognitiva de HEYTI.

---

## 17.84 Adapter Health

Cada adapter externo podrá tener estado de salud.

---

## 17.85 Consumer Health

Un consumidor podrá presentar alta tasa de fallos.

Esto no significa necesariamente que HEYTI Core esté fallando.

---

## 17.86 Health attribution

La observabilidad deberá permitir atribuir degradación a:

```text
Core
Adapter
Target
Gateway
Consumer
```

---

## 17.87 SLO futuro

En una fase madura podrán definirse objetivos como:

```text
99.9% successful Delivery
p95 latency
```

No forma parte obligatoria de Sprint 23.

---

## 17.88 Error Budget futuro

También podrá existir un presupuesto de errores.

No deberá implementarse antes de contar con métricas reales.

---

## 17.89 Baseline Metrics

Sprint 23 deberá preparar el sistema para obtener una línea base.

Ejemplos:

```text
average delivery latency
serialization latency
payload size
success rate
```

---

## 17.90 No optimization without measurement

La arquitectura deberá evitar optimizaciones prematuras.

Primero:

```text
measure
```

después:

```text
optimize
```

---

## 17.91 Performance regression

Una futura CI podrá comparar:

```text
delivery benchmark
```

contra baseline.

No es necesario inicialmente.

---

## 17.92 Logging and Testability

Los tests no deberán depender de texto exacto de logs salvo necesidad.

Preferible validar:

```text
structured event
```

o resultado.

---

## 17.93 InMemory Observer

Podrá existir un observador de prueba capaz de capturar eventos.

Ejemplo:

```text
InMemoryDeliveryObserver
```

si EventBus no cubre esa necesidad.

---

## 17.94 Testing events

Podrán probarse:

```text
delivery.started emitted
delivery.completed emitted
delivery.failed emitted
```

---

## 17.95 Event ordering

Cuando sea importante, deberá mantenerse:

```text
started
before
completed
```

---

## 17.96 No event after terminal duplicate

Una operación no deberá emitir:

```text
delivery.completed
```

y después:

```text
delivery.failed
```

para el mismo intento.

---

## 17.97 Terminal event consistency

Cada operación deberá emitir como máximo un evento terminal principal:

```text
completed
rejected
failed
```

---

## 17.98 Metric consistency

Los contadores deberán corresponder a estados reales.

---

## 17.99 Double counting

Queda prohibido incrementar:

```text
delivery_failed_total
```

dos veces para una misma operación.

---

## 17.100 Retry metrics

En el futuro cada retry será una nueva operación.

Así las métricas reflejarán intentos reales.

---

## 17.101 Metrics vs Business KPIs

Debe distinguirse:

```text
Delivery Metrics
```

de:

```text
Political / Territorial KPIs
```

Delivery mide infraestructura.

No resultados electorales.

---

## 17.102 No business metric pollution

Ejemplos prohibidos dentro de HRRD metrics:

```text
PAN margin
MORENA trend
field priority score
```

---

## 17.103 Observability and Session

Los logs podrán incluir:

```text
session_id
```

cuando sea seguro.

---

## 17.104 Session cardinality

`session_id` tampoco deberá utilizarse como label de métricas.

---

## 17.105 Observability and ConsumerProfile

Podrá registrarse:

```text
consumer_profile_version
```

para diagnosticar incompatibilidades.

---

## 17.106 Observability and ContractVersion

Será obligatorio conservar:

```text
delivery_contract_version
```

en DeliveryResult o trace.

---

## 17.107 Deprecation observability

Una versión deprecada deberá poder medirse.

Ejemplo:

```text
deprecated_contract_usage_total
```

---

## 17.108 Observability and Security

Los rechazos de seguridad deberán generar observabilidad adecuada.

---

## 17.109 No security detail leak

No deberán incluirse en métricas o logs públicos:

```text
token
password
authorization header
```

---

## 17.110 Security Event severity

Un único rechazo normal puede ser:

```text
INFO/WARNING
```

Mientras un patrón repetido puede activar alerta.

---

## 17.111 Observability failure metrics

Podrán existir métricas de fallos del propio subsistema de observabilidad si se vuelve crítico.

No es necesario inicialmente.

---

## 17.112 Audit write failure

Si la auditoría es obligatoria deberá producir un error operacional claro.

No deberá ignorarse.

---

## 17.113 Optional telemetry failure

Si una métrica no puede emitirse:

```text
delivery
```

no deberá fallar por ello.

---

## 17.114 Telemetry non-blocking preference

La telemetría ordinaria deberá ser:

```text
best effort
```

cuando sea seguro.

---

## 17.115 Exception safety in logging

Un logger defectuoso no debería tumbar Delivery.

La instrumentación deberá estar aislada.

---

## 17.116 No recursive logging failure

Un error al registrar otro error no deberá generar loops.

---

## 17.117 Diagnostic identifiers in public response

Podrá ser útil devolver:

```text
delivery_id
```

en errores públicos para soporte.

Esto deberá equilibrarse con seguridad.

---

## 17.118 Support Reference

La UI podría mostrar:

```text
Referencia: DEL-001
```

cuando ocurra un error.

No es obligación del Core decidir si se muestra.

---

## 17.119 Audit reference

Podrá existir:

```text
audit_id
```

en sistemas futuros.

No se requiere v1.0.

---

## 17.120 Operational Runbook

En una fase madura deberá existir un runbook de diagnóstico.

Por ejemplo:

```text
If delivery_failed_total rises:
1. identify error code
2. identify consumer
3. identify adapter
4. inspect target health
5. inspect serialization errors
```

---

## 17.121 Sprint 23 Diagnostic Baseline

Durante implementación deberá establecerse un diagnóstico simple que permita verificar:

```text
response_id
delivery_id
status
adapter
error
```

sin infraestructura externa.

---

## 17.122 Console logging initial

La primera versión podrá utilizar logging estándar de Python.

No será necesario incorporar inmediatamente una plataforma externa.

---

## 17.123 Python logging

Podrá utilizarse:

```text
logging
```

del estándar de Python como base inicial.

La configuración concreta se decidirá en implementación.

---

## 17.124 Structured fields with standard logging

Incluso con logging estándar podrán conservarse campos estructurados mediante:

- adapters;
- extra fields;
- serialización controlada.

---

## 17.125 No print debugging as architecture

Queda desaconsejado utilizar:

```python
print(...)
```

como mecanismo permanente de observabilidad.

---

## 17.126 Prints en pruebas manuales

Podrán utilizarse temporalmente durante desarrollo.

No deberán constituir la solución final.

---

## 17.127 Observability package

La arquitectura podría integrar HRRD con infraestructura común de observabilidad de HEYTI.

No deberá crear un subsistema paralelo innecesario.

---

## 17.128 Reutilización

Si HEYTI ya posee:

```text
EventBus
logging conventions
trace context
```

Delivery deberá reutilizarlos cuando corresponda.

---

## 17.129 Auditoría del repositorio previa

Antes de implementar, deberá revisarse qué infraestructura de:

```text
logging
EventBus
SessionManager
runtime events
```

ya existe.

No deberá duplicarse sin necesidad.

---

## 17.130 Mapa de observabilidad

Conceptualmente:

```text
Runtime Response Delivery
        │
        ├── Logs
        │
        ├── Metrics
        │
        ├── Trace
        │
        └── Events
               │
               ▼
         Observability
               │
               ▼
           Diagnosis
```

---

## 17.131 Mapa de auditoría

```text
Delivery Operation
      ↓
DeliveryTrace
      ↓
Audit Projection
      ↓
Audit Store
      ↓
Historical Review
```

---

## 17.132 Observability Pipeline

```text
Delivery Starts
      ↓
Start Event / Log
      ↓
Validation
      ↓
Serialization
      ↓
Adapter
      ↓
Result
      ↓
Terminal Event
      ↓
Metrics
      ↓
Trace Completion
```

---

## 17.133 Diagnostic Pipeline

```text
Incident
   ↓
Obtain delivery_id / response_id
   ↓
Locate trace
   ↓
Identify terminal status
   ↓
Identify stage
   ↓
Identify error code
   ↓
Identify adapter / consumer
   ↓
Determine responsible boundary
```

---

## 17.134 Metrics MVP

Para v1.0 se recomienda como mínimo:

```text
delivery_total
delivery_delivered_total
delivery_rejected_total
delivery_failed_total
delivery_duration_ms
```

---

## 17.135 Optional metrics MVP

También podrá medirse:

```text
payload_size_bytes
adapter_duration_ms
```

si la implementación lo hace fácilmente.

---

## 17.136 Logs MVP

Cada operación deberá producir al menos un registro terminal con:

```text
delivery_id
response_id
consumer_id
adapter_id
status
error_code if any
```

---

## 17.137 Trace MVP

El `DeliveryResult` o `DeliveryTrace` deberá conservar suficiente información para reconstrucción.

---

## 17.138 Audit MVP

Durante Sprint 23 puede bastar con garantizar que la estructura necesaria existe.

No necesariamente será obligatorio implementar persistencia permanente.

---

## 17.139 Diferencia entre arquitectura y materialización inmediata

El documento deberá definir:

```text
what must be possible
```

aunque la primera implementación materialice solo un subconjunto controlado.

---

## 17.140 No fake audit

No deberá afirmarse:

```text
auditable
```

si la implementación no conserva ninguna información.

Al menos deberá existir DeliveryTrace verificable.

---

## 17.141 Observability Quality Attributes

La observabilidad deberá ser:

```text
structured
correlatable
low-overhead
secure
non-invasive
version-aware
testable
```

---

## 17.142 Performance overhead

La instrumentación no deberá dominar la latencia de Delivery.

---

## 17.143 Sampling future

Si el volumen crece mucho, tracing detallado podrá utilizar sampling.

No es necesario en v1.0.

---

## 17.144 Audit not sampled

Los eventos de auditoría obligatoria no deberán perderse por sampling.

---

## 17.145 Metric aggregation

Las métricas deberán agregarse sin conservar datos individuales innecesarios.

---

## 17.146 Privacy advantage

Esto permite conocer:

```text
100 failed deliveries
```

sin almacenar 100 payloads completos.

---

## 17.147 Observability tests

Deberán existir pruebas como:

```text
test_delivery_completed_is_logged
test_failed_delivery_records_error_code
test_delivery_trace_preserves_ids
test_delivery_duration_is_non_negative
```

---

## 17.148 Event tests

Si EventBus se utiliza:

```text
test_delivery_started_event_emitted
test_delivery_terminal_event_emitted_once
```

---

## 17.149 Metrics tests

Cuando exista collector:

```text
test_success_counter_incremented
test_failed_counter_incremented
```

---

## 17.150 No sensitive logging tests

```text
test_payload_secrets_not_logged
test_auth_tokens_not_logged
```

---

## 17.151 Diagnostic tests

Podrá probarse que un fallo de serializer produce:

```text
stage = SERIALIZATION
```

y uno de adapter:

```text
stage = DELIVERY_EXECUTION
```

---

## 17.152 Audit consistency tests

Si existe AuditRecord:

```text
test_audit_status_matches_delivery_result
```

---

## 17.153 Concurrency observability tests

Dos operaciones concurrentes no deberán mezclar IDs en logs o traces.

---

## 17.154 Test correlation

```text
REQ-001
EXE-001
RESP-001
DEL-001
```

deberán permanecer correlacionados.

---

## 17.155 Test terminal uniqueness

Una entrega deberá tener exactamente un terminal result.

---

## 17.156 Failure isolation test

Si falla logging opcional:

```text
Delivery result
```

no deberá alterarse.

---

## 17.157 Mandatory audit failure test

Si se implementa auditoría obligatoria:

```text
audit write fails
```

deberá comportarse según política explícita.

---

## 17.158 Operational readiness criteria

Antes de conectar un consumidor real, deberá ser posible:

```text
see delivery start/end
identify failure stage
inspect result
correlate response and delivery
```

---

## 17.159 Production readiness criteria

Antes de producción deberá definirse además:

```text
log retention
metric collection
alert policy
security logging
audit retention
```

cuando corresponda.

---

## 17.160 No production without visibility

Una integración real no deberá desplegarse si un fallo de Delivery no puede diagnosticarse mínimamente.

---

## 17.161 Observability and six AT modules

Cuando los seis módulos consuman HEYTI, deberá ser posible conocer:

```text
delivery success by module/consumer
```

sin mezclarlo con sus KPIs de negocio.

---

## 17.162 Consumer identity for module diagnostics

Si los módulos se modelan como consumidores separados, `consumer_id` permitirá distinguirlos.

Si forman parte de un consumidor único, deberá existir otro contexto semántico solo si realmente es necesario.

---

## 17.163 No forced module labels

No deberá añadirse:

```text
module_id
```

a todas las entregas únicamente por conveniencia de métricas.

Solo si forma parte real del contexto.

---

## 17.164 UI telemetry

La futura UI podrá emitir su propia telemetría:

```text
presentation.rendered
presentation.failed
```

Esto permitirá distinguirla de Delivery.

---

## 17.165 End-to-end observability

Conceptualmente:

```text
delivery.completed
      ↓
consumer.received
      ↓
presentation.rendered
```

podrían convertirse en eventos distintos.

---

## 17.166 No fake end-to-end success

Delivery no deberá declarar:

```text
presentation.rendered
```

sin confirmación.

---

## 17.167 User-visible error and internal diagnostics

La UI puede mostrar:

```text
No fue posible mostrar la respuesta.
```

mientras internamente:

```text
delivery_id
error_stage
error_code
```

permiten diagnóstico detallado.

---

## 17.168 Support workflow futuro

```text
User reports issue
      ↓
delivery_id
      ↓
Operational trace
      ↓
Root cause
```

Esto será una capacidad importante de HEYTI.

---

## 17.169 Invariantes de observabilidad

Se establecen los siguientes invariantes.

### HRRD-O01 — Observable by Default

Toda operación deberá generar información suficiente para diagnóstico.

### HRRD-O02 — Structured Correlation

Logs y traces deberán utilizar identificadores estructurados.

### HRRD-O03 — No Semantic Mutation

La observabilidad no modificará la respuesta.

### HRRD-O04 — Secure Telemetry

No se registrarán secretos ni payloads sensibles indiscriminadamente.

### HRRD-O05 — Terminal Visibility

Toda operación deberá producir evidencia de su estado terminal.

### HRRD-O06 — Failure Stage Visibility

Los fallos deberán poder localizarse por etapa.

### HRRD-O07 — Metric Cardinality Control

Las métricas deberán evitar IDs únicos como labels.

### HRRD-O08 — Audit Historical Integrity

Los registros históricos no deberán reescribirse para ocultar fallos.

### HRRD-O09 — Auxiliary Failure Isolation

Los fallos de telemetría opcional no deberán corromper Delivery.

### HRRD-O10 — Technology Independence

La arquitectura de observabilidad no deberá acoplar el Core a un proveedor específico.

---

## 17.170 Prueba de conformidad

Una implementación deberá demostrar:

1. que puede identificar cada operación por `delivery_id`;
2. que puede correlacionar `response_id`;
3. que conoce el estado terminal;
4. que puede identificar el adapter;
5. que puede identificar el consumer;
6. que puede localizar la etapa de error;
7. que produce métricas básicas;
8. que no expone datos sensibles en logs;
9. que la observabilidad funciona sin UI;
10. que un fallo opcional de telemetría no modifica la semántica de la respuesta.

---

## 17.171 Prueba diagnóstica de referencia

Ante:

```text
delivery_id = DEL-001
```

deberá ser posible reconstruir como mínimo:

```text
response_id
consumer_id
adapter_id
status
started_at
completed_at
error_code if any
error_stage if any
```

---

## 17.172 Criterio de éxito

La observabilidad será considerada adecuada cuando una incidencia de Delivery pueda diagnosticarse utilizando evidencia estructurada, sin depender de reproducir manualmente el problema ni inferir su origen por mensajes vagos.

---

## 17.173 Declaración arquitectónica del capítulo

Runtime Response Delivery deberá ser una frontera transparente para operación y auditoría.

No transparente en el sentido de exponer datos internos, sino en el sentido de poder explicar qué ocurrió.

Toda entrega deberá dejar evidencia suficiente para identificar:

- su origen;
- su identidad;
- su consumidor;
- su adapter;
- su duración;
- su resultado;
- y su eventual error.

La regla arquitectónica consolidada queda establecida como:

> **HEYTI Runtime Response Delivery deberá ser observable, correlacionable, medible y auditable por diseño. La instrumentación deberá preservar la semántica, proteger la privacidad y permitir diagnosticar con precisión la frontera donde ocurrió cualquier fallo.**

La relación fundamental queda formalizada como:

```text
Delivery Operation
      ↓
Logs + Metrics + Trace + Events
      ↓
Operational Evidence
      ↓
Diagnosis
      ↓
Audit
      ↓
Continuous Improvement
```

Con esta dimensión de observabilidad establecida queda preparada la siguiente pieza de la arquitectura:

**integración con Presentation, modelos visuales y entrega de contenido para texto, KPIs, tablas, gráficas, mapas y acciones de interfaz.**

---

**Fin del Capítulo 17**


# Capítulo 18. Integración con Presentation, modelos visuales y entrega de contenido para texto, KPIs, tablas, gráficas, mapas y acciones

## 18.1 Propósito del capítulo

Este capítulo define la relación arquitectónica entre **HEYTI Runtime Response Delivery (HRRD)** y la futura capa de **Presentation** encargada de representar las respuestas ante el usuario.

La finalidad es establecer cómo HEYTI deberá entregar contenido suficientemente estructurado para que un consumidor visual pueda construir:

```text
texto
KPIs
tablas
gráficas
mapas
advertencias
evidencias
acciones
```

sin introducir en HEYTI-CORE dependencias directas de:

```text
HTML
CSS
DOM
Leaflet
Chart.js
component libraries
browser state
```

La regla fundamental será:

> **HEYTI entrega semántica estructurada; Presentation decide su forma visual.**

---

## 18.2 Delivery no es Presentation

Debe preservarse de manera estricta:

```text
Delivery
   ≠
Presentation
```

Delivery responde:

> ¿Qué contenido estructurado debe llegar al consumidor?

Presentation responde:

> ¿Cómo debe representarse ese contenido ante el usuario?

---

## 18.3 Presentation Boundary

La frontera conceptual será:

```text
HEYTI Core
     ↓
Materialization
     ↓
Runtime Response Delivery
     ↓
Delivery Contract
================================
      PRESENTATION BOUNDARY
================================
     ↓
Consumer Adapter
     ↓
Presentation Model
     ↓
UI Components
```

Todo lo que ocurre después de esta frontera pertenece al consumidor.

---

## 18.4 Presentation Model

Se define conceptualmente:

```text
PresentationModel
```

como una representación construida fuera de HEYTI Core a partir del Delivery Contract.

Ejemplo:

```text
DeliveryPayload
      ↓
Portal Adapter
      ↓
PresentationModel
      ↓
DOM / Leaflet / Chart.js
```

---

## 18.5 Delivery Contract como fuente

Presentation deberá construir sus vistas a partir del contrato entregado.

No deberá requerir acceso directo a:

```text
HKS
HES
Capability implementation
Runtime internals
database queries
```

---

## 18.6 Consumer Adapter

El consumidor deberá contar con una capa capaz de interpretar HEYTI.

Conceptualmente:

```text
HEYTI Consumer Adapter
```

será responsable de transformar contenido semántico en modelos de Presentation.

---

## 18.7 Consumer Adapter no es DeliveryAdapter

Debe distinguirse:

```text
DeliveryAdapter
```

de:

```text
Consumer Presentation Adapter
```

El primero transporta la respuesta.

El segundo interpreta la respuesta para presentación.

---

## 18.8 Ejemplo completo

```text
HEYTI
  ↓
DeliveryAdapter
  ↓
JSON
  ↓
Portal
  ↓
Consumer Adapter
  ↓
Presentation Model
  ↓
Leaflet / Chart.js / HTML
```

---

## 18.9 Neutralidad visual

La salida de HEYTI deberá permanecer suficientemente neutral para permitir diferentes representaciones.

Por ejemplo:

```text
Metric
```

podrá representarse como:

- tarjeta;
- indicador;
- fila de tabla;
- etiqueta;
- gráfico de gauge.

HEYTI no deberá decidir cuál.

---

## 18.10 Content Type Model

El Delivery Contract deberá soportar tipos semánticos de contenido.

Como base conceptual:

```text
TEXT
METRIC
TABLE
SERIES
TERRITORIAL_REFERENCE
GEOMETRY
EVIDENCE
WARNING
ACTION
```

Estos tipos deberán estar alineados con Materialization.

---

## 18.11 TEXT

`TEXT` representa contenido narrativo o descriptivo.

Ejemplo:

```json
{
  "type": "text",
  "content": "La sección presenta una competencia electoral elevada."
}
```

Presentation decidirá:

- tipografía;
- tamaño;
- posición;
- color;
- espaciado.

---

## 18.12 Texto no es HTML

Por defecto, `TEXT` deberá tratarse como texto.

No como:

```text
HTML executable
```

Esto reduce:

- acoplamiento;
- riesgo XSS;
- dependencia visual.

---

## 18.13 Rich text futuro

Si HEYTI necesita:

```text
Markdown
```

o contenido enriquecido, deberá existir un tipo contractual explícito.

No deberá introducirse de manera informal dentro de `TEXT`.

---

## 18.14 Narrative Blocks

La respuesta podrá contener varios bloques textuales.

Ejemplo:

```text
summary
interpretation
recommendation
warning
```

si Materialization los define.

Delivery deberá preservar su semántica.

---

## 18.15 METRIC

`METRIC` representa un valor cuantitativo con significado explícito.

Ejemplo:

```json
{
  "type": "metric",
  "key": "participation",
  "label": "Participación",
  "value": 61.4,
  "unit": "percent"
}
```

---

## 18.16 Metric Semantics

Un metric deberá permitir comprender:

```text
what?
how much?
in which unit?
```

sin depender de la forma visual.

---

## 18.17 Metric Status

Podrá existir:

```text
semantic_status
```

cuando sea necesario.

Ejemplo:

```text
HIGH
MEDIUM
LOW
```

si dicha clasificación proviene de una regla cognitiva válida.

---

## 18.18 Semantic status no es color

Ejemplo correcto:

```text
semantic_status = HIGH
```

Ejemplo incorrecto:

```text
color = "#FF0000"
```

La UI podrá decidir que `HIGH` se represente con determinado color.

---

## 18.19 KPI

Un KPI visual es una forma de presentar un `METRIC`.

Conceptualmente:

```text
HEYTI METRIC
     ↓
Presentation
     ↓
KPI Card
```

Por ello HEYTI no necesita un tipo:

```text
KPI_CARD
```

salvo que exista una semántica distinta real.

---

## 18.20 TABLE

`TABLE` representa información tabular estructurada.

Ejemplo:

```json
{
  "type": "table",
  "columns": [
    {
      "key": "year",
      "label": "Año",
      "data_type": "integer"
    },
    {
      "key": "votes",
      "label": "Votos",
      "data_type": "integer"
    }
  ],
  "rows": [
    {
      "year": 2018,
      "votes": 1200
    },
    {
      "year": 2024,
      "votes": 1450
    }
  ]
}
```

---

## 18.21 Table Presentation

El consumidor podrá decidir:

- orden;
- paginación;
- filtros;
- tamaño;
- scroll;
- exportación;
- estilos.

Estas decisiones no pertenecen a Delivery.

---

## 18.22 Table column order

Si el orden de columnas posee significado contractual deberá preservarse.

Si es únicamente visual, Presentation podrá cambiarlo.

La diferencia deberá documentarse.

---

## 18.23 SERIES

`SERIES` representa datos ordenados susceptibles de análisis o visualización.

Ejemplo:

```json
{
  "type": "series",
  "key": "electoral_history",
  "label": "Histórico electoral",
  "categories": [2018, 2021, 2024],
  "values": [1200, 1310, 1450],
  "unit": "votes"
}
```

---

## 18.24 Series no es Chart

Debe preservarse:

```text
SERIES
   ≠
CHART
```

Una serie puede representarse como:

- línea;
- barras;
- tabla;
- sparkline;
- texto.

La UI decide.

---

## 18.25 Multiple Series

Podrá existir una estructura como:

```json
{
  "type": "series",
  "categories": [2018, 2021, 2024],
  "series": [
    {
      "key": "pan",
      "label": "PAN",
      "values": [500, 480, 460]
    },
    {
      "key": "morena",
      "label": "MORENA",
      "values": [420, 510, 610]
    }
  ]
}
```

si el contrato de Materialization lo requiere.

---

## 18.26 No party colors in Core

HEYTI no deberá incluir automáticamente:

```text
PAN blue
MORENA burgundy
PRI red
```

como detalle visual de Delivery.

La Presentation podrá utilizar una configuración visual externa.

---

## 18.27 TERRITORIAL_REFERENCE

`TERRITORIAL_REFERENCE` representa una referencia geográfica lógica.

Ejemplo:

```json
{
  "type": "territorial_reference",
  "section_id": "1481",
  "municipality_id": "020"
}
```

---

## 18.28 Territorial reference first

Cuando el consumidor ya posee cartografía, deberá preferirse una referencia antes que geometría completa.

Esto permite:

```text
smaller payload
faster delivery
single source of geometry
```

---

## 18.29 GEOMETRY

`GEOMETRY` podrá utilizarse cuando sea necesario transportar geometría.

GeoJSON constituye una opción natural.

Ejemplo:

```json
{
  "type": "geometry",
  "format": "geojson",
  "geometry": {
    "type": "Polygon",
    "coordinates": []
  }
}
```

---

## 18.30 Geometry is not map style

La geometría deberá permanecer separada de:

```text
fillColor
strokeColor
weight
opacity
zoom
popup
```

Estas decisiones pertenecen a Presentation.

---

## 18.31 Leaflet integration

Una UI basada en Leaflet podrá realizar:

```text
TERRITORIAL_REFERENCE
      ↓
resolve geometry
      ↓
Leaflet Layer
```

o:

```text
GEOMETRY
      ↓
L.geoJSON(...)
```

HEYTI Core no deberá importar Leaflet.

---

## 18.32 Map interaction

Acciones como:

```text
zoomToSection
highlightSection
openPopup
```

pertenecen al Consumer Adapter o Presentation Controller.

---

## 18.33 EVIDENCE

`EVIDENCE` representa evidencia o referencias de evidencia.

Ejemplo:

```json
{
  "type": "evidence",
  "evidence_id": "EVD-001",
  "source": "..."
}
```

La UI podrá decidir:

- mostrarla completa;
- mostrar un botón;
- mostrar un tooltip;
- ocultarla en modo simple.

---

## 18.34 Evidence remains available

Aunque la UI no la muestre inicialmente, Delivery deberá preservarla si forma parte obligatoria del contrato.

---

## 18.35 WARNING

`WARNING` representa una advertencia formal.

Ejemplo:

```json
{
  "type": "warning",
  "code": "INCOMPLETE_DATA",
  "message": "La información disponible para este indicador es parcial."
}
```

---

## 18.36 Warning Presentation

La UI podrá representar una advertencia como:

- banner;
- icono;
- modal;
- texto;
- badge.

HEYTI no deberá decidirlo.

---

## 18.37 Warning severity

Si existe:

```text
severity
```

deberá expresar significado.

Ejemplo:

```text
INFO
WARNING
CRITICAL
```

No colores.

---

## 18.38 ACTION

`ACTION` representa una acción semántica que el consumidor puede decidir ejecutar.

Ejemplo:

```json
{
  "type": "action",
  "action": "OPEN_MODULE",
  "target": "TERRITORIAL",
  "context": {
    "section_id": "1481"
  }
}
```

---

## 18.39 Action is declarative

Las acciones deberán ser declarativas.

No código.

---

## 18.40 Action Catalog

Podrá existir un catálogo formal.

Ejemplos conceptuales:

```text
OPEN_MODULE
SHOW_SECTION
SHOW_EVIDENCE
OPEN_TERRITORIAL_CONTEXT
OPEN_FIELD_CONTEXT
OPEN_ELECTION_DAY_CONTEXT
```

La taxonomía deberá mantenerse controlada.

---

## 18.41 No DOM actions

Queda prohibido:

```json
{
  "action": "document.getElementById('x').click()"
}
```

---

## 18.42 Consumer resolves action

El consumidor podrá mapear:

```text
OPEN_MODULE / TERRITORIAL
```

a la navegación actual.

Hoy podría significar:

```text
abrir analisis_territorial.html
```

Mañana:

```text
navigate to /territorial
```

HEYTI no cambia.

---

## 18.43 Presentation Model Builder

El Consumer Adapter podrá utilizar conceptualmente:

```text
PresentationModelBuilder
```

para convertir contenido HEYTI a componentes de interfaz.

No deberá residir dentro de `src/heyti/`.

---

## 18.44 Example Presentation Model

```text
PresentationModel
├── title
├── summary
├── KPI cards
├── chart models
├── table models
├── map model
├── warnings
└── actions
```

Esta estructura pertenece al consumidor.

---

## 18.45 Response composition

Una respuesta HEYTI podrá contener varios bloques.

Ejemplo:

```text
DescribeSection Response
├── TEXT
├── METRIC
├── METRIC
├── TABLE
├── SERIES
├── TERRITORIAL_REFERENCE
├── WARNING
└── ACTION
```

---

## 18.46 Block ordering

El contrato deberá definir si el orden posee semántica.

Si Materialization produce una secuencia explícita:

```text
content_blocks
```

Delivery deberá conservarla.

---

## 18.47 Presentation reordering

La UI podrá reordenar visualmente bloques cuando esa libertad esté permitida.

Pero no deberá alterar un orden semántico obligatorio.

---

## 18.48 Section grouping

Los bloques podrán incluir grupos semánticos.

Ejemplo:

```text
electoral
socioeconomic
territorial
operational
```

si Materialization lo define.

Esto puede facilitar la UI.

---

## 18.49 Group is not panel

Un grupo semántico no implica:

```text
HTML panel
```

Presentation podrá decidir cómo representarlo.

---

## 18.50 Layout metadata

El contrato central deberá evitar metadata como:

```text
grid_column
width
height
position
```

salvo que se cree un contrato de Presentation separado.

---

## 18.51 Priority metadata

Si existe una prioridad cognitiva real:

```text
priority = HIGH
```

podrá viajar.

No deberá confundirse con:

```text
display_first = true
```

a menos que Materialization defina semántica de orden.

---

## 18.52 Visualization Hints

La arquitectura podrá evaluar en el futuro el concepto:

```text
visualization_hint
```

como una recomendación no vinculante.

Ejemplo:

```text
visualization_hint = "TIME_SERIES"
```

Sin embargo, deberá utilizarse con cautela.

---

## 18.53 Hints no dependency

Incluso si existe un hint:

```text
TIME_SERIES
```

no deberá especificar:

```text
Chart.js line chart
```

---

## 18.54 v1.0 sin hints si no son necesarios

Para la primera versión deberá preferirse no incluir hints visuales salvo necesidad real.

Los tipos semánticos pueden ser suficientes.

---

## 18.55 Presentation Contract futuro

Si la interfaz requiere una capa formal intermedia, podrá definirse:

```text
HEYTI Presentation Contract
```

fuera del Runtime Response Delivery Contract.

---

## 18.56 Separation of contracts

Conceptualmente:

```text
Response Contract
      ↓
Delivery Contract
      ↓
Consumer Adapter
      ↓
Presentation Contract
      ↓
UI
```

Esta separación protege el Core.

---

## 18.57 Portal Adapter v1

El Portal actual podrá implementar un adapter JavaScript capaz de interpretar:

```text
TEXT
METRIC
TABLE
SERIES
TERRITORIAL_REFERENCE
WARNING
ACTION
```

---

## 18.58 Portal adapter responsibilities

Podrá:

- parsear JSON;
- validar versión;
- transformar bloques;
- actualizar DOM;
- llamar Leaflet;
- llamar Chart.js;
- manejar navegación.

---

## 18.59 Portal adapter prohibited responsibilities

No deberá:

- recalcular reglas cognitivas;
- reinterpretar evidencia;
- inventar datos faltantes;
- modificar confidence;
- consultar bases internas para corregir HEYTI.

---

## 18.60 Data resolution in Presentation

La UI sí podrá resolver recursos de presentación.

Ejemplo:

```text
section_id
      ↓
local map geometry
```

si ese dataset forma parte de la UI.

No deberá reinterpretar conclusiones cognitivas.

---

## 18.61 Shared Data Sources

Si el Portal ya posee:

```text
secciones.geojson
```

puede reutilizarlo para dibujar la sección.

Esto evita enviar geometría repetidamente.

---

## 18.62 Data-source consistency

Sin embargo, deberá garantizarse que la referencia territorial utilizada por HEYTI y la UI corresponda al mismo sistema de identificadores.

---

## 18.63 Data version compatibility

En el futuro podrá ser necesario comparar:

```text
geometry_version
```

o:

```text
dataset_version
```

si existen diferencias temporales.

---

## 18.64 Map Data Mismatch

Si HEYTI devuelve:

```text
section_id = 1481
```

y el mapa del consumidor no reconoce la sección, eso será:

```text
Presentation/Data Integration Error
```

no un error cognitivo.

---

## 18.65 Presentation Error Model

La UI deberá tener su propio manejo de errores.

Ejemplos:

```text
UNSUPPORTED_CONTENT_TYPE
MAP_GEOMETRY_NOT_FOUND
CHART_RENDER_FAILED
ACTION_NOT_SUPPORTED
```

Estos errores no pertenecen a HRRD.

---

## 18.66 Presentation status

Conceptualmente podrá existir:

```text
RECEIVED
PARSED
RENDERED
FAILED
```

fuera del DeliveryResult.

---

## 18.67 End-to-end states

Ejemplo:

```text
Runtime = SUCCESS
Materialization = SUCCESS
Delivery = DELIVERED
Presentation = RENDERED
```

---

## 18.68 Presentation failure

Ejemplo:

```text
Runtime = SUCCESS
Materialization = SUCCESS
Delivery = DELIVERED
Presentation = FAILED
```

HEYTI Delivery continúa siendo exitoso.

---

## 18.69 Consumer parse failure

Si el consumidor recibe JSON pero no puede parsearlo:

- podría indicar corrupción;
- versión incompatible;
- bug del consumidor.

La observabilidad deberá ayudar a localizar la frontera.

---

## 18.70 Contract version check in UI

El Consumer Adapter deberá verificar:

```text
delivery_contract_version
```

antes de interpretar payload.

---

## 18.71 Unsupported contract in UI

Si recibe una versión no soportada, deberá fallar de manera segura.

No deberá intentar adivinar.

---

## 18.72 Unknown Content Type

Si el tipo es opcional y la política lo permite, el Consumer Adapter podrá ignorarlo.

Si es obligatorio, deberá marcar incompatibilidad.

---

## 18.73 Consumer fallback visual

Una UI puede representar un bloque desconocido mediante:

```text
generic textual fallback
```

solo si el contrato lo permite y no inventa significado.

---

## 18.74 Accessibility

Presentation deberá considerar accesibilidad.

Ejemplos:

- contraste;
- texto alternativo;
- navegación por teclado;
- semántica HTML.

Estos aspectos pertenecen a UI.

HEYTI deberá ayudar entregando etiquetas y significado estructurado.

---

## 18.75 Accessible semantics

Un metric con:

```text
label
value
unit
```

es más accesible que un valor sin contexto.

---

## 18.76 Color-independent meaning

HEYTI deberá evitar que el significado dependa exclusivamente de color.

Ejemplo:

```text
status = HIGH_RISK
```

es preferible a:

```text
color = RED
```

---

## 18.77 Localization

HEYTI podrá entregar:

```text
language
```

cuando sea necesario.

Presentation podrá aplicar:

- formatos numéricos;
- fechas;
- traducciones de labels visuales.

---

## 18.78 Raw values first

Para números, HEYTI deberá entregar:

```text
1842
```

y la UI podrá mostrar:

```text
1,842
```

---

## 18.79 Date formatting

HEYTI deberá entregar:

```text
2026-08-20
```

o timestamp formal.

La UI podrá mostrar:

```text
20 de agosto de 2026
```

---

## 18.80 Unit formatting

HEYTI podrá entregar:

```text
unit = percent
```

La UI puede mostrar:

```text
61.4%
```

---

## 18.81 Responsive design

Responsive layout pertenece completamente a Presentation.

No deberá aparecer en Delivery Contract.

---

## 18.82 Mobile vs Desktop

El mismo payload deberá servir para:

```text
desktop
tablet
mobile
```

cuando el consumidor soporte el contrato.

---

## 18.83 ConsumerProfile by device

No deberá crearse un ConsumerProfile diferente para cada tamaño de pantalla si la semántica es la misma.

---

## 18.84 Print views

La UI podrá crear vistas para impresión a partir del mismo contrato.

---

## 18.85 PDF export

Una futura exportación PDF podrá consumir la misma estructura.

Esto demuestra neutralidad.

---

## 18.86 CLI consumer

Incluso un consumidor CLI podría interpretar:

```text
TEXT
METRIC
TABLE
```

sin mapas o gráficas.

---

## 18.87 Consumer-specific capability

El CLI podría declarar que no soporta:

```text
GEOMETRY
```

La compatibilidad deberá respetarlo.

---

## 18.88 Cross-consumer reuse

La misma respuesta podrá alimentar:

```text
Portal
CLI
API
report generator
```

sin modificar cognición.

---

## 18.89 Presentation composition by module

Los seis módulos AT 27–30 podrán utilizar diferentes combinaciones de Content Types.

---

## 18.90 Análisis Territorial

Podrá requerir especialmente:

```text
TEXT
METRIC
SERIES
TABLE
TERRITORIAL_REFERENCE
GEOMETRY
ACTION
```

---

## 18.91 Ganar Todo

Podrá requerir:

```text
TEXT
METRIC
SERIES
TABLE
WARNING
ACTION
```

---

## 18.92 Campo

Podrá requerir:

```text
TEXT
METRIC
TABLE
TERRITORIAL_REFERENCE
WARNING
ACTION
```

y eventualmente puntos geográficos autorizados.

---

## 18.93 Día D

Podrá requerir:

```text
METRIC
TABLE
SERIES
TERRITORIAL_REFERENCE
WARNING
ACTION
```

además de updates en tiempo real en una fase futura.

---

## 18.94 ET-27

Podrá requerir:

```text
TEXT
METRIC
SERIES
TABLE
TERRITORIAL_REFERENCE
```

---

## 18.95 Socioeconómico

Podrá requerir:

```text
TEXT
METRIC
SERIES
TABLE
TERRITORIAL_REFERENCE
```

---

## 18.96 Módulos no determinan Core Contract

Estas combinaciones no deberán convertirse en seis contratos diferentes si pueden representarse mediante un modelo común.

---

## 18.97 Unified content model

La prioridad será:

```text
one semantic content system
```

reutilizable por los seis módulos.

---

## 18.98 Module-specific UI adapters

Cada módulo podrá tener una adaptación visual especializada.

---

## 18.99 HEYTI unified UI

Una futura interfaz unificada podrá interpretar todos los Content Types desde un único Consumer Adapter.

---

## 18.100 User journey

Una experiencia futura podrá ser:

```text
User selects section
      ↓
HEYTI receives query
      ↓
DescribeSection
      ↓
Delivery
      ↓
UI shows section radiography
      ↓
User asks another question
      ↓
HEYTI responds
      ↓
UI opens specialized module if needed
```

La navegación deberá ocurrir en Presentation.

---

## 18.101 Radiografía de sección

Una respuesta de radiografía podrá incluir:

```text
summary
electoral metrics
historical series
socioeconomic metrics
territorial reference
warnings
recommended actions
```

sin especificar layout.

---

## 18.102 Preference question

La interfaz podrá preguntar al usuario qué desea explorar a continuación.

Esta lógica pertenece a Interaction/Presentation, salvo que una futura capability genere opciones cognitivas.

---

## 18.103 Module opening

Una acción semántica podrá indicar:

```text
OPEN_MODULE
target = CAMPO
```

La UI realizará el cambio.

---

## 18.104 Close previous module

La regla:

```text
open one module, close previous
```

pertenece completamente al Portal/UI.

No a Delivery.

---

## 18.105 Navigation buttons

Los botones son Presentation.

HEYTI podrá proporcionar acciones.

No botones HTML.

---

## 18.106 Visual consistency

La UI deberá mantener un lenguaje visual coherente.

Esto no afecta la arquitectura de Delivery.

---

## 18.107 Visual hierarchy

La UI podrá decidir que:

- resumen va primero;
- KPIs arriba;
- mapa al centro;
- warnings visibles.

HEYTI solo preservará estructura semántica.

---

## 18.108 No hidden warnings

Aunque Presentation tenga libertad visual, no deberá ocultar advertencias obligatorias de manera engañosa.

Esto debe formar parte del contrato de integración.

---

## 18.109 Honest Presentation

La UI deberá conservar:

```text
partial
uncertain
warning
not available
```

de manera honesta.

---

## 18.110 Null Presentation

Si HEYTI entrega:

```text
null
```

la UI podrá mostrar:

```text
Sin dato disponible
```

pero no:

```text
0
```

salvo que ese sea el significado contractual.

---

## 18.111 Partial responses

Ejemplo:

```text
response.status = PARTIAL
delivery.status = DELIVERED
```

La UI deberá representar la incompletitud.

---

## 18.112 Evidence visibility

Podrá existir un modo:

```text
Ver evidencia
```

como interacción visual.

La evidencia ya deberá venir referenciada correctamente.

---

## 18.113 Trace visibility

La UI de soporte podrá mostrar:

```text
response_id
delivery_id
knowledge_version
```

La UI ordinaria puede ocultarlos.

---

## 18.114 Advanced mode

Podría existir un modo avanzado para:

- analistas;
- auditores;
- desarrolladores.

No forma parte de HRRD.

---

## 18.115 Presentation and Security

El Consumer Adapter deberá respetar la proyección autorizada recibida.

No deberá intentar consultar recursos internos para obtener datos ocultos.

---

## 18.116 Client-side authorization is insufficient

Aunque UI oculte contenido, la autorización real debe haber ocurrido antes de Delivery.

---

## 18.117 Presentation actions authorization

Una acción recibida deberá validarse también desde el lado consumidor antes de ejecutarse.

---

## 18.118 Navigation allowlist

El Portal podrá tener un mapping como:

```text
TERRITORIAL → valid internal route
CAMPO → valid internal route
DIA_D → valid internal route
```

No URLs arbitrarias.

---

## 18.119 No action eval

Se mantiene prohibido:

```text
eval()
```

para acciones recibidas.

---

## 18.120 Presentation testing

La integración visual deberá tener pruebas propias.

---

## 18.121 Contract parsing test

```text
test_portal_adapter_parses_delivery_contract_v1
```

---

## 18.122 TEXT test

```text
test_text_block_maps_to_text_model
```

---

## 18.123 METRIC test

```text
test_metric_maps_to_kpi_model
```

---

## 18.124 SERIES test

```text
test_series_maps_to_chart_model
```

---

## 18.125 TERRITORIAL_REFERENCE test

```text
test_territorial_reference_resolves_section
```

---

## 18.126 ACTION test

```text
test_open_module_action_is_allowlisted
```

---

## 18.127 Warning test

```text
test_warning_is_not_dropped
```

---

## 18.128 Null test

```text
test_null_is_not_rendered_as_zero
```

---

## 18.129 Contract version test

```text
test_unsupported_contract_version_fails_safely
```

---

## 18.130 Integration test

Conceptually:

```text
DescribeSection
      ↓
Delivery JSON
      ↓
Portal Adapter
      ↓
Presentation Model
```

deberá producir bloques correctos.

---

## 18.131 Visual test

Después podrán existir pruebas visuales o screenshots.

Estas pertenecen a la UI.

---

## 18.132 No visual testing in Core

HEYTI Core no deberá depender de screenshots para validar Delivery.

---

## 18.133 Data coverage audit

Antes de implementar visualización completa deberá verificarse la disponibilidad real de datos para los seis módulos.

Este punto será obligatorio para evitar construir una interfaz que prometa información que HEYTI no puede producir.

---

## 18.134 Objetivo de cobertura

La auditoría deberá responder para cada módulo:

```text
What questions should HEYTI answer?
Which data sources are required?
Which sources exist?
Which are complete?
Which are partial?
Which are outdated?
Which are missing?
```

---

## 18.135 Análisis Territorial — auditoría de fuentes

Deberán revisarse al menos las fuentes necesarias para:

- identificación territorial;
- históricos electorales;
- geometría;
- lista nominal;
- comparaciones;
- indicadores estratégicos.

---

## 18.136 Ganar Todo — auditoría de fuentes

Deberá verificarse información necesaria para:

- competitividad;
- objetivos;
- escenarios;
- prioridades;
- simulaciones;
- resultados históricos.

---

## 18.137 Campo — auditoría de fuentes

Deberá revisarse:

- puntos de campo;
- duplicados;
- contactos;
- estatus;
- referencias territoriales;
- datos operativos autorizados.

---

## 18.138 Día D — auditoría de fuentes

Deberá verificarse:

- casillas;
- georreferencias;
- estatus;
- incidencias;
- cobertura;
- actualización temporal.

---

## 18.139 ET-27 — auditoría de fuentes

Deberá revisarse:

- cobertura;
- representantes;
- semáforos;
- secciones históricas;
- indicadores de organización territorial.

---

## 18.140 Socioeconómico — auditoría de fuentes

Deberá revisarse:

- indicadores;
- años;
- cobertura territorial;
- calidad;
- agregados;
- unidades.

---

## 18.141 No UI before truth

La regla será:

> **La interfaz no deberá prometer una capacidad que las fuentes de datos no puedan respaldar.**

---

## 18.142 Missing source behavior

Si una fuente no existe o está incompleta:

```text
HEYTI response
```

deberá representarlo explícitamente mediante:

```text
warning
partial status
null
```

según contrato.

---

## 18.143 Presentation response to missing data

La UI podrá mostrar:

```text
Información no disponible
```

o una advertencia equivalente.

No deberá inventar un valor.

---

## 18.144 Visual source alignment

Cada gráfica, mapa o KPI deberá poder rastrearse hasta los datos entregados por HEYTI.

---

## 18.145 No independent UI calculation by default

La UI no deberá recalcular indicadores estratégicos por su cuenta si HEYTI ya los materializa.

Esto puede producir divergencias.

---

## 18.146 Presentation-only calculations

Sí podrá realizar cálculos puramente visuales como:

```text
pixel sizes
axis scaling
sorting for display
```

cuando no alteren significado.

---

## 18.147 Sorting caution

Si el orden es semántico, la UI deberá preservarlo.

---

## 18.148 Chart scaling

Cambiar escala visual no deberá distorsionar interpretación.

Este aspecto pertenece a buenas prácticas de visualización.

---

## 18.149 Map scale

La UI deberá evitar representar referencias territoriales con geometría incorrecta o desactualizada.

---

## 18.150 Visualization provenance

En una futura interfaz avanzada podría mostrarse:

```text
Fuente
Fecha del dato
Versión de conocimiento
```

si el contrato lo entrega.

---

## 18.151 Exportability

La neutralidad del modelo permitirá exportar la misma respuesta a:

```text
screen
PDF
report
API
```

sin modificar la cognición.

---

## 18.152 Print/PDF consumer

Un generador de informes podría ser otro ConsumerProfile.

---

## 18.153 Dashboard consumer

También podría existir un dashboard administrativo como consumidor.

---

## 18.154 Presentation-specific cache

La UI podrá cachear geometrías o recursos.

No deberá alterar Delivery.

---

## 18.155 Delivery cache future

Un eventual cache de respuestas pertenece a otra decisión arquitectónica.

No deberá mezclarse con Presentation cache.

---

## 18.156 UX latency

El usuario percibirá el tiempo total:

```text
request
+
runtime
+
materialization
+
delivery
+
presentation
```

La observabilidad deberá distinguir cada parte.

---

## 18.157 Loading state

La UI podrá mostrar:

```text
HEYTI está procesando...
```

durante espera.

Esto pertenece a Presentation.

---

## 18.158 Streaming UX

Si en el futuro se requieren respuestas progresivas, se necesitará un contrato streaming separado.

---

## 18.159 No fake streaming

La UI no deberá simular contenido parcial como si HEYTI ya lo hubiera producido.

---

## 18.160 Presentation acknowledgement

Podría existir en el futuro un evento:

```text
presentation.rendered
```

para observabilidad end-to-end.

No cambia el DeliveryResult original.

---

## 18.161 Consumer telemetry

La UI podrá enviar telemetría como:

```text
render_success
render_failure
interaction
```

mediante una frontera separada.

---

## 18.162 No circular Delivery

La telemetría de UI no deberá reingresar al mismo pipeline como una respuesta HEYTI.

Es otro tipo de evento.

---

## 18.163 Content hierarchy

Una respuesta podría tener:

```text
content:
  primary
  supporting
  warnings
  actions
```

si Materialization adopta este modelo.

La jerarquía deberá ser semántica.

---

## 18.164 Primary vs supporting

`primary` podría indicar información central.

No posición visual exacta.

---

## 18.165 Presentation mapping example

```text
primary metric
      ↓
large KPI card
```

es una decisión de UI.

---

## 18.166 Semantic label

Los bloques deberán tener labels suficientes para que la UI no tenga que inferir.

Ejemplo:

```text
label = Participación
```

---

## 18.167 Stable keys

Además del label humano, podrán utilizarse keys estables.

Ejemplo:

```text
key = participation
label = Participación
```

Esto facilita:

- traducción;
- UI mapping;
- pruebas.

---

## 18.168 Key vs label

`key` es identidad semántica.

`label` es texto de presentación sugerido.

---

## 18.169 Translation

En el futuro, la UI podría traducir:

```text
key = participation
```

a otro idioma.

---

## 18.170 Label preservation

Si HEYTI produce un label con significado específico, deberá preservarse como fallback.

---

## 18.171 Unit vocabulary

Deberá existir un vocabulario estable.

Ejemplos:

```text
percent
votes
persons
households
points
score
```

---

## 18.172 UI formatting map

Presentation podrá convertir:

```text
percent → %
votes → votos
```

---

## 18.173 Status vocabulary

También podrá existir vocabulario:

```text
HIGH
MEDIUM
LOW
PARTIAL
UNKNOWN
```

si esos estados son semánticos.

---

## 18.174 Avoid color statuses

No:

```text
RED
YELLOW
GREEN
```

como primera semántica si realmente significan:

```text
HIGH_RISK
MEDIUM_RISK
LOW_RISK
```

---

## 18.175 Semáforos ET-27

Si el dominio ya utiliza semáforos como concepto de negocio formal, deberá distinguirse:

```text
business semantic status
```

de:

```text
CSS color
```

---

## 18.176 Semantic semáforo

Ejemplo:

```text
status = CRITICAL
```

La UI puede representarlo en rojo.

---

## 18.177 No color-only semantics

Esto facilita accesibilidad y portabilidad.

---

## 18.178 Tooltips

Tooltips son Presentation.

HEYTI podrá entregar:

```text
description
```

si existe significado útil.

---

## 18.179 Drill-down

Una acción podrá habilitar drill-down:

```text
SHOW_EVIDENCE
OPEN_MODULE
SHOW_SECTION
```

La UI implementa la navegación.

---

## 18.180 Cross-module context

Una acción podrá conservar:

```text
section_id
municipality_id
```

al abrir otro módulo.

---

## 18.181 Context handoff

El Portal deberá propagar el contexto semántico.

No extraerlo de texto narrativo.

---

## 18.182 Example

Incorrecto:

```text
parse "Sección 1481" from narrative
```

Correcto:

```text
action.context.section_id = "1481"
```

---

## 18.183 Consumer contract parsing

Los Consumers deberán utilizar fields estructurados.

No técnicas frágiles de parsing textual.

---

## 18.184 Presentation fallback hierarchy

Una UI podría implementar:

```text
known structured type
      ↓
specific component

unknown optional type
      ↓
generic renderer / ignore safely

invalid required type
      ↓
presentation error
```

---

## 18.185 No hidden contract error

Un consumer no deberá simplemente ignorar un bloque obligatorio que no comprende.

---

## 18.186 Presentation and deprecation

Si recibe una versión deprecada todavía soportada, podrá funcionar y registrar warning.

---

## 18.187 Presentation migration

El Consumer Adapter deberá evolucionar antes del retiro de una versión antigua.

---

## 18.188 UI contract tests

Cada cambio del Consumer Adapter deberá ejecutar fixtures de Delivery reales o canónicos.

---

## 18.189 Golden payloads for UI

Podrán utilizarse fixtures como:

```text
describe_section_success_v1.json
describe_section_partial_v1.json
delivery_error_v1.json
```

---

## 18.190 UI regression

Esto ayudará a detectar cuando un cambio visual rompe interpretación contractual.

---

## 18.191 End-to-end vertical slice

La primera integración completa deberá recorrer:

```text
Known Section
      ↓
DescribeSection
      ↓
Materialization
      ↓
Delivery
      ↓
Gateway
      ↓
Portal Adapter
      ↓
TEXT + METRIC + MAP CONTEXT
```

---

## 18.192 First target capability

`DescribeSection` es una candidata natural porque ya está integrada en la evolución del Runtime y representa una radiografía territorial útil.

---

## 18.193 First visual success criterion

La primera vertical slice será exitosa cuando:

1. el usuario consulte una sección;
2. HEYTI produzca una respuesta;
3. Delivery la entregue;
4. Portal la interprete;
5. se muestre contenido estructurado;
6. la sección se relacione con el mapa;
7. la trazabilidad permanezca intacta.

---

## 18.194 No direct provider call from UI

El Portal no deberá llamar directamente:

```text
DescribeSectionProvider
```

o estructuras internas.

Debe hacerlo a través de Gateway/Runtime.

---

## 18.195 UI remains replaceable

Esto permitirá sustituir el Portal sin modificar DescribeSection.

---

## 18.196 Presentation Architecture future

La futura UI podrá tener una estructura semejante a:

```text
ui/
├── heyti-client
├── delivery-contract-parser
├── presentation-models
├── renderers
│   ├── text
│   ├── metric
│   ├── table
│   ├── series
│   ├── map
│   └── warning
└── actions
```

Esto es conceptual.

---

## 18.197 No forced framework

La arquitectura no exige React, Vue, Angular u otro framework.

El Portal actual puede evolucionar con JavaScript existente.

---

## 18.198 Progressive integration

La estrategia podrá ser:

```text
existing Portal
      ↓
HEYTI response panel
      ↓
structured renderers
      ↓
module integration
      ↓
future unified UI
```

---

## 18.199 Preserve existing modules

No es necesario desechar los módulos actuales.

Podrán funcionar como superficies visuales durante la transición.

---

## 18.200 Module bridge

Una acción HEYTI podrá actuar como puente hacia el módulo existente.

---

## 18.201 Module data duplication

Deberá revisarse si los módulos continúan consultando fuentes locales mientras HEYTI consulta PostgreSQL/PostGIS.

La divergencia deberá evitarse.

---

## 18.202 Single source of truth future

La meta deberá ser que, progresivamente, HEYTI y los módulos utilicen fuentes consistentes.

---

## 18.203 Source validation gate

Antes de migrar cada visualización deberá comprobarse:

```text
source exists
source complete
source current
source mapped
source tested
```

---

## 18.204 Six-module coverage matrix

Deberá construirse, antes o durante la fase visual, una matriz que cruce:

```text
Module
Question
Capability
Required Data
Source
Coverage
Delivery Content Type
Presentation Component
```

---

## 18.205 Example matrix row

```text
Module: Socioeconómico
Question: ¿Cuál es la población de la sección?
Capability: DescribeSection / future socioeconomic capability
Source: socioeconomico.section_indicator
Content Type: METRIC
Presentation: KPI / table
```

---

## 18.206 Coverage status

Podrán utilizarse estados:

```text
READY
PARTIAL
MISSING
UNVERIFIED
```

para la matriz.

---

## 18.207 No green without evidence

Una fuente no deberá marcarse `READY` únicamente porque exista una tabla.

Deberá verificarse:

- cobertura;
- calidad;
- consistencia;
- actualización.

---

## 18.208 Delivery readiness

Una visualización solo deberá activarse cuando el Content Type correspondiente esté correctamente materializado y entregado.

---

## 18.209 UI readiness

Además deberá existir un renderer probado.

---

## 18.210 End-to-end readiness

La capacidad estará realmente lista cuando:

```text
Source
→ Knowledge
→ Capability
→ Materialization
→ Delivery
→ Consumer
→ Presentation
```

funcione de extremo a extremo.

---

## 18.211 Invariantes Presentation/Delivery

Se establecen los siguientes invariantes.

### HRRD-PRES01 — Presentation After Delivery

La presentación comienza únicamente después de la frontera de Delivery.

### HRRD-PRES02 — Semantic Content

HEYTI entregará contenido semántico, no instrucciones visuales específicas.

### HRRD-PRES03 — Consumer Adapter

La traducción a UI deberá ocurrir en un adapter del consumidor.

### HRRD-PRES04 — No Visual Dependency in Core

HEYTI Core no dependerá de HTML, CSS, DOM, Leaflet o Chart.js.

### HRRD-PRES05 — Structured Data First

Gráficas, mapas, KPIs y tablas deberán construirse a partir de datos estructurados.

### HRRD-PRES06 — Warning Preservation

Presentation no deberá ocultar advertencias obligatorias.

### HRRD-PRES07 — Null Preservation

Valores ausentes no deberán convertirse arbitrariamente en cero.

### HRRD-PRES08 — Declarative Actions

Las acciones serán semánticas y declarativas.

### HRRD-PRES09 — Source Readiness

Ninguna capacidad visual deberá activarse sin datos suficientes y verificados.

### HRRD-PRES10 — Replaceable Presentation

La UI podrá cambiar sin modificar la semántica cognitiva de HEYTI.

---

## 18.212 Prueba de neutralidad visual

Un payload deberá poder ser interpretado conceptualmente por:

```text
web UI
CLI
report generator
test harness
```

sin modificar su significado.

---

## 18.213 Prueba de gráfica

Una `SERIES` deberá poder representarse como:

```text
line chart
bar chart
table
```

sin cambiar el payload.

---

## 18.214 Prueba de mapa

Una `TERRITORIAL_REFERENCE` deberá poder ser resuelta por:

```text
Leaflet
another mapping library
```

sin modificar HEYTI Core.

---

## 18.215 Prueba de KPI

Un `METRIC` deberá poder mostrarse como:

```text
card
table cell
text
```

---

## 18.216 Prueba de acciones

Una acción:

```text
OPEN_MODULE
```

deberá ser interpretable sin contener código ejecutable.

---

## 18.217 Prueba de advertencia

Un warning obligatorio deberá sobrevivir:

```text
Materialization
→ Delivery
→ Consumer Adapter
→ Presentation Model
```

---

## 18.218 Prueba de null

Un `null` contractual deberá permanecer distinguible de `0` hasta Presentation.

---

## 18.219 Prueba de data coverage

Cada visualización deberá poder asociarse con una fuente validada.

---

## 18.220 Prueba de consumer replacement

Una nueva UI deberá poder utilizar el mismo contrato sin cambios en capabilities.

---

## 18.221 MVP visual posterior al Sprint 23

Una primera integración visual deberá limitarse a un subconjunto controlado:

```text
TEXT
METRIC
TERRITORIAL_REFERENCE
WARNING
ACTION
```

si son suficientes para `DescribeSection`.

---

## 18.222 Gráficas posteriores

`SERIES` deberá incorporarse cuando exista un caso de uso estable y fuentes verificadas.

---

## 18.223 Tablas posteriores

`TABLE` podrá incorporarse de manera temprana si ayuda a mostrar evidencia o históricos.

---

## 18.224 Mapas

El mapa será una pieza central del contexto territorial y deberá integrarse utilizando referencias estructuradas.

---

## 18.225 Estadísticas

Las estadísticas deberán provenir de valores materializados.

No de cálculos duplicados de JavaScript salvo que sean puramente de Presentation.

---

## 18.226 Acciones de navegación

Las acciones permitirán conectar HEYTI con los seis módulos sin acoplar el Core a sus archivos actuales.

---

## 18.227 Flujo visual conceptual

```text
HEYTI Response
      ↓
Delivery Contract
      ↓
Portal Consumer Adapter
      ↓
PresentationModel
      ├── TextRenderer
      ├── MetricRenderer
      ├── TableRenderer
      ├── SeriesRenderer
      ├── MapRenderer
      └── ActionHandler
```

---

## 18.228 Flujo territorial conceptual

```text
TERRITORIAL_REFERENCE
      ↓
Portal Adapter
      ↓
Geometry Resolver
      ↓
Leaflet
      ↓
Highlight Section
```

---

## 18.229 Flujo gráfico conceptual

```text
SERIES
      ↓
Portal Adapter
      ↓
Chart Model
      ↓
Chart.js
```

---

## 18.230 Flujo KPI conceptual

```text
METRIC
      ↓
Portal Adapter
      ↓
KPI Model
      ↓
HTML Component
```

---

## 18.231 Flujo Action conceptual

```text
ACTION
OPEN_MODULE
target = CAMPO
      ↓
Action Handler
      ↓
Portal Navigation
      ↓
Campo Module
```

---

## 18.232 Criterio de éxito arquitectónico

La integración con Presentation será considerada correcta cuando:

1. HEYTI pueda entregar contenido sin conocimiento de UI;
2. el consumidor pueda construir texto, KPIs, tablas, gráficas y mapas;
3. las acciones sean declarativas;
4. los datos faltantes permanezcan explícitos;
5. advertencias y evidencia puedan preservarse;
6. cambiar Leaflet o Chart.js no afecte el Core;
7. cambiar completamente la UI no afecte Materialization;
8. los seis módulos puedan evolucionar como superficies compatibles;
9. cada visualización tenga fuentes de datos verificadas;
10. la trazabilidad continúe hasta la frontera de Presentation.

---

## 18.233 Declaración arquitectónica del capítulo

Runtime Response Delivery deberá preparar HEYTI para una experiencia visual rica sin convertir el Core en un framework de interfaz.

HEYTI deberá ser capaz de entregar:

- narrativa;
- métricas;
- series;
- tablas;
- referencias territoriales;
- geometría cuando sea necesaria;
- evidencia;
- advertencias;
- acciones.

La UI podrá convertir estos elementos en:

- tarjetas;
- mapas;
- gráficas;
- tablas;
- paneles;
- navegación;
- experiencias interactivas.

La regla arquitectónica consolidada queda establecida como:

> **HEYTI deberá expresar la semántica suficiente para que cualquier consumidor autorizado pueda construir una representación visual completa, pero ninguna decisión específica de layout, estilo, librería gráfica, librería cartográfica, DOM o navegación deberá contaminar Runtime Response Delivery.**

La frontera queda formalizada como:

```text
HEYTI Meaning
      ↓
Materialization
      ↓
Delivery Contract
      ↓
Consumer Adapter
      ↓
Presentation Model
      ↓
Text / KPI / Table / Chart / Map / Action
```

Y queda establecida además una condición operativa crítica para la fase visual:

> **Antes de habilitar una representación de los seis módulos AT 27–30, deberá auditarse y validar la cobertura real de las fuentes necesarias para producir esa respuesta, evitando interfaces visualmente completas construidas sobre datos incompletos, inconsistentes o no verificados.**

Con esta arquitectura de Presentation preparada queda lista la siguiente dimensión del documento:

**estrategia formal de pruebas, verificación, certificación y criterios de aceptación de Runtime Response Delivery.**

---

**Fin del Capítulo 18**


# Capítulo 19. Estrategia formal de pruebas, verificación, certificación y criterios de aceptación de Runtime Response Delivery

## 19.1 Propósito del capítulo

Este capítulo define la estrategia formal mediante la cual **HEYTI Runtime Response Delivery (HRRD)** deberá ser probado, verificado y certificado antes de considerarse listo para integración real.

La finalidad es evitar que la arquitectura descrita en los capítulos anteriores quede únicamente como intención documental.

Runtime Response Delivery deberá demostrar mediante evidencia técnica que cumple con:

```text
contratos
validación
serialización
trazabilidad
consumer compatibility
adapter substitution
seguridad
versionado
observabilidad
independencia de Presentation
```

La regla fundamental será:

> **Ninguna característica crítica de Delivery deberá considerarse implementada únicamente porque exista código; deberá existir una prueba que demuestre su comportamiento esperado y una evidencia verificable de que dicha prueba fue superada.**

---

## 19.2 Prueba como evidencia arquitectónica

En HRRD una prueba no deberá considerarse únicamente una herramienta de detección de bugs.

También deberá actuar como:

```text
Architectural Evidence
```

capaz de demostrar que una decisión de diseño realmente se preserva en implementación.

Ejemplo:

```text
Principle:
Adapter must not mutate response.

Evidence:
test_adapter_does_not_mutate_payload
```

---

## 19.3 Relación entre especificación y pruebas

Cada regla relevante del documento deberá poder traducirse, cuando sea razonable, a uno o más tests.

Conceptualmente:

```text
Architectural Principle
      ↓
Invariant
      ↓
Test
      ↓
Evidence
```

---

## 19.4 Capas de prueba

Se establecen cinco niveles principales:

```text
1. Unit Tests
2. Contract Tests
3. Integration Tests
4. End-to-End Tests
5. Architectural Conformance Tests
```

No todas las pruebas deberán implementarse en el mismo momento.

La cobertura deberá crecer conforme aumente la superficie de integración.

---

## 19.5 Unit Tests

Los Unit Tests deberán verificar componentes aislados.

Ejemplos:

```text
validators
serializers
context
contracts
consumer registry
adapter registry
in-memory adapter
error mapper
```

Deberán ser:

- rápidos;
- deterministas;
- independientes de red;
- independientes de UI;
- independientes de PostgreSQL salvo necesidad explícita.

---

## 19.6 Contract Tests

Los Contract Tests deberán verificar que las estructuras públicas cumplen sus reglas.

Ejemplos:

```text
DeliveryEnvelope
DeliveryResult
DeliveryError
ConsumerProfile
DeliveryTrace
```

La pregunta será:

> ¿La estructura producida cumple exactamente el contrato prometido?

---

## 19.7 Integration Tests

Los Integration Tests deberán probar la interacción entre componentes de HRRD.

Ejemplo:

```text
MaterializedResponse
      ↓
Validator
      ↓
Serializer
      ↓
Adapter
      ↓
DeliveryResult
```

Sin requerir todavía una UI real.

---

## 19.8 End-to-End Tests

Los End-to-End Tests deberán recorrer una vertical completa.

Ejemplo futuro:

```text
Request
→ Runtime
→ DescribeSection
→ Materialization
→ Delivery
→ Gateway
→ Consumer
```

Posteriormente podrá agregarse Presentation.

---

## 19.9 Architectural Conformance Tests

Estas pruebas deberán verificar propiedades estructurales difíciles de capturar únicamente mediante casos funcionales.

Ejemplos:

```text
Delivery package does not import Leaflet/DOM code
Capability implementation does not depend on Gateway
Adapter does not alter Response Contract
```

---

## 19.10 Test Pyramid

La estrategia deberá favorecer una pirámide:

```text
          End-to-End
             /\
            /  \
       Integration
          /    \
         /      \
        Contract
       /          \
      /            \
     Unit Tests
```

La mayoría deberán ser Unit y Contract Tests.

Los End-to-End deberán ser menos numerosos, pero más representativos.

---

## 19.11 Determinismo

Las pruebas deberán ser deterministas.

Dado:

```text
same input
same configuration
```

deberán producir:

```text
same expected result
```

salvo campos variables controlados.

---

## 19.12 Campos variables

Campos como:

```text
delivery_id
timestamps
duration_ms
```

podrán variar.

Los tests deberán:

- inyectar generadores deterministas;
- congelar tiempo;
- o validar propiedades en lugar de valores exactos.

---

## 19.13 ID Generator Testability

La generación de identificadores deberá poder ser sustituida en pruebas.

Conceptualmente:

```text
Real ID Generator
      ↓
Production
```

y:

```text
Deterministic ID Generator
      ↓
Tests
```

---

## 19.14 Clock Testability

De manera similar, el tiempo deberá poder controlarse.

Ejemplo conceptual:

```text
Clock
├── SystemClock
└── FixedClock
```

Solo deberá introducirse una abstracción si simplifica realmente las pruebas.

---

## 19.15 No sleep-based tests

Deberá evitarse:

```python
time.sleep(...)
```

para verificar duración o timeout cuando pueda simularse.

Estos tests son lentos y frágiles.

---

## 19.16 Test Fixtures

Deberán existir fixtures representativos de respuestas materializadas.

Ejemplos:

```text
valid_response
partial_response
response_with_warning
response_with_metric
response_with_series
response_with_territorial_reference
```

---

## 19.17 Fixture mínima

Una fixture mínima deberá representar la respuesta más pequeña válida soportada por Delivery.

---

## 19.18 Fixture rica

Una fixture rica deberá representar:

```text
text
metric
table
series
warnings
evidence
trace
```

si estos elementos forman parte del contrato.

---

## 19.19 Negative Fixtures

También deberán existir estructuras deliberadamente inválidas.

Ejemplos:

```text
missing response_id
invalid contract version
invalid status
unknown consumer
unsupported content type
unserializable object
```

---

## 19.20 Golden Fixtures

Podrán conservarse payloads canónicos.

Ejemplos:

```text
delivery_success_v1.json
delivery_failed_v1.json
delivery_rejected_v1.json
```

Estas fixtures ayudarán a detectar regresiones contractuales.

---

## 19.21 No snapshot blindness

Las pruebas snapshot deberán revisarse conscientemente.

No deberá aprobarse una nueva salida únicamente actualizando el snapshot.

---

## 19.22 Unit Tests — Contracts

Deberán existir tests para:

```text
DeliveryEnvelope
DeliveryResult
DeliveryError
DeliveryTrace
DeliveryContext
ConsumerProfile
AdapterResult
```

---

## 19.23 DeliveryEnvelope Tests

Ejemplos:

```text
test_delivery_envelope_requires_delivery_id
test_delivery_envelope_requires_contract_version
test_delivery_envelope_preserves_response
test_delivery_envelope_preserves_trace
```

---

## 19.24 DeliveryResult Tests

Ejemplos:

```text
test_delivered_result_has_no_fatal_error
test_failed_result_requires_error
test_rejected_result_requires_error
test_result_preserves_response_id
test_result_preserves_delivery_id
```

---

## 19.25 DeliveryError Tests

Ejemplos:

```text
test_error_code_is_required
test_error_category_is_valid
test_error_stage_is_valid
test_error_is_serializable
```

---

## 19.26 DeliveryTrace Tests

Ejemplos:

```text
test_trace_preserves_request_id
test_trace_preserves_execution_id
test_trace_preserves_response_id
test_trace_preserves_delivery_id
test_trace_preserves_consumer_id
test_trace_preserves_adapter_id
```

---

## 19.27 DeliveryContext Tests

Ejemplos:

```text
test_context_is_explicit
test_context_rejects_inconsistent_response_id
test_context_allows_optional_session
test_context_rejects_required_missing_session
```

---

## 19.28 ConsumerProfile Tests

Ejemplos:

```text
test_profile_requires_consumer_id
test_profile_requires_supported_contract
test_profile_rejects_unknown_content_type
test_profile_can_be_disabled
```

---

## 19.29 AdapterResult Tests

Ejemplos:

```text
test_adapter_result_success_has_no_error
test_adapter_result_failure_has_error
test_adapter_result_is_normalizable
```

---

## 19.30 Validator Tests

La validación deberá poseer pruebas positivas y negativas.

---

## 19.31 Positive Validation Tests

```text
test_valid_response_passes
test_valid_context_passes
test_valid_consumer_passes
test_valid_payload_passes
```

---

## 19.32 Negative Validation Tests

```text
test_missing_required_field_fails
test_invalid_enum_fails
test_invalid_version_fails
test_incompatible_consumer_fails
test_invalid_payload_fails
```

---

## 19.33 Zero Omission Test Rule

Para cada campo obligatorio deberá existir una prueba que lo elimine deliberadamente.

Ejemplo:

```text
Valid Contract
      ↓
Remove required field
      ↓
Validation MUST fail
```

Esta regla será una pieza central de:

```text
0 ERRORES
0 OMISIONES
```

---

## 19.34 Type Corruption Tests

Además de eliminar campos, deberán probarse tipos incorrectos.

Ejemplo:

```text
delivery_id = 123
```

cuando contractualmente debe ser string.

---

## 19.35 Value Corruption Tests

Ejemplo:

```text
status = "SUCCESS"
```

cuando el DeliveryStatus válido es:

```text
DELIVERED
REJECTED
FAILED
```

---

## 19.36 Semantic Invariant Tests

Ejemplos:

```text
FAILED without error → invalid
DELIVERED with fatal error → invalid
completed_at before started_at → invalid
```

---

## 19.37 Serializer Tests

La serialización deberá probarse ampliamente.

---

## 19.38 Primitive Serialization Tests

```text
test_serialize_none
test_serialize_boolean
test_serialize_integer
test_serialize_float
test_serialize_string
```

---

## 19.39 Complex Serialization Tests

```text
test_serialize_uuid
test_serialize_enum
test_serialize_date
test_serialize_datetime
test_serialize_list
test_serialize_nested_dict
```

---

## 19.40 Unsupported Type Test

```text
test_unsupported_type_fails_explicitly
```

Será obligatorio.

---

## 19.41 No generic str fallback test

Deberá comprobarse que un objeto no soportado no se convierta automáticamente mediante:

```text
str(obj)
```

---

## 19.42 Null Preservation Test

```text
test_null_remains_null
```

---

## 19.43 Identifier Preservation Test

Ejemplo:

```text
"0012"
```

deberá permanecer:

```text
"0012"
```

si es identificador.

---

## 19.44 Timezone Test

Un datetime timezone-aware deberá conservar su offset o normalización definida.

---

## 19.45 Semantic Round Trip Test

Conceptualmente:

```text
Object
→ serialize
→ deserialize
→ equivalent semantics
```

Deberá probarse al menos para estructuras críticas.

---

## 19.46 Required Field Preservation Test

Deberá verificarse explícitamente que serializar no omite campos obligatorios.

---

## 19.47 Warning Preservation Test

```text
test_warning_survives_serialization
```

---

## 19.48 Evidence Preservation Test

```text
test_evidence_reference_survives_serialization
```

---

## 19.49 Consumer Registry Tests

Deberán incluir:

```text
test_register_consumer
test_resolve_consumer
test_reject_duplicate_consumer
test_unknown_consumer
```

---

## 19.50 Consumer Compatibility Tests

```text
test_supported_contract_is_compatible
test_unsupported_contract_is_incompatible
test_required_content_types_supported
test_missing_required_content_type_rejected
```

---

## 19.51 Disabled Consumer Test

```text
test_disabled_consumer_is_rejected
```

---

## 19.52 Adapter Registry Tests

```text
test_register_adapter
test_resolve_adapter
test_reject_duplicate_adapter
test_unknown_adapter
```

---

## 19.53 InMemory Adapter Tests

Como adapter base del Sprint 23 deberá tener cobertura completa.

Ejemplos:

```text
test_inmemory_delivers_payload
test_inmemory_captures_payload
test_inmemory_returns_success
test_inmemory_preserves_context
test_inmemory_does_not_mutate_payload
```

---

## 19.54 Failing Adapter Tests

Deberá ser posible simular:

```text
adapter failure
```

y verificar:

```text
DeliveryResult = FAILED
```

---

## 19.55 Timeout Simulation

La futura lógica de timeout deberá poder simularse sin esperar tiempo real.

---

## 19.56 Adapter Error Mapping Tests

Ejemplos:

```text
test_target_unavailable_maps_correctly
test_timeout_maps_correctly
test_adapter_internal_failure_maps_correctly
```

---

## 19.57 Adapter Substitution Test

Esta prueba será arquitectónicamente crítica.

La misma respuesta deberá poder entregarse mediante:

```text
Adapter A
Adapter B
```

sin alterar:

```text
response_id
response content
contract semantics
```

---

## 19.58 Consumer Substitution Test

La misma respuesta deberá poder dirigirse a dos Consumers compatibles.

El contenido cognitivo deberá permanecer igual.

---

## 19.59 Context Tests

Deberán verificarse:

```text
session preservation
request preservation
execution preservation
consumer preservation
correlation preservation
```

---

## 19.60 Context Isolation Test

Dos operaciones concurrentes deberán conservar contextos independientes.

---

## 19.61 No Global State Test

La suite deberá detectar o evitar dependencias de:

```text
current_session
current_consumer
last_response
```

globales y mutables.

---

## 19.62 Security Tests

Deberán existir tests de seguridad desde la primera integración real.

---

## 19.63 Unknown Consumer Security Test

```text
test_unknown_consumer_does_not_execute_adapter
```

---

## 19.64 Unauthorized Consumer Test

```text
test_unauthorized_delivery_is_rejected
```

---

## 19.65 Fail Closed Test

Si la autorización obligatoria no puede determinarse:

```text
test_security_failure_fails_closed
```

---

## 19.66 Secret Leakage Test

Deberá verificarse que payload público no contenga:

```text
tokens
passwords
internal secrets
```

---

## 19.67 Public Projection Test

```text
test_public_projection_contains_only_allowed_fields
```

---

## 19.68 Action Security Test

```text
test_unknown_action_rejected
test_executable_action_rejected
```

---

## 19.69 Versioning Tests

Deberán existir:

```text
test_explicit_contract_version
test_supported_version_passes
test_unsupported_version_rejects
```

---

## 19.70 Version Preservation Test

La versión deberá sobrevivir:

```text
contract
→ envelope
→ serializer
→ payload
→ trace
```

---

## 19.71 No Silent Downgrade Test

```text
test_unsupported_requested_version_is_not_silently_downgraded
```

---

## 19.72 Deprecated Version Tests

Cuando exista deprecación:

```text
test_deprecated_version_warns
test_retired_version_rejects
```

---

## 19.73 Error Model Tests

Todo error público deberá probarse.

---

## 19.74 Error Code Stability

Fixtures podrán garantizar que errores conocidos mantengan:

```text
code
category
status mapping
```

---

## 19.75 Error Stage Test

Un fallo debe quedar asociado con la etapa correcta.

Ejemplo:

```text
serializer failure → SERIALIZATION
```

---

## 19.76 Error Trace Test

Un error deberá preservar:

```text
delivery_id
response_id
```

---

## 19.77 No Response Mutation Test

Ante cualquier error de Delivery:

```text
MaterializedResponse before
==
MaterializedResponse after
```

---

## 19.78 REJECTED Test

Debe verificarse que un rechazo por precondición:

```text
does not execute adapter
```

---

## 19.79 FAILED Test

Debe verificarse que un fallo operacional:

```text
does produce DeliveryResult FAILED
```

---

## 19.80 DELIVERED Test

Un flujo válido deberá producir:

```text
DELIVERED
```

y no error fatal.

---

## 19.81 Terminal State Test

Toda operación deberá terminar exactamente en uno de:

```text
DELIVERED
REJECTED
FAILED
```

---

## 19.82 No Terminal Mutation Test

Una operación ya terminal no deberá cambiar de estado posteriormente.

---

## 19.83 Observability Tests

Deberá verificarse:

```text
trace created
terminal status recorded
error stage recorded
duration non-negative
```

---

## 19.84 Event Tests

Si EventBus se utiliza:

```text
test_started_event_emitted
test_single_terminal_event_emitted
```

---

## 19.85 No Duplicate Terminal Event

Una operación no deberá producir dos eventos terminales.

---

## 19.86 Logging Tests

Deberá verificarse que información sensible no aparezca.

---

## 19.87 Metrics Tests

Cuando se implementen:

```text
success increments success counter
failure increments failure counter
rejection increments rejection counter
```

---

## 19.88 Metric Cardinality Test

No deberán utilizarse IDs únicos como labels.

---

## 19.89 Audit Tests

Si existe persistencia de auditoría:

```text
test_audit_record_matches_delivery_result
```

---

## 19.90 Historical Integrity Test

Un registro `FAILED` no deberá reescribirse después de un retry exitoso.

---

## 19.91 Gateway Contract Tests

Cuando se implemente Gateway deberán existir tests específicos.

---

## 19.92 Gateway Success Mapping

```text
DELIVERED
→ expected external success response
```

---

## 19.93 Gateway Error Mapping

```text
REJECTED
FAILED
```

deberán mapearse sin perder el código semántico.

---

## 19.94 Gateway Field Preservation

El Gateway no deberá eliminar campos obligatorios.

---

## 19.95 Gateway Internal Leakage Test

No deberá exponer:

```text
stack traces
internal exceptions
secrets
```

---

## 19.96 Gateway Independence Test

Delivery deberá continuar funcionando sin framework web instalado si Gateway es opcional.

---

## 19.97 Presentation Contract Tests

Cuando se integre Portal, deberá existir una suite independiente en el consumidor.

---

## 19.98 Portal Parser Test

El Portal deberá interpretar:

```text
Delivery Contract 1.0
```

correctamente.

---

## 19.99 UI Warning Preservation Test

Una advertencia contractual deberá llegar a Presentation.

---

## 19.100 UI Null Test

`null` no deberá convertirse en `0`.

---

## 19.101 UI Action Test

Las acciones deberán pasar por allowlist.

---

## 19.102 UI Geometry Test

Una referencia territorial deberá resolver correctamente una sección cuando la fuente cartográfica esté disponible.

---

## 19.103 UI Failure Attribution Test

Un fallo de renderizado no deberá modificar DeliveryResult.

---

## 19.104 End-to-End DescribeSection Test

Una de las pruebas clave deberá recorrer:

```text
Known section
      ↓
Runtime
      ↓
DescribeSection
      ↓
Materialization
      ↓
Delivery
      ↓
InMemory / Gateway
```

y validar:

```text
response_id
delivery_id
status
content
trace
```

---

## 19.105 End-to-End invalid consumer test

La misma vertical con un consumer inválido deberá terminar:

```text
REJECTED
```

sin ejecutar adapter.

---

## 19.106 End-to-End serialization failure test

Una respuesta deliberadamente no serializable deberá terminar:

```text
FAILED
```

antes de cruzar frontera.

---

## 19.107 End-to-End adapter failure test

Un adapter fallido deberá producir:

```text
FAILED
```

con trazabilidad completa.

---

## 19.108 Contract Coverage Matrix

Deberá construirse una matriz que relacione:

```text
Invariant
Implementation
Test
Status
```

Ejemplo:

| Invariante | Test |
|---|---|
| HRRD-S01 Semantic Preservation | `test_json_round_trip_preserves_semantics` |
| HRRD-T02 Unique Delivery Identity | `test_each_delivery_has_unique_id` |
| HRRD-A05 No Semantic Mutation | `test_adapter_does_not_mutate_payload` |
| HRRD-SEC01 Authorization Before Delivery | `test_unauthorized_does_not_execute_adapter` |

---

## 19.109 Invariant Traceability

Cada familia de invariantes:

```text
HRRD-P
HRRD-M
HRRD-PL
HRRD-C
HRRD-S
HRRD-V
HRRD-T
HRRD-E
HRRD-SC
HRRD-CO
HRRD-A
HRRD-G
HRRD-SEC
HRRD-VER
HRRD-O
HRRD-PRES
```

deberá poseer evidencia suficiente.

---

## 19.110 No requirement-to-test orphan

Una regla crítica no deberá quedar sin:

```text
implementation path
```

o:

```text
test/evidence path
```

---

## 19.111 No test-without-requirement drift

De igual manera, una prueba que imponga comportamiento no documentado deberá revisarse.

La suite no deberá convertirse en una segunda arquitectura secreta.

---

## 19.112 Traceability Matrix

Podrá utilizarse conceptualmente:

```text
Requirement
→ Architecture
→ Code
→ Test
→ Evidence
```

Esta matriz será especialmente útil para auditoría.

---

## 19.113 Test Naming Convention

Los nombres deberán describir comportamiento.

Preferible:

```text
test_unsupported_consumer_is_rejected
```

sobre:

```text
test_case_17
```

---

## 19.114 Test File Organization

La futura estructura podría incluir:

```text
tests/
├── delivery/
│   ├── test_contracts.py
│   ├── test_validator.py
│   ├── test_serializer.py
│   ├── test_context.py
│   ├── test_consumer_registry.py
│   ├── test_adapter_registry.py
│   ├── test_inmemory_adapter.py
│   └── test_delivery_service.py
```

La ubicación definitiva deberá ajustarse a la estructura real del repositorio.

---

## 19.115 No structure before repository audit

La estructura anterior es conceptual.

Antes de crear archivos deberá revisarse:

```text
current test organization
existing naming conventions
existing fixtures
```

---

## 19.116 Test Isolation

Cada test deberá limpiar estado mutable.

Especialmente:

```text
registries
captured payloads
global settings
```

---

## 19.117 Registry Fixture

Los tests deberán usar registries nuevos por caso cuando sea posible.

---

## 19.118 No order-dependent tests

La suite deberá funcionar en cualquier orden.

---

## 19.119 Parallel Test Safety

Si pytest se ejecuta en paralelo en el futuro, no deberá existir estado compartido peligroso.

---

## 19.120 Global pytest

Además de tests específicos de Delivery, siempre deberá ejecutarse:

```text
pytest -q
```

sobre todo el repositorio.

---

## 19.121 Regla de no regresión

Sprint 23 no podrá considerarse exitoso si los tests nuevos pasan pero rompen tests anteriores.

La condición será:

```text
New Delivery Tests = PASS
AND
Global Existing Suite = PASS
```

---

## 19.122 git diff --check

Antes de cierre deberá ejecutarse:

```text
git diff --check
```

para detectar errores de whitespace u otros problemas de diff.

---

## 19.123 Working Tree Review

También deberá verificarse:

```text
git status
```

para conocer exactamente qué archivos fueron modificados.

---

## 19.124 Scope Control

El Sprint deberá evitar cambios no relacionados.

Un diff inesperadamente grande deberá revisarse.

---

## 19.125 Test Evidence

Al cierre deberá conservarse evidencia de:

```text
test count
passed
failed
duration
```

---

## 19.126 Evidence Example

Conceptualmente:

```text
pytest -q
123 passed in 1.80s
```

El número real dependerá de la implementación.

---

## 19.127 No fabricated counts

El documento no deberá anticipar un número de tests final como si ya existiera.

La certificación deberá usar el resultado real.

---

## 19.128 Verification Layers

La verificación final deberá realizarse en cuatro capas:

```text
Code Verification
Contract Verification
Behavior Verification
Architecture Verification
```

---

## 19.129 Code Verification

Incluye:

```text
syntax
imports
type consistency
test execution
```

---

## 19.130 Contract Verification

Incluye:

```text
required fields
versions
serialization
errors
consumer compatibility
```

---

## 19.131 Behavior Verification

Incluye:

```text
successful delivery
rejection
failure
adapter substitution
trace preservation
```

---

## 19.132 Architecture Verification

Incluye:

```text
no UI coupling
no cognitive mutation
no hidden global state
no transport coupling
no silent retry
```

---

## 19.133 Certification

Se define conceptualmente una certificación de Sprint como la evidencia formal de que HRRD ha alcanzado un nivel determinado de implementación.

No deberá confundirse con una certificación externa.

---

## 19.134 Certification Level 1 — Core Contract Ready

Debe demostrar:

```text
contracts
validation
serialization
trace
error model
```

---

## 19.135 Certification Level 2 — Delivery Core Ready

Añade:

```text
consumer model
adapter registry
in-memory adapter
delivery service/pipeline
```

---

## 19.136 Certification Level 3 — Gateway Ready

Añade:

```text
gateway integration
external contract mapping
security boundary
```

---

## 19.137 Certification Level 4 — Presentation Integrated

Añade:

```text
consumer adapter
UI rendering
maps
charts
end-to-end visual verification
```

---

## 19.138 Sprint 23 Target

Sprint 23 deberá enfocarse principalmente en alcanzar, como mínimo:

```text
Core Contract Ready
+
Delivery Core Ready
```

según el alcance final de implementación que se defina tras cerrar arquitectura.

---

## 19.139 No premature Presentation certification

No deberá afirmarse que Presentation está integrada hasta que exista una vertical real funcionando.

---

## 19.140 Acceptance Criteria

Se establecen criterios formales de aceptación.

---

## 19.141 AC-01 — Contract Exists

Existe un Delivery Contract explícito y versionado.

---

## 19.142 AC-02 — Validation Exists

Una respuesta inválida es rechazada antes del adapter.

---

## 19.143 AC-03 — Serialization Exists

Una respuesta válida puede convertirse a representación canónica y JSON-compatible.

---

## 19.144 AC-04 — Unsupported Type Fails

Un tipo no soportado produce error explícito.

---

## 19.145 AC-05 — Delivery Identity Exists

Toda operación posee `delivery_id`.

---

## 19.146 AC-06 — Response Identity Preserved

`response_id` permanece intacto.

---

## 19.147 AC-07 — Consumer Explicit

Toda entrega identifica `consumer_id`.

---

## 19.148 AC-08 — Consumer Compatibility Validated

Un consumer incompatible es rechazado.

---

## 19.149 AC-09 — Adapter Explicit

Toda entrega identifica `adapter_id`.

---

## 19.150 AC-10 — InMemory Adapter Works

Puede realizarse Delivery sin red.

---

## 19.151 AC-11 — DeliveryResult Exists

Toda operación termina en `DeliveryResult`.

---

## 19.152 AC-12 — Terminal Status Valid

Toda operación termina en:

```text
DELIVERED
REJECTED
FAILED
```

---

## 19.153 AC-13 — Errors Structured

Los fallos producen `DeliveryError` estructurado.

---

## 19.154 AC-14 — Error Stage Traceable

Puede determinarse dónde ocurrió el error.

---

## 19.155 AC-15 — No Cognitive Mutation

Delivery no altera la respuesta materializada.

---

## 19.156 AC-16 — No Presentation Coupling

Delivery no depende de:

```text
HTML
CSS
DOM
Leaflet
Chart.js
```

---

## 19.157 AC-17 — No Transport Coupling

El Core no depende de una tecnología concreta de red.

---

## 19.158 AC-18 — No Silent Retry

No existen reintentos automáticos implícitos.

---

## 19.159 AC-19 — Traceability Exists

La relación:

```text
response_id
→ delivery_id
```

puede reconstruirse.

---

## 19.160 AC-20 — Session Context Preserved

Cuando exista sesión, su referencia puede conservarse.

---

## 19.161 AC-21 — Version Explicit

La versión de Delivery Contract es visible.

---

## 19.162 AC-22 — Security Projection

Los payloads públicos no exponen campos internos no autorizados.

---

## 19.163 AC-23 — Observability Exists

Cada operación deja evidencia terminal suficiente para diagnóstico.

---

## 19.164 AC-24 — Existing Tests Remain Green

La suite global continúa pasando.

---

## 19.165 AC-25 — Zero Omission Audit Passes

No existe campo obligatorio omitido silenciosamente.

---

## 19.166 Definition of Done

Sprint 23 no deberá considerarse terminado únicamente porque:

```text
code compiles
```

La Definition of Done deberá exigir:

```text
architecture documented
implementation aligned
tests complete
global suite green
zero omission review
zero error review
traceability review
Git clean
```

---

## 19.167 Zero Error Review

La revisión deberá buscar:

- excepciones no manejadas;
- estados inconsistentes;
- errores silenciosos;
- mappings ambiguos;
- imports rotos.

---

## 19.168 Zero Omission Review

La revisión deberá buscar:

- campos contractuales no serializados;
- trace IDs perdidos;
- warnings omitidos;
- versiones ausentes;
- ConsumerProfile incompleto;
- tests faltantes.

---

## 19.169 Boundary Review

Deberá revisarse explícitamente:

```text
Materialization → Delivery
Delivery → Adapter
Delivery → Gateway
Delivery → Presentation
```

para confirmar responsabilidades.

---

## 19.170 Architecture Smell Review

Deberán buscarse smells como:

```text
if consumer == portal.html
if adapter == HTTP then add UI data
default=str
global current_session
except: pass
hardcoded contract version everywhere
```

---

## 19.171 Dependency Review

Deberá verificarse que el paquete Delivery no introduzca dependencias innecesarias.

---

## 19.172 Security Review

Antes de Gateway real deberán revisarse:

```text
public fields
consumer authorization
secrets
logs
actions
target control
```

---

## 19.173 Performance Baseline

La versión inicial deberá poder medir suficientemente:

```text
delivery duration
payload size
```

aunque no se establezcan todavía objetivos estrictos.

---

## 19.174 Performance Test

Podrá existir una prueba básica para asegurar que Delivery no introduce complejidad absurda.

No deberá usarse como benchmark rígido inicialmente.

---

## 19.175 Payload Size Test

Una fixture rica podrá medir el tamaño de salida para detectar crecimiento accidental.

---

## 19.176 Large Payload Test

En el futuro deberá verificarse comportamiento frente a límites.

---

## 19.177 Concurrency Test

Cuando la arquitectura ejecute operaciones concurrentes, deberá probarse aislamiento.

---

## 19.178 Thread Safety Test

Solo será necesario si los adapters/registries se comparten entre threads.

---

## 19.179 Async Tests

Solo cuando exista async real.

No deberá incorporarse por anticipación.

---

## 19.180 Fault Injection

En una fase de hardening se podrán inyectar fallos.

Ejemplos:

```text
serializer exception
adapter exception
registry lookup failure
trace failure
```

---

## 19.181 Chaos Testing futuro

No es necesario para Sprint 23.

Podrá considerarse únicamente en sistemas distribuidos maduros.

---

## 19.182 Property-Based Testing

Podrá ser útil para invariantes como:

```text
serialize(valid_contract)
never loses required fields
```

---

## 19.183 Mutation Testing

Podrá ayudar a comprobar calidad real de tests.

No es obligatorio.

---

## 19.184 Static Analysis

La arquitectura podrá incorporar:

```text
ruff
mypy
pyright
```

u otras herramientas si el repositorio adopta formalmente alguna.

No deberán imponerse sin revisar estándares existentes.

---

## 19.185 Type Checking

Los type hints deberán apoyar claridad.

No sustituyen runtime validation.

---

## 19.186 Linting

El linting puede mejorar calidad.

No deberá utilizarse para bloquear el Sprint sin una política establecida.

---

## 19.187 CI Gate futuro

Una futura CI deberá ejecutar al menos:

```text
tests
contract checks
diff checks
```

antes de merge.

---

## 19.188 Branch Protection futuro

Podrán establecerse reglas GitHub si el flujo del repositorio lo requiere.

No forma parte estricta de HRRD.

---

## 19.189 Regression Gate

Toda modificación posterior en Delivery deberá ejecutar:

```text
delivery tests
+
global tests
```

---

## 19.190 Contract Change Gate

Si cambia una estructura pública:

```text
contract version impact review
```

deberá ser obligatoria.

---

## 19.191 Consumer Compatibility Gate

Si cambia Delivery Contract deberá probarse al menos contra consumidores activos.

---

## 19.192 Adapter Compatibility Gate

Si cambia payload técnico deberá probarse contra adapters soportados.

---

## 19.193 Gateway Compatibility Gate

Si existe Gateway deberá probarse mapping externo.

---

## 19.194 Presentation Compatibility Gate

Si existe UI integrada deberá probarse Consumer Adapter.

---

## 19.195 Certification Evidence Package

Al cerrar implementación podría generarse un conjunto de evidencia con:

```text
test output
test count
git status
git diff --check
changed files
contract version
acceptance criteria result
```

---

## 19.196 Nombre conceptual

Podría llamarse:

```text
HEYTI_Runtime_Response_Delivery_Verification_Report_v1.0
```

si decidimos crear un documento separado de auditoría al cierre.

---

## 19.197 No duplicar documentos prematuramente

Este reporte deberá crearse solo si aporta valor al cierre del Sprint.

No antes de terminar la implementación.

---

## 19.198 Acceptance Matrix

Conceptualmente:

| Criterio | Evidencia | Resultado |
|---|---|---|
| Contract version explicit | test + code | PASS/FAIL |
| Response ID preserved | unit test | PASS/FAIL |
| InMemory delivery | integration test | PASS/FAIL |
| Consumer incompatibility rejection | contract test | PASS/FAIL |
| No semantic mutation | unit test | PASS/FAIL |
| Global suite | pytest | PASS/FAIL |

---

## 19.199 No subjective PASS

Un criterio deberá marcarse `PASS` únicamente cuando exista evidencia verificable.

---

## 19.200 Failed Acceptance Criterion

Si un criterio falla:

```text
Sprint certification = NOT COMPLETE
```

aunque otros tests pasen.

---

## 19.201 Waivers

Una excepción solo podrá aceptarse mediante decisión arquitectónica explícita.

No deberá ignorarse silenciosamente.

---

## 19.202 Deferred Features

Elementos formalmente diferidos como:

```text
WebSocket
retry
streaming
multi-version negotiation
advanced audit persistence
```

no deberán considerarse fallos del Sprint si fueron declarados fuera de alcance.

---

## 19.203 Deferred vs Missing

Debe distinguirse:

```text
DEFERRED BY DESIGN
```

de:

```text
MISSING BY OMISSION
```

Esta distinción será crítica en auditoría.

---

## 19.204 Deferred Feature Register

Podrá mantenerse una sección de:

```text
Deferred Capabilities
```

en el cierre del Sprint.

---

## 19.205 Test Coverage

El porcentaje de coverage puede ser útil.

No deberá convertirse en objetivo vacío.

---

## 19.206 Coverage Quality

```text
100% line coverage
```

no garantiza:

```text
correct behavior
```

La prioridad será cubrir invariantes críticas.

---

## 19.207 Critical Path Coverage

Debe priorizarse:

```text
validation
serialization
errors
adapter execution
trace
security boundary
```

---

## 19.208 Error Path Coverage

Todos los códigos públicos principales deberán tener al menos una prueba.

---

## 19.209 Contract Field Coverage

Todo campo REQUIRED deberá aparecer en pruebas positivas y negativas.

---

## 19.210 Consumer Coverage

Todo ConsumerProfile productivo deberá tener pruebas de compatibilidad.

---

## 19.211 Adapter Coverage

Todo adapter productivo deberá tener:

```text
success test
failure test
configuration test
trace test
```

---

## 19.212 Certification Flow

```text
Implementation Complete
      ↓
Unit Tests
      ↓
Contract Tests
      ↓
Integration Tests
      ↓
Global pytest
      ↓
Zero Omission Audit
      ↓
Architecture Conformance Review
      ↓
Acceptance Matrix
      ↓
CERTIFIED / NOT CERTIFIED
```

---

## 19.213 Failure Flow

```text
Any critical test fails
      ↓
Identify cause
      ↓
Fix implementation
      ↓
Run targeted tests
      ↓
Run global suite
      ↓
Re-run acceptance
```

---

## 19.214 No partial green claim

No deberá declararse:

```text
Sprint complete
```

si:

```text
targeted tests pass
```

pero:

```text
global suite fails
```

---

## 19.215 No untested hotfix

Una corrección introducida al final deberá volver a ejecutar tests.

---

## 19.216 No final commit before verification

El commit de cierre deberá realizarse después de:

```text
tests
diff check
status review
```

---

## 19.217 Git Verification Sequence

Conceptualmente:

```text
git status
git diff --check
pytest -q
git diff --stat
```

y revisión de archivos modificados.

---

## 19.218 Clean Working Tree

Después del commit final:

```text
git status
```

deberá indicar el estado esperado.

Idealmente:

```text
nothing to commit, working tree clean
```

---

## 19.219 Commit Scope

El commit deberá describir claramente el Sprint.

Ejemplo conceptual:

```text
feat(heyti): implement runtime response delivery core
```

El mensaje final se definirá según cambios reales.

---

## 19.220 Certification and Git Commit

El hash final podrá incluirse en el reporte de cierre.

---

## 19.221 Baseline

Ese commit constituirá la baseline certificada de Sprint 23.

---

## 19.222 Regression Reference

Los Sprints posteriores deberán poder comparar contra esta baseline.

---

## 19.223 Test Documentation

Los tests deberán ser suficientemente legibles para explicar reglas.

---

## 19.224 No test comments replacing architecture

Los comentarios en tests no reemplazan este documento.

---

## 19.225 Architecture remains authoritative

El orden de autoridad será:

```text
Architecture
      ↓
Contracts
      ↓
Implementation
      ↓
Tests
```

aunque los tests actúen como evidencia ejecutable.

---

## 19.226 Inconsistency Resolution

Si código y documento divergen:

```text
stop
review
decide
align
```

No deberá asumirse automáticamente que el código tiene razón.

---

## 19.227 Test Failure as architectural signal

Un fallo puede revelar:

- bug;
- contrato incorrecto;
- requisito ambiguo;
- arquitectura mal interpretada.

Deberá analizarse antes de "hacer que pase".

---

## 19.228 No test weakening

Queda prohibido resolver una falla simplemente eliminando la aserción si el comportamiento requerido sigue siendo válido.

---

## 19.229 Test refactoring

Los tests pueden refactorizarse para claridad.

No deberán perder cobertura semántica.

---

## 19.230 Architecture Conformance Checklist

Antes de certificación deberá responderse:

```text
Does Delivery mutate cognition? NO
Does Delivery depend on UI? NO
Does Delivery depend on one transport? NO
Are errors explicit? YES
Are IDs traceable? YES
Are consumers explicit? YES
Are adapters replaceable? YES
Is version explicit? YES
Are required fields validated? YES
Is security boundary respected? YES
```

---

## 19.231 Zero Omission Checklist

```text
Response ID preserved?
Delivery ID present?
Contract version present?
Consumer ID present?
Adapter ID present?
Warnings preserved?
Errors structured?
Trace completed?
Terminal status present?
Required fields serialized?
```

---

## 19.232 Failure Classification Checklist

Para cada escenario deberá identificarse:

```text
REJECTED
or
FAILED
or
DELIVERED
```

sin ambigüedad.

---

## 19.233 Consumer Compatibility Checklist

```text
consumer known?
profile enabled?
contract supported?
content types supported?
adapter available?
authorization valid?
```

---

## 19.234 Serializer Checklist

```text
canonical types only?
timestamps explicit?
null preserved?
IDs preserved?
unsupported types fail?
UTF-8 compatible?
```

---

## 19.235 Adapter Checklist

```text
adapter registered?
identity stable?
payload read-only?
context read-only?
errors normalized?
timeout explicit when external?
retry hidden? NO
```

---

## 19.236 Security Checklist

```text
consumer authorized?
secrets excluded?
public projection explicit?
actions declarative?
targets controlled?
logs sanitized?
```

---

## 19.237 Observability Checklist

```text
delivery_id logged?
response_id correlated?
terminal status visible?
error stage visible?
duration available?
no sensitive payload logs?
```

---

## 19.238 Acceptance Decision

La decisión final deberá producir:

```text
PASS
```

o:

```text
FAIL
```

para cada criterio.

No:

```text
probably okay
```

---

## 19.239 Certification Status

Se proponen tres estados:

```text
CERTIFIED
CERTIFIED WITH EXPLICIT DEFERRED ITEMS
NOT CERTIFIED
```

---

## 19.240 CERTIFIED

Todos los criterios aplicables han sido superados.

---

## 19.241 CERTIFIED WITH EXPLICIT DEFERRED ITEMS

Todos los criterios del alcance acordado se cumplen.

Existen funcionalidades futuras documentadas como diferidas.

---

## 19.242 NOT CERTIFIED

Existe al menos un criterio crítico del alcance que no fue superado.

---

## 19.243 No "certified with errors"

No deberá existir un estado ambiguo:

```text
CERTIFIED WITH KNOWN CRITICAL ERRORS
```

Eso contradice la certificación.

---

## 19.244 Definition of Sprint Success

Sprint 23 podrá considerarse exitoso cuando:

```text
Architecture = CLOSED
Implementation = ALIGNED
Tests = GREEN
Contracts = VALIDATED
Traceability = VERIFIED
Zero Omission = VERIFIED
Global Regression = GREEN
```

---

## 19.245 Invariantes de pruebas y certificación

Se establecen los siguientes invariantes.

### HRRD-QA01 — Every Critical Invariant Needs Evidence

Toda regla crítica deberá contar con evidencia ejecutable o revisión formal.

### HRRD-QA02 — Positive and Negative Testing

Toda frontera crítica deberá probar casos válidos e inválidos.

### HRRD-QA03 — Global Regression Required

Los tests del Sprint no sustituyen la suite global.

### HRRD-QA04 — No Silent Omission

Todo campo REQUIRED deberá poseer pruebas de ausencia.

### HRRD-QA05 — Error Paths Are First-Class

Los fallos deberán probarse con la misma prioridad que los éxitos.

### HRRD-QA06 — Adapter Substitutability Verified

La independencia de transporte deberá demostrarse mediante pruebas.

### HRRD-QA07 — Consumer Compatibility Verified

La compatibilidad deberá ser ejecutable, no asumida.

### HRRD-QA08 — Historical Contract Stability

Los fixtures contractuales publicados deberán permanecer estables.

### HRRD-QA09 — Certification Requires Evidence

Ningún criterio deberá marcarse PASS sin evidencia.

### HRRD-QA10 — Zero Error / Zero Omission Discipline

La certificación deberá incluir revisión explícita de errores y omisiones.

---

## 19.246 Criterio de éxito del capítulo

La estrategia de pruebas será considerada adecuada cuando el comportamiento completo de Delivery pueda demostrarse mediante una combinación de:

```text
Unit Tests
Contract Tests
Integration Tests
Conformance Tests
Global Regression Tests
```

y cuando el cierre de Sprint pueda sustentarse en evidencia reproducible.

---

## 19.247 Declaración arquitectónica del capítulo

Runtime Response Delivery no deberá confiar en validación manual informal para demostrar que funciona.

Una frontera tan crítica debe poseer evidencia ejecutable.

Los contratos deberán probarse.

Los errores deberán probarse.

Las omisiones deberán probarse.

La independencia de consumidor deberá probarse.

La independencia de transporte deberá probarse.

La trazabilidad deberá probarse.

Y la suite completa de HEYTI deberá permanecer estable.

La regla arquitectónica consolidada queda establecida como:

> **HEYTI Runtime Response Delivery solo podrá considerarse implementado cuando sus contratos, invariantes, flujos de éxito, flujos de rechazo, flujos de fallo, consumers, adapters, serialización, seguridad y trazabilidad hayan sido verificados mediante pruebas reproducibles y la suite global permanezca sin regresiones.**

La disciplina final queda formalizada como:

```text
Architecture
      ↓
Implementation
      ↓
Verification
      ↓
Evidence
      ↓
Certification
```

y:

```text
0 ERRORES
0 OMISIONES
```

deberá funcionar como criterio verificable, no como declaración aspiracional.

Con esta estrategia de certificación establecida queda preparada la siguiente dimensión del documento:

**plan de implementación incremental, orden de materialización técnica y secuencia segura de construcción de Sprint 23.**

---

**Fin del Capítulo 19**


# Capítulo 20. Plan de implementación incremental, orden de materialización técnica y secuencia segura de construcción de Sprint 23

## 20.1 Propósito del capítulo

Este capítulo establece el **plan formal de implementación** de **HEYTI Runtime Response Delivery (HRRD)**.

Los capítulos anteriores han definido:

```text
qué es Delivery
qué responsabilidades posee
qué responsabilidades no posee
qué contratos necesita
cómo preserva la respuesta
cómo serializa
cómo identifica consumers
cómo utiliza adapters
cómo maneja errores
cómo mantiene trazabilidad
cómo controla seguridad
cómo versiona
cómo se observa
cómo se relaciona con Presentation
cómo deberá probarse
```

Ahora debe establecerse:

> **¿En qué orden exacto deberá materializarse todo esto dentro del repositorio sin romper la arquitectura existente de HEYTI?**

La regla fundamental será:

> **Sprint 23 deberá construirse incrementalmente, verificando cada frontera antes de avanzar a la siguiente y evitando implementar componentes cuya dependencia anterior todavía no haya sido certificada.**

---

## 20.2 Implementar desde el contrato hacia afuera

La secuencia de construcción deberá seguir:

```text
Contracts
    ↓
Context
    ↓
Validation
    ↓
Serialization
    ↓
Consumer Model
    ↓
Adapter Abstraction
    ↓
InMemory Adapter
    ↓
Delivery Orchestration
    ↓
Observability
    ↓
Runtime Integration
    ↓
Gateway Preparation
```

No deberá comenzarse por:

```text
HTTP endpoint
UI
WebSocket
Portal integration
```

porque estas piezas dependen de una frontera de Delivery todavía no materializada.

---

## 20.3 Principio Contract First

Antes de escribir lógica operacional deberán existir estructuras claras para representar:

```text
DeliveryContext
DeliveryEnvelope
DeliveryResult
DeliveryError
DeliveryTrace
ConsumerProfile
AdapterResult
```

Estas estructuras constituirán el lenguaje interno de HRRD.

---

## 20.4 No Code First

Queda prohibida como estrategia:

```text
write delivery()
      ↓
discover required fields later
      ↓
patch contract
      ↓
patch tests
```

La secuencia correcta será:

```text
define contract
      ↓
define invariant
      ↓
write test
      ↓
implement behavior
      ↓
verify
```

---

## 20.5 Repository Audit Before Implementation

Antes de crear un solo archivo nuevo deberá realizarse una auditoría del repositorio actual.

Deberán inspeccionarse al menos:

```text
src/heyti/
tests/
materialization/
runtime/
capabilities/
kernel/
event bus implementation
session management
existing contracts
existing errors
```

según la estructura real encontrada.

---

## 20.6 Objetivo de la auditoría

La auditoría deberá responder:

```text
What already exists?
What can be reused?
What must be extended?
What must remain untouched?
What would be duplicated?
```

---

## 20.7 Regla de no duplicación

Si ya existe una abstracción equivalente a:

```text
RuntimeContext
ResponseContract
ErrorContract
Event
Registry
```

deberá analizarse antes de crear otra.

No deberá introducirse una estructura paralela únicamente porque resulte más rápido.

---

## 20.8 Materialization Baseline

Sprint 23 deberá comenzar verificando el estado real del trabajo realizado en Sprint 22.

Especialmente:

```text
src/heyti/materialization/
```

y sus contratos asociados.

---

## 20.9 Materialization as Input Boundary

HRRD deberá consumir únicamente una respuesta que ya haya cruzado correctamente la frontera de Materialization.

Conceptualmente:

```text
Capability Result
      ↓
Materialization
      ↓
Materialized Response
========================
 HRRD INPUT BOUNDARY
========================
      ↓
Delivery
```

---

## 20.10 No Materialization Reimplementation

Sprint 23 no deberá volver a implementar:

```text
response construction
cognitive interpretation
evidence assembly
knowledge reasoning
```

Estas responsabilidades permanecen aguas arriba.

---

# 20.11 Fases de implementación

La implementación se dividirá en fases controladas:

```text
Phase 0  — Repository Baseline Audit
Phase 1  — Delivery Contracts
Phase 2  — Delivery Context and Trace
Phase 3  — Validation
Phase 4  — Serialization
Phase 5  — Consumer Model
Phase 6  — Adapter Abstraction
Phase 7  — InMemory Adapter
Phase 8  — Delivery Orchestration
Phase 9  — Error Normalization
Phase 10 — Observability
Phase 11 — Runtime Integration
Phase 12 — Verification and Certification
```

Cada fase deberá cerrar correctamente antes de avanzar.

---

# 20.12 Phase 0 — Repository Baseline Audit

La primera fase no deberá escribir código.

Deberá inspeccionar.

---

## 20.13 Elementos a revisar

Como mínimo:

```text
src/heyti/
tests/
pyproject.toml
runtime bootstrap
CapabilityRegistry
CapabilityRuntime
SessionManager
EventBus
DescribeSection
materialization
existing error hierarchy
```

---

## 20.14 Phase 0 Deliverable

La fase deberá producir una decisión clara sobre:

```text
package location
dependencies
reuse points
integration points
test location
```

---

## 20.15 Posible ubicación

Conceptualmente podría existir:

```text
src/heyti/delivery/
```

pero esta ruta no deberá crearse hasta confirmar que es consistente con la arquitectura real del repositorio.

---

## 20.16 Posible estructura

Después de auditoría podría resultar apropiado:

```text
src/heyti/delivery/
├── __init__.py
├── contracts.py
├── context.py
├── errors.py
├── validator.py
├── serializer.py
├── consumers.py
├── adapters/
│   ├── __init__.py
│   ├── base.py
│   └── in_memory.py
└── service.py
```

Esta estructura es una propuesta conceptual.

No constituye todavía una orden de creación.

---

## 20.17 No premature directories

La estructura real deberá derivarse de:

```text
existing repository conventions
```

no de preferencia estética.

---

# 20.18 Phase 1 — Delivery Contracts

Una vez auditado el repositorio, deberán materializarse primero los contratos.

---

## 20.19 Contratos mínimos

Deberán evaluarse como mínimo:

```text
DeliveryStatus
DeliveryStage
DeliveryEnvelope
DeliveryResult
DeliveryError
AdapterResult
```

---

## 20.20 DeliveryStatus

La enumeración mínima será conceptualmente:

```text
DELIVERED
REJECTED
FAILED
```

---

## 20.21 DeliveryStage

Podrá incluir:

```text
VALIDATION
SERIALIZATION
CONSUMER_RESOLUTION
ADAPTER_RESOLUTION
DELIVERY_EXECUTION
```

La lista definitiva deberá corresponder con la implementación real.

---

## 20.22 DeliveryEnvelope

Deberá encapsular la representación que cruza Delivery.

Conceptualmente:

```text
DeliveryEnvelope
├── delivery_contract_version
├── delivery_id
├── response_id
├── consumer_id
├── adapter_id
├── payload
└── trace
```

---

## 20.23 DeliveryResult

Deberá representar el resultado terminal.

Conceptualmente:

```text
DeliveryResult
├── delivery_id
├── response_id
├── status
├── consumer_id
├── adapter_id
├── error?
└── trace
```

---

## 20.24 Phase 1 Tests

Antes de continuar deberán existir tests para:

```text
valid contracts
required fields
invalid statuses
result invariants
serialization readiness
```

---

## 20.25 Phase 1 Exit Gate

La fase se considerará cerrada cuando:

```text
contracts import correctly
contract tests pass
global pytest passes
```

---

# 20.26 Phase 2 — Delivery Context and Trace

Después deberán materializarse contexto y trazabilidad.

---

## 20.27 DeliveryContext

Deberá transportar únicamente información operacional necesaria.

Ejemplo conceptual:

```text
request_id
execution_id
response_id
session_id
consumer_id
```

---

## 20.28 DeliveryTrace

Deberá preservar la continuidad de identidad.

Ejemplo:

```text
REQ-001
   ↓
EXE-001
   ↓
RESP-001
   ↓
DEL-001
```

---

## 20.29 Trace creation

`delivery_id` deberá generarse exactamente una vez por operación.

---

## 20.30 Trace immutability preference

Una vez creado, el trace deberá favorecer una semántica inmutable.

No deberá cambiarse arbitrariamente durante Delivery.

---

## 20.31 Phase 2 Tests

Deberán verificarse:

```text
ID preservation
context consistency
session preservation
unique delivery identity
trace correlation
```

---

## 20.32 Phase 2 Exit Gate

```text
trace tests pass
context tests pass
global suite passes
```

---

# 20.33 Phase 3 — Validation

Una vez definidos contrato y contexto deberá implementarse la validación.

---

## 20.34 Validation Order

El orden conceptual será:

```text
input existence
      ↓
contract integrity
      ↓
context integrity
      ↓
consumer requirements
      ↓
delivery readiness
```

---

## 20.35 Validation must precede adapter execution

Queda establecido:

```text
INVALID
   ↓
REJECTED
```

antes de:

```text
adapter.deliver(...)
```

---

## 20.36 Required-field validation

Todo campo REQUIRED deberá verificarse explícitamente.

---

## 20.37 No truthiness validation

Deberá evitarse lógica como:

```python
if not value:
```

cuando:

```text
0
False
""
```

puedan ser valores válidos.

---

## 20.38 Phase 3 Tests

Deberán incluir:

```text
missing field
wrong type
invalid enum
invalid relationship
valid contract
```

---

## 20.39 Zero Omission Gate

En esta fase deberá ejecutarse por primera vez la regla:

```text
remove every required field one by one
→ validation must fail
```

---

## 20.40 Phase 3 Exit Gate

```text
positive validation = PASS
negative validation = PASS
zero omission validation = PASS
global pytest = PASS
```

---

# 20.41 Phase 4 — Serialization

Después deberá construirse el serializer canónico.

---

## 20.42 Serializer responsibility

El serializer deberá transformar:

```text
typed internal structures
```

en:

```text
canonical delivery representation
```

---

## 20.43 Canonical values

Deberán soportarse explícitamente:

```text
None
bool
int
float
str
list
dict
Enum
UUID
date
datetime
```

si aparecen realmente en los contratos.

---

## 20.44 Unsupported values

Un tipo no soportado deberá producir:

```text
DeliverySerializationError
```

o equivalente.

---

## 20.45 Prohibición crítica

No deberá utilizarse:

```python
default=str
```

como estrategia general de serialización.

---

## 20.46 Identifier safety

Los identificadores deberán conservar su representación.

Ejemplo:

```text
"0012"
```

no deberá convertirse en:

```text
12
```

---

## 20.47 Null safety

```text
None
```

deberá convertirse en:

```json
null
```

sin reinterpretación.

---

## 20.48 Datetime safety

Los timestamps deberán producir una representación definida y consistente.

---

## 20.49 Phase 4 Tests

Deberán incluir:

```text
primitive types
nested structures
enums
UUIDs
dates
datetimes
null
unsupported objects
identifier preservation
```

---

## 20.50 Round-trip semantic test

Cuando corresponda:

```text
serialize
      ↓
deserialize
      ↓
semantic equivalence
```

---

## 20.51 Phase 4 Exit Gate

```text
serializer tests = PASS
unsupported type test = PASS
semantic preservation = PASS
global pytest = PASS
```

---

# 20.52 Phase 5 — Consumer Model

Solo después de poseer contratos y serialización deberá materializarse el modelo de consumers.

---

## 20.53 ConsumerProfile

Deberá representar:

```text
consumer identity
supported contract versions
supported content types
enabled state
adapter mapping
```

cuando sean necesarios.

---

## 20.54 Consumer Registry

Podrá existir:

```text
ConsumerRegistry
```

si la arquitectura confirma que el patrón aporta valor.

---

## 20.55 Registry responsibilities

Deberá limitarse a:

```text
register
resolve
inspect
```

No deberá ejecutar Delivery.

---

## 20.56 Initial Consumer

Durante Sprint 23 podrá utilizarse un consumidor técnico de prueba.

Ejemplo conceptual:

```text
TEST_CONSUMER
```

o un identificador alineado con el repositorio.

No deberá fingirse integración con Portal si todavía no existe.

---

## 20.57 Phase 5 Tests

```text
register
resolve
duplicate
unknown
disabled
compatible
incompatible
```

---

## 20.58 Phase 5 Exit Gate

```text
consumer tests = PASS
compatibility tests = PASS
global pytest = PASS
```

---

# 20.59 Phase 6 — Adapter Abstraction

Ahora podrá definirse la frontera de transporte.

---

## 20.60 DeliveryAdapter

Deberá existir una interfaz o abstracción equivalente.

Conceptualmente:

```python
deliver(envelope, context) -> AdapterResult
```

La firma definitiva dependerá de la arquitectura real.

---

## 20.61 Adapter responsibility

El adapter deberá:

```text
accept payload
perform delivery mechanism
return normalized result
```

---

## 20.62 Adapter prohibitions

No deberá:

```text
modify cognition
rebuild response
interpret evidence
apply UI logic
authorize consumer
```

---

## 20.63 Adapter identity

Cada adapter deberá poseer identidad estable.

Ejemplo:

```text
IN_MEMORY
```

---

## 20.64 Adapter Registry

Podrá existir:

```text
AdapterRegistry
```

si múltiples adapters requieren resolución dinámica.

---

## 20.65 Avoid premature registry

Si Sprint 23 solo necesita un adapter y la arquitectura no exige resolución dinámica inmediata, deberá evaluarse si el Registry puede diferirse.

No deberá introducirse complejidad innecesaria.

---

## 20.66 Phase 6 Tests

Deberán verificar:

```text
adapter contract
adapter result
no mutation
error normalization
```

---

## 20.67 Phase 6 Exit Gate

```text
adapter abstraction tests = PASS
global pytest = PASS
```

---

# 20.68 Phase 7 — InMemory Adapter

El primer adapter real deberá ser:

```text
InMemoryDeliveryAdapter
```

o equivalente.

---

## 20.69 Por qué InMemory primero

Permite probar Delivery sin:

```text
HTTP
network
framework
browser
external service
```

---

## 20.70 InMemory behavior

Deberá poder:

```text
receive envelope
capture payload
return AdapterResult
```

---

## 20.71 No artificial intelligence in adapter

El adapter no deberá modificar contenido.

---

## 20.72 Captured payload

En tests podrá conservar:

```text
last_delivery
```

o una colección controlada.

Esto deberá ser exclusivamente infraestructura de prueba o adapter in-memory.

---

## 20.73 Reset capability

Si mantiene estado, deberá poder limpiarse entre tests.

---

## 20.74 Phase 7 Tests

```text
delivery captured
payload unchanged
context preserved
result successful
state isolated
```

---

## 20.75 Failing InMemory Adapter

Podrá existir un test double separado que genere fallo deliberado.

No deberá contaminar el adapter normal.

---

## 20.76 Phase 7 Exit Gate

```text
in-memory tests = PASS
failure simulation = PASS
global pytest = PASS
```

---

# 20.77 Phase 8 — Delivery Orchestration

Solo en este punto deberá construirse el orquestador principal.

---

## 20.78 Possible name

Podría denominarse:

```text
DeliveryService
```

o:

```text
ResponseDeliveryService
```

La nomenclatura definitiva deberá alinearse con los estándares existentes.

---

## 20.79 Delivery Pipeline

El flujo deberá ser explícito:

```text
receive materialized response
      ↓
create delivery identity
      ↓
build context
      ↓
resolve consumer
      ↓
validate compatibility
      ↓
validate response
      ↓
serialize
      ↓
resolve adapter
      ↓
build envelope
      ↓
adapter.deliver
      ↓
normalize result
      ↓
complete trace
      ↓
return DeliveryResult
```

---

## 20.80 Pipeline ordering matters

El orden no deberá alterarse arbitrariamente.

Por ejemplo:

```text
adapter execution
```

nunca deberá ocurrir antes de:

```text
validation
```

---

## 20.81 One orchestration authority

Deberá existir una autoridad clara para coordinar Delivery.

No:

```text
validator partially delivers
serializer partially routes
adapter partially validates consumer
```

---

## 20.82 Happy Path Test

Deberá existir una prueba integral:

```text
valid response
+
valid consumer
+
valid adapter
→ DELIVERED
```

---

## 20.83 Rejection Path

```text
invalid precondition
→ REJECTED
→ adapter NOT called
```

---

## 20.84 Failure Path

```text
valid preconditions
+
operational adapter failure
→ FAILED
```

---

## 20.85 Serialization Failure Path

```text
unsupported value
→ FAILED
→ adapter NOT called
```

según la taxonomía final establecida.

---

## 20.86 Phase 8 Exit Gate

```text
happy path = PASS
rejection path = PASS
failure path = PASS
trace preservation = PASS
global pytest = PASS
```

---

# 20.87 Phase 9 — Error Normalization

Aunque los errores se hayan definido previamente, en esta fase deberá consolidarse su comportamiento extremo a extremo.

---

## 20.88 Exception Boundary

Las excepciones internas conocidas deberán transformarse en:

```text
DeliveryError
```

controlado.

---

## 20.89 No blanket except

Deberá evitarse:

```python
except Exception:
    pass
```

---

## 20.90 Unexpected Exceptions

Una excepción inesperada deberá:

```text
be captured at appropriate boundary
be observable
produce controlled failure
preserve trace
```

sin exponer detalles sensibles.

---

## 20.91 Error mapping table

Deberá existir una relación clara:

```text
Validation Error
→ REJECTED

Consumer Compatibility Error
→ REJECTED

Serialization Error
→ FAILED

Adapter Error
→ FAILED
```

La clasificación definitiva deberá coincidir con los capítulos previos.

---

## 20.92 Error code stability

Los códigos deberán ser:

```text
stable
documented
testable
```

---

## 20.93 Phase 9 Tests

Cada error público deberá poseer al menos una prueba.

---

## 20.94 Phase 9 Exit Gate

```text
all error paths = PASS
no silent exception = VERIFIED
global pytest = PASS
```

---

# 20.95 Phase 10 — Observability

Una vez estable el pipeline deberá instrumentarse.

---

## 20.96 Logging First

La primera implementación podrá utilizar:

```python
logging
```

estándar de Python.

---

## 20.97 Minimum terminal record

Cada operación deberá permitir registrar:

```text
delivery_id
response_id
consumer_id
adapter_id
status
error_code if any
```

---

## 20.98 No payload logging

El payload completo no deberá registrarse por defecto.

---

## 20.99 EventBus Integration

Antes de integrar eventos deberá revisarse el EventBus real de HEYTI.

---

## 20.100 Reuse before creation

Si EventBus ya soporta eventos adecuados, deberá reutilizarse.

No deberá crearse:

```text
DeliveryEventBus
```

sin necesidad.

---

## 20.101 Events MVP

Si se implementan:

```text
delivery.started
delivery.completed
delivery.rejected
delivery.failed
```

serán suficientes inicialmente.

---

## 20.102 Metrics

Las métricas avanzadas podrán diferirse si no existe todavía infraestructura común.

Sin embargo, el diseño deberá permitir incorporarlas.

---

## 20.103 Duration

El trace deberá permitir al menos calcular:

```text
delivery duration
```

---

## 20.104 Phase 10 Tests

```text
terminal trace exists
error stage exists
logging excludes secrets
event terminal uniqueness
```

cuando correspondan.

---

## 20.105 Phase 10 Exit Gate

```text
observability tests = PASS
security logging review = PASS
global pytest = PASS
```

---

# 20.106 Phase 11 — Runtime Integration

Solo después de certificar Delivery de forma aislada deberá conectarse con Runtime.

---

## 20.107 Integration Boundary

El punto exacto deberá identificarse mediante auditoría del código real.

Conceptualmente:

```text
CapabilityRuntime
      ↓
Capability Result
      ↓
Materialization
      ↓
Delivery
```

---

## 20.108 No Runtime Rewrite

Sprint 23 no deberá reescribir CapabilityRuntime para acomodar Delivery.

La integración deberá ser mínima y explícita.

---

## 20.109 Runtime responsibility

Runtime deberá producir o coordinar la obtención de una respuesta materializada.

Delivery deberá encargarse únicamente de entregarla.

---

## 20.110 Delivery responsibility

Delivery no deberá ejecutar capabilities.

---

## 20.111 Runtime integration test

Deberá existir una vertical controlada.

Preferentemente:

```text
DescribeSection
```

por ser una capability ya materializada y probada.

---

## 20.112 DescribeSection vertical slice

El flujo deberá ser:

```text
DescribeSection Request
      ↓
CapabilityRuntime
      ↓
DescribeSection
      ↓
Materialization
      ↓
HEYTI Response
      ↓
Runtime Response Delivery
      ↓
InMemory Adapter
      ↓
DeliveryResult
```

---

## 20.113 Known section fixture

Deberá utilizarse una sección de prueba conocida por el repositorio.

No deberá dependerse inicialmente de infraestructura externa si existe una fixture adecuada.

---

## 20.114 What the test must prove

Deberá demostrar:

```text
Capability executes
Materialization succeeds
Response ID exists
Delivery ID exists
Consumer is resolved
Adapter receives payload
Delivery status = DELIVERED
Trace remains correlated
```

---

## 20.115 Runtime Failure Isolation

Si Delivery falla:

```text
Capability result
```

no deberá ser reescrito.

---

## 20.116 Delivery as downstream state

El Runtime deberá poder distinguir:

```text
capability succeeded
delivery failed
```

si ese escenario ocurre.

---

## 20.117 No semantic rollback

Un fallo de Delivery no convierte una respuesta cognitiva correcta en una respuesta cognitivamente incorrecta.

---

## 20.118 Phase 11 Exit Gate

```text
DescribeSection vertical slice = PASS
Delivery trace = PASS
Materialization regression = PASS
Runtime regression = PASS
global pytest = PASS
```

---

# 20.119 Phase 12 — Verification and Certification

Después de completar implementación deberá ejecutarse la certificación definida en el Capítulo 19.

---

## 20.120 Targeted Tests

Primero:

```text
pytest tests/<delivery-scope> -q
```

según estructura real.

---

## 20.121 Global Tests

Después:

```text
pytest -q
```

---

## 20.122 Diff Verification

```text
git diff --check
```

---

## 20.123 Status Verification

```text
git status
```

---

## 20.124 Changed Files Review

Deberán revisarse todos los archivos modificados.

---

## 20.125 No accidental files

Deberán eliminarse:

```text
temporary files
debug outputs
manual verification files
cache artifacts
```

que no formen parte del repositorio.

---

## 20.126 Acceptance Matrix

Cada criterio del Capítulo 19 deberá evaluarse.

---

## 20.127 Zero Error Audit

Deberá buscarse:

```text
unhandled exceptions
broken imports
ambiguous states
unexpected mutation
```

---

## 20.128 Zero Omission Audit

Deberá revisarse:

```text
required fields
trace IDs
warnings
versions
error codes
consumer metadata
adapter metadata
tests
```

---

## 20.129 Architecture Conformance Audit

Deberá comprobarse:

```text
no UI dependency
no transport dependency in Core
no capability execution inside Delivery
no Materialization duplication
no hidden global context
```

---

## 20.130 Final Certification

Solo entonces podrá declararse:

```text
SPRINT 23
HEYTI RUNTIME RESPONSE DELIVERY
CERTIFIED
```

o el estado real correspondiente.

---

# 20.131 Orden exacto recomendado de materialización

El orden de trabajo deberá ser:

```text
01. Audit repository
02. Confirm package location
03. Confirm existing reusable abstractions
04. Create contracts
05. Test contracts
06. Create context/trace
07. Test context/trace
08. Create validator
09. Test validator
10. Create serializer
11. Test serializer
12. Create consumer model
13. Test consumer model
14. Create adapter abstraction
15. Test adapter abstraction
16. Create InMemory adapter
17. Test InMemory adapter
18. Create Delivery orchestration
19. Test happy path
20. Test rejection paths
21. Test failure paths
22. Consolidate error mapping
23. Add observability
24. Test observability
25. Integrate Runtime
26. Test DescribeSection vertical slice
27. Run targeted tests
28. Run global pytest
29. Run git diff --check
30. Perform Zero Omission Audit
31. Perform Architecture Conformance Audit
32. Review git status
33. Commit certified implementation
```

---

## 20.132 One Step at a Time Rule

Durante implementación no deberán ejecutarse cinco fases simultáneamente.

La disciplina será:

```text
implement
      ↓
test
      ↓
verify
      ↓
continue
```

---

## 20.133 No "we will fix tests later"

Queda prohibida la estrategia:

```text
implement everything
      ↓
run tests at the end
```

---

## 20.134 Micro-baselines

Después de cada fase importante deberá existir un estado funcional verificable.

Esto permitirá localizar regresiones inmediatamente.

---

## 20.135 Commit Strategy

No será obligatorio realizar un commit por cada archivo.

Sí deberá evitarse acumular una masa de cambios imposible de revisar.

---

## 20.136 Suggested Commit Boundaries

Podrían utilizarse, según evolución real:

```text
contracts + validation
serialization
consumers + adapters
delivery pipeline
runtime integration
certification
```

No constituyen una obligación.

---

## 20.137 No commit without green tests

Cada commit arquitectónicamente significativo debería realizarse con la suite correspondiente en verde.

---

## 20.138 Global Suite Frequency

La suite global deberá ejecutarse al menos después de cada fase con integración relevante.

Si continúa siendo rápida, podrá ejecutarse después de cada cambio importante.

---

## 20.139 Scope Freeze

Durante implementación deberá mantenerse congelado el alcance principal.

No deberán incorporarse espontáneamente:

```text
WebSocket
streaming
retry engine
message broker
advanced cache
React UI
distributed tracing platform
```

---

## 20.140 Deferred Items

Estos elementos deberán registrarse como:

```text
DEFERRED BY DESIGN
```

si aparecen como necesidades futuras.

---

## 20.141 Sprint 23 MVP

El núcleo mínimo deberá demostrar:

```text
Materialized Response
      ↓
Validated
      ↓
Serialized
      ↓
Consumer-resolved
      ↓
Adapter-delivered
      ↓
Traceable DeliveryResult
```

---

## 20.142 Sprint 23 Non-MVP

No es necesario para certificar el núcleo inicial:

```text
HTTP production adapter
WebSocket
message broker
retry policy
streaming
visual Portal
charts
maps
distributed telemetry
persistent audit store
```

salvo decisión explícita posterior.

---

## 20.143 Gateway Preparation

Aunque Gateway real pueda diferirse, Delivery deberá quedar preparado para recibir un adapter futuro.

---

## 20.144 HTTP Adapter Future

Conceptualmente:

```text
HTTPDeliveryAdapter
```

podrá añadirse sin modificar:

```text
Materialization
Delivery Contract
Consumer semantics
```

---

## 20.145 WebSocket Adapter Future

Deberá poder incorporarse como otro adapter si la semántica lo permite.

---

## 20.146 Message Queue Future

Igualmente:

```text
QueueDeliveryAdapter
```

podrá existir sin alterar cognición.

---

## 20.147 Proof of extensibility

La existencia del InMemory adapter deberá demostrar que Delivery no depende intrínsecamente de HTTP.

---

## 20.148 Proof of replaceability

Una prueba con un segundo fake adapter podrá demostrar sustitución aunque no sea productivo.

---

## 20.149 Presentation Deferred

La integración visual deberá comenzar después de que Delivery tenga una frontera estable.

---

## 20.150 UI Readiness Trigger

El inicio de UI deberá activar formalmente:

```text
Six-Module Data Source Coverage Audit
```

antes de construir la experiencia completa.

---

## 20.151 Coverage before visualization

La secuencia futura será:

```text
audit data
      ↓
confirm capability coverage
      ↓
confirm materialization
      ↓
confirm Delivery Content Type
      ↓
build renderer
```

---

## 20.152 No renderer before data truth

No deberá construirse una gráfica únicamente porque visualmente resulte atractiva.

Primero deberá existir:

```text
reliable source
```

---

## 20.153 DescribeSection as bridge to UI

Una vez HRRD esté estable, `DescribeSection` podrá convertirse en la primera vertical visual.

---

## 20.154 First Visual Slice Future

Conceptualmente:

```text
User
      ↓
Section Query
      ↓
HEYTI
      ↓
DescribeSection
      ↓
Materialization
      ↓
Delivery
      ↓
Gateway
      ↓
Portal
      ↓
Section Radiography
```

---

## 20.155 First Map Slice Future

Posteriormente:

```text
TERRITORIAL_REFERENCE
      ↓
Portal Geometry Resolver
      ↓
Leaflet
      ↓
Section Highlight
```

---

## 20.156 First KPI Slice Future

```text
METRIC
      ↓
Portal Adapter
      ↓
KPI Component
```

---

## 20.157 First Chart Slice Future

```text
SERIES
      ↓
Portal Adapter
      ↓
Chart Renderer
```

---

## 20.158 Implementation Risk Register

Durante Sprint 23 deberán vigilarse especialmente los siguientes riesgos.

---

## 20.159 Risk R1 — Duplicate Materialization

Síntoma:

```text
Delivery reconstructs response
```

Mitigación:

```text
consume Materialization output directly
```

---

## 20.160 Risk R2 — HTTP Coupling

Síntoma:

```text
DeliveryResult contains HTTP status as primary semantic status
```

Mitigación:

```text
Delivery semantic status first
Gateway mapping later
```

---

## 20.161 Risk R3 — UI Coupling

Síntoma:

```text
chart type
CSS color
Leaflet options
HTML
```

dentro de Core.

Mitigación:

```text
semantic Content Types only
```

---

## 20.162 Risk R4 — Serialization Shortcut

Síntoma:

```python
json.dumps(obj, default=str)
```

Mitigación:

```text
explicit canonical serializer
```

---

## 20.163 Risk R5 — Hidden Global Context

Síntoma:

```text
global current_consumer
global current_session
```

Mitigación:

```text
explicit DeliveryContext
```

---

## 20.164 Risk R6 — Silent Failure

Síntoma:

```python
except Exception:
    return None
```

Mitigación:

```text
structured DeliveryError
```

---

## 20.165 Risk R7 — Premature Retry

Síntoma:

```text
adapter silently retries
```

Mitigación:

```text
one operation = one attempt
```

---

## 20.166 Risk R8 — Contract Drift

Síntoma:

```text
serializer emits fields not represented in contract
```

Mitigación:

```text
contract tests + golden fixtures
```

---

## 20.167 Risk R9 — Test-only Architecture

Síntoma:

```text
production design distorted solely to satisfy fixtures
```

Mitigación:

```text
architecture remains authoritative
```

---

## 20.168 Risk R10 — Overengineering

Síntoma:

```text
dozens of abstractions before first delivery
```

Mitigación:

```text
implement only abstractions justified by current contract
```

---

## 20.169 Risk R11 — Underengineering

Síntoma:

```text
single deliver() function handling everything
```

Mitigación:

```text
preserve explicit boundaries
```

---

## 20.170 Risk R12 — False Integration

Síntoma:

```text
manual JSON print claimed as Portal integration
```

Mitigación:

```text
certify only what actually exists
```

---

## 20.171 Risk R13 — Data Source Assumption

Síntoma:

```text
UI expects metric not backed by validated source
```

Mitigación:

```text
coverage audit before visual activation
```

---

## 20.172 Risk R14 — Trace Loss

Síntoma:

```text
response_id disappears after serialization
```

Mitigación:

```text
trace tests at every boundary
```

---

## 20.173 Risk R15 — Existing Runtime Regression

Síntoma:

```text
Delivery tests pass
existing capability tests fail
```

Mitigación:

```text
global pytest after integration
```

---

# 20.174 Implementation Decision Log

Durante implementación, cualquier desviación significativa respecto a este plan deberá registrarse.

Ejemplo:

```text
Decision:
AdapterRegistry deferred.

Reason:
Only one adapter exists and no runtime resolution is required.

Impact:
None on contract.

Future trigger:
Second production adapter.
```

---

## 20.175 ADR threshold

No toda decisión requiere un ADR.

Deberá considerarse ADR cuando la decisión:

```text
changes architecture
creates long-term constraint
affects multiple components
is difficult to reverse
```

---

## 20.176 Minor implementation decision

Decisiones locales podrán registrarse en Sprint 23 o commit.

---

## 20.177 No undocumented architectural deviation

Una desviación importante no deberá introducirse silenciosamente.

---

# 20.178 Proposed Technical Dependency Graph

La dependencia deberá permanecer conceptualmente:

```text
Materialization Contracts
          │
          ▼
   Delivery Contracts
          │
    ┌─────┴─────┐
    ▼           ▼
 Context     Validation
    │           │
    └─────┬─────┘
          ▼
     Serialization
          │
          ▼
      Consumers
          │
          ▼
       Adapters
          │
          ▼
  Delivery Orchestration
          │
          ▼
    Observability
          │
          ▼
 Runtime Integration
```

---

## 20.179 Forbidden Dependency Direction

No deberá ocurrir:

```text
Materialization
      ↓ depends on
Delivery
```

Materialization deberá permanecer independiente.

---

## 20.180 Another forbidden dependency

No:

```text
Capability
      ↓ depends on
DeliveryAdapter
```

---

## 20.181 Presentation forbidden dependency

No:

```text
Delivery
      ↓ depends on
Portal HTML
```

---

## 20.182 Gateway dependency

Gateway podrá depender de Delivery.

Delivery no deberá depender del framework del Gateway.

---

## 20.183 Adapter dependency

Un adapter concreto podrá depender de una librería técnica.

La abstracción de Delivery no.

---

# 20.184 Suggested Test Growth

La suite deberá crecer aproximadamente por capacidades, no por una cuota arbitraria.

Ejemplo conceptual:

```text
Contracts
+ Context
+ Validation
+ Serialization
+ Consumers
+ Adapters
+ Pipeline
+ Integration
```

---

## 20.185 No target test count

No deberá establecerse:

```text
we need exactly 50 tests
```

La cantidad será consecuencia de la cobertura requerida.

---

## 20.186 Test count as evidence

Al cierre sí deberá registrarse el número real.

---

# 20.187 Safe Implementation Rhythm

La rutina recomendada durante codificación será:

```text
1. inspect
2. change one boundary
3. run focused tests
4. inspect diff
5. run global tests when appropriate
6. continue
```

---

## 20.188 Small Diff Principle

Cambios pequeños facilitan:

```text
review
diagnosis
rollback
```

---

## 20.189 Stop Condition

Si una fase rompe arquitectura previa:

```text
STOP
```

antes de continuar.

---

## 20.190 No cascading patches

No deberán añadirse parches sobre parches para forzar la suite a verde sin comprender el problema.

---

## 20.191 Root Cause First

Ante fallo:

```text
identify root cause
      ↓
decide architectural responsibility
      ↓
fix correct layer
```

---

# 20.192 Implementation Completion Checklist

Antes de declarar implementación terminada:

```text
[ ] Repository audited
[ ] Materialization boundary confirmed
[ ] Contracts implemented
[ ] Context implemented
[ ] Trace implemented
[ ] Validation implemented
[ ] Serialization implemented
[ ] Consumer model implemented
[ ] Adapter abstraction implemented
[ ] InMemory adapter implemented
[ ] Delivery orchestration implemented
[ ] Errors normalized
[ ] Observability baseline implemented
[ ] Runtime integration tested
[ ] DescribeSection vertical slice tested
[ ] Targeted tests green
[ ] Global tests green
[ ] git diff --check clean
[ ] Zero Error audit complete
[ ] Zero Omission audit complete
[ ] Architecture conformance complete
```

---

## 20.193 Sprint Completion Checklist

Después:

```text
[ ] Documentation updated
[ ] Deferred items documented
[ ] Acceptance matrix completed
[ ] Changed files reviewed
[ ] Temporary artifacts removed
[ ] Git status reviewed
[ ] Final commit created
[ ] Commit hash recorded
```

---

# 20.194 Implementation Invariants

Se establecen los siguientes invariantes.

### HRRD-IMP01 — Audit Before Code

La implementación comenzará únicamente después de revisar el repositorio real.

### HRRD-IMP02 — Contract First

Los contratos deberán preceder al pipeline operacional.

### HRRD-IMP03 — Incremental Construction

Cada frontera deberá probarse antes de construir la siguiente.

### HRRD-IMP04 — Materialization Independence

Delivery no duplicará responsabilidades de Materialization.

### HRRD-IMP05 — InMemory First

El primer adapter deberá permitir verificar Delivery sin infraestructura externa.

### HRRD-IMP06 — Validation Before Adapter

Ningún adapter deberá ejecutarse antes de superar validación.

### HRRD-IMP07 — Explicit Error Mapping

Todo fallo deberá producir comportamiento definido.

### HRRD-IMP08 — Runtime Integration Last

La integración con Runtime ocurrirá después de estabilizar Delivery aisladamente.

### HRRD-IMP09 — Global Regression Gate

Cada integración relevante deberá preservar la suite global.

### HRRD-IMP10 — Certification Before Expansion

No se avanzará a Gateway o Presentation real sin verificar el núcleo correspondiente.

---

# 20.195 Secuencia maestra del Sprint 23

La secuencia completa queda formalizada como:

```text
Architecture Document
        ↓
Repository Audit
        ↓
Materialization Boundary Verification
        ↓
Contracts
        ↓
Context + Trace
        ↓
Validation
        ↓
Serialization
        ↓
Consumer Model
        ↓
Adapter Abstraction
        ↓
InMemory Adapter
        ↓
Delivery Pipeline
        ↓
Error Normalization
        ↓
Observability
        ↓
Runtime Integration
        ↓
DescribeSection Vertical Slice
        ↓
Verification
        ↓
Zero Error Audit
        ↓
Zero Omission Audit
        ↓
Certification
        ↓
Sprint 23 Baseline
```

---

## 20.196 Resultado técnico esperado

Al terminar Sprint 23 deberá ser posible ejecutar conceptualmente:

```python
result = delivery_service.deliver(
    response=materialized_response,
    consumer_id="TEST_CONSUMER",
)
```

y obtener una estructura equivalente a:

```text
DeliveryResult
├── delivery_id
├── response_id
├── consumer_id
├── adapter_id
├── status = DELIVERED
└── trace
```

sin:

```text
HTTP
browser
Portal
Leaflet
Chart.js
```

---

## 20.197 Resultado arquitectónico esperado

Esto demostrará que HEYTI posee una nueva frontera estable:

```text
Cognition
      ↓
Materialization
      ↓
Delivery
      ↓
External World
```

---

## 20.198 Lo que Sprint 23 no deberá hacer

Sprint 23 no deberá convertirse en:

```text
UI Sprint
Gateway Sprint
WebSocket Sprint
Portal Rewrite Sprint
Data Migration Sprint
```

Su misión es materializar correctamente:

```text
Runtime Response Delivery
```

---

## 20.199 Criterio de éxito del capítulo

El plan de implementación será considerado correcto cuando permita construir HRRD:

- sin duplicar componentes existentes;
- sin alterar Materialization;
- sin contaminar Runtime;
- sin acoplarse a HTTP;
- sin acoplarse a Presentation;
- con pruebas desde cada fase;
- con una vertical real de DescribeSection;
- y con una certificación reproducible al final.

---

## 20.200 Declaración arquitectónica del capítulo

Sprint 23 deberá implementarse con una disciplina de construcción incremental.

No deberá saltarse desde la arquitectura directamente hacia una interfaz visible.

La frontera de Delivery deberá existir primero como componente independiente, verificable y sustituible.

Cada paso deberá responder tres preguntas:

```text
Is the responsibility correct?
Is the contract preserved?
Do the tests prove it?
```

Solo cuando las tres respuestas sean afirmativas deberá avanzarse.

La regla arquitectónica consolidada queda establecida como:

> **HEYTI Runtime Response Delivery deberá materializarse desde sus contratos hacia sus mecanismos externos, construyendo y certificando cada frontera antes de integrar la siguiente. La velocidad de implementación nunca deberá sustituir la verificación arquitectónica.**

La disciplina operacional queda resumida como:

```text
AUDIT
  ↓
BUILD
  ↓
TEST
  ↓
VERIFY
  ↓
CERTIFY
  ↓
CONTINUE
```

y permanece vigente el principio rector del desarrollo:

```text
0 ERRORES
0 OMISIONES
```

Con el plan de implementación formalmente establecido, queda preparada la siguiente dimensión del documento:

**gobernanza, compatibilidad evolutiva, deuda técnica controlada, elementos diferidos y reglas para la evolución futura de Runtime Response Delivery.**

---

**Fin del Capítulo 20**


# Capítulo 21. Gobernanza, deuda técnica controlada, elementos diferidos y evolución futura de Runtime Response Delivery

## 21.1 Propósito del capítulo

Este capítulo define las reglas de **gobernanza, control de deuda técnica, administración de elementos diferidos y evolución futura** de HEYTI Runtime Response Delivery.

La finalidad es evitar que, una vez implementado Sprint 23, el subsistema evolucione mediante:

```text
parches aislados
decisiones no documentadas
acoplamientos accidentales
excepciones permanentes
compatibilidad implícita
crecimiento descontrolado
```

Runtime Response Delivery deberá continuar evolucionando bajo la misma disciplina arquitectónica que permitió construirlo.

La regla fundamental será:

> **Toda evolución futura de Delivery deberá preservar sus fronteras, contratos, trazabilidad y sustituibilidad, o deberá justificar explícitamente por qué una modificación arquitectónica es necesaria.**

---

## 21.2 Gobernanza como continuidad

La arquitectura no termina cuando el código funciona.

Después de la implementación comienza una segunda responsabilidad:

```text
Preserve the architecture over time.
```

Sin gobernanza, incluso un diseño correcto puede degradarse gradualmente.

---

## 21.3 Riesgo de erosión arquitectónica

La erosión puede comenzar con cambios aparentemente pequeños.

Ejemplos:

```text
"solo agreguemos este campo para Portal"
```

```text
"solo hagamos un retry aquí"
```

```text
"solo llamemos directamente esta capability"
```

```text
"solo serialicemos con default=str"
```

Cada decisión aislada puede parecer razonable.

Acumuladas, pueden destruir la frontera.

---

## 21.4 Architectural Drift

Se define:

```text
Architectural Drift
```

como la divergencia progresiva entre:

```text
documented architecture
```

y:

```text
actual implementation
```

La gobernanza deberá detectarlo y corregirlo.

---

## 21.5 Fuentes de drift

Las causas más comunes serán:

```text
urgent fixes
new consumers
new transports
UI pressure
performance patches
security exceptions
temporary compatibility code
```

---

## 21.6 Temporary Code Risk

Todo código introducido como:

```text
temporary
```

deberá tener:

- propósito;
- alcance;
- criterio de retiro;
- owner o responsable lógico;
- trigger de eliminación.

De lo contrario suele convertirse en permanente.

---

## 21.7 Deuda técnica

Se define deuda técnica como una decisión conscientemente subóptima aceptada temporalmente para cumplir una necesidad legítima.

No deberá confundirse con:

```text
bug
omission
undocumented shortcut
```

---

## 21.8 Deuda técnica permitida

Una deuda técnica será aceptable únicamente cuando exista:

```text
explicit decision
known impact
bounded scope
future remediation path
```

---

## 21.9 Deuda técnica no permitida

No deberá etiquetarse como deuda técnica:

```text
missing required validation
broken traceability
security bypass
silent data loss
contract violation
```

Estos son defectos.

---

## 21.10 Technical Debt Register

Sprint 23 podrá mantener conceptualmente un:

```text
HRRD Technical Debt Register
```

con elementos como:

```text
ID
description
reason
impact
risk
remediation trigger
status
```

No necesariamente deberá ser un sistema complejo.

Puede comenzar como sección documental.

---

## 21.11 Ejemplo de deuda válida

```text
TD-HRRD-001

Description:
Only InMemory adapter implemented.

Reason:
Core Delivery certification before network integration.

Impact:
No production network delivery yet.

Risk:
Low.

Trigger:
Gateway implementation sprint.
```

Esto es deuda o alcance diferido controlado.

---

## 21.12 Ejemplo de defecto, no deuda

```text
Delivery occasionally loses response_id.
```

No puede clasificarse como:

```text
technical debt
```

Debe corregirse.

---

## 21.13 Elementos diferidos

Los capítulos anteriores identificaron múltiples elementos deliberadamente diferidos.

Deberán distinguirse de omisiones accidentales.

---

## 21.14 Deferred by Design

Se utilizará el concepto:

```text
DEFERRED BY DESIGN
```

para funcionalidades no necesarias en Sprint 23 pero previstas arquitectónicamente.

---

## 21.15 Deferred Item Register

Cada elemento diferido deberá registrar:

```text
feature
reason for deferral
future trigger
dependencies
risk
```

---

## 21.16 Elementos diferidos iniciales

Se consideran candidatos naturales:

```text
HTTP production adapter
Gateway real
WebSocket adapter
streaming
automatic retry
multi-version negotiation
persistent audit store
distributed tracing
payload signing
advanced security model
dynamic consumer discovery
contract downgrade/upgrade adapters
```

---

## 21.17 Diferido no significa comprometido

Un elemento diferido no significa que necesariamente será implementado.

Significa:

> La arquitectura reconoce el posible caso futuro sin obligarse a construirlo ahora.

---

## 21.18 Future Trigger

Todo elemento diferido debería tener un trigger.

Ejemplo:

```text
WebSocket
Trigger:
real need for push or streaming UI
```

---

## 21.19 No speculative implementation

Queda prohibido implementar componentes únicamente porque:

```text
"tal vez algún día los necesitemos"
```

La arquitectura deberá permitirlos.

No necesariamente materializarlos.

---

## 21.20 YAGNI controlado

El principio podrá expresarse:

```text
You Aren't Gonna Need It
```

pero con arquitectura preparada.

Es decir:

```text
do not build speculative infrastructure
```

sin cerrar la posibilidad futura.

---

## 21.21 Gobernanza de contratos

Todo cambio en Delivery Contract deberá someterse a revisión.

---

## 21.22 Preguntas obligatorias para cambio contractual

Antes de añadir, eliminar o modificar un campo deberá preguntarse:

```text
What problem does this solve?
Is the field semantic or visual?
Is it required?
Who consumes it?
Does it break compatibility?
Does it duplicate existing information?
Does it expose sensitive data?
```

---

## 21.23 Consumer-driven changes

Un consumidor podrá solicitar cambios.

Pero el Core no deberá aceptar automáticamente todas las necesidades de UI como cambios contractuales.

---

## 21.24 Example

Solicitud:

```text
Portal needs red background for high risk.
```

Respuesta arquitectónica:

```text
Presentation concern.
Do not add CSS color to Delivery Contract.
```

---

## 21.25 Legitimate Consumer Request

Solicitud:

```text
Portal cannot interpret metric because unit is missing.
```

Esto sí puede revelar un defecto contractual legítimo.

---

## 21.26 Contract Governance Board Concept

Los cambios importantes deberán revisarse bajo la gobernanza arquitectónica de HEYTI.

No es necesario crear un comité formal separado.

El concepto representa:

```text
explicit architectural review
```

antes de cambios de impacto.

---

## 21.27 Change Levels

Se proponen niveles:

```text
LEVEL 0 — Internal implementation change
LEVEL 1 — Compatible internal/public extension
LEVEL 2 — Consumer-impacting compatible change
LEVEL 3 — Breaking architectural change
```

---

## 21.28 Level 0

Ejemplos:

```text
refactor
performance optimization
logging improvement
```

sin cambio contractual.

---

## 21.29 Level 1

Ejemplo:

```text
add optional internal trace metadata
```

sin impacto público.

---

## 21.30 Level 2

Ejemplo:

```text
add optional public Content Type
```

que consumidores pueden empezar a utilizar.

---

## 21.31 Level 3

Ejemplos:

```text
change DeliveryStatus semantics
remove required field
change consumer model
change adapter boundary
```

Requieren revisión formal.

---

## 21.32 ADR Requirement

Los cambios Level 3 deberán normalmente producir:

```text
ADR
```

o una decisión arquitectónica equivalente.

---

## 21.33 ADR Content

Deberá incluir:

```text
context
decision
alternatives
consequences
migration
compatibility
security
rollback
```

---

## 21.34 No ADR inflation

Los cambios menores no deberán generar ADR innecesariamente.

---

## 21.35 Architectural Baseline

Al cerrar Sprint 23 deberá existir una baseline identificable.

Conceptualmente:

```text
HRRD v1.0 Baseline
```

asociada con:

```text
architecture document
code
tests
commit
```

---

## 21.36 Baseline Meaning

Una baseline representa:

> El estado conocido y certificado desde el cual se evaluarán cambios futuros.

---

## 21.37 Baseline Preservation

No deberá modificarse retroactivamente documentación histórica para aparentar que decisiones nuevas siempre existieron.

---

## 21.38 Superseding Documents

Si una nueva versión reemplaza este documento, deberá indicarse:

```text
supersedes
```

y conservar el documento anterior.

---

## 21.39 No historical rewrite

La historia arquitectónica deberá poder reconstruirse.

---

## 21.40 Documentation Lifecycle

Los documentos podrán atravesar:

```text
DRAFT
ACTIVE
SUPERSEDED
ARCHIVED
```

según la gobernanza documental de HEYTI.

---

## 21.41 Active Architecture

Solo una especificación deberá actuar como autoridad vigente para una versión concreta.

---

## 21.42 Document-Version Alignment

Deberá mantenerse:

```text
Document v1.0
↔
Delivery Contract 1.0 architecture
```

sin asumir que ambos números siempre deben avanzar juntos.

---

## 21.43 Code-Documentation Alignment

Cada cambio estructural deberá actualizar documentación relevante.

---

## 21.44 No stale architecture

Un documento que ya no representa el código deberá:

```text
be updated
or
be superseded
```

---

## 21.45 Documentation Audit

En revisiones futuras deberá comprobarse:

```text
document says?
code does?
tests prove?
```

---

## 21.46 Governance by Tests

Los tests críticos actuarán como guardrails.

Ejemplo:

```text
test_adapter_does_not_mutate_payload
```

evita erosión silenciosa de esa frontera.

---

## 21.47 Conformance Test Preservation

Las pruebas arquitectónicas no deberán eliminarse únicamente para facilitar una nueva implementación.

Si una regla deja de ser válida, primero deberá cambiar la arquitectura.

---

## 21.48 Architecture before test deletion

Secuencia:

```text
new requirement
      ↓
architecture review
      ↓
decision
      ↓
update contract
      ↓
update tests
      ↓
update code
```

No:

```text
test fails
→ delete test
```

---

## 21.49 Consumer Governance

Todo nuevo Consumer deberá registrarse formalmente.

---

## 21.50 New Consumer Checklist

Antes de activar un nuevo consumidor:

```text
consumer_id defined
profile defined
contract versions declared
content types declared
authorization defined
adapter defined
tests passed
```

---

## 21.51 Consumer Removal

Retirar un consumidor deberá:

```text
disable
observe no use
remove mappings
remove profile
remove tests only when historical support no longer required
```

---

## 21.52 Consumer Deprecation

Podrá aplicarse una fase:

```text
ACTIVE
→ DEPRECATED
→ REMOVED
```

---

## 21.53 Adapter Governance

Todo nuevo adapter deberá cumplir criterios mínimos.

---

## 21.54 Adapter Admission Checklist

```text
adapter_id stable
configuration validated
timeout policy defined
success semantics defined
error mapping defined
security reviewed
no hidden retry
tests implemented
trace integration verified
```

---

## 21.55 Adapter Removal

Un adapter podrá retirarse sin cambiar Delivery Contract cuando no afecte semántica.

---

## 21.56 Adapter replacement

Ejemplo:

```text
HTTP implementation A
      ↓
HTTP implementation B
```

deberá ser posible manteniendo el contrato.

---

## 21.57 Transport Evolution

La aparición de un nuevo transporte no deberá justificar automáticamente un nuevo Delivery Contract.

---

## 21.58 Streaming Exception

Streaming sí podría requerir una extensión contractual significativa.

Deberá tratarse como decisión arquitectónica.

---

## 21.59 Streaming Governance Questions

Antes de introducir streaming deberá definirse:

```text
What is a response chunk?
What is completion?
How are errors represented?
How is trace preserved?
What is delivery_id?
What does DELIVERED mean?
```

---

## 21.60 Retry Governance

Los retries futuros requerirán una política formal.

---

## 21.61 Retry Admission Criteria

No deberá implementarse retry hasta resolver:

```text
idempotency
attempt identity
duplicate delivery risk
timeout ambiguity
trace relationship
max attempts
backoff
```

---

## 21.62 No adapter-local retry

Incluso cuando se introduzca, no deberá ocultarse dentro de un adapter.

---

## 21.63 Retry Observation

Cada intento deberá ser observable.

---

## 21.64 Security Governance

Todo cambio en frontera de salida deberá revisarse desde seguridad.

---

## 21.65 Security Review Trigger

Deberá activarse cuando se introduzcan:

```text
new consumer
new adapter
new Content Type
new external target
new authentication mechanism
new sensitive data
```

---

## 21.66 Sensitive Content Types

Ejemplos futuros:

```text
FIELD_CONTACT
PRECISE_LOCATION
DOCUMENT
FILE
```

deberán recibir revisión especial.

---

## 21.67 Presentation Governance

Presentation podrá evolucionar libremente dentro de su frontera.

Pero no deberá trasladar sus detalles al contrato central.

---

## 21.68 UI Pressure Test

Ante una solicitud visual deberá preguntarse:

```text
Can this be solved entirely in Presentation?
```

Si la respuesta es sí, no debe modificarse Delivery.

---

## 21.69 Presentation Contract Evolution

Si surge una capa formal de Presentation Contract, deberá gobernarse separadamente.

---

## 21.70 Data Governance and Presentation

Antes de nuevas visualizaciones deberá verificarse la fuente de datos.

---

## 21.71 Six-Module Data Coverage Governance

La matriz de cobertura de los seis módulos deberá mantenerse actualizada conforme se construyan nuevas capacidades.

---

## 21.72 Coverage Drift

Si una fuente se vuelve:

```text
outdated
partial
deprecated
```

las capacidades visuales deberán reflejarlo.

---

## 21.73 No stale green status

Una fuente no deberá mantenerse marcada:

```text
READY
```

si ya no cumple criterios.

---

## 21.74 Data-to-Presentation Traceability

Toda visualización importante deberá mantener relación con:

```text
source
capability
response block
renderer
```

---

## 21.75 Governance of Content Types

El catálogo:

```text
TEXT
METRIC
TABLE
SERIES
TERRITORIAL_REFERENCE
GEOMETRY
EVIDENCE
WARNING
ACTION
```

deberá crecer únicamente por necesidad semántica.

---

## 21.76 New Content Type Review

Antes de añadir uno:

```text
Can existing type represent it?
Is it semantically distinct?
Do consumers need to recognize it?
Does it create security risk?
```

---

## 21.77 No content-type explosion

No deberán añadirse:

```text
LINE_CHART
RED_CARD
BIG_NUMBER
MAP_POPUP
```

como Content Types del Core.

---

## 21.78 Error Governance

El catálogo de errores deberá permanecer pequeño y estable.

---

## 21.79 New Error Code Review

Antes de agregar uno deberá preguntarse:

```text
Can an existing public code represent this?
Does consumer need to distinguish it?
Is this only an internal subcode?
```

---

## 21.80 Public Error Stability

Una vez publicado, el significado de un código no deberá cambiar silenciosamente.

---

## 21.81 Metrics Governance

Las métricas deberán agregarse solo cuando respondan una pregunta operacional.

---

## 21.82 No metric vanity

No deberá instrumentarse un dato únicamente porque puede medirse.

---

## 21.83 Cardinality Review

Toda nueva label deberá evaluarse para evitar cardinalidad excesiva.

---

## 21.84 Observability Cost

La instrumentación deberá revisarse cuando:

```text
volume
storage
latency
```

crezcan significativamente.

---

## 21.85 Audit Governance

La auditoría deberá evolucionar conforme aumente criticidad operacional.

---

## 21.86 Audit Persistence Trigger

Podrá activarse cuando:

```text
external consumers
production use
compliance requirement
formal operational review
```

lo exijan.

---

## 21.87 Audit Data Classification

Antes de persistir deberán definirse:

```text
what
why
retention
access
deletion
```

---

## 21.88 No collect-all audit

No deberá guardarse toda información "por si acaso".

---

## 21.89 Performance Governance

Las optimizaciones deberán basarse en medición.

---

## 21.90 Optimization Proposal

Toda optimización relevante deberá indicar:

```text
baseline
bottleneck
expected improvement
tradeoff
```

---

## 21.91 No semantic optimization

No deberá eliminarse evidencia, warnings o metadata obligatoria únicamente para acelerar payload.

---

## 21.92 Performance Projection

Si el payload es demasiado grande, deberá evaluarse:

```text
reference-based delivery
pagination
projection
compression
```

sin pérdida silenciosa.

---

## 21.93 Cache Governance

Si se introduce cache deberá definirse:

```text
cache key
TTL
invalidations
contract version
authorization context
```

---

## 21.94 No unsafe shared cache

Una respuesta autorizada para un principal no deberá servirse a otro sin verificar contexto.

---

## 21.95 Response Reuse

La reutilización de una MaterializedResponse deberá conservar:

```text
same response_id
new delivery_id
```

cuando corresponda.

---

## 21.96 Replay Governance

Todo replay deberá ser:

```text
explicit
authorized
traceable
```

---

## 21.97 Concurrency Governance

Si el volumen aumenta deberá revisarse:

```text
thread safety
async safety
registry immutability
context isolation
```

---

## 21.98 Async Introduction Trigger

Solo deberá introducirse async cuando exista una necesidad medida como:

```text
I/O concurrency
Gateway scalability
WebSocket
streaming
```

---

## 21.99 Async Migration

Una migración async no deberá romper la API semántica de Delivery.

---

## 21.100 No async for fashion

No deberá adoptarse únicamente porque sea una práctica popular.

---

## 21.101 Distributed Delivery

En una fase futura HEYTI podría distribuir Delivery en procesos o servicios separados.

---

## 21.102 Distributed Boundary Questions

Antes de hacerlo deberán resolverse:

```text
message contract
delivery identity
exactly-once vs at-least-once semantics
trace propagation
failure recovery
security
ordering
```

---

## 21.103 No premature microservice extraction

Mientras no exista necesidad operativa clara, Delivery deberá permanecer dentro de HEYTI-CORE.

---

## 21.104 Service Extraction Trigger

Podría considerarse si existen:

```text
independent scaling
multiple runtime producers
multiple transport infrastructures
operational isolation needs
```

---

## 21.105 Event-driven Delivery

También podrá evaluarse un futuro modelo:

```text
ResponseMaterialized Event
      ↓
Delivery Worker
```

pero requeriría nuevas garantías.

---

## 21.106 Event Delivery Semantics

Deberán definirse:

```text
ordering
duplication
retry
dead letters
idempotency
```

antes de introducirlo.

---

## 21.107 Current preference

Para v1.0 deberá preferirse:

```text
synchronous explicit invocation
```

por trazabilidad y simplicidad.

---

## 21.108 Governance of dependencies

Ninguna librería nueva deberá agregarse sin revisar:

```text
need
maintenance
security
license
runtime impact
```

---

## 21.109 Standard Library First

Cuando sea razonable deberá preferirse la biblioteca estándar.

Ejemplo:

```text
logging
json
uuid
datetime
```

si cubre adecuadamente la necesidad.

---

## 21.110 Dependency Exception

Una librería externa sí podrá justificarse cuando reduzca riesgo o complejidad significativamente.

---

## 21.111 Pydantic Decision

Si se evalúa Pydantic deberá revisarse:

```text
existing project dependencies
current modeling style
runtime overhead
benefit over dataclasses
```

No deberá introducirse solo para HRRD si rompe coherencia.

---

## 21.112 JSON Schema Decision

JSON Schema podrá añadirse cuando:

```text
external contract validation
multiple consumers
API documentation
```

lo justifiquen.

---

## 21.113 No schema duplication

Si existe JSON Schema, deberá evitarse mantener reglas diferentes en:

```text
Python validator
schema
documentation
```

sin una fuente de verdad clara.

---

## 21.114 Source of Truth Governance

Cada dimensión deberá poseer una autoridad.

Ejemplo:

```text
Contract fields
→ contract model

Public version
→ contract version declaration

Consumer capabilities
→ ConsumerProfile

Adapter mapping
→ delivery configuration
```

---

## 21.115 Configuration Governance

Los valores configurables deberán salir del código cuando exista necesidad.

---

## 21.116 Hardcoded Constants

Constantes contractuales estables sí pueden permanecer en código.

Ejemplo:

```text
DELIVERY_CONTRACT_VERSION = "1.0"
```

---

## 21.117 Runtime Configuration

Elementos como:

```text
endpoints
timeouts
enabled adapters
```

deberán ser configurables cuando se implementen.

---

## 21.118 No config explosion

No todo comportamiento necesita una variable de configuración.

La configuración excesiva aumenta combinaciones no probadas.

---

## 21.119 Safe Defaults

Toda configuración deberá tener defaults seguros cuando sean posibles.

---

## 21.120 Configuration Validation

La configuración deberá validarse durante bootstrap.

---

## 21.121 Environment Drift

Configuraciones distintas entre:

```text
development
testing
production
```

deberán mantenerse explícitas.

---

## 21.122 No architecture by environment

La arquitectura no deberá cambiar fundamentalmente según entorno.

Solo configuraciones operativas.

---

## 21.123 Test Governance

Toda nueva funcionalidad deberá añadir pruebas antes de considerarse completa.

---

## 21.124 Bug Regression Rule

Todo bug corregido deberá generar, cuando sea razonable, una prueba que hubiera detectado el problema.

---

## 21.125 Regression Test

La secuencia será:

```text
bug reproduced
      ↓
test added
      ↓
test fails
      ↓
fix
      ↓
test passes
```

---

## 21.126 No bug-only patch

Evitar:

```text
fix code
without preserving regression evidence
```

---

## 21.127 Global Regression Governance

Todo cambio significativo deberá continuar ejecutando:

```text
pytest -q
```

---

## 21.128 Test Speed

Mientras la suite siga rápida deberá mantenerse amplia ejecución frecuente.

---

## 21.129 Slow Test Separation

Si en el futuro aparecen tests de red lentos podrán clasificarse.

No deberá reducirse la suite principal innecesariamente.

---

## 21.130 CI Evolution

La futura CI podrá dividir:

```text
unit
contract
integration
security
```

pero el resultado final deberá seguir siendo un gate coherente.

---

## 21.131 Quality Gate

No deberá permitirse merge de cambios críticos con tests fallidos.

---

## 21.132 Emergency Patch

Un hotfix crítico podrá requerir un proceso acelerado.

Pero deberá seguir:

```text
test
trace
document
```

aunque con menor ceremonia.

---

## 21.133 Emergency Architecture Change

Si por seguridad debe romperse compatibilidad inmediatamente, deberá documentarse posteriormente de manera prioritaria.

---

## 21.134 Security Over Ceremony

En una emergencia:

```text
security fix first
```

pero no:

```text
forget governance forever
```

---

## 21.135 Rollback

Los cambios importantes deberán ser reversibles cuando sea posible.

---

## 21.136 Rollback Plan

Para un cambio de contrato MAJOR deberá definirse:

```text
how to restore previous supported version
```

durante migración.

---

## 21.137 Adapter Rollback

La sustitución de adapter debería permitir volver al anterior si falla.

---

## 21.138 Consumer Rollback

Un ConsumerProfile nuevo podrá mantener temporalmente el anterior durante transición.

---

## 21.139 No data corruption rollback

Rollback de Delivery no deberá implicar modificar respuestas históricas.

---

## 21.140 Governance of historical records

Los DeliveryResult históricos permanecerán inmutables.

---

## 21.141 Future Runtime Intelligence

Si HEYTI adquiere capacidades más complejas de orquestación cognitiva, Delivery deberá permanecer aguas abajo.

---

## 21.142 Cognitive Orchestrator Future

Un futuro Cognitive Orchestrator podrá decidir:

```text
which capability
which sequence
which evidence
```

pero no deberá asumir responsabilidades de Delivery.

---

## 21.143 Emerging Evidence Future

Un futuro ESE podrá enriquecer respuestas antes de Materialization.

Delivery seguirá recibiendo la respuesta ya materializada.

---

## 21.144 Confidence Engine Future

Un Confidence Engine podrá producir:

```text
confidence
```

que Delivery preservará.

No recalculará.

---

## 21.145 HEO Future

Una futura ontología de evidencias podrá cambiar la estructura de Evidence.

Esto deberá tratarse como evolución del Response Contract.

Delivery únicamente deberá adaptarse si su contrato cambia.

---

## 21.146 Future capabilities

Nuevas capabilities deberán poder utilizar HRRD sin implementar lógica de transporte propia.

---

## 21.147 Capability Integration Rule

Toda capability nueva deberá seguir:

```text
Capability
      ↓
Materialization
      ↓
HRRD
```

No:

```text
Capability
      ↓
direct HTTP response
```

---

## 21.148 Legacy Capability Migration

Si existen capabilities que devuelven estructuras ad hoc, deberán migrarse gradualmente.

---

## 21.149 No dual delivery path indefinitely

No deberá mantenerse permanentemente:

```text
new HRRD path
+
legacy direct response path
```

sin plan de convergencia.

---

## 21.150 Transitional Compatibility

Un periodo temporal sí puede existir durante migración.

---

## 21.151 Sunset Trigger

El camino legacy deberá retirarse cuando:

```text
all relevant capabilities migrated
tests pass
consumers compatible
```

---

## 21.152 Gateway Evolution

El Gateway podrá evolucionar a API formal.

---

## 21.153 Gateway Governance

Sus endpoints deberán utilizar contratos consistentes.

No deberán transformarse en APIs distintas por capability sin revisión.

---

## 21.154 Unified Query Future

Una futura entrada:

```text
Pregúntale a HEYTI
```

podrá utilizar un Gateway único.

---

## 21.155 Delivery remains generic

HRRD deberá permanecer suficientemente genérico para entregar respuestas de múltiples capabilities.

---

## 21.156 Portal Evolution

El Portal existente podrá convertirse gradualmente en consumidor HEYTI.

---

## 21.157 No big-bang migration

La transición deberá ser incremental.

---

## 21.158 First slice governance

La primera integración visual deberá utilizar:

```text
DescribeSection
```

como referencia de arquitectura.

---

## 21.159 Subsequent slices

Después podrán integrarse capabilities de:

```text
Territorial
Socioeconomic
Field
Election Day
ET-27
Ganar Todo
```

---

## 21.160 Reuse before special case

Cada nueva integración deberá intentar reutilizar:

```text
existing Content Types
existing Consumer Model
existing Delivery Pipeline
```

antes de introducir excepciones.

---

## 21.161 Special Case Review

Si una capability requiere un tratamiento especial deberá justificarse.

---

## 21.162 Example legitimate special case

Streaming de Día D en tiempo real podría requerir un contrato distinto.

---

## 21.163 Example illegitimate special case

```text
DescribeSection uses blue cards
```

no justifica cambiar Delivery.

---

## 21.164 UI Data Coverage Governance

Antes de cada módulo visual deberá actualizarse la cobertura de fuentes.

---

## 21.165 Module readiness gate

Un módulo estará listo para integración HEYTI cuando:

```text
data source verified
capability available
materialization available
delivery content types supported
consumer renderer available
tests green
```

---

## 21.166 Module readiness statuses

Podrán utilizarse:

```text
NOT_READY
DATA_READY
CAPABILITY_READY
DELIVERY_READY
PRESENTATION_READY
END_TO_END_READY
```

si resulta útil.

---

## 21.167 Avoid fake readiness

Un módulo no deberá marcarse:

```text
END_TO_END_READY
```

porque solo existe HTML.

---

## 21.168 Operational Governance

Cuando HEYTI entre en uso real deberán revisarse periódicamente:

```text
failure rate
rejection rate
deprecated contract usage
adapter health
consumer compatibility
```

---

## 21.169 Review cadence

La cadencia deberá ajustarse al nivel de uso.

No necesita fijarse todavía.

---

## 21.170 Incident Review

Incidentes importantes deberán producir análisis posterior.

---

## 21.171 Postmortem

Un postmortem técnico podrá documentar:

```text
what happened
impact
root cause
detection
resolution
preventive action
```

---

## 21.172 Blameless technical review

El objetivo deberá ser mejorar sistema y proceso.

No atribuir culpas personales.

---

## 21.173 Architecture feedback loop

Los incidentes podrán revelar cambios necesarios en arquitectura.

---

## 21.174 No patch-only culture

Cada incidente repetitivo deberá llevar a revisar la causa estructural.

---

## 21.175 Delivery Health Review

Podrá revisarse:

```text
contract drift
error distribution
payload growth
consumer failures
adapter failures
```

---

## 21.176 Payload Growth Alert

Si los payloads crecen significativamente deberá revisarse:

```text
duplicate data
geometry
evidence
metadata
```

---

## 21.177 Contract Bloat

Un contrato demasiado grande puede indicar mezcla de responsabilidades.

---

## 21.178 Consumer-specific fields warning

Si aparecen muchos campos utilizados solo por un consumer deberá revisarse si pertenecen a Presentation.

---

## 21.179 Adapter-specific fields warning

Si aparecen campos centrales usados solo por un adapter puede existir fuga de transporte.

---

## 21.180 Architecture Smells Future Audit

Deberán vigilarse:

```text
consumer-specific branches
adapter-specific semantic branches
UI fields in contracts
raw exception leakage
global session state
silent fallbacks
multiple contract sources
```

---

## 21.181 Governance Checklist for Every Significant Change

```text
[ ] Responsibility belongs to Delivery?
[ ] Contract impact reviewed?
[ ] Consumer impact reviewed?
[ ] Adapter impact reviewed?
[ ] Security impact reviewed?
[ ] Traceability preserved?
[ ] Version impact reviewed?
[ ] Tests added/updated?
[ ] Documentation updated?
[ ] Global suite green?
```

---

## 21.182 Release Checklist

Antes de una nueva release de HRRD:

```text
[ ] Contract version known
[ ] Supported consumers known
[ ] Supported adapters known
[ ] Deprecated items known
[ ] Tests green
[ ] Security review complete
[ ] Migration notes complete if needed
```

---

## 21.183 Deferred Item Review

Los elementos diferidos deberán revisarse periódicamente.

---

## 21.184 Remove obsolete deferred items

Si una necesidad desaparece, deberá eliminarse del backlog.

No debe mantenerse como obligación eterna.

---

## 21.185 Promote deferred item

Un elemento deberá pasar a implementación cuando su trigger se cumpla.

---

## 21.186 Example

```text
Deferred:
WebSocket Adapter

Trigger:
UI requires real-time Día D updates.

Trigger becomes true:
Create new architecture/implementation sprint.
```

---

## 21.187 New Sprint Rule

Una expansión significativa deberá tener su propio Sprint.

No deberá añadirse informalmente al Sprint 23 cerrado.

---

## 21.188 Sprint Boundary Integrity

Sprint 23 deberá permanecer como baseline de:

```text
Runtime Response Delivery foundation
```

---

## 21.189 Future Sprint candidates

Posibles futuros frentes:

```text
HEYTI Gateway Integration
HEYTI Presentation Integration
HEYTI Streaming Delivery
HEYTI Delivery Hardening
HEYTI Delivery Security
```

Los nombres concretos se definirán cuando corresponda.

---

## 21.190 Do not pre-commit roadmap

Estos nombres son conceptuales.

No constituyen una obligación de secuencia.

---

## 21.191 Evolution Principle

La evolución deberá obedecer:

```text
Need
      ↓
Architecture
      ↓
Contract
      ↓
Implementation
      ↓
Verification
      ↓
Release
```

---

## 21.192 Anti-pattern de evolución

Queda prohibido:

```text
Need
      ↓
Patch
      ↓
Production
      ↓
Architecture later
```

salvo emergencia crítica.

---

## 21.193 Minimum Change Principle

Ante una necesidad nueva deberá aplicarse el menor cambio arquitectónicamente correcto.

---

## 21.194 No broader change than required

Ejemplo:

Si solo se necesita un nuevo adapter:

```text
add adapter
```

No:

```text
rewrite Delivery Contract
```

sin razón.

---

## 21.195 Extension Points

Los principales puntos de extensión deberán ser:

```text
ConsumerProfile
DeliveryAdapter
Serializer support
Contract version
Security policy
Observability integration
```

---

## 21.196 Stable Core

El corazón de Delivery deberá cambiar poco.

Conceptualmente:

```text
validate
serialize
resolve
deliver
trace
result
```

deberá mantenerse estable.

---

## 21.197 Open/Closed Principle

HRRD deberá tender a:

> abierto para extensión, cerrado para modificación innecesaria.

Ejemplo:

```text
new adapter
```

debe poder agregarse sin reescribir el pipeline.

---

## 21.198 Consumer Extension

Un nuevo consumer deberá registrarse sin modificar capabilities.

---

## 21.199 Content Extension

Un nuevo Content Type sí requerirá revisión contractual porque amplía semántica pública.

---

## 21.200 Error Extension

Un nuevo error público deberá ser excepcional.

Los subcódigos internos pueden ofrecer granularidad.

---

## 21.201 Compatibility as Governance

La compatibilidad no deberá dejarse a "esperemos que funcione".

Debe ser comprobable.

---

## 21.202 Compatibility Evidence

Podrá incluir:

```text
consumer fixtures
contract tests
schema validation
integration tests
```

---

## 21.203 Deprecation Evidence

Antes de retirar una versión deberá demostrarse que los consumers activos ya no dependen de ella.

---

## 21.204 Version Usage Metric

Una métrica futura podrá apoyar esa decisión.

---

## 21.205 Governance and Git

Git deberá actuar como registro histórico de evolución.

---

## 21.206 Commit Quality

Los commits significativos deberán describir qué cambio arquitectónico o funcional incorporan.

---

## 21.207 No noisy history

Deberá evitarse incluir artefactos temporales innecesarios.

---

## 21.208 Tags or releases future

Una baseline importante podrá marcarse mediante tag si el flujo del repositorio lo adopta.

---

## 21.209 No tag without certification

Un tag de release deberá corresponder a un estado probado.

---

## 21.210 Reproducibility

Deberá ser posible volver a una baseline y ejecutar su suite.

---

## 21.211 Dependency Pinning

Las dependencias deberán versionarse conforme a la política del proyecto.

---

## 21.212 Reproducible environment

El proyecto deberá evitar depender de configuración manual no documentada para ejecutar tests.

---

## 21.213 Documentation Onboarding

El futuro Mapa Maestro de Consulta y Trazabilidad Documental deberá incluir este documento dentro de la secuencia de lectura adecuada.

---

## 21.214 HRRD place in documentation

Conceptualmente deberá aparecer después de documentos de:

```text
Runtime
Materialization
```

y antes de:

```text
Gateway / Presentation integration
```

---

## 21.215 Onboarding Question

Un desarrollador nuevo deberá poder comprender:

```text
where Response Delivery starts
where it ends
what it can depend on
what cannot depend on it
```

---

## 21.216 Architecture enforcement

Las reglas deberán ser suficientemente claras para que un programador nuevo no tenga que inferirlas del código.

---

## 21.217 Reviewability

Una Pull Request futura de HRRD deberá poder revisarse contra:

```text
contracts
invariants
dependency rules
tests
```

---

## 21.218 PR Review Questions

```text
Does this preserve semantic neutrality?
Does this change the contract?
Does this create consumer coupling?
Does this create transport coupling?
Does this preserve trace?
Does this preserve security?
```

---

## 21.219 Red Flags in PR

Ejemplos:

```text
import fastapi inside delivery core
import browser-specific code
default=str serializer
except Exception: pass
global session variable
hardcoded Portal special case
```

---

## 21.220 Governance and refactoring

Refactoring será bienvenido cuando:

```text
behavior preserved
contracts preserved
tests preserved
```

---

## 21.221 Refactor without version bump

No requiere nueva versión contractual si no cambia comportamiento público.

---

## 21.222 Refactor verification

La suite deberá demostrar equivalencia.

---

## 21.223 Breaking refactor

Si un "refactor" cambia semántica pública, no es solo refactor.

Deberá tratarse como evolución contractual.

---

## 21.224 Technical Simplification

La arquitectura podrá simplificarse en el futuro si se descubre que una abstracción no aporta valor.

---

## 21.225 Removal of unnecessary abstraction

Eliminar una abstracción interna no requiere cambio contractual si no altera comportamiento público.

---

## 21.226 No sacred code

La implementación puede cambiar.

Los principios y contratos son la guía.

---

## 21.227 No sacred document

Incluso la arquitectura puede evolucionar si existe una razón mejor.

Pero deberá hacerlo explícitamente.

---

## 21.228 Architecture Amendment

Una modificación de principio deberá documentarse.

---

## 21.229 Governance hierarchy

Se propone la siguiente jerarquía:

```text
Security / correctness
        ↓
Architecture
        ↓
Contracts
        ↓
Compatibility
        ↓
Implementation convenience
```

La comodidad de implementación no deberá vencer una regla superior.

---

## 21.230 Performance exception

El rendimiento podrá justificar cambios arquitectónicos solo con evidencia.

---

## 21.231 UX exception

Una necesidad fuerte de UX puede justificar nuevos Content Types o streaming.

Pero deberá resolverse manteniendo fronteras claras.

---

## 21.232 Operational exception

Una necesidad de confiabilidad puede justificar retry, circuit breaker o queue.

No deberá introducirse sin semántica formal.

---

## 21.233 Governance of failure semantics

El significado de:

```text
DELIVERED
REJECTED
FAILED
```

deberá preservarse rigurosamente.

---

## 21.234 No status inflation

No deberán agregarse estados nuevos sin necesidad.

---

## 21.235 New status review

Agregar:

```text
PARTIAL
UNKNOWN
CANCELLED
```

deberá evaluar impacto en todos los consumers.

---

## 21.236 Cancelled future

Si existe cancelación futura deberá definirse:

```text
who cancels
when
what if payload already sent
how trace records it
```

---

## 21.237 Unknown future

Si sistemas distribuidos requieren un estado de certeza insuficiente, deberá distinguirse cuidadosamente de FAILED.

---

## 21.238 No semantic shortcut

No deberá utilizarse:

```text
FAILED
```

para cualquier situación solo por conveniencia.

---

## 21.239 Governance of Delivery ID

`delivery_id` deberá permanecer una identidad por operación.

No deberá reutilizarse para retries.

---

## 21.240 Governance of Response ID

`response_id` deberá permanecer identidad de la respuesta materializada.

---

## 21.241 Identity semantics immutable

Cambiar estas reglas sería un cambio arquitectónico MAJOR.

---

## 21.242 Governance of Trace

La cadena:

```text
request_id
execution_id
response_id
delivery_id
```

deberá preservarse conforme otras capas maduren.

---

## 21.243 No collapsing IDs

No deberá simplificarse a:

```text
one universal id
```

si ello elimina significado.

---

## 21.244 Correlation ID remains grouping

`correlation_id` no deberá sustituir identidades específicas.

---

## 21.245 Governance of public trace

La cantidad de trace expuesta al consumer podrá cambiar según seguridad.

La traza interna deberá permanecer suficiente.

---

## 21.246 Public trace minimization

Solo deberán exponerse IDs útiles y seguros.

---

## 21.247 Governance of warnings

Warnings cognitivos deberán preservarse.

---

## 21.248 Delivery warnings

Warnings propios de Delivery deberán mantenerse diferenciados cuando existan.

---

## 21.249 No warning swallowing

Ningún adapter deberá eliminar warnings.

---

## 21.250 Governance of null

El significado de null deberá permanecer contractual.

---

## 21.251 No UI-driven null conversion

La UI puede mostrar texto alternativo.

El Core no deberá cambiar semántica por Presentation.

---

## 21.252 Governance of units

Las unidades deberán permanecer explícitas.

---

## 21.253 Unit vocabulary evolution

Agregar unidades nuevas puede ser compatible.

Cambiar significado de una existente no.

---

## 21.254 Governance of territorial references

Los identificadores territoriales deberán permanecer estables conforme a los modelos de datos vigentes.

---

## 21.255 Historical territorial evolution

Si una sección cambia históricamente, HEYTI deberá manejarlo en conocimiento/datos.

Delivery solo preservará la referencia materializada.

---

## 21.256 No Delivery territorial logic

HRRD no resolverá secciones históricas.

---

## 21.257 Governance of actions

Las acciones deberán permanecer declarativas y allowlisted.

---

## 21.258 New action review

Toda nueva acción deberá especificar:

```text
semantic meaning
required context
consumer support
security implications
```

---

## 21.259 No direct URL action by default

Debe preferirse:

```text
OPEN_MODULE / TERRITORIAL
```

a:

```text
navigate to arbitrary URL
```

---

## 21.260 Governance of evidence

Evidence seguirá siendo responsabilidad cognitiva/Materialization.

Delivery no alterará su peso o interpretación.

---

## 21.261 Evidence projection

Cualquier reducción por seguridad deberá ser explícita.

---

## 21.262 Governance of data freshness

Campos como:

```text
data_as_of
knowledge_version
```

deberán preservarse cuando formen parte del contrato.

---

## 21.263 No freshness inference in Delivery

Delivery no deberá decidir que un dato "ya está viejo".

Esa evaluación pertenece a conocimiento o política externa.

---

## 21.264 Architectural Health Check

Periódicamente podrá ejecutarse una auditoría de HRRD.

---

## 21.265 Health Check Questions

```text
Are contracts still explicit?
Are consumers still replaceable?
Are adapters still replaceable?
Is Presentation still outside Core?
Is Gateway still outside Core?
Is response_id preserved?
Is delivery_id unique?
Are errors structured?
Are tests green?
Are deferred items still intentional?
```

---

## 21.266 Architecture Debt

Si alguna respuesta se vuelve:

```text
NO
```

deberá registrarse como deuda arquitectónica o defecto según gravedad.

---

## 21.267 Debt Severity

Podrán utilizarse:

```text
LOW
MEDIUM
HIGH
CRITICAL
```

según impacto.

---

## 21.268 Critical Architecture Debt

Ejemplos:

```text
security bypass
trace loss
contract corruption
silent response mutation
```

deberán corregirse prioritariamente.

---

## 21.269 Low Debt

Ejemplo:

```text
consumer registry currently static
```

si cumple necesidades actuales.

---

## 21.270 Governance and deadlines

La presión de fechas no deberá ocultar deuda crítica.

---

## 21.271 Scope versus quality

Puede reducirse:

```text
scope
```

para proteger:

```text
correctness
```

No al contrario.

---

## 21.272 Future expansion discipline

Cada expansión deberá mantener la regla:

```text
smallest complete architectural increment
```

---

## 21.273 Vertical Slice Preference

Deberá preferirse completar una vertical real antes de construir múltiples piezas incompletas.

---

## 21.274 Example

Mejor:

```text
DescribeSection
fully delivered to first consumer
```

que:

```text
six adapters partially implemented
```

sin integración real.

---

## 21.275 Consumer Feedback

La integración real podrá revelar necesidades no previstas.

Estas deberán alimentar arquitectura futura.

---

## 21.276 No blind architecture

La arquitectura deberá aprender de operación real.

---

## 21.277 But no ad-hoc adaptation

Aprender no significa parchear sin gobernanza.

---

## 21.278 Governance cycle

La evolución deberá seguir:

```text
Observe
   ↓
Identify Need
   ↓
Analyze
   ↓
Decide
   ↓
Implement
   ↓
Verify
   ↓
Observe Again
```

---

## 21.279 Relationship with Observability

El Capítulo 17 proporciona la evidencia necesaria para este ciclo.

---

## 21.280 Relationship with Certification

El Capítulo 19 proporciona la disciplina de verificación.

---

## 21.281 Relationship with Implementation Plan

El Capítulo 20 proporciona la secuencia segura de construcción.

---

## 21.282 Governance closes the loop

Este capítulo garantiza que esas reglas sobrevivan después del Sprint.

---

# 21.283 Elementos diferidos consolidados de HRRD v1.0

Se establece el siguiente inventario conceptual inicial:

| Elemento | Estado | Trigger futuro |
|---|---|---|
| HTTP production adapter | Deferred | Gateway real |
| Gateway external API | Deferred | Consumer externo |
| WebSocket adapter | Deferred | Push/real-time UI |
| Streaming contract | Deferred | Respuesta progresiva |
| Automatic retry | Deferred | Idempotency + necesidad operacional |
| Circuit breaker | Deferred | Target externo inestable |
| Queue adapter | Deferred | Delivery asíncrono |
| Multi-version negotiation | Deferred | Coexistencia de versiones |
| Contract downgrade adapter | Deferred | Migración real |
| Persistent audit store | Deferred | Requisito operacional/auditoría |
| Distributed tracing | Deferred | Arquitectura distribuida |
| Payload hashing | Deferred | Integridad/auditoría |
| Digital signatures | Deferred | Integraciones de alta confianza |
| Advanced RBAC/ABAC | Deferred | Seguridad granular |
| Dynamic Consumer Discovery | Deferred | Consumers distribuidos |
| Presentation Contract | Deferred | UI compleja que lo justifique |
| UI telemetry acknowledgement | Deferred | Observabilidad end-to-end |

---

## 21.284 Regla sobre el inventario

Este inventario deberá revisarse al cierre de Sprint 23.

Los elementos podrán:

```text
remain deferred
be removed
be promoted to next sprint
```

según evidencia real.

---

# 21.285 Invariantes de gobernanza

Se establecen los siguientes invariantes.

### HRRD-GOV01 — Architecture Before Expansion

Toda expansión significativa deberá revisar primero la arquitectura.

### HRRD-GOV02 — Explicit Technical Debt

Toda deuda técnica aceptada deberá estar documentada.

### HRRD-GOV03 — Deferred Is Not Omitted

Todo elemento diferido deberá estar identificado explícitamente.

### HRRD-GOV04 — No Silent Contract Drift

Ningún cambio público podrá introducirse sin revisión contractual.

### HRRD-GOV05 — Consumer Pressure Does Not Define Core

Las necesidades visuales no deberán contaminar el contrato central.

### HRRD-GOV06 — Adapter Extensions Preserve Semantics

Un nuevo transporte no deberá modificar significado.

### HRRD-GOV07 — Tests Guard Architecture

Las pruebas de conformidad deberán preservarse como guardrails.

### HRRD-GOV08 — Historical Baselines Remain Immutable

La historia del sistema no deberá reescribirse.

### HRRD-GOV09 — Security Overrides Convenience

La seguridad tendrá prioridad sobre compatibilidad o facilidad de implementación cuando exista conflicto real.

### HRRD-GOV10 — Scope May Shrink, Correctness May Not

La presión de entrega podrá reducir alcance, pero no justificar corrupción contractual.

---

## 21.286 Checklist de evolución futura

Ante una nueva solicitud deberá revisarse:

```text
[ ] ¿Pertenece realmente a Delivery?
[ ] ¿Existe ya una extensión adecuada?
[ ] ¿Cambia el contrato?
[ ] ¿Cambia la versión?
[ ] ¿Afecta consumers?
[ ] ¿Afecta adapters?
[ ] ¿Afecta seguridad?
[ ] ¿Afecta trazabilidad?
[ ] ¿Afecta Presentation?
[ ] ¿Requiere ADR?
[ ] ¿Requiere migración?
[ ] ¿Requiere nuevos tests?
```

---

## 21.287 Criterio de éxito de gobernanza

La gobernanza será considerada adecuada cuando HEYTI pueda evolucionar Runtime Response Delivery sin convertir cada nueva necesidad en una excepción dentro del Core.

---

## 21.288 Prueba arquitectónica de evolución

Ante una nueva necesidad como:

```text
nuevo consumer
```

la respuesta ideal deberá ser:

```text
add ConsumerProfile
add authorized adapter mapping
add tests
```

no:

```text
rewrite Delivery pipeline
```

---

## 21.289 Prueba arquitectónica de transporte

Ante:

```text
WebSocket required
```

la respuesta ideal será:

```text
add adapter / specialized contract if justified
```

no:

```text
change capabilities
```

---

## 21.290 Prueba arquitectónica visual

Ante:

```text
new chart type
```

la respuesta ideal será:

```text
change Presentation
```

no:

```text
change Delivery
```

si los datos ya están disponibles.

---

## 21.291 Prueba arquitectónica de datos

Ante:

```text
new indicator
```

la primera pregunta deberá ser:

```text
does the data exist and is it valid?
```

antes de:

```text
how do we draw it?
```

---

## 21.292 Prueba de deuda

Ante un shortcut deberá preguntarse:

```text
Is this consciously bounded debt?
or
Is this an architectural defect?
```

---

## 21.293 Prueba de deprecación

Antes de retirar un elemento deberá demostrarse:

```text
no active dependent consumer
or
migration completed
```

---

## 21.294 Prueba de baseline

Cada release importante deberá poder vincularse a:

```text
document
commit
tests
contract version
```

---

# 21.295 Modelo consolidado de evolución

```text
                  ┌─────────────────────┐
                  │ HRRD Certified Core │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Observe Real Usage  │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ New Requirement     │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Architecture Review │
                  └──────────┬──────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
                    ▼                 ▼
             Existing Extension   Contract Change
                    │                 │
                    ▼                 ▼
              Implement/Test      Version/Migrate
                    │                 │
                    └────────┬────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ Certification       │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ New Baseline        │
                  └─────────────────────┘
```

---

## 21.296 Modelo de deuda controlada

```text
Constraint Identified
      ↓
Explicit Debt Decision
      ↓
Risk Documented
      ↓
Bounded Temporary Solution
      ↓
Trigger Reached
      ↓
Remediation
      ↓
Debt Closed
```

---

## 21.297 Modelo de elemento diferido

```text
Future Possibility
      ↓
Architecturally Recognized
      ↓
Not Needed Yet
      ↓
DEFERRED BY DESIGN
      ↓
Trigger?
   ┌──┴───┐
   │      │
  NO     YES
   │      │
Remain   New Sprint
Deferred
```

---

## 21.298 Criterio de éxito del capítulo

Este capítulo será considerado satisfecho cuando la evolución futura de HRRD pueda clasificarse claramente como una de las siguientes:

```text
compatible extension
internal refactor
new adapter
new consumer
new contract version
deferred capability activation
technical debt remediation
architectural change
```

y cada categoría posea una forma coherente de gobernarse.

---

## 21.299 Declaración arquitectónica del capítulo

Runtime Response Delivery no deberá ser únicamente una pieza de código funcional.

Deberá convertirse en una frontera estable del sistema HEYTI.

Su valor arquitectónico dependerá de que pueda crecer sin perder:

- claridad;
- trazabilidad;
- neutralidad;
- seguridad;
- compatibilidad;
- testabilidad.

La regla arquitectónica consolidada queda establecida como:

> **HEYTI Runtime Response Delivery deberá evolucionar únicamente mediante extensiones, migraciones y decisiones explícitas que preserven sus invariantes o documenten formalmente cualquier cambio de arquitectura. La deuda técnica deberá ser consciente y acotada; los elementos diferidos deberán permanecer identificados; y ninguna necesidad futura deberá justificar erosión silenciosa del contrato o de las fronteras del Core.**

La disciplina de evolución queda formalizada como:

```text
OBSERVE
   ↓
JUSTIFY
   ↓
DESIGN
   ↓
VERSION IF REQUIRED
   ↓
IMPLEMENT
   ↓
VERIFY
   ↓
CERTIFY
   ↓
ESTABLISH NEW BASELINE
```

y permanece vigente la regla de trabajo:

```text
0 ERRORES
0 OMISIONES
```

Con la gobernanza de evolución establecida queda preparado el siguiente capítulo:

**criterios de cierre arquitectónico, baseline oficial y declaración de preparación de HEYTI Runtime Response Delivery v1.0 para materialización técnica.**

---

**Fin del Capítulo 21**


# Capítulo 22. Cierre arquitectónico, baseline oficial y declaración de preparación de HEYTI Runtime Response Delivery v1.0

## 22.1 Propósito del capítulo

Este capítulo formaliza el **cierre arquitectónico** de **HEYTI Runtime Response Delivery v1.0 (HRRD)** y establece la baseline que deberá gobernar su posterior materialización técnica dentro de Sprint 23.

Los capítulos anteriores han definido progresivamente:

```text
propósito
alcance
fronteras
principios
contratos
pipeline
contexto
trazabilidad
consumers
adapters
serialización
errores
seguridad
versionado
observabilidad
Presentation
pruebas
implementación incremental
gobernanza
evolución futura
```

Por tanto, este capítulo no deberá introducir un nuevo subsistema.

Su función será responder formalmente:

> **¿La arquitectura de Runtime Response Delivery está suficientemente definida para abandonar la fase exclusivamente documental y comenzar su materialización técnica de manera controlada?**

La respuesta deberá basarse en criterios verificables.

No en entusiasmo.

No en intención.

No en percepción de avance.

---

# 22.2 Naturaleza del cierre

Cerrar arquitectura no significa:

```text
architecture will never change
```

Significa:

```text
architecture is sufficiently defined
to begin implementation safely
```

---

## 22.3 Architecture Freeze

A partir del cierre de este documento deberá existir un:

```text
Architecture Freeze
```

para el alcance v1.0.

Esto significa que durante la implementación no deberán modificarse silenciosamente:

```text
responsibilities
boundaries
contract semantics
identity semantics
terminal states
consumer model
adapter model
trace model
```

---

## 22.4 Freeze no significa inmovilidad

Si la implementación revela una contradicción real, podrá modificarse la arquitectura.

Pero deberá seguir:

```text
Detect
   ↓
Stop
   ↓
Analyze
   ↓
Decide
   ↓
Document
   ↓
Implement
```

No:

```text
Detect
   ↓
Patch
   ↓
Continue
```

---

# 22.5 Declaración de alcance consolidado

HRRD v1.0 deberá encargarse de:

```text
receiving a materialized response
establishing delivery context
creating delivery identity
validating delivery readiness
resolving consumer compatibility
serializing canonical payload
resolving delivery mechanism
executing delivery
normalizing delivery result
preserving traceability
exposing operational outcome
```

---

## 22.6 Responsabilidades excluidas

HRRD v1.0 no deberá encargarse de:

```text
knowledge reasoning
capability selection
capability execution
evidence interpretation
response cognition
response materialization
HTML rendering
CSS styling
map rendering
chart rendering
HTTP business semantics
UI navigation implementation
database migration
territorial analysis
electoral calculation
```

---

## 22.7 Frontera de entrada

La entrada conceptual será:

```text
Materialized Response
```

producida por la capa de Materialization.

---

## 22.8 Frontera de salida

La salida conceptual será:

```text
DeliveryResult
```

acompañada por la ejecución correspondiente del adapter.

---

## 22.9 Frontera completa

```text
Knowledge / Capability
        ↓
Materialization
        ↓
===========================
 HRRD INPUT BOUNDARY
===========================
        ↓
Validation
        ↓
Serialization
        ↓
Consumer Resolution
        ↓
Adapter Resolution
        ↓
Delivery Execution
        ↓
Trace Completion
        ↓
DeliveryResult
===========================
 HRRD OUTPUT BOUNDARY
===========================
        ↓
Gateway / Consumer / Future Transport
```

---

# 22.10 Principios arquitectónicos consolidados

La baseline v1.0 deberá preservar los siguientes principios.

---

## 22.11 P1 — Semantic Neutrality

Delivery transporta significado.

No lo redefine.

```text
Response meaning before Delivery
==
Response meaning after Delivery
```

---

## 22.12 P2 — Materialization Independence

Delivery no reconstruye una respuesta ya materializada.

---

## 22.13 P3 — Presentation Independence

Delivery no conoce:

```text
HTML
CSS
DOM
Leaflet
Chart.js
```

---

## 22.14 P4 — Transport Independence

El Core de Delivery no deberá depender de:

```text
HTTP
WebSocket
message queue
```

como mecanismo obligatorio.

---

## 22.15 P5 — Explicit Consumer

Toda operación de entrega deberá poseer un consumidor identificable.

---

## 22.16 P6 — Explicit Adapter

Toda operación deberá utilizar un mecanismo de entrega explícito y sustituible.

---

## 22.17 P7 — Explicit Identity

Toda operación deberá poseer:

```text
delivery_id
```

independiente de:

```text
response_id
```

---

## 22.18 P8 — Explicit Terminal State

Toda operación deberá finalizar en un estado semántico definido.

Baseline:

```text
DELIVERED
REJECTED
FAILED
```

---

## 22.19 P9 — Explicit Errors

Los errores deberán ser estructuras contractuales.

No mensajes arbitrarios.

---

## 22.20 P10 — Explicit Version

Toda frontera pública deberá identificar su versión contractual cuando corresponda.

---

## 22.21 P11 — Explicit Traceability

Deberá ser posible reconstruir:

```text
request
→ execution
→ response
→ delivery
```

según la información disponible.

---

## 22.22 P12 — Fail Explicitly

La pérdida silenciosa de información no deberá utilizarse como estrategia de tolerancia.

---

## 22.23 P13 — Security Before Delivery

Las precondiciones de seguridad aplicables deberán resolverse antes de cruzar la frontera externa.

---

## 22.24 P14 — Observable Outcome

Toda operación deberá dejar suficiente evidencia para conocer:

```text
what happened
where
to whom
through which adapter
with what terminal result
```

---

## 22.25 P15 — Incremental Evolution

Nuevos transports, consumers y mecanismos deberán incorporarse mediante extensión controlada.

---

# 22.26 Contratos conceptuales consolidados

La implementación deberá revisar y materializar, según la estructura real del repositorio:

```text
DeliveryStatus
DeliveryStage
DeliveryContext
DeliveryTrace
DeliveryEnvelope
DeliveryResult
DeliveryError
ConsumerProfile
AdapterResult
DeliveryAdapter
```

No todos deberán necesariamente convertirse en clases independientes.

La implementación deberá preservar las responsabilidades, no una cantidad artificial de archivos.

---

## 22.27 Regla contra la literalidad documental

El documento define arquitectura.

No exige convertir cada concepto en:

```text
one Python class
```

si una representación más simple preserva correctamente el contrato.

---

## 22.28 Regla contra la simplificación destructiva

La regla anterior tampoco deberá utilizarse para colapsar toda la arquitectura en:

```python
def deliver(data):
    ...
```

perdiendo fronteras importantes.

---

# 22.29 Modelo consolidado de identidad

La baseline establece:

```text
request_id
execution_id
response_id
delivery_id
```

como identidades conceptualmente distintas.

---

## 22.30 Request Identity

Identifica la solicitud cuando exista dicha identidad en el Runtime.

---

## 22.31 Execution Identity

Identifica la ejecución correspondiente cuando Runtime la provea.

---

## 22.32 Response Identity

Identifica la respuesta materializada.

---

## 22.33 Delivery Identity

Identifica una operación concreta de entrega.

---

## 22.34 Regla crítica de identidad

Una misma respuesta podrá conceptualmente producir:

```text
RESP-001
   ├── DEL-001
   └── DEL-002
```

si se entrega más de una vez.

---

## 22.35 Prohibición de colapso

No deberá asumirse:

```text
response_id == delivery_id
```

---

# 22.36 Modelo consolidado de estado

La baseline inicial será:

```text
DELIVERED
REJECTED
FAILED
```

---

## 22.37 DELIVERED

Significa que la operación de Delivery alcanzó exitosamente el resultado definido por el adapter.

No significa necesariamente:

```text
user saw it
```

---

## 22.38 REJECTED

Significa que la operación no debía ejecutarse porque una precondición no fue satisfecha.

Ejemplos:

```text
invalid contract
unknown consumer
incompatible consumer
unauthorized consumer
```

---

## 22.39 FAILED

Significa que la operación era válida para intentarse pero falló operacionalmente.

Ejemplos:

```text
serialization failure
adapter failure
target failure
```

según la taxonomía final implementada.

---

## 22.40 Estado terminal único

Cada `delivery_id` deberá alcanzar exactamente un estado terminal.

---

# 22.41 Modelo consolidado de consumer

Un Consumer deberá representar:

> una entidad lógica autorizada y técnicamente capaz de consumir una determinada representación de respuesta HEYTI.

---

## 22.42 ConsumerProfile mínimo

Conceptualmente deberá permitir conocer:

```text
consumer_id
enabled
supported_contract_versions
supported_content_types
adapter relationship
```

cuando estos campos sean necesarios.

---

## 22.43 Consumer no es UI

Un consumer puede ser:

```text
Portal
API client
test harness
future service
```

No deberá asumirse:

```text
consumer == browser
```

---

# 22.44 Modelo consolidado de adapter

Un adapter deberá representar:

> el mecanismo técnico utilizado para ejecutar una operación de entrega.

---

## 22.45 Adapter baseline

El primer adapter recomendado será:

```text
InMemoryDeliveryAdapter
```

o equivalente.

---

## 22.46 Razón arquitectónica

Esto permitirá demostrar:

```text
Delivery exists independently of HTTP.
```

---

## 22.47 Adapter contract

Conceptualmente:

```text
DeliveryEnvelope
      ↓
Adapter
      ↓
AdapterResult
```

---

## 22.48 Adapter neutrality

El adapter no deberá:

```text
reinterpret response
modify evidence
change warnings
invent UI instructions
execute capabilities
```

---

# 22.49 Modelo consolidado de serialización

La serialización deberá ser:

```text
explicit
deterministic
canonical
testable
```

---

## 22.50 Tipos soportados

La implementación deberá soportar explícitamente únicamente los tipos necesarios por los contratos reales.

Conceptualmente podrán incluir:

```text
None
bool
int
float
str
list
dict
Enum
UUID
date
datetime
```

---

## 22.51 Tipo desconocido

Un tipo no soportado deberá:

```text
FAIL EXPLICITLY
```

---

## 22.52 Prohibición consolidada

Queda prohibido utilizar como mecanismo general:

```python
default=str
```

para ocultar tipos no serializables.

---

## 22.53 Preservación semántica

La serialización deberá preservar:

```text
null
identifiers
units
timestamps
warnings
evidence references
contract versions
```

cuando formen parte de la respuesta.

---

# 22.54 Modelo consolidado de errores

Los errores deberán poseer suficiente estructura para permitir:

```text
classification
diagnosis
consumer mapping
traceability
```

---

## 22.55 Error mínimo conceptual

```text
code
category
stage
message
retryable
```

cuando resulte aplicable.

---

## 22.56 Error público versus interno

El sistema podrá mantener:

```text
internal diagnostic detail
```

sin exponerlo completamente al consumidor.

---

## 22.57 No exception leakage

No deberán exponerse directamente:

```text
stack traces
internal paths
secrets
raw exception internals
```

en payload público.

---

# 22.58 Modelo consolidado de trazabilidad

El objetivo será mantener continuidad entre:

```text
Runtime
Materialization
Delivery
Consumer boundary
```

---

## 22.59 Trace mínimo

Deberá permitir correlacionar al menos:

```text
response_id
delivery_id
consumer_id
adapter_id
status
```

y, cuando existan:

```text
request_id
execution_id
session_id
```

---

## 22.60 No inventar identidad upstream

Si Runtime no proporciona una identidad concreta, Delivery no deberá fingir que proviene de Runtime.

---

## 22.61 Delivery-owned identity

La única identidad que HRRD necesariamente deberá controlar será:

```text
delivery_id
```

---

# 22.62 Modelo consolidado de seguridad

La frontera de Delivery deberá operar bajo:

```text
explicit consumer
explicit target
explicit authorization
controlled projection
```

cuando la integración externa lo requiera.

---

## 22.63 Fail Closed

Ante una decisión obligatoria de autorización que no pueda resolverse:

```text
REJECTED
```

deberá ser preferible a:

```text
deliver anyway
```

---

## 22.64 Public Projection

La representación externa deberá contener únicamente información permitida.

---

## 22.65 No secret propagation

Delivery deberá impedir la exposición accidental de:

```text
credentials
tokens
internal configuration
private diagnostic information
```

---

# 22.66 Modelo consolidado de observabilidad

La observabilidad deberá poder responder:

```text
Did Delivery start?
Did it terminate?
What status?
Which consumer?
Which adapter?
Which response?
Which error?
```

---

## 22.67 Observabilidad mínima v1.0

Podrá comenzar mediante:

```text
structured logging
trace fields
terminal DeliveryResult
```

sin requerir todavía infraestructura distribuida.

---

## 22.68 No observability overengineering

No será obligatorio introducir:

```text
OpenTelemetry
distributed collectors
external metrics platform
```

durante Sprint 23.

---

# 22.69 Modelo consolidado de Presentation

Presentation deberá permanecer aguas abajo.

```text
HEYTI Core
   ↓
Materialization
   ↓
Delivery
   ↓
Gateway / Consumer Adapter
   ↓
Presentation
```

---

## 22.70 Presentation interpreta

Presentation podrá decidir:

```text
layout
colors
cards
charts
maps
interaction
responsive behavior
```

---

## 22.71 Delivery expresa significado

Delivery deberá transportar elementos semánticos suficientes como:

```text
metric
series
territorial reference
warning
evidence
action
```

cuando formen parte del Response Contract.

---

## 22.72 No visual leakage

No deberán incorporarse al Core detalles como:

```text
hex color
pixel width
CSS class
Leaflet zoom
Chart.js configuration
```

---

# 22.73 Baseline de integración

La primera vertical recomendada seguirá siendo:

```text
DescribeSection
```

---

## 22.74 Razón

DescribeSection ya constituye una capability adecuada para demostrar:

```text
Capability
→ Materialization
→ Delivery
```

sin necesitar construir simultáneamente todos los módulos.

---

## 22.75 Vertical mínima

```text
Known Section
      ↓
DescribeSection
      ↓
Materialization
      ↓
Materialized Response
      ↓
HRRD
      ↓
InMemory Adapter
      ↓
DeliveryResult
```

---

## 22.76 Qué deberá demostrar

La vertical deberá demostrar:

```text
response survives
response_id survives
delivery_id created
consumer resolved
adapter executed
status returned
trace preserved
```

---

# 22.77 Baseline de pruebas

La arquitectura queda preparada para:

```text
Unit Tests
Contract Tests
Integration Tests
Architectural Conformance Tests
Global Regression Tests
```

---

## 22.78 Regla de certificación

La implementación no deberá considerarse completa únicamente porque:

```text
new tests pass
```

También deberá verificarse:

```text
global pytest passes
```

---

## 22.79 Zero Omission Testing

Todo campo REQUIRED deberá ser eliminado deliberadamente en al menos un escenario de prueba relevante para verificar que la validación falla.

---

## 22.80 Error Path Testing

Deberán probarse explícitamente:

```text
REJECTED
FAILED
DELIVERED
```

---

## 22.81 Mutation Testing Conceptual

Deberá comprobarse que Delivery no modifica la respuesta materializada.

No implica necesariamente utilizar una herramienta formal de mutation testing.

---

# 22.82 Baseline de implementación

El orden recomendado queda congelado como:

```text
01. Repository Audit
02. Confirm Materialization Boundary
03. Contracts
04. Context + Trace
05. Validation
06. Serialization
07. Consumer Model
08. Adapter Abstraction
09. InMemory Adapter
10. Delivery Orchestration
11. Error Normalization
12. Observability
13. Runtime Integration
14. DescribeSection Vertical Slice
15. Verification
16. Zero Error Audit
17. Zero Omission Audit
18. Certification
```

---

## 22.83 No salto de fases críticas

Especialmente no deberá saltarse:

```text
Repository Audit
```

ni:

```text
Materialization Boundary Verification
```

---

## 22.84 Por qué

Sprint 22 ya materializó componentes reales.

Sprint 23 deberá integrarse con ellos.

No deberá reconstruirlos basándose únicamente en este documento.

---

# 22.85 Repository Reality Rule

Al iniciar código:

> **El repositorio real deberá ser inspeccionado antes de decidir nombres, rutas, imports, clases o dependencias definitivas.**

---

## 22.86 Documento versus repositorio

Si este documento propone:

```text
src/heyti/delivery/
```

pero la estructura real demuestra una ubicación mejor y arquitectónicamente consistente, deberá utilizarse la estructura correcta.

---

## 22.87 No architecture violation by naming

Cambiar:

```text
DeliveryService
```

por otro nombre coherente no viola la arquitectura.

---

## 22.88 Architecture violation by responsibility

En cambio, permitir que Delivery ejecute una capability sí la viola.

---

# 22.89 Baseline de dependencias

La dirección permitida deberá conservarse conceptualmente:

```text
Runtime
   ↓
Materialization
   ↓
Delivery
   ↓
Adapters
```

---

## 22.90 Dependencias prohibidas

No:

```text
Materialization
→ Delivery
```

como dependencia inversa necesaria.

No:

```text
Capability
→ HTTP Adapter
```

No:

```text
Delivery Core
→ Portal
```

No:

```text
Delivery Core
→ Leaflet
```

---

# 22.91 Baseline de extensibilidad

La arquitectura deberá admitir futuros:

```text
consumers
adapters
content types
security policies
observability integrations
```

sin reescribir el núcleo.

---

## 22.92 Extensión esperada

```text
new adapter
      ↓
register/configure
      ↓
tests
```

---

## 22.93 Extensión no esperada

```text
new adapter
      ↓
rewrite Materialization
```

indicaría una frontera incorrecta.

---

# 22.94 Baseline de compatibilidad

La versión inicial deberá comenzar con un contrato explícito.

Conceptualmente:

```text
Delivery Contract 1.0
```

---

## 22.95 Compatibility Rule

Un cambio incompatible deberá producir:

```text
version review
```

y, cuando corresponda:

```text
new MAJOR version
```

---

## 22.96 No silent compatibility break

Nunca:

```text
same version
+
different meaning
```

---

# 22.97 Baseline de deuda técnica

La implementación podrá aceptar deuda técnica únicamente cuando sea:

```text
explicit
bounded
documented
non-critical
```

---

## 22.98 Critical defects are not debt

No podrán diferirse como deuda:

```text
response corruption
security bypass
trace loss
silent omissions
contract violation
```

---

# 22.99 Baseline de elementos diferidos

Se mantienen como `DEFERRED BY DESIGN`, salvo decisión posterior:

```text
production HTTP adapter
Gateway real
WebSocket
streaming
automatic retry
circuit breaker
message queue
multi-version negotiation
persistent audit store
distributed tracing
advanced authorization
dynamic consumer discovery
```

---

## 22.100 Deferred does not block certification

Estos elementos no impedirán certificar HRRD v1.0 si no pertenecen al alcance aprobado.

---

## 22.101 Missing does block certification

En cambio, la ausencia accidental de una pieza requerida sí deberá bloquear certificación.

---

# 22.102 Architecture Closure Review

Antes de declarar el documento cerrado deberá comprobarse que responde claramente a las siguientes preguntas.

---

## 22.103 Question 1

```text
What enters HRRD?
```

Respuesta:

```text
a materialized response plus delivery context
```

---

## 22.104 Question 2

```text
What leaves HRRD?
```

Respuesta:

```text
delivery execution + structured DeliveryResult
```

---

## 22.105 Question 3

```text
Who receives the response?
```

Respuesta:

```text
an explicit Consumer
```

---

## 22.106 Question 4

```text
How is it delivered?
```

Respuesta:

```text
through an explicit Adapter
```

---

## 22.107 Question 5

```text
Who owns cognition?
```

Respuesta:

```text
not HRRD
```

---

## 22.108 Question 6

```text
Who owns rendering?
```

Respuesta:

```text
Presentation
```

---

## 22.109 Question 7

```text
Who owns transport specifics?
```

Respuesta:

```text
concrete Adapter / Gateway layer
```

---

## 22.110 Question 8

```text
How is delivery identified?
```

Respuesta:

```text
delivery_id
```

---

## 22.111 Question 9

```text
How is the original response identified?
```

Respuesta:

```text
response_id
```

---

## 22.112 Question 10

```text
What are the terminal states?
```

Respuesta:

```text
DELIVERED
REJECTED
FAILED
```

---

## 22.113 Question 11

```text
How are errors represented?
```

Respuesta:

```text
structured DeliveryError
```

---

## 22.114 Question 12

```text
How is compatibility controlled?
```

Respuesta:

```text
contract version + ConsumerProfile
```

---

## 22.115 Question 13

```text
How is trace preserved?
```

Respuesta:

```text
explicit DeliveryTrace / correlated identifiers
```

---

## 22.116 Question 14

```text
How is the architecture verified?
```

Respuesta:

```text
tests + conformance review + global regression
```

---

## 22.117 Question 15

```text
How does HRRD evolve?
```

Respuesta:

```text
controlled extension + explicit versioning + governance
```

---

# 22.118 Closure Result

Las preguntas fundamentales poseen una respuesta arquitectónica explícita.

Por tanto, la especificación puede considerarse:

```text
ARCHITECTURALLY COMPLETE
```

para su alcance v1.0.

---

## 22.119 Significado exacto

`ARCHITECTURALLY COMPLETE` no significa:

```text
IMPLEMENTED
```

ni:

```text
CERTIFIED IN CODE
```

Significa:

```text
READY FOR CONTROLLED MATERIALIZATION
```

---

# 22.120 Estado formal del documento

Se propone declarar:

```text
Document:
HEYTI_Runtime_Response_Delivery_v1.0.md

Architectural Status:
BASELINE READY

Implementation Status:
NOT YET CERTIFIED

Materialization Status:
AUTHORIZED TO BEGIN AFTER REPOSITORY AUDIT
```

---

## 22.121 Distinción crítica

Esta declaración evita afirmar prematuramente:

```text
HRRD works
```

antes de que exista evidencia ejecutable.

---

# 22.122 Baseline oficial HRRD v1.0

La baseline arquitectónica queda compuesta por:

```text
HEYTI_Runtime_Response_Delivery_v1.0.md
+
HEYTI architectural governance
+
existing Runtime contracts
+
existing Materialization contracts
+
implementation evidence to be created in Sprint 23
```

---

## 22.123 Baseline documental

El presente documento constituye la referencia principal de arquitectura específica de HRRD v1.0.

---

## 22.124 Baseline ejecutable futura

Después de implementación deberá añadirse:

```text
source code
tests
certified commit
```

como evidencia ejecutable de la baseline.

---

# 22.125 Condiciones para iniciar materialización

Antes de escribir código deberán cumplirse:

```text
[ ] Document saved
[ ] Architecture reviewed
[ ] Repository clean or known state
[ ] Existing Sprint 22 baseline identified
[ ] Current global pytest executed
[ ] Materialization package inspected
[ ] Runtime package inspected
[ ] Existing contracts inspected
[ ] Existing tests inspected
```

---

## 22.126 Importancia de la baseline previa

Antes de introducir HRRD deberá conocerse:

```text
how many tests pass now
```

para poder distinguir:

```text
existing state
```

de:

```text
Sprint 23 regression
```

---

## 22.127 Baseline Test Command

La secuencia inicial deberá incluir:

```powershell
pytest -q
```

---

## 22.128 Repository Status

También:

```powershell
git status
```

---

## 22.129 Diff Baseline

Si existen cambios no comprometidos deberán entenderse antes de continuar.

---

## 22.130 No coding on unknown state

No deberá comenzar materialización sobre un working tree cuyo estado no comprendamos.

---

# 22.131 Primera orden técnica después del cierre

La primera actividad de implementación será:

```text
AUDIT THE REAL REPOSITORY
```

No:

```text
CREATE delivery.py
```

---

## 22.132 Objetivo de la auditoría inicial

Determinar con precisión:

```text
current package tree
current Runtime flow
current Materialization API
existing response contract
existing error patterns
existing registry patterns
existing test conventions
```

---

## 22.133 Resultado esperado

Solo después de esa inspección deberá proponerse:

```text
exact files to create
exact files to modify
exact tests to add
```

---

# 22.134 No speculative code

Hasta completar dicha auditoría no deberán inventarse:

```text
imports
constructors
class names
function signatures
module paths
```

como si fueran hechos del repositorio.

---

## 22.135 Architecture can prescribe responsibility

Sí puede prescribir:

```text
there must be validation
```

pero la auditoría determinará si corresponde:

```text
validator.py
contract method
service method
existing validation framework
```

---

# 22.136 Definition of Architecture Done

La arquitectura HRRD v1.0 estará cerrada cuando:

```text
[✓] Purpose defined
[✓] Scope defined
[✓] Boundaries defined
[✓] Responsibilities defined
[✓] Non-responsibilities defined
[✓] Contracts defined conceptually
[✓] Identity semantics defined
[✓] Terminal states defined
[✓] Consumer model defined
[✓] Adapter model defined
[✓] Serialization rules defined
[✓] Error model defined
[✓] Traceability defined
[✓] Security principles defined
[✓] Versioning defined
[✓] Observability defined
[✓] Presentation boundary defined
[✓] Testing strategy defined
[✓] Implementation order defined
[✓] Governance defined
[✓] Deferred items identified
```

---

## 22.137 Architecture DoD Result

```text
ARCHITECTURE DEFINITION OF DONE
===============================
STATUS: SATISFIED
```

para el alcance documental v1.0.

---

# 22.138 Definition of Implementation Done

La implementación futura requerirá:

```text
[ ] Repository audit complete
[ ] Contracts materialized
[ ] Validation materialized
[ ] Serialization materialized
[ ] Consumer model materialized
[ ] Adapter abstraction materialized
[ ] InMemory adapter operational
[ ] Delivery orchestration operational
[ ] Errors normalized
[ ] Trace operational
[ ] Observability baseline operational
[ ] Runtime integration operational
[ ] DescribeSection vertical slice operational
[ ] Targeted tests green
[ ] Global tests green
[ ] Zero Error audit passed
[ ] Zero Omission audit passed
[ ] Architecture conformance passed
```

---

## 22.139 Important distinction

Por tanto:

```text
Architecture DoD = COMPLETE
Implementation DoD = PENDING
```

---

# 22.140 Certification levels consolidated

La futura implementación podrá atravesar:

```text
LEVEL 1 — Core Contract Ready
LEVEL 2 — Delivery Core Ready
LEVEL 3 — Gateway Ready
LEVEL 4 — Presentation Integrated
```

---

## 22.141 Sprint 23 objective

El objetivo principal deberá ser alcanzar:

```text
LEVEL 1
+
LEVEL 2
```

con evidencia real.

---

## 22.142 Gateway

Level 3 podrá pertenecer a una expansión posterior si no es requerido para certificar el núcleo.

---

## 22.143 Presentation

Level 4 deberá realizarse únicamente cuando exista una vertical visual real.

---

# 22.144 Gate de salida documental

Antes de cerrar este documento deberán cumplirse:

```text
Architecture coherent?
YES

Implementation sequence defined?
YES

Testing strategy defined?
YES

Governance defined?
YES

Deferred scope explicit?
YES

Presentation boundary protected?
YES

Materialization boundary protected?
YES

Runtime boundary identified?
YES

Ready for repository audit?
YES
```

---

# 22.145 Architectural Closure Decision

Con base en los capítulos desarrollados, se declara:

```text
HEYTI RUNTIME RESPONSE DELIVERY v1.0

ARCHITECTURAL DESIGN:
CLOSED

BASELINE:
ESTABLISHED

IMPLEMENTATION:
AUTHORIZED AFTER REPOSITORY AUDIT

CODE CERTIFICATION:
PENDING
```

---

# 22.146 Invariantes finales de cierre

Se establecen los siguientes invariantes finales.

### HRRD-CLOSE01 — Materialized Input

HRRD deberá recibir una respuesta ya materializada.

### HRRD-CLOSE02 — Semantic Preservation

Delivery no deberá modificar el significado cognitivo.

### HRRD-CLOSE03 — Explicit Delivery Identity

Cada operación deberá poseer `delivery_id`.

### HRRD-CLOSE04 — Response Identity Preservation

`response_id` deberá conservarse.

### HRRD-CLOSE05 — Explicit Consumer

Toda entrega deberá dirigirse a un Consumer explícito.

### HRRD-CLOSE06 — Explicit Adapter

Toda entrega deberá utilizar un Adapter explícito.

### HRRD-CLOSE07 — Terminal State

Cada operación deberá finalizar en un estado terminal válido.

### HRRD-CLOSE08 — Structured Failure

Todo fallo deberá expresarse mediante un error estructurado.

### HRRD-CLOSE09 — Trace Continuity

La operación deberá mantener correlación con la respuesta y el contexto disponible.

### HRRD-CLOSE10 — Presentation Independence

HRRD no deberá depender de implementación visual.

### HRRD-CLOSE11 — Transport Independence

El Core no deberá depender de un transporte concreto.

### HRRD-CLOSE12 — Explicit Versioning

Las fronteras públicas deberán evolucionar mediante reglas explícitas de versión.

### HRRD-CLOSE13 — Security Boundary

Ninguna entrega deberá saltarse controles obligatorios de seguridad.

### HRRD-CLOSE14 — Observable Terminal Outcome

El resultado final deberá poder diagnosticarse.

### HRRD-CLOSE15 — Tests as Evidence

La implementación deberá demostrar estos invariantes mediante evidencia reproducible.

### HRRD-CLOSE16 — Repository Audit Before Code

La materialización deberá comenzar inspeccionando el estado real del repositorio.

### HRRD-CLOSE17 — Zero Silent Omission

Ningún campo contractual obligatorio deberá perderse silenciosamente.

### HRRD-CLOSE18 — No Architectural Drift

Toda desviación significativa deberá documentarse antes de consolidarse.

### HRRD-CLOSE19 — Deferred by Design Is Explicit

Las capacidades diferidas deberán permanecer identificadas.

### HRRD-CLOSE20 — Global Regression Required

Sprint 23 no podrá certificarse mientras exista una regresión global conocida.

---

# 22.147 Declaración de preparación para materialización

Con la baseline arquitectónica establecida, HRRD queda preparado para pasar de:

```text
ARCHITECTURAL DEFINITION
```

a:

```text
CONTROLLED TECHNICAL MATERIALIZATION
```

La transición deberá ejecutarse exactamente bajo la disciplina:

```text
INSPECT
   ↓
UNDERSTAND
   ↓
DESIGN AGAINST REALITY
   ↓
IMPLEMENT
   ↓
TEST
   ↓
VERIFY
   ↓
CERTIFY
```

---

# 22.148 La frontera que ahora posee HEYTI

Con esta arquitectura, el recorrido conceptual de una respuesta queda definido como:

```text
User / Caller
      ↓
Runtime
      ↓
Capability
      ↓
Knowledge / Evidence
      ↓
Capability Result
      ↓
Materialization
      ↓
HEYTI Response
      ↓
Runtime Response Delivery
      ↓
Consumer / Gateway
      ↓
Presentation
      ↓
User
```

HEYTI ya no deberá pensar en una respuesta como:

```text
something returned by a Python function
```

sino como un artefacto con ciclo de vida completo:

```text
requested
executed
constructed
materialized
identified
validated
serialized
delivered
observed
presented
```

---

# 22.149 Importancia arquitectónica del Sprint 23

Sprint 23 establece una frontera decisiva.

Antes de HRRD:

```text
HEYTI can produce a response.
```

Después de HRRD:

```text
HEYTI can deliver that response
through a controlled,
traceable,
versioned,
consumer-aware,
transport-independent boundary.
```

Ese cambio no es únicamente técnico.

Es arquitectónico.

---

# 22.150 Relación con la futura interfaz visual

HRRD prepara la salida necesaria para que posteriormente puedan existir:

```text
graphs
maps
statistics
tables
warnings
evidence
territorial references
actions
```

sin contaminar el Core con Presentation.

---

## 22.151 Condición previa a la interfaz completa

Antes de materializar la experiencia visual de los seis módulos deberá realizarse formalmente la auditoría de cobertura y confiabilidad de sus fuentes de datos.

La interfaz no deberá asumir información inexistente.

---

## 22.152 Principio de visualización

La secuencia deberá permanecer:

```text
SOURCE TRUTH
      ↓
KNOWLEDGE
      ↓
CAPABILITY
      ↓
MATERIALIZATION
      ↓
DELIVERY
      ↓
PRESENTATION
```

Nunca:

```text
DESIRED GRAPH
      ↓
invent whatever data is needed
```

---

# 22.153 Preparación para el usuario final

La arquitectura deberá permitir que en una fase posterior un usuario pueda:

```text
consult a section
      ↓
receive its radiography
      ↓
review indicators
      ↓
inspect maps
      ↓
inspect graphs
      ↓
navigate to a module
      ↓
continue asking HEYTI
```

sin que el mecanismo visual invada la lógica cognitiva.

---

# 22.154 Preservación de los seis módulos

La futura experiencia deberá poder integrar progresivamente los dominios operativos de AT 27–30 bajo una frontera común de respuesta.

El objetivo no será crear seis HEYTI diferentes.

Será:

```text
ONE HEYTI
      ↓
MULTIPLE CAPABILITIES
      ↓
ONE MATERIALIZATION DISCIPLINE
      ↓
ONE DELIVERY DISCIPLINE
      ↓
MULTIPLE PRESENTATIONS
```

cuando sea necesario.

---

# 22.155 Cierre del ciclo Materialization → Delivery

Sprint 22 estableció la disciplina de Materialization.

Sprint 23 establece la disciplina de Delivery.

Conceptualmente:

```text
Capability Result
      ↓
Sprint 22
MATERIALIZATION
      ↓
HEYTI Response
      ↓
Sprint 23
DELIVERY
      ↓
Consumer Boundary
```

Esta relación deberá preservarse como una de las fronteras principales de HEYTI-CORE.

---

# 22.156 Regla de transición a código

Después de guardar y revisar este capítulo:

```text
NO MORE SPECULATIVE IMPLEMENTATION DESIGN
```

La siguiente fuente de verdad deberá ser:

```text
THE REAL REPOSITORY
```

---

## 22.157 Primera auditoría

Deberá comenzar revisando:

```text
git status
pytest -q
src/heyti/
tests/
src/heyti/materialization/
Runtime-related packages
DescribeSection
```

---

## 22.158 Después de la auditoría

Solo entonces deberá definirse:

```text
Phase 1 implementation
```

con archivos concretos.

---

# 22.159 Regla operativa de Sprint 23

Durante implementación deberá repetirse:

```text
ONE CHANGE
      ↓
ONE VERIFICATION
      ↓
NEXT CHANGE
```

cuando la naturaleza del cambio lo permita.

---

## 22.160 No sprint by avalanche

No deberá implementarse todo HRRD en un único bloque masivo antes de probarlo.

---

# 22.161 Criterio de cierre final del documento

El documento `HEYTI_Runtime_Response_Delivery_v1.0.md` podrá declararse completo cuando:

```text
all planned architecture chapters are present
the final document is saved
no chapter is truncated
the Markdown structure is valid
the repository contains the intended file
```

---

## 22.162 Auditoría documental posterior

Antes de comenzar código será recomendable revisar:

```text
heading sequence
chapter completeness
code fences
tables
internal terminology
repeated contradictions
```

sin reescribir el documento innecesariamente.

---

# 22.163 Estado oficial propuesto

```text
============================================================
HEYTI RUNTIME RESPONSE DELIVERY — HRRD v1.0
============================================================

DOCUMENT:
HEYTI_Runtime_Response_Delivery_v1.0.md

ARCHITECTURAL STATUS:
CLOSED

BASELINE STATUS:
ESTABLISHED

MATERIALIZATION READINESS:
READY

IMPLEMENTATION STATUS:
PENDING

CODE CERTIFICATION:
PENDING

PRIMARY NEXT ACTION:
REPOSITORY BASELINE AUDIT

DISCIPLINE:
0 ERRORES
0 OMISIONES
============================================================
```

---

# 22.164 Declaración arquitectónica final

HEYTI Runtime Response Delivery v1.0 queda definido como la frontera responsable de llevar una respuesta materializada desde el Runtime hacia un consumidor mediante un proceso explícito, validado, serializable, trazable, observable y desacoplado de Presentation y del transporte concreto.

Su arquitectura protege una separación fundamental:

```text
HEYTI decides and constructs meaning.
Materialization formalizes that meaning.
Delivery transports that meaning.
Presentation renders that meaning.
```

Ninguna de estas capas deberá apropiarse silenciosamente de la responsabilidad de otra.

La baseline final queda resumida como:

```text
KNOWLEDGE
   ↓
CAPABILITY
   ↓
MATERIALIZATION
   ↓
RESPONSE
   ↓
DELIVERY
   ↓
CONSUMER
   ↓
PRESENTATION
```

y su disciplina operacional queda establecida como:

```text
EXPLICIT CONTRACTS
+
EXPLICIT IDENTITIES
+
EXPLICIT ERRORS
+
EXPLICIT CONSUMERS
+
EXPLICIT ADAPTERS
+
EXPLICIT TRACEABILITY
+
REPRODUCIBLE TESTS
```

bajo la regla irrenunciable:

```text
0 ERRORES
0 OMISIONES
```

---

# 22.165 Declaración de cierre

Con este capítulo queda formalmente cerrada la definición arquitectónica de:

```text
HEYTI Runtime Response Delivery v1.0
```

y queda autorizada su transición a la siguiente etapa:

```text
REPOSITORY AUDIT
      ↓
TECHNICAL MATERIALIZATION
      ↓
VERIFICATION
      ↓
CERTIFICATION
```

La arquitectura ya estableció **qué debe construirse**, **qué no debe construirse**, **dónde comienza Delivery**, **dónde termina**, **cómo deberá evolucionar** y **cómo deberá demostrarse que funciona**.

A partir de este punto, la siguiente pregunta ya no será:

```text
¿Cómo imaginamos Runtime Response Delivery?
```

La siguiente pregunta será:

```text
¿Qué existe exactamente hoy
en el repositorio HEYTI
y cuál es el primer cambio mínimo,
correcto y verificable
para materializar esta arquitectura?
```

Ese será el punto de partida de la implementación real de Sprint 23.

---

**Fin del Capítulo 22**

**Fin de HEYTI Runtime Response Delivery v1.0 — Arquitectura**
