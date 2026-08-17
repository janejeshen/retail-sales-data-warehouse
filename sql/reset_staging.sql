USE WalmartBI;
GO

/*
Purpose: Resets the staging layer after an accidental duplicate ETL load.

Note:This script runs inside a transaction.
    - Use COMMIT TRANSACTION to permanently apply the reset.
    - Use ROLLBACK TRANSACTION to undo the reset.

Tables affected:
    - staging.stg_calendar
    - staging.stg_sell_prices
    - staging.stg_sales
    - staging.etl_load_history
*/

SET XACT_ABORT ON;

BEGIN TRY

    PRINT 'Starting staging reset transaction...';

    BEGIN TRANSACTION;

    -- Capturing row counts BEFORE reset
    PRINT 'Row counts BEFORE reset:';

    SELECT 'stg_sales' AS TableName,COUNT(*) AS RowsCount
    FROM staging.stg_sales

    UNION ALL

    SELECT 'stg_sell_prices', COUNT(*)
    FROM staging.stg_sell_prices

    UNION ALL

    SELECT 'stg_calendar',COUNT(*)
    FROM staging.stg_calendar

    UNION ALL

    SELECT 'etl_load_history', COUNT(*)
    FROM staging.etl_load_history;

    -- Clearing sales
    PRINT 'Truncating stg_sales...';
    TRUNCATE TABLE staging.stg_sales;

    -- Clearing sell prices
    PRINT 'Truncating stg_sell_prices...';

    TRUNCATE TABLE staging.stg_sell_prices;

    -- Clearing calendar
    PRINT 'Truncating stg_calendar...';
    TRUNCATE TABLE staging.stg_calendar;

    -- reset batch history
    DELETE FROM staging.etl_load_history;

    -- Verifying inside transaction
    PRINT 'Row counts AFTER reset:';

    SELECT 'stg_sales' AS TableName, COUNT(*) AS RowsCount
    FROM staging.stg_sales

    UNION ALL

    SELECT 'stg_sell_prices',COUNT(*)
    FROM staging.stg_sell_prices

    UNION ALL

    SELECT 'stg_calendar', COUNT(*)
    FROM staging.stg_calendar
    
    UNION ALL 
    
    SELECT 'etl_load_history', COUNT(*)
    FROM staging.etl_load_history;


    PRINT 'Staging reset completed successfully.';
    PRINT 'The transaction is still open.';


    COMMIT TRANSACTION;
    PRINT 'Staging reset COMMITTED.';

    -- ROLLBACK TRANSACTION;
    -- PRINT 'Staging reset ROLLED BACK.';

END TRY

BEGIN CATCH

    IF @@TRANCOUNT > 0
        ROLLBACK TRANSACTION;

    PRINT 'ERROR: Staging reset failed.';
    PRINT ERROR_MESSAGE();

    THROW;

END CATCH;

