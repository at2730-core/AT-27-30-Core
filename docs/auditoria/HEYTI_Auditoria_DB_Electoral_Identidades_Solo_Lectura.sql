-- HEYTI, 25-09-2026. Solo lectura; no modifica la base.
-- Confirma identidad de G 2018/2024 y conjuntos de secciones A/DL 2021.

WITH g18 AS (
    SELECT r.section_id, r.party_id, r.votes, r.total_votes, r.nominal_list
    FROM electoral.section_result r
    JOIN electoral.election e ON e.election_id = r.election_id
    WHERE e.election_year = 2018 AND e.election_type = 'G'
), g24 AS (
    SELECT r.section_id, r.party_id, r.votes, r.total_votes, r.nominal_list
    FROM electoral.section_result r
    JOIN electoral.election e ON e.election_id = r.election_id
    WHERE e.election_year = 2024 AND e.election_type = 'G'
)
SELECT '01_G_2018_2024_DB' AS bloque,
       COUNT(*) AS pares_seccion_partido,
       COUNT(*) FILTER (WHERE g18.section_id IS NULL) AS solo_2024,
       COUNT(*) FILTER (WHERE g24.section_id IS NULL) AS solo_2018,
       COUNT(*) FILTER (
           WHERE g18.section_id IS NOT NULL AND g24.section_id IS NOT NULL
             AND (g18.votes, g18.total_votes, g18.nominal_list)
                 IS DISTINCT FROM
                 (g24.votes, g24.total_votes, g24.nominal_list)
       ) AS pares_con_algun_valor_distinto
FROM g18 FULL OUTER JOIN g24
  ON g18.section_id = g24.section_id AND g18.party_id = g24.party_id;

WITH a21 AS (
    SELECT DISTINCT r.section_id
    FROM electoral.section_result r
    JOIN electoral.election e ON e.election_id = r.election_id
    WHERE e.election_year = 2021 AND e.election_type = 'A'
), dl21 AS (
    SELECT DISTINCT r.section_id
    FROM electoral.section_result r
    JOIN electoral.election e ON e.election_id = r.election_id
    WHERE e.election_year = 2021 AND e.election_type = 'DL'
)
SELECT '02_A_vs_DL_2021_DB' AS bloque,
       COUNT(*) AS secciones_en_union,
       COUNT(*) FILTER (WHERE a21.section_id IS NOT NULL
                         AND dl21.section_id IS NULL) AS solo_A,
       COUNT(*) FILTER (WHERE a21.section_id IS NULL
                         AND dl21.section_id IS NOT NULL) AS solo_DL,
       COUNT(*) FILTER (WHERE a21.section_id IS NOT NULL
                         AND dl21.section_id IS NOT NULL) AS compartidas
FROM a21 FULL OUTER JOIN dl21 ON a21.section_id = dl21.section_id;

WITH a21 AS (
    SELECT DISTINCT r.section_id
    FROM electoral.section_result r
    JOIN electoral.election e ON e.election_id = r.election_id
    WHERE e.election_year = 2021 AND e.election_type = 'A'
), dl21 AS (
    SELECT DISTINCT r.section_id
    FROM electoral.section_result r
    JOIN electoral.election e ON e.election_id = r.election_id
    WHERE e.election_year = 2021 AND e.election_type = 'DL'
)
SELECT '03_solo_A_2021_claves' AS bloque,
       s.section_code
FROM a21
LEFT JOIN dl21 ON dl21.section_id = a21.section_id
JOIN territorial.section s ON s.section_id = a21.section_id
WHERE dl21.section_id IS NULL
ORDER BY s.section_code::integer;
