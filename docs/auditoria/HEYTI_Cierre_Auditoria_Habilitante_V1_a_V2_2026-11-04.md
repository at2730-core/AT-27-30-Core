# HEYTI — Cierre de Auditoría Habilitante V1 → V2

**Fecha:** 4 de noviembre de 2026
**Rama:** `feature/heyti-v2-foundation`
**Checkpoint técnico:** `aa491f4`
**Checkpoint documental:** `12ac3d6`

## 1. Resultado

La auditoría habilitante previa a la continuación de la migración V1 → V2 queda cerrada.

El cierre no implica que todas las fuentes estén certificadas. Significa que cada componente quedó clasificado según su estado de verdad, sus restricciones y la forma segura de migrarlo.

## 2. Base técnica validada

- Backend y runtime: 507 pruebas aprobadas.
- Subpruebas backend: 94 aprobadas.
- Frontend: 283 pruebas aprobadas.
- Build TypeScript/Vite: aprobado.
- Oxlint: 0 errores.
- Capability Registry: 5 capacidades registradas.
- Worktree limpio y checkpoints respaldados en GitHub.

## 3. Clasificación final

| Componente | Estado | Decisión |
|---|---|---|
| Arquitectura HEYTI V2 | READY | Base autorizada |
| Análisis Territorial | READY_WITH_VERSIONING | Continuar sobre fuentes identificadas |
| Ganar Todo | READY_WITH_VERSIONING | Mantener límites de resultados rastreados |
| Socioeconómico | READY | Fuentes y cobertura visibles |
| Campo | READY_WITH_VERSIONING | Migrar los 45 registros existentes y flujos de captura |
| Día D — inventario de casillas | READY_WITH_VERSIONING | Migrar con cobertura y corte explícitos |
| Día D — estados operativos 2027 | STAGING_ONLY | No presentar como operación oficial |
| Estructura / ET-27 | STAGING_ONLY | Migrar modelo, interfaz y simulación controlada |
| Estructura oficial 2027 | BLOCKED_BY_MGE_2027 | No asignar identidad territorial definitiva |
| Marco geográfico nominal 2027 | BLOCKED_BY_MGE_2027 | Pendiente `GAP-MGE-2027-001` |

## 4. Universo territorial 2027

El acuerdo INE/CG526/2026 declara para Guanajuato:

- 15 distritos federales;
- 22 distritos locales;
- 46 municipios;
- 3,432 secciones.

La reconstrucción nominal disponible explica 3,431 secciones. La diferencia de una sección permanece registrada como `GAP-MGE-2027-001`.

Hasta disponer del producto nominal oficial:

- no se reemplazará la geografía vigente de HEYTI;
- no se inventarán genealogías;
- no se presentarán estructuras o casillas como definitivas para 2027.

## 5. Diagnóstico de módulos pendientes

### Campo

Disponibles:

- ETL de carga, validación y exportación;
- datos GeoJSON;
- 45 registros previamente cargados;
- modelo espacial y territorial;
- funciones V1 de captura, GPS, mapa, geocodificación y exportación.

Pendiente:

- capability específica;
- contratos HTTP;
- gateway frontend;
- workspace V2;
- pruebas end-to-end y Golden Cases.

### Día D

Disponibles:

- fuente de casillas;
- ETL de casillas;
- geometría puntual;
- relación territorial por sección;
- funciones V1 de panel, cobertura, representantes y navegación mapa-tabla.

Pendiente:

- reconciliar cobertura fuente → base;
- capability de lectura;
- contrato de estados operativos;
- workspace V2;
- Golden Cases.

Los estados 2027 serán simulación o staging mientras no exista corte operativo certificado.

### Estructura / ET-27

Disponibles:

- fuente territorial;
- casillas;
- puntos de Campo;
- lógica V1 de representantes, coordinadores, faltantes, ubicación y exportación.

Pendiente:

- dominio específico de estructura;
- persistencia versionada;
- capability;
- workspace V2;
- Golden Cases.

No se presentará ninguna estructura como oficial para 2027 mientras permanezca abierto `GAP-MGE-2027-001`.

## 6. Golden Cases obligatorios

### Campo

1. Conteo controlado de 45 registros.
2. Identidad de sección preservada.
3. Coordenadas y rol preservados.
4. Exportación sin pérdida de campos.
5. Registro sin geometría tratado explícitamente.

### Día D

1. Casilla ↔ sección.
2. Conteo fuente ↔ base con diferencias visibles.
3. Casilla con representante.
4. Casilla sin cobertura.
5. Estado operativo identificado como staging.

### Estructura

1. Representante de casilla.
2. Representante de sección.
3. Coordinador distrital.
4. Persona sin casilla asignada.
5. Déficit de cobertura calculado sin inventar asignaciones.

## 7. Decisión de continuidad

La auditoría deja de ser una fase bloqueante.

La migración continuará en este orden:

1. Campo.
2. Día D.
3. Estructura / ET-27.

Cada módulo deberá superar:

`fuente → base → capability → runtime → materialización → interfaz → Golden Case`

antes de considerarse migrado.

## 8. Pendientes externos no bloqueantes

- Publicación del marco geográfico nominal oficial 2027.
- Resolución de `GAP-MGE-2027-001`.
- Cierre de discrepancias electorales históricas registradas.
- Definición del corte operativo 2027 para Día D y Estructura.

Estos pendientes limitan certificaciones futuras, pero no impiden migrar ahora la arquitectura y los datos comprobados.
