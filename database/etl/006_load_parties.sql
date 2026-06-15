-- =====================================================
-- AT-27-30 CORE
-- ETL 006
-- Catálogo de Partidos
-- =====================================================

INSERT INTO electoral.party
(
    party_code,
    party_name
)
VALUES

('PAN','Partido Acción Nacional'),
('PRI','Partido Revolucionario Institucional'),
('PVEM','Partido Verde Ecologista de México'),
('MORENA','Movimiento Regeneración Nacional'),
('PRD','Partido de la Revolución Democrática'),
('PT','Partido del Trabajo'),
('MC','Movimiento Ciudadano'),
('NA','Nueva Alianza'),

('INDEPENDIENTE','Candidatura Independiente'),
('NULOS','Votos Nulos'),
('OTROS','Otros')

ON CONFLICT DO NOTHING;