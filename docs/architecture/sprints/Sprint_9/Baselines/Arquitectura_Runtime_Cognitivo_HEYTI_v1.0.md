# Sprint 9.4 — Arquitectura del Runtime Cognitivo HEYTI

## Baseline de Arquitectura del Runtime Core

**Documento:** Arquitectura del Runtime Cognitivo HEYTI  
**Versión:** 1.0  
**Estado:** Baseline de Fase A  
**Fuente única de verdad:** Documento maestro del Sprint 9.4  
**Clasificación:** Arquitectura CORE  
**Implementación:** Pendiente  
**Propietario:** Arquitectura HEYTI  
**Fecha de consolidación:** 15 de julio de 2026  

---

# Control del documento

| Campo | Valor |
|---|---|
| Sprint | 9.4 |
| Fase | A — Arquitectura del Runtime Core |
| Estado | Completada y auditada |
| Hallazgos críticos | 0 |
| Hallazgos mayores | 0 |
| Hallazgos menores | 3 |
| Decisiones aprobadas | PDA-001 a PDA-010, con ajuste PDA-005A |
| Próximo paso | Expansión documental, ACS detallados y preparación de implementación |

---

# Índice

1. Propósito del documento  
2. Visión del Runtime Cognitivo  
3. Filosofía y principios rectores  
4. Modelo operativo general  
5. Entidades y artefactos fundamentales  
6. Componentes CORE  
7. Contratos del Runtime  
8. Eventos y comunicaciones  
9. Políticas de gobierno  
10. Matriz de Componentes del Runtime  
11. Flujo end-to-end  
12. Clasificación CORE, FOUNDATION y EVOLUCIÓN  
13. Registro de PDA aprobadas  
14. Auditoría arquitectónica de Fase A  
15. Riesgos y anti-patrones  
16. Criterios de aceptación  
17. Decisiones diferidas  
18. Cierre de Fase A  

---

# 1. Propósito del documento

El presente documento consolida la arquitectura del **Runtime Cognitivo HEYTI** correspondiente a la Fase A del Sprint 9.4.

Su propósito es establecer una base implementable, trazable, defendible y suficientemente robusta para coordinar las capacidades cognitivas de HEYTI sin mezclar responsabilidades, sin acoplar el Runtime a motores específicos y sin permitir que la presión operativa de las campañas deteriore la arquitectura del sistema.

Este documento no constituye una transcripción de conversaciones de diseño. Representa la consolidación formal de las decisiones aprobadas, los principios aceptados, los contratos fundamentales, las políticas de gobierno y los resultados de la auditoría arquitectónica del CORE.

---

# 2. Visión del Runtime Cognitivo

El Runtime Cognitivo HEYTI es la infraestructura operativa responsable de administrar el ciclo completo de una interacción cognitiva, desde que una solicitud entra al sistema hasta que la misión es cerrada, auditada y comunicada al usuario.

El Runtime:

- recibe solicitudes externas mediante contratos controlados;
- comprende quién pregunta y qué necesita resolver;
- convierte solicitudes en misiones cognitivas ejecutables;
- autoriza y registra ejecuciones;
- prepara condiciones, capacidades, contexto y recursos;
- planifica y distribuye tareas;
- coordina motores especializados;
- gobierna eventos y transiciones;
- protege el contexto oficial de la ejecución;
- compone respuestas adaptadas al usuario;
- cierra la misión de forma responsable.

El Runtime no:

- realiza razonamiento estratégico;
- interpreta evidencia especializada;
- calcula confianza;
- ejecuta análisis territoriales;
- sustituye las responsabilidades de los motores cognitivos;
- improvisa respuestas ante misiones ambiguas.

> **HEYTI no administra una secuencia aislada de preguntas y respuestas; administra un diálogo orientado a resolver una misión.**

---

# 3. Filosofía y principios rectores

## 3.1 Principio de Responsabilidad Delimitada

Cada componente debe poseer una responsabilidad principal claramente definida y evitar asumir responsabilidades pertenecientes a otros componentes.

En lenguaje del Laboratorio HEYTI:

> **Cada quien haga su chamba.**

---

## 3.2 Principio de Honestidad Cognitiva

> **HEYTI nunca fingirá haber comprendido una solicitud cuando existan múltiples interpretaciones plausibles. En esos casos privilegiará la clarificación sobre la especulación.**

---

## 3.3 Ley de Clarificación

> **Una misión ambigua nunca debe convertirse en una Execution. Primero se clarifica; después se ejecuta.**

---

## 3.4 Principio de Identidad Cognitiva

Toda Cognitive Mission deberá poseer una identidad propia e independiente de las solicitudes individuales y de las ejecuciones utilizadas para resolverla.

---

## 3.5 Principio de Continuidad Dialógica

Cada intervención del usuario deberá interpretarse dentro de la sesión, la misión activa y su historial, evitando tratarla como una consulta aislada cuando exista continuidad semántica y estratégica.

> **El diálogo conserva el propósito; las ejecuciones materializan sus avances.**

