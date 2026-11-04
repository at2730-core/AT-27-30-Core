-- Verificación posterior a la proyección CAS completa, SOLO en base temporal.
CREATE TEMP VIEW cas_total_comparison AS
SELECT st.series_id,st.unit_id,st.total_votes AS sec_total,
       count(ct.casilla_id) AS cas_rows,
       sum(ct.total_votes) AS cas_total_crudo,
       sum(ct.total_votes) FILTER (WHERE upper(ct.tribunal)='ANULADA') AS cas_total_anulado,
       count(*) FILTER (WHERE ct.total_votes IS NULL) AS cas_totales_nulos
FROM electoral_stage.section_tally st
JOIN electoral_stage.casilla_tally ct ON ct.series_id=st.series_id AND ct.unit_id=st.unit_id
GROUP BY st.series_id,st.unit_id,st.total_votes;

DO $$
DECLARE
  raw_count bigint; tally_count bigint; option_count bigint; zero_count bigint;
  different_count bigint; explained_count bigint; unexplained_count bigint;
  duplicates_2018 bigint; special_2021 bigint;
BEGIN
  SELECT count(*) INTO raw_count FROM electoral_stage.raw_row rr
      JOIN electoral_stage.series_cas_member scm ON scm.cas_member_id=rr.member_id;
  SELECT count(*) INTO tally_count FROM electoral_stage.casilla_tally;
  SELECT count(*) INTO option_count FROM electoral_stage.casilla_option_vote;
  SELECT count(*) INTO zero_count FROM electoral_stage.casilla_tally ct
      JOIN electoral_stage.computation_unit cu ON cu.unit_id=ct.unit_id
      WHERE cu.section_code='0';
  IF raw_count<>179779 OR tally_count<>179779 OR option_count<>4061868 OR zero_count<>221 THEN
    RAISE EXCEPTION 'Cobertura CAS: raw %, tally %, opciones %, SEC0 %',raw_count,tally_count,option_count,zero_count;
  END IF;
  SELECT count(*) FILTER (WHERE sec_total IS NOT NULL AND cas_totales_nulos=0 AND sec_total<>cas_total_crudo),
         count(*) FILTER (WHERE sec_total IS NOT NULL AND cas_totales_nulos=0 AND sec_total<>cas_total_crudo
             AND sec_total=cas_total_crudo-coalesce(cas_total_anulado,0)),
         count(*) FILTER (WHERE sec_total IS NOT NULL AND cas_totales_nulos=0 AND sec_total<>cas_total_crudo
             AND sec_total IS DISTINCT FROM cas_total_crudo-coalesce(cas_total_anulado,0))
  INTO different_count,explained_count,unexplained_count FROM cas_total_comparison;
  IF different_count<>119 OR explained_count<>119 OR unexplained_count<>0 THEN
    RAISE EXCEPTION 'Identidad SEC/CAS: diferencias %, anuladas explicadas %, residuales %',
      different_count,explained_count,unexplained_count;
  END IF;
  SELECT count(*) INTO duplicates_2018 FROM electoral_stage.casilla_tally ct
      JOIN electoral_stage.election_series es ON es.series_id=ct.series_id
      JOIN electoral_stage.computation_unit cu ON cu.unit_id=ct.unit_id
      WHERE es.election_year=2018 AND es.election_type='A' AND cu.section_code='336'
        AND ct.original_identity->>'TIPO_CASILLA'='C'
        AND ct.original_identity->>'ID_CASILLA'='10';
  IF duplicates_2018<>2 THEN RAISE EXCEPTION 'A18 sección 336 C10: % filas, esperadas 2',duplicates_2018; END IF;
  SELECT count(DISTINCT ct.unit_id) INTO special_2021 FROM electoral_stage.casilla_tally ct
      JOIN electoral_stage.election_series es ON es.series_id=ct.series_id
      JOIN electoral_stage.computation_unit cu ON cu.unit_id=ct.unit_id
      WHERE es.election_year=2021 AND es.election_type='DF' AND es.modality='MR'
        AND cu.section_code='0' AND ct.original_identity->>'TIPO_CASILLA'='P'
        AND ct.original_identity->>'ID_CASILLA'='1';
  IF special_2021<>15 THEN RAISE EXCEPTION 'DF21 SEC0 P1: % unidades, esperadas 15',special_2021; END IF;
  RAISE NOTICE 'CAS 23 series OK: 179779 filas, 4061868 celdas, 221 SEC0, 119 exclusiones explicadas';
END $$;

SELECT es.election_year,es.election_type,es.modality,count(*) AS casillas
FROM electoral_stage.casilla_tally ct JOIN electoral_stage.election_series es ON es.series_id=ct.series_id
GROUP BY 1,2,3 ORDER BY 1,2,3;
