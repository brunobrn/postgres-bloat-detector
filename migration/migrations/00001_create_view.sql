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