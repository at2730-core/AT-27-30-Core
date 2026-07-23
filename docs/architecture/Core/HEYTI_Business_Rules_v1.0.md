# HEYTI Business Rules v1.0

## Libro Oficial de Reglas de Negocio de HEYTI Platform

**Código del documento:** HBR-001  
**Versión:** 1.0  
**Estado:** En revision de certificacion  
**Clasificación:** Documento Normativo de Arquitectura y Negocio  
**Dominio:** HEYTI Platform  
**Responsable:** Dirección de Arquitectura y Proyecto HEYTI  
**Fecha de inicio:** 2026-07-22  

---

## Referencias Normativas

La evolución de las Business Rules contenidas en este documento se regirá por lo establecido en:

- ADR-011 — Política de Evolución Arquitectónica de HEYTI.

# Control Documental

| Campo | Valor |
|---|---|
| Documento | HEYTI Business Rules |
| Código | HBR-001 |
| Clasificación | Documento Normativo de Arquitectura y Negocio |
| Estado | En revision de certificacion |
| Versión | 1.0 |
| Fecha de emisión | *(Completar al aprobar la versión oficial)* |
| Proyecto | HEYTI Platform |
| Propietario del documento | Arquitectura HEYTI |
| Responsable de mantenimiento | Arquitecto de Plataforma |
| Documento relacionado | Arquitectura Cognitiva HEYTI |
| Documento relacionado | Arquitectura Runtime Cognitivo |
| Documento relacionado | HEYTI Domain Model |
| Documento relacionado | HEYTI Knowledge System (HKS) |
| Documento relacionado | HEYTI Construction Blueprint (HCB) |
| Documento relacionado | Architecture Decision Records (ADR) |

---

# Gestión de Versiones

## Política de Versionado

El HEYTI Business Rules utilizará versionado mayor y menor conforme a los siguientes criterios:

| Versión | Significado |
|---|---|
| 1.x | Ajustes editoriales, aclaraciones, incorporación o refinamiento de reglas sin modificación estructural del modelo general. |
| 2.x | Cambios significativos en la clasificación, autoridad, aplicación o interpretación de las reglas de negocio. |
| 3.x o superior | Evoluciones mayores del modelo normativo o del gobierno de reglas de HEYTI. |

---

# Historial de Versiones

| Versión | Fecha | Descripción | Responsable |
|---|---|---|---|
| 0.1 | 2026-07-22 | Creación de la estructura inicial del documento | Arquitectura HEYTI |
| 1.0 | *(Completar al aprobar oficialmente)* | Primera versión oficial del Libro de Reglas de Negocio | Arquitectura HEYTI |

---

# Estado del Documento

Los estados oficiales del documento son:

- Borrador
- En elaboración
- En revisión
- Aprobado
- Vigente
- Obsoleto
- Archivado

La portada deberá indicar claramente el estado vigente.

---

# 1. Introducción

## 1.1 Propósito

El **HEYTI Business Rules —HBR—** establece el conjunto oficial de reglas de negocio que gobiernan el comportamiento, las decisiones, las validaciones, las restricciones y las capacidades de HEYTI Platform.

Su propósito es consolidar en una única fuente normativa las reglas que determinan:

- qué condiciones deben cumplirse;
- qué comportamientos están permitidos;
- qué restricciones no pueden ser vulneradas;
- qué decisiones puede ejecutar la plataforma;
- qué información requiere validación;
- qué relaciones deben preservarse;
- y qué principios deben respetar los componentes de software.

El HBR no define código fuente ni especificaciones técnicas de implementación.

Define las reglas que el código deberá implementar.

---

## 1.2 Objetivo general

Establecer una fuente única, trazable y verificable de reglas de negocio para HEYTI Platform, de manera que toda implementación, validación, automatización, recomendación o decisión estratégica pueda relacionarse con una regla formalmente documentada.

El documento deberá permitir que cada regla pueda vincularse con:

- un dominio;
- una entidad o capacidad;
- un activo arquitectónico de origen;
- una condición de aplicación;
- una consecuencia;
- un nivel de obligatoriedad;
- y uno o más componentes de software responsables de su implementación.

---

## 1.3 Problema que resuelve

Las reglas de negocio pueden quedar dispersas entre documentos arquitectónicos, decisiones técnicas, modelos de dominio, procesos operativos o código fuente.

Cuando esto ocurre, aumenta el riesgo de:

- interpretaciones contradictorias;
- duplicidad de lógica;
- comportamiento inconsistente;
- reglas ocultas dentro del código;
- pérdida de trazabilidad;
- decisiones no justificadas;
- validaciones incompletas;
- y dependencia excesiva del conocimiento tácito de los desarrolladores.

El HBR reduce estos riesgos mediante la consolidación, clasificación, identificación y gobierno formal de las reglas.

---

## 1.4 Alcance

El HEYTI Business Rules comprende:

1. Principios rectores de negocio.
2. Reglas fundamentales del sistema.
3. Reglas por dominio.
4. Reglas cognitivas.
5. Reglas de evidencia.
6. Reglas de confianza.
7. Reglas de explicabilidad.
8. Reglas de integridad y trazabilidad.
9. Reglas operativas.
10. Reglas de gobierno y evolución.
11. Criterios de identificación y versionado.
12. Relaciones entre reglas, activos y componentes.

El HBR no contiene:

- código fuente;
- especificaciones de clases;
- algoritmos detallados;
- configuraciones de infraestructura;
- instrucciones de despliegue;
- interfaces gráficas;
- ni decisiones tecnológicas no aprobadas.

---

## 1.5 Fuente de autoridad

Las reglas registradas en este documento deberán derivarse de activos arquitectónicos y documentales aprobados, entre ellos:

- Arquitectura Cognitiva HEYTI;
- Arquitectura Runtime Cognitivo;
- HEYTI Domain Model;
- HEYTI Knowledge System (HKS);
- Motor de Inteligencia Territorial (MIT);
- Motor de Evidencias;
- Modelo ADN Territorial;
- Architecture Decision Records (ADR);
- HEYTI Construction Blueprint (HCB);
- y documentos oficiales de los dominios funcionales.

Cuando una regla no pueda vincularse con una fuente reconocida, deberá identificarse como propuesta pendiente de validación y no podrá considerarse vigente.

---

## 1.6 Principio rector

> **Ninguna regla crítica de HEYTI podrá existir únicamente dentro del código fuente.**

Toda regla crítica deberá:

1. documentarse;
2. identificarse;
3. aprobarse;
4. vincularse con su fuente arquitectónica;
5. implementarse;
6. probarse;
7. y conservar evidencia de su cumplimiento.

El código será una implementación de las reglas.

Las reglas no dependerán del código para existir.

---

## 1.7 Principio de autoridad normativa

Cuando exista contradicción entre:

- una interpretación informal;
- una implementación técnica;
- una configuración operativa;
- y una regla aprobada en el HBR;

prevalecerá la regla aprobada, salvo que haya sido modificada formalmente mediante el proceso de gobierno correspondiente.

Cuando una regla contradiga un activo arquitectónico de mayor autoridad, la discrepancia deberá resolverse antes de su implementación.

---

## 1.8 Principio de trazabilidad

Toda regla deberá permitir reconstruir:

- su origen;
- su propósito;
- el dominio al que pertenece;
- la condición que la activa;
- la decisión o restricción que establece;
- el componente que la implementa;
- la prueba que verifica su cumplimiento;
- y la evidencia de su aplicación.

Una regla sin trazabilidad no podrá considerarse completamente gobernada.

---

## 1.9 Principio de claridad

Las reglas deberán redactarse de forma:

- precisa;
- verificable;
- no ambigua;
- consistente;
- independiente de tecnologías específicas;
- y comprensible para perfiles técnicos y no técnicos.

Las reglas no deberán redactarse como aspiraciones generales cuando su cumplimiento deba ser comprobable.

---

## 1.10 Principio de estabilidad

Los identificadores de las reglas serán permanentes.

Cuando una regla sea modificada, sustituida u obsoleta:

- no se reutilizará su identificador;
- se conservará su historial;
- se documentará la razón del cambio;
- y se registrará la regla que la sustituya, cuando corresponda.

---

## 1.11 Principio de aplicabilidad

Toda regla deberá indicar claramente:

- cuándo aplica;
- sobre qué entidad, proceso o capacidad actúa;
- qué condición evalúa;
- qué decisión produce;
- qué consecuencia genera;
- y qué excepciones admite, si existen.

Las reglas demasiado generales deberán dividirse cuando contengan más de una decisión verificable.

---

## 1.12 Resultado esperado

Al concluir la versión 1.0, HEYTI contará con un Libro Oficial de Reglas de Negocio que permita:

- implementar componentes sin reinterpretar el dominio;
- validar comportamientos de forma objetiva;
- construir el Rule Engine sobre una fuente formal;
- relacionar reglas con pruebas;
- auditar decisiones;
- preservar la coherencia entre arquitectura y software;
- y reducir la dependencia del conocimiento informal.

---

# 2. Convenciones del Documento

## 2.1 Acrónimos oficiales

