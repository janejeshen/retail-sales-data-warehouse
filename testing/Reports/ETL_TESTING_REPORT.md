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

| Result | Count |
| Passed | 41 |


## 2. Project Objective
The objective of this project is to build a retail sales data warehouse using the Walmart M5dataset.

The project follows a data engineering and business intelligence workflow:
Walmart CSV Files -> Python ETL -> Data Cleaning ->Data Warehouse -> Power BI

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

### 3.2 Sell P
