"""
Main Walmart BI ETL pipeline.
The pipeline is safe to run repeatedly because each dataset
is identified by a unique batch ID.
"""

from load_calendar import load_calendar
from load_prices import load_prices
from load_sales import load_sales


def run_etl():
    print("=" * 70)
    print("WALMART BI ETL PIPELINE")
    print("=" * 70)

    # CALENDAR
    load_calendar(
        batch_id="M5_CALENDAR_001"
    )

    # SELL PRICES
    load_prices(
        batch_id="M5_PRICES_001"
    )

    # SALES
    load_sales(
        batch_id="M5_VALIDATION_001"
    )


    print("\nETL pipeline finished.")


if __name__ == "__main__":
    run_etl()