# HEYTI Knowledge Domain Model v1.0

## Modelo de Dominios de Conocimiento

**Proyecto:** HEYTI-CORE\
**Sprint:** 8\
**Estado:** Auditoría arquitectónica (v1.0)

------------------------------------------------------------------------

# 1. Objetivo

Definir el modelo conceptual de dominios de conocimiento que conforman
HEYTI-CORE, estableciendo la organización del conocimiento alrededor de
la Sección Electoral como unidad mínima de Inteligencia Territorial.

Este documento describe el conocimiento del negocio y no representa el
diseño físico de PostgreSQL ni la arquitectura de software.

------------------------------------------------------------------------

# 2. Entidad Central

La **Sección Electoral** constituye la unidad mínima de Inteligencia
Territorial.

Toda entidad, regla de negocio y proceso de razonamiento deberá
relacionarse directa o indirectamente con una Sección Electoral.

La Sección funciona como un Expediente Estratégico Territorial donde
converge el conocimiento territorial, electoral, socioeconómico,
organizacional, operativo e histórico.

------------------------------------------------------------------------

# 3. Organización del Modelo

Todos los dominios utilizarán la misma estructura:

1.  Objetivo
2.  Entidades
3.  Relaciones
4.  Reglas del Dominio
5.  Información que entrega al MIT
6.  Información que recibe del MIT

## Parte I -- Dominios de Conocimiento

-   Territorial
-   Electoral
-   Socioeconómico
-   Capital Territorial
-   Operación Territorial
-   Riesgo y Seguridad

## Parte II -- Dominio Cognitivo

-   Inteligencia Territorial

## Parte III -- Productos de Inteligencia

-   Productos de Inteligencia

## Parte IV -- Infraestructura

-   Administración del Sistema

------------------------------------------------------------------------

# Ajustes derivados de la auditoría

-   Eliminar versiones duplicadas de los dominios.
-   Completar Territorial y Electoral con la estructura estándar.
-   Separar claramente los dominios de conocimiento de los dominios
    cognitivos.
-   Mantener el MIT como componente de la Arquitectura Lógica y no como
    entidad del dominio.
-   Incorporar un diagrama conceptual del modelo en la siguiente
    versión.

------------------------------------------------------------------------

# Próximos pasos

1.  Revisar todas las reglas BR-XXX.
2.  Consolidar el Catálogo de Entidades.
3.  Elaborar la Arquitectura Lógica.
4.  Generar el PostgreSQL Blueprint.

------------------------------------------------------------------------

# Conclusión

El Modelo de Dominios constituye el fundamento conceptual de HEYTI-CORE
y será la base para la Arquitectura Lógica, el Modelo Físico PostgreSQL
y el Motor de Inteligencia Territorial.
