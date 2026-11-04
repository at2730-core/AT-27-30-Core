-- Ensayo exclusivo de base aislada. No certifica ni corrige votos.
-- IDs negativos explícitos evitan consumir secuencias durante el ROLLBACK.
BEGIN;
CREATE TEMP TABLE heyti_expected_cas (
 casilla_id bigint PRIMARY KEY, unit_key text, literal_acta text,
 votes bigint, source_line bigint, row_hash text
) ON COMMIT DROP;
INSERT INTO heyti_expected_cas VALUES
(122857,'SEC:156','C01',361,343,'4657e55d7bcc3c2a1873eeb739be831ebbcdcedd7483a7707bc25c9d75adcd07'),
(122901,'SEC:172','B',453,387,'085f1f58ca4b460f84db3f8a19ec293375da72955e208b1993320e789086b01f'),
(122956,'SEC:191','B',284,442,'4b695c93bfec3c7b5096c67a266e5dd5d78c29d907000489ba68f9430113b289'),
(122973,'SEC:200','E01',273,459,'4c011ad31a0f287a1298f4be082611014dd5095fe3f7ee97f35720c67863b1b0');
DO $heyti$
DECLARE matched integer;
BEGIN
 IF current_database() <> 'heyti_cas_full_probe_d12d6718adb8' THEN
   RAISE EXCEPTION 'Base no autorizada para este ensayo'; END IF;
 IF (SELECT count(*) FROM electoral_stage.source_release sr
 JOIN electoral_stage.source_member sm ON sm.release_id=sr.release_id
 JOIN electoral_stage.election_series es ON es.member_id=sm.member_id
 WHERE sr.release_id=10 AND es.series_id=16
 AND sr.outer_zip_sha256='13fe6a2ddb432922bddc9090f08eb0e558aeb3094ef1ba763b78d789b3d55e69'
 AND sr.cut_label='SOURCE_AS_PUBLISHED_UNVERIFIED_DATE'
 AND sm.member_path='GTO_PEL_2024/AYUNTAMIENTOS_csv/2024_SEE_AYUN_GTO_SEC.csv'
 AND sm.member_sha256='b6f952da0c32b7e2750a0d40c1f14e10ed915685525da8347962e224c1c9502f'
 AND es.election_year=2024 AND es.election_type='A' AND es.modality='UNICA'
 AND es.geography='GTO' AND es.aggregation_level='SECTION'
 AND es.judicial_cut='SOURCE_AS_PUBLISHED') <> 1 THEN
 RAISE EXCEPTION 'Identidad de fuente/serie no coincide'; END IF;
 SELECT count(*) INTO matched FROM heyti_expected_cas e
 JOIN electoral_stage.casilla_tally c ON c.casilla_id=e.casilla_id
 JOIN electoral_stage.computation_unit u ON u.unit_id=c.unit_id AND u.series_id=c.series_id
 JOIN electoral_stage.raw_row rr ON rr.raw_row_id=c.raw_row_id AND rr.member_id=c.cas_member_id
 JOIN electoral_stage.source_member cm ON cm.member_id=c.cas_member_id
 WHERE c.series_id=16 AND u.unit_key=e.unit_key AND u.municipality_code='3'
 AND c.original_identity->>'ACTA_CASILLA-MEC'=e.literal_acta
 AND c.total_votes=e.votes AND c.total_raw=e.votes::text AND c.tribunal='ANULADA'
 AND rr.source_line=e.source_line AND rr.raw_line_sha256=e.row_hash
 AND cm.release_id=10
 AND cm.member_path='GTO_PEL_2024/AYUNTAMIENTOS_csv/2024_SEE_AYUN_GTO_CAS.csv'
 AND cm.member_sha256='90cb61ac6e71b0b5ce4486850107195dde5b2aedc8fb7813b3c967de4192907f';
 IF matched<>4 OR (SELECT sum(votes) FROM heyti_expected_cas)<>1371 THEN
 RAISE EXCEPTION 'No coinciden las cuatro casillas y sus hashes'; END IF;
 IF EXISTS (SELECT 1 FROM electoral_stage.audit_run WHERE run_id=-2026100301)
 OR EXISTS (SELECT 1 FROM electoral_stage.reconciliation_issue WHERE issue_id=-2026100301) THEN
 RAISE EXCEPTION 'IDs de ensayo ya ocupados'; END IF;
 IF EXISTS (SELECT 1 FROM electoral_stage.reconciliation_issue i
 JOIN electoral_stage.audit_run ar ON ar.run_id=i.run_id
 WHERE ar.release_id=10 AND i.series_id=16 AND i.issue_code='JUDICIAL_CUT_CONFLICT'
 AND i.resolution_status<>'RESOLVED') THEN
 RAISE EXCEPTION 'Ya existe incidencia abierta: revisar antes de duplicar'; END IF;
