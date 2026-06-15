-- =====================================================
-- AT-27-30 CORE
-- Sprint 4 - Socioeconomico
-- 005_create_socioeconomico_base.sql
-- =====================================================

CREATE SCHEMA IF NOT EXISTS socioeconomico;

CREATE TABLE IF NOT EXISTS socioeconomico.section_indicator
(
    section_indicator_id BIGSERIAL PRIMARY KEY,

    section_id           BIGINT NOT NULL,

    indicator_code       VARCHAR(100) NOT NULL,
    indicator_name       VARCHAR(150),
    indicator_value      NUMERIC,
    indicator_category   VARCHAR(100),

    source_dataset       VARCHAR(150) DEFAULT 'Datos_Socioeconomicos.json',
    created_at           TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_socio_section
        FOREIGN KEY (section_id)
        REFERENCES territorial.section(section_id),

    CONSTRAINT uq_section_indicator
        UNIQUE (section_id, indicator_code)
);

CREATE INDEX IF NOT EXISTS idx_socio_section
ON socioeconomico.section_indicator(section_id);

CREATE INDEX IF NOT EXISTS idx_socio_indicator_code
ON socioeconomico.section_indicator(indicator_code);