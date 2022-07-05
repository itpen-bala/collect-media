--
-- PostgreSQL database dump
--

-- Dumped from database version 14.4 (Debian 14.4-1.pgdg110+1)
-- Dumped by pg_dump version 14.4 (Debian 14.4-1.pgdg110+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: image_files; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.image_files (
    id integer NOT NULL,
    uuid uuid NOT NULL,
    url character varying(2048) NOT NULL,
    ftp_path character varying(2048) NOT NULL,
    format character varying(20) NOT NULL,
    width smallint NOT NULL,
    height smallint NOT NULL,
    image_size smallint[] NOT NULL,
    file_size integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL
);


ALTER TABLE public.image_files OWNER TO postgres;

--
-- Name: image_files_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.image_files_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.image_files_id_seq OWNER TO postgres;

--
-- Name: image_files_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.image_files_id_seq OWNED BY public.image_files.id;


--
-- Name: image_files id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.image_files ALTER COLUMN id SET DEFAULT nextval('public.image_files_id_seq'::regclass);


--
-- Data for Name: image_files; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.image_files (id, uuid, url, ftp_path, format, width, height, image_size, file_size, created_at, updated_at) FROM stdin;
\.


--
-- Name: image_files_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.image_files_id_seq', 2, true);


--
-- Name: image_files image_files_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.image_files
    ADD CONSTRAINT image_files_pkey PRIMARY KEY (id);


--
-- Name: TABLE image_files; Type: ACL; Schema: public; Owner: postgres
--

GRANT ALL ON TABLE public.image_files TO media_user;


--
-- Name: SEQUENCE image_files_id_seq; Type: ACL; Schema: public; Owner: postgres
--

GRANT SELECT,USAGE ON SEQUENCE public.image_files_id_seq TO media_user;


--
-- PostgreSQL database dump complete
--

