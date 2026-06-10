-- =====================================================
-- AT-27-30 Core
-- Sprint 1 - Territorial Base
-- =====================================================

-- ==========================================
-- territorial.municipio
-- ==========================================

CREATE TABLE territorial.municipio (
    municipio_id SERIAL PRIMARY KEY,
    municipio_code VARCHAR(10),
    municipio_name VARCHAR(150) NOT NULL,
    state VARCHAR(100) DEFAULT 'Guanajuato',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- territorial.distrito_local
-- ==========================================

CREATE TABLE territorial.distrito_local (
    distrito_local_id SERIAL PRIMARY KEY,
    dl_code VARCHAR(10),
    dl_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- territorial.distrito_federal
-- ==========================================

CREATE TABLE territorial.distrito_federal (
    distrito_federal_id SERIAL PRIMARY KEY,
    df_code VARCHAR(10),
    df_name VARCHAR(150) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- territorial.section
-- ==========================================

CREATE TABLE territorial.section (
    section_id BIGSERIAL PRIMARY KEY,

    section_code VARCHAR(20) NOT NULL,

    municipio_id INTEGER,
    distrito_local_id INTEGER,
    distrito_federal_id INTEGER,

    section_type VARCHAR(50),

    current_status VARCHAR(50) DEFAULT 'active',

    source_dataset VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_section_code UNIQUE (section_code),

    CONSTRAINT fk_section_municipio
        FOREIGN KEY (municipio_id)
        REFERENCES territorial.municipio (municipio_id),

    CONSTRAINT fk_section_dl
        FOREIGN KEY (distrito_local_id)
        REFERENCES territorial.distrito_local (distrito_local_id),

    CONSTRAINT fk_section_df
        FOREIGN KEY (distrito_federal_id)
        REFERENCES territorial.distrito_federal (distrito_federal_id)
);

-- ==========================================
-- Índices iniciales
-- ==========================================

CREATE INDEX idx_section_code
    ON territorial.section(section_code);

CREATE INDEX idx_section_status
    ON territorial.section(current_status);

CREATE INDEX idx_section_municipio
    ON territorial.section(municipio_id);