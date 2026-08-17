"""
Central configuration for the Walmart BI ETL pipeline.
Keeping configuration in one place to prevent database connection
details and file paths from being duplicated across scripts.
"""

# DATABASE CONFIGURATION

SERVER = r"JANEY-JESHEN"
DATABASE = "WalmartBI"

# SOURCE DATA CONFIGURATION

# Root folder containing the Walmart CSV files.
RAW_DATA_PATH = (r"C:\Users\janen\OneDrive\Desktop\walmart")

CALENDAR_CSV = (rf"{RAW_DATA_PATH}\calendar.csv")

PRICES_CSV = (rf"{RAW_DATA_PATH}\sell_prices.csv")

SALES_CSV = (rf"{RAW_DATA_PATH}\sales_train_validation.csv")


# ETL CONFIGURATION

# Number of products read from the sales CSV at a time.
CHUNK_SIZE = 500

# Number of rows sent to SQL Server per batch.
SQL_BATCH_SIZE = 250

# Dataset names used by the ETL load-history table.
CALENDAR_DATASET = "calendar"
PRICES_DATASET = "sell_prices"
SALES_DATASET = "sales"