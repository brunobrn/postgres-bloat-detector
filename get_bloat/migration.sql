-- drop schema dba cascade


-- cRIAR ROLE VIA ANSIBLE
-- drop role if exists dbapy_database_username cascade;
-- CREATE ROLE dbapy_database_username WITH
--   LOGIN
--   NOSUPERUSER
--   INHERIT
--   CREATEDB
--   CREATEROLE
--   NOREPLICATION
--   VALID UNTIL 'infinity';

-- ALTER ROLE dbapy_database_username PASSWORD '123456';
-- GRANT CREATE ON DATABASE panda_notifications TO dbapy_database_username;
-- GRANT SELECT ON ALL TABLES IN schema pix TO dbapy_database_username;
-- GRANT SELECT ON ALL TABLES IN schema public TO dbapy_database_username;
-- GRANT SELECT ON ALL TABLES IN schema dba TO dbapy_database_username;
-- GRANT SELECT ON TABLE dba.primary_keys TO dbapy_database_username;
-- GRANT ALL ON TABLE dba.primary_keys TO dbapy_database_username;
-- grant usage on schema pix to dbapy_database_username; -- criar grant automatico para qualquer owner
-- grant usage on schema dba to dbapy_database_username;
-- grant usage on schema public to dbapy_database_username;
-- grant insert on dba.bloat_monitor to dbapy_database_username;


CREATE SCHEMA IF NOT EXISTS dba;

CREATE TABLE IF NOT EXISTS dba.bloat_monitor
(
    id bigint NOT NULL GENERATED  ALWAYS AS IDENTITY,
	table_name varchar(100),
	schema varchar(25),
	size_original bigint,
	size_k8s bigint,
	percentage_diff numeric,
	inserted_at timestamp without time zone NOT NULL,
    PRIMARY KEY (id)
);

ALTER TABLE IF EXISTS dba.bloat_monitor OWNER to dbapy_database_username;

CREATE TABLE IF NOT EXISTS dba.schema_migration
(
	migration_version integer
);

ALTER TABLE IF EXISTS dba.schema_migration OWNER to dbapy_database_username;

ALTER ROLE dbapy_database_username SET search_path TO dba,public;

-- FUNCTION: dba.oid2text(oid)

-- DROP FUNCTION IF EXISTS dba.oid2text(oid);

CREATE OR REPLACE FUNCTION dba.oid2text(
	oid)
    RETURNS text
    LANGUAGE 'sql'
    COST 100
    STABLE STRICT PARALLEL UNSAFE
    SET search_path=pg_catalog
AS $BODY$
	SELECT textin(regclassout($1));
$BODY$;

ALTER FUNCTION dba.oid2text(oid) OWNER TO dbapy_database_username;

-- FUNCTION: dba.get_storage_param(oid)

-- DROP FUNCTION IF EXISTS dba.get_storage_param(oid);

CREATE OR REPLACE FUNCTION dba.get_storage_param(
	oid)
    RETURNS text
    LANGUAGE 'sql'
    COST 100
    STABLE STRICT PARALLEL UNSAFE
AS $BODY$
SELECT array_to_string(array_agg(param), ', ')
FROM (
    -- table storage parameter
    SELECT unnest(reloptions) as param
    FROM pg_class
    WHERE oid = $1
    UNION ALL
    -- TOAST table storage parameter
    SELECT ('toast.' || unnest(reloptions)) as param
    FROM (
        SELECT reltoastrelid from pg_class where oid = $1
         ) as t,
        pg_class as c
    WHERE c.oid = t.reltoastrelid
    UNION ALL
    -- table oid
    SELECT 'oids = ' ||
        CASE WHEN false
            THEN 'true'
            ELSE 'false'
        END
    FROM pg_class
    WHERE oid = $1

    ) as t
$BODY$;

ALTER FUNCTION dba.get_storage_param(oid) OWNER TO dbapy_database_username;

-- Aggregate: array_accum;

-- DROP AGGREGATE IF EXISTS dba.array_accum(anyelement);

CREATE OR REPLACE AGGREGATE dba.array_accum(anyelement) (
    SFUNC = array_append,
    STYPE = anyarray ,
    FINALFUNC_MODIFY = READ_ONLY,
    INITCOND = '{}',
    MFINALFUNC_MODIFY = READ_ONLY
);

alter AGGREGATE  dba.array_accum(anyelement) OWNER to dbapy_database_username;