---

## 3.6 Principio de Persistencia Inteligente

> **El Runtime preservará todo conocimiento cuya validez permanezca vigente y recalculará únicamente aquello afectado por un cambio en la misión, el contexto o las restricciones.**

---

## 3.7 Principio de Adaptación Comunicativa

> **La respuesta deberá adaptarse al perfil, rol, canal y objetivo del usuario sin alterar el conocimiento estratégico generado por el Runtime.**

---

## 3.8 Principio de Comunicación Controlada

> **Todo componente tendrá explícitamente definidos los componentes con los que puede interactuar. Cualquier interacción fuera de ese contrato constituye una violación arquitectónica.**

---

## 3.9 Principio de Coordinación

> **El Kernel gobierna el avance de la misión, no el contenido técnico producido por los motores.**

---

## 3.10 Principio de Cierre Responsable

> **HEYTI nunca declarará una misión como completada si los criterios definidos en la Cognitive Mission Specification no han sido satisfechos o si las limitaciones afectan materialmente la calidad de la recomendación.**

---

## 3.11 Principio de Mínimo Contexto

Cada motor recibirá únicamente la información necesaria para ejecutar correctamente su responsabilidad.

---

## 3.12 Principio de Inmutabilidad Contractual

Los contratos fundamentales del Runtime deberán ser inmutables. Toda evolución relevante generará una nueva versión en lugar de sobrescribir silenciosamente el artefacto anterior.

---

## 3.13 Principio de Arquitectura Defendible

Toda decisión operativa relevante deberá poder explicar:

- quién la tomó;
- bajo qué regla;
- con qué información;
- en qué momento;
- qué estado produjo;
- qué evidencia de trazabilidad existe.

---

# 4. Modelo operativo general

El Runtime Cognitivo se organiza en tres grandes fases:

1. **Cognitive Admission**
2. **Cognitive Execution**
3. **Cognitive Completion**

```text
Solicitud externa
        ↓
Cognitive Admission
        ↓
Cognitive Mission Specification
        ↓
Execution autorizada y registrada
        ↓
Cognitive Readiness
        ↓
Cognitive Execution
        ↓
Cognitive Completion
        ↓
Respuesta y cierre auditable
```

## 4.1 Cognitive Admission

Determina si una solicitud técnicamente válida puede convertirse en una misión cognitiva ejecutable.

Durante esta fase todavía no existe una Execution activa.

La admisión resuelve:

- identidad del solicitante;
- rol y permisos;
- ámbito territorial e institucional;
- intención;
- objetivo operativo;
- objetivo estratégico;
- necesidad de aclaración;
- capacidades requeridas;
- continuidad con una misión existente;
- elegibilidad de reutilización;
- decisión de admisión.

## 4.2 Cognitive Execution

Comienza cuando una misión admitida ha sido autorizada, registrada y declarada lista.

Durante esta fase el Runtime:

- construye el plan;
- resuelve capacidades;
- distribuye tareas;
- recibe resultados;
- actualiza el contexto mediante mecanismos gobernados;
- evalúa readiness para continuar;
- coordina reintentos, degradación o replanificación;
- solicita composición de respuesta.

## 4.3 Cognitive Completion

Comienza cuando la misión ha alcanzado un estado terminal o una condición de cierre.

Incluye:

- persistencia del resultado;
- registro de traza;
- auditoría;
- liberación de recursos;
- actualización de métricas;
- registro de limitaciones;
- cierre administrativo;
- publicación del estado terminal.

---

# 5. Entidades y artefactos fundamentales

## 5.1 Session

Representa la continuidad conversacional de un usuario.

Responde:

> ¿Quién está conversando y cuál es el hilo activo?

Una Session puede contener múltiples Requests y múltiples Missions.

---

## 5.2 Request

Representa una intervención concreta del usuario o sistema externo.

Cada Request posee identidad propia aunque el contenido textual se repita.

Campos conceptuales mínimos:

```text
request_id
session_id
source_channel
source_format
original_payload
normalized_payload
requester_reference
received_at
correlation_id
trace_metadata
```

---

## 5.3 Request Fingerprint

Huella contextual utilizada para identificar solicitudes funcionalmente equivalentes.

Considera, como mínimo:

- intención;
- objetivo;
- solicitante o perfil;
- permisos;
- ámbito territorial;
- fecha de corte;
- versiones de datos;
- políticas;
- parámetros relevantes.

La igualdad textual no implica equivalencia cognitiva.

---

## 5.4 Cognitive Mission

Representa el problema que HEYTI debe resolver a través del diálogo.

Responde:

> ¿Qué necesidad real del usuario estamos intentando resolver?

Una Mission puede generar múltiples Executions.

---

## 5.5 Cognitive Mission Specification — CMS

Contrato inmutable que convierte una solicitud admitida en una misión ejecutable.

