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

CREATE TABLE IF NOT EXISTS dba.schema_migration
(
	migration_version integer
);

insert into dba.schema_migration(migration_version) values (0);