# AT-27-30

# Manual de Arquitectura

## Versión 1.0

**Proyecto:** AT-27-30 – Copilot Electoral Territorial (HEYTI)

**Versión:** 1.0

**Estado:** En construcción

**Fecha de inicio:** Junio 2026

---

# 1. Propósito

Este documento define la arquitectura oficial de datos y componentes del proyecto AT-27-30.

Su objetivo es garantizar que todas las decisiones de diseño, desarrollo y evolución del sistema mantengan una estructura coherente, escalable y documentada.

Este manual constituye la referencia técnica principal del proyecto.

---

# 2. Filosofía del Proyecto

AT-27-30 no es únicamente una aplicación informática.

Es una plataforma de inteligencia territorial electoral diseñada para apoyar el análisis, la organización y la operación territorial durante cualquier proceso electoral.

El desarrollo se basa en los siguientes principios:

* Una única fuente de verdad para cada entidad.
* Separación clara de responsabilidades entre módulos.
* Arquitectura evolutiva.
* Datos auditables y trazables.
* Integración de fuentes oficiales.
* Evolución permanente sin romper compatibilidad.

---

# 3. Visión General

La plataforma sigue el flujo natural de una operación territorial.

ANÁLISIS TERRITORIAL

↓

SOCIOECONÓMICO

↓

GANAR TODO

↓

CAMPO

↓

ESTRUCTURA TERRITORIAL (ET-27)

↓

DÍA D

↓

HEYTI

---

# 4. Arquitectura por Esquemas

## territorial

Responsabilidad:

Administrar la organización geográfica electoral.

Contiene:

* Estados
* Municipios
* Distritos
* Secciones
* Historial territorial

Es la fuente oficial de la geografía electoral.

---

## spatial

Responsabilidad:

Administrar la información espacial.

Contiene:

* Geometrías
* Casillas
* Capas cartográficas
* Índices espaciales

---

## electoral

Responsabilidad:

Administrar resultados electorales históricos.

Contiene:

* Elecciones
* Resultados
* Partidos
* Candidaturas

---

## socioeconomico

Responsabilidad:

Administrar indicadores socioeconómicos.

Contiene:

* Población
* Lista nominal
* Indicadores
* Estadísticas

---

## field

Responsabilidad:

Administrar los recursos humanos territoriales.

Contiene:

* actor
* role
* actor_history

Es la fuente oficial de personas y roles.

---

## structure

Responsabilidad:

Administrar la organización territorial.

Contiene:

* casilla
* casilla_assignment
* general_assignment
* coverage
* coverage_history

No almacena personas.

Administra asignaciones.

---

## election_day

Responsabilidad:

Administrar la operación del Día D.

Contiene:

* Casillas
* Incidencias
* Actas
* Cobertura operativa

---

## analytics

Responsabilidad:

Administrar inteligencia electoral.

Contiene:

* Indicadores
* Escenarios
* Recomendaciones
* Modelos predictivos

---

# 5. Fuentes Oficiales

El proyecto mantiene un repositorio independiente denominado:

fuentes_oficiales

Este repositorio almacena exclusivamente información oficial sin modificaciones.

Ejemplos:

* INE
* IEEG
* INEGI
* CONAPO
* Históricos de Secciones
* Resultados Electorales
* Cartografía Oficial

---

# 6. Fuente Única de Verdad

## Personas

field.actor

---

## Roles

field.role

---

## Casillas

structure.casilla

---

## Secciones

territorial.section

---

## Resultados Electorales

electoral.*

---

## Indicadores Socioeconómicos

socioeconomico.*

---

# 7. Metodología Oficial de Desarrollo

Todo desarrollo seguirá el siguiente proceso.

1. Visión Estratégica.
2. Auditoría.
3. Comprensión.
4. Consolidación.
5. Evolución.
6. Validación.
7. Documentación.
8. Checkpoint.

---

# 8. Architecture Decision Records (ADR)

Las decisiones relevantes de arquitectura serán documentadas mediante ADR.

Cada ADR deberá indicar:

* Fecha.
* Contexto.
* Problema.
* Decisión.
* Consecuencias.

---

## ADR-001

Catálogo único de Roles.

Decisión:

El catálogo oficial de roles será field.role.

---

## ADR-002

Modelo de Asignaciones.

Decisión:

Las asignaciones territoriales se administrarán mediante:

* structure.casilla_assignment
* structure.general_assignment

No se duplicarán catálogos de roles dentro del esquema structure.

---

# 9. Evolución

Toda modificación deberá mantener compatibilidad con procesos electorales futuros.

La arquitectura deberá soportar:

* Nuevas elecciones.
* Redistritaciones.
* Reseccionamientos.
* Cambios cartográficos.
* Nuevas fuentes oficiales.

---

# 10. Objetivo Final

Construir una plataforma de inteligencia territorial electoral que permita analizar, organizar, operar y evolucionar procesos electorales utilizando una arquitectura de datos sólida, documentada y preparada para múltiples elecciones futuras.