```text
Cognitive Mission Specification
├── mission_id
├── specification_version
├── request_id
├── session_id
├── requester_context
├── normalized_intent
├── operational_objective
├── strategic_objective
├── mission_type
├── territorial_scope
├── institutional_scope
├── constraints
├── required_capabilities
├── expected_deliverables
├── completion_criteria
├── priority
├── clarification_history
├── authorization_snapshot
├── admission_decision
└── trace_metadata
```

Cuando una misión se refina, no se sobrescribe la CMS. Se genera una versión nueva.

---

## 5.6 Execution

Representa el trabajo técnico realizado para avanzar o resolver una Mission.

Responde:

> ¿Cómo estamos resolviendo este problema?

Una Mission puede generar varias Executions por:

- reintento;
- refinamiento;
- nuevas restricciones;
- replanificación;
- cambio parcial de alcance;
- recuperación.

---

## 5.7 Execution Context

Representa el conocimiento operativo vivo de una Execution.

Es un activo gobernado, no una estructura de escritura libre.

```text
Execution Context
├── execution_id
├── mission_id
├── cms_version
├── requester_context_reference
├── current_state
├── plan_reference
├── active_constraints
├── capability_resolutions
├── context_views
├── validated_results
├── evidence_references
├── confidence_references
├── warnings
├── limitations
├── validity_metadata
├── trace_references
└── context_version
```

Ningún motor cognitivo puede escribir directamente en el Execution Context oficial.

---

## 5.8 Context View

Vista mínima, controlada y específica del Execution Context entregada a un motor para ejecutar una tarea.

---

## 5.9 Cognitive Task Package — CTP

Contrato de entrada de un motor.

```text
Cognitive Task Package
├── task_id
├── execution_id
├── mission_id
├── capability_required
├── implementation_selected
├── context_view
├── task_objective
├── constraints
├── priority
├── timeout
├── retry_policy
├── contract_version
└── trace_metadata
```

---

## 5.10 Cognitive Task Result — CTR

Contrato de salida de un motor.

```text
Cognitive Task Result
├── task_id
├── execution_id
├── mission_id
├── producer_id
├── producer_version
├── status
├── payload
├── evidence_references
├── local_confidence
├── warnings
├── limitations
├── metrics
├── completed_at
├── contract_version
└── trace_metadata
```

Un CTR no modifica directamente el Context ni ordena la siguiente tarea.

---

## 5.11 Cognitive Response

Contrato de salida orientado al usuario o canal consumidor.

```text
Cognitive Response
├── response_id
├── mission_id
├── execution_id
├── summary
├── findings
├── recommendations
├── evidence
├── confidence
├── limitations
├── next_actions
├── references
├── attachments
├── requested_output_format
├── channel_profile
└── trace_id
```

---

# 6. Componentes CORE

# 6.1 ACS-001 — Cognitive Runtime Kernel

## Misión

Coordinar el ciclo completo de una interacción cognitiva sin realizar trabajo cognitivo especializado.

## Responsabilidad principal

Gobernar el avance de las Missions y Executions mediante decisiones, comandos, eventos, estados y políticas.

## Activo protegido

La integridad operativa del Runtime.

## Hace

- recibe decisiones de admisión;
- autoriza el registro de Executions;
- coordina readiness;
- solicita planificación;
- emite comandos;
- valida eventos;
- gobierna transiciones;
- decide continuidad;
- coordina recuperación;
- determina cierre;
- inicia completion.

## Nunca hace

- análisis especializado;
- interpretación estratégica;
- cálculo de confianza;
- lectura de documentos;
- modificación directa del Context;
- invocación directa de motores;
- selección técnica de implementaciones.

## Analogía operativa

El Kernel es el **director-capataz**: no ejecuta la chamba especializada; organiza, verifica, coordina y confirma el cierre.

---

# 6.2 ACS-002 — Cognitive Request Gateway

## Misión

Aislar al Runtime de la diversidad tecnológica de los canales externos.

## Responsabilidad principal

Recibir, validar, normalizar y preservar solicitudes externas para producir un Canonical Cognitive Request.

## Activo protegido

La frontera de entrada del Runtime.

## Hace

- recibe solicitudes;
- valida contratos, tamaño y formato;
- conserva el payload original;
- registra canal y metadatos;
- genera `request_id` y `correlation_id`;
- conserva referencias a adjuntos;
- inicia trazabilidad;
- entrega la solicitud canónica a Admission.

## Nunca hace

- interpretar intención;
- leer adjuntos;
- autorizar;
- crear Missions;
- crear Executions;
- consultar motores;
- construir respuestas estratégicas.

---

# 6.3 ACS-003 — Cognitive Admission Manager

## Misión

Convertir una solicitud técnicamente válida en una misión cognitivamente admitida, rechazada o sujeta a clarificación.

## Responsabilidad principal

Ejecutar el Cognitive Admission Protocol.

## Activo protegido

La calidad semántica y operativa de las misiones que ingresan al Runtime.

## Hace

