# ADR-012 — Lenguaje y Plataforma de Implementación de HEYTI-CORE

**Estado:** Propuesto

**Fecha:** 2026-07-25

**Autor:** Arquitecto Fundador (Alex) / HEYTI-CORE Copilot

**Tipo:** Architecture Decision Record (ADR)

---

# 1. Objetivo

El presente ADR establece el lenguaje de programación y la plataforma tecnológica oficial para la implementación del núcleo (Kernel) de HEYTI.

Esta decisión define la base sobre la cual se desarrollarán todos los componentes del Runtime Cognitivo, incluyendo el Gateway, Session Manager, Capability Registry, Motor de Auditoría, Event Bus y las futuras capacidades del sistema.

La decisión deberá privilegiar:

- simplicidad arquitectónica;
- mantenibilidad a largo plazo;
- escalabilidad;
- integración con PostgreSQL/PostGIS;
- integración con modelos de Inteligencia Artificial;
- facilidad de pruebas automatizadas;
- productividad del desarrollo.

---

# 2. Contexto

Durante las primeras catorce etapas del proyecto se construyó la arquitectura conceptual de HEYTI sin comprometer la implementación con un lenguaje específico.

Esta estrategia permitió que las decisiones arquitectónicas permanecieran independientes de cualquier tecnología concreta.

Con el inicio del Sprint 15 comienza la construcción del software, por lo que resulta necesario seleccionar oficialmente la plataforma tecnológica sobre la cual será implementado el Kernel.

---

# 3. Alternativas Evaluadas

Las siguientes plataformas fueron consideradas:

- Python
- TypeScript / Node.js
- C#
- Java
- Go

Cada alternativa fue evaluada considerando los requerimientos funcionales y no funcionales definidos para HEYTI.

---

# 4. Criterios de Evaluación

Los criterios utilizados son:

1. Integración con PostgreSQL/PostGIS.
2. Capacidades para Inteligencia Artificial.
3. Facilidad de desarrollo.
4. Productividad.
5. Ecosistema de librerías.
6. Mantenibilidad.
7. Portabilidad.
8. Curva de aprendizaje.
9. Escalabilidad.
10. Facilidad para pruebas automatizadas.

Las alternativas serán comparadas objetivamente antes de emitir la decisión final.

---

# 5. Estado

Este ADR permanece en estado **Propuesto** hasta concluir el análisis comparativo de las alternativas.

La decisión definitiva será registrada en las siguientes secciones del documento.

# 6. Matriz Comparativa de Tecnologías

La evaluación se realizó considerando los requerimientos funcionales, arquitectónicos y operativos establecidos durante las primeras etapas del proyecto HEYTI.

La siguiente matriz resume el comportamiento esperado de cada alternativa.

| Criterio | Python | TypeScript / Node.js | C# (.NET) | Java | Go |
|----------|:------:|:--------------------:|:---------:|:----:|:--:|
| Integración PostgreSQL/PostGIS | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★☆ |
| Ecosistema para Inteligencia Artificial | ★★★★★ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ |
| Productividad de desarrollo | ★★★★★ | ★★★★☆ | ★★★★☆ | ★★★☆☆ | ★★★★☆ |
| Facilidad de mantenimiento | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★★★ | ★★★★★ |
| Disponibilidad de librerías | ★★★★★ | ★★★★★ | ★★★★☆ | ★★★★★ | ★★★☆☆ |
| Curva de aprendizaje | ★★★★★ | ★★★★☆ | ★★★☆☆ | ★★☆☆☆ | ★★★☆☆ |
| Automatización de pruebas | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★☆ |
| Escalabilidad | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ |
| Portabilidad | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ | ★★★★★ |
| Integración futura con modelos de IA | ★★★★★ | ★★★☆☆ | ★★★☆☆ | ★★★☆☆ | ★★☆☆☆ |

---

## Resultado General

La evaluación muestra que todas las plataformas analizadas son técnicamente capaces de soportar la arquitectura de HEYTI.

