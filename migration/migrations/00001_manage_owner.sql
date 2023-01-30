ALTER TABLE IF EXISTS dba.bloat_monitor OWNER to dba_pg_tools_username;

ALTER ROLE dba_pg_tools_username SET search_path TO dba,public;

ALTER TABLE IF EXISTS dba.schema_migration OWNER to dba_pg_tools_username;

ALTER FUNCTION dba.oid2text(oid) OWNER TO dba_pg_tools_username;

ALTER FUNCTION dba.get_storage_param(oid) OWNER TO dba_pg_tools_username;

ALTER AGGREGATE  dba.array_accum(anyelement) OWNER to dba_pg_tools_username;

ALTER FUNCTION dba.get_columns_for_create_as(oid) OWNER TO dba_pg_tools_username;

ALTER TABLE dba.primary_keys OWNER TO dba_pg_tools_username;

ALTER VIEW dba.get_ddl_tables OWNER TO dba_pg_tools_username;
