USE WalmartBI;
GO

-- stg_sell_prices PROFILING

-- 1.ROW COUNT
SELECT COUNT(*) AS row_counts
FROM staging.stg_sell_prices;

-- 2. column information
SELECT COLUMN_NAME,DATA_TYPE,CHARACTER_MAXIMUM_LENGTH,IS_NULLABLE
FROM INFORMATION_SCHEMA.columns
WHERE table_schema='staging' AND table_name='stg_sell_prices';

-- 3. NULL PROFILING
SELECT COUNT(*) AS total_row_count,
		SUM(CASE WHEN store_id IS NULL THEN 1 ELSE 0 END) AS store_id_nulls,
		SUM(CASE WHEN item_id IS NULL THEN 1 ELSE 0 END) AS item_id_nulls,
		SUM(CASE WHEN wm_yr_wk IS NULL THEN 1 ELSE 0 END) AS wm_yr_wk_nulls,
		SUM(CASE WHEN sell_price IS NULL THEN 1 ELSE 0 END) AS sell_price_nulls
FROM staging.stg_sell_prices;

-- 4. DISTINCT VALUES
SELECT COUNT(DISTINCT store_id) AS distinct_store_id,
		COUNT(DISTINCT item_id) AS distinct_item_id,
		COUNT(DISTINCT wm_yr_wk) AS distinct_wm_yr_wk,
		COUNT(DISTINCT sell_price) AS distinct_sell_price
FROM staging.stg_sell_prices;

-- 5. store_id duplicates
SELECT store_id,COUNT(*) AS duplicate_count
FROM staging.stg_sell_prices
GROUP BY store_id
HAVING COUNT(*)>1
ORDER BY duplicate_count DESC;

-- 6. item_id duplicates
SELECT item_id,COUNT(*) AS duplicate_count
FROM staging.stg_sell_prices
GROUP BY item_id
HAVING COUNT(*)>1
ORDER BY duplicate_count DESC;

--7. wm_yr_wk  and sell_price RANGE
SELECT MIN(wm_yr_wk) AS min_wm_yr_wk,
		MAX(wm_yr_wk) AS max_wm_yr_wk,

		MIN(sell_price) AS min_sell_price,
		MAX(sell_price) AS max_sell_price
FROM staging.stg_sell_prices

--8. Zero/negative prices
SELECT *
FROM staging.stg_sell_prices
where sell_price<=0;

--9. uniqueness check		
SELECT store_id, item_id,wm_yr_wk,count(*) as record_count
FROM staging.stg_sell_prices
GROUP BY store_id,item_id,wm_yr_wk
HAVING COUNT(*) > 1;

--10.Suspicious price values
-- getting price distribution
WITH price_stats AS (
    SELECT
        sell_price,
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY sell_price) OVER () AS q1,
        PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY sell_price) OVER () AS median_price,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY sell_price) OVER () AS q3
    FROM staging.stg_sell_prices),

stats AS (
    SELECT
        COUNT(*) AS total_records,
        MIN(sell_price) AS minimum_price,
        MAX(sell_price) AS maximum_price,
        AVG(sell_price) AS average_price,
        MAX(q1) AS q1,
        MAX(median_price) AS median_price,
        MAX(q3) AS q3
    FROM price_stats),

-- CALCULATING IQR AND BOUNDARIES
boundaries AS (SELECT *, q3-q1 as iqr,
                q1-1.5*(q3-q1) as lower_bound,
                q3+1.5*(q3-q1) as upper_bound
                FROM stats)

--  profiling summary
SELECT
    total_records,
    ROUND(minimum_price, 2) AS minimum_price,
    ROUND(maximum_price, 2) AS maximum_price,
    ROUND(average_price, 2) AS average_price,
    ROUND(q1, 2) AS q1,
    ROUND(median_price, 2) AS median_price,
    ROUND(q3, 2) AS q3,
    ROUND(iqr, 2) AS iqr,
    ROUND(lower_bound, 2) AS lower_bound,
    ROUND(upper_bound, 2) AS upper_bound
FROM boundaries;

-- finding how many suspicious prices there are
WITH price_stats AS (
    SELECT
        PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY sell_price) OVER () AS q1,
        PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY sell_price) OVER () AS q3
    FROM staging.stg_sell_prices
),
boundaries AS (
    SELECT
        MAX(q1) AS q1,
        MAX(q3) AS q3
    FROM price_stats
),
limits AS (
    SELECT
        q1,
        q3,
        q1 - 1.5 * (q3 - q1) AS lower_bound,
        q3 + 1.5 * (q3 - q1) AS upper_bound
    FROM boundaries
)
SELECT
    COUNT(*) AS suspicious_records,
    SUM(CASE
          WHEN sell_price < lower_bound THEN 1
          ELSE 0
        END) AS below_lower_bound,
    SUM(CASE
           WHEN sell_price > upper_bound THEN 1
           ELSE 0
        END) AS above_upper_bound
FROM staging.stg_sell_prices
CROSS JOIN limits
WHERE sell_price < lower_bound OR sell_price > upper_bound;

-- Find what percentage the suspicious records take
WITH price_stats AS (
    SELECT
        PERCENTILE_CONT(0.25)
            WITHIN GROUP (ORDER BY sell_price) OVER () AS q1,
        PERCENTILE_CONT(0.75)
            WITHIN GROUP (ORDER BY sell_price) OVER () AS q3
    FROM staging.stg_sell_prices
),
boundaries AS (
    SELECT
        MAX(q1) AS q1,
        MAX(q3) AS q3
    FROM price_stats
),
limits AS (
    SELECT
        q3 + 1.5 * (q3 - q1) AS upper_bound
    FROM boundaries
)
SELECT
    COUNT(*) AS total_records,

    SUM(
        CASE
            WHEN sell_price > upper_bound THEN 1
            ELSE 0
        END
    ) AS above_upper_bound,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN sell_price > upper_bound THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS percentage_above_upper_bound
FROM staging.stg_sell_prices
CROSS JOIN limits;

--the distribution of those suspicious prices
SELECT
    CASE
        WHEN sell_price <= 5 THEN '0 - 5'
        WHEN sell_price <= 10 THEN '5 - 10'
        WHEN sell_price <= 20 THEN '10 - 20'
        WHEN sell_price <= 50 THEN '20 - 50'
        WHEN sell_price <= 100 THEN '50 - 100'
        WHEN sell_price <= 500 THEN '100 - 500'
        ELSE '500+'
    END AS price_range,
    COUNT(*) AS record_count
FROM staging.stg_sell_prices
GROUP BY
    CASE
        WHEN sell_price <= 5 THEN '0 - 5'
        WHEN sell_price <= 10 THEN '5 - 10'
        WHEN sell_price <= 20 THEN '10 - 20'
        WHEN sell_price <= 50 THEN '20 - 50'
        WHEN sell_price <= 100 THEN '50 - 100'
        WHEN sell_price <= 500 THEN '100 - 500'
        ELSE '500+'
    END
ORDER BY MIN(sell_price);

--check the actual highest prices
SELECT TOP 30
    store_id,
    item_id,
    wm_yr_wk,
    sell_price
FROM staging.stg_sell_prices
ORDER BY sell_price DESC;