Sin embargo, únicamente Python obtiene la máxima calificación de manera consistente en los criterios considerados estratégicos para el proyecto, particularmente en:

- Inteligencia Artificial.
- Ciencia de datos.
- Analítica territorial.
- Integración con PostgreSQL/PostGIS.
- Rapidez de construcción.
- Ecosistema científico.
- Automatización.
- Disponibilidad de bibliotecas maduras.
- Facilidad de evolución.

Las demás alternativas presentan fortalezas importantes, especialmente para arquitecturas empresariales o aplicaciones de alto rendimiento, pero requieren un mayor esfuerzo para integrar capacidades avanzadas de análisis e inteligencia artificial, las cuales constituyen el núcleo funcional de HEYTI.

# 7. Decisión Arquitectónica

Después del análisis técnico realizado y de la evaluación de las alternativas disponibles, se establece la siguiente decisión oficial para la implementación de HEYTI.

## 7.1 Plataforma Oficial del Core

El núcleo de HEYTI (HEYTI-CORE) será implementado utilizando **Python** como lenguaje oficial de desarrollo.

Python constituye la plataforma que mejor satisface los objetivos estratégicos del proyecto debido a:

- Integración nativa con el ecosistema de Inteligencia Artificial.
- Amplio soporte para ciencia de datos y análisis territorial.
- Excelente integración con PostgreSQL y PostGIS.
- Ecosistema maduro para procesamiento geoespacial.
- Facilidad para automatización de pruebas.
- Alta productividad durante el desarrollo.
- Amplia comunidad y estabilidad tecnológica.

En consecuencia, todos los componentes centrales del Runtime Cognitivo deberán desarrollarse utilizando Python.

---

## 7.2 Alcance de la Decisión

Esta decisión aplica a los siguientes componentes:

- HEYTI Kernel.
- Runtime Cognitivo.
- Gateway.
- Capability Registry.
- Session Manager.
- Event Bus.
- Motor de Auditoría.
- Motor de Evidencias.
- Motor de Inteligencia Territorial (MIT).
- Knowledge System (HKS).
- Motores analíticos y algoritmos estratégicos.
- Servicios internos del Core.

---

## 7.3 Separación entre Backend y Frontend

La arquitectura de HEYTI adopta una separación estricta entre la lógica de negocio y la interfaz de usuario.

### Backend

El Backend será implementado en Python y concentrará toda la lógica del sistema.

Sus responsabilidades incluyen:

- procesamiento territorial;
- razonamiento cognitivo;
- análisis estratégico;
- administración del conocimiento;
- acceso a datos;
- auditoría;
- ejecución de capacidades;
- exposición de servicios mediante APIs.

### Frontend

La interfaz web será implementada utilizando **TypeScript** y **React**.

El Frontend tendrá exclusivamente responsabilidades de presentación e interacción con el usuario.

Entre ellas:

- visualización cartográfica;
- paneles de control;
- captura de información;
- administración;
- operación territorial;
- consumo de APIs del Core.

El Frontend nunca contendrá lógica estratégica ni reglas de negocio.

---

## 7.4 Principio de Desacoplamiento

El Frontend no podrá comunicarse directamente con la base de datos ni con componentes internos del Kernel.

Toda interacción deberá realizarse exclusivamente mediante el Gateway oficial del Runtime.

Este principio garantiza:

- desacoplamiento tecnológico;
- seguridad;
- mantenibilidad;
- escalabilidad;
- auditoría completa;
- independencia entre las capas del sistema.

---

## 7.5 Estado de la Decisión

**Estado:** Aprobado.

La presente decisión entra en vigor a partir del Sprint 15 y será considerada normativa para todas las implementaciones futuras del proyecto HEYTI.

# 8. Consecuencias de la Decisión

La adopción de Python como plataforma oficial del Core de HEYTI implica las siguientes consecuencias arquitectónicas:

## 8.1 Beneficios

La implementación del Kernel sobre Python permitirá:

