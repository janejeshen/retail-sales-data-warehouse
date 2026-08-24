# ETL Testing & Validation Report
**Project:** Walmart Retail Sales Data Warehouse

**Dataset:** [M5 Forecasting – Walmart Retail Sales](https://www.kaggle.com/competitions/m5-forecasting-accuracy/data)

**Database:** WalmartBI

**Database Platform:** Microsoft SQL Server

**ETL Tool:** Python, Pandas, SQLAlchemy, PyODBC

**Validation Tool:** Jupyter Notebook

**Testing Notebook:** validate_staging_etl.ipynb

**ETL Layer Tested:** Source - Staging


## 1. EXECUTIVE SUMMARY
This report documents testing and validation that was performed on the ETL pipeline for the Walmart retail sales data warehouse project.

The purpose of testing was to verify that the walmart source datasets were correctly loaded into the SQL Server staging layer and that the transformations that were performed during the loading process did not introduce missing records, duplicated values, invalid values or any referential integrity issues.

The three source datasets that wer tested are:
- `calendar.csv`
- `sell_prices.csv`
- `sales_train_validation.csv`

The validations covered include:
- Source file availability
- Source dataset structure
- Row counts
- Column counts
- Schema validation
- Duplicate records
- NULL values
- Invalid dates
- Invalid price values
- Price business-key duplicates
- Sales identifier integrity
- Sales transformation logic
- Sales staging row counts
- Sales duplicate id + d combinations
- Calendar-to-sales referential integrity
- ETL staging table existence

A total of 41 validation checks were executed.

- Checks executed : 41
- Passed : 40
- Failed : 1


## 2. Project Objective
The objective of this project is to build a retail sales data warehouse using the Walmart M5dataset.

The project follows a data engineering and business intelligence workflow:

`Walmart CSV Files -> Python ETL -> Data Cleaning ->Data Warehouse -> Power BI`

The staging layer acts as the initial landing area for the source data before cleaning, transformation, dimensional modelling anf loading into the data warehouse.

## 3. Data Sources
The ETL pipeline uses 3 primary datasets

### 3.1 Calendar dataset
The calendar dataset contains information about the dates represented by the walmart sales data.
The source contains:
- Date
- Walmart Week
- Weekday
- Day of week number
- Month
- Year
- Day identifier
- Event information
- Snap Indicators

The Source validation reported:
- ROWS: 1969
- Columns: 14
- Duplicated: 0

### 3.2 Sell PRice Dataset
The sell price dataset contains information about the pricing of products by store and Walmart week.
The source contains four columns that is:
- store_id
- item_id
- wm_yr_wk
- sell_price

The source validation reported:
- Rows : 6,841,121
- Columns : 4
- Duplicates : 0

### 3.3 Sales Dataset
The sales dataset contains historical daily sales across walmart stores.
The source contains:
- 6 identifier columns
- 1,913 daily sales columns

The source validation reported:
- Rows : 30,490
- Total columns : 1,919
- Daily columns : 1,913

The sales dataset is originally stored in a wide format.

## 4. ETL Architecture

```text
SOURCE
│   |──────────┼──────────┐
│   │          │          │
▼   ▼          ▼          ▼
Calendar     Prices     Sales
  CSV         CSV        CSV
│   │          │          │
│   └──────────┼──────────┘
▼
Python ETL
│   ┌──────────┼──────────┐
▼   ▼          ▼          ▼
Cleaning   Unpivoting  Validation
│   │          │          │
│   └──────────┼──────────┘
▼
SQL SERVER
│
STAGING LAYER
│
▼
DATA WAREHOUSE
│
▼
POWER BI
```

## 5. ETL Technologies
The pipeline uses the following technologies:
1. Python	ETL processing
2. Pandas	CSV reading and transformation
3. SQLAlchemy	Database connectivity
4. PyODBC	SQL Server connectivity
5. Microsoft SQL Server	Staging and warehouse database
6. Jupyter Notebook	Data validation
7. Git/GitHub	Version control
8. Power BI	Business intelligence and visualization


## 6. Staging Layer
The SQL Server staging schema is: `Staging`

The primary staging tables are: 
- staging.stg_calendar
- staging.stg_sell_prices
- staging.stg_sales

The staging layer is intentionally kept separate from the final warehouse.

Its purpose is to provide a controlled landing area where source data can be:

- Loaded
- Inspected
- Validated
- Cleaned
- Transformed
- Prepared for warehouse loading

## 7.ETL Load Strategy
The pipeline uses python to load the large Walmart datasets and the large files are processed in chunks instead of loading the entire dataset into memory.
For example the sales data is processed in chunks of products and transformed from wide to a long format using `melt()` function in pandas. 

The process is conceptually:

``` text
Read chunk
     ↓
Unpivot sales columns
     ↓
Clean identifiers
     ↓
Convert sales values
     ↓
Remove non-positive sales
     ↓
Remove duplicates
     ↓
Insert into SQL Server
     ↓
Process next chunk
```

This approach reduces memory pressure and avoids relying on the sql server import wizard for the large sales dataset.

## 8. ETL Batch Control
The pipeline also uses an ETL load-history table (staging.etl_load history).

This table is used to track ETL batches and prevent accidental repeated loading of the same dataset. The batch process records information such as:
- Dataset name
- Source file
- Batch ID
- Load start time
- Load end time
- Status
- Number of rows loaded
- Error information

The batch-control mechanism is intended to prevent duplicate loads when the same ETL process is executed more than once.

## 9. Testing Objectives
The ETL testing process was designed to answer the following questions:
1. Completeness - Did all required source records reach the staging layer?
2. Accuracy - Were values loaded without unintended changes?
3. Consistency - Are the source and staging schemas consistent with the ETL design.
4. Uniqueness - Were duplicate records introduced during the load?
5. Validity - Are dates, prices, sales values, and identifiers valid?
6. Referential Integrity - Do sales day identifiers correspond to valid calendar records?
7. Transformation Accuracy - Did the wide-to-long sales transformation produce the expected results?
8. Load Safety - Can the ETL process prevent accidental duplicate batch loads?

## 10. Validation Tests Performed
A total of 41 validation checks were executed.

### 10.1 Source File Validation
The following source files were checked for availability:

```text
calendar.csv
sell_prices.csv
sales_train_validation.csv
```

All required source files were available.

## 11. Calendar Validation
The calendar source was tested for:
- Row count
- Column count
- Schema
- Duplicate rows
- Required-field NULLs
- Invalid dates
- Unique day identifiers

The calendar dataset passed all validation checks.

## 12.Sell Price Validation
The sell-price source was tested for:
- Row count
- Column count
- Schema
- Duplicate rows
- Required NULLs
- Invalid Walmart week values
- Invalid prices
- Negative prices
- Duplicate business keys

The sell-price source passed all validation checks.

## 13. Sale Source Validation
The sales source was tested for:
- Number of records
- Number of daily columns
- Total number of columns
- Duplicate rows
- Duplicate sales identifiers
- NULL identifiers
- Required identifier columns

The sales source structure passed all validation checks.

## 14. Sales Transformation Validation
The sales dataset is transformed from wide format into long format.

The source contains: `30,490 product/store records` and `1,913 daily sales columns`

The ETL process creates records containing:
```text 
id
item_id
dept_id
cat_id
store_id
state_id
d
units_sold
```

The transformation also applies the following logic:

1. Normalize text identifiers.
2. Convert sales values to numeric/integer values.
3. Replace missing sales values with zero where applicable.
4. Remove non-positive sales records.
5. Remove duplicates.
6. Load the resulting records into staging.stg_sales.

The validation notebook calculated the transformed sales observation count and compared it against the staging table.

## 15. Staging Row-Count Validation
The source files were compared with the SQL Server staging tables:

- Calendar: 1,969 source rows = 1,969 staging rows - PASS

- Sell Prices: 6,841,121 source rows = 6,841,121 staging rows - PASS

- Sales: 18,550,276 expected rows = 18,550,276 staging rows - PASS

All source data was loaded successfully with the expected row counts.