END $heyti$;

-- Solo tablas temporales: no crea un corte persistente.
CREATE TEMP TABLE heyti_expected_options (
 casilla_id bigint, ordinal integer, votes bigint, PRIMARY KEY(casilla_id,ordinal)
) ON COMMIT DROP;
INSERT INTO heyti_expected_options VALUES
(122857,11,70),
(122857,12,124),
(122857,13,6),
(122857,14,4),
(122857,15,3),
(122857,16,11),
(122857,17,116),
(122857,18,0),
(122857,19,0),
(122857,20,0),
(122857,21,0),
(122857,22,0),
(122857,23,10),
(122857,24,0),
(122857,25,344),
(122857,26,0),
(122857,27,17),
(122901,11,87),
(122901,12,179),
(122901,13,3),
(122901,14,2),
(122901,15,0),
(122901,16,6),
(122901,17,156),
(122901,18,0),
(122901,19,0),
(122901,20,0),
(122901,21,0),
(122901,22,0),
(122901,23,11),
(122901,24,0),
(122901,25,444),
(122901,26,1),
(122901,27,8),
(122956,11,70),
(122956,12,104),
(122956,13,2),
(122956,14,5),
(122956,15,8),
(122956,16,3),
(122956,17,67),
(122956,18,0),
(122956,19,0),
(122956,20,0),
(122956,21,0),
(122956,22,0),
(122956,23,2),
(122956,24,0),
(122956,25,261),
(122956,26,0),
(122956,27,23),
(122973,11,73),
(122973,12,86),
(122973,13,4),
(122973,14,6),
(122973,15,1),
(122973,16,5),
(122973,17,83),
(122973,18,0),
(122973,19,0),
(122973,20,0),
(122973,21,0),
(122973,22,0),
(122973,23,4),
(122973,24,0),
(122973,25,262),
(122973,26,0),
(122973,27,11);
DO $heyti$
BEGIN
 IF (SELECT count(*) FROM heyti_expected_options e
 JOIN electoral_stage.casilla_option_vote v ON v.casilla_id=e.casilla_id AND v.series_id=16
 JOIN electoral_stage.option_column o ON o.option_id=v.option_id AND o.series_id=v.series_id
 WHERE o.column_ordinal=e.ordinal AND v.votes=e.votes AND v.raw_value=e.votes::text)<>68 THEN
 RAISE EXCEPTION 'El vector de 68 celdas CAS no coincide'; END IF;
 IF (SELECT count(*) FROM electoral_stage.computation_unit WHERE series_id=16 AND municipality_code='3')<>106 THEN
 RAISE EXCEPTION 'Cobertura municipal SEC distinta'; END IF;
 IF (SELECT count(*) FROM electoral_stage.option_column WHERE series_id=16)<>17 THEN
 RAISE EXCEPTION 'Catálogo de opciones distinto'; END IF;
END $heyti$;
CREATE TEMP TABLE heyti_derived_totals ON COMMIT DROP AS
SELECT u.unit_id,u.unit_key,u.unit_kind,t.total_votes AS base_total,
 COALESCE(a.delta,0) AS delta,t.total_votes+COALESCE(a.delta,0) AS derived_total
FROM electoral_stage.computation_unit u
LEFT JOIN electoral_stage.section_tally t ON t.unit_id=u.unit_id AND t.series_id=u.series_id
LEFT JOIN (SELECT c.unit_id,sum(e.votes) AS delta
 FROM heyti_expected_cas e JOIN electoral_stage.casilla_tally c ON c.casilla_id=e.casilla_id
 GROUP BY c.unit_id) a ON a.unit_id=u.unit_id
WHERE u.series_id=16 AND u.municipality_code='3';
CREATE TEMP TABLE heyti_derived_options ON COMMIT DROP AS
SELECT u.unit_id,u.unit_key,o.column_ordinal,o.literal_header,o.option_type,
 v.votes AS base_votes,COALESCE(a.delta,0) AS delta,
 v.votes+COALESCE(a.delta,0) AS derived_votes