| Acrónimo | Significado |
|---|---|
| ADR | Architecture Decision Record |
| HBR | HEYTI Business Rules |
| HCB | HEYTI Construction Blueprint |
| HKS | HEYTI Knowledge System |
| MIT | Motor de Inteligencia Territorial |
| BR | Business Rule |
| CORE | Núcleo central de capacidades de HEYTI |
| EVD | Evidencia |
| CNF | Confianza |
| EXP | Explicabilidad |

Todo acrónimo deberá escribirse con su significado completo entre paréntesis en su primera aparición.

---

## 2.2 Convención de identificadores

Cada regla tendrá un identificador permanente con la siguiente estructura:

`BR-[DOMINIO]-[NÚMERO]`

Ejemplos:

- `BR-CORE-001`
- `BR-TER-001`
- `BR-ELE-001`
- `BR-SOC-001`
- `BR-EVD-001`
- `BR-CNF-001`
- `BR-EXP-001`
- `BR-SYS-001`

El número será correlativo dentro de cada familia.

---

## 2.3 Familias iniciales de reglas

| Código | Familia |
|---|---|
| CORE | Reglas fundamentales del núcleo |
| SYS | Reglas generales del sistema |
| TER | Reglas territoriales |
| ELE | Reglas electorales |
| SOC | Reglas socioeconómicas |
| CAP | Reglas de capital territorial |
| OPS | Reglas de operación territorial |
| RSK | Reglas de riesgo y seguridad |
| INT | Reglas de inteligencia territorial |
| PRD | Reglas de productos de inteligencia |
| ADM | Reglas administrativas |
| EVD | Reglas de evidencia |
| CNF | Reglas de confianza |
| EXP | Reglas de explicabilidad |
| MEM | Reglas de memoria y contexto |
| GOV | Reglas de gobierno y evolución |

La incorporación de nuevas familias deberá documentarse formalmente.

---

## 2.4 Estructura oficial de una regla

Cada regla deberá documentarse con los siguientes campos:

| Campo | Descripción |
|---|---|
| ID | Identificador permanente |
| Nombre | Título breve de la regla |
| Dominio | Familia o dominio al que pertenece |
| Estado | Propuesta, aprobada, vigente, obsoleta o sustituida |
| Prioridad | Crítica, alta, media o baja |
| Fuente | Activo arquitectónico o documento de origen |
| Enunciado | Regla expresada de forma normativa |
| Condición | Situación que activa la regla |
| Acción o restricción | Comportamiento obligatorio |
| Resultado esperado | Consecuencia verificable |
| Excepciones | Excepciones permitidas |
| Implementación | Componentes responsables |
| Prueba | Evidencia requerida para verificarla |
| Observaciones | Información complementaria |

---

## 2.5 Plantilla oficial de regla


ID:
Nombre:
Dominio:
Estado:
Prioridad:
Fuente:

Enunciado:

Condición:

Acción o restricción:

Resultado esperado:

Excepciones:

Componentes responsables:

Criterio de prueba:

Observaciones:

# 3. Modelo de Gobierno de las Reglas de Negocio

## 3.1 Objetivo

El Modelo de Gobierno de las Reglas de Negocio establece el proceso oficial mediante el cual las reglas de HEYTI son propuestas, evaluadas, aprobadas, implementadas, verificadas, modificadas y retiradas.

Su propósito es asegurar que las reglas evolucionen de manera controlada, preservando la coherencia arquitectónica y evitando interpretaciones inconsistentes entre la documentación y la implementación.

---

## 3.2 Principios del Gobierno

El gobierno de las reglas se fundamenta en los siguientes principios:

### Autoridad

Toda regla deberá contar con una fuente documental reconocida.

No se admitirán reglas cuya única justificación sea una decisión de implementación.

---

### Trazabilidad

Toda regla deberá poder relacionarse con:

- un activo arquitectónico;
- un documento oficial;
- uno o más componentes de software;
- una evidencia de validación.

---

### Evolución Controlada

Las reglas podrán evolucionar conforme madure la plataforma.

Toda modificación deberá quedar registrada y justificarse documentalmente.

---

### Transparencia

Las reglas vigentes deberán permanecer accesibles para todos los integrantes del proyecto.

No existirán reglas "implícitas" conocidas únicamente por determinados desarrolladores.

---

## 3.3 Ciclo de Vida de una Regla

Toda regla recorrerá el siguiente ciclo de vida:

1. Propuesta
2. Análisis
3. Validación Arquitectónica
4. Aprobación
5. Implementación
6. Verificación
7. Vigencia
8. Evolución o Retiro

Cada transición deberá quedar documentada.

---

## 3.4 Estados Oficiales

Las reglas podrán encontrarse en alguno de los siguientes estados:

| Estado | Descripción |
|---------|-------------|
| Propuesta | La regla ha sido identificada pero aún no ha sido aprobada. |
| En revisión | La regla está siendo evaluada técnica y arquitectónicamente. |
| Aprobada | La regla ha sido aceptada como parte oficial del HBR. |
| Implementada | Existe una implementación de software que la satisface. |
| Verificada | Se cuenta con evidencia de cumplimiento. |
| Vigente | La regla continúa siendo aplicable. |
| Sustituida | Fue reemplazada por otra regla. |
| Obsoleta | Dejó de ser aplicable, pero se conserva por trazabilidad. |

---

## 3.5 Autoridad de las Reglas

Cuando exista conflicto entre varias reglas, prevalecerá el siguiente orden de autoridad:

1. Arquitectura Cognitiva HEYTI.
2. Architecture Decision Records (ADR).
3. HEYTI Business Rules (HBR).
4. HEYTI Domain Model.
5. HEYTI Construction Blueprint (HCB).
6. Engineering Book.
7. Implementación de software.

Si una implementación contradice una regla vigente del HBR, deberá corregirse la implementación o iniciarse formalmente un proceso de modificación de la regla.

---

## 3.6 Modificación de una Regla

Toda modificación deberá registrar, como mínimo:

- identificador de la regla;
- versión afectada;
- motivo del cambio;
- impacto esperado;
- documentos relacionados;
- responsable;
- fecha;
- evidencia de aprobación.

Cuando el cambio afecte principios arquitectónicos, deberá emitirse el ADR correspondiente.

---

## 3.7 Sustitución de Reglas

Cuando una regla sustituya a otra:

- la regla original conservará su identificador;
- se marcará como "Sustituida";
- se indicará la nueva regla que la reemplaza;
- ambas permanecerán registradas para mantener la trazabilidad histórica.

---

## 3.8 Eliminación de Reglas

Las reglas no deberán eliminarse físicamente del documento.

Cuando dejen de ser aplicables, cambiarán su estado a:

**Obsoleta**

y conservarán:

- su identificador;
- su historial;
- la justificación de su retiro.

---

## 3.9 Resultado Esperado

El Modelo de Gobierno permitirá que las reglas evolucionen junto con HEYTI sin perder coherencia, trazabilidad ni autoridad normativa.

Cada cambio quedará documentado y podrá reconstruirse históricamente, fortaleciendo la gobernanza del conocimiento de la plataforma.


---

# PARTE I  
# LEYES FUNDAMENTALES DE HEYTI

## Declaración Institucional

Las Leyes Fundamentales de HEYTI constituyen el conjunto de principios normativos que gobiernan el comportamiento esencial de la plataforma.

A diferencia de las reglas de negocio específicas de cada dominio, estas leyes representan principios transversales que deberán respetarse en cualquier componente, proceso, motor cognitivo o evolución futura de HEYTI.

Las Leyes Fundamentales tienen como propósito preservar la identidad arquitectónica de la plataforma y garantizar que su evolución mantenga coherencia con los principios sobre los cuales fue diseñada.

Toda capacidad implementada deberá ser compatible con estas leyes.

Cuando exista conflicto entre una regla de negocio específica y una Ley Fundamental, prevalecerá la Ley Fundamental.

Las Leyes Fundamentales constituyen el nivel normativo superior dentro del HEYTI Business Rules (HBR).

---

## Jerarquía Normativa de HEYTI

La normativa oficial de HEYTI se organiza conforme a la siguiente jerarquía:

1. Leyes Fundamentales de HEYTI.
2. Reglas de Negocio.
3. Políticas Operativas.
4. Procedimientos de Implementación.
5. Código Fuente.

Ningún nivel inferior podrá contradecir a un nivel superior.

Toda modificación a una Ley Fundamental requerirá una revisión arquitectónica formal y la emisión del correspondiente **Architecture Decision Record (ADR)** cuando implique cambios en la arquitectura de referencia.

---

## Alcance de las Leyes Fundamentales

Las Leyes Fundamentales son de cumplimiento obligatorio para:

- todos los módulos de HEYTI;
- todos los motores cognitivos;
- todos los servicios internos;
- todos los procesos de razonamiento;
- todas las recomendaciones estratégicas;
- todas las futuras capacidades incorporadas a la plataforma.

Su vigencia es permanente y únicamente podrán modificarse mediante el proceso oficial de gobierno arquitectónico.


# 4. Reglas Fundamentales del CORE

## 4.1 Introducción

Las Reglas Fundamentales del CORE constituyen el conjunto de principios normativos que gobiernan el comportamiento esencial de HEYTI Platform.

