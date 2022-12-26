CREATE ROLE panda_notifications_dbapy WITH
  LOGIN
  NOSUPERUSER
  INHERIT
  CREATEDB
  CREATEROLE
  NOREPLICATION
  VALID UNTIL 'infinity';

GRANT panda_notifications_dbapy TO postgres;

ALTER ROLE panda_notifications_dbapy PASSWORD 'xxxxxx';

ALTER ROLE panda_notifications_dbapy SET search_path TO repack,public;

-- View: repack.tables

-- DROP VIEW repack.tables;

CREATE OR REPLACE VIEW repack.get_ddl_tables
 AS
 SELECT repack.oid2text(r.oid) AS relname,
    r.oid AS relid,
    r.reltoastrelid,
        CASE
            WHEN r.reltoastrelid = 0::oid THEN 0::oid
            ELSE ( SELECT pg_index.indexrelid
               FROM pg_index
              WHERE pg_index.indrelid = r.reltoastrelid AND pg_index.indisvalid)
        END AS reltoastidxid,
    n.nspname AS schemaname,
    pk.indexrelid AS pkid,
    ck.indexrelid AS ckid,
    repack.get_create_index_type(pk.indexrelid, ('repack.pk_'::text || r.oid)::name) AS create_pktype,
    ((((('CREATE TABLE repack.log_'::text || r.oid) || ' (id bigserial PRIMARY KEY, pk repack.pk_'::text) || r.oid) || ', row '::text) || repack.oid2text(r.oid)) || ')'::text AS create_log,
    repack.get_create_trigger(r.oid, pk.indexrelid) AS create_trigger,
    repack.get_enable_trigger(r.oid) AS enable_trigger,
    ((('CREATE TABLE repack.table_'::text || r.oid) || ' WITH ('::text) || repack.get_storage_param(r.oid)) || ') TABLESPACE '::text AS create_table_1,
    COALESCE(quote_ident(s.spcname::text), 'pg_default'::text) AS tablespace_orig,
    ((' AS SELECT '::text || repack.get_columns_for_create_as(r.oid)) || ' FROM ONLY '::text) || repack.oid2text(r.oid) AS create_table_2,
    (((('INSERT INTO repack.table_'::text || r.oid) || ' SELECT '::text) || repack.get_columns_for_create_as(r.oid)) || ' FROM ONLY '::text) || repack.oid2text(r.oid) AS copy_data,
    repack.get_alter_col_storage(r.oid) AS alter_col_storage,
    repack.get_drop_columns(r.oid, 'repack.table_'::text || r.oid) AS drop_columns,
    'DELETE FROM repack.log_'::text || r.oid AS delete_log,
    ('LOCK TABLE '::text || repack.oid2text(r.oid)) || ' IN ACCESS EXCLUSIVE MODE'::text AS lock_table,
    repack.get_order_by(ck.indexrelid, r.oid) AS ckey,
    ('SELECT * FROM repack.log_'::text || r.oid) || ' ORDER BY id LIMIT $1'::text AS sql_peek,
    ('INSERT INTO repack.table_'::text || r.oid) || ' VALUES ($1.*)'::text AS sql_insert,
    (('DELETE FROM repack.table_'::text || r.oid) || ' WHERE '::text) || repack.get_compare_pkey(pk.indexrelid, '$1'::text) AS sql_delete,
    (((('UPDATE repack.table_'::text || r.oid) || ' SET '::text) || repack.get_assign(r.oid, '$2'::text)) || ' WHERE '::text) || repack.get_compare_pkey(pk.indexrelid, '$1'::text) AS sql_update,
    ('DELETE FROM repack.log_'::text || r.oid) || ' WHERE id IN ('::text AS sql_pop
   FROM pg_class r
     LEFT JOIN pg_class t ON r.reltoastrelid = t.oid
     LEFT JOIN repack.primary_keys pk ON r.oid = pk.indrelid
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
  WHERE r.relkind = 'r'::"char" AND r.relpersistence = 'p'::"char" AND (n.nspname <> ALL (ARRAY['pg_catalog'::name, 'information_schema'::name])) AND n.nspname !~~ 'pg\_temp\_%'::text;

ALTER TABLE repack.tables OWNER TO panda_notifications_dbapy;

