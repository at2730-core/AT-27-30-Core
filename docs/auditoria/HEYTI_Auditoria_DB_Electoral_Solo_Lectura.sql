-- HEYTI / auditoría electoral, 25-09-2026.
-- Solo lectura. Ejecutar contra la base local de HEYTI-CORE y guardar la salida.
-- No modifica tablas ni presupone que el ETL 008 se haya ejecutado.
-- Las cifras mostradas por la base son legado; este archivo no las certifica.

SELECT '01_catalogo_elecciones' AS bloque,
       e.election_year, e.election_type, e.election_id,
       COUNT(r.result_id) AS filas_resultado,
       COUNT(DISTINCT r.section_id) AS secciones,
       COUNT(DISTINCT r.party_id) AS partidos,
       COUNT(r.result_id) FILTER (WHERE r.total_votes IS NULL) AS filas_total_nulo,
       COUNT(r.result_id) FILTER (WHERE r.nominal_list IS NULL) AS filas_ln_nula
FROM electoral.election e
LEFT JOIN electoral.section_result r ON r.election_id = e.election_id
WHERE e.election_year IN (2018, 2021, 2024)
GROUP BY e.election_year, e.election_type, e.election_id
ORDER BY e.election_year, e.election_type;

-- Los totales están repetidos por partido en el modelo legado.
-- Este bloque cuenta valores distintos del total por sección, sin sumar partidos.
SELECT '02_inconsistencia_interna' AS bloque,
       e.election_year, e.election_type,
       COUNT(*) AS secciones_con_resultado,
       COUNT(*) FILTER (WHERE x.totales_distintos > 1) AS secciones_total_discordante,
       COUNT(*) FILTER (WHERE x.ln_distintas > 1) AS secciones_ln_discordante,
       COUNT(*) FILTER (WHERE x.totales_no_nulos = 0) AS secciones_sin_total
FROM (
    SELECT election_id, section_id,
           COUNT(DISTINCT total_votes) AS totales_distintos,
           COUNT(DISTINCT nominal_list) AS ln_distintas,
           COUNT(total_votes) AS totales_no_nulos
    FROM electoral.section_result
    GROUP BY election_id, section_id
) x
JOIN electoral.election e ON e.election_id = x.election_id
WHERE e.election_year IN (2018, 2021, 2024)
GROUP BY e.election_year, e.election_type
ORDER BY e.election_year, e.election_type;

-- Casos semilla. La comparación oficial se hará con fuente y modalidad explícitas.
SELECT '03_casos_semilla' AS bloque,
       e.election_year, e.election_type, s.section_code,
       p.party_code, r.votes, r.total_votes,
       r.nominal_list, r.participation_pct
FROM electoral.section_result r
JOIN electoral.election e ON e.election_id = r.election_id
JOIN electoral.party p ON p.party_id = r.party_id
JOIN territorial.section s ON s.section_id = r.section_id
WHERE (e.election_year = 2024 AND e.election_type = 'G' AND s.section_code = '1')
   OR (e.election_year = 2024 AND e.election_type = 'P' AND s.section_code = '1150')
   OR (e.election_year = 2021 AND e.election_type = 'DL' AND s.section_code = '1080')
   OR (e.election_year = 2021 AND e.election_type = 'A' AND s.section_code = '1404')
ORDER BY e.election_year, e.election_type, s.section_code, p.party_code;

-- Secciones que el ETL legado pudo omitir por falta de identidad territorial.
-- El conteo de 97 casillas históricas de Día D pertenece a otra tabla;
-- no debe confundirse con filas electorales de este resultado.
SELECT '04_secciones_especiales_en_tabla_territorial' AS bloque,
       COUNT(*) AS secciones_9000_o_mayores,
       MIN(section_code) AS primera_clave,
       MAX(section_code) AS ultima_clave
FROM territorial.section
WHERE CASE WHEN section_code ~ '^[0-9]+$'
           THEN section_code::integer >= 9000
           ELSE FALSE END;