- identifica al solicitante;
- resuelve rol y permisos;
- interpreta intención;
- identifica objetivo operativo y estratégico;
- determina si existe continuidad de misión;
- solicita aclaración;
- identifica capacidades requeridas;
- evalúa reutilización;
- construye o versiona la CMS;
- produce la Admission Decision.

## Nunca hace

- registrar Executions;
- coordinar motores;
- construir planes;
- modificar Context;
- generar recomendaciones;
- decidir contenido estratégico.

## Decisiones posibles

```text
ADMITTED
REJECTED
CLARIFICATION_REQUIRED
DEFERRED
REUSED
CONTINUE_MISSION
REFINE_MISSION
REPLAN_MISSION
CREATE_NEW_MISSION
CLOSE_MISSION
```

---

# 6.4 ACS-004 — Execution Lifecycle Manager

## Misión

Materializar y administrar la existencia formal de una Execution.

## Responsabilidad principal

Crear, identificar, registrar, versionar y cerrar administrativamente las Executions.

## Activo protegido

El expediente administrativo de la Execution.

## Hace

- genera `execution_id`;
- registra la Execution;
- vincula Request, Session, Mission y CMS;
- establece el estado inicial;
- administra relaciones padre-hija;
- registra reintentos y reutilización;
- persiste versiones administrativas;
- ejecuta el cierre administrativo autorizado;
- publica eventos de ciclo de vida.

## Nunca hace

- decidir admisión;
- autorizar una Execution;
- planificar;
- coordinar motores;
- modificar conocimiento;
- determinar cierre cognitivo.

---

# 6.5 ACS-005 — Execution Context Manager

## Misión

Custodiar el conocimiento operativo vivo de una Execution.

## Responsabilidad principal

Administrar, versionar y exponer de manera controlada el Execution Context.

## Activo protegido

El Context oficial de la Execution.

## Hace

- inicializa Context;
- versiona;
- construye Context Views;
- valida actualizaciones autorizadas;
- registra vigencia;
- conserva trazabilidad de cambios;
- evita mezcla de ejecuciones;
- aplica mínimo contexto;
- identifica conocimiento vigente, obsoleto o afectado.

## Nunca hace

- interpretar resultados;
- decidir qué resultado es correcto;
- planificar;
- coordinar motores;
- generar recomendaciones;
- aceptar escrituras directas de motores.

---

# 6.6 ACS-006 — Cognitive Scheduler

## Misión

Transformar una Cognitive Mission en un plan ordenado de tareas ejecutables.

## Responsabilidad principal

Administrar dependencias, prioridades y condiciones de ejecución.

## Activo protegido

El Execution Plan.

## Hace

- construye el DAG de tareas;
- define dependencias;
- identifica paralelismo;
- prioriza;
- replanifica;
- determina readiness de tareas;
- evalúa si el plan puede avanzar;
- declara plan completado.

## Nunca hace

- ejecutar tareas;
- hablar directamente con motores;
- interpretar contenido técnico;
- modificar Context;
- seleccionar implementaciones concretas;
- coordinar transportes.

---

# 6.7 ACS-007 — Task Dispatcher

## Misión

Entregar el trabajo correcto a una implementación autorizada de la capacidad requerida.

## Responsabilidad principal

Materializar el despacho de tareas.

## Activo protegido

La distribución controlada de trabajo.

## Hace

- recibe tareas listas;
- consulta el Capability Registry;
- selecciona implementación conforme a políticas;
- construye CTP;
- envía tareas;
- controla timeout y retry operativo;
- recibe CTR;
- publica resultados y fallos.

## Nunca hace

- construir el plan;
- priorizar misiones;
- interpretar resultados;
- modificar Context;
- decidir continuidad global;
- evaluar estrategia.

---

# 6.8 ACS-008 — Capability Registry

## Misión

Mantener el directorio oficial de capacidades cognitivas y sus implementaciones disponibles.

## Responsabilidad principal

Resolver capacidades hacia implementaciones compatibles.

## Activo protegido

El catálogo oficial de capacidades.

## Estructura conceptual

```text
Capability
├── capability_id
├── name
├── contract_version
├── implementations[]
│   ├── implementation_id
│   ├── version
│   ├── status
│   ├── health
│   ├── endpoint
│   ├── latency
│   ├── cost_profile
│   ├── restrictions
│   └── supported_contracts
└── governance_metadata
```

## Hace

- registra capacidades;
- registra implementaciones;
- valida compatibilidad;
- informa disponibilidad;
- informa versiones y restricciones;
- soporta selección por política.

## Nunca hace

- ejecutar tareas;
- planificar;
- coordinar;
- interpretar resultados;
- decidir estrategia.

---

# 6.9 ACS-009 — Cognitive Event Bus

## Misión

Transportar eventos entre componentes autorizados de manera desacoplada.

## Responsabilidad principal

Publicar, entregar y soportar consumo confiable de eventos.

## Activo protegido

La comunicación desacoplada.

## Hace

- recibe eventos;
- valida estructura básica;
- entrega a consumidores;
- soporta correlación;
- permite deduplicación e idempotencia;
- conserva orden cuando la política lo exige.

