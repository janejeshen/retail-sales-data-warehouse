"""
Runs the complete ETL pipeline.
"""

import create_staging_tables
import load_calendar
import load_prices
import load_sales

print("=" * 60)
print("ETL completed successfully.")
print("=" * 60)