Estas reglas son transversales a todos los dominios funcionales y deberán ser respetadas por cualquier componente, servicio, motor cognitivo o módulo operativo de la plataforma.

Su incumplimiento comprometería la coherencia arquitectónica del sistema.

---

### Relación entre las Leyes Fundamentales y las Business Rules del CORE

Las **Leyes Fundamentales de HEYTI (LAW)** representan los principios normativos superiores que rigen el comportamiento de toda la plataforma.

Las **Business Rules del CORE (BR-CORE)** constituyen la operacionalización verificable de dichas leyes, definiendo las condiciones de cumplimiento, los componentes responsables y los criterios de validación necesarios para garantizar su aplicación.

En caso de existir una discrepancia entre una Business Rule del CORE y una Ley Fundamental, **prevalecerá siempre la Ley Fundamental**, debiendo actualizarse la regla correspondiente mediante el proceso oficial de gobernanza documental.


# BR-CORE-001

## Nombre

La arquitectura gobierna a la implementación.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

- Arquitectura Cognitiva HEYTI
- ADR-009
- Runtime Cognitivo

### Enunciado

Toda implementación de software deberá derivarse de la arquitectura previamente aprobada.

No podrán implementarse capacidades cuya definición arquitectónica no exista.

### Condición

Siempre.

### Acción

La implementación deberá respetar la arquitectura vigente.

### Resultado esperado

La plataforma conservará coherencia entre diseño e implementación.

### Excepciones

Ninguna.

### Componentes responsables

Todos.

### Criterio de prueba

Toda funcionalidad implementada deberá poder vincularse con un activo arquitectónico aprobado.

---

# BR-CORE-002

## Nombre

Toda decisión estratégica deberá ser explicable.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

- Runtime Cognitivo
- Motor de Inteligencia Territorial (MIT)

### Enunciado

HEYTI no podrá emitir recomendaciones estratégicas que no puedan justificarse mediante evidencia documentada y una cadena de razonamiento verificable.

### Condición

Cuando el sistema genere una recomendación.

### Acción

Registrar evidencia, razonamiento y nivel de confianza.

### Resultado esperado

Toda recomendación será auditable.

### Excepciones

Ninguna.

### Componentes responsables

MIT
Evidence Engine
Confidence Engine
Explainability Engine

### Criterio de prueba

Toda recomendación deberá generar un expediente de explicación.

---

# BR-CORE-003

## Nombre

La evidencia precede a la conclusión.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

ADR-010

Motor de Evidencias

### Enunciado

Ninguna conclusión estratégica podrá construirse sin evidencia suficiente para sustentarla.

### Condición

Durante cualquier proceso de razonamiento.

### Acción

Evaluar previamente la disponibilidad y calidad de la evidencia.

### Resultado esperado

Las conclusiones estarán sustentadas documentalmente.

### Excepciones

Ninguna.

### Componentes responsables

Evidence Engine

MIT

Confidence Engine

### Criterio de prueba

Cada conclusión deberá vincularse con las evidencias utilizadas.

---

# BR-CORE-004

## Nombre

La incertidumbre deberá declararse explícitamente.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Confidence Engine

### Enunciado

Cuando la evidencia disponible no sea suficiente, HEYTI deberá informar el nivel de incertidumbre asociado a la recomendación.

Nunca deberá ocultarse la incertidumbre.

### Condición

Cuando el nivel de confianza no alcance el umbral definido.

### Acción

Mostrar el nivel de confianza e identificar los factores que lo afectan.

### Resultado esperado

El usuario comprenderá las limitaciones de la recomendación.

### Excepciones

Ninguna.

### Componentes responsables

Confidence Engine

### Criterio de prueba

Las recomendaciones con confianza inferior al umbral deberán incluir explicación de incertidumbre.

---

# BR-CORE-005

## Nombre

Toda decisión deberá conservar trazabilidad.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Cognitiva

Runtime

Domain Model

### Enunciado

Toda decisión generada por HEYTI deberá permitir reconstruir completamente el proceso que condujo a ella.

### Condición

Siempre.

### Acción

Registrar:

- solicitud;
- contexto;
- evidencia;
- reglas aplicadas;
- razonamiento;
- confianza;
- resultado.

### Resultado esperado

Cada decisión será completamente auditable.

### Excepciones

Ninguna.

### Componentes responsables

Runtime Cognitivo

Knowledge System

Evidence Engine

MIT

### Criterio de prueba

Toda decisión deberá poder reconstruirse íntegramente mediante los registros almacenados.

---

# BR-CORE-006

## Nombre

El conocimiento nunca sustituye a la evidencia.

### Estado

Vigente

### Prioridad

Alta

### Fuente

HEYTI Knowledge System (HKS)

### Enunciado

El conocimiento almacenado en el HKS podrá orientar el razonamiento, pero no reemplazará la evidencia requerida para sustentar una conclusión estratégica.

### Condición

Cuando exista conocimiento previo aplicable al caso analizado.

### Acción

Utilizar el conocimiento como contexto y validar las conclusiones con evidencia vigente.

### Resultado esperado

Las decisiones combinarán conocimiento acumulado y evidencia actual.

### Excepciones

Ninguna.

### Componentes responsables

HKS

Evidence Engine

MIT

### Criterio de prueba

Toda conclusión deberá distinguir explícitamente entre conocimiento reutilizado y evidencia utilizada.

# 4.2 Leyes Fundamentales de HEYTI

Las siguientes leyes constituyen el nivel normativo superior de HEYTI Platform.

Toda arquitectura, componente, motor cognitivo, proceso operativo, algoritmo, implementación de software y evolución futura deberá respetarlas.

Su incumplimiento constituye una desviación arquitectónica que deberá corregirse antes de considerarse válida cualquier implementación.

---

# LAW-001
## Ley de Primacía Arquitectónica

### Declaración

La arquitectura gobierna la implementación.

Toda capacidad desarrollada para HEYTI deberá derivarse de una definición arquitectónica previamente aprobada.

Ninguna implementación podrá introducir comportamientos que contradigan la arquitectura oficial de la plataforma.

### Fundamentación

La estabilidad de HEYTI depende de mantener una relación unidireccional:

Arquitectura → Ingeniería → Implementación

Nunca en sentido inverso.

### Implicaciones

- Ningún desarrollador podrá definir comportamiento de negocio desde el código.
- Todo componente deberá poder relacionarse con un activo arquitectónico.
- Toda excepción requerirá una decisión arquitectónica formal.

### Activos relacionados

- Arquitectura Cognitiva
- ADR-009
- Runtime Cognitivo
- HCB

---

# LAW-002
## Ley de Explicabilidad

### Declaración

Toda decisión estratégica generada por HEYTI deberá poder explicarse.

No existirán recomendaciones cuyo razonamiento no pueda reconstruirse posteriormente.

### Fundamentación

La inteligencia territorial requiere transparencia para generar confianza institucional.

### Implicaciones

- Toda recomendación deberá conservar evidencia.
- Toda recomendación deberá conservar razonamiento.
- Toda recomendación deberá registrar nivel de confianza.
- Toda recomendación deberá poder auditarse.

### Activos relacionados

- Runtime Cognitivo
- MIT
- Explainability Engine

---

# LAW-003
## Ley de Primacía de la Evidencia

### Declaración

La evidencia precede a toda conclusión.

Ninguna conclusión estratégica podrá emitirse sin evidencia suficiente que la sustente.

### Fundamentación

La inteligencia territorial debe construirse sobre hechos verificables y no sobre suposiciones.

### Implicaciones

- La evidencia deberá validarse antes del razonamiento.
- La calidad de la evidencia influirá en el nivel de confianza.
- La ausencia de evidencia deberá declararse explícitamente.

### Activos relacionados

- ADR-010
- Evidence Engine
- Confidence Engine

---

# LAW-004
## Ley de Declaración de la Incertidumbre

### Declaración

Toda incertidumbre deberá comunicarse explícitamente.

HEYTI nunca ocultará las limitaciones de una recomendación.

### Fundamentación

Una confianza incorrectamente comunicada representa un riesgo mayor que una confianza baja correctamente declarada.

### Implicaciones

- Mostrar nivel de confianza.
- Mostrar factores limitantes.
- Mostrar información faltante cuando corresponda.

### Activos relacionados

- Confidence Engine

---

# LAW-005
## Ley de la Trazabilidad Total

### Declaración

Toda decisión deberá poder reconstruirse completamente.

### Fundamentación

Cada recomendación deberá conservar la cadena completa de razonamiento.

### Implicaciones

La plataforma deberá registrar:

- solicitud;
- contexto;
- evidencia utilizada;
- reglas aplicadas;
- razonamiento;
- confianza;
- resultado.

### Activos relacionados

- Runtime Cognitivo
- HKS
- MIT

---

# LAW-006
## Ley de Complementariedad entre Conocimiento y Evidencia

### Declaración

El conocimiento orienta.

La evidencia demuestra.

Ninguno sustituye al otro.

### Fundamentación

El conocimiento acumulado proporciona contexto.

La evidencia valida la situación específica analizada.

### Implicaciones

Toda recomendación deberá distinguir claramente:

- conocimiento reutilizado;
- evidencia utilizada;
- inferencias generadas.

### Activos relacionados