## Nunca hace

- interpretar eventos;
- decidir continuidad;
- modificar Context;
- producir conocimiento;
- coordinar componentes.

---

# 6.10 ACS-010 — Response Composer

## Misión

Transformar el resultado cognitivo en una respuesta clara, útil, accionable y adaptada al usuario.

## Responsabilidad principal

Componer la representación final sin alterar el conocimiento estratégico.

## Activo protegido

La comunicación entre HEYTI y el usuario.

## Hace

- recibe estado final, evidencia, confianza y limitaciones;
- adapta profundidad, tono y formato;
- conserva trazabilidad;
- construye Cognitive Response;
- produce salida para canal o API.

## Nunca hace

- analizar datos;
- calcular confianza;
- generar estrategia;
- modificar evidencia;
- ocultar limitaciones;
- inventar contenido.

---

# 6.11 ACS-011 — Runtime Configuration

## Misión

Centralizar la configuración operativa del Runtime.

## Responsabilidad principal

Cargar, validar, versionar y exponer configuración por ambiente.

## Activo protegido

La configuración oficial del Runtime.

## Contiene

- timeouts;
- retries;
- prioridades;
- concurrencia;
- políticas;
- límites;
- feature flags;
- capacidades habilitadas;
- versiones;
- parámetros por ambiente.

## Nunca hace

- lógica cognitiva;
- coordinación;
- decisiones de negocio;
- persistencia de conocimiento;
- planificación.

---

# 7. Contratos del Runtime

## 7.1 Reglas generales

Todo contrato deberá:

- poseer identidad;
- estar versionado;
- ser inmutable;
- incluir trazabilidad;
- incluir contexto de seguridad;
- incluir `correlation_id`;
- incluir `causation_id` cuando corresponda;
- validar esquema;
- permitir compatibilidad evolutiva.

## 7.2 Contratos fundamentales

| Contrato | Productor | Consumidor principal |
|---|---|---|
| Canonical Cognitive Request | Gateway | Admission Manager |
| Admission Decision | Admission Manager | Kernel |
| Cognitive Mission Specification | Admission Manager | Kernel / Scheduler |
| Execution Registration Command | Kernel | Lifecycle Manager |
| Execution Record | Lifecycle Manager | Kernel / Context Manager |
| Execution Plan | Scheduler | Kernel / Dispatcher |
| Cognitive Task Package | Dispatcher | Motor |
| Cognitive Task Result | Motor | Dispatcher / Kernel |
| Context Update Command | Kernel | Context Manager |
| Context View | Context Manager | Dispatcher / Motor |
| Cognitive Response | Response Composer | Gateway / Channel Adapter |
| Completion Command | Kernel | Lifecycle / Completion services |

---

# 8. Eventos y comunicaciones

## 8.1 Catálogo inicial de eventos

```text
REQUEST_RECEIVED
REQUEST_NORMALIZED
ADMISSION_STARTED
CLARIFICATION_REQUIRED
MISSION_ADMITTED
MISSION_REJECTED
MISSION_REFINED
EXECUTION_AUTHORIZED
EXECUTION_REGISTERED
READINESS_STARTED
EXECUTION_READY
PLAN_CREATED
PLAN_UPDATED
TASK_READY
TASK_DISPATCHED
TASK_COMPLETED
TASK_FAILED
CONTEXT_UPDATED
RESPONSE_READY
MISSION_COMPLETED
MISSION_PARTIALLY_COMPLETED
MISSION_SUSPENDED
MISSION_CANCELLED
MISSION_FAILED
EXECUTION_CLOSED
CONFIGURATION_LOADED
CONFIGURATION_UPDATED
```

## 8.2 Contrato mínimo de evento

```text
Cognitive Event
├── event_id
├── event_type
├── event_version
├── request_id
├── mission_id
├── execution_id
├── task_id
├── correlation_id
├── causation_id
├── producer_id
├── producer_version
├── occurred_at
├── payload
├── idempotency_key
├── security_context
└── trace_metadata
```

## 8.3 Reglas

- Los motores publican hechos; no ordenan continuidad.
- El Kernel gobierna la transición.
- Los eventos no sustituyen contratos.
- Todo evento debe ser compatible con el estado actual.
- Todo evento debe ser idempotente o deduplicable.
- Los eventos deberán estar versionados.

---

# 9. Políticas de gobierno

## 9.1 Execution Completion Policy

Estados terminales oficiales:

```text
MISSION_COMPLETED
MISSION_PARTIALLY_COMPLETED
MISSION_FAILED
MISSION_CANCELLED
MISSION_SUSPENDED
```

### Completed

Se cumplieron los criterios de finalización de la CMS.

### Partially Completed

Existe una respuesta útil, pero hay limitaciones materiales documentadas.

### Failed

No fue posible producir un resultado confiable o recuperable.

### Cancelled

El usuario o una política autorizada canceló la misión.

### Suspended

La misión espera una condición externa.

