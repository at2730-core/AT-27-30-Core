# Sprint 5.2.5 – Auditoría de Migración – Módulo Socioeconómico

**Proyecto:** AT 27-30 → HEYTI-CORE  
**Sprint:** 5.2.5  
**Módulo:** Socioeconómico  
**Fecha:** Junio 2026

---

# Objetivo

Realizar la auditoría técnica completa del módulo **Socioeconómico**, identificando su arquitectura funcional, fuentes de datos, dependencias, lógica de procesamiento, indicadores, cálculos, estructuras utilizadas y requerimientos para su migración completa hacia PostgreSQL/PostGIS como parte de la construcción de **AT2730-HEYTI-CORE**.

---

# Archivos auditados

## Interfaz

- socioeconomico.html
- socioeconomico.css
- socioeconomico.js

## Datos

- Datos_Socioeconomicos.json
- catalogo_territorial.json
- secciones.geojson

---

# Objetivo funcional del módulo

El módulo Socioeconómico permite visualizar indicadores demográficos y sociales por sección electoral mediante mapas coropléticos, aplicando diferentes esquemas de clasificación y permitiendo realizar proyecciones demográficas hacia 2027.

Su propósito es apoyar el análisis estratégico territorial previo a la planeación política y electoral.

---

# Componentes funcionales identificados

## 1. Buscador de Sección

Permite localizar una sección electoral específica dentro del universo seleccionado.

Funciones:

- búsqueda por número
- resaltado de geometría
- zoom automático

---

## 2. Universo de trabajo

Permite filtrar:

- Estado
- Municipio
- Distrito Federal
- Distrito Local

El universo es heredado desde el Portal mediante:

```
AT_UNIVERSE
```

---

## 3. Indicadores

Actualmente el módulo presenta seis indicadores.

| Código | Indicador |
|---------|-----------|
| IM | Marginación |
| EDU | Rezago Educativo |
| ING | Ingreso Estimado |
| SERV | Acceso a Servicios |
| POB | Pobreza (Proxy) |
| URB | Índice Urbano-Rural |

---

## 4. Clasificación estadística

El mapa puede representarse mediante:

- Quintiles (Q5)
- Cuartiles (Q4)
- Tercios (Q3)

Los rangos son calculados dinámicamente utilizando cuantiles.

---

## 5. Mapa temático

Características:

- Leaflet
- Choropleth
- Colores dinámicos
- Tooltip por sección
- Leyenda automática
- Zoom por universo

---

## 6. Proyección 2027

El módulo incorpora una herramienta para calcular:

- Lista Nominal 2027
- Población mayor de 18 años 2027

La proyección utiliza:

- CAGR (cuando existen datos históricos)
- tasa anual definida por el usuario como respaldo

---

# Fuentes de datos identificadas

## Geografía

```
secciones.geojson
```

Contiene:

- geometría
- sección
- municipio
- distrito local
- distrito federal

---

## Catálogo Territorial

```
catalogo_territorial.json
```

Contiene:

- municipios
- distritos federales
- distritos locales

---

## Datos Socioeconómicos

```
Datos_Socioeconomicos.json
```

Contiene información por sección electoral.

Entre los indicadores encontrados destacan:

- población total
- población 15-17
- población 18+
- escolaridad promedio
- analfabetismo
- PEA
- ocupación
- desocupación
- viviendas con agua
- drenaje
- electricidad
- internet
- computadora
- telefonía

---

# Hallazgos técnicos

## Hallazgo 1

Los indicadores mostrados en pantalla:

- IM
- EDU
- ING
- SERV
- POB
- URB

NO existen físicamente dentro del JSON.

Corresponden a indicadores derivados.

---

## Hallazgo 2

El JSON almacena variables censales.

Los índices deberán calcularse posteriormente.

---

## Hallazgo 3

Las proyecciones 2027 requieren información histórica.

Actualmente sólo existe parcialmente.

Será necesario construir el dataset histórico.

---

## Hallazgo 4

Existe un modo DEMO.

Cuando no encuentra el dataset genera valores aleatorios.

Esta funcionalidad deberá eliminarse en PostgreSQL.

---

## Hallazgo 5

El módulo permite cargar CSV y JSON manualmente.

Actualmente estos datos se almacenan temporalmente mediante:

```
AT_SOCIO_USER
```

---

# Dependencias

## LocalStorage

AT_PATHS

AT_UNIVERSE

AT_SOCIO_USER

---

## Librerías

Leaflet

OpenStreetMap

---

# Modelo PostgreSQL propuesto

Se propone crear el esquema:

```
socioeconomico
```

Con las siguientes tablas:

## indicator_catalog

Catálogo de indicadores.

---

## section_indicator

Valores de indicadores por sección.

---

## section_projection

Resultados de proyecciones demográficas.

---

## classification_run

Ejecución de clasificaciones.

---

## classification_break

Rangos de clasificación.

---

# Relaciones con otros módulos

## Territorial

Obtiene:

- sección
- municipio
- distrito local
- distrito federal

---

## Electoral

Obtendrá:

- Lista Nominal
- Padrón Electoral

---

## Analytics

Consumirá:

- indicadores
- proyecciones
- clasificaciones

---

## HEYTI

Consumirá todas las vistas analíticas.

---

# Matriz de Migración

| Origen | Destino PostgreSQL |
|---------|-------------------|
| Datos_Socioeconomicos.json | socioeconomico.section_indicator |
| Catálogo Territorial | territorial.* |
| GeoJSON | spatial.section_geometry |
| Indicadores derivados | analytics |
| Clasificaciones | analytics |
| Proyecciones | socioeconomico.section_projection |

---

# Riesgos detectados

- indicadores derivados sin definición formal
- falta dataset histórico para proyecciones
- existencia de modo DEMO
- persistencia temporal mediante LocalStorage
- dependencia parcial del Portal

---

# Recomendaciones

1. Migrar primero los datos base.

2. Calcular indicadores mediante vistas PostgreSQL.

3. Eliminar completamente el modo DEMO.

4. Generar el dataset histórico de Lista Nominal.

5. Construir las proyecciones desde PostgreSQL.

6. Integrar las vistas directamente al futuro HEYTI-CORE.

---

# Resultado del Sprint

## Estado

✅ Auditoría completada.

---

## Migración

🟡 Lista para iniciar una vez concluya la auditoría de todos los módulos.

---

## Próximo Sprint

**Sprint 5.2.6**

Auditoría de Migración

**Módulo GANAR TODO**

---

# Conclusión

La auditoría del módulo Socioeconómico permitió identificar completamente su arquitectura funcional, fuentes de información, lógica estadística y dependencias.

Se concluye que el módulo puede migrarse íntegramente hacia PostgreSQL/PostGIS, separando claramente:

- datos censales base
- indicadores derivados
- procesos analíticos
- proyecciones demográficas

Esta separación permitirá que **HEYTI-CORE** utilice un modelo de datos escalable, consistente y desacoplado de la lógica actual implementada en JavaScript, facilitando el desarrollo de capacidades analíticas, simulaciones estratégicas y recomendaciones inteligentes.