- HKS
- Evidence Engine
- MIT


# PARTE II
# REGLAS DE NEGOCIO DE HEYTI

## Declaración

Las Reglas de Negocio de HEYTI constituyen el conjunto de disposiciones normativas que regulan el comportamiento operativo de la plataforma dentro de cada dominio funcional.

A diferencia de las Leyes Fundamentales, las Reglas de Negocio describen condiciones específicas de operación, validación, restricción, decisión o comportamiento que deberán implementarse en los distintos componentes de software.

Las Reglas de Negocio podrán evolucionar conforme evolucione la plataforma, siempre que dicha evolución no contradiga las Leyes Fundamentales de HEYTI ni los principios arquitectónicos aprobados.

---

### LAW-007 — Ley de Integridad del Conocimiento

Todo conocimiento utilizado por HEYTI deberá conservar su integridad semántica, estructural y contextual durante todo su ciclo de vida.

Ningún componente podrá alterar, reinterpretar o degradar el significado de un conocimiento sin que dicho cambio quede explícitamente registrado, versionado y trazable.

La integridad del conocimiento constituye un requisito obligatorio para garantizar la consistencia del razonamiento cognitivo, la interoperabilidad entre componentes y la confiabilidad de las recomendaciones generadas por HEYTI.

# 5. Estructura del Catálogo de Reglas de Negocio

## 5.1 Objetivo

El Catálogo de Reglas de Negocio organiza todas las reglas oficiales de HEYTI en familias temáticas, permitiendo su identificación, trazabilidad, mantenimiento y evolución.

Cada familia agrupa reglas pertenecientes a un mismo dominio funcional y constituye una unidad lógica de gobierno dentro del HEYTI Business Rules (HBR).

---

## 5.2 Organización General

Las reglas de negocio se organizan conforme a la siguiente estructura:

| Capítulo | Familia | Prefijo |
|-----------|----------|----------|
| 6 | Reglas Generales del Sistema | BR-SYS |
| 7 | Reglas Territoriales | BR-TER |
| 8 | Reglas Electorales | BR-ELE |
| 9 | Reglas Socioeconómicas | BR-SOC |
| 10 | Reglas del Capital Territorial | BR-CAP |
| 11 | Reglas de Operación Territorial | BR-OPS |
| 12 | Reglas de Riesgo y Seguridad | BR-RSK |
| 13 | Reglas del Motor de Evidencias | BR-EVD |
| 14 | Reglas del Motor de Confianza | BR-CNF |
| 15 | Reglas de Explicabilidad | BR-EXP |
| 16 | Reglas del Knowledge System | BR-MEM |
| 17 | Reglas de Gobierno y Evolución | BR-GOV |

Cada familia mantiene su propia numeración independiente.

---

## 5.3 Organización Interna

Cada familia podrá subdividirse en categorías funcionales.

Ejemplo:

BR-SYS

- Runtime
- Sesiones
- Persistencia
- Auditoría
- Versionado
- Configuración

BR-TER

- Secciones
- Municipios
- Distritos
- Geometría
- Cobertura Territorial

BR-ELE

- Procesos Electorales
- Partidos Políticos
- Resultados
- Participación Ciudadana
- Competitividad Electoral

Esta organización permitirá mantener un crecimiento ordenado del catálogo.

---

## 5.4 Principio de Extracción

Las reglas de negocio no deberán redactarse de manera aislada.

Toda regla incorporada al HBR deberá derivarse de uno o más activos arquitectónicos previamente aprobados.

El HBR consolida reglas existentes; no crea comportamiento nuevo.

Las fuentes autorizadas incluyen, entre otras:

- Arquitectura Cognitiva HEYTI.
- Runtime Cognitivo.
- HEYTI Domain Model.
- HEYTI Knowledge System (HKS).
- Motor de Inteligencia Territorial (MIT).
- Architecture Decision Records (ADR).
- HEYTI Construction Blueprint (HCB).
- Engineering Workspace.
- Documentación oficial de dominios funcionales.

Cuando una nueva necesidad funcional requiera una regla inédita, ésta deberá incorporarse primero al proceso de gobierno arquitectónico antes de registrarse como regla vigente.

---

## 5.5 Principio de Trazabilidad Documental

Cada regla deberá mantener, como mínimo, las siguientes relaciones:

- Documento de origen.
- Dominio funcional.
- Componente responsable de implementarla.
- Casos de prueba asociados.
- Ley Fundamental relacionada (cuando aplique).
- ADR relacionado (cuando exista).
- Evidencia de validación.

Esta trazabilidad permitirá reconstruir completamente el origen y la evolución de cada regla.

---

## 5.6 Relación con la Implementación

Las reglas documentadas en el HBR constituyen la especificación normativa para el desarrollo del software.

La implementación deberá cumplir las reglas; las reglas no dependerán de la implementación.

Cuando una implementación requiera modificar una regla, deberá iniciarse previamente el proceso formal de actualización del HBR.

---

## 5.7 Resultado Esperado

Al finalizar este documento, HEYTI dispondrá de un Catálogo Maestro de Reglas de Negocio completamente organizado, trazable y alineado con la arquitectura oficial de la plataforma.

Cada componente del sistema podrá identificar con precisión qué reglas debe implementar y qué activos arquitectónicos justifican su comportamiento.


# 6. Reglas Generales del Sistema (BR-SYS)

## 6.1 Introducción

Las Reglas Generales del Sistema establecen el comportamiento operativo común que deberá respetar toda la plataforma HEYTI.

Estas reglas son independientes del dominio funcional y gobiernan aspectos transversales como la gestión de solicitudes, sesiones, contexto, ejecución, persistencia, auditoría y control operativo del Runtime Cognitivo.

Las reglas de esta familia derivan principalmente de la Arquitectura Runtime Cognitivo y de los Architecture Decision Records (ADR) relacionados.

---

# BR-SYS-001

## Nombre

Toda solicitud deberá ejecutarse dentro de una sesión cognitiva.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

- Arquitectura Runtime Cognitivo
- ADR-009

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Toda solicitud procesada por HEYTI deberá ejecutarse dentro de una sesión cognitiva formalmente identificada.

No existirán procesos cognitivos fuera del contexto de una sesión.

### Condición

Siempre que el Runtime reciba una nueva solicitud.

### Acción

El Runtime deberá:

- crear una nueva sesión o
- reutilizar una sesión vigente cuando corresponda.

Toda ejecución deberá quedar asociada a un identificador único de sesión.

### Resultado esperado

Cada proceso cognitivo podrá reconstruirse completamente mediante su sesión correspondiente.

### Componentes responsables

- Runtime Cognitivo
- Session Manager

### Criterio de prueba

Toda recomendación, análisis o respuesta deberá contener un Session ID válido asociado al proceso que la originó.

### Observaciones

Esta regla garantiza la trazabilidad completa del ciclo de vida de cada solicitud procesada por HEYTI.


## 6.2 Reglas Derivadas de los Principios Rectores del Runtime

Las siguientes reglas derivan directamente de los principios arquitectónicos establecidos en la Arquitectura del Runtime Cognitivo HEYTI.

Su propósito es transformar dichos principios en especificaciones normativas implementables y verificables dentro del software.

---

# BR-SYS-002

## Nombre

Responsabilidad única de los componentes.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 3.1 — Principio de Responsabilidad Delimitada

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Todo componente del Runtime deberá poseer una responsabilidad principal claramente definida y no deberá asumir responsabilidades asignadas a otros componentes.

### Condición

Siempre.

### Acción

Cada componente implementará únicamente las funciones correspondientes a su misión arquitectónica.

### Resultado esperado

Se preservará la separación de responsabilidades y el bajo acoplamiento entre componentes.

### Componentes responsables

Todos los componentes CORE del Runtime.

### Criterio de prueba

Durante revisiones de arquitectura y código no deberá identificarse un componente ejecutando responsabilidades pertenecientes a otro.

---

# BR-SYS-003

## Nombre

Clarificación obligatoria ante ambigüedad.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Secciones 3.2 y 3.3

### Ley Fundamental relacionada

LAW-002 — Ley de Explicabilidad

### Enunciado

Cuando una solicitud admita múltiples interpretaciones plausibles, HEYTI deberá solicitar clarificación antes de iniciar cualquier ejecución cognitiva.

### Condición

Solicitud ambigua.

### Acción

Suspender el proceso de admisión y generar una solicitud de clarificación.

### Resultado esperado

No existirán ejecuciones iniciadas sobre misiones ambiguas.

### Componentes responsables

Cognitive Admission Manager.

Cognitive Runtime Kernel.

### Criterio de prueba

Toda Execution deberá estar asociada a una misión previamente admitida y libre de ambigüedad significativa.

---

# BR-SYS-004

## Nombre

Identidad obligatoria de toda Cognitive Mission.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 3.4

### Ley Fundamental relacionada

LAW-005 — Ley de la Trazabilidad Total

### Enunciado

Toda Cognitive Mission deberá poseer una identidad propia e independiente de las solicitudes y ejecuciones utilizadas para resolverla.

### Condición

Creación de una nueva misión.

### Acción

Asignar un identificador único y permanente a la misión.

### Resultado esperado

Las misiones podrán rastrearse independientemente de las ejecuciones que las conforman.