El Kernel determina el estado cognitivo terminal. El Lifecycle Manager materializa el cierre administrativo.

---

## 9.2 Communication Policy

Cada componente deberá declarar:

- con quién puede comunicarse;
- qué contrato utiliza;
- qué eventos publica;
- qué eventos consume;
- qué comunicaciones están prohibidas.

Interacciones prohibidas principales:

- Gateway → motores;
- motores → Context directo;
- motores → Scheduler;
- motores → otros motores;
- Admission → Dispatcher;
- Scheduler → implementación concreta;
- Response Composer → modificación de evidencia.

---

## 9.3 Clarification Policy

Cuando la misión no pueda formularse con suficiente claridad:

1. se suspende la admisión;
2. se genera una pregunta de clarificación;
3. se conserva la sesión y el Request;
4. no se crea Execution;
5. se reanuda Admission al recibir respuesta.

---

## 9.4 Retry Policy

Orden preferente:

```text
Retry
→ Alternate Implementation
→ Replan
→ Degrade
→ Suspend
→ Human Escalation
→ Cancel
```

Los detalles cuantitativos se definirán por Runtime Configuration.

---

## 9.5 Context Update Policy

- Ningún motor escribe directamente.
- Todo CTR se registra.
- El Kernel evalúa readiness y continuidad, no veracidad técnica.
- El Context Manager aplica actualizaciones autorizadas.
- Toda actualización genera versión y trazabilidad.
- Las vistas se generan bajo mínimo contexto.

---

## 9.6 Mission Continuity Policy

Una nueva intervención puede producir:

- continuidad sin cambio;
- refinamiento;
- replanificación;
- nueva Execution;
- nueva Mission;
- cierre;
- clarificación.

El criterio principal es si cambia el objetivo de fondo o únicamente las restricciones.

---

# 10. Matriz de Componentes del Runtime

| ACS | Componente | Clasificación | Misión | Activo protegido | Consume | Produce | Nunca hace |
|---|---|---:|---|---|---|---|---|
| ACS-001 | Cognitive Runtime Kernel | CORE | Coordinar el Runtime | Integridad operativa | Admission Decision, eventos, estados | Comandos, decisiones, cierre | Razonar |
| ACS-002 | Cognitive Request Gateway | CORE | Normalizar entrada | Frontera externa | Solicitudes externas | Canonical Request | Interpretar intención |
| ACS-003 | Cognitive Admission Manager | CORE | Construir misión admitida | Calidad de admisión | Canonical Request | CMS, Admission Decision | Ejecutar |
| ACS-004 | Execution Lifecycle Manager | CORE | Registrar ciclo administrativo | Expediente de Execution | Autorización | Execution Record | Coordinar |
| ACS-005 | Execution Context Manager | CORE | Custodiar Context | Conocimiento vivo oficial | Updates autorizados | Context Views, versiones | Interpretar |
| ACS-006 | Cognitive Scheduler | CORE | Planificar trabajo | Execution Plan | CMS, Context, eventos | Plan, tareas ready | Ejecutar |
| ACS-007 | Task Dispatcher | CORE | Entregar trabajo | Distribución | Task Ready, Registry | CTP, eventos | Planificar |
| ACS-008 | Capability Registry | CORE | Resolver capacidades | Catálogo oficial | Registro y queries | Implementaciones compatibles | Ejecutar |
| ACS-009 | Cognitive Event Bus | CORE | Transportar eventos | Desacoplamiento | Eventos | Entrega | Decidir |
| ACS-010 | Response Composer | CORE | Comunicar resultado | Respuesta al usuario | Resultado, evidencia, confianza | Cognitive Response | Razonar |
| ACS-011 | Runtime Configuration | CORE | Centralizar configuración | Configuración oficial | Archivos, variables | Config validada | Lógica |

---

# 11. Flujo end-to-end

```text
Usuario / Sistema externo
        ↓
Channel Adapter
        ↓
Cognitive Request Gateway
        ↓
Canonical Cognitive Request
        ↓
Cognitive Admission Manager
        ├── identidad
        ├── permisos
        ├── intención
        ├── objetivo
        ├── clarificación
        ├── continuidad
        └── capacidades
        ↓
Cognitive Mission Specification
        ↓
Cognitive Runtime Kernel
        ↓
Execution Authorization
        ↓
Execution Lifecycle Manager
        ↓
Execution Registered
        ↓
Execution Context Manager
        ↓
Context Initialized
        ↓
Cognitive Scheduler
        ↓
Execution Plan
        ↓
Task Dispatcher
        ↓
Capability Registry
        ↓
Cognitive Task Package
        ↓
Motor especializado
        ↓
Cognitive Task Result
        ↓
Event Bus
        ↓
Kernel
        ├── valida evento
        ├── actualiza progreso
        ├── evalúa readiness
        └── ordena continuidad
        ↓
Execution Context Manager
        ↓
Context Updated
        ↓
Scheduler / siguientes tareas
        ↓
Completion Criteria Satisfied
        ↓
Response Composer
        ↓
Cognitive Response
        ↓
Canal de salida
        ↓
Usuario
        ↓
Cognitive Completion
        ↓
Execution Closed
```

