"""
Loads sell_prices.csv into staging.stg_sell_prices.
"""

import pandas as pd
from sqlalchemy import types

from database import engine
from config import PRICES_CSV

chunk_size = 250_000

for i, prices in enumerate(pd.read_csv(PRICES_CSV, chunksize=chunk_size), start=1):
    prices.to_sql(
        "stg_sell_prices",
        engine,
        schema="staging",
        if_exists="append",
        index=False,
        dtype={"sell_price": types.DECIMAL(10, 2)}
    )
    print(f"Loaded prices chunk {i} ({len(prices)} rows)")

engine.dispose()

print("Prices loaded.")