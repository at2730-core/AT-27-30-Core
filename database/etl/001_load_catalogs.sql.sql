-- =====================================================
-- AT-27-30 Core
-- ETL 001 - Load Territorial Catalogs
-- Estado inicial: Guanajuato
-- =====================================================

-- Limpiar catálogos antes de recargar
TRUNCATE TABLE territorial.section_history RESTART IDENTITY CASCADE;
TRUNCATE TABLE territorial.section RESTART IDENTITY CASCADE;
TRUNCATE TABLE territorial.municipio RESTART IDENTITY CASCADE;
TRUNCATE TABLE territorial.distrito_local RESTART IDENTITY CASCADE;
TRUNCATE TABLE territorial.distrito_federal RESTART IDENTITY CASCADE;

-- =====================================================
-- Municipios de Guanajuato
-- =====================================================

INSERT INTO territorial.municipio (municipio_code, municipio_name, state)
VALUES
('1', 'Abasolo', 'Guanajuato'),
('2', 'Acambaro', 'Guanajuato'),
('3', 'San Miguel de Allende', 'Guanajuato'),
('4', 'Apaseo el Alto', 'Guanajuato'),
('5', 'Apaseo el Grande', 'Guanajuato'),
('6', 'Atarjea', 'Guanajuato'),
('7', 'Celaya', 'Guanajuato'),
('8', 'Cd. Manuel Doblado', 'Guanajuato'),
('9', 'Comonfort', 'Guanajuato'),
('10', 'Coroneo', 'Guanajuato'),
('11', 'Cortazar', 'Guanajuato'),
('12', 'Cueramaro', 'Guanajuato'),
('13', 'Doctor Mora', 'Guanajuato'),
('14', 'Dolores Hidalgo', 'Guanajuato'),
('15', 'Guanajuato', 'Guanajuato'),
('16', 'Huanimaro', 'Guanajuato'),
('17', 'Irapuato', 'Guanajuato'),
('18', 'Jaral Del Progreso', 'Guanajuato'),
('19', 'Jerecuaro', 'Guanajuato'),
('20', 'Leon de los Aldama', 'Guanajuato'),
('21', 'Moroleon', 'Guanajuato'),
('22', 'Ocampo', 'Guanajuato'),
('23', 'Penjamo', 'Guanajuato'),
('24', 'Pueblo Nuevo', 'Guanajuato'),
('25', 'Purisima de Bustos', 'Guanajuato'),
('26', 'Romita', 'Guanajuato'),
('27', 'Salamanca', 'Guanajuato'),
('28', 'Salvatierra', 'Guanajuato'),
('29', 'San Diego de la Union', 'Guanajuato'),
('30', 'San Felipe', 'Guanajuato'),
('31', 'San Francisco del Rincon', 'Guanajuato'),
('32', 'San José Iturbide', 'Guanajuato'),
('33', 'San Luis de la Paz', 'Guanajuato'),
('34', 'Santa Catarina', 'Guanajuato'),
('35', 'Santa Cruz de Juventino Rosas', 'Guanajuato'),
('36', 'Santiago Maravatio', 'Guanajuato'),
('37', 'Silao de la Victoria', 'Guanajuato'),
('38', 'Tarandacuao', 'Guanajuato'),
('39', 'Tarimoro', 'Guanajuato'),
('40', 'Tierra Blanca', 'Guanajuato'),
('41', 'Uriangato', 'Guanajuato'),
('42', 'Valle de Santiago', 'Guanajuato'),
('43', 'Victoria', 'Guanajuato'),
('44', 'Villagran', 'Guanajuato'),
('45', 'Xichu', 'Guanajuato'),
('46', 'Yuriria', 'Guanajuato');

-- =====================================================
-- Distritos Locales de Guanajuato
-- =====================================================

INSERT INTO territorial.distrito_local (dl_code, dl_name)
SELECT 
    gs::text,
    'Distrito Local ' || gs::text
FROM generate_series(1, 21) AS gs;

-- =====================================================
-- Distritos Federales de Guanajuato
-- =====================================================

INSERT INTO territorial.distrito_federal (df_code, df_name)
SELECT 
    gs::text,
    'Distrito Federal ' || gs::text
FROM generate_series(1, 15) AS gs;

-- =====================================================
-- Validaciones rápidas
-- =====================================================

SELECT 'municipios' AS catalogo, COUNT(*) AS total
FROM territorial.municipio
UNION ALL
SELECT 'distritos_locales', COUNT(*)
FROM territorial.distrito_local
UNION ALL
SELECT 'distritos_federales', COUNT(*)
FROM territorial.distrito_federal;