-- FUNCTION: dba.get_columns_for_create_as(oid)

-- DROP FUNCTION IF EXISTS dba.get_columns_for_create_as(oid);

CREATE OR REPLACE FUNCTION dba.get_columns_for_create_as(
	oid)
    RETURNS text
    LANGUAGE 'sql'
    COST 100
    STABLE STRICT PARALLEL UNSAFE
AS $BODY$
SELECT array_to_string(dba.array_accum(c), ',') FROM (SELECT
	CASE WHEN attisdropped
		THEN 'NULL::integer AS ' || quote_ident(attname)
		ELSE quote_ident(attname)
	END AS c
FROM pg_attribute
WHERE attrelid = $1 AND attnum > 0 ORDER BY attnum
) AS COL
$BODY$;

ALTER FUNCTION dba.get_columns_for_create_as(oid) OWNER TO dbapy_database_username;

-- View: repack.primary_keys

-- DROP VIEW repack.primary_keys;

CREATE OR REPLACE VIEW dba.primary_keys
 AS
 SELECT tmp.indrelid,
    (dba.array_accum(tmp.indexrelid))[1] AS indexrelid
   FROM ( SELECT pg_index.indrelid,
            pg_index.indexrelid
           FROM pg_index
          WHERE pg_index.indisunique AND pg_index.indisvalid AND pg_index.indpred IS NULL AND (0 <> ALL (pg_index.indkey::smallint[])) AND NOT (EXISTS ( SELECT 1
                   FROM pg_attribute
                  WHERE pg_attribute.attrelid = pg_index.indrelid AND (pg_attribute.attnum = ANY (pg_index.indkey::smallint[])) AND NOT pg_attribute.attnotnull))
          ORDER BY pg_index.indrelid, pg_index.indisprimary DESC, pg_index.indnatts, pg_index.indkey) tmp
  GROUP BY tmp.indrelid;

ALTER TABLE dba.primary_keys OWNER TO dbapy_database_username;

-- View: dba.get_ddl_tables

-- DROP VIEW dba.get_ddl_tables;

CREATE OR REPLACE VIEW dba.get_ddl_tables
 AS
 SELECT dba.oid2text(r.oid) AS relname,
    r.oid AS relid,
    n.nspname AS schemaname,
    pk.indexrelid AS pkid,
    ck.indexrelid AS ckid,
    ((('CREATE TABLE dba.table_'::text || r.oid) || ' WITH ('::text) || dba.get_storage_param(r.oid)) || ') TABLESPACE '::text AS create_table_1,
    COALESCE(quote_ident(s.spcname::text), 'pg_default'::text) AS tablespace_orig,
    ((' AS SELECT '::text || dba.get_columns_for_create_as(r.oid)) || ' FROM ONLY fdw.'::text) || split_part(dba.oid2text(r.oid), '.', 2) AS create_table_2
   FROM pg_class r
     LEFT JOIN pg_class t ON r.reltoastrelid = t.oid
     LEFT JOIN dba.primary_keys pk ON r.oid = pk.indrelid
     LEFT JOIN ( SELECT cki.indexrelid,
            cki.indrelid,
            cki.indnatts,
            cki.indnkeyatts,
            cki.indisunique,
            cki.indisprimary,
            cki.indisexclusion,
            cki.indimmediate,
            cki.indisclustered,
            cki.indisvalid,
            cki.indcheckxmin,
            cki.indisready,
            cki.indislive,
            cki.indisreplident,
            cki.indkey,
            cki.indcollation,
            cki.indclass,
            cki.indoption,
            cki.indexprs,
            cki.indpred
           FROM pg_index cki,
            pg_class ckt
          WHERE cki.indisvalid AND cki.indexrelid = ckt.oid AND cki.indisclustered AND ckt.relam = 403::oid) ck ON r.oid = ck.indrelid
     LEFT JOIN pg_namespace n ON n.oid = r.relnamespace
     LEFT JOIN pg_tablespace s ON s.oid = r.reltablespace
  WHERE r.relkind = 'r'::"char" AND r.relpersistence = 'p'::"char" 
  AND (n.nspname <> ALL (ARRAY['pg_catalog'::name, 'information_schema'::name])) 
  AND n.nspname !~~ 'pg\_temp\_%'::text;

ALTER VIEW dba.get_ddl_tables OWNER TO dbapy_database_username;

---------------


insert into dba.schema_migration(migration_version) values (1);