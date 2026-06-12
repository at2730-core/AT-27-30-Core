-- =====================================================
-- AT-27-30 Core
-- Sprint 2 - Spatial Base
-- =====================================================

-- ==========================================
-- spatial.section_geometry
-- ==========================================

CREATE TABLE spatial.section_geometry (

    section_id BIGINT PRIMARY KEY,

    geom geometry(MULTIPOLYGON, 4326),

    area_m2 NUMERIC,

    centroid geometry(POINT, 4326),

    geometry_source VARCHAR(255),

    geometry_status VARCHAR(50),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_section_geometry_section
        FOREIGN KEY (section_id)
        REFERENCES territorial.section(section_id)

);

-- ==========================================
-- spatial.casilla_point
-- ==========================================

CREATE TABLE spatial.casilla_point (

    casilla_id BIGSERIAL PRIMARY KEY,

    section_id BIGINT NOT NULL,

    section_code VARCHAR(20),

    geom geometry(POINT, 4326),

    casilla_code VARCHAR(50),

    casilla_name VARCHAR(255),

    casilla_type VARCHAR(50),

    address TEXT,

    localidad VARCHAR(255),

    reference TEXT,

    latitude NUMERIC(12,8),

    longitude NUMERIC(12,8),

    source VARCHAR(255),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_casilla_point_section
        FOREIGN KEY (section_id)
        REFERENCES territorial.section(section_id)

);

-- ==========================================
-- Índices espaciales GiST
-- ==========================================

CREATE INDEX idx_section_geometry_geom
    ON spatial.section_geometry
    USING GIST (geom);

CREATE INDEX idx_section_geometry_centroid
    ON spatial.section_geometry
    USING GIST (centroid);

CREATE INDEX idx_casilla_point_geom
    ON spatial.casilla_point
    USING GIST (geom);

-- ==========================================
-- Índices operativos
-- ==========================================

CREATE INDEX idx_casilla_section
    ON spatial.casilla_point(section_id);

CREATE INDEX idx_casilla_code
    ON spatial.casilla_point(casilla_code);