---

# 12. Clasificación CORE, FOUNDATION y EVOLUCIÓN

## 12.1 CORE

Sin estos elementos el Runtime no puede operar correctamente:

- Kernel;
- Gateway;
- Admission Manager;
- CMS;
- Lifecycle Manager;
- Context Manager;
- Scheduler;
- Dispatcher;
- Capability Registry;
- Event Bus;
- Response Composer;
- Runtime Configuration;
- CTP;
- CTR;
- Completion Policy;
- Communication Policy;
- Clarification Policy.

## 12.2 FOUNDATION

Elementos necesarios para una implementación profesional, aunque no representen lógica cognitiva central:

- persistencia de estados;
- auditoría compartida;
- versionado contractual;
- logging estructurado;
- manejo de secretos;
- pruebas de contratos;
- control de concurrencia;
- feature flags.

## 12.3 EVOLUCIÓN

- Runtime Health Monitor;
- Capability Marketplace;
- Mission Validation Loop;
- Execution Reuse avanzado;
- aprendizaje adaptativo;
- priorización dinámica;
- optimización automática de planes;
- autoajuste de presupuestos;
- ejecución multi-región;
- orquestación multiagente.

---

# 13. Registro de PDA aprobadas

| PDA | Decisión | Estado |
|---|---|---|
| PDA-001 | Cognitive Scheduler | Aprobada |
| PDA-002 | Task Dispatcher | Aprobada |
| PDA-003 | Cognitive Event Bus | Aprobada |
| PDA-004 | Catálogo inicial de Runtime Events | Aprobada |
| PDA-005 | Motor Registry | Sustituida |
| PDA-005A | Capability Registry | Aprobada |
| PDA-006 | Response Composer | Aprobada |
| PDA-007 | Execution Completion Policy | Aprobada |
| PDA-008 | Runtime Health Monitor | Diferida a Evolución |
| PDA-009 | Runtime Configuration | Aprobada |
| PDA-010 | Runtime Security & Governance / Communication Policy | Aprobada |

---

# 14. Auditoría arquitectónica de Fase A

## 14.1 Alcance

La auditoría revisó:

- responsabilidades;
- dependencias;
- gobierno;
- flujo;
- contratos;
- escalabilidad;
- vacíos estructurales;
- duplicidades;
- acoplamiento;
- capacidad de implementación.

## 14.2 Resultado

| Severidad | Hallazgos |
|---|---:|
| Críticos | 0 |
| Mayores | 0 |
| Menores | 3 |

## 14.3 Hallazgos menores

### A-001 — Versionado obligatorio de eventos

Todo evento deberá incluir `event_version`.

**Estado:** Aceptado.  
**Implementación:** FOUNDATION.

### A-002 — Inmutabilidad contractual

CMS, CTP, CTR, Cognitive Response y eventos deberán ser inmutables.

**Estado:** Aceptado.  
**Implementación:** CORE/FOUNDATION.

### A-003 — Auditoría compartida

Todos los componentes deberán emitir evidencia hacia un mecanismo común de auditoría.

**Estado:** Aceptado.  
**Implementación:** FOUNDATION.

## 14.4 Dictamen

El Runtime Core es:

- consistente;
- desacoplado;
- gobernado;
- implementable;
- extensible;
- defendible;
- apto para avanzar a la siguiente fase.

---

# 15. Riesgos y anti-patrones

## 15.1 God Kernel

El Kernel acumula lógica de negocio, persistencia, planificación o análisis.

**Mitigación:** contratos, managers especializados y auditoría de responsabilidad.

## 15.2 Gateway inteligente

El Gateway interpreta intención o procesa documentos.

**Mitigación:** normalización sin interpretación.

## 15.3 Motores coordinándose

Un motor llama a otro.

**Mitigación:** Event Bus + Kernel + Scheduler + Dispatcher.

## 15.4 Escritura directa al Context

Motores modifican el Context.

**Mitigación:** Context Update Policy.

## 15.5 Scheduler ejecutor

El Scheduler despacha o ejecuta.

**Mitigación:** separación con Dispatcher.

## 15.6 Dispatcher planificador

El Dispatcher decide dependencias o prioridades.

**Mitigación:** Execution Plan como contrato.

## 15.7 Silencio ante ambigüedad

HEYTI adivina intención.

**Mitigación:** Honestidad Cognitiva y Clarification Policy.

## 15.8 Cierre técnico prematuro

Se declara completada una misión porque terminó el último motor.

**Mitigación:** Completion Criteria de la CMS.

## 15.9 Reutilización textual

Se reutiliza una respuesta solo porque la pregunta coincide.

**Mitigación:** Request Fingerprint contextual.

## 15.10 Acoplamiento a motores

El Runtime conoce implementaciones.

**Mitigación:** Capability Registry.

---

# 16. Criterios de aceptación de Fase A

