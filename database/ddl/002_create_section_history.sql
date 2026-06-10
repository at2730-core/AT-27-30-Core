-- =====================================================
-- AT-27-30 Core
-- Sprint 1 - Section History
-- =====================================================

CREATE TABLE territorial.section_history (

    section_history_id BIGSERIAL PRIMARY KEY,

    section_id BIGINT NOT NULL,

    valid_from DATE,
    valid_to DATE,

    section_code VARCHAR(20),

    previous_section_code VARCHAR(20),

    previous_section_id BIGINT,

    reason VARCHAR(100),

    geometry_status VARCHAR(50),

    notes TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_section_history_section
        FOREIGN KEY (section_id)
        REFERENCES territorial.section(section_id),

    CONSTRAINT fk_section_history_previous
        FOREIGN KEY (previous_section_id)
        REFERENCES territorial.section(section_id)
);

-- ==========================================
-- Índices
-- ==========================================

CREATE INDEX idx_section_history_section
    ON territorial.section_history(section_id);

CREATE INDEX idx_section_history_previous
    ON territorial.section_history(previous_section_id);

CREATE INDEX idx_section_history_reason
    ON territorial.section_history(reason);