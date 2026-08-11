/*
File Purpose:Remove duplicate records accidentally introduced into the staging layer 
after the ETL process was executed twice.

Affected Tables:
    1. staging.stg_calendar
    2. staging.stg_sell_prices
    3. staging.stg_sales

Cause:The Python ETL uses INSERT/APPEND behavior. Running the ETL multiple times appended 
the same source data to the staging tables instead of replacing or skipping existing records.

Expected Result: Restore each staging table to one unique copy of the source data.

Note:This script should NOT be used as a routine ETL process. 
It is a data correction script for the duplicate-load incident.
*/

USE WalmartBI;
GO

/*

CORRECTING stg_calendar

The calendar table should contain one record per calendar date.
We keep one copy of each unique record and remove duplicates.
*/


WITH DuplicateCalendar AS
(
    SELECT
        *,
        ROW_NUMBER() OVER
        (
            PARTITION BY
                d,
                [date],
                wm_yr_wk,
                weekday,
                wday,
                month,
                year,
                event_name_1,
                event_type_1,
                event_name_2,
                event_type_2,
                snap_CA,
                snap_TX,
                snap_WI
            ORDER BY
                (SELECT NULL)
        ) AS rn
    FROM staging.stg_calendar
)
DELETE FROM DuplicateCalendar
WHERE rn > 1;

PRINT 'Duplicate calendar records removed.';
GO
