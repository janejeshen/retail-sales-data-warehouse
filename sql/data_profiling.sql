Use WalmartBI;
GO
 

--Understand the contents and quality of staging data
-- before building the warehouse.

-- Counting number of rows
SELECT
    'stg_sales' AS TableName,
    COUNT(*) AS RowsCount
FROM staging.stg_sales

UNION ALL

SELECT
    'stg_calendar',
    COUNT(*)
FROM staging.stg_calendar

UNION ALL

SELECT
    'stg_sell_prices',
    COUNT(*)
FROM staging.stg_sell_prices;

--Noted that the data is more than expected so am verifying the uniqueness
--Checking the uniqueness in sales
SELECT
    COUNT(*) AS TotalRows,
    COUNT(DISTINCT CONCAT(
        id, '|',
        item_id, '|',
        dept_id, '|',
        cat_id, '|',
        store_id, '|',
        state_id, '|',
        d, '|',
        units_sold
    )) AS DistinctRows
FROM staging.stg_sales;

--Checking the uniqueness in sell price 
SELECT
    COUNT(*) AS TotalRows,
    COUNT(DISTINCT CONCAT(
        store_id, '|',
        item_id, '|',
        wm_yr_wk, '|',
        sell_price
    )) AS DistinctRows
FROM staging.stg_sell_prices;

--Checking the uniqueness in calendar
SELECT
    COUNT(*) AS TotalRows,
    COUNT(DISTINCT d) AS DistinctRows
FROM staging.stg_calendar;



--Checking nulls in Sales
SELECT
	SUM(CASE WHEN id IS NULL THEN 1 ELSE 0 END) AS Null_ID,
	SUM(CASE WHEN item_id IS NULL THEN 1 ELSE 0 END) AS Null_ItemID,
	SUM(CASE WHEN dept_id IS NULL THEN 1 ELSE 0 END) AS Null_DeptID,
	SUM(CASE WHEN cat_id IS NULL THEN 1 ELSE 0 END) AS Null_Category,
	 SUM(CASE WHEN store_id IS NULL THEN 1 ELSE 0 END) AS Null_StoreID,
    SUM(CASE WHEN state_id IS NULL THEN 1 ELSE 0 END) AS Null_StateID,
    SUM(CASE WHEN d IS NULL THEN 1 ELSE 0 END) AS Null_DateID,
    SUM(CASE WHEN units_sold IS NULL THEN 1 ELSE 0 END) AS Null_UnitsSold
FROM staging.stg_sales;
