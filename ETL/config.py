"""
Stores all paths and database settings here so that the
rest of the project imports them instead of hardcoding values.
"""

SERVER = r"JANEY-JESHEN"
DATABASE = "WalmartBI"

RAW_DATA = r"C:\Users\janen\OneDrive\Desktop\walmart"

CALENDAR_CSV = fr"{RAW_DATA}\calendar.csv"
PRICES_CSV = fr"{RAW_DATA}\sell_prices.csv"
SALES_CSV = fr"{RAW_DATA}\sales_train_validation.csv"

CHUNK_SIZE = 500

SQL_BATCH_SIZE = 250