La Fase A se considera completada cuando:

- cada responsabilidad principal tiene dueño;
- cada componente tiene límites explícitos;
- el Kernel no ejecuta trabajo cognitivo;
- Admission está separado de Execution;
- Session, Request, Mission y Execution están diferenciados;
- existe CMS;
- existen CTP y CTR;
- el Context está gobernado;
- los motores no se invocan entre sí;
- las capacidades están desacopladas de implementaciones;
- el flujo tiene estados terminales;
- existe Communication Policy;
- existe Completion Policy;
- los contratos son versionables e inmutables;
- la auditoría no reporta hallazgos críticos o mayores.

**Resultado:** Cumplido.

---

# 17. Decisiones diferidas

## 17.1 Runtime Health Monitor

Se conserva para una fase posterior de observabilidad avanzada.

## 17.2 Mission Validation Loop

Validará si la misión resolvió realmente la necesidad del usuario.

## 17.3 Execution Reuse avanzado

Reutilización semántica con vigencia, permisos, datos, políticas y confianza.

## 17.4 Capability Marketplace

Registro dinámico y descubrimiento avanzado de capacidades.

## 17.5 Cognitive Orchestrator / Cognitive Kernel Layer

Hallazgo diferido previamente registrado: antes de implementar el runtime cognitivo y antes de codificar la orquestación del MIT, evaluar si conviene introducir una capa dedicada exclusivamente a coordinar motores cognitivos, manteniendo al MIT enfocado solo en razonamiento estratégico.

## 17.6 Uncertainty Reduction Plan

Evolución del Confidence Engine para identificar brechas de evidencia y proponer acciones de adquisición de datos.

## 17.7 Emergent Strategic Evidence

Evolución del Evidence Fusion Engine para producir evidencia estratégica emergente derivada de múltiples evidencias HES.

## 17.8 Mission Validation y Problem Resolution Rate

Medición futura de si la interacción resolvió realmente el problema del usuario.

---

# 18. Estrategia temporal de implementación

HEYTI deberá mantener dos vías coordinadas:

## Vía 1 — HEYTI-CORE

Continúa con rigor arquitectónico, contratos, trazabilidad, confianza, evidencia y seguridad.

## Vía 2 — Capacidad Operativa de Campaña

Cuando el CORE alcance madurez suficiente, podrá liberarse un MVP controlado para misiones prioritarias:

- priorización municipal;
- priorización seccional;
- diagnóstico de estructura;
- recomendación de arranque;
- asignación de recursos;
- explicación con evidencia y confianza.

El MVP no deberá deformar ni interrumpir el desarrollo del CORE.

---

# 19. Cierre de Fase A

La Fase A del Sprint 9.4 queda formalmente completada.

El Runtime Cognitivo HEYTI dispone de:

- un modelo operativo;
- entidades diferenciadas;
- componentes CORE;
- contratos fundamentales;
- políticas de gobierno;
- eventos iniciales;
- una matriz de responsabilidades;
- una auditoría arquitectónica satisfactoria;
- un backlog de evolución controlado.

La base queda preparada para iniciar la siguiente fase documental y técnica sin reinterpretar la arquitectura.

> **No construimos componentes por anticipación. Las responsabilidades descubren los componentes.**

> **Cada quien haga su chamba.**

> **Primero comprender; después construir.**

> **La base debe ser a prueba de balas; lo demás brotará de manera natural.**

---

# Anexo A — Comunicación autorizada resumida

| Componente | Puede comunicarse con |
|---|---|
| Gateway | Channel Adapters, Admission Manager |
| Admission Manager | Gateway, Identity/Policy services, Kernel |
| Kernel | Admission, Lifecycle, Context, Scheduler, Dispatcher, Event Bus, Response Composer, Configuration |
| Lifecycle Manager | Kernel, persistencia, Event Bus |
| Context Manager | Kernel, Scheduler, Dispatcher, persistencia |
| Scheduler | Kernel, Context Manager, Dispatcher |
| Dispatcher | Scheduler, Capability Registry, motores, Event Bus |
| Capability Registry | Dispatcher, Configuration |
| Event Bus | Productores y consumidores autorizados |
| Response Composer | Kernel, Context Manager, canales de salida |
| Runtime Configuration | Componentes autorizados en modo lectura |

---

# Anexo B — Preguntas de control para revisión de código

Antes de aceptar una implementación:

1. ¿Esta función pertenece realmente a este componente?
2. ¿El componente está invadiendo la responsabilidad de otro?
3. ¿La comunicación está autorizada?
4. ¿El contrato está versionado?
5. ¿La operación es trazable?
6. ¿El estado puede recuperarse?
7. ¿Existe escritura directa al Context?
8. ¿Existe invocación directa entre motores?
9. ¿La misión ambigua se clarifica?
10. ¿El cierre cumple los criterios de la CMS?
11. ¿La implementación depende de una capacidad o de un motor concreto?
12. ¿La respuesta conserva evidencia, confianza y limitaciones?

---

# Fin del documento