FROM electoral_stage.computation_unit u
JOIN electoral_stage.option_column o ON o.series_id=u.series_id
LEFT JOIN electoral_stage.section_tally t ON t.unit_id=u.unit_id AND t.series_id=u.series_id
LEFT JOIN electoral_stage.option_vote v ON v.tally_id=t.tally_id AND v.series_id=t.series_id AND v.option_id=o.option_id
LEFT JOIN (SELECT c.unit_id,e.ordinal,sum(e.votes) AS delta
 FROM heyti_expected_options e JOIN electoral_stage.casilla_tally c ON c.casilla_id=e.casilla_id
 GROUP BY c.unit_id,e.ordinal) a ON a.unit_id=u.unit_id AND a.ordinal=o.column_ordinal
WHERE u.series_id=16 AND u.municipality_code='3';
CREATE TEMP TABLE heyti_judicial_expected(ordinal integer PRIMARY KEY,base_votes bigint,derived_votes bigint) ON COMMIT DROP;
INSERT INTO heyti_judicial_expected VALUES
(11,15196,15496),(12,25520,26013),(13,663,678),(14,1130,1147),
(15,1052,1064),(16,1725,1750),(17,25031,25453),
(18,0,0),(19,0,0),(20,0,0),(21,0,0),(22,0,0),
(23,1884,1911),(24,0,0),(25,72201,73512),(26,20,21),(27,3165,3224);
DO $heyti$
BEGIN
 IF (SELECT count(*) FROM heyti_derived_totals)<>106
 OR EXISTS(SELECT 1 FROM heyti_derived_totals WHERE base_total IS NULL)
 OR (SELECT sum(base_total) FROM heyti_derived_totals)<>75386
 OR (SELECT sum(delta) FROM heyti_derived_totals)<>1371
 OR (SELECT sum(derived_total) FROM heyti_derived_totals)<>76757
 OR (SELECT count(*) FROM heyti_derived_totals WHERE delta<>0)<>4 THEN
 RAISE EXCEPTION 'Cobertura o totales de derivación no coinciden'; END IF;
 IF (SELECT count(*) FROM heyti_derived_options)<>1802
 OR EXISTS(SELECT 1 FROM heyti_derived_options WHERE base_votes IS NULL)
 OR EXISTS(SELECT 1 FROM heyti_judicial_expected e
 LEFT JOIN (SELECT column_ordinal,sum(base_votes) b,sum(derived_votes) d FROM heyti_derived_options GROUP BY column_ordinal) a
 ON a.column_ordinal=e.ordinal WHERE a.b IS DISTINCT FROM e.base_votes OR a.d IS DISTINCT FROM e.derived_votes) THEN
 RAISE EXCEPTION 'Vector municipal de derivación no coincide'; END IF;
 IF EXISTS(SELECT 1 FROM heyti_derived_totals t
 JOIN (SELECT unit_id,
 sum(derived_votes) FILTER(WHERE option_type<>'VALID_VOTE_TOTAL') AS total_from_options,
 sum(derived_votes) FILTER(WHERE option_type IN ('PARTY','COALITION_COMBINATION','INDEPENDENT')) AS valid_from_options,
 max(derived_votes) FILTER(WHERE option_type='VALID_VOTE_TOTAL') AS valid_control
 FROM heyti_derived_options GROUP BY unit_id) a ON a.unit_id=t.unit_id
 WHERE a.total_from_options IS DISTINCT FROM t.derived_total
 OR a.valid_from_options IS DISTINCT FROM a.valid_control) THEN
 RAISE EXCEPTION 'Alguna sección derivada falla control aritmético'; END IF;
 RAISE NOTICE 'DERIVACION TEMPORAL OK: 106 unidades, 1802 celdas, 4 secciones restituidas; 75386 + 1371 = 76757';
END $heyti$;
SELECT unit_key,base_total,delta,derived_total FROM heyti_derived_totals WHERE delta<>0 ORDER BY unit_key;
SELECT column_ordinal,literal_header,option_type,sum(base_votes) AS base,sum(delta) AS agregado,sum(derived_votes) AS derivado
FROM heyti_derived_options GROUP BY column_ordinal,literal_header,option_type ORDER BY column_ordinal;
ROLLBACK;
SELECT to_regclass('pg_temp.heyti_derived_totals') IS NULL
 AND to_regclass('pg_temp.heyti_derived_options') IS NULL AS temporales_eliminadas;