- aprovechar un ecosistema maduro para Inteligencia Artificial y Ciencia de Datos;
- integrar de manera nativa bibliotecas para análisis geoespacial;
- facilitar la evolución del Motor de Inteligencia Territorial (MIT);
- reducir el tiempo de desarrollo del Runtime;
- simplificar la automatización de pruebas;
- favorecer la mantenibilidad del software a largo plazo.

---

## 8.2 Restricciones

Como consecuencia de esta decisión:

- toda la lógica estratégica deberá implementarse exclusivamente dentro del Core;
- el Frontend no podrá incorporar reglas de negocio;
- cualquier nueva capacidad deberá integrarse mediante el Capability Registry;
- las interfaces externas consumirán únicamente los servicios publicados por el Gateway.

---

## 8.3 Evolución Futura

La presente decisión no impide que componentes especializados puedan desarrollarse en otros lenguajes cuando exista una justificación técnica suficientemente documentada.

No obstante, cualquier excepción deberá aprobarse mediante un nuevo Architecture Decision Record (ADR) y garantizar la compatibilidad con la arquitectura oficial del Runtime.

---

# 9. Referencias

Este ADR se fundamenta en los siguientes documentos institucionales de HEYTI:

- HEYTI Software Architecture Specification (HSAS).
- HEYTI Software Engineering Specification (HSES).
- HEYTI Runtime Foundation.
- HEYTI Core Construction Guide.
- HEYTI Engineering Blueprint.
- HEYTI Business Rules (HBR-001).
- ADR-009 — Arquitectura Cognitiva de HEYTI.
- ADR-010 — Motor de Evidencias.
- ADR-011 — Política de Evolución Arquitectónica.

---

# 10. Vigencia

El presente ADR entra en vigor a partir de su aprobación por la Gobernanza Arquitectónica de HEYTI.

Toda implementación futura deberá respetar las decisiones aquí establecidas mientras este documento permanezca vigente.

---

**Estado Final:** **Aprobado**# 8. Consecuencias de la Decisión

La adopción de Python como plataforma oficial del Core de HEYTI implica las siguientes consecuencias arquitectónicas:

## 8.1 Beneficios

La implementación del Kernel sobre Python permitirá:

- aprovechar un ecosistema maduro para Inteligencia Artificial y Ciencia de Datos;
- integrar de manera nativa bibliotecas para análisis geoespacial;
- facilitar la evolución del Motor de Inteligencia Territorial (MIT);
- reducir el tiempo de desarrollo del Runtime;
- simplificar la automatización de pruebas;
- favorecer la mantenibilidad del software a largo plazo.

---

## 8.2 Restricciones

Como consecuencia de esta decisión:

- toda la lógica estratégica deberá implementarse exclusivamente dentro del Core;
- el Frontend no podrá incorporar reglas de negocio;
- cualquier nueva capacidad deberá integrarse mediante el Capability Registry;
- las interfaces externas consumirán únicamente los servicios publicados por el Gateway.

---

## 8.3 Evolución Futura

La presente decisión no impide que componentes especializados puedan desarrollarse en otros lenguajes cuando exista una justificación técnica suficientemente documentada.

No obstante, cualquier excepción deberá aprobarse mediante un nuevo Architecture Decision Record (ADR) y garantizar la compatibilidad con la arquitectura oficial del Runtime.

---

# 9. Referencias

Este ADR se fundamenta en los siguientes documentos institucionales de HEYTI:

- HEYTI Software Architecture Specification (HSAS).
- HEYTI Software Engineering Specification (HSES).
- HEYTI Runtime Foundation.
- HEYTI Core Construction Guide.
- HEYTI Engineering Blueprint.
- HEYTI Business Rules (HBR-001).
- ADR-009 — Arquitectura Cognitiva de HEYTI.
- ADR-010 — Motor de Evidencias.
- ADR-011 — Política de Evolución Arquitectónica.

---

# 10. Vigencia

El presente ADR entra en vigor a partir de su aprobación por la Gobernanza Arquitectónica de HEYTI.

Toda implementación futura deberá respetar las decisiones aquí establecidas mientras este documento permanezca vigente.

---

**Estado Final:** **Aprobado**