### Componentes responsables

Cognitive Admission Manager.

Execution Lifecycle Manager.

### Criterio de prueba

No deberán existir dos misiones diferentes compartiendo el mismo identificador.

---

# BR-SYS-005

## Nombre

Continuidad del diálogo.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 3.5

### Ley Fundamental relacionada

LAW-005 — Ley de la Trazabilidad Total

### Enunciado

Toda nueva intervención del usuario deberá evaluarse dentro del contexto de la sesión, la misión activa y el historial conversacional antes de tratarse como una solicitud independiente.

### Condición

Recepción de una nueva intervención.

### Acción

Evaluar continuidad semántica y estratégica con la misión existente.

### Resultado esperado

El diálogo conservará coherencia durante toda la interacción.

### Componentes responsables

Cognitive Admission Manager.

Runtime Kernel.

### Criterio de prueba

Las solicitudes relacionadas deberán vincularse con la misión correspondiente cuando exista continuidad demostrable.

## 6.3 Reglas Derivadas del Modelo Operativo General

Las siguientes reglas derivan del Capítulo 4 de la Arquitectura del Runtime Cognitivo HEYTI y norman el ciclo de vida obligatorio de toda interacción cognitiva.

---

# BR-SYS-006

## Nombre

Toda solicitud deberá seguir el ciclo oficial del Runtime.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 4 — Modelo Operativo General

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Toda solicitud admitida deberá recorrer exclusivamente las fases oficiales definidas por el Runtime Cognitivo.

### Condición

Toda interacción aceptada por el sistema.

### Acción

Ejecutar secuencialmente las fases de Cognitive Admission, Cognitive Execution y Cognitive Completion.

### Resultado esperado

Todas las misiones seguirán un flujo uniforme, gobernado y auditable.

### Componentes responsables

Cognitive Runtime Kernel.

### Criterio de prueba

No deberá existir ninguna Execution que omita una fase obligatoria del ciclo de vida definido por el Runtime.

---

# BR-SYS-007

## Nombre

Prohibición de iniciar una Execution sin Admission.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 4.1 — Cognitive Admission

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Ninguna Execution podrá iniciarse sin que exista previamente una Cognitive Mission admitida mediante el proceso oficial de Admission.

### Condición

Solicitud recibida.

### Acción

Completar el protocolo de Admission antes de autorizar cualquier Execution.

### Resultado esperado

Toda Execution tendrá una Mission válida y una decisión formal de admisión.

### Componentes responsables

Cognitive Admission Manager.

Cognitive Runtime Kernel.

### Criterio de prueba

Cada Execution deberá estar vinculada a una Admission Decision válida y a una CMS vigente.

---

# BR-SYS-008

## Nombre

La Admission deberá resolver los elementos mínimos de una misión.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 4.1 — Cognitive Admission

### Ley Fundamental relacionada

LAW-002 — Ley de Explicabilidad

### Enunciado

Toda Cognitive Admission deberá identificar, como mínimo, la identidad del solicitante, el objetivo operativo, el objetivo estratégico, la intención, las capacidades requeridas y la decisión de admisión.

### Condición

Proceso de Admission.

### Acción

Construir una Cognitive Mission Specification completa antes de autorizar la ejecución.

### Resultado esperado

La misión dispondrá de toda la información necesaria para su correcta ejecución.

### Componentes responsables

Cognitive Admission Manager.

### Criterio de prueba

No deberá existir una CMS que omita alguno de los elementos mínimos definidos por la arquitectura.

---

# BR-SYS-009

## Nombre

La Execution deberá realizarse únicamente sobre una misión autorizada.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 4.2 — Cognitive Execution

### Ley Fundamental relacionada

LAW-005 — Ley de la Trazabilidad Total

### Enunciado

Toda Execution deberá encontrarse asociada a una Cognitive Mission previamente autorizada y registrada.

### Condición

Inicio de Execution.

### Acción

Registrar formalmente la Execution antes de iniciar cualquier tarea cognitiva.

### Resultado esperado

Existirá correspondencia uno a uno entre la Execution activa y la misión que la originó.

### Componentes responsables

Execution Lifecycle Manager.

Runtime Kernel.

### Criterio de prueba

Cada Execution deberá conservar referencias válidas a Mission, Session, Request y CMS.

---

# BR-SYS-010

## Nombre

Toda misión deberá concluir mediante un proceso formal de Completion.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 4.3 — Cognitive Completion

### Ley Fundamental relacionada

LAW-005 — Ley de la Trazabilidad Total

### Enunciado

Toda misión deberá finalizar mediante el proceso oficial de Cognitive Completion antes de declararse concluida.

### Condición

Cumplimiento de un estado terminal.

### Acción

Persistir resultados, registrar trazabilidad, liberar recursos, actualizar métricas y publicar el estado terminal.

### Resultado esperado

Toda misión conservará evidencia completa de su cierre.

### Componentes responsables

Cognitive Runtime Kernel.

Execution Lifecycle Manager.

### Criterio de prueba

No deberá existir una misión marcada como completada sin evidencia de su proceso de Completion.


## 6.4 Reglas Derivadas de las Entidades Fundamentales

Las siguientes reglas derivan del Capítulo 5 de la Arquitectura del Runtime Cognitivo HEYTI.

Su propósito es normar la creación, administración, identificación, versionado y relaciones entre las entidades fundamentales del Runtime.

---

# BR-SYS-011

## Nombre

Toda Session deberá representar una continuidad conversacional.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 5.1 — Session

### Ley Fundamental relacionada

LAW-005 — Ley de la Trazabilidad Total

### Enunciado

Toda interacción deberá pertenecer a una Session que represente la continuidad conversacional del usuario.

### Condición

Recepción de una nueva solicitud.

### Acción

Crear una nueva Session o asociar la solicitud a una Session existente.

### Resultado esperado

Toda Request quedará vinculada a una única Session activa.

### Componentes responsables

Cognitive Admission Manager.
Execution Lifecycle Manager.

### Criterio de prueba

No deberá existir ninguna Request sin Session asociada.

---

# BR-SYS-012

## Nombre

Toda Request deberá poseer identidad propia.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 5.2 — Request

### Ley Fundamental relacionada

LAW-005 — Ley de la Trazabilidad Total

### Enunciado

Toda Request deberá poseer un identificador único, aun cuando su contenido sea idéntico al de solicitudes anteriores.

### Condición

Recepción de una solicitud.

### Acción

Generar un request_id único e irrepetible.

### Resultado esperado

Cada intervención será trazable de manera independiente.

### Componentes responsables

Cognitive Request Gateway.

### Criterio de prueba

No deberán existir Request duplicadas compartiendo el mismo identificador.

---

# BR-SYS-013

## Nombre

La equivalencia cognitiva no dependerá del texto.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 5.3 — Request Fingerprint

### Ley Fundamental relacionada

LAW-007 Ley de Integridad del Conocimiento

### Enunciado

La reutilización de conocimiento deberá basarse en el Request Fingerprint y no únicamente en la igualdad textual de la solicitud.

### Condición

Evaluación de reutilización.

### Acción

Comparar la huella contextual definida por la arquitectura.

### Resultado esperado

Se evitará reutilizar respuestas cuando exista diferencia funcional entre solicitudes aparentemente iguales.

### Componentes responsables

Cognitive Admission Manager.

### Criterio de prueba

Las decisiones de reutilización deberán justificarse mediante el Request Fingerprint.

---

# BR-SYS-014

## Nombre

Toda Cognitive Mission deberá representar un problema real.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 5.4 — Cognitive Mission

### Ley Fundamental relacionada

LAW-002 — Ley de Explicabilidad

### Enunciado

Toda Cognitive Mission deberá representar la necesidad real que HEYTI intentará resolver y no únicamente una solicitud textual.

### Condición

Construcción de una nueva Mission.

### Acción

Definir explícitamente el problema a resolver antes de iniciar la ejecución.

### Resultado esperado

Las Executions estarán orientadas a resolver problemas y no únicamente preguntas.

### Componentes responsables

Cognitive Admission Manager.

### Criterio de prueba

Cada Mission deberá documentar el objetivo que justifica su existencia.

---

# BR-SYS-015

## Nombre

Toda CMS deberá ser inmutable.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 5.5 — Cognitive Mission Specification

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Una Cognitive Mission Specification aprobada no podrá modificarse directamente.

### Condición

Refinamiento de una misión.

### Acción

Generar una nueva versión de la CMS conservando el historial.

### Resultado esperado

Toda evolución de una misión será completamente trazable.

### Componentes responsables

Cognitive Admission Manager.

### Criterio de prueba

No deberán existir sobrescrituras directas de una CMS aprobada.


## 6.5 Reglas Contractuales del Runtime

Las siguientes reglas regulan los contratos fundamentales utilizados por el Runtime Cognitivo HEYTI.

Su cumplimiento es obligatorio para garantizar la interoperabilidad, la trazabilidad y la estabilidad evolutiva de la plataforma.

---

# BR-SYS-016

## Nombre

Toda Execution deberá pertenecer a una única Cognitive Mission.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 5.6 — Execution

### Ley Fundamental relacionada

LAW-005 — Ley de la Trazabilidad Total

