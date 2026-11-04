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
INSERT INTO electoral_stage.audit_run
(run_id,release_id,importer_version,manifest_sha256,finished_at,status,metrics)
VALUES (-2026100301,10,'A2024_CONFLICT_ROLLBACK_PROBE_v0_1','b98968050574fb6af9d849d57bfee8aeadb87fcd9e5eb545d0625edcc9705c88',now(),
 'TECHNICAL_PROBE_NOT_CERTIFICATION',
 jsonb_build_object('series_id',16,'restored_cas_count',4,'restored_raw_votes',1371,
 'writes_results',false,'ends_with_rollback',true));
INSERT INTO electoral_stage.reconciliation_issue
(issue_id,run_id,series_id,unit_id,issue_code,field_name,expected_value,observed_value,evidence,resolution_status)
VALUES (-2026100301,-2026100301,16,NULL,'JUDICIAL_CUT_CONFLICT','MUNICIPAL_TOTAL_VOTES',
 '76757','75386',jsonb_build_object(
 'municipality_code','3','municipality','SAN MIGUEL DE ALLENDE',
 'metric_scope','RESULT','scope','SERIES_CONSERVATIVE_BLOCK',
 'expected_origin','Judicial total documented in prior audit; not a new certification',
 'observed_origin','SICEE MUN total documented in prior audit; not a staging MUN row',
 'evidence_report','HEYTI_Registro_Municipal_A2024_46_v0_1(1).md',
 'evidence_report_sha256','b98968050574fb6af9d849d57bfee8aeadb87fcd9e5eb545d0625edcc9705c88',
 'case_refs',jsonb_build_array('SM-JDC-517/2024','SUP-REC-22097/2024'),
 'delta',1371,'excluded_annulled_cas','156 C04',
 'cas_rows',(SELECT jsonb_agg(to_jsonb(e) ORDER BY casilla_id) FROM heyti_expected_cas e)), 'OPEN');
DO $heyti$
BEGIN
 IF (SELECT count(*) FROM electoral_stage.reconciliation_issue
 WHERE issue_id=-2026100301 AND run_id=-2026100301 AND series_id=16
 AND unit_id IS NULL AND resolution_status='OPEN')<>1 THEN
 RAISE EXCEPTION 'Incidencia no quedó vinculada a A2024'; END IF;
 RAISE NOTICE 'ENSAYO OK: 4 CAS, 1371 votos, incidencia OPEN solo serie 16; sin certificación';
END $heyti$;
SELECT issue_id,series_id,issue_code,expected_value,observed_value,resolution_status
FROM electoral_stage.reconciliation_issue WHERE issue_id=-2026100301;
ROLLBACK;
SELECT
 (SELECT count(*) FROM electoral_stage.audit_run WHERE run_id=-2026100301) AS auditorias_ensayo_restantes,
 (SELECT count(*) FROM electoral_stage.reconciliation_issue WHERE issue_id=-2026100301) AS incidencias_ensayo_restantes;
