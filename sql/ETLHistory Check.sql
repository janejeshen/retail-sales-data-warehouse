USE WalmartBI;
GO

SELECT
    load_id,
    dataset_name,
    source_file,
    batch_id,
    rows_loaded,
    status,
    load_started,
    load_completed
FROM staging.etl_load_history
ORDER BY load_id;