### Enunciado

Toda Execution deberá encontrarse asociada a una única Cognitive Mission, aun cuando una misma Mission pueda generar múltiples Executions.

### Condición

Registro de una Execution.

### Acción

Vincular obligatoriamente la Execution con la Mission correspondiente.

### Resultado esperado

La trazabilidad entre misión y ejecución permanecerá íntegra durante todo el ciclo de vida.

### Componentes responsables

Execution Lifecycle Manager.

### Criterio de prueba

No deberá existir ninguna Execution sin Mission asociada.

---

# BR-SYS-017

## Nombre

El Execution Context constituye el único contexto oficial de una Execution.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 5.7 — Execution Context

### Ley Fundamental relacionada

LAW-007 Ley de Integridad del Conocimiento

### Enunciado

El Execution Context será el único repositorio oficial del conocimiento operativo vivo de una Execution.

### Condición

Toda Execution activa.

### Acción

Centralizar el estado operativo exclusivamente en el Execution Context gobernado.

### Resultado esperado

Existirá una única fuente oficial de contexto para cada Execution.

### Componentes responsables

Execution Context Manager.

### Criterio de prueba

No deberán existir repositorios paralelos considerados como contexto oficial.

---

# BR-SYS-018

## Nombre

Prohibición de escritura directa sobre el Execution Context.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 5.7 — Execution Context

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Ningún motor cognitivo podrá modificar directamente el Execution Context oficial.

### Condición

Actualización del contexto.

### Acción

Toda modificación deberá realizarse mediante el Execution Context Manager conforme a las políticas autorizadas.

### Resultado esperado

La integridad del contexto permanecerá protegida por el Runtime.

### Componentes responsables

Execution Context Manager.

Cognitive Runtime Kernel.

### Criterio de prueba

Toda actualización del contexto deberá quedar registrada mediante el mecanismo oficial del Runtime.

---

# BR-SYS-019

## Nombre

Toda Context View deberá aplicar el principio de mínimo contexto.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 5.8 — Context View

### Ley Fundamental relacionada

LAW-007 Ley de Integridad del Conocimiento

### Enunciado

Cada motor cognitivo recibirá únicamente la información estrictamente necesaria para ejecutar su responsabilidad.

### Condición

Generación de una Context View.

### Acción

Construir una vista mínima derivada del Execution Context.

### Resultado esperado

Se minimizará el acoplamiento y la exposición innecesaria de información.

### Componentes responsables

Execution Context Manager.

### Criterio de prueba

Las Context Views deberán contener únicamente los elementos requeridos por la capacidad solicitada.

---

# BR-SYS-020

## Nombre

Todo Cognitive Task Package deberá constituir el único contrato de entrada para un motor.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 5.9 — Cognitive Task Package (CTP)

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Todo motor cognitivo deberá recibir exclusivamente un Cognitive Task Package como contrato formal de entrada.

### Condición

Despacho de una tarea.

### Acción

Construir y entregar un CTP completo antes de iniciar la ejecución.

### Resultado esperado

Todos los motores trabajarán bajo un contrato uniforme y verificable.

### Componentes responsables

Task Dispatcher.

### Criterio de prueba

No deberá existir ninguna ejecución de un motor sin un CTP válido.

---

# BR-SYS-021

## Nombre

Todo Cognitive Task Result deberá ser el único contrato de salida de un motor.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 5.10 — Cognitive Task Result (CTR)

### Ley Fundamental relacionada

LAW-005 — Ley de la Trazabilidad Total

### Enunciado

Todo resultado producido por un motor cognitivo deberá entregarse mediante un Cognitive Task Result.

### Condición

Finalización de una tarea.

### Acción

Emitir un CTR conforme al contrato oficial del Runtime.

### Resultado esperado

Todos los resultados serán homogéneos, trazables y auditables.

### Componentes responsables

Motores Cognitivos.

Task Dispatcher.

### Criterio de prueba

No deberán aceptarse resultados producidos fuera del contrato CTR.

---

# BR-SYS-022

## Nombre

La Cognitive Response será el único contrato oficial de salida hacia el usuario.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 5.11 — Cognitive Response

### Ley Fundamental relacionada

LAW-002 — Ley de Explicabilidad

### Enunciado

Toda respuesta entregada al usuario deberá construirse mediante una Cognitive Response conforme al contrato oficial del Runtime.

### Condición

Finalización de una Mission.

### Acción

Generar una Cognitive Response preservando evidencia, confianza, limitaciones y trazabilidad.

### Resultado esperado

Toda salida del Runtime será consistente, explicable y verificable.

### Componentes responsables

Response Composer.

### Criterio de prueba

No deberá existir ninguna respuesta al usuario generada fuera del contrato Cognitive Response.


## 6.6 Reglas de los Componentes CORE

Las siguientes reglas derivan de las responsabilidades, límites y activos protegidos definidos para los componentes CORE del Runtime Cognitivo.

Su finalidad es garantizar la separación de responsabilidades y prevenir violaciones arquitectónicas durante la implementación del HEYTI-CORE.

---

# BR-SYS-023

## Nombre

El Cognitive Runtime Kernel no realizará trabajo cognitivo especializado.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 6.1 — ACS-001 Cognitive Runtime Kernel

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

El Cognitive Runtime Kernel coordinará el ciclo de vida de las Missions y Executions, pero nunca ejecutará razonamiento estratégico, interpretación de evidencia, cálculo de confianza o cualquier otro trabajo cognitivo especializado.

### Condición

Durante la ejecución de cualquier misión.

### Acción

Delegar el trabajo especializado a los motores cognitivos correspondientes.

### Resultado esperado

El Kernel conservará exclusivamente funciones de coordinación y gobierno.

### Componentes responsables

Cognitive Runtime Kernel.

### Criterio de prueba

No deberá existir código de análisis especializado implementado dentro del Kernel.

---

# BR-SYS-024

## Nombre

El Cognitive Request Gateway únicamente normalizará solicitudes.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 6.2 — ACS-002 Cognitive Request Gateway

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

El Gateway recibirá, validará y normalizará solicitudes, pero nunca interpretará intención, construirá Missions o autorizará Executions.

### Condición

Recepción de solicitudes externas.

### Acción

Generar un Canonical Cognitive Request y entregarlo al Admission Manager.

### Resultado esperado

La frontera de entrada permanecerá desacoplada de la lógica cognitiva.

### Componentes responsables

Cognitive Request Gateway.

### Criterio de prueba

El Gateway no deberá contener lógica de interpretación semántica.

---

# BR-SYS-025

## Nombre

El Cognitive Admission Manager será el único componente autorizado para admitir misiones.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 6.3 — ACS-003 Cognitive Admission Manager

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

La admisión, rechazo, clarificación, refinamiento o continuidad de una Mission únicamente podrá ser determinada por el Cognitive Admission Manager.

### Condición

Proceso de Admission.

### Acción

Ejecutar el Cognitive Admission Protocol y emitir una Admission Decision.

### Resultado esperado

Todas las Missions ingresarán al Runtime mediante un proceso uniforme y gobernado.

### Componentes responsables

Cognitive Admission Manager.

### Criterio de prueba

No deberá existir ningún componente distinto autorizando una Mission.

---

# BR-SYS-026

## Nombre

El Execution Lifecycle Manager administrará exclusivamente el ciclo administrativo de las Executions.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 6.4 — ACS-004 Execution Lifecycle Manager

### Ley Fundamental relacionada

LAW-005 — Ley de la Trazabilidad Total

### Enunciado

El Lifecycle Manager administrará el registro, versionado y cierre administrativo de las Executions sin intervenir en decisiones cognitivas.

### Condición

Creación, actualización o cierre de una Execution.

### Acción

Registrar y mantener el expediente administrativo de la Execution.

### Resultado esperado

La administración de Executions permanecerá separada del razonamiento.

### Componentes responsables

Execution Lifecycle Manager.

### Criterio de prueba

El Lifecycle Manager no deberá construir planes ni generar recomendaciones.

---

# BR-SYS-027

## Nombre

El Execution Context Manager será el único custodio del contexto oficial.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 6.5 — ACS-005 Execution Context Manager

### Ley Fundamental relacionada

LAW-007 Ley de Integridad del Conocimiento

### Enunciado

La administración, versionado y exposición del Execution Context corresponderán exclusivamente al Execution Context Manager.

### Condición

Actualización o consulta del contexto.

### Acción

Gestionar el Context mediante los mecanismos oficiales definidos por el Runtime.

### Resultado esperado

La integridad y trazabilidad del conocimiento operativo permanecerán protegidas.

### Componentes responsables

Execution Context Manager.

### Criterio de prueba

Ningún otro componente deberá modificar directamente el Execution Context.

---

# BR-SYS-028

## Nombre

El Cognitive Scheduler será el único responsable de la planificación.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 6.6 — ACS-006 Cognitive Scheduler

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

La planificación, priorización, establecimiento de dependencias y replanificación corresponderán exclusivamente al Cognitive Scheduler.

### Condición

Construcción o modificación del Execution Plan.

### Acción

Generar y mantener el plan oficial de ejecución.

### Resultado esperado

Las decisiones de planificación permanecerán centralizadas.

