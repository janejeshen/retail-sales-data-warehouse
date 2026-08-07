CREATE TABLE staging.stg_sales
(
    id VARCHAR(50),
    item_id VARCHAR(50),
    dept_id VARCHAR(50),
    cat_id VARCHAR(50),
    store_id VARCHAR(20),
    state_id VARCHAR(10),
    d VARCHAR(10),
    units_sold INT
);

--verifying
SELECT
    s.name AS SchemaName,
    t.name AS TableName
FROM sys.tables t
JOIN sys.schemas s
    ON t.schema_id = s.schema_id
WHERE t.name = 'stg_sales';