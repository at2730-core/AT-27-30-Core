# Checkpoints del Proyecto AT-27-30-Core

## Checkpoint 001 - Territorial Base

Fecha: 2026-06-11

Estado:

* PostgreSQL 18 instalado
* PostGIS 3.6 instalado
* Base de datos at2730_core creada
* Esquemas creados:

  * territorial
  * spatial
  * electoral
  * socioeconomico
  * field
  * election_day
  * metadata
  * analytics
  * audit

Tablas creadas:

* territorial.municipio
* territorial.distrito_local
* territorial.distrito_federal
* territorial.section
* territorial.section_history

Respaldo generado:

* at2730_core_checkpoint_001_territorial.sql

Observaciones:

* Docker descartado para esta fase del proyecto.
* Arquitectura local PostgreSQL/PostGIS estable.
* Primer respaldo validado.
