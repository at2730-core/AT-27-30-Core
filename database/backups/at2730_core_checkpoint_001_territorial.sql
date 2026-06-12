--
-- PostgreSQL database dump
--

\restrict faFqoKNVvbOrNQSRLreahjc7QRWMHklbQvoUMVcVDx19nVILDV3AwevyyIFcu4r

-- Dumped from database version 18.4
-- Dumped by pg_dump version 18.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: analytics; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA analytics;


ALTER SCHEMA analytics OWNER TO postgres;

--
-- Name: audit; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA audit;


ALTER SCHEMA audit OWNER TO postgres;

--
-- Name: election_day; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA election_day;


ALTER SCHEMA election_day OWNER TO postgres;

--
-- Name: electoral; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA electoral;


ALTER SCHEMA electoral OWNER TO postgres;

--
-- Name: field; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA field;


ALTER SCHEMA field OWNER TO postgres;

--
-- Name: metadata; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA metadata;


ALTER SCHEMA metadata OWNER TO postgres;

--
-- Name: socioeconomico; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA socioeconomico;


ALTER SCHEMA socioeconomico OWNER TO postgres;

--
-- Name: spatial; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA spatial;


ALTER SCHEMA spatial OWNER TO postgres;

--
-- Name: territorial; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA territorial;


ALTER SCHEMA territorial OWNER TO postgres;

--
-- Name: topology; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA topology;


ALTER SCHEMA topology OWNER TO postgres;

--
-- Name: SCHEMA topology; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA topology IS 'PostGIS Topology schema';


--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- Name: postgis_topology; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis_topology WITH SCHEMA topology;


--
-- Name: EXTENSION postgis_topology; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis_topology IS 'PostGIS topology spatial types and functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: distrito_federal; Type: TABLE; Schema: territorial; Owner: postgres
--

