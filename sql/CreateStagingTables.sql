USE WalmartBI;
GO

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


-- Create the ETL history table
CREATE TABLE staging.etl_load_history
(
    load_id INT IDENTITY(1,1) PRIMARY KEY,
    -- Name of the dataset being loaded
    dataset_name VARCHAR(100) NOT NULL,

    -- Original source file
    source_file VARCHAR(500) NOT NULL,

    -- Unique identifier for this particular batch
    batch_id VARCHAR(100) NOT NULL,

    -- Number of rows successfully loaded
    rows_loaded BIGINT NULL,

    -- When the load started
    load_started DATETIME2 NULL,

    -- When the load finished
    load_completed DATETIME2 NULL,

    -- RUNNING, SUCCESS, or FAILED
    status VARCHAR(20) NOT NULL,

    -- Stores an error message if the batch fails
    error_message VARCHAR(MAX) NULL,

    -- When this history record was created
    created_at DATETIME2 NOT NULL
        DEFAULT SYSDATETIME(),

    -- Prevent the same dataset + batch from being registered twice
    CONSTRAINT UQ_ETL_DATASET_BATCH
        UNIQUE (dataset_name, batch_id)
);
GO
-- Verifying
SELECT *
FROM staging.etl_load_history;

/*
Register the existing M5 sales load.
*/

INSERT INTO staging.etl_load_history
(
    dataset_name,
    source_file,
    batch_id,
    rows_loaded,
    load_started,
    load_completed,
    status
)
VALUES
(
    'sales',
    'sales_train_validation.csv',
    'M5_VALIDATION_001',
    18550276,
    SYSDATETIME(),
    SYSDATETIME(),
    'SUCCESS'
);

USE WalmartBI;
GO

SELECT *
FROM staging.etl_load_history;