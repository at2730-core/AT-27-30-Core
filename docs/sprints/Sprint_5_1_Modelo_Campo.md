# Sprint 5.1 – Modelo de Datos CAMPO

## Fecha

19 de junio de 2026

---

## Objetivo

Diseñar e implementar el modelo de datos inicial del módulo CAMPO dentro de PostgreSQL/PostGIS, con el propósito de migrar la información actualmente almacenada en archivos GeoJSON y almacenamiento local hacia una estructura robusta, escalable y preparada para la evolución del sistema AT 27-30 hacia el Copilot Electoral Territorial (HEYTI).

El modelo debía soportar:

* Registro de actores territoriales.
* Catálogo de tipos de asignación.
* Control de promotores.
* Validación administrativa de registros.
* Historial de modificaciones.
* Administración de objetivos operativos.
* Generación y seguimiento de rutas inteligentes.

---

## Tablas creadas

### Esquema

```text
field
```

### Catálogos

```text
field.assignment_type
field.validation_status
field.promoter
```

### Operación Territorial

```text
field.actor
field.actor_history
```

### Base Operativa

```text
field.operational_target
```

### Planeación de Rutas

```text
field.route
field.route_target
```

---

## Resultado

Se creó exitosamente el esquema funcional del módulo CAMPO dentro de PostgreSQL/PostGIS.

El modelo implementado permite representar los principales procesos operativos del trabajo territorial:

```text
Promotor
↓
Captura
↓
Validación Administrativa
↓
Actor Territorial
↓
Planeación Operativa
↓
Generación de Rutas
↓
Seguimiento
```

Asimismo, se estableció la separación conceptual entre:

### Actores Territoriales

Representan personas y estructuras políticas registradas en territorio.

Fuente actual:

```text
puntos_campo.geojson
```

Destino futuro:

```text
field.actor
```

### Objetivos Operativos

Representan domicilios o personas objetivo para visitas, recorridos y jornadas de campo.

Fuente actual:

```text
df3_base_operativa.geojson
```

Destino futuro:

```text
field.operational_target
```

También se incorporó un modelo de validación administrativa para garantizar la calidad de la información capturada por promotores.

Flujo definido:

```text
PROMOTOR
↓
Captura
↓
PENDIENTE_VALIDACION
↓
ADMINISTRADOR
↓
Valida / Corrige / Rechaza
↓
ACTIVO
```

---

## Pendientes

### Sprint 5.2 – Migración de Datos CAMPO

* Migrar registros de `puntos_campo.geojson` hacia `field.actor`.
* Migrar registros de `df3_base_operativa.geojson` hacia `field.operational_target`.
* Validar integridad territorial (sección, municipio, distrito local y distrito federal).
* Generar scripts ETL de carga inicial.

### Sprint 5.3 – Operación Territorial

* Implementar catálogo administrable de tipos de asignación.
* Implementar edición administrativa de actores territoriales.
* Implementar historial automático de cambios.
* Implementar consulta territorial por sección.

### Sprint 5.4 – Rutas Inteligentes

* Integrar generación de rutas desde PostgreSQL.
* Incorporar seguimiento de visitas.
* Incorporar estados de cumplimiento de ruta.
* Incorporar métricas de productividad territorial.

### Sprint 5.5 – Integración HEYTI

* Generar indicadores de cobertura territorial.
* Detectar vacíos operativos por sección.
* Recomendar asignación de promotores.
* Recomendar generación de rutas.
* Integrar recomendaciones tácticas dentro del Copilot Electoral Territorial.

```
```
