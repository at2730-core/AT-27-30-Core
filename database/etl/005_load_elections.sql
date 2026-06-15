-- =====================================================
-- AT-27-30 CORE
-- ETL 005
-- Catálogo de Elecciones
-- =====================================================

INSERT INTO electoral.election
(
    election_year,
    election_type,
    election_name,
    election_scope
)
VALUES

-- 2015
(2015,'A','Ayuntamiento 2015','MUNICIPAL'),
(2015,'DF','Diputado Federal 2015','FEDERAL'),
(2015,'DL','Diputado Local 2015','ESTATAL'),

-- 2018
(2018,'A','Ayuntamiento 2018','MUNICIPAL'),
(2018,'DF','Diputado Federal 2018','FEDERAL'),
(2018,'DL','Diputado Local 2018','ESTATAL'),
(2018,'G','Gobernador 2018','ESTATAL'),
(2018,'P','Presidente 2018','FEDERAL'),
(2018,'S','Senado 2018','FEDERAL'),

-- 2021
(2021,'A','Ayuntamiento 2021','MUNICIPAL'),
(2021,'DF','Diputado Federal 2021','FEDERAL'),
(2021,'DL','Diputado Local 2021','ESTATAL'),

-- 2024
(2024,'A','Ayuntamiento 2024','MUNICIPAL'),
(2024,'DF','Diputado Federal 2024','FEDERAL'),
(2024,'DL','Diputado Local 2024','ESTATAL'),
(2024,'G','Gobernador 2024','ESTATAL'),
(2024,'P','Presidente 2024','FEDERAL'),
(2024,'S','Senado 2024','FEDERAL')

ON CONFLICT DO NOTHING;