-- Ejecutar solo en base temporal tras carga cruda. No escribe tablas persistentes.
CREATE TEMP TABLE expected_member_rows(member_path text PRIMARY KEY, expected_rows bigint NOT NULL);
INSERT INTO expected_member_rows(member_path,expected_rows) VALUES
  ('DIPUTACIONES_FED_MR_2018/2018_SEE_DIP_FED_MR_NAL_SEC.csv',3137),
  ('DIPUTACIONES_FED_MR_2021/2021_SEE_DIP_FED_MR_NAL_SEC.csv',3174),
  ('DIPUTACIONES_FED_MR_2024/CSV/2024_SEE_DIP_FED_MR_NAL_SEC.csv',3233),
  ('DIPUTACIONES_FED_RP_2018/2018_SEE_DIP_FED_RP_NAL_SEC.csv',3137),
  ('DIPUTACIONES_FED_RP_2021/2021_SEE_DIP_FED_RP_NAL_SEC.csv',3174),
  ('DIPUTACIONES_FED_RP_2024/CSV/2024_SEE_DIP_FED_RP_NAL_SEC.csv',3233),
  ('GTO_PEL_2018/AYUNTAMIENTOS_csv/2018_SEE_AYUN_GTO_SEC.csv',3137),
  ('GTO_PEL_2018/DIPUTACIONES_LOC_MR_csv/2018_SEE_DIP_LOC_MR_GTO_SEC.csv',3137),
  ('GTO_PEL_2018/DIPUTACIONES_LOC_RP_csv/2018_SEE_DIP_LOC_RP_GTO_SEC.csv',3137),
  ('GTO_PEL_2018/GUBERNATURA_csv/2018_SEE_GOB_GTO_SEC.csv',3138),
  ('GTO_PEL_2021/AYUNTAMIENTOS_csv/2021_SEE_AYUN_GTO_SEC.csv',3159),
  ('GTO_PEL_2021/DIPUTACIONES_LOC_MR_csv/2021_SEE_DIP_LOC_MR_GTO_SEC.csv',3159),
  ('GTO_PEL_2021/DIPUTACIONES_LOC_RP_csv/2021_SEE_DIP_LOC_RP_GTO_SEC.csv',3159),
  ('GTO_PEL_2024/AYUNTAMIENTOS_csv/2024_SEE_AYUN_GTO_SEC.csv',3257),
  ('GTO_PEL_2024/DIPUTACIONES LOC_MR_csv/2024_SEE_DIP_LOC_MR_GTO_SEC.csv',3258),
  ('GTO_PEL_2024/DIPUTACIONES LOC_RP_csv/2024_SEE_DIP_LOC_RP_GTO_SEC.csv',3258),
  ('GTO_PEL_2024/GUBERNATURA_csv/2024_SEE_GOB_GTO_SEC.csv',3259),
  ('PRESIDENCIA_2018/2018_SEE_PRE_NAL_SEC.csv',3138),
  ('PRESIDENCIA_2024/CSV/2024_SEE_PRE_NAL_SEC.csv',3234),
  ('SENADURIAS_MR_2018/2018_SEE_SEN_MR_NAL_SEC.csv',3138),
  ('SENADURÍAS_MR_2024/CSV/2024_SEE_SEN_FED_MR_NAL_SEC.csv',3234),
  ('SENADURIAS_RP_2018/2018_SEE_SEN_RP_NAL_SEC.csv',3138),
  ('SENADURÍAS_RP_2024/CSV/2024_SEE_SEN_FED_RP_NAL_SEC.csv',3234);
DO $$ BEGIN
 IF (SELECT count(*) FROM electoral_stage.source_release)<>15 OR
    (SELECT count(*) FROM electoral_stage.source_member)<>23 OR
    (SELECT count(*) FROM electoral_stage.election_series)<>23 OR
    (SELECT count(*) FROM electoral_stage.raw_row)<>73262 THEN
   RAISE EXCEPTION 'Conteos 15/23/23/73262 no cumplen'; END IF;
 IF EXISTS (
   SELECT 1 FROM expected_member_rows e
   LEFT JOIN electoral_stage.source_member m ON m.member_path=e.member_path
   LEFT JOIN electoral_stage.raw_row r ON r.member_id=m.member_id
   GROUP BY e.member_path,e.expected_rows
   HAVING count(r.raw_row_id)<>e.expected_rows OR count(DISTINCT m.member_id)<>1
 ) THEN RAISE EXCEPTION 'Conteo por miembro discrepante'; END IF;
 IF EXISTS (SELECT 1 FROM electoral_stage.raw_row
            WHERE raw_cells->>'ID_ESTADO' IS DISTINCT FROM '11') THEN
   RAISE EXCEPTION 'Fila fuera de GTO'; END IF;
 IF (SELECT count(*) FROM electoral_stage.raw_row
     WHERE raw_cells->>'SECCION'='0')<>137 THEN
   RAISE EXCEPTION 'SEC=0 distinta de 137'; END IF;
 RAISE NOTICE 'Carga cruda OK: 15 ZIP, 23 series, 73262 filas GTO, 137 SEC=0';
END $$;
SELECT s.election_year,s.election_type,s.modality,count(r.raw_row_id) AS filas_gto
FROM electoral_stage.election_series s
JOIN electoral_stage.source_member m ON m.member_id=s.member_id
LEFT JOIN electoral_stage.raw_row r ON r.member_id=m.member_id
GROUP BY s.series_id,s.election_year,s.election_type,s.modality
ORDER BY s.election_year,s.election_type,s.modality;
