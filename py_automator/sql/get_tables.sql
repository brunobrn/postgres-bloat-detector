-- primeiro pegar o tamanho da tabela ativa
SELECT 
-- 	n.nspname as "Schema",
--   c.relname as "Name",
--   CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized view' WHEN 'i' THEN 'index' WHEN 'S' THEN 'sequence' WHEN 's' THEN 'special' WHEN 't' THEN 'TOAST table' WHEN 'f' THEN 'foreign table' WHEN 'p' THEN 'partitioned table' WHEN 'I' THEN 'partitioned index' END as "Type",
--   pg_catalog.pg_get_userbyid(c.relowner) as "Owner",
--   CASE c.relpersistence WHEN 'p' THEN 'permanent' WHEN 't' THEN 'temporary' WHEN 'u' THEN 'unlogged' END as "Persistence",
--   am.amname as "Access method",
  pg_catalog.pg_size_pretty(pg_catalog.pg_table_size(c.oid)) as "Size"
--  ,  pg_catalog.obj_description(c.oid, 'pg_class') as "Description"
FROM pg_catalog.pg_class c
     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
     LEFT JOIN pg_catalog.pg_am am ON am.oid = c.relam
WHERE c.relkind IN ('r','p','v','m','S','f','')
      AND n.nspname <> 'pg_catalog'
      AND n.nspname !~ '^pg_toast'
      AND n.nspname <> 'information_schema'
  AND pg_catalog.pg_table_is_visible(c.oid)
  and c.relname = 'oban_jobs'; --720
  
 -- depois 

SELECT * INTO oban_jobs_bloat FROM oban_jobs;
ALTER TABLE IF EXISTS public.oban_jobs_bloat
    SET (FILLFACTOR=50);
	
	vacuum full oban_jobs_bloat --576
	
	drop table oban_jobs_bloat

SELECT pg_get_indexdef('oban_jobs_queue_state_priority_scheduled_at_id_index'::regclass);
  
SELECT c2.relname, i.indisprimary, i.indisunique, i.indisclustered, i.indisvalid, pg_catalog.pg_get_indexdef(i.indexrelid, 0, true),
  pg_catalog.pg_get_constraintdef(con.oid, true), contype, condeferrable, condeferred, i.indisreplident, c2.reltablespace
FROM pg_catalog.pg_class c, pg_catalog.pg_class c2, pg_catalog.pg_index i
  LEFT JOIN pg_catalog.pg_constraint con ON (conrelid = i.indrelid AND conindid = i.indexrelid AND contype IN ('p','u','x'))
WHERE c.oid = '66067' AND c.oid = i.indrelid AND i.indexrelid = c2.oid
ORDER BY i.indisprimary DESC, c2.relname;


CREATE INDEX oban_jobs_args_index_bloat ON public.oban_jobs_bloat USING gin (args);
CREATE INDEX oban_jobs_meta_index_bloat ON public.oban_jobs_bloat USING gin (meta);
CREATE INDEX oban_jobs_queue_state_priority_scheduled_at_id_index_bloat ON public.oban_jobs_bloat USING btree (queue, state, priority, scheduled_at, id);
CREATE UNIQUE INDEX oban_jobs_pkey_bloat ON public.oban_jobs_bloat USING btree (id);

SELECT c.relchecks, c.relkind, c.relhasindex, c.relhasrules, c.relhastriggers, c.relrowsecurity, c.relforcerowsecurity, false AS relhasoids, c.relispartition, pg_catalog.array_to_string(c.reloptions || array(select 'toast.' || x from pg_catalog.unnest(tc.reloptions) x), ', ')
, c.reltablespace, CASE WHEN c.reloftype = 0 THEN '' ELSE c.reloftype::pg_catalog.regtype::pg_catalog.text END, c.relpersistence, c.relreplident, am.amname
FROM pg_catalog.pg_class c
 LEFT JOIN pg_catalog.pg_class tc ON (c.reltoastrelid = tc.oid)
LEFT JOIN pg_catalog.pg_am am ON (c.relam = am.oid)
WHERE c.oid = '66067';


SELECT 
-- 	n.nspname as "Schema",
  c.relname as "Name"
--   ,CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized view' WHEN 'i' THEN 'index' WHEN 'S' THEN 'sequence' WHEN 's' THEN 'special' WHEN 't' THEN 'TOAST table' WHEN 'f' THEN 'foreign table' WHEN 'p' THEN 'partitioned table' WHEN 'I' THEN 'partitioned index' END as "Type",
--   pg_catalog.pg_get_userbyid(c.relowner) as "Owner",
--   c2.relname as "Table",
--   CASE c.relpersistence WHEN 'p' THEN 'permanent' WHEN 't' THEN 'temporary' WHEN 'u' THEN 'unlogged' END as "Persistence",
--   am.amname as "Access method",
--   pg_catalog.pg_size_pretty(pg_catalog.pg_table_size(c.oid)) as "Size",
--   pg_catalog.obj_description(c.oid, 'pg_class') as "Description"
FROM pg_catalog.pg_class c
     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
     LEFT JOIN pg_catalog.pg_am am ON am.oid = c.relam
     LEFT JOIN pg_catalog.pg_index i ON i.indexrelid = c.oid
     LEFT JOIN pg_catalog.pg_class c2 ON i.indrelid = c2.oid
WHERE c.relkind IN ('i','I','s','')
  AND c.relname OPERATOR(pg_catalog.~) '^(oban_.*)$' COLLATE pg_catalog.default
  AND pg_catalog.pg_table_is_visible(c.oid)
  and c2.relname = 'oban_jobs';
  
  

  
SELECT c.relchecks, c.relkind, c.relhasindex, c.relhasrules, c.relhastriggers, c.relrowsecurity, c.relforcerowsecurity, false AS relhasoids, c.relispartition, pg_catalog.array_to_string(c.reloptions || array(select 'toast.' || x from pg_catalog.unnest(tc.reloptions) x), ', ')
, c.reltablespace, CASE WHEN c.reloftype = 0 THEN '' ELSE c.reloftype::pg_catalog.regtype::pg_catalog.text END, c.relpersistence, c.relreplident, am.amname
FROM pg_catalog.pg_class c
 LEFT JOIN pg_catalog.pg_class tc ON (c.reltoastrelid = tc.oid)
LEFT JOIN pg_catalog.pg_am am ON (c.relam = am.oid)
WHERE c.oid = '66067';





-- comparar tamanho

-- primeiro pegar o tamanho da tabela ativa

select  sum(pg_catalog.pg_table_size('oban_jobs')-pg_catalog.pg_table_size('oban_jobs_bloat'))/pg_catalog.pg_table_size('oban_jobs') as size_difference


