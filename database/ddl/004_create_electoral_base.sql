-- =====================================================
-- AT-27-30 CORE
-- Sprint 3 - Electoral
-- 004_create_electoral_base.sql
-- =====================================================

CREATE SCHEMA IF NOT EXISTS electoral;

-- =====================================================
-- Tabla: election
-- Catálogo de elecciones
-- =====================================================

CREATE TABLE IF NOT EXISTS electoral.election
(
    election_id         BIGSERIAL PRIMARY KEY,

    election_year       INTEGER NOT NULL,

    election_type       VARCHAR(20) NOT NULL,

    election_name       VARCHAR(100) NOT NULL,

    election_scope      VARCHAR(20) NOT NULL,

    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    UNIQUE (election_year, election_type)
);

COMMENT ON TABLE electoral.election IS
'Catálogo de elecciones. Ej: 2024 Ayuntamiento, 2024 Diputado Federal';

-- =====================================================
-- Tabla: party
-- Catálogo de partidos
-- =====================================================

CREATE TABLE IF NOT EXISTS electoral.party
(
    party_id            BIGSERIAL PRIMARY KEY,

    party_code          VARCHAR(20) NOT NULL UNIQUE,

    party_name          VARCHAR(100) NOT NULL,

    active_flag         BOOLEAN DEFAULT TRUE,

    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE electoral.party IS
'Catálogo de partidos políticos';

-- =====================================================
-- Tabla: section_result
-- Resultados por sección
-- =====================================================

CREATE TABLE IF NOT EXISTS electoral.section_result
(
    result_id           BIGSERIAL PRIMARY KEY,

    section_id          BIGINT NOT NULL,

    election_id         BIGINT NOT NULL,

    party_id            BIGINT NOT NULL,

    votes               INTEGER NOT NULL,

    total_votes         INTEGER,

    nominal_list        INTEGER,

    participation_pct   NUMERIC(6,2),

    created_at          TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_result_section
        FOREIGN KEY (section_id)
        REFERENCES territorial.section(section_id),

    CONSTRAINT fk_result_election
        FOREIGN KEY (election_id)
        REFERENCES electoral.election(election_id),

    CONSTRAINT fk_result_party
        FOREIGN KEY (party_id)
        REFERENCES electoral.party(party_id),

    CONSTRAINT uq_section_election_party
        UNIQUE
        (
            section_id,
            election_id,
            party_id
        )
);

COMMENT ON TABLE electoral.section_result IS
'Resultados electorales por sección, elección y partido';

-- =====================================================
-- Índices
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_result_section
ON electoral.section_result(section_id);

CREATE INDEX IF NOT EXISTS idx_result_election
ON electoral.section_result(election_id);

CREATE INDEX IF NOT EXISTS idx_result_party
ON electoral.section_result(party_id);