### Componentes responsables

Cognitive Scheduler.

### Criterio de prueba

Ningún componente distinto deberá modificar el Execution Plan.

---

# BR-SYS-029

## Nombre

El Task Dispatcher será el único responsable del despacho de tareas.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 6.7 — ACS-007 Task Dispatcher

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

El despacho de tareas hacia las implementaciones autorizadas corresponderá exclusivamente al Task Dispatcher.

### Condición

Existencia de una tarea lista para ejecución.

### Acción

Construir el Cognitive Task Package (CTP), resolver la implementación autorizada y entregar la tarea.

### Resultado esperado

Toda tarea será despachada mediante un proceso uniforme, gobernado y trazable.

### Componentes responsables

Task Dispatcher.

### Criterio de prueba

Ningún otro componente deberá enviar tareas directamente a un motor cognitivo.

---

# BR-SYS-030

## Nombre

El Capability Registry será la única fuente oficial de capacidades.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 6.8 — ACS-008 Capability Registry

### Ley Fundamental relacionada

LAW-007 Ley de Integridad del Conocimiento

### Enunciado

Toda resolución entre una capacidad cognitiva y su implementación deberá realizarse mediante el Capability Registry oficial.

### Condición

Resolución de capacidades.

### Acción

Consultar el catálogo oficial antes de seleccionar cualquier implementación.

### Resultado esperado

La implementación permanecerá desacoplada de las capacidades.

### Componentes responsables

Capability Registry.

Task Dispatcher.

### Criterio de prueba

No deberán existir referencias directas desde el Runtime hacia implementaciones específicas.

---

# BR-SYS-031

## Nombre

El Cognitive Event Bus únicamente transportará eventos.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 6.9 — ACS-009 Cognitive Event Bus

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

El Event Bus será responsable exclusivamente del transporte confiable de eventos entre componentes autorizados.

### Condición

Publicación de un evento.

### Acción

Validar la estructura mínima y distribuir el evento a los consumidores autorizados.

### Resultado esperado

La comunicación permanecerá desacoplada del procesamiento de negocio.

### Componentes responsables

Cognitive Event Bus.

### Criterio de prueba

El Event Bus no deberá interpretar eventos ni decidir el flujo del Runtime.

---

# BR-SYS-032

## Nombre

El Response Composer será el único responsable de construir la respuesta final.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 6.10 — ACS-010 Response Composer

### Ley Fundamental relacionada

LAW-002 — Ley de Explicabilidad

### Enunciado

Toda respuesta entregada al usuario deberá construirse mediante el Response Composer sin alterar el conocimiento estratégico producido por los motores.

### Condición

Finalización de una Mission.

### Acción

Componer la Cognitive Response conforme al perfil del usuario y al canal de salida.

### Resultado esperado

La comunicación conservará evidencia, confianza, limitaciones y trazabilidad.

### Componentes responsables

Response Composer.

### Criterio de prueba

No deberán modificarse recomendaciones, evidencia o confianza durante la composición de la respuesta.

---

# BR-SYS-033

## Nombre

La configuración operativa será administrada exclusivamente por Runtime Configuration.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 6.11 — ACS-011 Runtime Configuration

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Los parámetros operativos del Runtime deberán centralizarse en Runtime Configuration y no podrán encontrarse dispersos dentro del código de los componentes.

### Condición

Inicialización o actualización de configuración.

### Acción

Cargar, validar, versionar y exponer la configuración oficial por ambiente.

### Resultado esperado

La operación del Runtime será consistente, configurable y controlada.

### Componentes responsables

Runtime Configuration.

### Criterio de prueba

No deberán existir valores críticos codificados directamente dentro de los componentes CORE.

## 6.7 Reglas Derivadas de los Contratos del Runtime

Las siguientes reglas derivan del Capítulo 7 de la Arquitectura del Runtime Cognitivo HEYTI.

Su propósito es establecer las obligaciones normativas que deberán cumplir todos los contratos intercambiados entre los componentes del Runtime.

---

# BR-SYS-034

## Nombre

Todo contrato deberá poseer identidad única.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 7.1 — Reglas Generales

### Ley Fundamental relacionada

LAW-005 — Ley de la Trazabilidad Total

### Enunciado

Todo contrato utilizado por el Runtime deberá poseer un identificador único que permita su trazabilidad durante todo el ciclo de vida de la misión.

### Condición

Creación de cualquier contrato.

### Acción

Asignar una identidad única e irrepetible.

### Resultado esperado

Todos los contratos serán individualmente identificables.

### Componentes responsables

Todos los componentes productores de contratos.

### Criterio de prueba

No deberán existir contratos sin identificador.

---

# BR-SYS-035

## Nombre

Todo contrato deberá estar versionado.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 7.1

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Todo contrato oficial del Runtime deberá indicar explícitamente su versión.

### Condición

Definición o modificación de un contrato.

### Acción

Registrar la versión correspondiente.

### Resultado esperado

Será posible mantener compatibilidad evolutiva entre versiones.

### Componentes responsables

Todos los productores de contratos.

### Criterio de prueba

No deberá aceptarse un contrato sin versión.

---

# BR-SYS-036

## Nombre

Todo contrato será inmutable.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 7.1

### Ley Fundamental relacionada

LAW-007 Ley de Integridad del Conocimiento

### Enunciado

Una vez emitido, ningún contrato podrá modificarse directamente.

### Condición

Actualización de información contractual.

### Acción

Emitir una nueva versión del contrato.

### Resultado esperado

Se preservará el historial completo de cambios.

### Componentes responsables

Todos los componentes productores.

### Criterio de prueba

No deberán detectarse modificaciones directas sobre contratos emitidos.

---

# BR-SYS-037

## Nombre

Todo contrato deberá incluir trazabilidad.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 7.1

### Ley Fundamental relacionada

LAW-005 — Ley de la Trazabilidad Total

### Enunciado

Todo contrato deberá contener la información necesaria para reconstruir su origen y su recorrido dentro del Runtime.

### Condición

Emisión de cualquier contrato.

### Acción

Incluir los identificadores de trazabilidad definidos por la arquitectura.

### Resultado esperado

Cada contrato podrá relacionarse con la misión, la ejecución y la sesión correspondientes.

### Componentes responsables

Todos los componentes productores.

### Criterio de prueba

Todos los contratos deberán contener información suficiente para auditoría.

---

# BR-SYS-038

## Nombre

Todo contrato deberá superar validación estructural.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 7.1

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Ningún contrato podrá ser aceptado por el Runtime sin cumplir previamente su esquema oficial.

### Condición

Recepción de un contrato.

### Acción

Validar el contrato contra su definición oficial.

### Resultado esperado

Únicamente contratos válidos participarán en el flujo operativo.

### Componentes responsables

Todos los consumidores de contratos.

### Criterio de prueba

Los contratos inválidos deberán rechazarse antes de su procesamiento.

---

# BR-SYS-039

## Nombre

Los contratos fundamentales serán de uso obligatorio.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 7.2 — Contratos Fundamentales

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Las interacciones entre componentes deberán utilizar exclusivamente los contratos fundamentales definidos por la arquitectura.

### Condición

Comunicación entre componentes.

### Acción

Utilizar el contrato oficial correspondiente.

### Resultado esperado

Todas las comunicaciones serán homogéneas y compatibles.

### Componentes responsables

Todos los componentes CORE.

### Criterio de prueba

No deberán existir contratos propietarios o ad hoc fuera del catálogo oficial.

## 6.8 Reglas Derivadas de los Eventos y Comunicaciones

Las siguientes reglas derivan del Capítulo 8 de la Arquitectura del Runtime Cognitivo HEYTI.

Su propósito es regular la comunicación desacoplada entre los componentes CORE mediante eventos gobernados.

---

# BR-SYS-040

## Nombre

Todo evento deberá pertenecer al catálogo oficial del Runtime.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 8.1 — Catálogo inicial de eventos

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Todo evento publicado por el Runtime deberá corresponder a un tipo definido en el catálogo oficial de eventos o en una extensión formalmente versionada.

### Condición

Publicación de un evento.

### Acción

Validar el tipo de evento antes de publicarlo.

### Resultado esperado

El Runtime utilizará exclusivamente eventos oficialmente reconocidos.

### Componentes responsables

Cognitive Event Bus.

Todos los productores de eventos.

### Criterio de prueba

No deberán existir eventos con tipos no registrados en el catálogo oficial.

---

# BR-SYS-041

## Nombre

Todo evento deberá cumplir el contrato mínimo del Runtime.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 8.2 — Contrato mínimo de evento

### Ley Fundamental relacionada

LAW-005 — Ley de la Trazabilidad Total

### Enunciado

Todo evento deberá cumplir el contrato estructural mínimo definido por la arquitectura.

### Condición

Creación de un evento.

### Acción

Incluir todos los campos obligatorios del contrato oficial.

### Resultado esperado

Los eventos serán interoperables, auditables y consistentes.

### Componentes responsables

Todos los productores de eventos.

### Criterio de prueba

No deberá aceptarse un evento que incumpla el contrato mínimo.

---

# BR-SYS-042

## Nombre

