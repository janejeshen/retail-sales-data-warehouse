"""
Creating the staging schema and tables.
"""

from database import engine

sql = """

IF NOT EXISTS (
SELECT * FROM sys.schemas WHERE name='staging')

EXEC('CREATE SCHEMA staging');

IF OBJECT_ID('staging.stg_calendar') IS NULL
CREATE TABLE staging.stg_calendar
(
    [date] DATE,
    wm_yr_wk INT,
    weekday VARCHAR(20),
    wday INT,
    month INT,
    year INT,
    d VARCHAR(10),
    event_name_1 VARCHAR(50),
    event_type_1 VARCHAR(50),
    event_name_2 VARCHAR(50),
    event_type_2 VARCHAR(50),
    snap_CA BIT,
    snap_TX BIT,
    snap_WI BIT
);

IF OBJECT_ID('staging.stg_sell_prices') IS NULL
CREATE TABLE staging.stg_sell_prices
(
    store_id VARCHAR(20),
    item_id VARCHAR(50),
    wm_yr_wk INT,
    sell_price DECIMAL(10,2)
);

IF OBJECT_ID('staging.stg_sales') IS NULL
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

"""

with engine.begin() as conn:
    conn.exec_driver_sql(sql)

print("Staging tables created.")