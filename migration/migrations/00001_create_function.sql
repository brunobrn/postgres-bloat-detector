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

CREATE OR REPLACE AGGREGATE dba.array_accum(anyelement) (
    SFUNC = array_append,
    STYPE = anyarray ,
    FINALFUNC_MODIFY = READ_ONLY,
    INITCOND = '{}',
    MFINALFUNC_MODIFY = READ_ONLY
);

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
