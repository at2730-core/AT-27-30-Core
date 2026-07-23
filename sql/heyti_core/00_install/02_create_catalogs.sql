-- ============================================================
-- HEYTI-CORE
-- Sprint 7.1 – Catálogos Fundamentales
-- Script: 02_create_catalogs.sql
-- Objetivo: Crear catálogos territoriales base
-- ============================================================

-- =========================
-- ESTADOS
-- =========================
CREATE TABLE IF NOT EXISTS territorial.state (
    state_id BIGSERIAL PRIMARY KEY,
    state_code INTEGER NOT NULL UNIQUE,
    state_name TEXT NOT NULL,
    abbreviation TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

COMMENT ON TABLE territorial.state IS
'Catálogo de entidades federativas. Usa llave interna state_id y código oficial state_code.';

-- =========================
-- MUNICIPIOS
-- =========================
CREATE TABLE IF NOT EXISTS territorial.municipality (
    municipality_id BIGSERIAL PRIMARY KEY,
    state_id BIGINT NOT NULL REFERENCES territorial.state(state_id),
    municipality_code INTEGER NOT NULL,
    municipality_name TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT uq_municipality_state_code UNIQUE (state_id, municipality_code)
);

COMMENT ON TABLE territorial.municipality IS
'Catálogo de municipios por entidad federativa. El código municipal solo es único dentro de cada estado.';

-- =========================
-- DISTRITOS FEDERALES
-- =========================
CREATE TABLE IF NOT EXISTS territorial.federal_district (
    federal_district_id BIGSERIAL PRIMARY KEY,
    state_id BIGINT NOT NULL REFERENCES territorial.state(state_id),
    federal_district_code INTEGER NOT NULL,
    federal_district_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT uq_federal_district_state_code UNIQUE (state_id, federal_district_code)
);

COMMENT ON TABLE territorial.federal_district IS
'Catálogo de distritos federales. El número de distrito se repite entre estados, por eso depende de state_id.';

-- =========================
-- DISTRITOS LOCALES
-- =========================
CREATE TABLE IF NOT EXISTS territorial.local_district (
    local_district_id BIGSERIAL PRIMARY KEY,
    state_id BIGINT NOT NULL REFERENCES territorial.state(state_id),
    local_district_code INTEGER NOT NULL,
    local_district_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT uq_local_district_state_code UNIQUE (state_id, local_district_code)
);

COMMENT ON TABLE territorial.local_district IS
'Catálogo de distritos locales. El número de distrito local se interpreta dentro de cada estado.';

-- =========================
-- SECCIONES
-- =========================
CREATE TABLE IF NOT EXISTS territorial.section (
    section_id BIGSERIAL PRIMARY KEY,
    state_id BIGINT NOT NULL REFERENCES territorial.state(state_id),
    municipality_id BIGINT REFERENCES territorial.municipality(municipality_id),
    federal_district_id BIGINT REFERENCES territorial.federal_district(federal_district_id),
    local_district_id BIGINT REFERENCES territorial.local_district(local_district_id),
    section_code INTEGER NOT NULL,
    section_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    CONSTRAINT uq_section_state_code UNIQUE (state_id, section_code)
);

COMMENT ON TABLE territorial.section IS
'Catálogo maestro de secciones electorales. section_id es la llave interna; section_code conserva el número oficial de sección.';