Los motores cognitivos únicamente publicarán hechos.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 8.3 — Reglas

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Los motores cognitivos podrán publicar únicamente hechos derivados de su ejecución y nunca instrucciones para controlar el flujo del Runtime.

### Condición

Finalización de una tarea cognitiva.

### Acción

Emitir únicamente eventos descriptivos del resultado obtenido.

### Resultado esperado

La coordinación permanecerá bajo responsabilidad del Kernel.

### Componentes responsables

Motores Cognitivos.

### Criterio de prueba

No deberán existir eventos emitidos por motores que ordenen transiciones del Runtime.

---

# BR-SYS-043

## Nombre

El Kernel será el único responsable de gobernar las transiciones del Runtime.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 8.3 — Reglas

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Las decisiones sobre continuidad, cambio de estado y transición entre fases corresponderán exclusivamente al Cognitive Runtime Kernel.

### Condición

Recepción de eventos.

### Acción

Evaluar el evento y determinar la transición correspondiente.

### Resultado esperado

La lógica de control permanecerá centralizada.

### Componentes responsables

Cognitive Runtime Kernel.

### Criterio de prueba

Ningún componente distinto al Kernel deberá modificar el estado global de una Mission.

---

# BR-SYS-044

## Nombre

Los eventos no sustituirán a los contratos.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 8.3 — Reglas

### Ley Fundamental relacionada

LAW-007 Ley de Integridad del Conocimiento

### Enunciado

Los eventos deberán complementar la comunicación entre componentes, pero nunca reemplazar los contratos oficiales del Runtime.

### Condición

Diseño de una interacción entre componentes.

### Acción

Utilizar el contrato correspondiente cuando la arquitectura así lo establezca.

### Resultado esperado

La comunicación conservará consistencia estructural y semántica.

### Componentes responsables

Todos los componentes CORE.

### Criterio de prueba

No deberán implementarse flujos donde un evento sustituya un contrato obligatorio.

---

# BR-SYS-045

## Nombre

Todo evento deberá ser compatible con el estado actual del Runtime.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 8.3 — Reglas

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Un evento únicamente podrá procesarse si es compatible con el estado actual de la Mission o de la Execution.

### Condición

Recepción de un evento.

### Acción

Validar el estado antes de procesar el evento.

### Resultado esperado

Se evitarán transiciones inconsistentes o inválidas.

### Componentes responsables

Cognitive Runtime Kernel.

### Criterio de prueba

Los eventos incompatibles deberán rechazarse o registrarse como anomalías.

---

# BR-SYS-046

## Nombre

Todo evento deberá ser idempotente o deduplicable.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 8.3 — Reglas

### Ley Fundamental relacionada

LAW-005 — Ley de la Trazabilidad Total

### Enunciado

Todo evento deberá garantizar procesamiento seguro frente a retransmisiones o duplicados.

### Condición

Diseño de un evento.

### Acción

Implementar mecanismos de idempotencia o deduplicación.

### Resultado esperado

El Runtime evitará efectos secundarios por procesamiento repetido.

### Componentes responsables

Cognitive Event Bus.

Productores de eventos.

### Criterio de prueba

El procesamiento repetido del mismo evento no deberá alterar el resultado esperado.

---

# BR-SYS-047

## Nombre

Todo evento deberá estar versionado.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Capítulo 8.3 — Reglas
Auditoría Arquitectónica A-001

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Todo evento publicado por el Runtime deberá indicar explícitamente su versión.

### Condición

Publicación de un evento.

### Acción

Asignar el campo event_version conforme a la versión vigente del contrato.

### Resultado esperado

La evolución del Runtime conservará compatibilidad entre versiones.

### Componentes responsables

Todos los productores de eventos.

### Criterio de prueba

No deberá aceptarse ningún evento sin el campo event_version.

## 6.9 Reglas Derivadas de las Políticas de Gobierno

Las siguientes reglas derivan del Capítulo 9 de la Arquitectura del Runtime Cognitivo HEYTI.

Su propósito es normar las políticas obligatorias que gobiernan el comportamiento operativo del Runtime durante todo el ciclo de vida de una Cognitive Mission.

---

# BR-SYS-048

## Nombre

Toda Mission deberá finalizar mediante un estado terminal oficial.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 9.1 — Execution Completion Policy

### Ley Fundamental relacionada

LAW-005 — Ley de la Trazabilidad Total

### Enunciado

Toda Cognitive Mission deberá concluir utilizando exclusivamente uno de los estados terminales oficiales definidos por la arquitectura.

### Condición

Finalización de una Mission.

### Acción

Asignar uno de los estados terminales autorizados y registrar formalmente el cierre.

### Resultado esperado

Todas las misiones finalizarán de manera uniforme y auditable.

### Componentes responsables

Cognitive Runtime Kernel.
Execution Lifecycle Manager.

### Criterio de prueba

No deberá existir ninguna Mission cerrada con un estado distinto a los definidos oficialmente.

---

# BR-SYS-049

## Nombre

Toda comunicación entre componentes deberá respetar la Communication Policy.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 9.2 — Communication Policy

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Todo componente únicamente podrá comunicarse con los componentes expresamente autorizados por la arquitectura.

### Condición

Interacción entre componentes.

### Acción

Validar la comunicación contra la Communication Policy oficial.

### Resultado esperado

No existirán dependencias no autorizadas.

### Componentes responsables

Todos los componentes CORE.

### Criterio de prueba

Toda comunicación fuera del catálogo autorizado deberá considerarse una violación arquitectónica.

---

# BR-SYS-050

## Nombre

Toda misión ambigua deberá suspender su admisión.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 9.3 — Clarification Policy

### Ley Fundamental relacionada

LAW-002 — Ley de Explicabilidad

### Enunciado

Cuando una misión no pueda formularse con suficiente claridad, el proceso de admisión deberá suspenderse hasta completar la clarificación correspondiente.

### Condición

Ambigüedad significativa.

### Acción

Emitir una solicitud de clarificación y detener temporalmente la admisión.

### Resultado esperado

No se crearán Executions sobre misiones ambiguas.

### Componentes responsables

Cognitive Admission Manager.

### Criterio de prueba

Toda Mission ambigua deberá registrar un estado de clarificación antes de continuar.

---

# BR-SYS-051

## Nombre

La recuperación de fallos seguirá el orden oficial del Runtime.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 9.4 — Retry Policy

### Ley Fundamental relacionada

LAW-001 — Ley de Primacía Arquitectónica

### Enunciado

Los mecanismos de recuperación deberán ejecutarse siguiendo el orden de prioridad definido por la Retry Policy.

### Condición

Fallo durante la ejecución.

### Acción

Aplicar la secuencia Retry → Alternate Implementation → Replan → Degrade → Suspend → Human Escalation → Cancel.

### Resultado esperado

La recuperación será uniforme y gobernada.

### Componentes responsables

Cognitive Runtime Kernel.
Task Dispatcher.
Cognitive Scheduler.

### Criterio de prueba

Las recuperaciones deberán respetar la secuencia oficial definida por la arquitectura.

---

# BR-SYS-052

## Nombre

Toda actualización del Context deberá seguir la Context Update Policy.

### Estado

Vigente

### Prioridad

Crítica

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 9.5 — Context Update Policy

### Ley Fundamental relacionada

LAW-007 Ley de Integridad del Conocimiento

### Enunciado

Toda modificación del Execution Context deberá realizarse exclusivamente mediante el mecanismo oficial de actualización gobernada.

### Condición

Actualización del Context.

### Acción

Registrar el CTR correspondiente y aplicar la actualización mediante el Execution Context Manager.

### Resultado esperado

El Context conservará integridad, versionado y trazabilidad.

### Componentes responsables

Execution Context Manager.
Cognitive Runtime Kernel.

### Criterio de prueba

No deberán detectarse escrituras directas al Context fuera del flujo autorizado.

---

# BR-SYS-053

## Nombre

Toda nueva intervención deberá evaluarse conforme a la Mission Continuity Policy.

### Estado

Vigente

### Prioridad

Alta

### Fuente

Arquitectura Runtime Cognitivo HEYTI
Sección 9.6 — Mission Continuity Policy

### Ley Fundamental relacionada

LAW-002 — Ley de Explicabilidad

### Enunciado

Toda nueva intervención del usuario deberá evaluarse para determinar si continúa, refina, replanifica, reinicia o concluye una Mission existente.

### Condición

Recepción de una nueva intervención.

### Acción

Aplicar la Mission Continuity Policy antes de crear una nueva Mission.

### Resultado esperado

Se preservará la continuidad estratégica del diálogo.

### Componentes responsables

Cognitive Admission Manager.
Cognitive Runtime Kernel.

### Criterio de prueba

No deberán crearse nuevas Missions cuando corresponda continuar una Mission existente.


## Estado del Documento

Nombre:
HEYTI Business Rules (HBR-001)

Versión:
1.0

Clasificacion de Baseline:
BASELINE ARQUITECTÓNICO v1.0

Fuente Normativa:
Runtime Cognitivo HEYTI v1.0

Business Rules Certificadas:
59

Estado Documental:
APROBADO

Modificaciones futuras:
Únicamente mediante ADR aprobado y actualización conforme al ADR-011.

Nivel de certificación:
BA-001 (Pendiente de emisión)

