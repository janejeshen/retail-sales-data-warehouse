USE WalmartBI;
GO

-- stg_calendar PROFILING

-- 1.ROW COUNT

SELECT COUNT(*) AS row_count
FROM staging.stg_calendar;

-- 2.COLUMN INFORMATION

SELECT COLUMN_NAME,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH,IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = 'staging' AND TABLE_NAME = 'stg_calendar'
ORDER BY ORDINAL_POSITION

-- 3. NULL PROFILING

SELECT COUNT(*) AS total_rows,
		SUM(CASE WHEN date IS NULL THEN 1 ELSE 0 END) AS date_nulls,
		SUM(CASE WHEN wm_yr_wk IS NULL THEN 1 ELSE 0 END) AS wm_yr_wk_nulls,
		SUM(CASE WHEN weekday IS NULL THEN 1 ELSE 0 END) AS weekday_nulls,
		SUM(CASE WHEN wday IS NULL THEN 1 ELSE 0 END) AS wday_nulls,
		SUM(CASE WHEN month IS NULL THEN 1 ELSE 0 END) AS month_nulls,
		SUM(CASE WHEN year IS NULL THEN 1 ELSE 0 END) AS year_nulls,
        SUM(CASE WHEN d IS NULL THEN 1 ELSE 0 END) AS d_nulls,
        SUM(CASE WHEN event_name_1 IS NULL THEN 1 ELSE 0 END) AS event_name_1_nulls,
        SUM(CASE WHEN event_type_1 IS NULL THEN 1 ELSE 0 END) AS event_type_1_nulls,
        SUM(CASE WHEN event_name_2 IS NULL THEN 1 ELSE 0 END) AS event_name_2_nulls,
        SUM(CASE WHEN event_type_2 IS NULL THEN 1 ELSE 0 END) AS event_type_2_nulls,
        SUM(CASE WHEN snap_CA IS NULL THEN 1 ELSE 0 END) AS snap_CA_nulls,
        SUM(CASE WHEN snap_TX IS NULL THEN 1 ELSE 0 END) AS snap_TX_nulls,
        SUM(CASE WHEN snap_WI IS NULL THEN 1 ELSE 0 END) AS snap_WI_nulls
FROM staging.stg_calendar;

-- 4. DISTINCT VALUES
SELECT COUNT(DISTINCT date) AS distinct_dates,
        COUNT(DISTINCT wm_yr_wk) AS distinct_weeks,
        COUNT(DISTINCT weekday) AS distinct_weekdays,
        COUNT(DISTINCT wday) AS distinct_wday_values,
        COUNT(DISTINCT month) AS distinct_months,
        COUNT(DISTINCT year) AS distinct_years,
        COUNT(DISTINCT d) AS distinct_day_keys
FROM staging.stg_calendar;

-- 5. DUPLICATE DATE CHECK
SELECT date, COUNT(*) AS duplicate_count
FROM staging.stg_calendar
GROUP BY date
HAVING COUNT(*) >1
ORDER BY duplicate_count DESC;

-- 6. DUPLICATE DAY-KEY CHECK
SELECT d,COUNT(*) AS duplicate_count
FROM staging.stg_calendar
GROUP BY d
HAVING COUNT(*) >1
ORDER BY duplicate_count DESC;

-- 7. DATE RANGE
SELECT MIN(date) AS minimum_date,
        MAX(date) AS maximum_date,
        COUNT(DISTINCT date) AS distinct_dates
FROM staging.stg_calendar;

--8 NUMERIC RANGES
SELECT MIN(wday) AS min_wday,
        MAX(wday) AS max_wday,

        MIN(month) AS min_month,
        MAX(month) AS max_month,

        MIN(year) AS min_year,
        MAX(year) AS max_year
FROM staging.stg_calendar;

-- BUSINESS RULE CHECKS
 
--9. Invalid months
SELECT *
FROM staging.stg_calendar
WHERE month NOT BETWEEN 1 AND 12;

--10. invalid weekday numbers
SELECT *
FROM staging.stg_calendar
WHERE wday NOT BETWEEN 1 AND 7;

--11. SNAP_CA DISTRIBUTION
SELECT snap_CA, COUNT(*) AS row_count
FROM staging.stg_calendar
GROUP BY snap_CA
ORDER BY snap_CA;

--12. snap_TX Distribution
SELECT snap_TX,COUNT(*) AS row_count
FROM staging.stg_calendar
GROUP BY snap_TX
ORDER BY snap_TX;

--13. SNAP_WI Distribution
SELECT snap_WI, COUNT(*) AS row_count
FROM staging.stg_calendar
GROUP BY snap_WI
ORDER BY snap_WI;

-- Text consistency

-- 14. WEEKDAY VALUES
SELECT weekday,COUNT(*) AS row_counts
FROM staging.stg_calendar
GROUP BY weekday
ORDER BY row_counts DESC;

-- 15. EVENT TYPES
SELECT event_type_1, COUNT(*) AS row_count
FROM staging.stg_calendar
GROUP BY event_type_1
ORDER BY row_count DESC;

-- 16. SECOND EVENT TYPES
SELECT event_type_2,COUNT(*) AS row_count
FROM staging.stg_calendar
GROUP BY event_type_2
ORDER BY row_count;

-- 17. DATE vs WEEKDAY CONSISTENCY
SELECT date,weekday, DATENAME(WEEKDAY,date) AS calculated_weekday
FROM staging.stg_calendar
WHERE weekday <> DATENAME(WEEKDAY,date);