CREATE TABLE territorial.distrito_federal (
    distrito_federal_id integer NOT NULL,
    df_code character varying(10),
    df_name character varying(150) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE territorial.distrito_federal OWNER TO postgres;

--
-- Name: distrito_federal_distrito_federal_id_seq; Type: SEQUENCE; Schema: territorial; Owner: postgres
--

CREATE SEQUENCE territorial.distrito_federal_distrito_federal_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE territorial.distrito_federal_distrito_federal_id_seq OWNER TO postgres;

--
-- Name: distrito_federal_distrito_federal_id_seq; Type: SEQUENCE OWNED BY; Schema: territorial; Owner: postgres
--

ALTER SEQUENCE territorial.distrito_federal_distrito_federal_id_seq OWNED BY territorial.distrito_federal.distrito_federal_id;


--
-- Name: distrito_local; Type: TABLE; Schema: territorial; Owner: postgres
--

CREATE TABLE territorial.distrito_local (
    distrito_local_id integer NOT NULL,
    dl_code character varying(10),
    dl_name character varying(150) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE territorial.distrito_local OWNER TO postgres;

--
-- Name: distrito_local_distrito_local_id_seq; Type: SEQUENCE; Schema: territorial; Owner: postgres
--

CREATE SEQUENCE territorial.distrito_local_distrito_local_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE territorial.distrito_local_distrito_local_id_seq OWNER TO postgres;

--
-- Name: distrito_local_distrito_local_id_seq; Type: SEQUENCE OWNED BY; Schema: territorial; Owner: postgres
--

ALTER SEQUENCE territorial.distrito_local_distrito_local_id_seq OWNED BY territorial.distrito_local.distrito_local_id;


--
-- Name: municipio; Type: TABLE; Schema: territorial; Owner: postgres
--

CREATE TABLE territorial.municipio (
    municipio_id integer NOT NULL,
    municipio_code character varying(10),
    municipio_name character varying(150) NOT NULL,
    state character varying(100) DEFAULT 'Guanajuato'::character varying,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE territorial.municipio OWNER TO postgres;

--
-- Name: municipio_municipio_id_seq; Type: SEQUENCE; Schema: territorial; Owner: postgres
--

CREATE SEQUENCE territorial.municipio_municipio_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE territorial.municipio_municipio_id_seq OWNER TO postgres;

--
-- Name: municipio_municipio_id_seq; Type: SEQUENCE OWNED BY; Schema: territorial; Owner: postgres
--

ALTER SEQUENCE territorial.municipio_municipio_id_seq OWNED BY territorial.municipio.municipio_id;


--
-- Name: section; Type: TABLE; Schema: territorial; Owner: postgres
--

CREATE TABLE territorial.section (
    section_id bigint NOT NULL,
    section_code character varying(20) NOT NULL,
    municipio_id integer,
    distrito_local_id integer,
    distrito_federal_id integer,
    section_type character varying(50),
    current_status character varying(50) DEFAULT 'active'::character varying,
    source_dataset character varying(255),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE territorial.section OWNER TO postgres;

--
-- Name: section_history; Type: TABLE; Schema: territorial; Owner: postgres
--

CREATE TABLE territorial.section_history (
    section_history_id bigint NOT NULL,
    section_id bigint NOT NULL,
    valid_from date,
    valid_to date,
    section_code character varying(20),
    previous_section_code character varying(20),
    previous_section_id bigint,
    reason character varying(100),
    geometry_status character varying(50),
    notes text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE territorial.section_history OWNER TO postgres;

--
-- Name: section_history_section_history_id_seq; Type: SEQUENCE; Schema: territorial; Owner: postgres
--

CREATE SEQUENCE territorial.section_history_section_history_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE territorial.section_history_section_history_id_seq OWNER TO postgres;

--
-- Name: section_history_section_history_id_seq; Type: SEQUENCE OWNED BY; Schema: territorial; Owner: postgres
--

ALTER SEQUENCE territorial.section_history_section_history_id_seq OWNED BY territorial.section_history.section_history_id;


--
-- Name: section_section_id_seq; Type: SEQUENCE; Schema: territorial; Owner: postgres
--

CREATE SEQUENCE territorial.section_section_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE territorial.section_section_id_seq OWNER TO postgres;

--
-- Name: section_section_id_seq; Type: SEQUENCE OWNED BY; Schema: territorial; Owner: postgres
--

ALTER SEQUENCE territorial.section_section_id_seq OWNED BY territorial.section.section_id;


--
-- Name: distrito_federal distrito_federal_id; Type: DEFAULT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.distrito_federal ALTER COLUMN distrito_federal_id SET DEFAULT nextval('territorial.distrito_federal_distrito_federal_id_seq'::regclass);


--
-- Name: distrito_local distrito_local_id; Type: DEFAULT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.distrito_local ALTER COLUMN distrito_local_id SET DEFAULT nextval('territorial.distrito_local_distrito_local_id_seq'::regclass);


--
-- Name: municipio municipio_id; Type: DEFAULT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.municipio ALTER COLUMN municipio_id SET DEFAULT nextval('territorial.municipio_municipio_id_seq'::regclass);


--
-- Name: section section_id; Type: DEFAULT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.section ALTER COLUMN section_id SET DEFAULT nextval('territorial.section_section_id_seq'::regclass);


--
-- Name: section_history section_history_id; Type: DEFAULT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.section_history ALTER COLUMN section_history_id SET DEFAULT nextval('territorial.section_history_section_history_id_seq'::regclass);


--
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: distrito_federal; Type: TABLE DATA; Schema: territorial; Owner: postgres
--

COPY territorial.distrito_federal (distrito_federal_id, df_code, df_name, created_at) FROM stdin;
\.


--
-- Data for Name: distrito_local; Type: TABLE DATA; Schema: territorial; Owner: postgres
--

COPY territorial.distrito_local (distrito_local_id, dl_code, dl_name, created_at) FROM stdin;
\.


--
-- Data for Name: municipio; Type: TABLE DATA; Schema: territorial; Owner: postgres
--

COPY territorial.municipio (municipio_id, municipio_code, municipio_name, state, created_at) FROM stdin;
\.


--
-- Data for Name: section; Type: TABLE DATA; Schema: territorial; Owner: postgres
--

COPY territorial.section (section_id, section_code, municipio_id, distrito_local_id, distrito_federal_id, section_type, current_status, source_dataset, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: section_history; Type: TABLE DATA; Schema: territorial; Owner: postgres
--

COPY territorial.section_history (section_history_id, section_id, valid_from, valid_to, section_code, previous_section_code, previous_section_id, reason, geometry_status, notes, created_at) FROM stdin;
\.


--
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology.topology (id, name, srid, "precision", hasz, useslargeids) FROM stdin;
\.


--
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: postgres
--

COPY topology.layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
\.


--
-- Name: distrito_federal_distrito_federal_id_seq; Type: SEQUENCE SET; Schema: territorial; Owner: postgres
--

SELECT pg_catalog.setval('territorial.distrito_federal_distrito_federal_id_seq', 1, false);


--
-- Name: distrito_local_distrito_local_id_seq; Type: SEQUENCE SET; Schema: territorial; Owner: postgres
--

SELECT pg_catalog.setval('territorial.distrito_local_distrito_local_id_seq', 1, false);


--
-- Name: municipio_municipio_id_seq; Type: SEQUENCE SET; Schema: territorial; Owner: postgres
--

SELECT pg_catalog.setval('territorial.municipio_municipio_id_seq', 1, false);


--
-- Name: section_history_section_history_id_seq; Type: SEQUENCE SET; Schema: territorial; Owner: postgres
--

SELECT pg_catalog.setval('territorial.section_history_section_history_id_seq', 1, false);


--
-- Name: section_section_id_seq; Type: SEQUENCE SET; Schema: territorial; Owner: postgres
--

SELECT pg_catalog.setval('territorial.section_section_id_seq', 1, false);


--
-- Name: topology_id_seq; Type: SEQUENCE SET; Schema: topology; Owner: postgres
--

SELECT pg_catalog.setval('topology.topology_id_seq', 1, false);


--
-- Name: distrito_federal distrito_federal_pkey; Type: CONSTRAINT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.distrito_federal
    ADD CONSTRAINT distrito_federal_pkey PRIMARY KEY (distrito_federal_id);


--
-- Name: distrito_local distrito_local_pkey; Type: CONSTRAINT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.distrito_local
    ADD CONSTRAINT distrito_local_pkey PRIMARY KEY (distrito_local_id);


--
-- Name: municipio municipio_pkey; Type: CONSTRAINT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.municipio
    ADD CONSTRAINT municipio_pkey PRIMARY KEY (municipio_id);


--
-- Name: section_history section_history_pkey; Type: CONSTRAINT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.section_history
    ADD CONSTRAINT section_history_pkey PRIMARY KEY (section_history_id);


--
-- Name: section section_pkey; Type: CONSTRAINT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.section
    ADD CONSTRAINT section_pkey PRIMARY KEY (section_id);


--
-- Name: section uq_section_code; Type: CONSTRAINT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.section
    ADD CONSTRAINT uq_section_code UNIQUE (section_code);


--
-- Name: idx_section_code; Type: INDEX; Schema: territorial; Owner: postgres
--

CREATE INDEX idx_section_code ON territorial.section USING btree (section_code);


--
-- Name: idx_section_history_previous; Type: INDEX; Schema: territorial; Owner: postgres
--

CREATE INDEX idx_section_history_previous ON territorial.section_history USING btree (previous_section_id);


--
-- Name: idx_section_history_reason; Type: INDEX; Schema: territorial; Owner: postgres
--

CREATE INDEX idx_section_history_reason ON territorial.section_history USING btree (reason);


--
-- Name: idx_section_history_section; Type: INDEX; Schema: territorial; Owner: postgres
--

CREATE INDEX idx_section_history_section ON territorial.section_history USING btree (section_id);


--
-- Name: idx_section_municipio; Type: INDEX; Schema: territorial; Owner: postgres
--

CREATE INDEX idx_section_municipio ON territorial.section USING btree (municipio_id);


--
-- Name: idx_section_status; Type: INDEX; Schema: territorial; Owner: postgres
--

CREATE INDEX idx_section_status ON territorial.section USING btree (current_status);


--
-- Name: section fk_section_df; Type: FK CONSTRAINT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.section
    ADD CONSTRAINT fk_section_df FOREIGN KEY (distrito_federal_id) REFERENCES territorial.distrito_federal(distrito_federal_id);


--
-- Name: section fk_section_dl; Type: FK CONSTRAINT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.section
    ADD CONSTRAINT fk_section_dl FOREIGN KEY (distrito_local_id) REFERENCES territorial.distrito_local(distrito_local_id);


--
-- Name: section_history fk_section_history_previous; Type: FK CONSTRAINT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.section_history
    ADD CONSTRAINT fk_section_history_previous FOREIGN KEY (previous_section_id) REFERENCES territorial.section(section_id);


--
-- Name: section_history fk_section_history_section; Type: FK CONSTRAINT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.section_history
    ADD CONSTRAINT fk_section_history_section FOREIGN KEY (section_id) REFERENCES territorial.section(section_id);


--
-- Name: section fk_section_municipio; Type: FK CONSTRAINT; Schema: territorial; Owner: postgres
--

ALTER TABLE ONLY territorial.section
    ADD CONSTRAINT fk_section_municipio FOREIGN KEY (municipio_id) REFERENCES territorial.municipio(municipio_id);


--
-- PostgreSQL database dump complete
--

\unrestrict faFqoKNVvbOrNQSRLreahjc7QRWMHklbQvoUMVcVDx19nVILDV3AwevyyIFcu4r

