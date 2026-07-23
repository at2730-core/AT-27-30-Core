-- ============================================================
-- HEYTI-CORE
-- Sprint 7.0 – Fundación
-- Script: 01_create_schemas_heyti_core.sql
-- Objetivo: Crear esquemas base de HEYTI-CORE
-- ============================================================

CREATE SCHEMA IF NOT EXISTS territorial;
CREATE SCHEMA IF NOT EXISTS spatial;
CREATE SCHEMA IF NOT EXISTS electoral;
CREATE SCHEMA IF NOT EXISTS socioeconomico;
CREATE SCHEMA IF NOT EXISTS field;
CREATE SCHEMA IF NOT EXISTS election_day;
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS metadata;
CREATE SCHEMA IF NOT EXISTS security;
CREATE SCHEMA IF NOT EXISTS ai;

COMMENT ON SCHEMA territorial IS 'Catálogo territorial: estado, municipios, distritos, secciones.';
COMMENT ON SCHEMA spatial IS 'Geometrías PostGIS: secciones, casillas, puntos territoriales.';
COMMENT ON SCHEMA electoral IS 'Resultados electorales históricos, partidos, elecciones y lista nominal.';
COMMENT ON SCHEMA socioeconomico IS 'Indicadores socioeconómicos por sección.';
COMMENT ON SCHEMA field IS 'Operación territorial de campo: actores, puntos, promotores, liderazgos.';
COMMENT ON SCHEMA election_day IS 'Operación Día D: casillas, actas, estatus, incidencias y cortes.';
COMMENT ON SCHEMA analytics IS 'Vistas, indicadores estratégicos, scoring y motores analíticos.';
COMMENT ON SCHEMA metadata IS 'Control de fuentes, auditorías, cobertura y trazabilidad.';
COMMENT ON SCHEMA security IS 'Usuarios, roles, permisos y control de acceso.';
COMMENT ON SCHEMA ai IS 'Memoria, prompts, recomendaciones y contexto de HEYTI.';