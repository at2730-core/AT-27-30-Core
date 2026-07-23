# Territorial Domain Specification v1.0

**Proyecto:** HEYTI-CORE  
**Sprint:** 7.1  
**Dominio:** Territorial  
**Estado:** En construcción  
**Propósito:** Definir conceptualmente la estructura territorial base de HEYTI-CORE.

---

## 1. Objetivo del dominio

El dominio Territorial representa la columna vertebral geográfica y administrativa de HEYTI-CORE.

Su función es organizar la jerarquía territorial necesaria para relacionar secciones, municipios, distritos, casillas, resultados electorales, operación de campo, estructura territorial, análisis socioeconómico y modelos estratégicos.

---

## 2. Principio rector

HEYTI no se diseña para un solo estado.

HEYTI se diseña para soportar múltiples entidades federativas, evitando colisiones entre códigos oficiales repetidos como:

- Distrito Federal 3 en distintos estados.
- Distrito Local 5 en distintos estados.
- Sección 0001 en distintas entidades.

Por ello, todos los códigos oficiales deberán interpretarse dentro de su contexto territorial.

---

## 3. Entidades conceptuales

El dominio Territorial contempla:

- Country
- State
- Municipality
- Federal District
- Local District
- Section
- Section History

---

## 4. Jerarquía base

