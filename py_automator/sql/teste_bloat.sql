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
  
 -- depois cria a tablea para testar bloat
 
 select concat(create_table_1, tables.tablespace_orig, create_table_2) from repack.tables where relname = 'public.oban_jobs'
 



-- comparar tamanho

--  pegar o tamanho da tabela original diminuir pela de testes e dividir pela original e multiplicar por 100

select  (sum(pg_catalog.pg_table_size('oban_jobs')-pg_catalog.pg_table_size('repack.table_66067'))/pg_catalog.pg_table_size('oban_jobs'))*100 as size_difference

 --
	drop table repack.table_66067


	CREATE TYPE public.oban_job_state AS ENUM ('available', 'scheduled', 'executing', 'retryable', 'completed', 'discarded', 'cancelled');
	CREATE SERVER foreigndb_fdw FOREIGN DATA WRAPPER postgres_fdw OPTIONS (host 'panda-notifications-4d3e2afe.cexop9zvz2f9.us-east-1.rds.amazonaws.com', port '5432', dbname 'panda_notifications');
	CREATE USER MAPPING FOR dba_pg_tools_username SERVER foreigndb_fdw OPTIONS (user 'panda_notifications_dbapy', password '123456789');
	GRANT USAGE ON FOREIGN SERVER foreigndb_fdw TO dba_pg_tools_username;
	CREATE SCHEMA fdw;
	IMPORT FOREIGN SCHEMA public LIMIT TO (oban_jobs) FROM SERVER foreigndb_fdw INTO fdw;
	CREATE TABLE repack.table_66067 WITH (fillfactor=50, oids = false) TABLESPACE pg_default AS SELECT id,queue,worker,args,errors,attempt,max_attempts,inserted_at,scheduled_at,attempted_at,completed_at,attempted_by,discarded_at,priority,tags,meta,cancelled_at,state FROM ONLY fdw.oban_jobs;
	-- select  pg_catalog.pg_table_size('repack.table_66067')
	
	-- drop table  repack.table_66067 