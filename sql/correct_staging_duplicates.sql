USE WalmartBI;
GO

/*
File: 02_reset_staging.sql

Purpose:
    Resest the staging layer after an accidental duplicate ETL load.

NOTE:
    This permanently removes all data from the staging tables.
    Only run this when you intentionally want to perform a
    complete staging reload.

Tables affected:
    - staging.stg_calendar
    - staging.stg_sell_prices
    - staging.stg_sales
*/

PRINT 'Starting staging reset...';

-- Clear sales

TRUNCATE TABLE staging.stg_sales;

PRINT 'stg_sales truncated.';


-- Clear sell prices

TRUNCATE TABLE staging.stg_sell_prices;

PRINT 'stg_sell_prices truncated.';


-- Clear calendar

TRUNCATE TABLE staging.stg_calendar;

PRINT 'stg_calendar truncated.';


-- 4. Verifying

SELECT
    'stg_sales' AS TableName,
    COUNT(*) AS RowsCount
FROM staging.stg_sales

UNION ALL

SELECT
    'stg_sell_prices',
    COUNT(*)
FROM staging.stg_sell_prices

UNION ALL

SELECT
    'stg_calendar',
    COUNT(*)
FROM staging.stg_calendar;

PRINT 'Staging reset completed.';

--SELECT TOP 5 * FROM staging.stg_calendar