-- Ejecutar exclusivamente en base temporal después de 001, 004 y DDL propuesto.
-- ON_ERROR_STOP=1. La transacción de datos de prueba se revierte al final.
DO $$
DECLARE n integer;
BEGIN
 SELECT count(*) INTO n FROM information_schema.tables
 WHERE table_schema='electoral_stage' AND table_type='BASE TABLE';
 IF n <> 11 THEN RAISE EXCEPTION 'Tablas staging: esperadas 11; encontradas %', n; END IF;
 IF NOT EXISTS (SELECT 1 FROM information_schema.columns
       WHERE table_schema='electoral_stage' AND table_name='computation_unit'
         AND column_name='territorial_section_id' AND is_nullable='YES')
 THEN RAISE EXCEPTION 'FK territorial histórica no nullable'; END IF;
END $$;

BEGIN;
DO $$
DECLARE
 rel bigint; mem bigint; ser bigint; ser2 bigint; raw bigint;
 unit bigint; special bigint; tally bigint; opt bigint; opt2 bigint; opt3 bigint;
BEGIN
 INSERT INTO electoral_stage.source_release(authority,source_name,cut_label,outer_zip_sha256)
 VALUES('INE/SICEE','fixture','SOURCE_AS_PUBLISHED',repeat('a',64)) RETURNING release_id INTO rel;
 INSERT INTO electoral_stage.source_member(release_id,member_path,member_sha256,header_columns)
 VALUES(rel,'fixture/SEC.csv',repeat('b',64),'["SECCION","PAN"]'::jsonb)
 RETURNING member_id INTO mem;
 INSERT INTO electoral_stage.election_series(member_id,election_year,election_type,modality,aggregation_level)
 VALUES(mem,2021,'DF','MR','SECTION') RETURNING series_id INTO ser;
 INSERT INTO electoral_stage.election_series(member_id,election_year,election_type,modality,aggregation_level)
 VALUES(mem,2021,'DF','RP','SECTION') RETURNING series_id INTO ser2;
 INSERT INTO electoral_stage.raw_row(member_id,source_line,raw_cells,raw_line_sha256)
 VALUES(mem,2,'{"SECCION":"343","PAN":"0"}'::jsonb,repeat('c',64))
 RETURNING raw_row_id INTO raw;
 INSERT INTO electoral_stage.computation_unit(series_id,unit_key,unit_kind,section_code,original_identity)
 VALUES(ser,'2021-DF-MR-343','ORDINARY_SECTION','343','{"SECCION":"343"}'::jsonb)
 RETURNING unit_id INTO unit;
 INSERT INTO electoral_stage.computation_unit(series_id,unit_key,unit_kind,section_code,original_identity)
 VALUES(ser,'2021-DF-MR-SEC0-D1','SPECIAL_SECTION_ROW','0','{"SECCION":"0","DF":"1"}'::jsonb)
 RETURNING unit_id INTO special;
 INSERT INTO electoral_stage.option_column(series_id,literal_header,column_ordinal,option_type)
 VALUES(ser,'PAN',1,'PARTY') RETURNING option_id INTO opt;
 INSERT INTO electoral_stage.option_column(series_id,literal_header,column_ordinal,option_type)
 VALUES(ser2,'PAN',1,'PARTY') RETURNING option_id INTO opt2;
 INSERT INTO electoral_stage.option_column(series_id,literal_header,column_ordinal,option_type)
 VALUES(ser,'PRI',2,'PARTY') RETURNING option_id INTO opt3;
 INSERT INTO electoral_stage.section_tally(series_id,member_id,unit_id,raw_row_id,
   total_votes,nominal_list,total_cause,nominal_cause,total_truth_status)
 VALUES(ser,mem,unit,raw,NULL,NULL,'ANNULLED','NOT_PUBLISHED','SOURCE_MISSING')
 RETURNING tally_id INTO tally;
 INSERT INTO electoral_stage.option_vote(series_id,tally_id,option_id,votes,raw_value,truth_status)
 VALUES(ser,tally,opt,0,'0','OFFICIAL_ZERO');
 IF (SELECT territorial_section_id FROM electoral_stage.computation_unit WHERE unit_id=unit) IS NOT NULL
 THEN RAISE EXCEPTION 'La sección histórica adquirió FK actual'; END IF;
 IF (SELECT unit_kind FROM electoral_stage.computation_unit WHERE unit_id=special)<>'SPECIAL_SECTION_ROW'
 THEN RAISE EXCEPTION 'SEC0 se confundió con sección ordinaria'; END IF;
 BEGIN
   INSERT INTO electoral_stage.option_vote(series_id,tally_id,option_id,votes,raw_value)
   VALUES(ser,tally,opt2,1,'1');
   RAISE EXCEPTION 'ERROR: aceptó opción de otra modalidad';
 EXCEPTION WHEN foreign_key_violation THEN NULL; END;
 BEGIN
   INSERT INTO electoral_stage.option_vote(series_id,tally_id,option_id,votes,raw_value,missing_cause)
   VALUES(ser,tally,opt3,NULL,'',NULL);
   RAISE EXCEPTION 'ERROR: aceptó NULL sin causa';
 EXCEPTION WHEN check_violation THEN NULL; END;
 RAISE NOTICE 'Prueba staging v0.1: 11 tablas, identidad histórica, SEC0, MR/RP, NULL y cero: OK';
END $$;
ROLLBACK;