```text
Country
   └── State
        ├── Municipality
        ├── Federal District
        ├── Local District
        └── Section


        ---

## 8. Fichas conceptuales

### 8.1 territorial.country

**Descripción:**  
Representa el país al que pertenece la estructura territorial.

**Propósito:**  
Servir como raíz de la jerarquía territorial de HEYTI-CORE y permitir que la plataforma pueda escalar más allá de una sola entidad federativa o incluso adaptarse a otros contextos nacionales en el futuro.

**Regla principal:**  
Todo estado deberá pertenecer a un país.

**Identificador interno:**  
`country_id`

**Código oficial:**  
`country_code`

**Relaciones:**  

- 1:N con `territorial.state`

**Uso esperado:**  

- Agrupar entidades federativas.
- Evitar que la arquitectura quede limitada únicamente a México.
- Permitir trazabilidad territorial completa desde país hasta sección.

**Fuente inicial:**  
Configuración interna de HEYTI-CORE.

**Registro inicial esperado:**  

| country_code | country_name |
|---|---|
| MX | México |

**Decisión de arquitectura:**  
Aunque la primera implementación de HEYTI-CORE se desarrollará para México, se incluye `territorial.country` desde la versión inicial para mantener una jerarquía territorial completa y escalable.

---

## 8.2 State

### Descripción

Representa una entidad federativa de la República Mexicana.

Constituye el primer nivel administrativo utilizado por HEYTI-CORE para organizar la información territorial.

Actualmente el sistema iniciará con el estado de Guanajuato, pero el modelo está diseñado para soportar las 32 entidades federativas y futuras ampliaciones.

---

### Objetivo

Organizar toda la información territorial dentro de una entidad federativa.

Todo elemento territorial deberá pertenecer a un Estado.

---

### Responsabilidades

El Estado es responsable de agrupar:

- Municipios
- Distritos Federales
- Distritos Locales
- Secciones

---

### Identificador interno

state_id

---

### Código oficial

state_code

---

### Atributos principales

- state_id
- country_id
- state_code
- abbreviation
- state_name
- created_at
- updated_at
- is_active

---

### Reglas de negocio

1. Todo Estado pertenece a un único País.

2. Un Estado puede contener múltiples Municipios.

3. Un Estado puede contener múltiples Distritos Federales.

4. Un Estado puede contener múltiples Distritos Locales.

5. Un Estado puede contener múltiples Secciones.

6. El código oficial del Estado debe ser único dentro del País.

---

### Relaciones

Country

↓

State

↓

Municipality

Federal District

Local District

Section

---

### Fuente Oficial

INE

Marco Geoestadístico Nacional

---

### Observaciones de Arquitectura

El Estado constituye la raíz operativa de toda la plataforma.

La incorporación futura de nuevas entidades federativas no requerirá modificar el modelo relacional; únicamente implicará cargar nuevos registros.

---

### Dependencias

Este dominio será consumido por:

- Spatial
- Electoral
- Socioeconómico
- Field
- Election Day
- Analytics
- AI


---

## 8.3 Municipality

### Descripción

Representa la unidad básica de administración territorial dentro de una entidad federativa.

Para HEYTI-CORE, el Municipio constituye el principal nivel de agregación operativa para el análisis electoral, la organización territorial, la operación de campo y la toma de decisiones estratégicas.

Es el punto donde convergen la información geográfica, demográfica, socioeconómica y electoral.

---

### Objetivo

Agrupar territorialmente las secciones electorales y servir como nivel natural para el análisis estratégico y operativo.

---

### Responsabilidades

Un Municipio es responsable de contener:

- Secciones electorales
- Casillas
- Información socioeconómica agregada
- Resultados electorales agregados
- Operación territorial
- Estructura territorial

---

### Identificador interno

municipality_id

---

### Código oficial

municipality_code

---

### Atributos principales

- municipality_id
- state_id
- municipality_code
- municipality_name
- created_at
- updated_at
- is_active

---

### Reglas de negocio

1. Todo Municipio pertenece a un único Estado.

2. El código oficial del Municipio únicamente es único dentro del Estado al que pertenece.

3. Un Municipio puede contener múltiples Secciones.

4. Una Sección pertenece únicamente a un Municipio.

5. Toda información estratégica municipal deberá calcularse a partir de las Secciones que contiene.

---

### Relaciones

Country

↓

State

↓

Municipality

↓

Section

↓

Casilla

---

### Fuente Oficial

INE

Marco Geoestadístico Nacional

---

### Uso dentro de HEYTI

El Municipio será utilizado para:

- Reportes ejecutivos.
- Agregación de indicadores.
- Simulaciones territoriales.
- Planeación de operación.
- Seguimiento de campañas.
- Generación de mapas temáticos.
- Consolidados municipales.

---

### Observaciones de Arquitectura

Aunque el Municipio constituye una división administrativa, para HEYTI representa además una unidad estratégica de análisis.

La mayor parte de los indicadores ejecutivos del sistema podrán calcularse y visualizarse a nivel municipal.

---

### Dependencias

Consumido por:

- Spatial
- Electoral
- Socioeconómico
- Field
- Election Day
- Analytics
- AI

Produce información para:

- Dashboards
- Reportes
- Simuladores
- Copilot

---

## 8.4 Federal District

### Descripción

Representa un Distrito Electoral Federal definido por el Instituto Nacional Electoral (INE).

El Distrito Federal constituye una agrupación territorial de secciones electorales utilizada para la elección de Diputaciones Federales y como unidad estratégica de análisis dentro de HEYTI-CORE.

Aunque pertenece a una entidad federativa, su finalidad es eminentemente electoral.

---

### Objetivo

Agrupar secciones electorales bajo una delimitación oficial para el análisis, simulación y seguimiento de procesos electorales federales.

---

### Responsabilidades

Un Distrito Federal es responsable de agrupar:

- Secciones electorales
- Resultados electorales federales
- Lista Nominal Federal
- Participación Federal
- Indicadores estratégicos federales
- Cobertura territorial

---

### Identificador interno

federal_district_id

---

### Código oficial

federal_district_code

---

### Atributos principales

- federal_district_id
- state_id
- federal_district_code
- federal_district_name
- created_at
- updated_at
- is_active

---

### Reglas de negocio

1. Todo Distrito Federal pertenece a un único Estado.

2. El número oficial del Distrito Federal únicamente es único dentro del Estado.

3. Un Distrito Federal contiene múltiples Secciones.

4. Una Sección pertenece únicamente a un Distrito Federal.

5. La delimitación territorial es determinada exclusivamente por el INE.

---

### Relaciones

Country

↓

State

↓

Federal District

↓

Section

↓

Electoral Results

---

### Fuente Oficial

Instituto Nacional Electoral (INE)

Distritación Federal vigente.

---

### Uso dentro de HEYTI

El Distrito Federal será utilizado para:

- Reportes legislativos.
- Simulación electoral federal.
- Indicadores estratégicos.
- Seguimiento territorial.
- Comparativos históricos.
- Planeación de campañas federales.
- Análisis de competitividad.

---

### Observaciones de Arquitectura

Los Distritos Federales constituyen una organización electoral y no una división administrativa.

Su existencia responde exclusivamente a la representación política federal.

HEYTI deberá permitir conservar versiones históricas de las distritaciones para análisis comparativos.

---

### Dependencias

Consumido por:

- Electoral
- Analytics
- AI

Produce información para:

- Dashboards
- Simuladores
- Copilot
- Reportes Ejecutivos