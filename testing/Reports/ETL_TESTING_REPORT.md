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